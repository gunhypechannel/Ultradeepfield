-- v413: live updates by topic (Realtime Broadcast from the database) instead of postgres_changes on the whole table.
-- postgres_changes checks every subscriber's read rule for every change (load grows with players squared). Now each change to a shared
-- record is broadcast once to its topic; a player's right to a topic is checked once, when they join it.
--   udf:pub         planets, occ, alliances, assaults, chat, event, galaxy, players, profiles (everyone signed in may read these)
--   udf:u:<uid>     that player's inbox, and every DM they take part in
--   udf:in:<uid>    that player's inbound fleets (readable by any signed-in player, as before: allies watch them)
-- Player saves (data), feedback and _locks are never broadcast. The docs table stays in the supabase_realtime publication for now so
-- clients older than v413 keep working; remove it once they have updated.
create or replace function public.udf_broadcast() returns trigger
language plpgsql security definer set search_path = public, realtime as $$
declare r record; u text;
begin
  if TG_OP = 'DELETE' then r := OLD; else r := NEW; end if;
  if r.top in ('data', 'feedback', '_locks') then return null; end if;
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
end $$;
revoke all on function public.udf_broadcast() from public, anon, authenticated;
drop trigger if exists docs_broadcast on public.docs;
create trigger docs_broadcast after insert or update or delete on public.docs for each row execute function public.udf_broadcast();
drop policy if exists udf_topics_read on realtime.messages;
create policy udf_topics_read on realtime.messages for select to authenticated using (
  (select realtime.topic()) = 'udf:pub'
  or (select realtime.topic()) = 'udf:u:' || (select auth.uid())::text
  or (select realtime.topic()) like 'udf:in:%');
