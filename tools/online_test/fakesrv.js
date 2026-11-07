// A shared stand-in for the Supabase project, so several browsers (several players) play in one galaxy:
// the docs table (seeded from the live galaxy), row rules for private data/ records, RPCs, auth users, and live changes (SSE).
const http = require('http'), fs = require('fs');
const PORT = +process.env.FPORT || 8124, T = {}, USERS = {}, subs = new Set(), LOG = [];
for (const r of JSON.parse(fs.readFileSync(__dirname + '/seed.json'))) T[r.path] = { data: r.data, u: new Date().toISOString() };
const clone = v => v == null ? v : JSON.parse(JSON.stringify(v)), colOf = p => p.replace(/\/[^/]*$/, '');
const canRead = (p, uid) => { const m = /^data\/users\/([^/]+)\//.exec(p); return !m || m[1] === uid; };
const canWrite = (p, uid) => { if (!uid) return false; const m = /^data\/users\/([^/]+)\//.exec(p); return !m || m[1] === uid; };
function val(row, c) {
  if (c === 'path') return row.path; if (c === 'col') return colOf(row.path); if (c === 'top') return row.path.split('/')[0]; if (c === 'id') return row.path.split('/').pop();
  if (c === 'updated_at') return row.u; if (c === 'data') return clone(row.data);
  const m = /^data->(>?)(\w+)$/.exec(c); if (m) { const v = row.data ? row.data[m[2]] : undefined; if (v === undefined) return null; return m[1] ? (typeof v === 'object' ? JSON.stringify(v) : String(v)) : clone(v); }
  throw new Error('fake: column ' + c);
}
const merge = (a, b) => (a && b && typeof a === 'object' && typeof b === 'object' && !Array.isArray(a) && !Array.isArray(b)) ? Object.fromEntries([...new Set([...Object.keys(a), ...Object.keys(b)])].map(k => [k, k in b ? (k in a ? merge(a[k], b[k]) : b[k]) : a[k]])) : b;
function test(r, w) { const [k, c, op, v] = w, x = val(r, c);
  if (k === 'eq') return String(x) === String(v); if (k === 'is') return x === v; if (k === 'in') return v.indexOf(x) >= 0;
  if (op === 'eq') return /->>/.test(c) ? x === v : JSON.stringify(x) === v;
  if (op === 'cs') { const want = JSON.parse(v); return Array.isArray(x) && want.every(y => x.some(z => JSON.stringify(z) === JSON.stringify(y))); }
  if (op === 'neq') return String(x) !== String(v); throw new Error('fake: op ' + op); }
function broadcast(ev, path, data) { if (path.split('/')[0] === 'data') return; const msg = 'data: ' + JSON.stringify({ eventType: ev, new: ev === 'DELETE' ? {} : { path, data, top: path.split('/')[0] }, old: { path } }) + '\n\n'; for (const s of subs) s.write(msg); }
function exec(q, uid) {
  if (q.op === 'upsert') { const rs = Array.isArray(q.row) ? q.row : [q.row];
    for (const r of rs) if (!canWrite(r.path, uid)) return { data: null, error: { code: '42501', message: 'new row violates row-level security policy' } };
    for (const r of rs) { T[r.path] = { data: clone(r.data), u: new Date().toISOString() }; LOG.push([uid, 'upsert', r.path]); broadcast('UPDATE', r.path, r.data); } return { data: null, error: null }; }
  let rows = Object.keys(T).map(p => ({ path: p, data: T[p].data, u: T[p].u })).filter(r => canRead(r.path, uid) && q.w.every(w => test(r, w)));
  if (q.op === 'delete') { for (const r of rows) if (canWrite(r.path, uid)) { delete T[r.path]; LOG.push([uid, 'delete', r.path]); broadcast('DELETE', r.path); } return { data: null, error: null }; }
  rows = rows.slice(0, q.lim); const cols = q.cols === '*' ? ['path', 'data'] : q.cols.split(',');
  const out = rows.map(r => Object.fromEntries(cols.map(c => { const a = c.split(':'); return [a.length > 1 ? a[0] : c, val(r, a.length > 1 ? a[1] : c)]; })));
  if (q.one) { if (out.length > 1) return { data: null, error: { code: 'PGRST116', message: 'multiple rows' } }; if (!out.length && q.one === 2) return { data: null, error: { code: 'PGRST116', message: 'no rows' } }; return { data: out[0] || null, error: null }; }
  return { data: out, error: null };
}
function rpc(name, a, uid) {
  if (!uid && name !== 'is_owner') return { data: null, error: { code: '42501', message: 'permission denied' } };
  if (name === 'is_owner') return { data: false, error: null };
  if (name === 'doc_update') { if (!T[a.p] || !canRead(a.p, uid)) return { data: null, error: { code: 'P0002', message: 'not found ' + a.p } }; if (!canWrite(a.p, uid)) return { data: null, error: { code: '42501', message: 'rls' } };
    T[a.p] = { data: merge(T[a.p].data, clone(a.patch)), u: new Date().toISOString() }; LOG.push([uid, 'update', a.p]); broadcast('UPDATE', a.p, T[a.p].data); return { data: clone(T[a.p].data), error: null }; }
  if (name === 'doc_acquire') { const lp = '_locks/' + a.p.replace(/\//g, '~'), d = (T[lp] || {}).data || {};
    if (d.until > a.t && d.holder !== a.holder) return { data: { acquired: false, holder: d.holder, until: d.until }, error: null };
    T[lp] = { data: { holder: a.holder, until: a.t + a.ttl }, u: new Date().toISOString() }; return { data: { acquired: true, until: a.t + a.ttl }, error: null }; }
  return { data: null, error: { message: 'fake: rpc ' + name } };
}
function auth(a) { const e = String(a.email || '').toLowerCase();
  if (a.op === 'signUp') { if (USERS[e]) return { data: { user: { id: USERS[e].u.id, identities: [] }, session: null }, error: null };
    if (String(a.password).length < 6) return { data: null, error: { message: 'Password should be at least 6 characters' } };
    const u = { id: require('crypto').randomUUID(), email: e, user_metadata: a.meta || {}, identities: [{}] }; USERS[e] = { pw: a.password, u }; return { data: { user: u }, error: null }; }
  if (a.op === 'signIn') { const r = USERS[e]; if (!r || r.pw !== a.password) return { data: null, error: { message: 'Invalid login credentials' } }; return { data: { user: r.u }, error: null }; }
  return { data: null, error: { message: 'fake auth op' } };
}
http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*'); res.setHeader('Access-Control-Allow-Headers', '*'); if (req.method === 'OPTIONS') return res.end();
  if (req.url.startsWith('/live')) { res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' }); res.write(': hi\n\n'); subs.add(res); req.on('close', () => subs.delete(res)); return; }
  if (req.url.startsWith('/dump')) { res.setHeader('Content-Type', 'application/json'); return res.end(JSON.stringify({ T, LOG: LOG.slice(-500), users: Object.keys(USERS) })); }
  let b = ''; req.on('data', c => b += c); req.on('end', () => { let out; try { const m = JSON.parse(b || '{}');
    out = req.url.startsWith('/q') ? exec(m.q, m.uid) : req.url.startsWith('/rpc') ? rpc(m.name, m.args || {}, m.uid) : req.url.startsWith('/auth') ? auth(m) : { error: { message: 'bad url' } }; }
    catch (e) { out = { data: null, error: { message: String(e.message || e) } }; }
    res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(out)); });
}).listen(PORT, () => console.log('fake supabase on', PORT));
