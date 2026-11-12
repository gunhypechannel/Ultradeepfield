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
