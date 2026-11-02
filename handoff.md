# Ultra Deep Field — handoff

Last updated: 2026-11-01 (America/Phoenix). Current game version: **v220** (`GAME_V` in `docs/index.html`, and `docs/version.json`). Offline cache: **udf-v27**.

**This repo is the master copy of the game.** The claude.ai artifact is `docs/index.html` without the website-only head lines and the service-worker line at the bottom. The Android app and the Desktop launcher are being switched to load this live site. Don't overwrite `docs/index.html` with an older copy from anywhere else.

## What this is
A space empire strategy game ("the GitHub version"), played by friends and family as an installable web app. There is also an older claude.ai artifact copy of the game; this repo is the website build.

- **Live site:** https://gunhypechannel.github.io/Ultradeepfield/
- **Repo:** https://github.com/gunhypechannel/Ultradeepfield (the old lowercase `ultradeepfield` URL redirects; use the new one as `origin`)
- **Hosting:** GitHub Pages serves `docs/` from `main`. A push to `main` is a deploy (live in ~1–2 min).
- **Server:** Supabase project "Ultradeepfield" (`slubtpfnimxtrfcozvhk`). The old Firebase project (`udf-ultra-deep-field`) is the fallback only if `supabase-config.js` isn't filled in.
- **Main test device:** Samsung Galaxy Z Fold 6, usually unfolded (CSS viewport ≈ 884 × 1030 at DPR ~2.1).

## Layout
| Path | What it is |
|---|---|
| `docs/index.html` | The whole game (~2 MB, one file: CSS + JS + inline art). Version notes are comments like `/* v207: … */`. |
| `docs/udf-supabase.js` | Adapter that gives the game a Firestore-like API (`doc().get/set/update/onSnapshot`, `acquire` locks) on top of one Supabase `docs` table, plus the sign-in screen. |
| `docs/supabase-config.js` | Supabase URL and anon key (public by design; RLS protects data). `google: false` until Google sign-in is enabled in Supabase. |
| `docs/udf-firebase.js`, `docs/firebase-config.js`, `firestore.rules`, `firebase.json` | The old Firebase path, kept as a fallback. |
| `docs/sw.js` | Service worker. **Bump `CACHE` (`udf-vN`) on every release** or installed phones keep the old copy. |
| `docs/manifest.webmanifest`, `docs/icons/` | Install-as-app support. |
| `supabase/schema.sql` | Table, row-level security, and the save guard (each save must carry the next `seq`; refuses saves that would wipe a much bigger empire). Run once in Supabase SQL Editor; safe to re-run. |
| `tools/` | Playwright tests against mock servers (`mock-supabase.js`, `mock-firebase*.js`) and an icon generator. |

## How saving works
- The whole empire (`S`: resources, buildings, research, ships, **fleets in flight, stationed guards, timers**) is one JSON blob saved to `data/users/<uid>/save` with `seq`, `sess` (per-tab session id), `savedAt` and a signature.
- Shared world data (planets, players, alliances, joint strikes) lives in separate docs and syncs live.
- Hourly/daily backups go to `data/users/<uid>/backups/`.
- Device-only settings (audio, graphics, key bindings) stay in `localStorage` per device on purpose.

## Changes this session
1. **Tablet / unfolded Fold layout (v207 CSS).** On screens ≥700px, `.gstack` used `margin-inline:auto` inside the flex page column, which shrank Rankings, Quests, Fleets and Alliances to a narrow middle strip. Added `width:100%`.
2. **Seamless device hand-off (v207).**
   - When another device saves, this copy pauses and loads that save in place (`followCloud` → `adoptCloud`) instead of the "Playing on another device" wall + full reload. The wall (`sessTakeover`) now only shows for the "your saved empire is bigger" case.
   - On returning to a backgrounded tab (`visibilitychange` → visible), it reads the server save first and adopts it if newer, before this copy writes anything.
   - `saveSoon()` saves ~0.9 s after any tap / `act()` instead of waiting for the 6 s timer; a save requested mid-write now re-runs after it (`store.again`).
3. **Fleets tab (v208).** Now shows only: fleets in flight (Recall, Hurry, Afterburners, Use boost), joint strikes you're in (add participants, invite, boost), missiles in flight, and ships at each planet with **Deploy** (`fDeploy`: sets launch planet, opens galaxy targets) and **Transport** (`fTransport`: opens the Planets sheet logistics panel with that planet as source). Radar/Hive-raid warnings still appear here only while an attack is inbound. The Plunder & Rewards log moved to the Quests tab; Repair Bay and Jump Gate are on their buildings.

## Testing
Playwright + Chrome are available in the cloud workspace. Pattern used this session:
- Serve `docs/` with `python3 -m http.server`, route `cdn.jsdelivr.net/**` to `tools/mock-supabase.js`, abort other external requests, sign up through the in-game form, wait ~9 s.
- Game variables are top-level `let/const` inside the page script, so they are **not** on `window`. `tools/test_supabase.py` and `tools/test_v205.py` reference a `window.__T` hook that no longer exists in `index.html`; to test, inject one when serving the page (e.g. replace `function saveSoon() {` with `window.__T={get S(){return S},store,…};function saveSoon() {` in the served HTML).
- The mock exposes `window.__sbRows` (server rows) and `window.__sbServerWrite(path, data)` (simulate another device's write).
- Fold 6 unfolded viewport: 884 × 1030, `device_scale_factor` 2.1, `is_mobile`, `has_touch`.

## Not yet verified / open items
- **Transport button** wasn't tested end-to-end (test account had one planet). Check on a real account with 2+ planets.
- **Simultaneous play on two devices:** a tap made in the ~1 s before the other device's save arrives can still be lost. Normal switching is covered.
- Leaving a page relies on an async save on `visibilitychange`/`pagehide`; with `saveSoon()` the gap is ~1 s.
- Google sign-in on Supabase is off (`google: false`).
- `README.md` still describes the Firebase setup and should be updated for Supabase.
- `tools/test_*.py` need the `__T` hook restored or the injection approach above.

## Release checklist
1. Edit `docs/index.html` (add a `/* vNNN: … */` note by the change).
2. Bump `CACHE` in `docs/sw.js`, **and bump `GAME_V` in `docs/index.html` and `docs/version.json` to the same new number.** Open games check `version.json` every 2 minutes and when the tab comes back, and show an "Update now" bar when it's newer than their `GAME_V` (v220).
3. Run a Playwright check at phone (390 × 844) and Fold (884 × 1030) sizes.
4. `git fetch origin main && git rebase origin/main`, commit, push to `main`.
5. Publish the same game to the claude.ai artifact (https://claude.ai/artifact/YSphcWgn5cKuSSYNPhD8hP): `docs/index.html` without the website-only lines.

## Recent versions
- **v215:** the Citadel Supercarrier launches twice as many, smaller fighters (16–28).
- **v216:** Cube champion titles (`allyGlory`, `gloryPill`, `gloryBanner`) on the alliance page, alliance list and sheet, Rankings and profile cards; a "Holding the Cube" badge during a live battle.
- **v217–v219:** the Void Concord bot pact is disbanded. Each player's 30 nearest bots (`FRIEND_BOTS`, `S.friendBots`, the same as `allyBots()`) are friendly and join joint strikes; the other 970 are hostile to everyone and raid colonies. (v218 was taken by an app build that changed only `sw.js`.)
- **v220:** `GAME_V` plus `version.json` "Update now" bar; the service worker always asks the server for fresh files (no 10-minute browser cache).
