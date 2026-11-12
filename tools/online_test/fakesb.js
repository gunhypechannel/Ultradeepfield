/* A stand-in for the Supabase JS client: an in-memory copy of the real `docs` table (seeded from the live galaxy), with the same
   query builder, RPCs (doc_update, doc_acquire, doc_cas, is_owner), row rules for private data/ records, auth (sign up / sign in /
   session kept across reloads) and the realtime channel. The real udf-supabase.js runs on top of it unchanged. */
(function () {
  var LAT = window.__lat || 120, LS = window.localStorage;
  function load(k, d) { try { var v = LS.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function save(k, v) { try { LS.setItem(k, JSON.stringify(v)); } catch (e) {} }
  var T = load("__fakedb", null);
  if (!T) { T = {}; (window.__seedRows || []).forEach(function (r) { T[r.path] = { data: r.data, u: new Date().toISOString() }; }); save("__fakedb", T); }
  var USERS = load("__fakeusers", {}), SESS = load("__fakesess", null), log = (window.__sbLog = []);
  function persist() { save("__fakedb", T); }
  function clone(v) { return v == null ? v : JSON.parse(JSON.stringify(v)); }
  function later(v) { return new Promise(function (r) { setTimeout(function () { r(v); }, LAT * (0.5 + Math.random())); }); }
  function colOf(p) { return p.replace(/\/[^/]*$/, ""); }
  function uid() { return SESS && SESS.user && SESS.user.id; }
  function canRead(p) { var m = /^data\/users\/([^/]+)\//.exec(p); return !m || m[1] === uid(); }
  function canWrite(p) { if (!uid()) return false; var m = /^data\/users\/([^/]+)\//.exec(p); return !m || m[1] === uid(); }
  var chans = [];
  function broadcast(ev, path, data) { if (path.split("/")[0] === "data") return;
    chans.forEach(function (c) { setTimeout(function () { c.cbs.forEach(function (f) { try { f({ eventType: ev, new: ev === "DELETE" ? {} : { path: path, data: clone(data), top: path.split("/")[0] }, old: { path: path } }); } catch (e) { console.error(e); } }); }, LAT); }); }
  function val(row, c) {
    if (c === "path") return row.path; if (c === "col") return colOf(row.path); if (c === "top") return row.path.split("/")[0]; if (c === "id") return row.path.split("/").pop();
    if (c === "updated_at") return row.u; if (c === "data") return clone(row.data);
    var m = /^data->(>?)(\w+)$/.exec(c); if (m) { var v = row.data ? row.data[m[2]] : undefined; if (v === undefined) return null; return m[1] ? (typeof v === "object" ? JSON.stringify(v) : String(v)) : clone(v); }
    throw new Error("fake: column " + c);
  }
  function merge(a, b) { if (a && b && typeof a === "object" && typeof b === "object" && !Array.isArray(a) && !Array.isArray(b)) { var o = {}; Object.keys(a).forEach(function (k) { o[k] = a[k]; }); Object.keys(b).forEach(function (k) { o[k] = k in a ? merge(a[k], b[k]) : b[k]; }); return o; } return b; }
  function Q() { this.w = []; this.cols = "*"; this.lim = 1e9; this.op = "select"; }
  Q.prototype.select = function (c) { if (this.op === "select") this.cols = c || "*"; return this; };
  Q.prototype.eq = function (c, v) { this.w.push(function (r) { return String(val(r, c)) === String(v); }); return this; };
  Q.prototype.is = function (c, v) { this.w.push(function (r) { return val(r, c) === v; }); return this; };
  Q.prototype.in = function (c, a) { this.w.push(function (r) { return a.indexOf(val(r, c)) >= 0; }); return this; };
  Q.prototype.filter = function (c, op, v) { this.w.push(function (r) { var x = val(r, c);
    if (op === "eq") return /->>/.test(c) ? x === v : JSON.stringify(x) === v; if (op === "cs") { var want = JSON.parse(v); return Array.isArray(x) && want.every(function (y) { return x.some(function (z) { return JSON.stringify(z) === JSON.stringify(y); }); }); }
    if (op === "neq") return String(x) !== String(v); throw new Error("fake: op " + op); }); return this; };
  Q.prototype.neq = function (c, v) { return this.filter(c, "neq", v); };
  Q.prototype.order = function () { return this; };
  Q.prototype.limit = function (n) { this.lim = n; return this; };
  Q.prototype.maybeSingle = function () { this.one = 1; return this; };
  Q.prototype.single = function () { this.one = 2; return this; };
  Q.prototype.upsert = function (row) { this.op = "upsert"; this.row = row; return this; };
  Q.prototype.delete = function () { this.op = "delete"; return this; };
  Q.prototype.exec = function () {
    var self = this, rows = Object.keys(T).map(function (p) { return { path: p, data: T[p].data, u: T[p].u }; }).filter(function (r) { return canRead(r.path) && self.w.every(function (f) { return f(r); }); });
    if (this.op === "upsert") { var rs = Array.isArray(this.row) ? this.row : [this.row];
      for (var i = 0; i < rs.length; i++) if (!canWrite(rs[i].path)) return { data: null, error: { code: "42501", message: "new row violates row-level security policy" } };
      rs.forEach(function (r) { T[r.path] = { data: clone(r.data), u: new Date().toISOString() }; log.push(["upsert", r.path]); broadcast("UPDATE", r.path, r.data); }); persist(); return { data: null, error: null }; }
    if (this.op === "delete") { rows.forEach(function (r) { if (canWrite(r.path)) { delete T[r.path]; log.push(["delete", r.path]); broadcast("DELETE", r.path); } }); persist(); return { data: null, error: null }; }
    rows = rows.slice(0, this.lim);
    var cols = this.cols === "*" ? ["path", "data"] : this.cols.split(",");
    var out = rows.map(function (r) { var o = {}; cols.forEach(function (c) { var a = c.split(":"), name = a.length > 1 ? a[0] : c, src = a.length > 1 ? a[1] : c; o[name] = val(r, src); }); return o; });
    if (this.one) { if (out.length > 1) return { data: null, error: { code: "PGRST116", message: "multiple rows" } }; if (!out.length && this.one === 2) return { data: null, error: { code: "PGRST116", message: "no rows" } }; return { data: out[0] || null, error: null }; }
    return { data: out, error: null };
  };
  Q.prototype.then = function (ok, no) { var r; try { r = this.exec(); } catch (e) { r = { data: null, error: { message: e.message } }; } return later(r).then(ok, no); };
  function rpc(name, a) { var r;
    if (name === "is_owner") r = { data: false, error: null };
    else if (name === "doc_update") { if (!T[a.p] || !canRead(a.p)) r = { data: null, error: { code: "P0002", message: "not found " + a.p } }; else if (!canWrite(a.p)) r = { data: null, error: { code: "42501", message: "rls" } };
      else { T[a.p] = { data: merge(T[a.p].data, clone(a.patch)), u: new Date().toISOString() }; persist(); log.push(["update", a.p]); broadcast("UPDATE", a.p, T[a.p].data); r = { data: clone(T[a.p].data), error: null }; } }
    else if (name === "doc_acquire") { var lp = "_locks/" + a.p.replace(/\//g, "~"), d = (T[lp] || {}).data || {};
      if (d.until > a.t && d.holder !== a.holder) r = { data: { acquired: false, holder: d.holder, until: d.until }, error: null };
      else { T[lp] = { data: { holder: a.holder, until: a.t + a.ttl }, u: new Date().toISOString() }; persist(); r = { data: { acquired: true, until: a.t + a.ttl }, error: null }; } }
    else if (name === "doc_cas") { var cur = T[a.p]; if (!canWrite(a.p)) r = { data: null, error: { code: "42501", message: "rls" } };
      else if (cur ? cur.u !== a.expect : a.expect != null) r = { data: { ok: false, v: cur ? cur.u : null }, error: null };
      else { var u = new Date().toISOString(); if (cur && u <= cur.u) u = new Date(Date.parse(cur.u) + 1).toISOString(); T[a.p] = { data: clone(a.d), u: u }; persist(); log.push(["cas", a.p]); broadcast("UPDATE", a.p, a.d); r = { data: { ok: true, v: u }, error: null }; } }
    else r = { data: null, error: { message: "fake: rpc " + name } };
    return later(r); }
  var authL = [];
  function fire(ev) { var s = clone(SESS); authL.slice().forEach(function (f) { setTimeout(function () { f(ev, s); }, 0); }); }
  function mkSess(u) { SESS = { access_token: "tok-" + u.id, refresh_token: "ref-" + u.id, user: u }; save("__fakesess", SESS); return SESS; }
  var auth = {
    getSession: function () { return later({ data: { session: clone(SESS) }, error: null }); },
    onAuthStateChange: function (f) { authL.push(f); setTimeout(function () { f("INITIAL_SESSION", clone(SESS)); }, 0); return { data: { subscription: { unsubscribe: function () { var i = authL.indexOf(f); if (i >= 0) authL.splice(i, 1); } } } }; },
    signUp: function (o) { var e = String(o.email).toLowerCase(); if (USERS[e]) return later({ data: { user: { id: USERS[e].id, identities: [] }, session: null }, error: null });
      if (String(o.password).length < 6) return later({ data: null, error: { message: "Password should be at least 6 characters" } });
      var u = { id: (crypto.randomUUID ? crypto.randomUUID() : "u" + Date.now()), email: e, user_metadata: (o.options && o.options.data) || {}, identities: [{}] };
      USERS[e] = { id: u.id, pw: o.password, u: u }; save("__fakeusers", USERS); mkSess(u); fire("SIGNED_IN"); return later({ data: { user: u, session: clone(SESS) }, error: null }); },
    signInWithPassword: function (o) { var e = String(o.email).toLowerCase(), r = USERS[e];
      if (!r || r.pw !== o.password) return later({ data: null, error: { message: "Invalid login credentials" } }); mkSess(r.u); fire("SIGNED_IN"); return later({ data: { user: r.u, session: clone(SESS) }, error: null }); },
    signOut: function () { SESS = null; save("__fakesess", null); fire("SIGNED_OUT"); return later({ error: null }); },
    setSession: function () { return later({ data: { session: clone(SESS) }, error: null }); },
    resend: function () { return later({ error: null }); }, resetPasswordForEmail: function () { return later({ error: null }); },
    updateUser: function () { return later({ data: { user: SESS && SESS.user }, error: null }); }, signInWithOAuth: function () { return later({ error: { message: "provider is not enabled" } }); }
  };
  window.supabase = { createClient: function () { return {
    auth: auth, rpc: rpc, from: function () { return new Q(); },
    channel: function () { var c = { cbs: [] }; return { on: function (t, opt, f) { c.cbs.push(f); return this; }, subscribe: function (st) { chans.push(c); setTimeout(function () { st && st("SUBSCRIBED"); }, LAT); return this; } }; } }; } };
  window.__fake = { T: T, USERS: USERS, get sess() { return SESS; } };
})();
