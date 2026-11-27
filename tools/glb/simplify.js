// Simplify a GLB's triangle count with meshoptimizer (tools/sculpt/mo.js): node simplify.js <in.glb> <out.glb> <ratio> [maxErr]
// Keeps every vertex attribute, texture and material; only each primitive's index buffer is replaced (seams and borders kept).
const fs = require('fs'), path = require('path'), S = require(path.join(__dirname, '..', 'sculpt', 'mo.js'));
const [inp, out, ratio, maxErr] = [process.argv[2], process.argv[3], +process.argv[4] || .4, +process.argv[5] || .02];
(async () => { await S.ready; const b = fs.readFileSync(inp); const jl = b.readUInt32LE(12), J = JSON.parse(b.slice(20, 20 + jl).toString()), bo = 20 + jl, bl = b.readUInt32LE(bo), BIN = b.slice(bo + 8, bo + 8 + bl);
  const view = i => { const v = J.bufferViews[i]; return BIN.slice(v.byteOffset || 0, (v.byteOffset || 0) + v.byteLength); };
  const repl = {}; let t0 = 0, t1 = 0;
  for (const m of J.meshes) for (const p of m.primitives) { if (p.indices == null || (p.mode != null && p.mode !== 4)) continue;
    const ia = J.accessors[p.indices], pa = J.accessors[p.attributes.POSITION]; if (pa.componentType !== 5126 || pa.bufferView == null) continue;
    const pv = J.bufferViews[pa.bufferView], stride = (pv.byteStride || 12) / 4, pb = view(pa.bufferView), P = new Float32Array(pb.buffer.slice(pb.byteOffset + (pa.byteOffset || 0), pb.byteOffset + pb.byteLength));
    const ib = view(ia.bufferView).slice(ia.byteOffset || 0); const I = ia.componentType === 5125 ? new Uint32Array(ib.buffer.slice(ib.byteOffset, ib.byteOffset + ia.count * 4)) : Uint32Array.from(new Uint16Array(ib.buffer.slice(ib.byteOffset, ib.byteOffset + ia.count * 2)));
    const islandOf = (() => { const nt = I.length / 3, par = new Int32Array(nt).map((_, i) => i), f = x => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; }, first = new Map();
      for (let t = 0; t < nt; t++) for (let k = 0; k < 3; k++) { const v = I[t * 3 + k], o = first.get(v); if (o == null) first.set(v, t); else { const a = f(o), b = f(t); if (a !== b) par[a] = b; } }
      const out = {}; for (let t = 0; t < nt; t++) out[t * 3] = f(t); return out; })();
    const tgt = Math.floor(I.length * ratio / 3) * 3;
    /* weld: every vertex at the same position shares one index for the simplifier (the seams Meshy splits on every UV island would
       otherwise lock the mesh); a collapsed triangle then takes, for each corner, the original vertex of the source triangle it came from */
    const nv = P.length / stride, can = new Uint32Array(nv), M = new Map(); for (let v = 0; v < nv; v++) { const k = Math.round(P[v * stride] * 1e4) + "," + Math.round(P[v * stride + 1] * 1e4) + "," + Math.round(P[v * stride + 2] * 1e4); let c = M.get(k); if (c == null) { c = v; M.set(k, v); } can[v] = c; }
    const IW = I.map(v => can[v]); let [R0, err] = S.simplify(IW, P, stride, tgt, maxErr, ["LockBorder"].filter(() => false));
    const twins = new Map(); for (let v = 0; v < nv; v++) { const c = can[v]; if (c !== v) { if (!twins.has(c)) twins.set(c, [c]); twins.get(c).push(v); } }
    /* pick, per output triangle, the UV island used by most of its corners in the source: the vertex of each canonical corner whose source
       triangles share the most corners with the other two */
    const vt = new Map(); for (let t = 0; t < I.length; t += 3) for (let k = 0; k < 3; k++) { const v = I[t + k]; if (!vt.has(v)) vt.set(v, []); vt.get(v).push(t); }
    const R = new Uint32Array(R0.length); for (let t = 0; t < R0.length; t += 3) { const cs = [R0[t], R0[t + 1], R0[t + 2]], opts = cs.map(c => twins.get(c) || [c]);
      let best = null, bs = -1; for (const a of opts[0]) for (const b2 of opts[1]) for (const c of opts[2]) { const isl = v => new Set((vt.get(v) || []).map(x => islandOf[x])); const A = isl(a), B = isl(b2), C = isl(c); let sc = 0; for (const x of A) { if (B.has(x)) sc++; if (C.has(x)) sc++; } for (const x of B) if (C.has(x)) sc++; if (sc > bs) { bs = sc; best = [a, b2, c]; } if (opts[0].length * opts[1].length * opts[2].length > 64) break; }
      R[t] = best[0]; R[t + 1] = best[1]; R[t + 2] = best[2]; }
    t0 += I.length / 3; t1 += R.length / 3; const data = ia.componentType === 5125 ? Buffer.from(new Uint32Array(R).buffer) : Buffer.from(Uint16Array.from(R).buffer);
    repl[ia.bufferView] = data; ia.count = R.length; ia.byteOffset = 0; delete ia.min; delete ia.max; }
  // rebuild the binary chunk view by view, 4-byte aligned
  const parts = []; let off = 0; J.bufferViews.forEach((v, i) => { const d = repl[i] || view(i); const pad = (4 - (off % 4)) % 4; if (pad) { parts.push(Buffer.alloc(pad)); off += pad; } v.byteOffset = off; v.byteLength = d.length; parts.push(d); off += d.length; });
  let nb = Buffer.concat(parts); const bp = (4 - (nb.length % 4)) % 4; if (bp) nb = Buffer.concat([nb, Buffer.alloc(bp)]); J.buffers[0].byteLength = nb.length;
  let js = Buffer.from(JSON.stringify(J)); const jp = (4 - (js.length % 4)) % 4; js = Buffer.concat([js, Buffer.alloc(jp, 0x20)]);
  const hdr = Buffer.alloc(12); hdr.writeUInt32LE(0x46546C67, 0); hdr.writeUInt32LE(2, 4); hdr.writeUInt32LE(12 + 8 + js.length + 8 + nb.length, 8);
  const ch = (len, type) => { const c = Buffer.alloc(8); c.writeUInt32LE(len, 0); c.writeUInt32LE(type, 4); return c; };
  fs.writeFileSync(out, Buffer.concat([hdr, ch(js.length, 0x4E4F534A), js, ch(nb.length, 0x004E4942), nb]));
  console.log(path.basename(inp), Math.round(t0), '->', Math.round(t1), 'tris', (fs.statSync(inp).size / 1024 | 0) + 'K ->', (fs.statSync(out).size / 1024 | 0) + 'K'); })();
