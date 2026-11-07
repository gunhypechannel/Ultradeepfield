/* The Supabase JS client, pointed at the shared fake server (fakesrv.js), so several browsers share one galaxy. */
(function () {
  var SRV = window.__fakeSrv || "http://localhost:8124", LS = window.localStorage, LAT = window.__lat || 80;
  function load(k, d) { try { var v = LS.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  var SESS = load("__fakesess", null);
  function uid() { return SESS && SESS.user && SESS.user.id; }
  function post(path, body) { return new Promise(function (r) { setTimeout(r, LAT * (0.5 + Math.random())); }).then(function () {
    return fetch(SRV + path, { method: "POST", body: JSON.stringify(body) }).then(function (r) { return r.json(); }); }).catch(function (e) { return { data: null, error: { message: "Failed to fetch" } }; }); }
  function Q() { this.q = { w: [], cols: "*", lim: 1e9, op: "select" }; }
  Q.prototype.select = function (c) { if (this.q.op === "select") this.q.cols = c || "*"; return this; };
  Q.prototype.eq = function (c, v) { this.q.w.push(["eq", c, null, v]); return this; };
  Q.prototype.is = function (c, v) { this.q.w.push(["is", c, null, v]); return this; };
  Q.prototype.in = function (c, a) { this.q.w.push(["in", c, null, a]); return this; };
  Q.prototype.filter = function (c, op, v) { this.q.w.push(["f", c, op, v]); return this; };
  Q.prototype.neq = function (c, v) { return this.filter(c, "neq", v); };
  Q.prototype.order = function () { return this; };
  Q.prototype.limit = function (n) { this.q.lim = n; return this; };
  Q.prototype.maybeSingle = function () { this.q.one = 1; return this; };
  Q.prototype.single = function () { this.q.one = 2; return this; };
  Q.prototype.upsert = function (row) { this.q.op = "upsert"; this.q.row = row; return this; };
  Q.prototype.delete = function () { this.q.op = "delete"; return this; };
  Q.prototype.then = function (ok, no) { return post("/q", { q: this.q, uid: uid() }).then(ok, no); };
  var authL = [];
  function fire(ev) { var s = SESS; authL.slice().forEach(function (f) { setTimeout(function () { f(ev, s); }, 0); }); }
  function mkSess(u) { SESS = { access_token: "tok-" + u.id, refresh_token: "ref-" + u.id, user: u }; try { LS.setItem("__fakesess", JSON.stringify(SESS)); } catch (e) {} return SESS; }
  var auth = {
    getSession: function () { return Promise.resolve({ data: { session: SESS }, error: null }); },
    onAuthStateChange: function (f) { authL.push(f); setTimeout(function () { f("INITIAL_SESSION", SESS); }, 0); return { data: { subscription: { unsubscribe: function () { var i = authL.indexOf(f); if (i >= 0) authL.splice(i, 1); } } } }; },
    signUp: function (o) { return post("/auth", { op: "signUp", email: o.email, password: o.password, meta: o.options && o.options.data }).then(function (r) {
      if (r.error || !r.data.user.identities.length) return r; mkSess(r.data.user); fire("SIGNED_IN"); return { data: { user: r.data.user, session: SESS }, error: null }; }); },
    signInWithPassword: function (o) { return post("/auth", { op: "signIn", email: o.email, password: o.password }).then(function (r) { if (r.error) return r; mkSess(r.data.user); fire("SIGNED_IN"); return { data: { user: r.data.user, session: SESS }, error: null }; }); },
    signOut: function () { SESS = null; try { LS.setItem("__fakesess", "null"); } catch (e) {} fire("SIGNED_OUT"); return Promise.resolve({ error: null }); },
    setSession: function () { return Promise.resolve({ data: { session: SESS }, error: null }); },
    resend: function () { return Promise.resolve({ error: null }); }, resetPasswordForEmail: function () { return Promise.resolve({ error: null }); },
    updateUser: function () { return Promise.resolve({ data: { user: SESS && SESS.user }, error: null }); }, signInWithOAuth: function () { return Promise.resolve({ error: { message: "provider is not enabled" } }); }
  };
  window.supabase = { createClient: function () { return {
    auth: auth, rpc: function (n, a) { return post("/rpc", { name: n, args: a, uid: uid() }); }, from: function () { return new Q(); },
    channel: function () { var cbs = []; return { on: function (t, opt, f) { cbs.push(f); return this; }, subscribe: function (st) {
      var es = new EventSource(SRV + "/live"); es.onopen = function () { st && st("SUBSCRIBED"); }; es.onerror = function () { st && st("CHANNEL_ERROR"); };
      es.onmessage = function (e) { var p = JSON.parse(e.data); cbs.forEach(function (f) { try { f(p); } catch (x) { console.error(x); } }); }; return this; } }; } }; } };
})();
