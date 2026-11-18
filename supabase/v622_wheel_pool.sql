-- v622 the Glyph Wheel's shared jackpot: every spin by anyone adds a shard to one pot; a Jackpot takes half of it, a Mega Jackpot all of it.
create table if not exists public.wheel_pool (id int primary key check (id = 1), pool int not null default 0, at timestamptz not null default now());
insert into public.wheel_pool(id, pool) values (1, 40) on conflict do nothing;
create table if not exists public.wheel_spins (uid uuid not null, d date not null, n int not null default 0, w int not null default 0, primary key (uid, d));
create table if not exists public.wheel_wins (id bigserial primary key, uid uuid not null, name text not null, kind text not null, amt int not null, at timestamptz not null default now());
alter table public.wheel_pool enable row level security; alter table public.wheel_spins enable row level security; alter table public.wheel_wins enable row level security;
revoke all on public.wheel_pool, public.wheel_spins, public.wheel_wins from anon, authenticated;
create or replace function public.whl_spin(p_n int default 1) returns int language plpgsql security definer set search_path to 'public' as $$
declare k int; used int; p int;
begin
  if auth.uid() is null then raise exception 'bad'; end if;
  k := greatest(1, least(coalesce(p_n, 1), 5));
  insert into wheel_spins(uid, d, n) values (auth.uid(), current_date, 0) on conflict (uid, d) do nothing;
  select n into used from wheel_spins where uid = auth.uid() and d = current_date for update;
  k := least(k, greatest(0, 40 - used));
  update wheel_spins set n = n + k where uid = auth.uid() and d = current_date;
  update wheel_pool set pool = least(1000, pool + k), at = now() where id = 1 returning pool into p;
  return p;
end $$;
create or replace function public.whl_win(p_kind text, p_name text) returns int language plpgsql security definer set search_path to 'public' as $$
declare p int; take int; wins int;
begin
  if auth.uid() is null or p_kind not in ('jack', 'mega') then raise exception 'bad'; end if;
  insert into wheel_spins(uid, d, n) values (auth.uid(), current_date, 0) on conflict (uid, d) do nothing;
  select w into wins from wheel_spins where uid = auth.uid() and d = current_date for update;
  if wins >= 3 then return 0; end if;
  update wheel_spins set w = w + 1 where uid = auth.uid() and d = current_date;
  select pool into p from wheel_pool where id = 1 for update;
  take := case when p_kind = 'mega' then p else p / 2 end;
  update wheel_pool set pool = pool - take, at = now() where id = 1;
  insert into wheel_wins(uid, name, kind, amt) values (auth.uid(), left(coalesce(nullif(trim(p_name), ''), 'A commander'), 24), p_kind, take);
  delete from wheel_wins where id not in (select id from wheel_wins order by at desc limit 50);
  return take;
end $$;
create or replace function public.whl_state() returns jsonb language sql security definer set search_path to 'public' as $$
  select jsonb_build_object('pool', (select pool from wheel_pool where id = 1),
    'last', coalesce((select jsonb_agg(jsonb_build_object('name', name, 'kind', kind, 'amt', amt, 'at', extract(epoch from at) * 1000) order by at desc) from (select * from wheel_wins order by at desc limit 5) x), '[]'::jsonb));
$$;
revoke all on function public.whl_spin(int), public.whl_win(text, text), public.whl_state() from public, anon;
grant execute on function public.whl_spin(int), public.whl_win(text, text), public.whl_state() to authenticated;
