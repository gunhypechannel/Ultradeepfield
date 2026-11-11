import numpy as np
from ckpt import load
def nm(base, i): return base if i == 0 else f"{base}_{i}"
def conv_s2(x, W, b):  # TF SAME, k5, s2: out[o] = sum_k x[2o+k-1] W[k]
    H, Wd, C = x.shape; Ho, Wo = H // 2, Wd // 2; xp = np.zeros((H + 3, Wd + 3, C), np.float32); xp[1:H+1, 1:Wd+1] = x
    out = np.zeros((Ho, Wo, W.shape[3]), np.float32)
    for ky in range(5):
        for kx in range(5): out += xp[ky:ky + 2*Ho:2, kx:kx + 2*Wo:2] @ W[ky, kx]
    return out + b
def deconv_s2(x, W, b):  # TF conv2d_transpose SAME, k5, s2: y[2o+k-1] += x[o] W[k]^T ; W (5,5,out,in)
    H, Wd, C = x.shape; Ho, Wo = 2*H, 2*Wd; y = np.zeros((Ho + 6, Wo + 6, W.shape[2]), np.float32)
    for ky in range(5):
        for kx in range(5): y[ky + 2:ky + 2 + 2*H:2, kx + 2:kx + 2 + 2*Wd:2] += x @ W[ky, kx].T  # index 2o+k-1, offset +3
    return y[3:3 + Ho, 3:3 + Wo] + b
def conv_final(x, W, b):  # k4, dilation 2, SAME: out[i] = sum_k x[i+2k-3] W[k]
    H, Wd, C = x.shape; xp = np.zeros((H + 6, Wd + 6, C), np.float32); xp[3:3+H, 3:3+Wd] = x; out = np.zeros((H, Wd, W.shape[3]), np.float32)
    for ky in range(4):
        for kx in range(4): out += xp[2*ky:2*ky + H, 2*kx:2*kx + Wd] @ W[ky, kx]
    return out + b
def bn(x, T, i): p = nm("batch_normalization", i); return (x - T[p + "/moving_mean"]) / np.sqrt(T[p + "/moving_variance"] + 1e-3) * T[p + "/gamma"] + T[p + "/beta"]
lrelu = lambda x: np.where(x > 0, x, .2 * x); relu = lambda x: np.maximum(x, 0)
elu = lambda x: np.where(x > 0, x, np.expm1(np.minimum(x, 0)))
ACT = {'enc': None, 'dec': None}
def unet(x, T, s, logit=False):  # x: (512, 1024, 2) magnitude; s: instrument index
    c0, t0, b0 = 7 * s, 6 * s, 12 * s; C = lambda i: (T[nm("conv2d", c0 + i) + "/kernel"], T[nm("conv2d", c0 + i) + "/bias"]); D = lambda i: (T[nm("conv2d_transpose", t0 + i) + "/kernel"], T[nm("conv2d_transpose", t0 + i) + "/bias"])
    convs = []; h = x
    for i in range(6):
        c = conv_s2(h, *C(i)); convs.append(c); h = (ACT['enc'] or lrelu)(bn(c, T, b0 + i))
    u = convs[5]
    for i in range(5):
        u = bn((ACT['dec'] or relu)(deconv_s2(u, *D(i))), T, b0 + 6 + i); u = np.concatenate([convs[4 - i], u], -1)
    u = bn((ACT['dec'] or relu)(deconv_s2(u, *D(5))), T, b0 + 11)
    z = conv_final(u, *C(6))
    if logit: return z
    return 1 / (1 + np.exp(-np.clip(z, -60, 60))) * x

def softmax_unet(x, T, n):  # spleeter softmax_unet (5stems): logits per instrument, softmax across instruments, times the input
    z = np.stack([unet(x, T, s, True) for s in range(n)]); z -= z.max(0); e = np.exp(z); return e / e.sum(0) * x
