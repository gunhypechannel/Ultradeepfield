/* Ultra Deep Field: Supabase settings (Supabase dashboard → Project Settings → API).
   The URL and the anon / publishable key are meant to be public; the row-level security in supabase/schema.sql protects the data.
   While these say PASTE, the game keeps using the old Firebase server. */
window.UDF_SUPABASE = {
  url: "PASTE_PROJECT_URL",
  anonKey: "PASTE_ANON_KEY",
  google: false /* true once Google sign-in is switched on in Supabase → Authentication → Providers */
};
