/* In-memory stand-in for the Firebase compat SDK, for local testing only. Records every write in window.__mockLog. */
(function () {
  if (window.firebase) return;
  var store = {}, subs = [], log = (window.__mockLog = []);
  function FieldPath() { this.segs = Array.prototype.slice.call(arguments); }
  function clone(v) { return v === undefined ? undefined : JSON.parse(JSON.stringify(v)); }
  function strip(v) { if (Array.isArray(v)) return v.map(strip); if (v && typeof v === "object") { var o = {}; for (var k in v) if (v[k] !== undefined) o[k] = strip(v[k]); return o; } return v; }
  function err(code, msg) { var e = new Error(msg || code); e.code = code; return e; }
  function snapDoc(path) { var id = path.split("/").pop(), d = store[path]; return { id: id, ref: { path: path }, exists: d !== undefined, data: function () { return clone(d); } }; }
  function notify() { setTimeout(function () { subs.slice().forEach(function (s) { try { s(); } catch (e) { console.error(e); } }); }, 0); }
  function Doc(path) { this.path = path; this.id = path.split("/").pop(); this.firestore = FS; }
  Doc.prototype.get = function () { return Promise.resolve(snapDoc(this.path)); };
  Doc.prototype.set = function (d, opt) {
    if (!window.__authUser) return Promise.reject(err("permission-denied"));
    var p = this.path; if (window.__rule && !window.__rule(p, store[p], d)) return Promise.reject(err("permission-denied")); log.push(["set", p, clone(d)]);
    store[p] = opt && opt.merge && store[p] ? Object.assign(clone(store[p]), strip(d)) : strip(clone(d)); notify(); return Promise.resolve();
  };
  Doc.prototype.update = function () {
    var p = this.path; if (store[p] === undefined) return Promise.reject(err("not-found"));
    var a = arguments, d = clone(store[p]);
    for (var i = 0; i < a.length; i += 2) { var f = a[i], segs = f instanceof FieldPath ? f.segs : String(f).split("."), o = d;
      for (var j = 0; j < segs.length - 1; j++) { if (!o[segs[j]] || typeof o[segs[j]] !== "object") o[segs[j]] = {}; o = o[segs[j]]; } o[segs[segs.length - 1]] = clone(a[i + 1]); }
    log.push(["update", p, a.length / 2]); store[p] = d; notify(); return Promise.resolve();
  };
  Doc.prototype.delete = function () { log.push(["delete", this.path]); delete store[this.path]; notify(); return Promise.resolve(); };
  Doc.prototype.collection = function (c) { return new Query(this.path + "/" + c, []); };
  Doc.prototype.onSnapshot = function (next) { var p = this.path, last = "\0"; function run() { var j = JSON.stringify(store[p]); if (j !== last) { last = j; next(snapDoc(p)); } } subs.push(run); setTimeout(run, 0); return function () { subs.splice(subs.indexOf(run), 1); }; };
  function Query(path, f, lim) { this.path = path; this.f = f; this.lim = lim || 1e9; }
  Query.prototype.where = function (a, op, v) { return new Query(this.path, this.f.concat([[a, op, v]]), this.lim); };
  Query.prototype.orderBy = function () { return this; };
  Query.prototype.limit = function (n) { return new Query(this.path, this.f, n); };
  Query.prototype.doc = function (id) { return new Doc(this.path + "/" + id); };
  Query.prototype._docs = function () {
    var pre = this.path + "/", depth = pre.split("/").length, f = this.f, out = [];
    Object.keys(store).forEach(function (k) { if (k.indexOf(pre) !== 0 || k.split("/").length !== depth) return; var d = store[k];
      if (f.every(function (w) { var v = d[w[0]]; return w[1] === "==" ? v === w[2] : w[1] === "array-contains" ? Array.isArray(v) && v.indexOf(w[2]) >= 0 : true; })) out.push(snapDoc(k)); });
    return out.slice(0, this.lim);
  };
  Query.prototype.get = function () { var d = this._docs(); return Promise.resolve({ docs: d, size: d.length, empty: !d.length, docChanges: function () { return []; } }); };
  Query.prototype.onSnapshot = function (next) { var q = this, last = "\0", prev = {}; function run() { var d = q._docs(), j = JSON.stringify(d.map(function (x) { return [x.id, x.data()]; }));
      if (j === last) return; last = j; var ch = d.map(function (x) { return { type: prev[x.id] ? "modified" : "added", doc: x }; }); prev = {}; d.forEach(function (x) { prev[x.id] = 1; });
      next({ docs: d, size: d.length, empty: !d.length, docChanges: function () { return ch; } }); } subs.push(run); setTimeout(run, 0); return function () { subs.splice(subs.indexOf(run), 1); }; };
  var FS = {
    settings: function () {}, enablePersistence: function () { return Promise.resolve(); },
    doc: function (p) { return new Doc(p); }, collection: function (p) { return new Query(p, []); },
    runTransaction: function (fn) { var tx = { get: function (r) { return r.get(); }, set: function (r, d) { store[r.path] = clone(d); notify(); } }; return Promise.resolve(fn(tx)); }
  };
  var listeners = [];
  function setUser(u) { window.__authUser = u; AUTH.currentUser = u; listeners.forEach(function (l) { l(u); }); }
  function mkUser(email, name) { var u = { uid: "uid_" + email.replace(/\W/g, "").slice(0, 20) + "_test", email: email, displayName: name || null, updateProfile: function (p) { u.displayName = p.displayName; return Promise.resolve(); } }; return u; }
  var AUTH = {
    currentUser: null,
    onAuthStateChanged: function (fn) { listeners.push(fn); setTimeout(function () { fn(AUTH.currentUser); }, 0); return function () { listeners.splice(listeners.indexOf(fn), 1); }; },
    createUserWithEmailAndPassword: function (e, p) { if (!/@/.test(e)) return Promise.reject(err("auth/invalid-email")); if (p.length < 6) return Promise.reject(err("auth/weak-password")); var u = mkUser(e); setTimeout(function () { setUser(u); }, 10); return Promise.resolve({ user: u }); },
    signInWithEmailAndPassword: function (e) { var u = mkUser(e, "Tester"); setUser(u); return Promise.resolve({ user: u }); },
    signInWithPopup: function () { var u = mkUser("google@test.dev", "Google Tester"); setUser(u); return Promise.resolve({ user: u }); },
    signInWithRedirect: function () { return Promise.resolve(); },
    sendPasswordResetEmail: function () { return Promise.resolve(); },
    signOut: function () { setUser(null); return Promise.resolve(); }
  };
  function GoogleAuthProvider() {} GoogleAuthProvider.prototype.setCustomParameters = function () {};
  var auth = function () { return AUTH; }; auth.GoogleAuthProvider = GoogleAuthProvider;
  var firestore = function () { return FS; }; firestore.FieldPath = FieldPath;
  window.firebase = { initializeApp: function () { return {}; }, auth: auth, firestore: firestore };
  window.__store = store;
})();
