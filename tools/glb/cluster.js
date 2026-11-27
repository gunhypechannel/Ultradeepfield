// Vertex-clustering simplifier for single-primitive GLBs whose meshes are split on UV seams (Meshy): node cluster.js <in> <out> <ratio>
// Within each UV island (triangles joined through shared vertex indices) vertices falling in the same grid cell collapse onto the cell's
// most central existing vertex (its position, normal and UV are kept as they are: no new attributes). Vertices on an island's edge (their
// position is also used by another island) never move, so seams cannot open into cracks. The grid size is searched for the target count.
const fs = require('fs'), path = require('path');
const [inp, out, ratio] = [process.argv[2], process.argv[3], +process.argv[4] || .4];
const b = fs.readFileSync(inp), jl = b.readUInt32LE(12), J = JSON.parse(b.slice(20, 20 + jl).toString()), bo = 20 + jl, bl = b.readUInt32LE(bo), BIN = b.slice(bo + 8, bo + 8 + bl);
const view = i => { const v = J.bufferViews[i]; return BIN.slice(v.byteOffset || 0, (v.byteOffset || 0) + v.byteLength); };
const pr = J.meshes[0].primitives[0], ia = J.accessors[pr.indices], pa = J.accessors[pr.attributes.POSITION], pvw = J.bufferViews[pa.bufferView], st = (pvw.byteStride || 12) / 4;
const pb = view(pa.bufferView), P = new Float32Array(pb.buffer.slice(pb.byteOffset + (pa.byteOffset || 0), pb.byteOffset + pb.byteLength)), nv = pa.count;
const ib = view(ia.bufferView).slice(ia.byteOffset || 0), I = ia.componentType === 5125 ? new Uint32Array(ib.buffer.slice(ib.byteOffset, ib.byteOffset + ia.count * 4)) : Uint32Array.from(new Uint16Array(ib.buffer.slice(ib.byteOffset, ib.byteOffset + ia.count * 2)));
const nt = I.length / 3, X = v => P[v * st], Y = v => P[v * st + 1], Z = v => P[v * st + 2];
// islands of vertices (union-find over each triangle's three vertices)
const par = new Int32Array(nv).map((_, i) => i), f = x => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; }, un = (a, c) => { a = f(a); c = f(c); if (a !== c) par[a] = c; };
for (let t = 0; t < nt; t++) { un(I[t * 3], I[t * 3 + 1]); un(I[t * 3], I[t * 3 + 2]); }
const isl = new Int32Array(nv); for (let v = 0; v < nv; v++) isl[v] = f(v);
// edge vertices: their quantized position is also used by a vertex of another island
let mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9]; for (let v = 0; v < nv; v++) { mn = [Math.min(mn[0], X(v)), Math.min(mn[1], Y(v)), Math.min(mn[2], Z(v))]; mx = [Math.max(mx[0], X(v)), Math.max(mx[1], Y(v)), Math.max(mx[2], Z(v))]; }
const diag = Math.hypot(mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2]), q = 1e-5 * diag, pk = v => Math.round(X(v) / q) + "," + Math.round(Y(v) / q) + "," + Math.round(Z(v) / q);
const owner = new Map(), edge = new Uint8Array(nv); for (let v = 0; v < nv; v++) { const k = pk(v), o = owner.get(k); if (o == null) owner.set(k, isl[v]); else if (o !== isl[v]) edge[v] = 1; }
for (let v = 0; v < nv; v++) if (!edge[v] && owner.get(pk(v)) !== isl[v]) edge[v] = 1; // the first owner's twins too
for (let v = 0; v < nv; v++) { const k = pk(v); if (edge[v]) owner.set(k, -1); } for (let v = 0; v < nv; v++) if (owner.get(pk(v)) === -1) edge[v] = 1;
function run(G) { const cs = diag / G, cell = new Map(), rep = new Uint32Array(nv);
  for (let v = 0; v < nv; v++) { if (edge[v]) { rep[v] = v; continue; } const k = isl[v] + "|" + Math.floor((X(v) - mn[0]) / cs) + "," + Math.floor((Y(v) - mn[1]) / cs) + "," + Math.floor((Z(v) - mn[2]) / cs); let c = cell.get(k); if (!c) cell.set(k, c = { s: [0, 0, 0], n: 0, vs: [] }); c.s[0] += X(v); c.s[1] += Y(v); c.s[2] += Z(v); c.n++; c.vs.push(v); }
  for (const c of cell.values()) { const m = c.s.map(x => x / c.n); let best = c.vs[0], bd = 1e18; for (const v of c.vs) { const d = (X(v) - m[0]) ** 2 + (Y(v) - m[1]) ** 2 + (Z(v) - m[2]) ** 2; if (d < bd) { bd = d; best = v; } } for (const v of c.vs) rep[v] = best; }
  const R = [], seen = new Set(); for (let t = 0; t < nt; t++) { const a = rep[I[t * 3]], c = rep[I[t * 3 + 1]], d = rep[I[t * 3 + 2]]; if (a === c || c === d || a === d) continue; const key = [a, c, d].sort((x, y) => x - y).join(","); if (seen.has(key)) continue; seen.add(key); R.push(a, c, d); }
  return R; }
let lo = 8, hi = 2000, best = null; const want = nt * ratio; for (let it = 0; it < 18; it++) { const G = Math.sqrt(lo * hi), R = run(G); if (!best || Math.abs(R.length / 3 - want) < Math.abs(best.length / 3 - want)) best = R; if (R.length / 3 > want) hi = G; else lo = G; }
const R = best, data = ia.componentType === 5125 ? Buffer.from(new Uint32Array(R).buffer) : Buffer.from(Uint16Array.from(R).buffer); ia.count = R.length; ia.byteOffset = 0; delete ia.min; delete ia.max;
const parts = []; let off = 0; J.bufferViews.forEach((v, i) => { const d = i === ia.bufferView ? data : view(i); const pad = (4 - (off % 4)) % 4; if (pad) { parts.push(Buffer.alloc(pad)); off += pad; } v.byteOffset = off; v.byteLength = d.length; parts.push(d); off += d.length; });
let nb = Buffer.concat(parts); const bp = (4 - (nb.length % 4)) % 4; if (bp) nb = Buffer.concat([nb, Buffer.alloc(bp)]); J.buffers[0].byteLength = nb.length;
let js = Buffer.from(JSON.stringify(J)); js = Buffer.concat([js, Buffer.alloc((4 - (js.length % 4)) % 4, 0x20)]);
const hdr = Buffer.alloc(12); hdr.writeUInt32LE(0x46546C67, 0); hdr.writeUInt32LE(2, 4); hdr.writeUInt32LE(12 + 8 + js.length + 8 + nb.length, 8);
const ch = (len, type) => { const c = Buffer.alloc(8); c.writeUInt32LE(len, 0); c.writeUInt32LE(type, 4); return c; };
fs.writeFileSync(out, Buffer.concat([hdr, ch(js.length, 0x4E4F534A), js, ch(nb.length, 0x004E4942), nb]));
console.log(path.basename(inp), nt, '->', R.length / 3, 'tris', `(${(R.length / 3 / nt * 100).toFixed(0)}%)`, 'islands', new Set(isl).size, 'edge verts', edge.reduce((a, x) => a + x, 0), 'of', nv);
