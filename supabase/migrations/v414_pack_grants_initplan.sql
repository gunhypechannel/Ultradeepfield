-- v414 (applied 2026-11-10): the Supabase advisor's 'Auth RLS Initialization Plan' warning: check the signed-in player once per query, not per row
alter policy pack_grants_own on public.pack_grants using (uid = (select auth.uid()));
