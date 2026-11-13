# Ultra Deep Field

A space empire strategy game. Build up your homeworld, form alliances and fight for the galaxy with friends.

**Play:** https://gunhypechannel.github.io/Ultradeepfield/

## What's here
- `docs/` — the game website (served by GitHub Pages from `main`; a push to `main` is a deploy)
  - `index.html` — the game
  - `udf-supabase.js` — connects the game to Supabase (sign-in and the shared galaxy)
  - `supabase-config.js` — this project's Supabase URL and public key (public by design)
  - `udf-firebase.js`, `firebase-config.js` — the old Firebase connection, used only if `supabase-config.js` is empty
  - `voice/` — the Advisor's voice clips (made with `voicelab.html`), `art/` — boss and ship art
  - `manifest.webmanifest`, `sw.js`, `icons/` — lets phones install it like an app
- `supabase/` — the server: `schema.sql`, `migrations/`, and the `settle_fight` Edge Function that checks boss fights
- `tools/patches/` — every game change as a script, applied in version order
- `tools/` — voice tools, icon generator and older local tests
- `handoff.md` — the full change log and open items; start there
- `firestore.rules`, `firebase.json` — the old Firebase setup, kept as the fallback
