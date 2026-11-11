# v438 Convergence theme, choral and orchestral (owner: "remaster a new one to sound like Omnis Lacrima"): an original piece in that
# vein (a sorrowful choir over strings, low brass, timpani and a dark piano ostinato), not a copy of it. It is built on our own
# 4-note motif (C#, A, E, B over F#m - D - A - E, the game song's piano intro) and an original 8-bar melody grown from it, with real
# recorded instrument samples (MusyngKite / FluidR3 General MIDI sets, gleitz/midi-js-soundfonts) instead of synthesis.
# Input: samples.npz (instrument__note -> 16-bit mono 44.1 kHz, ~3.1 s each, made from the soundfont JS files). Output: orch_raw.wav.
# Master: ffmpeg -i orch_raw.wav -af "acompressor=threshold=-18dB:ratio=2:attack=30:release=300:makeup=1.5,loudnorm=I=-14:TP=-1.5:LRA=11" -c:a libmp3lame -b:a 128k music_conv.mp3
import numpy as np, scipy.signal as sg, scipy.io.wavfile as w
sr = 44100; S = np.load('samples.npz'); rng = np.random.default_rng(5)
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def smp(ins, m, setn='MusyngKite'):
    k = f"{setn}__{ins}__{NN[m % 12]}{m // 12 - 1}"; return S[k].astype(np.float32) / 32768 if k in S else None
BAR = 8.75 / 4; NC = 12; T0 = 1.0; L = int((T0 + NC * 4 * BAR + 9) * sr)
mix = {}
def bus(n): return mix.setdefault(n, np.zeros((L, 2), np.float32))
def lp(y, fc, o=2): b, a = sg.butter(o, min(.99, fc / (sr / 2))); return sg.lfilter(b, a, y, axis=0).astype(np.float32)
def sustain(x, dur, rel):
    """a sample held for dur seconds: its own attack, then its steady middle looped with crossfades, then a release fade"""
    n = int((dur + rel) * sr)
    if n <= len(x) - int(.05 * sr): y = x[:n].copy()
    else:
        a, b, X = int(.7 * sr), int(min(2.5, len(x) / sr - .3) * sr), int(.35 * sr); y = x[:b].copy(); fi = np.sin(np.linspace(0, np.pi / 2, X)) ** 2
        while len(y) < n:
            s0 = a + int(rng.random() * .2 * sr); seg = x[s0:b]; y[-X:] = y[-X:] * (1 - fi) + seg[:X] * fi; y = np.concatenate([y, seg[X:]])
        y = y[:n]
    r0 = int(dur * sr); r = len(y) - r0
    if r > 0: y[r0:] *= np.linspace(1, 0, r) ** 2
    return y
def note(b, ins, m, t, dur, vel, pan=0., rel=.6, setn='MusyngKite', det=0.):
    x = smp(ins, m, setn)
    if x is None: return
    if det: x = sg.resample(x, int(len(x) / (2 ** (det / 1200)))).astype(np.float32)
    y = sustain(x, dur, rel) * vel; i0 = int(t * sr); i1 = min(L, i0 + len(y)); B = bus(b)
    B[i0:i1, 0] += y[:i1 - i0] * (1 - pan) * .7071 * 1.0; B[i0:i1, 1] += y[:i1 - i0] * (1 + pan) * .7071
# ---- the score ----
CH = [(42, [54, 57, 61, 66]), (38, [50, 57, 62, 66]), (45, [52, 57, 61, 64]), (40, [52, 56, 59, 64])]   # F#m, D, A, E: bass + upper voices
MOT = [73, 69, 76, 71]                                                   # the motif: C#5, A4, E5, B4
# an original 8-bar melody grown from the motif, in beats (3/4): (midi, start beat in bar, beats)
MEL = [[(73, 0, 3)], [(69, 0, 2), (71, 2, 1)], [(76, 0, 2), (74, 2, 1)], [(73, 0, 1), (71, 1, 2)],
       [(73, 0, 2), (74, 2, 1)], [(76, 0, 2), (78, 2, 1)], [(76, 0, 1), (73, 1, 2)], [(71, 0, 3)]]
OST = {42: [42, 49, 57, 61, 57, 49], 38: [38, 45, 54, 57, 54, 45], 45: [45, 52, 61, 64, 61, 52], 40: [40, 47, 56, 59, 56, 47]}  # piano: root, fifth, tenth, up and back
# per cycle: piano, motif (piano), oohs, aahs (chords), strings, cello+bass, horns, timpani, melody (choir)
ARC = [(1, 1, 0, 0, 0, .3, 0, 0, 0), (1, 1, 0, 0, .25, .5, 0, 0, 0), (.9, 0, .6, 0, .4, .6, 0, .2, 0), (.9, 0, .7, .3, .55, .7, 0, .35, 0),
       (.8, 0, .5, .6, .75, .85, .4, .55, 0), (.8, 0, .4, .8, .9, 1, .6, .75, 0), (.75, 0, .3, 1, 1, 1, 1, 1, 1), (.75, 0, .3, 1, 1, 1, 1, 1, 1),
       (.85, 0, .6, .6, .7, .8, .4, .5, 0), (.9, 0, .5, .3, .45, .6, 0, .25, 0), (1, .9, .25, 0, .2, .4, 0, 0, 0), (1, .9, 0, 0, 0, .25, 0, 0, 0)]
q = BAR / 3                                                              # a beat
for c in range(NC):
    A = ARC[c]
    for k in range(4):
        t = T0 + (c * 4 + k) * BAR; root, up = CH[k]; bar = c * 4 + k
        if A[0]:   # the piano ostinato, quietly insistent
            for e, m in enumerate(OST[root]): note('pno', 'acoustic_grand_piano', m, t + e * q / 2, q * .9, .32 * A[0] * (1.1 if e == 0 else .85), pan=-.15 + .06 * (e % 3), rel=.5)
        if A[1]: note('pno', 'acoustic_grand_piano', MOT[k], t, BAR * .95, .55 * A[1], pan=.1, rel=1.2); note('pno', 'acoustic_grand_piano', MOT[k] - 12, t + .02, BAR * .95, .3 * A[1], pan=.05, rel=1.2)
        if A[2]:   # oohs carry the motif
            for d, p in [(0, -.3), (-12, .3)]: note('ooh', 'voice_oohs', MOT[k] + d, t, BAR * 1.02, .5 * A[2], pan=p, rel=.9, det=4 * (d != 0))
        if A[3]:   # the full choir on the chords
            for i, m in enumerate(up): note('aah', 'choir_aahs', m + 12 * (i >= 2 and c in (6, 7)), t, BAR * 1.02, .34 * A[3], pan=(i - 1.5) * .35, rel=1.0)
        if A[4]:   # strings: tremolo on the chord, sustained ensemble beneath
            for i, m in enumerate(up): note('str', 'tremolo_strings', m, t, BAR * 1.02, .26 * A[4], pan=(i - 1.5) * .45, rel=.7); note('str', 'string_ensemble_1', m - 12, t, BAR * 1.02, .2 * A[4], pan=(1.5 - i) * .3, rel=.9)
        if A[5]: note('low', 'cello', root + 12, t, BAR * 1.02, .45 * A[5], pan=-.25, rel=.8); note('low', 'contrabass', root, t, BAR * 1.02, .5 * A[5], pan=.2, rel=.8)
        if A[6]:   # horns double the melody (or the motif) an octave down
            src = MEL[bar % 8] if A[8] else [(MOT[k], 0, 3)]
            for m, b0, nb in src: note('hrn', 'french_horn', m - 12, t + b0 * q, nb * q * 1.02, .5 * A[6], pan=-.1, rel=.7); note('hrn', 'french_horn', m - 24, t + b0 * q, nb * q * 1.02, .32 * A[6], pan=.15, rel=.7)
        if A[7]:   # timpani: a stroke on each bar, a roll into every phrase
            note('tim', 'timpani', root + (12 if root < 40 else 0), t, q * 1.5, .7 * A[7], rel=1.4)
            if k == 3:
                for r in range(12): note('tim', 'timpani', 42, t + 2 * q + r * q / 12, q / 10, (.15 + .5 * r / 11) * A[7], rel=.4)
        if A[8]:   # the melody, full choir in octaves
            for m, b0, nb in MEL[bar % 8]:
                for d, g, p in [(0, .62, 0), (-12, .45, -.25), (12, .18, .25)]: note('mel', 'choir_aahs', m + d, t + b0 * q, nb * q * 1.03, g * A[8], pan=p, rel=1.1, det=3 * (d != 0))
# ---- the hall, the balance, the loop ----
def hall(sec, damp, pre):
    n = int(sec * sr); it = np.arange(n) / sr; irs = []
    for ch in range(2):
        nz = rng.standard_normal(n).astype(np.float32) * np.exp(-it / (sec / 6.9)); nz = lp(nz, damp); p = int(pre * sr); nz = np.concatenate([np.zeros(p, np.float32), nz])[:n]; irs.append(nz / np.sqrt((nz ** 2).sum()))
    return irs
IR = hall(5.5, 3600, .035)
G = {'pno': (.9, .5), 'ooh': (1.1, 1.0), 'aah': (.8, 1.0), 'str': (.62, .6), 'low': (.62, .45), 'hrn': (.8, .7), 'tim': (1.0, .6), 'mel': (2.2, 1.6)}  # the melody sits on top
dry = np.zeros((L, 2), np.float32); send = np.zeros((L, 2), np.float32)
for n, B in mix.items(): d, s = G[n]; dry += B * d; send += B * s
wet = np.stack([sg.fftconvolve(send[:, c], IR[c])[:L] for c in range(2)], 1).astype(np.float32)
out = dry + wet * .55; out = out / np.max(np.abs(out)) * .97
LOOP = int((T0 + NC * 4 * BAR) * sr); y = out[:LOOP + int(4 * sr)]
X = int(4 * sr); fade = np.linspace(0, 1, X)[:, None]; y[:X] = y[:X] * fade + y[LOOP:LOOP + X] * (1 - fade); y = y[:LOOP]
w.write('orch_raw.wav', sr, (y * 32767).astype(np.int16)); print('len', round(len(y) / sr, 1), 's; buses', sorted(mix))
