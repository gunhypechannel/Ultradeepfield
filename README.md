# Ultra Deep Field

A space empire strategy game. Build up your homeworld, form alliances and fight for the galaxy with friends.

**Play:** https://gunhypechannel.github.io/Ultradeepfield/

## What's here
- `docs/` — the game website (served by GitHub Pages)
  - `index.html` — the game
  - `udf-firebase.js` — connects the game to Firebase (sign-in and the shared galaxy)
  - `firebase-config.js` — this project's Firebase settings (public by design)
  - `manifest.webmanifest`, `sw.js`, `icons/` — lets phones install it like an app
- `firestore.rules` — database security rules (paste into Firebase console → Firestore → Rules)
- `firebase.json` — settings if you ever deploy with Firebase Hosting instead
- `tools/` — icon generator and a local test that runs the game against a fake Firebase
