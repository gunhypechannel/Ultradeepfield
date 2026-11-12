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
