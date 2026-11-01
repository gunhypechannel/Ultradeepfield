/* Ultra Deep Field service worker: lets phones install the game and opens it fast.
   The game page is always fetched fresh when online (so updates show up), with the last copy as a fallback offline.
   Galaxy data never goes through here: Firebase handles that itself. */
const CACHE = "udf-v21";
const SHELL = ["./", "./index.html", "./udf-firebase.js", "./firebase-config.js", "./udf-supabase.js", "./supabase-config.js", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== "GET") return;
  const same = u.origin === location.origin;
  const lib = /^(fonts\.(googleapis|gstatic)\.com|cdnjs\.cloudflare\.com|www\.gstatic\.com|cdn\.jsdelivr\.net)$/.test(u.hostname) && !/firestore|identitytoolkit|securetoken/.test(u.href);
  if (same && !u.pathname.startsWith("/__/")) {
    // network first for our own files, so a new version of the game shows up on the next open
    e.respondWith(fetch(r).then(res => { if (res.ok) { const cp = res.clone(); caches.open(CACHE).then(c => c.put(r, cp)); } return res; })
      .catch(() => caches.match(r).then(m => m || caches.match("./index.html"))));
  } else if (lib) {
    // fonts, 3D engine and Firebase libraries rarely change: cache first
    e.respondWith(caches.match(r).then(m => m || fetch(r).then(res => { if (res.ok || res.type === "opaque") { const cp = res.clone(); caches.open(CACHE).then(c => c.put(r, cp)); } return res; })));
  }
});
