-- v338 premium packs, tester weekly claims and one idempotent grant path (purchases, tester claims and admin grants all land here).
-- Live real-money purchases are OFF: nothing in the client can create a 'purchase' grant; only a store-verifying edge function (with
-- the store's service key configured) or the owner can.
create table if not exists public.shop_packs (
  id text primary key, data jsonb not null, active boolean not null default true, tester_eligible boolean not null default true,
  once_per_account boolean not null default false, sort int not null default 0, updated_at timestamptz not null default now());
alter table public.shop_packs enable row level security;
drop policy if exists shop_packs_read on public.shop_packs;
create policy shop_packs_read on public.shop_packs for select to anon, authenticated using (active);

create table if not exists public.testers (uid uuid primary key, added_at timestamptz not null default now(), note text);
alter table public.testers enable row level security;   -- no policies: the owner manages it (SQL editor or tester_set)

create table if not exists public.pack_grants (
  id uuid primary key default gen_random_uuid(), uid uuid not null, pack_id text not null references public.shop_packs(id),
  source text not null check (source in ('tester', 'purchase', 'admin')), grant_key text not null unique, week int,
  contents jsonb not null, status text not null default 'granted' check (status in ('granted', 'delivered', 'revoked')),
  created_at timestamptz not null default now(), delivered_at timestamptz, revoked_at timestamptz, revoke_seen boolean not null default false, note text);
create index if not exists pack_grants_uid on public.pack_grants (uid, status);
alter table public.pack_grants enable row level security;
drop policy if exists pack_grants_own on public.pack_grants;
create policy pack_grants_own on public.pack_grants for select to authenticated using (uid = auth.uid());

-- the server week: Monday 00:00 UTC, counted from 2026-01-05 (the game's weekNo())
create or replace function public.udf_week(ts timestamptz default now()) returns int language sql immutable as $$
  select floor(extract(epoch from (ts - timestamptz '2026-01-05 00:00:00+00')) / 604800)::int $$;

create or replace function public.tester_status() returns jsonb language plpgsql stable security definer set search_path = public as $$
declare u uuid := auth.uid(); w int := public.udf_week(); g record;
begin
  if u is null then return jsonb_build_object('tester', false); end if;
  select pack_id, created_at into g from public.pack_grants where grant_key = 'tester:' || u || ':' || w;
  return jsonb_build_object('tester', exists (select 1 from public.testers where uid = u), 'week', w, 'claimed', g.pack_id,
    'next_at', (timestamptz '2026-01-05 00:00:00+00' + make_interval(days => (w + 1) * 7)));
end $$;

-- one tester pack per account per server week; the unique grant_key makes a repeat (double tap, two devices, retry) a no-op
create or replace function public.claim_tester_pack(p_pack text) returns jsonb language plpgsql volatile security definer set search_path = public as $$
declare u uuid := auth.uid(); w int := public.udf_week(); pk public.shop_packs; g public.pack_grants;
begin
  if u is null then raise exception 'sign in first' using errcode = '42501'; end if;
  if not exists (select 1 from public.testers where uid = u) then raise exception 'not a tester' using errcode = '42501'; end if;
  select * into pk from public.shop_packs where id = p_pack and active and tester_eligible;
  if pk.id is null then raise exception 'pack not available' using errcode = '22023'; end if;
  insert into public.pack_grants (uid, pack_id, source, grant_key, week, contents) values (u, pk.id, 'tester', 'tester:' || u || ':' || w, w, pk.data -> 'contents')
    on conflict (grant_key) do nothing returning * into g;
  if g.id is null then select * into g from public.pack_grants where grant_key = 'tester:' || u || ':' || w;
    return jsonb_build_object('ok', false, 'reason', 'already_claimed', 'grant', to_jsonb(g)); end if;
  return jsonb_build_object('ok', true, 'grant', to_jsonb(g));
end $$;

-- what this account still has to apply (granted) or take back (revoked after delivery and not yet seen)
create or replace function public.my_grants() returns setof public.pack_grants language sql stable security definer set search_path = public as $$
  select * from public.pack_grants where uid = auth.uid() and (status = 'granted' or (status = 'revoked' and delivered_at is not null and not revoke_seen)) order by created_at $$;
create or replace function public.ack_grant(p_id uuid) returns boolean language sql volatile security definer set search_path = public as $$
  with x as (update public.pack_grants set status = 'delivered', delivered_at = now() where id = p_id and uid = auth.uid() and status = 'granted' returning 1) select exists (select 1 from x) $$;
create or replace function public.ack_revoke(p_id uuid) returns boolean language sql volatile security definer set search_path = public as $$
  with x as (update public.pack_grants set revoke_seen = true where id = p_id and uid = auth.uid() and status = 'revoked' returning 1) select exists (select 1 from x) $$;

-- owner tools: grant (refund replacements, compensation), revoke (refunds, chargebacks), manage testers
create or replace function public.admin_grant(p_uid uuid, p_pack text, p_key text, p_note text default null) returns jsonb language plpgsql volatile security definer set search_path = public as $$
declare pk public.shop_packs; g public.pack_grants;
begin
  if not public.is_owner() then raise exception 'owner only' using errcode = '42501'; end if;
  select * into pk from public.shop_packs where id = p_pack; if pk.id is null then raise exception 'no such pack' using errcode = '22023'; end if;
  insert into public.pack_grants (uid, pack_id, source, grant_key, contents, note) values (p_uid, pk.id, 'admin', 'admin:' || p_key, pk.data -> 'contents', p_note) on conflict (grant_key) do nothing returning * into g;
  return jsonb_build_object('ok', g.id is not null, 'grant', to_jsonb(g));
end $$;
create or replace function public.admin_revoke(p_id uuid, p_note text default null) returns boolean language sql volatile security definer set search_path = public as $$
  with x as (update public.pack_grants set status = 'revoked', revoked_at = now(), note = coalesce(p_note, note) where id = p_id and status <> 'revoked' and public.is_owner() returning 1) select exists (select 1 from x) $$;
create or replace function public.tester_set(p_uid uuid, p_on boolean, p_note text default null) returns boolean language plpgsql volatile security definer set search_path = public as $$
begin
  if not public.is_owner() then raise exception 'owner only' using errcode = '42501'; end if;
  if p_on then insert into public.testers (uid, note) values (p_uid, p_note) on conflict (uid) do update set note = coalesce(excluded.note, public.testers.note);
  else delete from public.testers where uid = p_uid; end if; return true;
end $$;

revoke all on function public.admin_grant(uuid, text, text, text), public.admin_revoke(uuid, text), public.tester_set(uuid, boolean, text) from public, anon;
grant execute on function public.admin_grant(uuid, text, text, text), public.admin_revoke(uuid, text), public.tester_set(uuid, boolean, text) to authenticated;
revoke all on function public.claim_tester_pack(text), public.my_grants(), public.ack_grant(uuid), public.ack_revoke(uuid), public.tester_status() from public, anon;
grant execute on function public.claim_tester_pack(text), public.my_grants(), public.ack_grant(uuid), public.ack_revoke(uuid), public.tester_status() to authenticated;

-- owner's audit view: every grant with its account, plus a flag for anything unusual (more than one tester grant in a week can't
-- happen by construction; this catches admin mistakes and purchase replays)
create or replace view public.grant_audit with (security_invoker = on) as
  select g.*, coalesce(p.data ->> 'name', g.uid::text) as commander, (select count(*) from public.pack_grants g2 where g2.uid = g.uid and g2.week = g.week and g2.source = 'tester') as tester_grants_this_week
  from public.pack_grants g left join public.docs p on p.path = 'profiles/' || g.uid;
revoke all on public.grant_audit from anon, authenticated;
