/* Ultra Deep Field: Firebase connection layer.
   The game was built for claude.ai, where the page asks window.claude.use("db") and use("user") for the shared galaxy.
   This file provides the same two services on top of Firebase (Firestore for the galaxy, Firebase Auth for logins),
   so the game itself runs unchanged on its own website. Settings live in firebase-config.js. */
(function () {
  "use strict";
  var CFG = window.UDF_FIREBASE || {};
  var SDK = "https://www.gstatic.com/firebasejs/10.12.2/";
  var configured = !!(CFG.apiKey && CFG.projectId && String(CFG.apiKey).indexOf("PASTE") < 0);

  function loadScript(src) {
    return new Promise(function (ok, fail) {
      var s = document.createElement("script"); s.src = src; s.async = false;
      s.onload = ok; s.onerror = function () { fail(new Error("Couldn't load " + src)); };
      document.head.appendChild(s);
    });
  }
  var sdkReady = null;
  function loadSdk() {
    if (!sdkReady) sdkReady = loadScript(SDK + "firebase-app-compat.js")
      .then(function () { return Promise.all([loadScript(SDK + "firebase-auth-compat.js"), loadScript(SDK + "firebase-firestore-compat.js")]); })
      .then(function () {
        var conf = Object.assign({}, CFG); delete conf.ownerUids;
        /* on Firebase Hosting, sign in through the game's own address: Safari blocks the cross-site cookie the default needs */
        if (/\.(web\.app|firebaseapp\.com)$/.test(location.hostname) || (CFG.customDomain && location.hostname === CFG.customDomain)) conf.authDomain = location.hostname;
        var app = firebase.initializeApp(conf);
        var fs = firebase.firestore();
        try { fs.settings({ ignoreUndefinedProperties: true }); } catch (e) {}
        try { fs.enablePersistence({ synchronizeTabs: true }).catch(function () {}); } catch (e) {}
        return { app: app, auth: firebase.auth(), fs: fs };
      });
    return sdkReady;
  }

  /* ---------- errors: Firebase codes → the codes the game already handles ---------- */
  var CODE = { "permission-denied": "not_granted", "unauthenticated": "not_granted", "resource-exhausted": "quota_exceeded", "invalid-argument": "invalid_argument", "not-found": "invalid_argument", "failed-precondition": "invalid_argument" };
  function mapErr(e) {
    var c = String((e && e.code) || "").replace(/^(firestore|auth)\//, "");
    var out = new Error((e && e.message) || String(e)); out.code = CODE[c] || c.replace(/-/g, "_") || "unknown"; out.cause = e; return out;
  }
  function guard(p) { return p.catch(function (e) { throw mapErr(e); }); }
  function isPlain(v) { return v && typeof v === "object" && !Array.isArray(v) && Object.getPrototypeOf(v) === Object.prototype; }

  /* claude.ai's update() deep-merges nested objects: { gifts: { a: 1 } } adds gifts.a and keeps the other gifts.
     Firestore's update() would replace the whole gifts map, so nested objects become field paths. */
  function flatten(o, pre, out) {
    Object.keys(o).forEach(function (k) {
      var v = o[k], p = pre.concat(k);
      if (v === undefined) return;
      if (isPlain(v) && Object.keys(v).length) flatten(v, p, out); else if (!(isPlain(v) && !Object.keys(v).length)) out.push([p, v]);
    });
    return out;
  }

  function wrapQuery(q) {
    return {
      where: function (f, op, v) { return wrapQuery(q.where(f, op, v)); },
      orderBy: function (f, d) { return wrapQuery(q.orderBy(f, d)); },
      limit: function (n) { return wrapQuery(q.limit(n)); },
      get: function () { return guard(q.get()); },
      onSnapshot: function (next, err) { return q.onSnapshot(next, function (e) { if (err) err(mapErr(e)); }); },
      doc: q.doc ? function (id) { return wrapDoc(q.doc(id)); } : undefined
    };
  }
  function wrapDoc(ref) {
    var fs = ref.firestore;
    return {
      id: ref.id, path: ref.path,
      get: function () { return guard(ref.get()); },
      set: function (d) { return guard(ref.set(d)); },
      delete: function () { return guard(ref.delete()); },
      update: function (d) {
        var pairs = flatten(d || {}, [], []); if (!pairs.length) return Promise.resolve();
        var args = []; pairs.forEach(function (p) { args.push(new firebase.firestore.FieldPath(...p[0].map(String)), p[1]); });
        return guard(ref.update.apply(ref, args));
      },
      onSnapshot: function (next, err) { return ref.onSnapshot(next, function (e) { if (err) err(mapErr(e)); }); },
      collection: function (c) { return wrapQuery(ref.collection(c)); },
      /* a short lease so only one player at a time edits a busy record (the Cube battle, joint strikes, joining the galaxy) */
      acquire: function (o) {
        var holder = (o && o.holder) || "?", ttl = Math.min(Math.max(+(o && o.ttlMs) || 10000, 1000), 60000);
        var lref = fs.doc("_locks/" + ref.path.replace(/\//g, "~"));
        return fs.runTransaction(function (tx) {
          return tx.get(lref).then(function (s) {
            var T = Date.now(), d = s.exists ? s.data() : null;
            if (d && d.until > T && d.holder !== holder) return { acquired: false, holder: d.holder, until: d.until };
            tx.set(lref, { holder: holder, until: T + ttl }); return { acquired: true, until: T + ttl };
          });
        }).catch(function () { return { acquired: false }; });
      }
    };
  }
  function makeDb(fs) {
    return {
      doc: function (p) { return wrapDoc(fs.doc(p)); },
      collection: function (p) { return wrapQuery(fs.collection(p)); }
    };
  }

  /* ---------- sign-in screen ---------- */
  var css = "#udfAuth{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:20px;background:radial-gradient(120% 70% at 50% 0%,#0f2230 0%,#05090f 70%);font-family:'Barlow Semi Condensed',Arial,sans-serif;color:#d5e4ec}" +
    "#udfAuth .bx{width:min(380px,100%);display:flex;flex-direction:column;gap:12px}" +
    "#udfAuth .logo{width:88px;height:88px;margin:0 auto 4px;border-radius:22px;background:url(icons/icon-192.png) center/cover;box-shadow:0 0 30px rgba(85,214,232,.35)}" +
    "#udfAuth h1{margin:0;text-align:center;font:800 26px 'Oxanium',sans-serif;letter-spacing:.06em;color:#eaf6fb}" +
    "#udfAuth p{margin:0;text-align:center;color:#7d95a5;font-size:14px}" +
    "#udfAuth button,#udfAuth input{font:inherit;font-size:16px;border-radius:12px;padding:13px 14px;width:100%;box-sizing:border-box}" +
    "#udfAuth input{background:#05090f;border:1px solid #2c5468;color:#eaf6fb;user-select:text;-webkit-user-select:text}" +
    "#udfAuth .g{background:#fff;color:#1f1f1f;border:0;font-weight:600;display:flex;align-items:center;justify-content:center;gap:10px}" +
    "#udfAuth .p{background:rgba(85,214,232,.18);border:1px solid #55d6e8;color:#55d6e8;font:700 15px 'Oxanium',sans-serif;letter-spacing:.06em;text-transform:uppercase}" +
    "#udfAuth .l{background:none;border:0;color:#55d6e8;padding:6px;font-size:14px;text-decoration:underline}" +
    "#udfAuth .or{display:flex;align-items:center;gap:10px;color:#7d95a5;font-size:12px;letter-spacing:.14em}#udfAuth .or:before,#udfAuth .or:after{content:'';flex:1;height:1px;background:#1d3647}" +
    "#udfAuth .er{min-height:18px;color:#ff6262;font-size:14px;text-align:center}#udfAuth .ok{color:#71df90}" +
    "#udfAuth .row{display:flex;justify-content:space-between}";
  var GICON = '<svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.7 13.2l7.9 6.2C12.5 13.6 17.8 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.4 5.7c4.3-4 6.9-9.9 6.9-17.1z"/><path fill="#FBBC05" d="M10.6 28.6c-.5-1.4-.8-2.9-.8-4.6s.3-3.2.8-4.6l-7.9-6.2C1 16.6 0 20.2 0 24s1 7.4 2.7 10.8l7.9-6.2z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.4-5.7c-2.1 1.4-4.8 2.3-8.5 2.3-6.2 0-11.5-4.1-13.4-9.7l-7.9 6.2C6.6 42.6 14.6 48 24 48z"/></svg>';

  function signInScreen(auth) {
    return new Promise(function (resolve) {
      var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
      var w = document.createElement("div"); w.id = "udfAuth"; document.body.appendChild(w);
      var mode = "in", signingUp = null; /* a new account finishes setting its commander name before the game starts */
      function draw(msg, okMsg) {
        var up = mode === "up", reset = mode === "reset";
        w.innerHTML = '<form class="bx" novalidate><div class="logo"></div><h1>ULTRA DEEP FIELD</h1><p>' + (reset ? "We'll email you a link to set a new password." : up ? "Create your commander account." : "Sign in to join the galaxy.") + '</p>' +
          (reset ? "" : '<button type="button" class="g" data-a="google">' + GICON + 'Continue with Google</button><div class="or">OR</div>') +
          (up ? '<input name="n" autocomplete="nickname" placeholder="Commander name" maxlength="24">' : "") +
          '<input name="e" type="email" autocomplete="email" placeholder="Email" inputmode="email">' +
          (reset ? "" : '<input name="p" type="password" autocomplete="' + (up ? "new-password" : "current-password") + '" placeholder="Password' + (up ? ' (6+ characters)' : "") + '">') +
          '<div class="er' + (okMsg ? " ok" : "") + '" role="alert">' + (msg || okMsg || "") + '</div>' +
          '<button type="submit" class="p">' + (reset ? "Send reset link" : up ? "Create account" : "Sign in") + '</button>' +
          '<div class="row">' + (mode === "in" ? '<button type="button" class="l" data-a="up">New here? Create account</button><button type="button" class="l" data-a="reset">Forgot password?</button>' : '<button type="button" class="l" data-a="in">Back to sign in</button>') + '</div></form>';
      }
      function fail(e) {
        var c = String((e && e.code) || "").replace("auth/", "");
        var t = { "invalid-email": "That email doesn't look right.", "missing-password": "Enter your password.", "weak-password": "Use at least 6 characters.", "email-already-in-use": "That email already has an account. Sign in instead.", "invalid-credential": "Wrong email or password.", "wrong-password": "Wrong email or password.", "user-not-found": "No account with that email.", "too-many-requests": "Too many tries. Wait a minute and try again.", "network-request-failed": "No connection. Check your internet.", "popup-closed-by-user": "", "cancelled-popup-request": "", "unauthorized-domain": "This web address isn't approved in Firebase yet (Authentication → Settings → Authorized domains)." }[c];
        say(t != null ? t : "Couldn't sign in (" + (c || "error") + ").");
      }
      /* show a message without redrawing, so what the player typed stays in the boxes */
      function say(t) { var el = w.querySelector(".er"); if (!el) return draw(t); el.className = "er"; el.textContent = t; }
      w.addEventListener("click", function (e) {
        var b = e.target.closest("[data-a]"); if (!b) return; e.preventDefault();
        var a = b.getAttribute("data-a");
        if (a === "google") {
          var prov = new firebase.auth.GoogleAuthProvider(); prov.setCustomParameters({ prompt: "select_account" });
          auth.signInWithPopup(prov).catch(function (err) {
            var c = String(err && err.code);
            if (/popup-blocked|operation-not-supported/.test(c)) return auth.signInWithRedirect(prov).catch(fail);
            fail(err);
          });
        } else { mode = a; draw(); }
      });
      w.addEventListener("submit", function (e) {
        e.preventDefault(); var f = e.target, em = (f.e.value || "").trim();
        if (mode === "reset") { auth.sendPasswordResetEmail(em).then(function () { mode = "in"; draw("", "Check your email for the reset link."); }, fail); return; }
        var pw = f.p.value || "";
        if (mode === "up") {
          var nm = (f.n.value || "").trim().slice(0, 24); if (nm.length < 2) return say("Pick a commander name (2+ characters).");
          signingUp = auth.createUserWithEmailAndPassword(em, pw).then(function (cr) { return cr.user.updateProfile({ displayName: nm }); }).catch(function (err) { signingUp = null; fail(err); });
        } else auth.signInWithEmailAndPassword(em, pw).catch(fail);
      });
      draw();
      var off = auth.onAuthStateChanged(function (u) { if (u) Promise.resolve(signingUp).then(function () { off(); w.remove(); resolve(auth.currentUser || u); }); });
    });
  }

  /* ---------- the window.claude.use() the game expects ---------- */
  var session = null;
  function start() {
    if (session) return session;
    session = loadSdk().then(function (fb) {
      return new Promise(function (ok) {
        var first = fb.auth.onAuthStateChanged(function (u) { first(); ok(u); });
      }).then(function (u) { return u || signInScreen(fb.auth); }).then(function (u) {
        fb.user = u;
        /* public commander name, so other players see who you are */
        var nm = (u.displayName || (u.email || "").split("@")[0] || "Commander").slice(0, 24);
        fb.fs.doc("profiles/" + u.uid).set({ name: nm, at: Date.now() }, { merge: true }).catch(function () {});
        return fb;
      });
    }).catch(function (e) { console.warn("Firebase unavailable:", e); return null; });
    return session;
  }
  function makeUser(fb) {
    var cache = {};
    return {
      id: function () { return Promise.resolve(fb.user.uid); },
      me: function () { var u = fb.auth.currentUser || fb.user; return Promise.resolve({ id: u.uid, name: u.displayName || (u.email || "").split("@")[0] || "", guest: false }); },
      isOwner: function () { return Promise.resolve((CFG.ownerUids || []).indexOf(fb.user.uid) >= 0); },
      canEdit: function () { return Promise.resolve((CFG.ownerUids || []).indexOf(fb.user.uid) >= 0); },
      can: function () { return Promise.resolve(true); },
      profiles: function (ids) {
        var want = (ids || []).filter(function (id) { return typeof id === "string" && id.length > 10 && !(cache[id] && Date.now() - cache[id].t < 300000); });
        return Promise.all(want.slice(0, 200).map(function (id) {
          return fb.fs.doc("profiles/" + id).get().then(function (s) { cache[id] = { t: Date.now(), name: s.exists ? String(s.data().name || "") : "" }; }, function () {});
        })).then(function () { var o = {}; (ids || []).forEach(function (id) { if (cache[id]) o[id] = { id: id, name: cache[id].name }; }); return o; });
      }
    };
  }
  var memo = {};
  window.claude = {
    use: function (name) {
      if (!configured) return Promise.resolve(null);
      if (name !== "db" && name !== "user") return Promise.resolve(null);
      if (!memo[name]) memo[name] = start().then(function (fb) { return fb ? (name === "db" ? makeDb(fb.fs) : makeUser(fb)) : null; });
      return memo[name];
    }
  };
  window.udfAccount = {
    label: function () { var u = sdkReady && window.firebase && firebase.auth().currentUser; return u ? (u.email || u.displayName || "Signed in") : "Not signed in"; },
    signOut: function () { if (!window.firebase) return; firebase.auth().signOut().then(function () { location.reload(); }); }
  };
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-act=udfSignOut]"); if (!b) return;
    e.preventDefault(); e.stopPropagation(); if (confirm("Sign out of Ultra Deep Field on this device?")) window.udfAccount.signOut();
  }, true);
  if (configured) start(); /* show the sign-in screen right away instead of waiting for the game to ask */
})();
