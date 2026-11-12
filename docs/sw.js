/* Ultra Deep Field service worker: lets phones install the game and opens it fast.
   The game page is always fetched fresh when online (so updates show up), with the last copy as a fallback offline.
   Galaxy data never goes through here: Firebase handles that itself. */
const CACHE = "udf-v282";
const MODELS = "udf-models"; // v356 3D models: fingerprinted file names, kept across updates
const SHELL = ["./", "./index.html", "./udf-firebase.js", "./firebase-config.js", "./udf-supabase.js", "./udf-install.js", "./art/login.webp", "./supabase-config.js", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== MODELS).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== "GET") return;
  const same = u.origin === location.origin;
  /* v284: music and video go straight to the network. Rebuilding one of these requests below removed its Range header, so every seek downloaded the whole file,
     Safari can refuse media served that way, and a failed download came back as the game's HTML page. */
  if (same && (r.headers.has("range") || r.destination === "audio" || r.destination === "video" || /\.(mp3|mp4)$/.test(u.pathname))) return;
  const lib = /^(fonts\.(googleapis|gstatic)\.com|cdnjs\.cloudflare\.com|www\.gstatic\.com|cdn\.jsdelivr\.net)$/.test(u.hostname) && !/firestore|identitytoolkit|securetoken/.test(u.href);
  if (same && /\/models\/.+\.glb$/.test(u.pathname)) { // v356 cache-first: a model file only changes with its fingerprint
    e.respondWith(caches.open(MODELS).then(c => c.match(r).then(m => m || fetch(r).then(res => { if (res.ok) { c.put(r, res.clone()); c.keys().then(ks => { const name = u.pathname.split("/").pop(), sub = u.pathname.includes("/m/"); ks.filter(q => { const qu = new URL(q.url); return qu.pathname.split("/").pop() === name && qu.pathname.includes("/m/") === sub && qu.search !== u.search; }).forEach(q => c.delete(q)); }); } return res; })))); return; }
  if (same && !u.pathname.startsWith("/__/")) {
    // network first for our own files, so a new version of the game shows up on the next open
    /* v220: ask the server every time (a quick "has it changed?" check), never the browser's own 10-minute copy, so a new
       version shows up on the very next open. version.json is never cached at all. */
    const fresh = u.pathname.endsWith("/version.json") ? new Request(r, { cache: "no-store" }) : r.mode === "navigate" ? new Request(r.url, { cache: "no-cache", credentials: "same-origin" }) : new Request(r, { cache: "no-cache" });
    if (u.pathname.endsWith("/version.json")) { e.respondWith(fetch(fresh)); return; }
    e.respondWith(fetch(fresh).then(res => { if (res.ok) { const cp = res.clone(); caches.open(CACHE).then(c => c.put(r, cp)); } return res; })
      .catch(() => caches.match(r).then(m => m || (r.mode === "navigate" ? caches.match("./index.html") : Response.error()))));
  } else if (lib) {
    // fonts, 3D engine and Firebase libraries rarely change: cache first
    e.respondWith(caches.match(r).then(m => m || fetch(r).then(res => { if (res.ok || res.type === "opaque") { const cp = res.clone(); caches.open(CACHE).then(c => c.put(r, cp)); } return res; })));
  }
});
