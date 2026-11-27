"""Re-encode a GLB's large JPEG textures at a smaller size (mobile): python3 tex1024.py <in> <out> [max=1024] [quality=86].
Only images larger than max are touched; everything else in the file is copied byte for byte."""
import sys, json, struct, io
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]; MX = int(sys.argv[3]) if len(sys.argv) > 3 else 1024; Q = int(sys.argv[4]) if len(sys.argv) > 4 else 86
b = open(src, 'rb').read(); jl = struct.unpack_from('<I', b, 12)[0]; J = json.loads(b[20:20 + jl]); bo = 20 + jl; bl = struct.unpack_from('<I', b, bo)[0]; BIN = b[bo + 8: bo + 8 + bl]
views = [BIN[(v.get('byteOffset', 0)):(v.get('byteOffset', 0)) + v['byteLength']] for v in J['bufferViews']]; ch = 0
for im in J.get('images', []):
    if 'bufferView' not in im: continue
    d = views[im['bufferView']]; I = Image.open(io.BytesIO(d))
    if max(I.size) <= MX: continue
    s = MX / max(I.size); I2 = I.convert('RGB').resize((round(I.size[0] * s), round(I.size[1] * s)), Image.LANCZOS); o = io.BytesIO()
    if im.get('mimeType') == 'image/png': I2.save(o, 'PNG', optimize=True)
    else: I2.save(o, 'JPEG', quality=Q, optimize=True)
    views[im['bufferView']] = o.getvalue(); ch += 1; print(' ', I.size, '->', I2.size, len(d) // 1024, 'K ->', len(o.getvalue()) // 1024, 'K')
parts = []; off = 0
for i, v in enumerate(J['bufferViews']):
    pad = (-off) % 4; parts.append(b'\0' * pad); off += pad; v['byteOffset'] = off; v['byteLength'] = len(views[i]); parts.append(views[i]); off += len(views[i])
nb = b''.join(parts); nb += b'\0' * ((-len(nb)) % 4); J['buffers'][0]['byteLength'] = len(nb)
js = json.dumps(J, separators=(',', ':')).encode(); js += b' ' * ((-len(js)) % 4)
open(dst, 'wb').write(struct.pack('<III', 0x46546C67, 2, 28 + len(js) + len(nb)) + struct.pack('<II', len(js), 0x4E4F534A) + js + struct.pack('<II', len(nb), 0x004E4942) + nb)
print(src.split('/')[-1], 'images changed', ch)
