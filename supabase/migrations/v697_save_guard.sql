-- v697: an old copy of the game can no longer overwrite an empire. Saves must say which game version wrote them (gv) and come from
-- v697 or later (both rollbacks on 2026-11-20 were old versions waking up on another device). Whenever a save comes from a different
-- device or tab than the one before, the save it replaces is kept in backups/k0..k7 (the game's Restore list shows them as
-- "Replaced by another device").
create or replace function public.save_guard() returns trigger language plpgsql security definer set search_path = public as $$
declare os numeric; ns numeric; ol numeric; nl numeric; uid text; slot int;
begin
  if new.path ~ '^data/users/[^/]+/save$' then
    if coalesce((new.data->>'gv')::numeric, 0) < 697 then raise exception 'update the game to save' using errcode = '42501'; end if;
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
    if old.data ? 'json' and (old.data->>'sess') is distinct from (new.data->>'sess') then
      uid := split_part(new.path, '/', 3); slot := (floor(extract(epoch from now()) / 60)::bigint % 8)::int;
      insert into public.docs (path, col, data, updated_at)
      values ('data/users/' || uid || '/backups/k' || slot, 'data/users/' || uid || '/backups',
              jsonb_build_object('v', 3, 'at', coalesce((old.data->>'savedAt')::numeric, extract(epoch from now()) * 1000), 'json', old.data->>'json', 'sig', old.data->>'sig', 'lv', old.data->'lv', 'ships', old.data->'ships', 'kept', true), now())
      on conflict (path) do update set data = excluded.data, updated_at = excluded.updated_at;
    end if;
  end if;
  return new;
end $$;
