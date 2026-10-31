/* In-memory stand-in for supabase-js v2 (only what udf-supabase.js uses), for local testing. Mirrors supabase/schema.sql:
   path → col/top/id, row-level rules, the save guard, deep-merge update, leases and live changes. */
(function () {
  var rows = (window.__sbRows = {}), chans = [], log = (window.__sbLog = []), users = {}, sess = null, authL = [];
  var DELAY = window.__sbDelay || 40;
  try { var saved = JSON.parse(localStorage.getItem("__sbSession") || "null"); if (saved) sess = saved; } catch (e) {}
  try { Object.assign(rows, JSON.parse(localStorage.getItem("__sbRows") || "{}")); } catch (e) {}
  function persist() { try { localStorage.setItem("__sbRows", JSON.stringify(rows)); } catch (e) {} }
  function clone(v) { return v === undefined ? undefined : JSON.parse(JSON.stringify(v)); }
  function later(v) { return new Promise(function (ok) { setTimeout(function () { ok(v); }, DELAY); }); }
  function uid() { return sess && sess.user.id; }
  var SHARED = ["planets", "occ", "inbox", "inbound", "alliances", "assaults", "chat", "event", "galaxy", "_locks", "players", "profiles"];
  function canRead(p, d) { var t = p.split("/")[0]; if (!uid()) return false; if (SHARED.indexOf(t) >= 0) return true; if (t === "data") return p.split("/")[2] === uid(); if (t === "dms") return (d.p || []).indexOf(uid()) >= 0; return false; }
  function canWrite(p, adding) { var t = p.split("/")[0], s2 = p.split("/")[1]; if (!uid()) return false;
    if (["planets", "occ", "inbox", "inbound", "alliances", "assaults", "chat", "event", "galaxy", "_locks", "dms"].indexOf(t) >= 0) return true;
    if (t === "players" || t === "profiles") return s2 === uid(); if (t === "data") return p.split("/")[2] === uid(); if (t === "feedback") return adding; return false; }
  function err(code, message) { return { code: code, message: message, details: null, hint: null }; }
  function guard(p, old, nd) {
    if (!/^data\/users\/[^/]+\/save$/.test(p) || !old) return null;
    if ("seq" in old && (+nd.seq || 0) !== (+old.seq || 0) + 1) return err("42501", "save out of order");
    if ("lv" in old && (+old.lv || 0) >= 10 && String(nd.shrink) !== "true" && (+nd.lv || 0) * 2 < (+old.lv || 0)) return err("42501", "save would wipe progress");
    return null;
  }
  function notify(type, path, data) {
    setTimeout(function () {
      chans.forEach(function (c) { if (!c.on) return;
        if (type === "DELETE") return c.fn({ eventType: "DELETE", old: { path: path }, new: {} });
        if (!canRead(path, data)) return;
        c.fn({ eventType: type, new: { path: path, col: path.replace(/\/[^/]*$/, ""), data: clone(data) }, old: { path: path } });
      });
    }, DELAY);
  }
  /* writes from "another player": skip the rules, still broadcast */
  window.__sbServerWrite = function (path, data) { var had = !!rows[path]; if (data === null) { delete rows[path]; notify("DELETE", path); } else { rows[path] = clone(data); notify(had ? "UPDATE" : "INSERT", path, data); } persist(); };
  function mergeDeep(a, b) { if (a && b && typeof a === "object" && typeof b === "object" && !Array.isArray(a) && !Array.isArray(b)) { var o = clone(a); for (var k in b) o[k] = k in o ? mergeDeep(o[k], b[k]) : clone(b[k]); return o; } return clone(b); }
  function getPath(d, f) { return f.split("->").reduce(function (o, k) { return o == null ? undefined : o[k]; }, d); }

  function Builder() { this.op = "select"; this.f = []; this.lim = 1000; this.single = false; }
  Builder.prototype.select = function () { return this; };
  Builder.prototype.eq = function (c, v) { this.f.push(function (r) { return c === "path" ? r.path === v : c === "col" ? r.col === v : false; }); return this; };
  Builder.prototype.in = function (c, vs) { this.f.push(function (r) { return vs.indexOf(r.path) >= 0; }); return this; };
  Builder.prototype.is = function (c, v) { var f = c.replace(/^data->>?/, ""); this.f.push(function (r) { return getPath(r.data, f) == null; }); return this; };
  Builder.prototype.filter = function (c, op, v) {
    var text = c.indexOf("->>") >= 0, f = c.replace(/^data->>?/, "");
    this.f.push(function (r) { var x = getPath(r.data, f);
      if (op === "eq") return text ? x != null && typeof x !== "object" && String(x) === v : JSON.stringify(x) === JSON.stringify(JSON.parse(v));
      if (op === "cs") { var want = JSON.parse(v); return Array.isArray(x) && want.every(function (w) { return x.indexOf(w) >= 0; }); }
      return false; });
    return this;
  };
  Builder.prototype.limit = function (n) { this.lim = n; return this; };
  Builder.prototype.maybeSingle = function () { this.single = true; return this; };
  Builder.prototype.upsert = function (row) { this.op = "upsert"; this.row = row; return this; };
  Builder.prototype.delete = function () { this.op = "delete"; return this; };
  Builder.prototype.then = function (ok, bad) { return this._run().then(ok, bad); };
  Builder.prototype._run = function () {
    var self = this;
    if (!uid()) return later({ data: null, error: err("42501", "permission denied for table docs") });
    if (this.op === "upsert") {
      var p = this.row.path, d = this.row.data, old = rows[p];
      if (!/^[^/]+(\/[^/]+)+$/.test(p)) return later({ data: null, error: err("22023", "bad path " + p) });
      if (!canWrite(p, !old)) return later({ data: null, error: err("42501", 'new row violates row-level security policy for table "docs"') });
      var g = guard(p, old, d); if (g) return later({ data: null, error: g });
      rows[p] = clone(d); log.push(["upsert", p]); persist(); notify(old ? "UPDATE" : "INSERT", p, d); return later({ data: null, error: null });
    }
    var hits = Object.keys(rows).map(function (p) { return { path: p, col: p.replace(/\/[^/]*$/, ""), data: rows[p] }; })
      .filter(function (r) { return canRead(r.path, r.data) && self.f.every(function (fn) { return fn(r); }); });
    if (this.op === "delete") { hits.forEach(function (r) { if (canWrite(r.path, false)) { delete rows[r.path]; log.push(["delete", r.path]); notify("DELETE", r.path); } }); persist(); return later({ data: null, error: null }); }
    hits = hits.slice(0, this.lim).map(function (r) { return { path: r.path, data: clone(r.data) }; });
    return later({ data: this.single ? (hits[0] || null) : hits, error: null });
  };
  function rpc(name, a) {
    if (!uid()) return later({ data: null, error: err("42501", "permission denied") });
    if (name === "is_owner") return later({ data: false, error: null });
    if (name === "doc_update") { var old = rows[a.p]; if (!old || !canRead(a.p, old)) return later({ data: null, error: err("P0002", "not found " + a.p) });
      if (!canWrite(a.p, false)) return later({ data: null, error: null });
      var nd = mergeDeep(old, a.patch), g = guard(a.p, old, nd); if (g) return later({ data: null, error: g });
      rows[a.p] = nd; log.push(["update", a.p]); persist(); notify("UPDATE", a.p, nd); return later({ data: clone(nd), error: null }); }
    if (name === "doc_acquire") { var lp = "_locks/" + a.p.replace(/\//g, "~"), d = rows[lp] || {}, ms = Math.min(Math.max(a.ttl || 10000, 1000), 60000);
      if (d.until > a.t && d.holder !== a.holder) return later({ data: { acquired: false, holder: d.holder, until: d.until }, error: null });
      rows[lp] = { holder: a.holder, until: a.t + ms }; persist(); return later({ data: { acquired: true, until: a.t + ms }, error: null }); }
    return later({ data: null, error: err("PGRST202", "no function " + name) });
  }
  function setSess(s, ev) { sess = s; try { localStorage.setItem("__sbSession", JSON.stringify(s)); } catch (e) {} authL.slice().forEach(function (fn) { fn(ev, s); }); }
  function mkUser(email, name) { var id = "u" + (Math.abs(email.split("").reduce(function (a, c) { return (a * 31 + c.charCodeAt(0)) | 0; }, 7)).toString(16) + "0000000000000000000000000000").slice(0, 32).replace(/(.{8})(.{4})(.{4})(.{4})(.{12})/, "$1-$2-$3-$4-$5");
    return { id: id, email: email, user_metadata: { name: name } }; }
  var AUTH = {
    getSession: function () { return later({ data: { session: sess }, error: null }); },
    onAuthStateChange: function (fn) { authL.push(fn); setTimeout(function () { fn("INITIAL_SESSION", sess); }, 0); return { data: { subscription: { unsubscribe: function () { authL.splice(authL.indexOf(fn), 1); } } } }; },
    signUp: function (o) { if (!/@/.test(o.email)) return later({ data: {}, error: { message: "Unable to validate email address: invalid format" } }); if ((o.password || "").length < 6) return later({ data: {}, error: { message: "Password should be at least 6 characters." } });
      var u = mkUser(o.email, o.options && o.options.data && o.options.data.name); users[o.email] = { u: u, pw: o.password };
      if (window.__sbConfirm) return later({ data: { user: u, session: null }, error: null });
      var s = { user: u, access_token: "t" }; return later({ data: { user: u, session: s }, error: null }).then(function (r) { setSess(s, "SIGNED_IN"); return r; }); },
    signInWithPassword: function (o) { var u = (users[o.email] && users[o.email].u) || mkUser(o.email, "Tester"); var s = { user: u, access_token: "t" }; return later({ data: { user: u, session: s }, error: null }).then(function (r) { setSess(s, "SIGNED_IN"); return r; }); },
    signInWithOAuth: function () { return later({ data: {}, error: { message: "Unsupported provider: provider is not enabled" } }); },
    resetPasswordForEmail: function () { return later({ data: {}, error: null }); },
    updateUser: function () { return later({ data: { user: sess && sess.user }, error: null }); },
    signOut: function () { return later({ error: null }).then(function (r) { setSess(null, "SIGNED_OUT"); return r; }); }
  };
  window.supabase = { createClient: function () { return {
    auth: AUTH,
    from: function () { return new Builder(); },
    rpc: rpc,
    channel: function () { var c = { on: false, fn: null }; return { on: function (t, f, fn) { c.fn = fn; return this; }, subscribe: function (cb) { chans.push(c); setTimeout(function () { c.on = true; cb && cb("SUBSCRIBED"); }, DELAY); window.__sbDrop = function () { c.on = false; cb && cb("CHANNEL_ERROR"); setTimeout(function () { c.on = true; cb && cb("SUBSCRIBED"); }, 300); }; return this; } };
    },
    removeChannel: function () {}
  }; } };
})();
