-- Ultra Deep Field on Supabase: run this whole file once in Supabase → SQL Editor → New query → Run.
-- Safe to run again (it replaces what it made before).
--
-- Every game record is one row in "docs", addressed by a path like the game uses ("planets/p12", "data/users/<you>/save").
-- Row-level security decides who can read and write what, the same rules the Firebase version had, and the save guard
-- keeps saves in order and refuses saves that would wipe out an empire.

create table if not exists public.docs (
  path text primary key,
  col text not null,                       -- the collection: everything before the last "/" ("planets", "data/users/<uid>/backups")
  top text not null,                       -- the first part of the path ("planets", "data", "players")
  id text not null,                        -- the last part of the path
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);
create index if not exists docs_col on public.docs (col);
create index if not exists docs_sh on public.docs (col, ((data->>'sh')));

-- game owners (you): add yourself after signing up once, see the README
create table if not exists public.owners (uid uuid primary key);
alter table public.owners enable row level security;   -- no policies: only the SQL editor can change it

create or replace function public.is_owner() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.owners where uid = auth.uid())
$$;

-- col / top / id always come from the path, so nobody can file a record under someone else's area
create or replace function public.docs_fill() returns trigger language plpgsql set search_path = public as $$
begin
  if new.path is null or new.path !~ '^[^/]+(/[^/]+)+$' then
    raise exception 'bad path %', new.path using errcode = '22023';
  end if;
  new.top := split_part(new.path, '/', 1);
  new.id := regexp_replace(new.path, '^.*/', '');
  new.col := regexp_replace(new.path, '/[^/]*$', '');
  new.updated_at := now();
  return new;
end $$;
drop trigger if exists a_docs_fill on public.docs;
create trigger a_docs_fill before insert or update on public.docs for each row execute function public.docs_fill();

-- the save guard: each save must carry the next number (seq), so a stale copy on another device can't save over newer
-- progress; a save that drops a built-up empire (10+ levels) below half is refused unless the game marks it deliberate
create or replace function public.save_guard() returns trigger language plpgsql set search_path = public as $$
declare os numeric; ns numeric; ol numeric; nl numeric;
begin
  if new.path ~ '^data/users/[^/]+/save$' then
    if old.data ? 'seq' then
      os := coalesce((old.data->>'seq')::numeric, 0); ns := coalesce((new.data->>'seq')::numeric, 0);
      if ns <> os + 1 then raise exception 'save out of order' using errcode = '42501'; end if;
    end if;
    if old.data ? 'lv' then
      ol := coalesce((old.data->>'lv')::numeric, 0); nl := coalesce((new.data->>'lv')::numeric, 0);
      if ol >= 10 and coalesce(new.data->>'shrink', 'false') <> 'true' and nl * 2 < ol then
        raise exception 'save would wipe progress' using errcode = '42501';
      end if;
    end if;
  end if;
  return new;
end $$;
drop trigger if exists b_save_guard on public.docs;
create trigger b_save_guard before update on public.docs for each row execute function public.save_guard();

-- who can do what
alter table public.docs enable row level security;
drop policy if exists docs_read on public.docs;
drop policy if exists docs_add on public.docs;
drop policy if exists docs_change on public.docs;
drop policy if exists docs_remove on public.docs;

create or replace function public.can_read(p text, t text, d jsonb) returns boolean
language sql stable set search_path = public as $$
  select auth.uid() is not null and (
    t in ('planets','occ','inbox','inbound','alliances','assaults','chat','event','galaxy','_locks','players','profiles')
    or (t = 'data' and split_part(p, '/', 3) = auth.uid()::text)
    or (t = 'feedback' and public.is_owner())
    or (t = 'dms' and coalesce(d->'p', '[]'::jsonb) ? auth.uid()::text))
$$;
create or replace function public.can_write(p text, t text, adding boolean) returns boolean
language sql stable set search_path = public as $$
  select auth.uid() is not null and (
    t in ('planets','occ','inbox','inbound','alliances','assaults','chat','event','galaxy','_locks','dms')
    or (t in ('players','profiles') and split_part(p, '/', 2) = auth.uid()::text)
    or (t = 'players' and public.is_owner())
    or (t = 'data' and split_part(p, '/', 3) = auth.uid()::text)
    or (t = 'feedback' and (adding or public.is_owner())))
$$;
create policy docs_read on public.docs for select using (public.can_read(path, top, data));
create policy docs_add on public.docs for insert with check (public.can_write(path, top, true));
create policy docs_change on public.docs for update using (public.can_write(path, top, false)) with check (public.can_write(path, top, false));
create policy docs_remove on public.docs for delete using (public.can_write(path, top, false));
grant select, insert, update, delete on public.docs to authenticated;
revoke all on public.docs from anon;

-- update(): merges nested objects ({gifts:{a:1}} adds gifts.a and keeps the other gifts), returns the merged record
create or replace function public.jsonb_merge_deep(a jsonb, b jsonb) returns jsonb
language sql immutable set search_path = public as $$
  select case when jsonb_typeof(a) = 'object' and jsonb_typeof(b) = 'object' then
    (select coalesce(jsonb_object_agg(k, case when a ? k and b ? k then public.jsonb_merge_deep(a->k, b->k) when b ? k then b->k else a->k end), '{}'::jsonb)
       from (select jsonb_object_keys(a) as k union select jsonb_object_keys(b)) s)
  else b end
$$;
create or replace function public.doc_update(p text, patch jsonb) returns jsonb
language plpgsql security invoker set search_path = public as $$
declare out jsonb;
begin
  update public.docs set data = public.jsonb_merge_deep(data, patch) where path = p returning data into out;
  if not found then raise exception 'not found %', p using errcode = 'P0002'; end if;
  return out;
end $$;

-- a short lease so only one player at a time edits a busy record (the Cube battle, joint strikes, joining the galaxy)
create or replace function public.doc_acquire(p text, holder text, ttl integer, t bigint) returns jsonb
language plpgsql security invoker set search_path = public as $$
declare lp text := '_locks/' || replace(p, '/', '~'); d jsonb; ms integer := least(greatest(coalesce(ttl, 10000), 1000), 60000);
begin
  insert into public.docs (path, col, top, id, data) values (lp, '', '', '', '{}'::jsonb) on conflict (path) do nothing;
  select data into d from public.docs where path = lp for update;
  if d ? 'until' and (d->>'until')::bigint > t and d->>'holder' <> holder then
    return jsonb_build_object('acquired', false, 'holder', d->>'holder', 'until', (d->>'until')::bigint);
  end if;
  update public.docs set data = jsonb_build_object('holder', holder, 'until', t + ms) where path = lp;
  return jsonb_build_object('acquired', true, 'until', t + ms);
end $$;
revoke execute on function public.doc_update(text, jsonb), public.doc_acquire(text, text, integer, bigint), public.is_owner() from public, anon;
grant execute on function public.doc_update(text, jsonb), public.doc_acquire(text, text, integer, bigint), public.is_owner() to authenticated;

-- live updates: every client hears about the records it is allowed to read
do $$ begin
  if not exists (select 1 from pg_publication_tables where pubname = 'supabase_realtime' and schemaname = 'public' and tablename = 'docs') then
    alter publication supabase_realtime add table public.docs;
  end if;
end $$;

-- v325 security pass: the RLS auto-enable event-trigger function is not an API endpoint; is_owner() only for signed-in users
do $$ begin if exists (select 1 from pg_proc where proname = 'rls_auto_enable' and pronamespace = 'public'::regnamespace) then
  revoke execute on function public.rls_auto_enable() from public, anon, authenticated; end if; end $$;
revoke execute on function public.is_owner() from public, anon;
grant execute on function public.is_owner() to authenticated;

-- v333: Academy funnel for the owner (read with the service role / SQL editor; no client access)
create or replace view public.academy_funnel as
with s as (select split_part(path,'/',3) uid, (data->>'json')::jsonb j from docs where path like 'data/users/%/save' and data ? 'json')
select s.uid, coalesce(s.j->>'cname', p.data->>'name') commander, (s.j->'tut'->>'i')::int + 1 as step, s.j->>'faction' faction,
  to_timestamp(((pl.data->>'joined')::bigint)/1000) joined, to_timestamp(((pl.data->>'last')::bigint)/1000) last_seen,
  s.j->'tutT' step_opened, s.j->'tutH' show_me_taps, s.j->'errs' errors, (s.j->>'comeback') comeback, s.j->'tut'->>'k' step_id, s.j->'tutStuck' stuck_hints,
  ((pl.data->>'last')::bigint - (pl.data->>'joined')::bigint) >= 86400000 back_day1, ((pl.data->>'last')::bigint - (pl.data->>'joined')::bigint) >= 7*86400000 back_day7,
  (s.j->>'tutBoostGiven')::int boosts_given
from s left join docs p on p.path='profiles/'||s.uid left join docs pl on pl.path='players/'||s.uid;
alter view public.academy_funnel set (security_invoker = on);
revoke all on public.academy_funnel from anon, authenticated;

-- v483 (multiplayer plan, phase 1): compare-and-set for the shared event records (boss hunts, the Omega Cube, the super bosses).
-- A client reads a record with its version (updated_at) and writes back only if nobody has written since; on a conflict it gets
-- ok=false, re-reads and works its change out again, so two players hitting the same boss at the same moment both land.
-- security invoker: the row rules (can_write) still decide who may write.
create or replace function public.doc_cas(p text, expect timestamptz, d jsonb) returns jsonb
language plpgsql security invoker set search_path = public as $$
declare cur timestamptz; nt timestamptz;
begin
  select updated_at into cur from public.docs where path = p for update;
  if found then
    if expect is null or cur <> expect then return jsonb_build_object('ok', false, 'v', cur); end if;
    update public.docs set data = d where path = p returning updated_at into nt;
  else
    if expect is not null then return jsonb_build_object('ok', false, 'v', null); end if;
    insert into public.docs (path, col, top, id, data) values (p, '', '', '', d) returning updated_at into nt;
  end if;
  return jsonb_build_object('ok', true, 'v', nt);
end $$;
revoke execute on function public.doc_cas(text, timestamptz, jsonb) from public, anon;
grant execute on function public.doc_cas(text, timestamptz, jsonb) to authenticated;

-- v484 (multiplayer plan, phase 2): every boss fight a phone decides is re-run by the settle_fight Edge Function, and the two results
-- are logged here. Only the function (service role) writes; the owner can read it.
create table if not exists public.fight_log (
  id bigserial primary key, at timestamptz not null default now(), uid uuid, kind text, unit text, game_v int,
  ok boolean, client jsonb, server jsonb, ms real);
create index if not exists fight_log_at on public.fight_log (at desc);
alter table public.fight_log enable row level security;
drop policy if exists fight_log_owner_read on public.fight_log;
create policy fight_log_owner_read on public.fight_log for select to authenticated using (public.is_owner());
revoke all on public.fight_log from anon;
