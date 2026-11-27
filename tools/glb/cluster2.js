// Crack-free vertex clustering for Meshy GLBs (one primitive, interleaved POSITION/NORMAL/TEXCOORD_0 at stride 32):
// node cluster2.js <in> <out> <ratio>. Positions cluster on one grid for the whole mesh (so every UV island moves its seam vertices to the
// same point: no cracks); each island gets its own new vertex per cell (normal averaged, UV from its vertex nearest the cell's point).
const fs = require('fs'), path = require('path');
const [inp, out, ratio] = [process.argv[2], process.argv[3], +process.argv[4] || .4];
const b = fs.readFileSync(inp), jl = b.readUInt32LE(12), J = JSON.parse(b.slice(20, 20 + jl).toString()), bo = 20 + jl, bl = b.readUInt32LE(bo), BIN = b.slice(bo + 8, bo + 8 + bl);
const view = i => { const v = J.bufferViews[i]; return BIN.slice(v.byteOffset || 0, (v.byteOffset || 0) + v.byteLength); };
const pr = J.meshes[0].primitives[0], A = pr.attributes, ia = J.accessors[pr.indices], pa = J.accessors[A.POSITION], na = J.accessors[A.NORMAL], ua = J.accessors[A.TEXCOORD_0];
if (Object.keys(A).length !== 3 || !(A.POSITION != null && A.NORMAL != null && A.TEXCOORD_0 != null) || [pa, na, ua].some(a => a.componentType !== 5126)) { console.log(path.basename(inp), "layout not supported, skipped"); process.exit(2); }
/* read any float layout (interleaved or separate) into one stride-8 array */
const nv = pa.count, S8 = 8, F = new Float32Array(nv * 8);
for (const [a, off, n] of [[pa, 0, 3], [na, 3, 3], [ua, 6, 2]]) { const bv = J.bufferViews[a.bufferView], st = bv.byteStride || n * 4, base = (bv.byteOffset || 0) + (a.byteOffset || 0); for (let v = 0; v < nv; v++) for (let k = 0; k < n; k++) F[v * 8 + off + k] = BIN.readFloatLE(base + v * st + k * 4); }
const ib = view(ia.bufferView).slice(ia.byteOffset || 0), I = ia.componentType === 5125 ? new Uint32Array(ib.buffer.slice(ib.byteOffset, ib.byteOffset + ia.count * 4)) : Uint32Array.from(new Uint16Array(ib.buffer.slice(ib.byteOffset, ib.byteOffset + ia.count * 2)));
const nt = I.length / 3, X = v => F[v * S8], Y = v => F[v * S8 + 1], Z = v => F[v * S8 + 2];
const par = new Int32Array(nv).map((_, i) => i), f = x => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; }, un = (a, c) => { a = f(a); c = f(c); if (a !== c) par[a] = c; };
for (let t = 0; t < nt; t++) { un(I[t * 3], I[t * 3 + 1]); un(I[t * 3], I[t * 3 + 2]); } const isl = new Int32Array(nv); for (let v = 0; v < nv; v++) isl[v] = f(v);
let mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9]; for (let v = 0; v < nv; v++) { mn = [Math.min(mn[0], X(v)), Math.min(mn[1], Y(v)), Math.min(mn[2], Z(v))]; mx = [Math.max(mx[0], X(v)), Math.max(mx[1], Y(v)), Math.max(mx[2], Z(v))]; }
const diag = Math.hypot(mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2]);
// each island's thinnest extent: thin parts (wire domes, antennas, struts) stay at full detail, or they shatter into floating shards
const gp = new Int32Array(nv).map((_, i) => i), gf = x => { while (gp[x] !== x) { gp[x] = gp[gp[x]]; x = gp[x]; } return x; }, gu = (a, c) => { a = gf(a); c = gf(c); if (a !== c) gp[a] = c; };
for (let v = 0; v < nv; v++) gu(v, isl[v]); { const pk = new Map(); for (let v = 0; v < nv; v++) { const k = X(v).toFixed(5) + "," + Y(v).toFixed(5) + "," + Z(v).toFixed(5), o = pk.get(k); if (o == null) pk.set(k, v); else gu(v, o); } }
const geo = new Int32Array(nv); for (let v = 0; v < nv; v++) geo[v] = gf(v);
const ib0 = new Map(); for (let v = 0; v < nv; v++) { let q = ib0.get(geo[v]); if (!q) { q = [1e9, 1e9, 1e9, -1e9, -1e9, -1e9]; ib0.set(geo[v], q); } q[0] = Math.min(q[0], X(v)); q[1] = Math.min(q[1], Y(v)); q[2] = Math.min(q[2], Z(v)); q[3] = Math.max(q[3], X(v)); q[4] = Math.max(q[4], Y(v)); q[5] = Math.max(q[5], Z(v)); }
const thin = new Float32Array(nv); for (let v = 0; v < nv; v++) { const q = ib0.get(geo[v]); thin[v] = Math.max(q[3] - q[0], q[4] - q[1], q[5] - q[2]); }
const THIN = +process.env.THIN || 4; /* a detached piece smaller than THIN cells keeps every vertex */
function run(G) { const cs = diag / G, cellOf = new Int32Array(nv), cells = new Map(), C = [];
  for (let v = 0; v < nv; v++) { const k = Math.floor((X(v) - mn[0]) / cs) + "," + Math.floor((Y(v) - mn[1]) / cs) + "," + Math.floor((Z(v) - mn[2]) / cs); const k2 = thin[v] < cs * THIN ? "v" + v : k; let c = cells.get(k2); if (c == null) { c = C.length; cells.set(k2, c); C.push({ s: [0, 0, 0], n: 0, vs: [] }); } const o = C[c]; o.s[0] += X(v); o.s[1] += Y(v); o.s[2] += Z(v); o.n++; o.vs.push(v); cellOf[v] = c; }
  const cp = C.map(o => { const m = o.s.map(x => x / o.n); let best = o.vs[0], bd = 1e18; for (const v of o.vs) { const d = (X(v) - m[0]) ** 2 + (Y(v) - m[1]) ** 2 + (Z(v) - m[2]) ** 2; if (d < bd) { bd = d; best = v; } } return [X(best), Y(best), Z(best)]; });
  const nvMap = new Map(), NV = [], rep = new Int32Array(nv);
  for (let v = 0; v < nv; v++) { const key = cellOf[v] * 1e7 + isl[v]; let r = nvMap.get(key); if (r == null) { r = NV.length; nvMap.set(key, r); NV.push({ c: cellOf[v], vs: [] }); } NV[r].vs.push(v); rep[v] = r; }
  const R = [], seen = new Set(); for (let t = 0; t < nt; t++) { const a = rep[I[t * 3]], c = rep[I[t * 3 + 1]], d = rep[I[t * 3 + 2]]; if (a === c || c === d || a === d) continue; const key = a < c ? (c < d ? a + "," + c + "," + d : a < d ? a + "," + d + "," + c : d + "," + a + "," + c) : (a < d ? c + "," + a + "," + d : c < d ? c + "," + d + "," + a : d + "," + c + "," + a); if (seen.has(key)) continue; seen.add(key); R.push(a, c, d); }
  return { R, NV, cp }; }
let lo = 6, hi = 3000, best = null; const want = nt * ratio; for (let it = 0; it < 20; it++) { const G = Math.sqrt(lo * hi), r = run(G); if (!best || Math.abs(r.R.length / 3 - want) < Math.abs(best.R.length / 3 - want)) best = r; if (r.R.length / 3 > want) hi = G; else lo = G; }
// keep only the new vertices still used, then write them interleaved
const { R, NV, cp } = best, used = new Int32Array(NV.length).fill(-1); let n2 = 0; for (const x of R) if (used[x] < 0) used[x] = n2++;
const OF = new Float32Array(n2 * 8), omn = [1e9, 1e9, 1e9], omx = [-1e9, -1e9, -1e9];
NV.forEach((g, i) => { const j = used[i]; if (j < 0) return; const p = cp[g.c]; let nx = 0, ny = 0, nz = 0, bu = g.vs[0], bd = 1e18; for (const v of g.vs) { nx += F[v * 8 + 3]; ny += F[v * 8 + 4]; nz += F[v * 8 + 5]; const d = (X(v) - p[0]) ** 2 + (Y(v) - p[1]) ** 2 + (Z(v) - p[2]) ** 2; if (d < bd) { bd = d; bu = v; } }
  const nl = Math.hypot(nx, ny, nz) || 1; OF.set([p[0], p[1], p[2], nx / nl, ny / nl, nz / nl, F[bu * 8 + 6], F[bu * 8 + 7]], j * 8); for (let k = 0; k < 3; k++) { omn[k] = Math.min(omn[k], p[k]); omx[k] = Math.max(omx[k], p[k]); } });
const RI = R.map(x => used[x]), big = n2 > 65535, idx = big ? Buffer.from(new Uint32Array(RI).buffer) : Buffer.from(Uint16Array.from(RI).buffer);
ia.count = RI.length; ia.byteOffset = 0; ia.componentType = big ? 5125 : 5123; delete ia.min; delete ia.max; for (const a of [pa, na, ua]) a.count = n2; pa.min = omn; pa.max = omx; const oldV = new Set([na.bufferView, ua.bufferView].filter(x => x !== pa.bufferView));
pa.byteOffset = 0; na.bufferView = ua.bufferView = pa.bufferView; na.byteOffset = 12; ua.byteOffset = 24; J.bufferViews[pa.bufferView].byteStride = 32; J.bufferViews[pa.bufferView].target = 34962;
const parts = []; let off = 0; J.bufferViews.forEach((v, i) => { const d = i === ia.bufferView ? idx : i === pa.bufferView ? Buffer.from(OF.buffer) : oldV.has(i) ? Buffer.alloc(4) : view(i); const pad = (4 - (off % 4)) % 4; if (pad) { parts.push(Buffer.alloc(pad)); off += pad; } v.byteOffset = off; v.byteLength = d.length; parts.push(d); off += d.length; });
let nb = Buffer.concat(parts); const bp = (4 - (nb.length % 4)) % 4; if (bp) nb = Buffer.concat([nb, Buffer.alloc(bp)]); J.buffers[0].byteLength = nb.length;
let js = Buffer.from(JSON.stringify(J)); js = Buffer.concat([js, Buffer.alloc((4 - (js.length % 4)) % 4, 0x20)]);
const hdr = Buffer.alloc(12); hdr.writeUInt32LE(0x46546C67, 0); hdr.writeUInt32LE(2, 4); hdr.writeUInt32LE(12 + 8 + js.length + 8 + nb.length, 8);
const ch = (len, type) => { const c = Buffer.alloc(8); c.writeUInt32LE(len, 0); c.writeUInt32LE(type, 4); return c; };
fs.writeFileSync(out, Buffer.concat([hdr, ch(js.length, 0x4E4F534A), js, ch(nb.length, 0x004E4942), nb]));
console.log(path.basename(inp), nt, '->', RI.length / 3, `tris (${(RI.length / 3 / nt * 100).toFixed(0)}%)`, 'verts', nv, '->', n2, (fs.statSync(inp).size / 1024 | 0) + 'K ->', (fs.statSync(out).size / 1024 | 0) + 'K');
