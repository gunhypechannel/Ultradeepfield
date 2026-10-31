/* Ultra Deep Field: Supabase connection layer.
   The game was built for claude.ai, where the page asks window.claude.use("db") and use("user") for the shared galaxy.
   This file provides the same two services on top of Supabase (one Postgres table of records for the galaxy, Supabase Auth
   for logins), so the game itself runs unchanged on its own website. Settings live in supabase-config.js; the database
   setup is supabase/schema.sql. It also offers a one-time move of your empire from the old Firebase server. */
(function () {
  "use strict";
  var CFG = window.UDF_SUPABASE || {};
  var LIB = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js";
  var configured = !!(CFG.url && CFG.anonKey && String(CFG.url + CFG.anonKey).indexOf("PASTE") < 0);
  var RECOVERY = /type=recovery/.test(location.hash); /* opened from a "set a new password" email */
  var HERE = location.origin + location.pathname;

  function loadScript(src) {
    return new Promise(function (ok, fail) {
      var s = document.createElement("script"); s.src = src; s.async = false;
      s.onload = ok; s.onerror = function () { fail(new Error("Couldn't load " + src)); };
      document.head.appendChild(s);
    });
  }
  var sb = null, sdkReady = null;
  function loadSdk() {
    if (!sdkReady) sdkReady = (window.supabase && window.supabase.createClient ? Promise.resolve() : loadScript(LIB)).then(function () {
      sb = window.supabase.createClient(CFG.url, CFG.anonKey, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, storageKey: "udf.auth" } });
      return sb;
    });
    return sdkReady;
  }

  /* ---------- errors: database codes → the codes the game already handles ---------- */
  var CODE = { "42501": "not_granted", "P0002": "invalid_argument", "22023": "invalid_argument", "23505": "invalid_argument", "22P02": "invalid_argument", "PGRST116": "invalid_argument" };
  function mapErr(e) {
    var c = String((e && e.code) || ""), m = (e && e.message) || String(e);
    var out = new Error(m); out.cause = e;
    out.code = CODE[c] || (/JWT|PGRST30/.test(c + m) ? "unavailable" : /fetch|network|Failed|timeout|ECONN/i.test(m) ? "unavailable" : c ? c.toLowerCase() : "unknown");
    return out;
  }
  function run(q) { return Promise.resolve(q).then(function (r) { if (r && r.error) throw mapErr(r.error); return r ? r.data : null; }, function (e) { throw mapErr(e); }); }
  function clone(v) { return v === undefined || v === null ? v : JSON.parse(JSON.stringify(v)); }
  function strip(v) { if (Array.isArray(v)) return v.map(function (x) { return x === undefined ? null : strip(x); }); if (v && typeof v === "object") { var o = {}; for (var k in v) if (v[k] !== undefined) o[k] = strip(v[k]); return o; } return v; }
  var colOf = function (p) { return p.replace(/\/[^/]*$/, ""); };

  function dsnap(path, data) {
    var has = data !== undefined && data !== null;
    return { id: path.split("/").pop(), ref: { path: path }, exists: has, data: function () { return has ? clone(data) : undefined; } };
  }

  /* ---------- live updates: one channel for the whole table, handed out to whoever listens to a record or collection ---------- */
  var docL = {}, colL = {}, refreshers = [], chan = null, chanDown = false;
  function addL(map, k, fn) { (map[k] = map[k] || []).push(fn); return function () { var a = map[k]; if (!a) return; var i = a.indexOf(fn); if (i >= 0) a.splice(i, 1); if (!a.length) delete map[k]; }; }
  function emit(path, data) {
    (docL[path] || []).slice().forEach(function (fn) { try { fn(data); } catch (e) { console.error(e); } });
    (colL[colOf(path)] || []).slice().forEach(function (fn) { try { fn(path, data); } catch (e) { console.error(e); } });
  }
  function refetch(path) { run(sb.from("docs").select("path,data").eq("path", path).maybeSingle()).then(function (r) { emit(path, r ? r.data : null); }, function () {}); }
  function onChange(p) {
    if (!p) return;
    if (p.eventType === "DELETE") { var op = p.old && p.old.path; if (op) emit(op, null); return; }
    var r = p.new || {}; if (!r.path) return;
    if (!docL[r.path] && !colL[colOf(r.path)]) return;
    if (r.data === undefined || r.data === null || (p.errors && p.errors.length)) refetch(r.path); /* too big to arrive live: read it */
    else emit(r.path, r.data);
  }
  function startLive() {
    if (chan) return;
    chan = sb.channel("udf-docs").on("postgres_changes", { event: "*", schema: "public", table: "docs" }, onChange)
      .subscribe(function (status) {
        if (status === "SUBSCRIBED") { if (chanDown) { chanDown = false; refreshers.slice().forEach(function (f) { try { f(); } catch (e) {} }); } } /* back online: catch up */
        else if (status === "CHANNEL_ERROR" || status === "TIMED_OUT" || status === "CLOSED") chanDown = true;
      });
  }

  /* ---------- the database the game expects (the same shape as claude.ai's) ---------- */
  function matches(f, d) {
    return f.every(function (w) {
      var v = d ? d[w[0]] : undefined;
      if (w[1] === "==") return v === w[2];
      if (w[1] === "array-contains") return Array.isArray(v) && v.indexOf(w[2]) >= 0;
      return true;
    });
  }
  function Query(col, f, lim) { this.col = col; this.f = f || []; this.lim = lim || 1000; }
  Query.prototype.where = function (a, op, v) { return new Query(this.col, this.f.concat([[a, op, v]]), this.lim); };
  Query.prototype.orderBy = function () { return this; };
  Query.prototype.limit = function (n) { return new Query(this.col, this.f, Math.min(+n || 1000, 1000)); };
  Query.prototype.doc = function (id) { return new Doc(this.col + "/" + id); };
  Query.prototype._fetch = function () {
    var q = sb.from("docs").select("path,data").eq("col", this.col);
    this.f.forEach(function (w) {
      if (w[1] === "==") q = w[2] === null ? q.is("data->" + w[0], null) : typeof w[2] === "object" ? q.filter("data->" + w[0], "eq", JSON.stringify(w[2])) : q.filter("data->>" + w[0], "eq", String(w[2]));
      else if (w[1] === "array-contains") q = q.filter("data->" + w[0], "cs", JSON.stringify([w[2]]));
    });
    return run(q.limit(this.lim)).then(function (rows) { return rows || []; });
  };
  function qsnap(map, changes) {
    var docs = Object.keys(map).map(function (p) { return dsnap(p, map[p]); });
    return { docs: docs, size: docs.length, empty: !docs.length, docChanges: function () { return changes; }, forEach: function (fn) { docs.forEach(fn); } };
  }
  Query.prototype.get = function () {
    return this._fetch().then(function (rows) { var m = {}; rows.forEach(function (r) { m[r.path] = r.data; }); return qsnap(m, []); });
  };
  Query.prototype.onSnapshot = function (next, err) {
    var q = this, map = {}, ready = false, alive = true, early = [];
    function send(changes) { if (!alive) return; try { next(qsnap(map, changes)); } catch (e) { console.error(e); } }
    function apply(path, data) {
      var had = Object.prototype.hasOwnProperty.call(map, path), keep = data !== null && data !== undefined && matches(q.f, data);
      if (keep) { if (had && JSON.stringify(map[path]) === JSON.stringify(data)) return null; map[path] = data; return { type: had ? "modified" : "added", doc: dsnap(path, data) }; }
      if (had) { var old = map[path]; delete map[path]; return { type: "removed", doc: dsnap(path, old) }; }
      return null;
    }
    var off = addL(colL, q.col, function (path, data) { if (!ready) { early.push([path, data]); return; } var c = apply(path, data); if (c) send([c]); });
    function load(first) {
      return q._fetch().then(function (rows) {
        if (!alive) return; var fresh = {}; rows.forEach(function (r) { fresh[r.path] = r.data; });
        var changes = [];
        if (first) { map = fresh; ready = true; early.forEach(function (e) { apply(e[0], e[1]); }); early = []; changes = Object.keys(map).map(function (p) { return { type: "added", doc: dsnap(p, map[p]) }; }); send(changes); return; }
        Object.keys(map).forEach(function (p) { if (!fresh.hasOwnProperty(p)) { var c = apply(p, null); if (c) changes.push(c); } });
        Object.keys(fresh).forEach(function (p) { var c = apply(p, fresh[p]); if (c) changes.push(c); });
        if (changes.length) send(changes);
      }, function (e) { if (first && err) err(e); });
    }
    var refresh = function () { if (ready) load(false); }; refreshers.push(refresh);
    load(true);
    return function () { alive = false; off(); var i = refreshers.indexOf(refresh); if (i >= 0) refreshers.splice(i, 1); };
  };

  function Doc(path) { this.path = path; this.id = path.split("/").pop(); }
  Doc.prototype.get = function () { var p = this.path; return run(sb.from("docs").select("path,data").eq("path", p).maybeSingle()).then(function (r) { return dsnap(p, r ? r.data : null); }); };
  Doc.prototype.set = function (d) {
    var p = this.path, data = strip(clone(d || {}));
    return run(sb.from("docs").upsert({ path: p, col: "", top: "", id: "", data: data }, { onConflict: "path" })).then(function () { emit(p, data); });
  };
  Doc.prototype.update = function (d) {
    var p = this.path, patch = strip(clone(d || {})); if (!Object.keys(patch).length) return Promise.resolve();
    return run(sb.rpc("doc_update", { p: p, patch: patch })).then(function (merged) { if (merged) emit(p, merged); });
  };
  Doc.prototype.delete = function () { var p = this.path; return run(sb.from("docs").delete().eq("path", p)).then(function () { emit(p, null); }); };
  Doc.prototype.collection = function (c) { return new Query(this.path + "/" + c); };
  Doc.prototype.onSnapshot = function (next, err) {
    var p = this, last = "\0", alive = true, heard = false;
    function deliver(data) { if (!alive) return; var j = JSON.stringify(data === undefined ? null : data); if (j === last) return; last = j; try { next(dsnap(p.path, data)); } catch (e) { console.error(e); } }
    var off = addL(docL, p.path, function (data) { heard = true; deliver(data); });
    var refresh = function () { p.get().then(function (s) { deliver(s.exists ? s.data() : null); }, function () {}); }; refreshers.push(refresh);
    p.get().then(function (s) { if (!heard) deliver(s.exists ? s.data() : null); }, function (e) { if (err) err(e); });
    return function () { alive = false; off(); var i = refreshers.indexOf(refresh); if (i >= 0) refreshers.splice(i, 1); };
  };
  /* a short lease so only one player at a time edits a busy record (the Cube battle, joint strikes, joining the galaxy) */
  Doc.prototype.acquire = function (o) {
    var holder = (o && o.holder) || "?", ttl = Math.min(Math.max(+(o && o.ttlMs) || 10000, 1000), 60000);
    return run(sb.rpc("doc_acquire", { p: this.path, holder: holder, ttl: ttl, t: Date.now() })).then(function (r) { return r || { acquired: false }; }, function () { return { acquired: false }; });
  };
  var DB = { doc: function (p) { return new Doc(p); }, collection: function (p) { return new Query(p); } };

  /* ---------- sign-in screen ---------- */
  var css = "#udfAuth,#udfOld{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:20px;background:radial-gradient(120% 70% at 50% 0%,#0f2230 0%,#05090f 70%);font-family:'Barlow Semi Condensed',Arial,sans-serif;color:#d5e4ec}" +
    "#udfOld{z-index:400;background:rgba(3,7,12,.92)}" +
    ".udfa .bx{width:min(380px,100%);display:flex;flex-direction:column;gap:12px}" +
    ".udfa .logo{width:88px;height:88px;margin:0 auto 4px;border-radius:22px;background:url(icons/icon-192.png) center/cover;box-shadow:0 0 30px rgba(85,214,232,.35)}" +
    ".udfa h1{margin:0;text-align:center;font:800 26px 'Oxanium',sans-serif;letter-spacing:.06em;color:#eaf6fb}.udfa h2{margin:0;text-align:center;font:800 20px 'Oxanium',sans-serif;color:#eaf6fb}" +
    ".udfa p{margin:0;text-align:center;color:#7d95a5;font-size:14px}" +
    ".udfa button,.udfa input{font:inherit;font-size:16px;border-radius:12px;padding:13px 14px;width:100%;box-sizing:border-box}" +
    ".udfa input{background:#05090f;border:1px solid #2c5468;color:#eaf6fb;user-select:text;-webkit-user-select:text}" +
    ".udfa .g{background:#fff;color:#1f1f1f;border:0;font-weight:600;display:flex;align-items:center;justify-content:center;gap:10px}" +
    ".udfa .p{background:rgba(85,214,232,.18);border:1px solid #55d6e8;color:#55d6e8;font:700 15px 'Oxanium',sans-serif;letter-spacing:.06em;text-transform:uppercase}" +
    ".udfa .l{background:none;border:0;color:#55d6e8;padding:6px;font-size:14px;text-decoration:underline}" +
    ".udfa .or{display:flex;align-items:center;gap:10px;color:#7d95a5;font-size:12px;letter-spacing:.14em}.udfa .or:before,.udfa .or:after{content:'';flex:1;height:1px;background:#1d3647}" +
    ".udfa .er{min-height:18px;color:#ff6262;font-size:14px;text-align:center}.udfa .ok{color:#71df90}" +
    ".udfa .row{display:flex;justify-content:space-between}" +
    ".udfa .pw{position:relative}.udfa .pw input{padding-right:70px}.udfa .pw .eye{position:absolute;right:6px;top:50%;transform:translateY(-50%);width:auto;padding:6px 10px;background:none;border:0;color:#55d6e8;font-size:14px}";
  var GICON = '<svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.7 13.2l7.9 6.2C12.5 13.6 17.8 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.4 5.7c4.3-4 6.9-9.9 6.9-17.1z"/><path fill="#FBBC05" d="M10.6 28.6c-.5-1.4-.8-2.9-.8-4.6s.3-3.2.8-4.6l-7.9-6.2C1 16.6 0 20.2 0 24s1 7.4 2.7 10.8l7.9-6.2z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.4-5.7c-2.1 1.4-4.8 2.3-8.5 2.3-6.2 0-11.5-4.1-13.4-9.7l-7.9 6.2C6.6 42.6 14.6 48 24 48z"/></svg>';
  var cssDone = false;
  function addCss() { if (cssDone) return; cssDone = true; var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function lastEmail() { try { return localStorage.getItem("udf.lastEmail") || ""; } catch (x) { return ""; } }
  function authMsg(e) {
    var m = String((e && (e.message || e.error_description)) || e || "");
    if (/Invalid login credentials/i.test(m)) return "Wrong email or password.";
    if (/Email not confirmed/i.test(m)) return "Confirm your email first: open the link we emailed you, then sign in.";
    if (/already registered|already been registered|User already exists/i.test(m)) return "That email already has an account. Sign in instead.";
    if (/Password should be|weak/i.test(m)) return "Use at least 6 characters.";
    if (/invalid format|valid email|Unable to validate email/i.test(m)) return "That email doesn't look right.";
    if (/rate limit|too many/i.test(m)) return "Too many tries. Wait a minute and try again.";
    if (/provider is not enabled|Unsupported provider/i.test(m)) return "Google sign-in isn't switched on yet. Use email for now.";
    if (/same_password|different from the old/i.test(m)) return "Pick a password different from your old one.";
    if (/fetch|network/i.test(m)) return "No connection. Check your internet.";
    return "Couldn't sign in (" + (m || "error") + ").";
  }

  function signInScreen(startMode) {
    return new Promise(function (resolve) {
      addCss();
      var w = document.createElement("div"); w.id = "udfAuth"; w.className = "udfa"; document.body.appendChild(w);
      var mode = startMode || "in", busy = false, finished = false;
      function draw(msg, okMsg) {
        var up = mode === "up", reset = mode === "reset", np = mode === "newpw";
        var google = CFG.google && !reset && !np;
        w.innerHTML = '<form class="bx" novalidate><div class="logo"></div><h1>ULTRA DEEP FIELD</h1><p>' + (np ? "Choose a new password." : reset ? "We'll email you a link to set a new password." : up ? "Create your commander account." : "Sign in to join the galaxy.") + '</p>' +
          (google ? '<button type="button" class="g" data-a="google">' + GICON + 'Continue with Google</button><div class="or">OR</div>' : "") +
          (up ? '<input name="n" autocomplete="nickname" placeholder="Commander name" maxlength="24">' : "") +
          (np ? "" : '<input name="e" type="email" autocomplete="email" placeholder="Email" inputmode="email" value="' + esc(lastEmail()) + '">') +
          (reset ? "" : '<div class="pw"><input name="p" type="password" autocomplete="' + (up || np ? "new-password" : "current-password") + '" placeholder="' + (np ? "New password" : "Password") + (up || np ? ' (6+ characters)' : "") + '"><button type="button" class="eye" data-a="eye" aria-label="Show password">Show</button></div>') +
          '<div class="er' + (okMsg ? " ok" : "") + '" role="alert">' + esc(msg || okMsg || "") + '</div>' +
          '<button type="submit" class="p">' + (np ? "Save password" : reset ? "Send reset link" : up ? "Create account" : "Sign in") + '</button>' +
          (np ? "" : '<div class="row">' + (mode === "in" ? '<button type="button" class="l" data-a="up">New here? Create account</button><button type="button" class="l" data-a="reset">Forgot password?</button>' : '<button type="button" class="l" data-a="in">Back to sign in</button>') + '</div>') + '</form>';
      }
      function say(t, ok) { var el = w.querySelector(".er"); if (!el) return draw(t); el.className = "er" + (ok ? " ok" : ""); el.textContent = t; }
      function done(u) { if (finished) return; finished = true; try { sub && sub.data && sub.data.subscription.unsubscribe(); } catch (x) {} w.remove(); resolve(u); }
      w.addEventListener("click", function (e) {
        var b = e.target.closest("[data-a]"); if (!b) return; e.preventDefault();
        var a = b.getAttribute("data-a");
        if (a === "google") sb.auth.signInWithOAuth({ provider: "google", options: { redirectTo: HERE, queryParams: { prompt: "select_account" } } }).then(function (r) { if (r && r.error) say(authMsg(r.error)); });
        else if (a === "eye") { var pi = w.querySelector("input[name=p]"); if (pi) { var sh = pi.type === "password"; pi.type = sh ? "text" : "password"; b.textContent = sh ? "Hide" : "Show"; } }
        else { mode = a; draw(); }
      });
      w.addEventListener("submit", function (e) {
        e.preventDefault(); if (busy) return; var f = e.target;
        var em = f.e ? (f.e.value || "").trim() : "", pw = f.p ? f.p.value || "" : "";
        try { if (em) localStorage.setItem("udf.lastEmail", em); } catch (x) {}
        function go(p, then) { busy = true; say("…", true); p.then(function (r) { busy = false; if (r && r.error) return say(authMsg(r.error)); then(r && r.data); }, function (er) { busy = false; say(authMsg(er)); }); }
        if (mode === "newpw") { if (pw.length < 6) return say("Use at least 6 characters."); return go(sb.auth.updateUser({ password: pw }), function (d) { try { history.replaceState(null, "", HERE); } catch (x) {} done(d && d.user); }); }
        if (mode === "reset") return go(sb.auth.resetPasswordForEmail(em, { redirectTo: HERE }), function () { mode = "in"; draw("", "Check your email for the reset link."); });
        if (mode === "up") {
          var nm = (f.n.value || "").trim().slice(0, 24); if (nm.length < 2) return say("Pick a commander name (2+ characters).");
          return go(sb.auth.signUp({ email: em, password: pw, options: { data: { name: nm }, emailRedirectTo: HERE } }), function (d) {
            if (d && d.session) return done(d.user);
            if (d && d.user && Array.isArray(d.user.identities) && !d.user.identities.length) return say("That email already has an account. Sign in instead.");
            mode = "in"; draw("", "Account made. Open the link we just emailed you, then sign in here.");
          });
        }
        go(sb.auth.signInWithPassword({ email: em, password: pw }), function (d) { done(d && d.user); });
      });
      draw();
      /* Google sign-in comes back here with the session already set */
      var sub = sb.auth.onAuthStateChange(function (ev, s) { if (mode !== "newpw" && s && s.user && (ev === "SIGNED_IN" || ev === "INITIAL_SESSION")) setTimeout(function () { done(s.user); }, 0); });
    });
  }

  /* ---------- the window.claude.use() the game expects ---------- */
  var session = null, me = null;
  function nameOf(u) { var md = (u && u.user_metadata) || {}; return String(md.name || md.full_name || (u && u.email || "").split("@")[0] || "Commander").slice(0, 24); }
  function start() {
    if (session) return session;
    session = loadSdk().then(function () { return sb.auth.getSession(); }).then(function (r) {
      var s = r && r.data && r.data.session;
      if (s && RECOVERY) return signInScreen("newpw");
      return s ? s.user : signInScreen("in");
    }).then(function (u) {
      me = u; startLive();
      sb.auth.onAuthStateChange(function (ev, s) { if (s && s.user) me = s.user; if (ev === "SIGNED_OUT" && !signingOut) location.reload(); });
      /* public commander name, so other players see who you are */
      new Doc("profiles/" + u.id).set({ name: nameOf(u), at: Date.now() }).catch(function () {});
      return true;
    }).catch(function (e) { console.warn("Supabase unavailable:", e); return null; });
    return session;
  }
  var ownerP = null;
  function isOwner() { if (!ownerP) ownerP = run(sb.rpc("is_owner")).then(function (v) { return !!v; }, function () { return false; }); return ownerP; }
  var profCache = {};
  var USER = {
    id: function () { return Promise.resolve(me.id); },
    me: function () { return Promise.resolve({ id: me.id, name: nameOf(me), guest: false }); },
    isOwner: isOwner, canEdit: isOwner,
    can: function () { return Promise.resolve(true); },
    profiles: function (ids) {
      var want = (ids || []).filter(function (id) { return typeof id === "string" && id.length > 10 && !(profCache[id] && Date.now() - profCache[id].t < 300000); }).slice(0, 200);
      var p = want.length ? run(sb.from("docs").select("path,data").in("path", want.map(function (id) { return "profiles/" + id; }))).then(function (rows) {
        var T = Date.now(); want.forEach(function (id) { profCache[id] = { t: T, name: "" }; });
        (rows || []).forEach(function (r) { profCache[r.path.slice(9)] = { t: T, name: String((r.data && r.data.name) || "") }; });
      }, function () {}) : Promise.resolve();
      return p.then(function () { var o = {}; (ids || []).forEach(function (id) { if (profCache[id]) o[id] = { id: id, name: profCache[id].name }; }); return o; });
    }
  };
  var memo = {};
  window.claude = {
    use: function (name) {
      if (!configured) return Promise.resolve(null);
      if (name !== "db" && name !== "user") return Promise.resolve(null);
      if (!memo[name]) memo[name] = start().then(function (ok) { return ok ? (name === "db" ? DB : USER) : null; });
      return memo[name];
    }
  };
  var signingOut = false;
  window.udfAccount = {
    label: function () { return me ? (me.email || nameOf(me) || "Signed in") : "Not signed in"; },
    signOut: function () { if (!sb) return; signingOut = true; /* save the empire to the account first, then sign out */
      Promise.resolve(window.udfBeforeSignOut && window.udfBeforeSignOut()).catch(function () {}).then(function () { return sb.auth.signOut(); }).catch(function () {}).then(function () { location.reload(); }); }
  };
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-act=udfSignOut]"); if (!b) return;
    e.preventDefault(); e.stopPropagation(); if (confirm("Sign out of Ultra Deep Field on this device? Your empire is saved to your account first, so you can sign back in on any phone.")) window.udfAccount.signOut();
  }, true);

  /* ---------- one-time move from the old Firebase server ----------
     You sign in to your old account here; your saved empire and the worlds you held are read and handed to the game,
     which checks the save's signature and brings it across (the same as importing an empire file). */
  var FB = window.UDF_FIREBASE || {}, FBSDK = "https://www.gstatic.com/firebasejs/10.12.2/", fbApp = null;
  function oldSdk() {
    if (fbApp) return Promise.resolve(fbApp);
    return (window.firebase && window.firebase.initializeApp ? Promise.resolve() : loadScript(FBSDK + "firebase-app-compat.js")
      .then(function () { return Promise.all([loadScript(FBSDK + "firebase-auth-compat.js"), loadScript(FBSDK + "firebase-firestore-compat.js")]); }))
      .then(function () { var conf = Object.assign({}, FB); delete conf.ownerUids; fbApp = window.firebase.initializeApp(conf, "old"); return fbApp; });
  }
  function oldSignIn(app) {
    return new Promise(function (resolve, reject) {
      addCss(); var auth = window.firebase.auth(app), w = document.createElement("div"); w.id = "udfOld"; w.className = "udfa"; document.body.appendChild(w);
      w.innerHTML = '<form class="bx" novalidate><h2>Bring your empire</h2><p>Sign in with the account you used on the old server. Your saved empire and worlds are copied here; nothing is changed there.</p>' +
        '<button type="button" class="g" data-a="google">' + GICON + 'Old account: Google</button><div class="or">OR</div>' +
        '<input name="e" type="email" autocomplete="email" placeholder="Old account email" inputmode="email" value="' + esc(lastEmail()) + '">' +
        '<div class="pw"><input name="p" type="password" autocomplete="current-password" placeholder="Old account password"><button type="button" class="eye" data-a="eye">Show</button></div>' +
        '<div class="er" role="alert"></div><button type="submit" class="p">Sign in to old server</button><button type="button" class="l" data-a="cancel">Cancel</button></form>';
      function say(t) { w.querySelector(".er").textContent = t; }
      function fail(e) { var c = String((e && e.code) || "").replace("auth/", ""); say({ "invalid-credential": "Wrong email or password.", "wrong-password": "Wrong email or password.", "user-not-found": "No account with that email on the old server.", "invalid-email": "That email doesn't look right.", "too-many-requests": "Too many tries. Wait a minute.", "popup-closed-by-user": "", "network-request-failed": "No connection." }[c] || ("Couldn't sign in (" + (c || "error") + ").")); }
      function ok(u) { w.remove(); resolve(u); }
      w.addEventListener("click", function (e) {
        var b = e.target.closest("[data-a]"); if (!b) return; e.preventDefault(); var a = b.getAttribute("data-a");
        if (a === "cancel") { w.remove(); reject(null); }
        else if (a === "eye") { var pi = w.querySelector("input[name=p]"); var sh = pi.type === "password"; pi.type = sh ? "text" : "password"; b.textContent = sh ? "Hide" : "Show"; }
        else if (a === "google") { var prov = new window.firebase.auth.GoogleAuthProvider(); prov.setCustomParameters({ prompt: "select_account" }); auth.signInWithPopup(prov).then(function (c) { ok(c.user); }, fail); }
      });
      w.addEventListener("submit", function (e) { e.preventDefault(); var f = e.target; auth.signInWithEmailAndPassword((f.e.value || "").trim(), f.p.value || "").then(function (c) { ok(c.user); }, fail); });
    });
  }
  window.udfOld = {
    available: !!(FB.apiKey && FB.projectId),
    fetch: function () {
      var app;
      return oldSdk().then(function (a) { app = a; return oldSignIn(app); }).then(function (u) {
        var fs = window.firebase.firestore(app);
        return Promise.all([fs.doc("data/users/" + u.uid + "/save").get(), fs.collection("planets").where("owner", "==", u.uid).limit(200).get().catch(function () { return { docs: [] }; })])
          .then(function (r) {
            var s = r[0].exists ? r[0].data() : null;
            window.firebase.auth(app).signOut().catch(function () {});
            if (!s || typeof s.json !== "string") throw new Error("No saved empire was found on the old server for that account.");
            return { json: s.json, sig: s.sig, savedAt: s.savedAt || 0, planets: r[1].docs.map(function (d) { return Object.assign({ id: d.id }, d.data()); }) };
          });
      }, function (e) { if (e === null) return null; throw new Error("Couldn't reach the old server."); });
    }
  };

  if (configured) start(); /* show the sign-in screen right away instead of waiting for the game to ask */
})();
