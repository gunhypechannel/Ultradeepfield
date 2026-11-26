-- v800 the Aetherion Gateway: the server's ledger of fleet transfers through the gateway, and of reward claims.
-- Every transfer has one row per (commander, transaction id). The server keeps the clock (charge, transit and return times), the
-- allowed order of states, the deployment limit and the realm's availability, so a transfer cannot be faked, sped up, repeated or
-- doubled: asking for the same step twice returns the same row. Ships in a transfer can only go down (battle losses), never up.
-- Owner previews (prev) are only allowed for the owner and never count against anything.
create table if not exists public.aet_cfg (k text primary key, v jsonb not null);
insert into public.aet_cfg (k, v) values
  ('open', to_jsonb(1835229600000::bigint)),            -- 2028-02-27 02:00 UTC: an hour after the First Aperture's finale (Sat Feb 26, 6 pm Phoenix) ends
  ('off', 'false'::jsonb),                               -- the owner's switch: true closes the gateway to new departures (returns always work)
  ('realms', '["int","shat","dom","tide"]'::jsonb),                       -- realms open to travel; more are added as they are charted
  ('charge', '45'::jsonb),                               -- seconds the gateway charges before a departure
  ('tt', '{"int": 180, "shat": 240, "dom": 300, "tide": 300}'::jsonb),  -- seconds through the corridor, each way
  ('limit', '3'::jsonb)                                  -- most transfers a commander may have beyond the gateway at once
on conflict (k) do nothing;

create table if not exists public.aet_tx (
  uid uuid not null, txid text not null, realm text not null, st text not null, n jsonb not null, prev boolean not null default false,
  t_res timestamptz not null default now(), t_out timestamptz, eta timestamptz, t_arr timestamptz, t_ret timestamptz, ret_eta timestamptz, t_home timestamptz,
  upd timestamptz not null default now(), primary key (uid, txid));
create table if not exists public.aet_claims (uid uuid not null, cid text not null, at timestamptz not null default now(), v jsonb, primary key (uid, cid));
create table if not exists public.aet_log (id bigserial primary key, uid uuid, txid text, op text, at timestamptz not null default now(), ok boolean, note text);
alter table public.aet_cfg enable row level security; alter table public.aet_tx enable row level security;
alter table public.aet_claims enable row level security; alter table public.aet_log enable row level security;
create index if not exists aet_tx_open on public.aet_tx (uid) where st not in ('HOME', 'VOID', 'LOST');
create index if not exists aet_log_uid on public.aet_log (uid, at);

create or replace function public.aet_cfgv(p text) returns jsonb language sql stable security definer set search_path = public as $$ select v from aet_cfg where k = p $$;

create or replace function public.aet_row(r public.aet_tx) returns jsonb language sql stable as $$
  select jsonb_build_object('txid', r.txid, 'realm', r.realm, 'st', r.st, 'n', r.n, 'prev', r.prev,
    't_res', floor(extract(epoch from r.t_res) * 1000), 't_out', floor(extract(epoch from r.t_out) * 1000), 'eta', floor(extract(epoch from r.eta) * 1000),
    't_arr', floor(extract(epoch from r.t_arr) * 1000), 't_ret', floor(extract(epoch from r.t_ret) * 1000), 'ret_eta', floor(extract(epoch from r.ret_eta) * 1000),
    't_home', floor(extract(epoch from r.t_home) * 1000), 'now', floor(extract(epoch from now()) * 1000)) $$;

-- one step of a transfer: reserve | depart | arrive | recall | home | losses | void
create or replace function public.aet_tx(p_op text, p_txid text, p jsonb default '{}'::jsonb) returns jsonb
language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); r aet_tx; k text; v jsonb; tot bigint := 0; nn jsonb; pv boolean; tt int; chg int; lim int; open_ms bigint; recent int;
begin
  if me is null then raise exception 'sign in first' using errcode = '42501'; end if;
  if p_txid is null or p_txid !~ '^[a-z0-9-]{8,40}$' then raise exception 'bad transfer id'; end if;
  select count(*) into recent from aet_log where uid = me and at > now() - interval '10 seconds';
  if recent > 30 then raise exception 'too many requests, wait a moment' using errcode = '42501'; end if;
  select * into r from aet_tx where uid = me and txid = p_txid for update;
  chg := coalesce((aet_cfgv('charge'))::int, 45);

  if p_op = 'reserve' then
    if found then insert into aet_log(uid, txid, op, ok, note) values (me, p_txid, p_op, true, 'repeat'); return aet_row(r); end if;
    if coalesce(p->>'realm', '') !~ '^(int|shat|dom|tide)$' then raise exception 'unknown realm'; end if;
    pv := coalesce((p->>'prev')::boolean, false);
    if pv and not is_owner() then raise exception 'previews are for the owner' using errcode = '42501'; end if;
    if not pv then
      open_ms := coalesce((aet_cfgv('open'))::bigint, 0);
      if extract(epoch from now()) * 1000 < open_ms then raise exception 'the gateway is not open yet'; end if;
      if coalesce((aet_cfgv('off'))::boolean, false) then raise exception 'the gateway is closed for maintenance'; end if;
      if not (aet_cfgv('realms') ? (p->>'realm')) then raise exception 'that realm cannot be reached yet'; end if;
    end if;
    nn := p->'n'; if jsonb_typeof(nn) <> 'object' then raise exception 'no fleet'; end if;
    for k, v in select * from jsonb_each(nn) loop
      if k !~ '^[A-Za-z]{2,24}$' or jsonb_typeof(v) <> 'number' or (v::text)::numeric <> floor((v::text)::numeric) or (v::text)::numeric < 0 or (v::text)::numeric > 10000000 then raise exception 'bad fleet'; end if;
      tot := tot + (v::text)::bigint; end loop;
    if tot < 1 then raise exception 'send at least one ship'; end if;
    lim := coalesce((aet_cfgv('limit'))::int, 3);
    if (select count(*) from aet_tx where uid = me and prev = pv and st not in ('HOME', 'VOID', 'LOST')) >= lim then raise exception 'every gateway slot is in use'; end if;
    insert into aet_tx(uid, txid, realm, st, n, prev) values (me, p_txid, p->>'realm', 'RESERVED', nn, pv) returning * into r;
    insert into aet_log(uid, txid, op, ok) values (me, p_txid, p_op, true); return aet_row(r);
  end if;

  if not found then raise exception 'no such transfer'; end if;
  tt := coalesce((aet_cfgv('tt')->>r.realm)::int, 180);
  if p_op = 'depart' then
    if r.st = 'RESERVED' then
      if now() < r.t_res + make_interval(secs => chg) then raise exception 'the gateway is still charging'; end if;
      if not r.prev and coalesce((aet_cfgv('off'))::boolean, false) then raise exception 'the gateway is closed for maintenance'; end if;
      update aet_tx set st = 'IN_TRANSIT', t_out = now(), eta = now() + make_interval(secs => tt), upd = now() where uid = me and txid = p_txid returning * into r;
    end if;
  elsif p_op = 'arrive' then
    if r.st = 'IN_TRANSIT' then
      if now() < r.eta then raise exception 'still in the corridor'; end if;
      update aet_tx set st = 'ACTIVE', t_arr = now(), upd = now() where uid = me and txid = p_txid returning * into r;
    end if;
  elsif p_op = 'recall' then
    if r.st = 'RESERVED' then update aet_tx set st = 'HOME', t_home = now(), upd = now() where uid = me and txid = p_txid returning * into r;
    elsif r.st = 'ACTIVE' then update aet_tx set st = 'RETURNING', t_ret = now(), ret_eta = now() + make_interval(secs => tt), upd = now() where uid = me and txid = p_txid returning * into r; end if;
  elsif p_op = 'home' then
    if r.st = 'RETURNING' then
      if now() < r.ret_eta then raise exception 'still on the way home'; end if;
      update aet_tx set st = 'HOME', t_home = now(), upd = now() where uid = me and txid = p_txid returning * into r;
    end if;
  elsif p_op = 'losses' then
    if r.st not in ('ACTIVE', 'RETURNING') then raise exception 'that fleet is not beyond the gateway'; end if;
    nn := coalesce(p->'n', '{}'::jsonb); if jsonb_typeof(nn) <> 'object' then raise exception 'bad fleet'; end if;
    for k, v in select * from jsonb_each(nn) loop
      if jsonb_typeof(v) <> 'number' or (v::text)::numeric < 0 or (v::text)::numeric > coalesce((r.n->>k)::numeric, 0) or (v::text)::numeric <> floor((v::text)::numeric) then raise exception 'a fleet can only lose ships out there'; end if;
      tot := tot + (v::text)::bigint; end loop;
    update aet_tx set n = nn, st = case when tot = 0 then 'LOST' else st end, upd = now() where uid = me and txid = p_txid returning * into r;
  elsif p_op = 'void' then
    if r.st not in ('HOME', 'VOID', 'LOST') then update aet_tx set st = 'VOID', upd = now() where uid = me and txid = p_txid returning * into r; end if;
  else raise exception 'unknown step';
  end if;
  insert into aet_log(uid, txid, op, ok) values (me, p_txid, p_op, true);
  return aet_row(r);
end $$;

-- every transfer of mine that is not finished, and those finished in the last week (to reconcile a save)
create or replace function public.aet_mine() returns jsonb language sql stable security definer set search_path = public as $$
  select coalesce(jsonb_agg(aet_row(t) order by t.t_res), '[]'::jsonb) from aet_tx t
  where t.uid = auth.uid() and (t.st not in ('HOME', 'VOID', 'LOST') or t.upd > now() - interval '7 days') $$;

-- a reward claim: true the first time, false ever after (so a reconnect or a double tap can never pay twice)
create or replace function public.aet_claim(p_cid text, p jsonb default null) returns boolean language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid();
begin
  if me is null then raise exception 'sign in first' using errcode = '42501'; end if;
  if p_cid is null or p_cid !~ '^[A-Za-z0-9:_.-]{2,80}$' then raise exception 'bad claim'; end if;
  insert into aet_claims(uid, cid, v) values (me, p_cid, p) on conflict do nothing;
  return found;
end $$;

-- the gateway's public settings (open time, switch, realms)
create or replace function public.aet_state() returns jsonb language sql stable security definer set search_path = public as $$
  select jsonb_object_agg(k, v) || jsonb_build_object('now', floor(extract(epoch from now()) * 1000)) from aet_cfg $$;

revoke all on function public.aet_tx(text, text, jsonb), public.aet_mine(), public.aet_claim(text, jsonb), public.aet_state() from public;
revoke all on function public.aet_cfgv(text) from public;
grant execute on function public.aet_tx(text, text, jsonb), public.aet_mine(), public.aet_claim(text, jsonb), public.aet_state() to authenticated;
revoke execute on function public.aet_tx(text, text, jsonb), public.aet_mine(), public.aet_claim(text, jsonb), public.aet_state(), public.aet_cfgv(text) from anon;
revoke execute on function public.aet_cfgv(text) from authenticated;
alter function public.aet_row(public.aet_tx) set search_path = public;
