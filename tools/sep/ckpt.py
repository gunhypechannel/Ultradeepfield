import struct, numpy as np
def varint(b, i):
    r = s = 0
    while True:
        c = b[i]; i += 1; r |= (c & 0x7f) << s; s += 7
        if c < 128: return r, i
def block(b, off, size):
    d = b[off:off+size]; assert b[off+size] == 0, "compressed block"
    nre = struct.unpack('<I', d[-4:])[0]; end = len(d) - 4 - 4*nre; i = 0; key = b''; out = []
    while i < end:
        sh, i = varint(d, i); ns, i = varint(d, i); vl, i = varint(d, i)
        key = key[:sh] + d[i:i+ns]; i += ns; out.append((key, d[i:i+vl])); i += vl
    return out
def pb(buf):
    i = 0; f = {}
    while i < len(buf):
        k, i = varint(buf, i); fn, wt = k >> 3, k & 7
        if wt == 0: v, i = varint(buf, i)
        elif wt == 2: l, i = varint(buf, i); v = buf[i:i+l]; i += l
        elif wt == 5: v = buf[i:i+4]; i += 4
        elif wt == 1: v = buf[i:i+8]; i += 8
        f.setdefault(fn, []).append(v)
    return f
def load(prefix):
    b = open(prefix + '.index', 'rb').read(); ft = b[-48:]; i = 0
    _, i = varint(ft, i); _, i = varint(ft, i); io, i = varint(ft, i); isz, i = varint(ft, i)
    data = open(prefix + '.data-00000-of-00001', 'rb').read(); T = {}
    for _, h in block(b, io, isz):
        o, j = varint(h, 0); s, j = varint(h, j)
        for k, v in block(b, o, s):
            if not k: continue
            e = pb(v); dt = e.get(1, [1])[0]; shape = [pb(d).get(1, [0])[0] for d in pb(e[2][0]).get(2, [])] if 2 in e else []
            off = e.get(4, [0])[0]; sz = e.get(5, [0])[0]
            if dt != 1: continue
            T[k.decode()] = np.frombuffer(data[off:off+sz], np.float32).reshape(shape)
    return T
if __name__ == '__main__':
    import sys; T = load(sys.argv[1])
    for k in sorted(T)[:80]: print(k, T[k].shape)
    print(len(T))
