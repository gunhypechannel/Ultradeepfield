-- v748 the Resurrection War at 10,000 commanders.
-- Before: every commander read the whole war record, took a lock, changed it and wrote it back (compare-and-set). The record carried
-- every commander's war points and damage, so it grew with the player count, and every write sent the whole of it (old and new) to
-- every open game. Past a few hundred commanders at once that queues, conflicts and floods.
-- Now:
--   * war points go to their own table, one row per commander (cnt_con): adding them touches no shared row, so any number at once;
--   * damage shares go to cnt_share; the record keeps only the shared state (hit points, relays, commanders, the finale) and totals;
--   * hits are applied by the server in one short transaction (cnt_apply), with the war's rules, so nobody's write is ever rejected
--     as stale and nothing is lost to a race;
--   * every 15 seconds pg_cron folds the war points into the record (sup, n, top five) — the record changes at most 4 times a minute
--     from war points, whatever the player count;
--   * the record is no longer broadcast on every hit: pg_cron sends the newest version every 3 seconds when it changed (cnt_bcast).
-- Direct writes to a v2 record are refused (cnt_guard): only cnt_apply and the roll-up change it.

create table if not exists public.cnt_con (path text not null, k text not null, uid text not null, total int not null default 0, day int not null default 0,
  dpts int not null default 0, at timestamptz not null default now(), primary key (path, k, uid));
create index if not exists cnt_con_top on public.cnt_con (path, k, total desc);
create table if not exists public.cnt_share (path text not null, k text not null, tgt text not null, uid text not null, dmg int not null default 0,
  hits int not null default 0, primary key (path, k, tgt, uid));
create index if not exists cnt_share_top on public.cnt_share (path, k, tgt, dmg desc);
create table if not exists public.cnt_bc (path text primary key, at timestamptz not null);
alter table public.cnt_con enable row level security; alter table public.cnt_share enable row level security; alter table public.cnt_bc enable row level security;
revoke all on public.cnt_con, public.cnt_share, public.cnt_bc from anon, authenticated;

-- the network: kind, hit points and region of each target (as the game's CNT_NET)
create or replace function public.cnt_net(p_id text, out g text, out hp int, out reg int) language plpgsql immutable as $$
begin
  if p_id ~ '^ka[0-3]$' then g := 'ark'; hp := 160; reg := substr(p_id, 3, 1)::int;
  elsif p_id ~ '^kr[0-3][0-2]$' then g := 'rel'; hp := 60; reg := substr(p_id, 3, 1)::int;
  elsif p_id ~ '^kc[0-7]$' then g := 'cmd'; hp := 40; reg := substr(p_id, 3, 1)::int / 2;
  elsif p_id = 'ke0' then g := 'cmd'; hp := 200; reg := -1;
  else g := null; end if;
end $$;

-- a commander's war points: at most 300 a day (UTC), atomic per commander
create or replace function public.cnt_con_add(p_path text, p_k text, p_uid text, p_pts int) returns int language plpgsql set search_path to 'public' as $$
declare dnow int := floor(extract(epoch from now()) / 86400)::int; r record; add int;
begin
  p_pts := greatest(0, least(coalesce(p_pts, 0), 300)); if p_pts = 0 then return 0; end if;
  insert into cnt_con(path, k, uid, total, day, dpts) values (p_path, p_k, p_uid, 0, dnow, 0) on conflict (path, k, uid) do nothing;
  select * into r from cnt_con where path = p_path and k = p_k and uid = p_uid for update;
  add := least(p_pts, 300 - case when r.day = dnow then r.dpts else 0 end); if add <= 0 then return 0; end if;
  update cnt_con set total = total + add, dpts = case when day = dnow then dpts + add else add end, day = dnow, at = now() where path = p_path and k = p_k and uid = p_uid;
  return add;
end $$;

create or replace function public.cnt_fresh(p_k text) returns jsonb language sql immutable as $$
  select jsonb_build_object('k', p_k, 'v2', 1, 'sup', 0, 'n', 0, 'top', '[]'::jsonb, 'rk', 0, 'rel', '{}'::jsonb, 'ark', '{}'::jsonb, 'cmd', '{}'::jsonb) $$;

-- the finale's record with every timer applied (as the game's cntFinNorm)
create or replace function public.cnt_fin_norm(o jsonb, fe numeric) returns jsonb language plpgsql immutable as $$
declare fmin numeric := 60000; arr numeric := 5 * fmin; shield numeric := 20 * fmin; casc numeric := 40 * fmin; xfer numeric := 10 * fmin;
  t1 numeric; t0 numeric; live int; rate numeric; add int; w int; i int; c jsonb; c0 int; v int; best int;
begin
  if coalesce(o->>'out', '') <> '' or fe < arr then return o; end if;
  if coalesce((o->>'p3')::numeric, 0) = 0 then
    if fe >= shield then o := o || jsonb_build_object('out', 'fail', 'end', shield); end if; return o; end if;
  if coalesce((o->>'p4')::numeric, 0) = 0 then
    t1 := least(fe, casc); select count(*) into live from jsonb_array_elements_text(o->'hang') h where h::numeric > 0;
    rate := live * greatest(0, 1 - .15 * coalesce((o->>'conv')::numeric, 0)) / fmin;
    t0 := greatest(coalesce(nullif((o->>'rg')::numeric, 0), (o->>'p3')::numeric), (o->>'p3')::numeric);
    add := case when rate > 0 then floor((t1 - t0) * rate)::int else 0 end;
    if add > 0 then
      o := jsonb_set(o, '{rg}', to_jsonb((t0 + add / rate)::float8)); c := o->'cond'; c0 := (o->>'cond0')::int;
      while add > 0 loop
        w := -1; best := 0;
        for i in 0 .. jsonb_array_length(c) - 1 loop v := (c->>i)::int; if v > 0 and v < c0 and (w < 0 or v < best) then w := i; best := v; end if; end loop;
        exit when w < 0; c := jsonb_set(c, array[w::text], to_jsonb(best + 1)); add := add - 1;
      end loop;
      o := jsonb_set(o, '{cond}', c);
    end if;
    if fe >= casc then o := jsonb_set(o, '{p4}', to_jsonb(casc)); else return o; end if;
  end if;
  if coalesce((o->>'dead_')::numeric, 0) = 0 and fe >= (o->>'p4')::numeric + xfer then o := o || jsonb_build_object('out', 'fail', 'end', (o->>'p4')::numeric + xfer); end if;
  return o;
end $$;

-- the finale at its start (as the game's cntFinInit): scaled by the number of commanders in the war, fewer hangars per Ark destroyed
create or replace function public.cnt_fin_init(d jsonb, p_n int) returns jsonb language plpgsql immutable as $$
declare n int := greatest(1, p_n); sc numeric := greatest(.5, least(3, n / 4.0)); dead int := 0; h int; a int; hh int; c int; i int;
begin
  for i in 0 .. 3 loop if coalesce((d->'ark'->('ka' || i)->>'dead')::numeric, 0) > 0 then dead := dead + 1; end if; end loop;
  h := greatest(1, 4 - dead); a := round(18 * sc); hh := round(14 * sc); c := round(12 * sc);
  return jsonb_build_object('k', d->>'k', 'sc', sc, 'dead', dead, 'anc', jsonb_build_array(a, a, a), 'anc0', a, 'hang', (select jsonb_agg(hh) from generate_series(1, h)), 'hang0', hh,
    'cond', jsonb_build_array(c, c, c), 'cond0', c, 'conv', 0, 'esc', 0, 'rx', round(26 * sc), 'rx0', round(26 * sc), 'tx', round(16 * sc), 'tx0', round(16 * sc),
    'p3', 0, 'p4', 0, 'cut', 0, 'dead_', 0, 'out', '', 'end', 0, 'rg', 0, 'last', '');
end $$;

-- everything a fight changes in the war, applied by the server in one transaction.
-- ops: [{t:"con", pts}] war points only; [{t:"hit", id, seg, at}] a network target; [{t:"fin", tg, seg, fe, win}] the finale.
-- Returns {d: the record (null when only war points changed), o: [per op: {ev, counted, ...}], me: this commander's own numbers}.
create or replace function public.cnt_apply(p_path text, p_k text, p_ops jsonb) returns jsonb language plpgsql security definer set search_path to 'public' as $$
#variable_conflict use_column
declare me text := auth.uid()::text; tnow numeric := floor(extract(epoch from now()) * 1000); d jsonb; op jsonb; outs jsonb := '[]'::jsonb; need boolean;
  nt record; id text; e jsonb; seg int; at numeric; ev text; counted int; reg int; ups int; j int; r jsonb; aid text; ark jsonb;
  o jsonb; fe numeric; tg text; ph int; idx int; v int; def numeric; xr boolean; pts int; nn int; kk text; u text;
begin
  if me is null then raise exception 'cnt: sign in first'; end if;
  if p_path not in ('event/cnt', 'event/cnt_prev') or coalesce(p_k, '') = '' then raise exception 'cnt: bad record'; end if;
  if p_path = 'event/cnt_prev' and not public.is_owner() then raise exception 'cnt: the preview is the owner''s'; end if;
  if jsonb_typeof(p_ops) <> 'array' or jsonb_array_length(p_ops) > 4 then raise exception 'cnt: bad ops'; end if;
  perform set_config('udf.cnt_rpc', '1', true);
  need := exists (select 1 from jsonb_array_elements(p_ops) x where x->>'t' in ('hit', 'fin'));
  if need then
    insert into docs(path, data) values (p_path, cnt_fresh(p_k)) on conflict (path) do nothing;
    select data into d from docs where path = p_path for update;
    if coalesce(d->>'k', '') <> p_k then d := cnt_fresh(p_k); end if;
    if not (d ? 'v2') then -- a record from before v748: move its per-commander maps into the tables, once
      for kk in select jsonb_object_keys(coalesce(d->'con', '{}'::jsonb)) loop
        insert into cnt_con(path, k, uid, total) values (p_path, p_k, kk, coalesce((d->'con'->>kk)::int, 0)) on conflict do nothing; end loop;
      for id in select jsonb_object_keys(coalesce(d->'ark', '{}'::jsonb)) union all select jsonb_object_keys(coalesce(d->'rel', '{}'::jsonb)) union all select jsonb_object_keys(coalesce(d->'cmd', '{}'::jsonb)) loop
        nt := cnt_net(id); e := coalesce(d->nt.g->id, d->'rel'->id, d->'ark'->id, d->'cmd'->id);
        for u in select jsonb_object_keys(coalesce(e->'dmg', '{}'::jsonb)) loop
          insert into cnt_share(path, k, tgt, uid, dmg) values (p_path, p_k, id, u, coalesce((e->'dmg'->>u)::int, 0)) on conflict do nothing; end loop;
        if nt.g = 'ark' then d := jsonb_set(d, array['ark', id, 'tot'], to_jsonb((select coalesce(sum(value::int), 0) from jsonb_each_text(coalesce(e->'dmg', '{}'::jsonb))))); end if;
        d := d #- array[nt.g, id, 'dmg'];
      end loop;
      if d ? 'fin' then
        for u in select jsonb_object_keys(coalesce(d->'fin'->'hits', '{}'::jsonb)) loop
          insert into cnt_share(path, k, tgt, uid, dmg, hits) values (p_path, p_k, 'fin', u, coalesce((d->'fin'->'dmg'->>u)::int, 0), coalesce((d->'fin'->'hits'->>u)::int, 0)) on conflict do nothing; end loop;
        d := (d #- '{fin,dmg}') #- '{fin,hits}';
      end if;
      d := (d - 'con' - 'cday') || jsonb_build_object('v2', 1, 'n', (select count(*) from cnt_con where path = p_path and k = p_k), 'top', '[]'::jsonb);
    end if;
  end if;
  for op in select * from jsonb_array_elements(p_ops) loop
    ev := ''; counted := 0; pts := 0;
    if op->>'t' = 'con' then counted := cnt_con_add(p_path, p_k, me, (op->>'pts')::int); outs := outs || jsonb_build_object('ev', '', 'counted', counted);
    elsif op->>'t' = 'hit' then
      id := op->>'id'; nt := cnt_net(id); if nt.g is null then raise exception 'cnt: unknown target'; end if;
      seg := greatest(0, least(coalesce((op->>'seg')::int, 0), 200)); at := greatest(tnow - 86400000, least(coalesce((op->>'at')::numeric, tnow), tnow + 300000));
      reg := nt.reg; aid := case when reg >= 0 then 'ka' || reg else null end;
      -- defaults for anything not yet in the record; a relay rebuilds itself 12 hours after it fell, unless its Ark is gone
      if aid is not null then ark := coalesce(d->'ark'->aid, '{}'::jsonb);
        d := jsonb_set(d, array['ark', aid], ark || jsonb_build_object('hp', coalesce((ark->>'hp')::int, 160), 'cap', coalesce((ark->>'cap')::int, 6), 'dead', coalesce((ark->>'dead')::numeric, 0)));
        ups := 0;
        for j in 0 .. 2 loop r := coalesce(d->'rel'->('kr' || reg || j), '{}'::jsonb); r := r || jsonb_build_object('hp', coalesce((r->>'hp')::int, 60), 'down', coalesce((r->>'down')::numeric, 0));
          if (r->>'down')::numeric > 0 and (d->'ark'->aid->>'dead')::numeric = 0 and tnow - (r->>'down')::numeric >= 12 * 3600000 then r := r || jsonb_build_object('hp', 60, 'down', 0); end if;
          d := jsonb_set(d, array['rel', 'kr' || reg || j], r); if (r->>'down')::numeric = 0 then ups := ups + 1; end if; end loop;
      else ups := 0; end if;
      if nt.g = 'cmd' then e := coalesce(d->'cmd'->id, '{}'::jsonb); d := jsonb_set(d, array['cmd', id], e || jsonb_build_object('hp', coalesce((e->>'hp')::int, nt.hp), 'dead', coalesce((e->>'dead')::numeric, 0), 'back', coalesce((e->>'back')::numeric, 0), 'res', coalesce((e->>'res')::int, 0))); end if;
      e := d->nt.g->id;
      -- still open? (the game checks the stage before it sends a fleet; the server checks the state)
      if nt.g = 'rel' and (e->>'down')::numeric > 0 then ev := 'blocked';
      elsif nt.g = 'ark' and ((e->>'dead')::numeric > 0 or ups > 0) then ev := 'blocked';
      elsif nt.g = 'cmd' and ((e->>'dead')::numeric > 0 or (e->>'back')::numeric > at) then ev := 'blocked';
      elsif seg > 0 then
        seg := least(seg, (e->>'hp')::int); pts := 4 * seg; e := jsonb_set(e, '{hp}', to_jsonb((e->>'hp')::int - seg));
        insert into cnt_share(path, k, tgt, uid, dmg, hits) values (p_path, p_k, id, me, seg, 1) on conflict (path, k, tgt, uid) do update set dmg = cnt_share.dmg + seg, hits = cnt_share.hits + 1;
        if nt.g = 'rel' then if (e->>'hp')::int <= 0 then e := e || jsonb_build_object('hp', 0, 'down', at); d := jsonb_set(d, '{rk}', to_jsonb(coalesce((d->>'rk')::int, 0) + 1)); ev := 'reldown'; end if;
        elsif nt.g = 'ark' then e := jsonb_set(e, '{tot}', to_jsonb(coalesce((e->>'tot')::int, 0) + seg)); if (e->>'hp')::int <= 0 then e := e || jsonb_build_object('hp', 0, 'dead', at, 'last', me); ev := 'arkdead'; end if;
        else if (e->>'hp')::int <= 0 then
            if reg < 0 or ((d->'ark'->aid->>'dead')::numeric = 0 and (d->'ark'->aid->>'cap')::int > 0 and ups > 0) then
              e := e || jsonb_build_object('hp', nt.hp, 'back', at + 6 * 3600000, 'res', (e->>'res')::int + 1); ev := 'transfer';
              if reg >= 0 then d := jsonb_set(d, array['ark', aid, 'cap'], to_jsonb((d->'ark'->aid->>'cap')::int - 1)); end if;
            else e := e || jsonb_build_object('hp', 0, 'dead', at, 'last', me); ev := 'dead'; end if; end if;
        end if;
        d := jsonb_set(d, array[nt.g, id], e);
        counted := cnt_con_add(p_path, p_k, me, pts);
      end if;
      outs := outs || jsonb_build_object('ev', ev, 'seg', seg, 'counted', counted, 'id', id);
    elsif op->>'t' = 'fin' then
      fe := coalesce((op->>'fe')::numeric, -1); tg := coalesce(op->>'tg', ''); seg := greatest(0, least(coalesce((op->>'seg')::int, 0), 200));
      o := d->'fin'; if o is null or coalesce(o->>'k', '') <> p_k then
        nn := coalesce((d->>'n')::int, 0); if nn = 0 then select count(*) into nn from cnt_con where path = p_path and k = p_k; end if; o := cnt_fin_init(d, nn); end if; -- the same count every game shows
      o := cnt_fin_norm(o, fe);
      ph := case when fe < 0 then 0 when fe < 300000 then 1 when coalesce(o->>'out', '') <> '' then 5 when (o->>'p3')::numeric = 0 then 2 when (o->>'p4')::numeric = 0 then 3 else 4 end;
      xr := (o->>'p4')::numeric > 0 and (o->>'cut')::numeric = 0 and fe < (o->>'p4')::numeric + 6 * 60000;
      if ph < 2 or ph > 4 then ev := 'closed';
      elsif not ((ph = 2 and tg ~ '^anc[0-2]$' and (o->'anc'->>(substr(tg, 4)::int))::int > 0)
              or (ph = 3 and ((tg ~ '^hang[0-9]$' and coalesce((o->'hang'->>(substr(tg, 5)::int))::int, 0) > 0) or (tg ~ '^cond[0-2]$' and (o->'cond'->>(substr(tg, 5)::int))::int > 0) or tg in ('conv', 'esc')))
              or (ph = 4 and ((tg = 'tx' and (o->>'tx')::int > 0 and xr) or tg = 'rx'))) then ev := 'gone';
      elsif tg = 'rx' and xr then ev := 'shielded';
      else
        if tg in ('conv', 'esc') then if coalesce((op->>'win')::boolean, false) then pts := 3; o := jsonb_set(o, array[tg], to_jsonb((o->>tg)::int + 1)); ev := tg; end if;
        elsif seg > 0 then
          if tg ~ '^anc' then idx := substr(tg, 4)::int; v := greatest(0, (o->'anc'->>idx)::int - seg); seg := (o->'anc'->>idx)::int - v; o := jsonb_set(o, array['anc', idx::text], to_jsonb(v));
            if v = 0 then ev := 'ancdown'; if not exists (select 1 from jsonb_array_elements_text(o->'anc') a where a::int > 0) then o := o || jsonb_build_object('p3', fe, 'rg', fe); ev := 'p3'; end if; end if;
          elsif tg ~ '^hang' then idx := substr(tg, 5)::int; v := greatest(0, (o->'hang'->>idx)::int - seg); seg := (o->'hang'->>idx)::int - v; o := jsonb_set(o, array['hang', idx::text], to_jsonb(v)); if v = 0 then ev := 'hangdown'; end if;
          elsif tg ~ '^cond' then idx := substr(tg, 5)::int; v := greatest(0, (o->'cond'->>idx)::int - seg); seg := (o->'cond'->>idx)::int - v; o := jsonb_set(o, array['cond', idx::text], to_jsonb(v)); if v = 0 then ev := 'condcut'; end if;
          elsif tg = 'tx' then v := greatest(0, (o->>'tx')::int - seg); seg := (o->>'tx')::int - v; o := jsonb_set(o, '{tx}', to_jsonb(v)); if v = 0 then o := jsonb_set(o, '{cut}', to_jsonb(fe)); ev := 'cut'; end if;
          else v := greatest(0, (o->>'rx')::int - seg); seg := (o->>'rx')::int - v; o := jsonb_set(o, '{rx}', to_jsonb(v));
            if v = 0 then o := o || jsonb_build_object('dead_', fe, 'out', case when (o->>'cut')::numeric > 0 then 'win' else 'part' end, 'end', fe, 'last', me); ev := 'dead'; end if; end if;
          pts := 4 * seg;
          if ev <> 'dead' and (o->>'p4')::numeric = 0 and (o->>'p3')::numeric > 0 then
            def := ((select coalesce(sum(greatest(0, x::int)), 0) from jsonb_array_elements_text(o->'hang') x) + (select coalesce(sum(greatest(0, x::int)), 0) from jsonb_array_elements_text(o->'cond') x))
              / greatest(1, jsonb_array_length(o->'hang') * (o->>'hang0')::int + 3 * (o->>'cond0')::int)::numeric;
            if def <= .25 then o := jsonb_set(o, '{p4}', to_jsonb(fe)); ev := case when ev = '' then 'p4' else ev || '+p4' end; end if;
          end if;
          insert into cnt_share(path, k, tgt, uid, dmg, hits) values (p_path, p_k, 'fin', me, least(100, seg), 0) on conflict (path, k, tgt, uid) do update set dmg = cnt_share.dmg + least(100, seg);
        end if;
        insert into cnt_share(path, k, tgt, uid, dmg, hits) values (p_path, p_k, 'fin', me, 0, 1) on conflict (path, k, tgt, uid) do update set hits = cnt_share.hits + 1;
        if pts > 0 then counted := cnt_con_add(p_path, p_k, me, pts); end if;
      end if;
      d := jsonb_set(d, '{fin}', o);
      outs := outs || jsonb_build_object('ev', ev, 'seg', seg, 'counted', counted, 'tg', tg);
    else raise exception 'cnt: bad op'; end if;
  end loop;
  if need then update docs set data = d where path = p_path; end if;
  perform set_config('udf.cnt_rpc', '', true); -- the permission ends with this call
  return jsonb_build_object('d', case when need then d else null end, 'o', outs, 'me', cnt_me_of(p_path, p_k, me));
end $$;

-- one commander's own numbers: war points (all, today), damage per target, the finale (damage, attacks, in the top ten)
create or replace function public.cnt_me_of(p_path text, p_k text, p_uid text) returns jsonb language sql stable set search_path to 'public' as $$
  select jsonb_build_object(
    'con', coalesce((select total from cnt_con where path = p_path and k = p_k and uid = p_uid), 0),
    'today', coalesce((select case when day = floor(extract(epoch from now()) / 86400)::int then dpts else 0 end from cnt_con where path = p_path and k = p_k and uid = p_uid), 0),
    'day', floor(extract(epoch from now()) / 86400)::int,
    'dmg', coalesce((select jsonb_object_agg(tgt, dmg) from cnt_share where path = p_path and k = p_k and uid = p_uid and tgt <> 'fin'), '{}'::jsonb),
    'fin', (select jsonb_build_object('dmg', s.dmg, 'hits', s.hits, 't10', s.dmg > 0 and (select count(*) from cnt_share x where x.path = p_path and x.k = p_k and x.tgt = 'fin' and x.dmg > s.dmg) < 10)
            from cnt_share s where s.path = p_path and s.k = p_k and s.tgt = 'fin' and s.uid = p_uid)) $$;
create or replace function public.cnt_me(p_path text, p_k text) returns jsonb language plpgsql security definer set search_path to 'public' as $$
begin if auth.uid() is null then return null; end if; return cnt_me_of(p_path, p_k, auth.uid()::text); end $$;

-- every 15 seconds: fold the war points into the record (total, commanders, top five); only writes when something changed
create or replace function public.cnt_roll() returns void language plpgsql security definer set search_path to 'public' as $$
declare p text; d jsonb; s bigint; n int; t jsonb;
begin
  for p in select path from docs where path in ('event/cnt', 'event/cnt_prev') and data ? 'v2' loop
    select data into d from docs where path = p;
    select coalesce(sum(total), 0), count(*) into s, n from cnt_con where path = p and k = d->>'k';
    select coalesce(jsonb_agg(jsonb_build_array(uid, total) order by total desc), '[]'::jsonb) into t from (select uid, total from cnt_con where path = p and k = d->>'k' order by total desc limit 5) x;
    if coalesce((d->>'sup')::bigint, -1) <> s or coalesce((d->>'n')::int, -1) <> n or coalesce(d->'top', 'null'::jsonb) <> t then
      perform set_config('udf.cnt_rpc', '1', true);
      update docs set data = data || jsonb_build_object('sup', s, 'n', n, 'top', t) where path = p and data->>'k' = d->>'k';
      perform set_config('udf.cnt_rpc', '', true);
    end if;
  end loop;
end $$;

-- every 3 seconds: send the newest war record to every open game, if it changed since the last send
create or replace function public.cnt_bcast() returns void language plpgsql security definer set search_path to 'public', 'realtime' as $$
declare r record;
begin
  for r in select d.path, d.data, d.updated_at from docs d left join cnt_bc b on b.path = d.path where d.path in ('event/cnt', 'event/cnt_prev') and d.data ? 'v2' and (b.at is null or d.updated_at > b.at) loop
    begin
      perform realtime.send(jsonb_build_object('operation', 'UPDATE', 'record', jsonb_build_object('path', r.path, 'data', r.data)), 'UPDATE', 'udf:pub', true);
    exception when others then null; end;
    insert into cnt_bc(path, at) values (r.path, r.updated_at) on conflict (path) do update set at = excluded.at;
  end loop;
end $$;

-- the per-write broadcast skips v2 war records (cnt_bcast sends them, at most every 3 seconds)
create or replace function public.udf_broadcast() returns trigger language plpgsql security definer set search_path to 'public', 'realtime' as $function$
declare r record; u text;
begin
  if TG_OP = 'DELETE' then r := OLD; else r := NEW; end if;
  if r.top in ('data', 'feedback', '_locks') then return null; end if;
  if r.path in ('event/cnt', 'event/cnt_prev') and TG_OP <> 'DELETE' and r.data ? 'v2' then return null; end if; /* v748 */
  begin -- a broadcast that fails never blocks the write
  if r.top = 'inbox' then
    perform realtime.broadcast_changes('udf:u:' || split_part(r.path, '/', 2), TG_OP, TG_OP, TG_TABLE_NAME, TG_TABLE_SCHEMA, NEW, OLD, 'ROW');
  elsif r.top = 'inbound' then
    perform realtime.broadcast_changes('udf:in:' || split_part(r.path, '/', 2), TG_OP, TG_OP, TG_TABLE_NAME, TG_TABLE_SCHEMA, NEW, OLD, 'ROW');
  elsif r.top = 'dms' then
    for u in select distinct jsonb_array_elements_text(coalesce(r.data -> 'p', '[]'::jsonb)) loop
      perform realtime.broadcast_changes('udf:u:' || u, TG_OP, TG_OP, TG_TABLE_NAME, TG_TABLE_SCHEMA, NEW, OLD, 'ROW');
    end loop;
  else
    perform realtime.broadcast_changes('udf:pub', TG_OP, TG_OP, TG_TABLE_NAME, TG_TABLE_SCHEMA, NEW, OLD, 'ROW');
  end if;
  exception when others then null;
  end;
  return null;
end $function$;

-- the v746 rules, unchanged, except that a v2 record carries no per-commander maps (moved out above, once)
create or replace function public.cnt_guard() returns trigger language plpgsql set search_path to 'public' as $function$
declare me text := auth.uid()::text; o jsonb; n jsonb; k text; dv numeric; dsum numeric := 0; id text; oa jsonb; na jsonb; reg text; ups int; tnow numeric := extract(epoch from now()) * 1000;
begin
  if me is null or new.path <> 'event/cnt' then return new; end if;
  n := coalesce(new.data, '{}'::jsonb);
  o := case when tg_op = 'UPDATE' then coalesce(old.data, '{}'::jsonb) else '{}'::jsonb end;
  if coalesce(o->>'k', '') <> coalesce(n->>'k', '') then o := '{}'::jsonb; end if;
  if n ? 'v2' then o := o - 'con' - 'cday'; end if; -- v748: war points and damage shares live in their own tables now
  -- contributions: only your own, at most a day's cap per write, never removed; the meter grows only by them
  for k in select jsonb_object_keys(coalesce(n->'con', '{}'::jsonb)) loop
    dv := coalesce((n->'con'->>k)::numeric, 0) - coalesce((o->'con'->>k)::numeric, 0);
    if dv <> 0 and k <> me then raise exception 'cnt: only your own contribution can change'; end if;
    if dv < 0 or dv > 300 then raise exception 'cnt: contribution change out of range'; end if;
    dsum := dsum + dv;
  end loop;
  for k in select jsonb_object_keys(coalesce(o->'con', '{}'::jsonb)) loop
    if not (coalesce(n->'con', '{}'::jsonb) ? k) then raise exception 'cnt: contributions cannot be removed'; end if;
  end loop;
  if not (n ? 'v2') and coalesce((n->>'sup')::numeric, 0) - coalesce((o->>'sup')::numeric, 0) > dsum then raise exception 'cnt: war points grew without contribution'; end if; -- v2: the server totals them
  -- the Arks: dead stays dead, no healing, no capacity regained, damage shares only your own
  for id in select jsonb_object_keys(coalesce(o->'ark', '{}'::jsonb)) loop
    oa := o->'ark'->id; na := coalesce(n->'ark'->id, '{}'::jsonb);
    if coalesce((oa->>'dead')::numeric, 0) > 0 and coalesce((na->>'dead')::numeric, 0) <> (oa->>'dead')::numeric then raise exception 'cnt: a destroyed Ark stays destroyed'; end if;
    if oa ? 'hp' and coalesce((na->>'hp')::numeric, 0) > (oa->>'hp')::numeric then raise exception 'cnt: an Ark cannot heal'; end if;
    if oa ? 'cap' and coalesce((na->>'cap')::numeric, 0) > (oa->>'cap')::numeric then raise exception 'cnt: rebuild capacity cannot grow'; end if;
    for k in select jsonb_object_keys(coalesce(na->'dmg', '{}'::jsonb)) loop
      dv := coalesce((na->'dmg'->>k)::numeric, 0) - coalesce((oa->'dmg'->>k)::numeric, 0);
      if dv <> 0 and (k <> me or dv < 0 or dv > 200) then raise exception 'cnt: Ark damage change not allowed'; end if;
    end loop;
  end loop;
  -- the relays: a fallen relay comes back only 12 hours later, and never once its Ark is gone
  for id in select jsonb_object_keys(coalesce(o->'rel', '{}'::jsonb)) loop
    oa := o->'rel'->id; na := coalesce(n->'rel'->id, '{}'::jsonb); reg := substr(id, 3, 1);
    if coalesce((oa->>'down')::numeric, 0) > 0 and coalesce((na->>'down')::numeric, 0) = 0 then
      if tnow + 300000 < (oa->>'down')::numeric + 12 * 3600000 then raise exception 'cnt: a relay rebuilds only 12 hours after it fell'; end if;
      if coalesce((n->'ark'->('ka' || reg)->>'dead')::numeric, 0) > 0 then raise exception 'cnt: a relay cannot rebuild once its Ark is gone'; end if;
    end if;
    for k in select jsonb_object_keys(coalesce(na->'dmg', '{}'::jsonb)) loop
      dv := coalesce((na->'dmg'->>k)::numeric, 0) - coalesce((oa->'dmg'->>k)::numeric, 0);
      if dv <> 0 and (k <> me or dv < 0 or dv > 200) then raise exception 'cnt: relay damage change not allowed'; end if;
    end loop;
  end loop;
  -- the commanders: gone for good stays gone; a rebuild needs a living Ark with capacity (spent now) and a relay up
  for id in select jsonb_object_keys(coalesce(o->'cmd', '{}'::jsonb)) loop
    oa := o->'cmd'->id; na := coalesce(n->'cmd'->id, '{}'::jsonb);
    if coalesce((oa->>'dead')::numeric, 0) > 0 and coalesce((na->>'dead')::numeric, 0) <> (oa->>'dead')::numeric then raise exception 'cnt: a commander gone for good stays gone'; end if;
    dv := coalesce((na->>'res')::numeric, 0) - coalesce((oa->>'res')::numeric, 0);
    if dv < 0 or dv > 1 then raise exception 'cnt: resurrection count out of range'; end if;
    if dv = 1 and id like 'kc%' then
      reg := (floor(substr(id, 3)::numeric / 2))::int::text;
      if coalesce((n->'ark'->('ka' || reg)->>'dead')::numeric, 0) > 0 then raise exception 'cnt: no Ark left to rebuild this commander'; end if;
      if coalesce((n->'ark'->('ka' || reg)->>'cap')::numeric, 0) <> coalesce((o->'ark'->('ka' || reg)->>'cap')::numeric, 6) - 1 then raise exception 'cnt: a rebuild must spend its Ark''s capacity'; end if;
      select count(*) into ups from jsonb_each(coalesce(n->'rel', '{}'::jsonb)) r where r.key like 'kr' || reg || '%' and coalesce((r.value->>'down')::numeric, 0) = 0;
      if ups < 1 then raise exception 'cnt: no relay up to carry the transfer'; end if;
    end if;
    for k in select jsonb_object_keys(coalesce(na->'dmg', '{}'::jsonb)) loop
      dv := coalesce((na->'dmg'->>k)::numeric, 0) - coalesce((oa->'dmg'->>k)::numeric, 0);
      if dv <> 0 and (k <> me or dv < 0 or dv > 200) then raise exception 'cnt: commander damage change not allowed'; end if;
    end loop;
  end loop;
  -- the finale: once decided, the outcome stands; damage and attack counts only your own
  if o ? 'fin' and coalesce(o->'fin'->>'k', '') = coalesce(n->'fin'->>'k', '') then
    if coalesce(o->'fin'->>'out', '') <> '' and coalesce(n->'fin'->>'out', '') <> o->'fin'->>'out' then raise exception 'cnt: the finale''s outcome is decided'; end if;
    for k in select jsonb_object_keys(coalesce(n->'fin'->'dmg', '{}'::jsonb)) loop
      dv := coalesce((n->'fin'->'dmg'->>k)::numeric, 0) - coalesce((o->'fin'->'dmg'->>k)::numeric, 0);
      if dv <> 0 and (k <> me or dv < 0 or dv > 100) then raise exception 'cnt: finale damage change not allowed'; end if;
    end loop;
    for k in select jsonb_object_keys(coalesce(n->'fin'->'hits', '{}'::jsonb)) loop
      dv := coalesce((n->'fin'->'hits'->>k)::numeric, 0) - coalesce((o->'fin'->'hits'->>k)::numeric, 0);
      if dv <> 0 and (k <> me or dv < 0 or dv > 1) then raise exception 'cnt: finale attack count change not allowed'; end if;
    end loop;
  end if;
  return new;
end $function$;

-- the guard: a v2 record is changed only by cnt_apply and the roll-up (plus the v746 rules, unchanged)
create or replace function public.cnt_guard_v2() returns trigger language plpgsql set search_path to 'public' as $$
begin
  if auth.uid() is null then return new; end if;
  if ((tg_op = 'UPDATE' and old.data ? 'v2') or new.data ? 'v2') and coalesce(current_setting('udf.cnt_rpc', true), '') <> '1' then
    raise exception 'cnt: the war record is changed by the server only'; end if;
  return new;
end $$;
drop trigger if exists d_cnt_guard2 on public.docs;
create trigger d_cnt_guard2 before insert or update on public.docs for each row when (new.path = 'event/cnt') execute function public.cnt_guard_v2();

revoke all on function public.cnt_apply(text, text, jsonb), public.cnt_me(text, text), public.cnt_roll(), public.cnt_bcast(), public.cnt_con_add(text, text, text, int), public.cnt_me_of(text, text, text) from public, anon, authenticated;
grant execute on function public.cnt_apply(text, text, jsonb), public.cnt_me(text, text) to authenticated;

select cron.unschedule(jobid) from cron.job where jobname in ('cnt_roll', 'cnt_bcast');
select cron.schedule('cnt_roll', '15 seconds', 'select public.cnt_roll()');
select cron.schedule('cnt_bcast', '3 seconds', 'select public.cnt_bcast()');

-- the 3-second broadcast job writes ~29,000 run records a day: keep one day of them
select cron.unschedule(jobid) from cron.job where jobname = 'cron_log_trim';
select cron.schedule('cron_log_trim', '17 * * * *', $$delete from cron.job_run_details where end_time < now() - interval '1 day'$$);
