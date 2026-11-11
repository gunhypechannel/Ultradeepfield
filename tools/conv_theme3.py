# v436 Convergence theme, violin solo (owner: "a strong violin solo, same tempo, same everything, just remaster it in violin"):
# conv_theme2.py with the piano replaced by a bowed violin playing the same motif (C#, A, E, B at 80% pitch, an octave up), legato, with
# bow attacks, vibrato that blooms as a note is held, small slides between notes, a violin-body resonance, and a dynamic arc that
# grows from a quiet opening to a strong, bright climax and back. Everything else (score, arc, timing, hall, loop) is unchanged.
# Original v433 notes: Convergence theme: slower, deeper and sadder, built round the song's own solo piano (owner: "slower and deep/sad sounding,
# isolate the piano, enhance the emotional and cinematic experience"). The song (docs/music.mp3) opens with a 4-note piano motif
# alone (C#, A, E, B, one cycle every ~7 s, played twice in 0-14 s); this takes those two cycles of real piano, plays them at 80%
# speed (slower and ~4 semitones deeper, like a slowed tape), and scores them: F#m - D - A - E strings, cellos, a wordless choir,
# a sub, and a slow heartbeat drum, in an arc: piano alone, strings, the swell, the climax, back to the lone piano (it loops).
# Run in a folder holding song.wav (ffmpeg -i docs/music.mp3 -ar 44100 -ac 2 song.wav), then master:
# ffmpeg -i conv3_raw.wav -af "acompressor=threshold=-20dB:ratio=2:attack=40:release=400:makeup=1.5,loudnorm=I=-14:TP=-1.5:LRA=11" -c:a libmp3lame -b:a 128k music_conv.mp3
import numpy as np, scipy.io.wavfile as w, scipy.signal as sg
sr, x = w.read('song.wav'); x = x.astype(np.float32) / 32768; rng = np.random.default_rng(11)
K = .8                                   # 80% speed: slower and deeper
C0 = .18; CYC = 7.0                      # the motif's first note, and one cycle, in the song
ON = [0, 1.79, 3.42, 5.13]               # its four notes within a cycle (chord changes)
cyc = [x[int((C0 + i * CYC - .05) * sr):int((C0 + (i + 1) * CYC + 1.6) * sr)] for i in range(2)]  # a little tail past the cycle (the decay)
cyc = [sg.resample_poly(c, 5, 4, axis=0).astype(np.float32) for c in cyc]   # 1/0.8 longer, pitch x0.8
for c in cyc: f = np.minimum(1, np.arange(len(c)) / (.02 * sr)); c *= f[:, None]
CY = CYC / K                             # one cycle after slowing (8.75 s)
NC = 12; L = int((NC * CY + 8) * sr); out = np.zeros((L, 2), np.float32); t = np.arange(L) / sr
mt = lambda m: 440 * 2 ** ((m - 69) / 12) * K   # every synth note is in the slowed key
# chords under the four notes (original key): F#m, D, A, E
CH = [[42, 54, 57, 61, 66], [38, 50, 54, 57, 62], [45, 52, 57, 61, 64], [40, 52, 56, 59, 64]]
BASS = [30, 26, 33, 28]
# the arc: per cycle, how loud each layer is (piano, strings, cello, choir, drum, sub)
ARC = [(1, 0, 0, 0, 0, .3), (1, .25, 0, 0, 0, .5), (1, .5, .3, 0, 0, .7), (1, .65, .55, .2, .3, .8), (1, .75, .7, .4, .5, .9), (1, .9, .85, .6, .7, 1),
       (1, 1, 1, .85, 1, 1), (1, 1, 1, 1, 1, 1), (1, .7, .6, .6, .4, .8), (1, .45, .35, .3, 0, .6), (1, .2, .1, 0, 0, .4), (1, 0, 0, 0, 0, .25)]
def env(n, a, r, hold):
    e = np.ones(n, np.float32); ia = int(a * sr); ir = int(r * sr); e[:ia] = np.linspace(0, 1, ia) ** 2
    h = int(hold * sr); e[h:h + ir] *= np.linspace(1, 0, min(ir, n - h)) ** 1.5 if h < n else 1; e[h + ir:] = 0; return e
def lp(y, fc, o=2): b, a = sg.butter(o, min(.99, fc / (sr / 2))); return sg.lfilter(b, a, y).astype(np.float32)
def strings(m, dur, v):    # a section: detuned saws, slow bow, vibrato, warm lowpass
    n = int((dur + 3) * sr); tt = np.arange(n) / sr; s = np.zeros(n, np.float32)
    for d in (-.11, -.04, .03, .1): vib = .003 * np.sin(2 * np.pi * (4.6 + d * 5) * tt + rng.random() * 6); s += sg.sawtooth(2 * np.pi * mt(m + d) * tt * (1 + vib) + rng.random() * 6)
    return lp(lp(s, 1500 + 400 * (m > 55)), 2600) * env(n, 1.6, 2.6, dur) * v / 4
def choir(m, dur, v):      # wordless "ah": a buzz through vowel formants
    n = int((dur + 3) * sr); tt = np.arange(n) / sr; s = np.zeros(n, np.float32)
    for d in (-.07, 0, .06): s += sg.sawtooth(2 * np.pi * mt(m + d) * tt * (1 + .004 * np.sin(2 * np.pi * 5.2 * tt + d * 30)))
    y = np.zeros(n, np.float32)
    for fc, bw, g in [(700, 110, 1), (1220, 140, .5), (2600, 220, .2)]: b, a = sg.iirpeak(fc / (sr / 2), fc / bw); y += g * sg.lfilter(b, a, s)
    return lp(y, 3000) * env(n, 2.2, 3, dur) * v / 3
def heart(at, v):          # a low, soft heartbeat: two muffled thumps
    for dt, g in [(0, 1), (.32, .6)]:
        i0 = int((at + dt) * sr); n = int(1.2 * sr); tt = np.arange(n) / sr; f0 = 52
        y = np.sin(2 * np.pi * (f0 * tt - 14 * .08 * (1 - np.exp(-tt / .08)))) * np.exp(-tt / .4) * v * g * .5
        i1 = min(L, i0 + n); out[i0:i1, 0] += y[:i1 - i0]; out[i0:i1, 1] += y[:i1 - i0]
pad = np.zeros((L, 2), np.float32); pno = np.zeros((L, 2), np.float32)
for c in range(NC):
    t0 = 4 + c * CY; a = ARC[c]
    for k, o in enumerate(ON):
        at = t0 + o / K; dur = ((ON[k + 1] if k < 3 else CYC) - o) / K; j0 = int(at * sr)
        def add(y, pan):
            j1 = min(L, j0 + len(y)); pad[j0:j1, 0] += y[:j1 - j0] * (1 - pan); pad[j0:j1, 1] += y[:j1 - j0] * (1 + pan)
        if a[1]: [add(strings(m, dur, .16 * a[1]), (i - 2) * .25) for i, m in enumerate(CH[k][1:])]
        if a[2]: add(strings(BASS[k] + 12, dur, .3 * a[2]), -.2); add(strings(BASS[k] + 24, dur, .14 * a[2]), .2)
        if a[3]: [add(choir(m, dur, .1 * a[3]), (i - 1) * .4) for i, m in enumerate(CH[k][2:5])]
        if a[5]: n = int((dur + 2) * sr); tt = np.arange(n) / sr; y = (np.sin(2 * np.pi * mt(BASS[k]) * tt) * .6 + .25 * np.sin(2 * np.pi * mt(BASS[k] + 12) * tt)) * env(n, .8, 2, dur) * .22 * a[5]; add(y, 0)
        if a[4] and k in (0, 2): heart(at, .9 * a[4])

# ---- the violin: one legato line over the whole piece ----
MEL = [73, 69, 76, 71]                                  # the song's C#4, A3, E4, B3 an octave up (at 80% pitch the A would sit below the violin's lowest string), the violin's singing register
DYN = [.42, .52, .62, .7, .8, .9, 1, 1, .86, .7, .55, .42]   # per cycle: quiet opening, strong climax, quiet close
notes = []
for c in range(NC):
    for k, o in enumerate(ON):
        at = 4 + c * CY + o / K; nx = 4 + c * CY + (ON[k + 1] if k < 3 else CYC) / K; notes.append((at, nx, MEL[k], DYN[c]))
f0 = np.zeros(L, np.float32); A = np.zeros(L, np.float32); BR = np.zeros(L, np.float32); prev = None
for j, (a0, a1, m, d) in enumerate(notes):
    i0, i1 = int(a0 * sr), min(L, int(a1 * sr)); n = i1 - i0; tt = np.arange(n) / sr; ft = mt(m)
    if prev is not None: ft = ft + (mt(prev) - ft) * np.exp(-tt / .055)             # a short slide from the last note
    dep = (.12 + .14 * d) * np.minimum(1, np.maximum(0, tt - .18) / .55)              # vibrato blooms after the bow settles (in semitones)
    vr = 5.4 + .5 * np.sin(j * 1.3); f0[i0:i1] = ft * 2 ** (dep * np.sin(2 * np.pi * vr * tt + j) / 12)
    dur = n / sr; u = tt / dur; att = np.minimum(1, tt / .11) ** 1.5; bite = 1 + .25 * np.exp(-tt / .06) * d
    sw = .78 + .22 * np.sin(np.pi * np.minimum(1, u * 1.15)); chg = np.minimum(1, (dur - tt) / .07) * .35 + .65   # swell, and the bow change at the end
    A[i0:i1] = att * bite * sw * chg * (.55 + .45 * d); BR[i0:i1] = .45 + .55 * d * sw; prev = m
last = notes[-1]; i1 = int(last[1] * sr); rel = np.exp(-np.arange(L - i1) / (1.2 * sr)); A[i1:] = A[i1 - 1] * rel; f0[i1:] = f0[i1 - 1]; BR[i1:] = BR[i1 - 1]
A[:int(4 * sr)] = 0; A = lp(lp(A, 30), 30); BR = lp(BR, 8)
ph = 2 * np.pi * np.cumsum(f0) / sr; vio = np.zeros(L, np.float32); jit = lp(rng.standard_normal(L).astype(np.float32), 40) * .05
for h in range(1, 34):                                   # a bowed string: harmonics falling off like a sawtooth, darker when played softly
    fh = f0 * h; amp = np.where(fh < 9000, h ** -(.85 + 1.1 * (1 - BR)), 0).astype(np.float32); vio += amp * np.sin(h * ph + h * 1.7) * (1 + jit * (h % 3))
vio *= A
# the body: the wood's resonances (air, the two main body modes, the bridge hill), then a gentle top
body = vio * .6
for fc, q, g in [(280, 4, 1.6), (460, 3.5, 1.3), (590, 3, 1.0), (2600, 2.2, 1.4), (3400, 3, .9)]:
    b, a = sg.iirpeak(fc / (sr / 2), q); body += g * sg.lfilter(b, a, vio).astype(np.float32)
b, a = sg.butter(2, 150 / (sr / 2), 'high'); body = sg.lfilter(b, a, body).astype(np.float32); body = lp(body, 7500)
bow = sg.lfilter(*sg.butter(2, [2200 / (sr / 2), 6500 / (sr / 2)], 'band'), rng.standard_normal(L)).astype(np.float32) * A * .012
vio = body + bow; vio /= np.max(np.abs(vio)) + 1e-9
pno = np.stack([vio * .95, vio * .9], 1) * 1.0          # (the solo sits in the middle of the hall, as the piano did)
# the hall: long and dark for the piano (with a pre-delay), a little shorter for the score
def hall(sec, damp, pre):
    n = int(sec * sr); it = np.arange(n) / sr; irs = []
    for ch in range(2):
        nz = rng.standard_normal(n).astype(np.float32) * np.exp(-it / (sec / 6.9)); nz = lp(nz, damp); p = int(pre * sr); nz = np.concatenate([np.zeros(p, np.float32), nz])[:n]; irs.append(nz / np.sqrt((nz ** 2).sum()))
    return irs
IRp, IRs = hall(6.5, 3200, .045), hall(4.5, 2600, .02)
wetp = np.stack([sg.fftconvolve(pno[:, c], IRp[c])[:L] for c in range(2)], 1); wets = np.stack([sg.fftconvolve(pad[:, c], IRs[c])[:L] for c in range(2)], 1)
out += pno * .7 + wetp * .8 + pad * 1.25 + wets * 1.4
out[:, 0] += lp(out[:, 0], 120) * .15; out[:, 1] += lp(out[:, 1], 120) * .15  # a little weight below
y = out / np.max(np.abs(out)) * .97
LOOP = int((4 + NC * CY) * sr); y = y[:LOOP + int(4 * sr)]            # the reverb tail of the last cycle crossfades into the start
X = int(4 * sr); fade = np.linspace(0, 1, X)[:, None]; head = y[:X].copy(); y[:X] = head * fade + y[LOOP:LOOP + X] * (1 - fade); y = y[:LOOP]
w.write('conv3_raw.wav', sr, (y * 32767).astype(np.int16)); print('len', round(len(y) / sr, 1), 's')
