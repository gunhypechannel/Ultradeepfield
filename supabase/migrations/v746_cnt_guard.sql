-- v746 the Resurrection War's rules, enforced by the server on every write to the live war record (event/cnt):
-- a destroyed Ark or a commander gone for good stays gone, an Ark never heals or regains rebuild capacity, a commander is rebuilt
-- only while its Ark lives, has capacity (spent in the same write) and keeps a relay up, a relay rebuilds only 12 hours after it
-- fell and only while its Ark lives, contributions and damage shares change only for the writer and within bounds, and the
-- finale's outcome, once decided, never changes.
create or replace function public.cnt_guard() returns trigger language plpgsql set search_path to 'public' as $function$
declare me text := auth.uid()::text; o jsonb; n jsonb; k text; dv numeric; dsum numeric := 0; id text; oa jsonb; na jsonb; reg text; ups int; tnow numeric := extract(epoch from now()) * 1000;
begin
  if me is null or new.path <> 'event/cnt' then return new; end if;
  n := coalesce(new.data, '{}'::jsonb);
  o := case when tg_op = 'UPDATE' then coalesce(old.data, '{}'::jsonb) else '{}'::jsonb end;
  if coalesce(o->>'k', '') <> coalesce(n->>'k', '') then o := '{}'::jsonb; end if;
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
  if coalesce((n->>'sup')::numeric, 0) - coalesce((o->>'sup')::numeric, 0) > dsum then raise exception 'cnt: war points grew without contribution'; end if;
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
drop trigger if exists d_cnt_guard on public.docs;
create trigger d_cnt_guard before insert or update on public.docs for each row when (new.path = 'event/cnt') execute function public.cnt_guard();
