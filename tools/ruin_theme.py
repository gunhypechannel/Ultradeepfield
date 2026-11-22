# Draft (owner: "make another song that sounds like Final Fantasy X Zanarkand"): an ORIGINAL piece in that vein, not a copy of it:
# a slow, wistful solo piano (flowing broken chords under a lyrical right-hand melody, rubato at the phrase ends) that strings and
# cello slowly join, swell, and leave. Its own melody and chords in D minor. Same samples as orch_theme.py (samples.npz, MusyngKite).
# Form (66 bpm, 4/4): intro 2 bars, A (piano alone), A' (+ soft strings), B (strings rise, harp), A'' (melody on strings + piano), coda.
# Output ruin_raw.wav; master: ffmpeg -i ruin_raw.wav -af "acompressor=threshold=-20dB:ratio=1.8:attack=40:release=400:makeup=1.3,loudnorm=I=-15:TP=-1.5:LRA=11" -c:a libmp3lame -b:a 128k music_ruin.mp3
import sys, numpy as np, scipy.signal as sg, scipy.io.wavfile as w
sr = 44100; S = np.load(sys.argv[1] if len(sys.argv) > 1 else 'samples.npz'); rng = np.random.default_rng(11)
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def smp(ins, m): k = f"MusyngKite__{ins}__{NN[m % 12]}{m // 12 - 1}"; return S[k].astype(np.float32) / 32768 if k in S else None
def lp(y, fc, o=2): b, a = sg.butter(o, min(.99, fc / (sr / 2))); return sg.lfilter(b, a, y, axis=0).astype(np.float32)
# ---- the score ----
# chords: (bass, [tones for the broken-chord pattern]) ; melody per bar: (midi, start beat, beats)
D = {'Dm': (38, [45, 50, 53, 57, 62, 57, 53, 50]), 'Bb': (34, [41, 46, 50, 53, 58, 53, 50, 46]), 'F/A': (33, [41, 45, 48, 53, 57, 53, 48, 45]),
     'Gm7': (31, [38, 43, 46, 50, 53, 50, 46, 43]), 'C': (36, [43, 48, 52, 55, 60, 55, 52, 48]), 'Am': (33, [40, 45, 48, 52, 57, 52, 48, 45]),
     'A': (33, [40, 45, 49, 52, 57, 52, 49, 45]), 'Asus': (33, [40, 45, 50, 52, 57, 52, 50, 45]), 'Gm': (31, [38, 43, 46, 50, 55, 50, 46, 43]),
     'F': (29, [36, 41, 45, 48, 53, 48, 45, 41]), 'A7': (33, [40, 45, 49, 55, 57, 55, 49, 45])}
A_CH = ['Dm', 'Bb', 'F/A', 'Gm7', 'C', 'Am', 'Bb', 'A']
A_MEL = [[(69, 0, 1.5), (74, 1.5, .5), (76, 2, 1), (77, 3, 1)], [(76, 0, 1.5), (74, 1.5, .5), (74, 2, 2)],
         [(72, 0, 1), (77, 1, 1), (81, 2, 1.5), (79, 3.5, .5)], [(77, 0, 3), (76, 3, 1)],
         [(76, 0, 1), (79, 1, 1), (77, 2, 1), (76, 3, 1)], [(76, 0, 1.5), (72, 1.5, .5), (69, 2, 2)],
         [(74, 0, 1), (77, 1, 1), (82, 2, 1.5), (81, 3.5, .5)], [(81, 0, 2), (73, 2, 1), (76, 3, 1)]]
A2_LAST = [(76, 0, 1), (73, 1, 1), (74, 2, 2)]                     # the second time, it comes home to D
B_CH = ['Bb', 'C', 'Am', 'Dm', 'Gm', 'C', 'F', 'A7']
B_MEL = [[(77, 0, 1), (82, 1, 1), (86, 2, 2)], [(84, 0, 1.5), (82, 1.5, .5), (81, 2, 1), (79, 3, 1)], [(81, 0, 3), (76, 3, 1)],
         [(77, 0, 1.5), (76, 1.5, .5), (74, 2, 2)], [(74, 0, 1), (79, 1, 1), (82, 2, 1.5), (81, 3.5, .5)],
         [(79, 0, 1.5), (77, 1.5, .5), (76, 1, 1), (79, 3, 1)], [(81, 0, 1.5), (79, 1.5, .5), (77, 2, 1), (72, 3, 1)], [(76, 0, 2), (79, 2, 1), (73, 3, 1)]]
B_MEL[5] = [(79, 0, 1.5), (77, 1.5, .5), (76, 2, 1), (79, 3, 1)]
# sections: (chords, melody, piano mel gain, strings pad, cello, string melody, harp)
SEC = [(['Dm', 'Bb'], [[], []], 0, 0, 0, 0, 0),
       (A_CH, A_MEL, 1, 0, 0, 0, 0),
       (A_CH, A_MEL[:7] + [A2_LAST], 1, .45, .35, 0, 0),
       (B_CH, B_MEL, .9, .8, .7, .0, .6),
       (A_CH, A_MEL, .8, 1, 1, 1, .3),
       (['Bb', 'Gm7', 'Asus', 'Dm'], [A_MEL[6], [(77, 0, 3), (76, 3, 1)], [(76, 0, 2), (73, 2, 2)], [(74, 0, 4)]], .9, .3, .3, 0, 0)]
BPM = 66; q0 = 60 / BPM
bars = []
for si, (ch, mel, *g) in enumerate(SEC):
    for b, c in enumerate(ch): bars.append((si, b, c, mel[b], g))
# rubato: phrase-end bars breathe longer, the first bar of B pushes on a touch
fac = []
for i, (si, b, c, m, g) in enumerate(bars):
    f = 1.0
    if b % 4 == 3: f = 1.07
    if b == 7: f = 1.12
    if si == 5 and b == 3: f = 1.25
    fac.append(f)
T0 = .6; starts = np.concatenate([[T0], T0 + np.cumsum([4 * q0 * f for f in fac])]); LOOP_T = starts[-1]
L = int((LOOP_T + 10) * sr); mix = {}
def bus(n): return mix.setdefault(n, np.zeros((L, 2), np.float32))
def place(bn, y, t, pan):
    i0 = int(t * sr); i1 = min(L, i0 + len(y)); B = bus(bn); B[i0:i1, 0] += y[:i1 - i0] * (1 - pan) * .7071; B[i0:i1, 1] += y[:i1 - i0] * (1 + pan) * .7071
def piano(m, t, dur, vel, pan=0., ring=1.2):
    x = smp('acoustic_grand_piano', m)
    if x is None: return
    n = min(len(x), int((dur + ring) * sr)); y = x[:n].copy(); r0 = int(min(dur, n / sr) * sr); r = n - r0
    if r > 0: y[r0:] *= np.linspace(1, 0, r) ** 1.5    # the damper falls slowly (pedal)
    y = lp(y, 2500 + 4000 * vel) * vel                   # softer = darker
    place('pno', y, t + rng.normal(0, .008), pan)
def held(bn, ins, m, t, dur, vel, pan=0., rel=1.2, att=.6):
    x = smp(ins, m)
    if x is None: return
    n = int((dur + rel) * sr); a, b, X = int(.7 * sr), int(min(2.5, len(x) / sr - .3) * sr), int(.35 * sr); y = x[:b].copy(); fi = np.sin(np.linspace(0, np.pi / 2, X)) ** 2
    while len(y) < n:
        s0 = a + int(rng.random() * .2 * sr); seg = x[s0:b]; y[-X:] = y[-X:] * (1 - fi) + seg[:X] * fi; y = np.concatenate([y, seg[X:]])
    y = y[:n]; at = int(att * sr); y[:at] *= np.linspace(0, 1, at) ** 1.5; r0 = int(dur * sr); y[r0:] *= np.linspace(1, 0, n - r0) ** 2
    place(bn, y * vel, t, pan)
for i, (si, b, c, mel, (pm, pad, cel, smel, harp)) in enumerate(bars):
    t = starts[i]; q = q0 * fac[i]; bass, tones = D[c]; sw = .9 if si in (3, 4) else .75
    # left hand: a low root, then the broken chord in eighths, rising and falling
    piano(bass, t, 4 * q, .42 * sw, pan=-.25, ring=2)
    for e, m in enumerate(tones): piano(m, t + e * q / 2, q * 1.6, (.30 if e % 4 == 0 else .22) * sw * (1 + .1 * rng.random()), pan=-.2 + .05 * e, ring=1)
    # right hand: the melody, with a quiet octave below in the fuller sections
    for k, (m, b0, nb) in enumerate(mel):
        v = (.62 if b0 == 0 else .52) * (pm or 0) * (1 + .08 * rng.random())
        if v: piano(m, t + b0 * q, nb * q, v, pan=.15, ring=1.6)
        if v and si in (3, 4): piano(m - 12, t + b0 * q + .01, nb * q, v * .45, pan=.1, ring=1.4)
        if smel: held('smel', 'string_ensemble_1', m, t + b0 * q, nb * q * 1.02, .42 * smel, pan=.05, rel=.9, att=.12); held('smel', 'cello', m - 24, t + b0 * q, nb * q * 1.02, .2 * smel, pan=-.2, rel=.9, att=.15)
    if pad:   # strings hold the chord's upper tones, swelling in
        for j, m in enumerate(sorted(set(tones[2:5]))): held('str', 'string_ensemble_1', m + 12, t, 4 * q * 1.02, .2 * pad, pan=(j - 1) * .5, rel=1.4, att=1.4)
    if cel: held('low', 'cello', bass + 12, t, 4 * q * 1.02, .34 * cel, pan=-.3, rel=1.2, att=.8); held('low', 'contrabass', bass + 12 if bass < 36 else bass, t, 4 * q * 1.02, .22 * cel, pan=.25, rel=1.2, att=.8)
    if harp and b % 2 == 0:   # a harp sweep up the chord, every other bar
        for e, m in enumerate(tones[:5] + [x + 12 for x in tones[1:5]]): held('hrp', 'orchestral_harp', m + 12, t + e * .07, 1.4, .26 * harp * (.7 + .3 * e / 8), pan=.35, rel=1.5, att=.005)
# ---- the hall, the balance, the loop ----
def hall(sec, damp, pre):
    n = int(sec * sr); it = np.arange(n) / sr; irs = []
    for ch in range(2):
        nz = rng.standard_normal(n).astype(np.float32) * np.exp(-it / (sec / 6.9)); nz = lp(nz, damp); p = int(pre * sr); nz = np.concatenate([np.zeros(p, np.float32), nz])[:n]; irs.append(nz / np.sqrt((nz ** 2).sum()))
    return irs
IR = hall(4.2, 4200, .03)
G = {'pno': (1.0, .45), 'str': (.75, .8), 'low': (.7, .5), 'smel': (.7, .7), 'hrp': (.7, .8)}
dry = np.zeros((L, 2), np.float32); send = np.zeros((L, 2), np.float32)
for n, B in mix.items(): d, s = G[n]; dry += B * d; send += B * s
wet = np.stack([sg.fftconvolve(send[:, c], IR[c])[:L] for c in range(2)], 1).astype(np.float32)
out = dry + wet * .5; out = out / np.max(np.abs(out)) * .97
LOOP = int(LOOP_T * sr); y = out[:LOOP + int(5 * sr)].copy(); X = int(5 * sr); fade = np.linspace(0, 1, X)[:, None]
y[:X] = y[:X] * fade + y[LOOP:LOOP + X] * (1 - fade); y = y[:LOOP]   # the coda's tail rings into the intro
w.write('ruin_raw.wav', sr, (y * 32767).astype(np.int16)); print('len', round(len(y) / sr, 1), 's, bars', len(bars))
