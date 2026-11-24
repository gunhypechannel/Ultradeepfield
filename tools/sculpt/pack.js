// Simplify a baked hull (raw P/N/A/E/F from sdf.py) and pack it: node pack.js <dir> <target tris> <out.bin>
// Format CNT2 (little-endian): u32 magic 0x324E5443, u32 nv, u32 ni, f32 bbox[6], then u16 pos[nv*3] (padded to 4), i8 nrm[nv*4],
// u8 alb[nv*4] (rgb albedo, a = roughness), u8 emi[nv*4] (rgb emissive, a = metalness), then indices (u16 if nv < 65536, else u32).
const fs = require('fs'), path = require('path'), S = require(process.env.MESHOPT || path.join(__dirname, 'mo.js'));
const [dir, tgt, out, maxErr] = [process.argv[2], +process.argv[3] || 60000, process.argv[4], +process.argv[5] || .004];
const f32 = f => { const b = fs.readFileSync(path.join(dir, f)); return new Float32Array(b.buffer, b.byteOffset, b.byteLength / 4); };
(async () => { await S.ready; S.useExperimentalFeatures = true; const P = f32('P.bin'), N = f32('N.bin'), A = f32('A.bin'), E = f32('E.bin'), Fb = fs.readFileSync(path.join(dir, 'F.bin')), F = new Uint32Array(Fb.buffer, Fb.byteOffset, Fb.byteLength / 4), nv = P.length / 3;
  const at = new Float32Array(nv * 7); for (let i = 0; i < nv; i++) { at[i * 7] = A[i * 4]; at[i * 7 + 1] = A[i * 4 + 1]; at[i * 7 + 2] = A[i * 4 + 2]; at[i * 7 + 3] = E[i * 4] * .6; at[i * 7 + 4] = N[i * 3]; at[i * 7 + 5] = N[i * 3 + 1]; at[i * 7 + 6] = N[i * 3 + 2]; }
  const [I, err] = tgt * 3 >= F.length ? [F, 0] : S.simplifyWithAttributes(F, P, 3, at, 7, [3, 3, 3, 3, .3, .3, .3], null, tgt * 3, maxErr, []);
  const [rem, un] = S.compactMesh(I); const map = new Uint32Array(un); for (let i = 0; i < nv; i++) if (rem[i] !== 0xffffffff) map[rem[i]] = i;
  const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9]; for (const i of map) for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], P[i * 3 + k]); mx[k] = Math.max(mx[k], P[i * 3 + k]); }
  const pos = new Uint16Array(un * 3 + (un * 3) % 2), nrm = new Int8Array(un * 4), alb = new Uint8Array(un * 4), emi = new Uint8Array(un * 4), q = (v, k) => Math.round((v - mn[k]) / Math.max(1e-6, mx[k] - mn[k]) * 65535), c = v => Math.max(0, Math.min(255, Math.round(v * 255)));
  for (let j = 0; j < un; j++) { const i = map[j]; for (let k = 0; k < 3; k++) { pos[j * 3 + k] = q(P[i * 3 + k], k); nrm[j * 4 + k] = Math.round(N[i * 3 + k] * 127); } for (let k = 0; k < 4; k++) { alb[j * 4 + k] = c(Math.sqrt(Math.max(0, A[i * 4 + k]))); emi[j * 4 + k] = c(k < 3 ? E[i * 4 + k] : E[i * 4 + 3]); } }
  const big = un > 65535, idx = big ? new Uint32Array(I) : new Uint16Array(I), hdr = Buffer.alloc(36); hdr.writeUInt32LE(0x324E5443, 0); hdr.writeUInt32LE(un, 4); hdr.writeUInt32LE(I.length, 8); for (let k = 0; k < 3; k++) { hdr.writeFloatLE(mn[k], 12 + k * 4); hdr.writeFloatLE(mx[k], 24 + k * 4); }
  const parts = [hdr, Buffer.from(pos.buffer), Buffer.from(nrm.buffer), Buffer.from(alb.buffer), Buffer.from(emi.buffer), Buffer.from(idx.buffer)]; fs.writeFileSync(out, Buffer.concat(parts));
  console.log(out, 'tris', F.length / 3, '->', I.length / 3, 'verts', un, 'bytes', fs.statSync(out).size, 'err', (+err).toFixed(4)); })();
