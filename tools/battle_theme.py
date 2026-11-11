# v457 boss battle theme (owner: "a theme song for all of these boss battles" in the spirit of a classic JRPG boss battle track). An
# original piece, not a copy of any existing song: our own riff, chord plan and melody. Driving rock rhythm section at 172 bpm (synthesized
# kit, picked bass, palm-muted distorted guitar), organ stabs, urgent strings, brass melody, taiko and orchestra hits, a dark choir in the
# bridge. Recorded instrument samples from gleitz/midi-js-soundfonts (MusyngKite) like tools/orch_theme.py.
# Input: battle.npz (new instruments) and samples.npz (orchestra), both  set__instrument__note -> 16-bit mono 44.1 kHz.
# Output: battle_raw.wav. Master: ffmpeg -i battle_raw.wav -af "acompressor=threshold=-16dB:ratio=2.5:attack=15:release=200:makeup=1.6,
#   loudnorm=I=-14:TP=-1.5:LRA=9" -ar 44100 -c:a libmp3lame -b:a 128k music_boss.mp3
import numpy as np, scipy.signal as sg, scipy.io.wavfile as w, sys
sr = 44100; rng = np.random.default_rng(11)
SM = {}
for f in sys.argv[1:] or ['battle.npz', 'samples.npz']:
    z = np.load(f); SM.update({k: z[k] for k in z.files})
NN = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def smp(ins, m, setn='MusyngKite'):
    k = f"{setn}__{ins}__{NN[m % 12]}{m // 12 - 1}"; return SM[k].astype(np.float32) / 32768 if k in SM else None
BPM = 172; q = 60 / BPM; BAR = 4 * q; T0 = .5
# the form, in bars: intro 4, A (riff) 8, B (brass melody) 8, A2 (riff) 4, C (bridge, choir) 8, D (lead + strings) 8, turnaround 4
FORM = [('I', 4), ('A', 8), ('B', 8), ('A2', 4), ('C', 8), ('D', 8), ('T', 4)]
NB = sum(n for _, n in FORM); LOOP = T0 + NB * BAR; L = int((LOOP + 6) * sr)
mix = {}
def bus(n): return mix.setdefault(n, np.zeros((L, 2), np.float32))
def lp(y, fc, o=2): b, a = sg.butter(o, min(.99, fc / (sr / 2))); return sg.lfilter(b, a, y, axis=0).astype(np.float32)
def hp(y, fc, o=2): b, a = sg.butter(o, fc / (sr / 2), 'high'); return sg.lfilter(b, a, y, axis=0).astype(np.float32)
def put(b, y, t, pan=0.):
    i0 = int(t * sr); i1 = min(L, i0 + len(y)); B = bus(b)
    if i1 <= i0: return
    B[i0:i1, 0] += y[:i1 - i0] * (1 - pan) * .7071; B[i0:i1, 1] += y[:i1 - i0] * (1 + pan) * .7071
def sustain(x, dur, rel):
    n = int((dur + rel) * sr)
    if n <= len(x) - int(.05 * sr): y = x[:n].copy()
    else:
        a, b, X = int(.5 * sr), int(min(2.5, len(x) / sr - .3) * sr), int(.3 * sr); y = x[:b].copy(); fi = np.sin(np.linspace(0, np.pi / 2, X)) ** 2
        while len(y) < n:
            s0 = a + int(rng.random() * .2 * sr); seg = x[s0:b]; y[-X:] = y[-X:] * (1 - fi) + seg[:X] * fi; y = np.concatenate([y, seg[X:]])
        y = y[:n]
    r0 = int(dur * sr); r = len(y) - r0
    if r > 0: y[r0:] *= np.linspace(1, 0, r) ** 2
    return y
def note(b, ins, m, t, dur, vel, pan=0., rel=.15, det=0.):
    x = smp(ins, m)
    if x is None: return
    if det: x = sg.resample(x, int(len(x) / (2 ** (det / 1200)))).astype(np.float32)
    put(b, sustain(x, dur, rel) * vel, t, pan)
# ---- the kit, synthesized ----
def env(n, d): return np.exp(-np.arange(n) / sr / d).astype(np.float32)
def kick(t, v=1.):
    n = int(.42 * sr); tt = np.arange(n) / sr; f = 46 + 110 * np.exp(-tt / .035); ph = 2 * np.pi * np.cumsum(f) / sr
    y = np.sin(ph) * env(n, .16) + .5 * rng.standard_normal(n).astype(np.float32) * env(n, .004); put('kik', np.tanh(1.6 * y) * v * .9, t)
def snare(t, v=1.):
    n = int(.32 * sr); tt = np.arange(n) / sr; nz = hp(lp(rng.standard_normal(n).astype(np.float32), 7500), 900) * env(n, .085)
    tone = np.sin(2 * np.pi * (185 + 40 * np.exp(-tt / .02)) * tt) * env(n, .05); put('snr', (nz * 1.1 + tone * .7) * v * .8, t)
def hat(t, v=1., op=False):
    n = int((.32 if op else .07) * sr); y = hp(rng.standard_normal(n).astype(np.float32), 7000, 3) * env(n, .11 if op else .018); put('hat', y * v * .32, t, .25)
def crash(t, v=1.):
    n = int(2.6 * sr); y = hp(rng.standard_normal((n, 2)).astype(np.float32), 4200, 2) * env(n, .75)[:, None]; i0 = int(t * sr); i1 = min(L, i0 + n); bus('cym')[i0:i1] += y[:i1 - i0] * v * .3
def tom(t, f, v=1.):
    n = int(.5 * sr); tt = np.arange(n) / sr; ff = f * (1 + .6 * np.exp(-tt / .04)); y = np.sin(2 * np.pi * np.cumsum(ff) / sr) * env(n, .2); put('tom', np.tanh(1.4 * y) * v * .7, t, (f - 120) / 200)
# ---- the score (E minor, our own riff and melody) ----
E2, A2, B1, C2, D2, G2 = 40, 45, 35, 36, 38, 43
# the riff: palm-muted pedal on the root with accents climbing out of it (8ths); 'x' accent = open power chord
RIFF = [(0, 'x'), (0, 'm'), (0, 'm'), (3, 'x'), (0, 'm'), (5, 'x'), (0, 'm'), (6, 'x')]            # E . . G . A . Bb
RIFF2 = [(0, 'x'), (0, 'm'), (0, 'm'), (3, 'x'), (0, 'm'), (5, 'x'), (7, 'x'), (5, 'x')]           # E . . G . A B A
A_ROOTS = [E2, E2, C2 + 12, D2 + 12, E2, E2, C2 + 12, B1 + 12]                                       # Em Em C D | Em Em C B
B_CH = [(E2, 'm'), (C2 + 12, 'M'), (A2, 'm'), (B1 + 12, '7'), (E2, 'm'), (C2 + 12, 'M'), (D2 + 12, 'M'), (B1 + 12, '7')]
C_CH = [(C2 + 12, 'M7'), (D2 + 12, 'M'), (B1 + 12, 'm'), (E2, 'm'), (A2, 'm'), (B1 + 12, 'M'), (C2 + 12, 'M'), (B1 + 12, 's')]
IV = {'m': [0, 7, 12, 15, 19], 'M': [0, 7, 12, 16, 19], '7': [0, 7, 10, 16, 19], 'M7': [0, 7, 11, 16, 19], 's': [0, 7, 12, 17, 19]}
# brass melody over B (and the lead over D): (midi, start beat, beats)
MEL = [[(71, 0, 1.5), (76, 1.5, .5), (78, 2, 1), (79, 3, 1)], [(79, 0, 1.5), (78, 1.5, .5), (76, 2, 1), (72, 3, 1)],
       [(69, 0, 1), (72, 1, 1), (76, 2, 1.5), (74, 3.5, .5)], [(75, 0, 3), (71, 3, 1)],
       [(76, 0, 1.5), (79, 1.5, .5), (83, 2, 2)], [(81, 0, 1), (79, 1, 1), (76, 2, 1), (79, 3, 1)],
       [(78, 0, 1.5), (81, 1.5, .5), (74, 2, 2)], [(75, 0, 2), (78, 2, 1), (83, 3, 1)]]
CMEL = [[(76, 0, 4)], [(78, 0, 2), (81, 2, 2)], [(78, 0, 4)], [(79, 0, 2), (76, 2, 2)], [(76, 0, 3), (72, 3, 1)], [(75, 0, 2), (78, 2, 2)], [(79, 0, 3), (81, 3, 1)], [(83, 0, 4)]]
def guitar(t, root, iv, kind, v=1.):
    if kind == 'm':   # palm mute: a short, dark chug
        for i, d in enumerate([0, 7]): note('gtm', 'distortion_guitar', root + d, t, q * .32, .5 * v, pan=-.45 + .9 * i, rel=.03)
    else:
        for i, d in enumerate([0, 7, 12]): note('gto', 'distortion_guitar', root + iv + d, t, q * .46, .42 * v, pan=-.5 + .5 * i, rel=.05); note('gto', 'overdriven_guitar', root + iv + d, t + .006, q * .46, .2 * v, pan=.5 - .5 * i, rel=.05)
def bass8(t, root, nb=8, v=1., pat=None):
    for e in range(nb): d = (pat[e][0] if pat else 0); note('bas', 'electric_bass_pick', root - 12 + d, t + e * q / 2, q * .45, .6 * v * (1.15 if e % 2 == 0 else .9), rel=.04)
def beat(t, kind, v=1., bar=0):
    if kind == 'rock':        # kick 1, 2&, 3, 3&; snare 2, 4; 8th hats
        for b in [0, 1.5, 2, 2.5]: kick(t + b * q, v)
        for b in [1, 3]: snare(t + b * q, v)
        for e in range(8): hat(t + e * q / 2, v * (1 if e % 2 == 0 else .6), op=(e == 7 and bar % 2 == 1))
    elif kind == 'drive':     # straight 8th kicks, snare 2 and 4, ride-ish hats on quarters
        for e in range(8): kick(t + e * q / 2, v * (1 if e % 2 == 0 else .75))
        for b in [1, 3]: snare(t + b * q, v * 1.05)
        for b in range(4): hat(t + b * q, v * .9, op=True)
    elif kind == 'half':      # half time: kick 1, snare 3, toms
        kick(t, v); kick(t + 2.5 * q, v * .8); snare(t + 2 * q, v * 1.1)
        for e in range(4): hat(t + e * q, v * .7)
def fill(t, v=1.):            # a 16th tom fill over the bar's last two beats
    for i in range(8): tom(t + 2 * q + i * q / 4, [210, 210, 165, 165, 130, 130, 95, 95][i], v * (.7 + .04 * i))
    snare(t + 3.75 * q, v)
def stab(t, root, iv, v=1., hit=True):   # organ + brass section + an orchestra hit on top
    for i, d in enumerate(iv[:4]): note('org', 'rock_organ', root + 24 + d, t, q * .5, .22 * v, pan=(i - 1.5) * .3, rel=.08); note('brs', 'brass_section', root + 24 + d, t, q * .55, .3 * v, pan=(1.5 - i) * .25, rel=.12)
    if hit: note('hit', 'orchestra_hit', root + 36, t, q * .9, .55 * v, rel=.3)
bar = 0
for sec, n in FORM:
    for k in range(n):
        t = T0 + bar * BAR; last = k == n - 1
        if sec == 'I':   # taiko and timpani roll under rising tremolo strings, hits on each bar
            for e in range(4): note('tai', 'taiko_drum', 45, t + e * q, q, .8 if e == 0 else .45, rel=.4)
            for r in range(16 * (k == 3)): note('tim', 'timpani', 40, t + r * q / 4, q / 4, .15 + .45 * r / 15, rel=.2)
            for i, m in enumerate([52, 59, 64, 67]): note('str', 'tremolo_strings', m + k, t, BAR, .16 + .05 * k, pan=(i - 1.5) * .4, rel=.1)
            if k < 3: stab(t, E2, IV['m'], .8 + .1 * k)
            else:
                for b in [0, 1.5, 3]: stab(t + b * q, E2 - 1 if b == 3 else E2, IV['M'] if b == 3 else IV['m'], 1.0)
            note('low', 'contrabass', E2 - 12 + 12, t, BAR, .5, rel=.2)
            if k == 3: fill(t, .9)
        elif sec in ('A', 'A2'):
            root = A_ROOTS[k % 8]; R = RIFF2 if k % 2 == 1 else RIFF
            if k == 0: crash(t)
            for e, (d, kind) in enumerate(R if root == E2 else [(0, 'x'), (0, 'm'), (0, 'm'), (0, 'x'), (0, 'm'), (0, 'x'), (0, 'm'), (0, 'x')]):
                guitar(t + e * q / 2, root, d, kind)
            bass8(t, root, pat=R if root == E2 else None)
            for b in [1.5, 3.5]: note('org', 'rock_organ', root + 24 + 7, t + b * q, q * .4, .2, pan=.3, rel=.06); note('org', 'rock_organ', root + 24 + (15 if root == E2 else 16), t + b * q, q * .4, .16, pan=-.3, rel=.06)
            for i, m in enumerate([0, 7, 12]): note('str', 'string_ensemble_1', root + 24 + m, t, BAR * 1.02, .14, pan=(i - 1) * .5, rel=.2)
            if sec == 'A' and k >= 4: note('brs', 'brass_section', root + 36, t, q * 3.5, .22, rel=.2)
            beat(t, 'rock', 1, k)
            if last: fill(t, .9 if sec == 'A' else 1)
        elif sec in ('B', 'D'):
            root, ch = (B_CH if sec == 'B' else B_CH)[k]; iv = IV[ch]
            if k in (0, 4): crash(t)
            for e in range(8): guitar(t + e * q / 2, root, 0, 'x' if e in (0, 3, 6) else 'm', .9)
            bass8(t, root)
            for e in range(8):   # strings: an urgent 8th ostinato on the chord
                m = root + 36 + iv[[0, 2, 3, 2, 1, 2, 3, 4][e]] - 12; note('str', 'string_ensemble_1', m, t + e * q / 2, q * .42, .2, pan=.35, rel=.06)
            for m, b0, nb in MEL[k]:
                if sec == 'B':
                    note('mel', 'trumpet', m, t + b0 * q, nb * q, .5, pan=-.05, rel=.15); note('mel', 'trombone', m - 12, t + b0 * q, nb * q, .42, pan=.15, rel=.15); note('mel', 'french_horn', m - 12, t + b0 * q, nb * q, .3, pan=-.2, rel=.2)
                else:
                    note('lead', 'overdriven_guitar', m, t + b0 * q, nb * q, .42, pan=0, rel=.15, det=-6); note('lead', 'distortion_guitar', m, t + b0 * q, nb * q, .3, pan=.1, rel=.12, det=6)
                    note('mel', 'brass_section', m - 12, t + b0 * q, nb * q, .28, pan=-.15, rel=.2)
            if sec == 'D':
                for i, d in enumerate(iv[1:4]): note('aah', 'choir_aahs', root + 24 + d, t, BAR * 1.02, .2, pan=(i - 1) * .5, rel=.3)
                note('tim', 'timpani', root + (12 if root < 40 else 0), t, q, .55, rel=.4)
            beat(t, 'drive' if sec == 'D' else 'rock', 1, k)
            if k == 3: fill(t, .8)
            if last and sec == 'B': fill(t, 1)
        elif sec == 'C':   # the bridge: half time, dark choir, low brass and taiko; the riff falls silent and the strings tremble
            root, ch = C_CH[k]; iv = IV[ch]
            if k in (0, 4): crash(t, .8)
            for i, d in enumerate(iv[1:]): note('aah', 'choir_aahs', root + 24 + d, t, BAR * 1.02, .3, pan=(i - 1.5) * .4, rel=.4); note('aah', 'synth_choir', root + 12 + d, t, BAR * 1.02, .14, pan=(1.5 - i) * .4, rel=.4)
            for i, d in enumerate(iv[1:4]): note('str', 'tremolo_strings', root + 36 + d - 12, t, BAR * 1.02, .2, pan=(i - 1) * .5, rel=.2)
            for m, b0, nb in CMEL[k]: note('mel', 'french_horn', m - 12, t + b0 * q, nb * q, .5, pan=-.1, rel=.3); note('mel', 'trombone', m - 24, t + b0 * q, nb * q, .3, pan=.2, rel=.3)
            note('bas', 'electric_bass_pick', root - 12, t, q * 1.8, .7, rel=.2); note('bas', 'electric_bass_pick', root - 12, t + 2.5 * q, q * 1.3, .6, rel=.2)
            note('low', 'contrabass', root, t, BAR, .45, rel=.3)
            guitar(t, root, 0, 'x', .7 if k < 4 else .9)
            for e in range(4): note('tai', 'taiko_drum', 45 if e % 2 == 0 else 50, t + e * q, q, .55 + .1 * (e == 0), rel=.4)
            beat(t, 'half', .9 + .1 * (k >= 4), k)
            if k >= 6:   # build: 8th snares rising into the lead section
                for e in range(8): snare(t + e * q / 2, .25 + .5 * ((k - 6) * 8 + e) / 15)
            if last:
                for r in range(16): note('tim', 'timpani', 40, t + r * q / 4, q / 4, .2 + .5 * r / 15, rel=.2)
        elif sec == 'T':   # the turnaround: unison stabs on a rising line, then the riff kicks back in
            roots = [(C2 + 12, 'M'), (D2 + 12, 'M'), (B1 + 12, '7'), (B1 + 12, '7')][k]; root, ch = roots; iv = IV[ch]
            if k == 0: crash(t)
            hits = [0, 1.5, 3] if k < 3 else [0, .5, 1, 1.5]
            for b in hits: stab(t + b * q, root, iv, 1.0); guitar(t + b * q, root, 0, 'x', 1); note('bas', 'electric_bass_pick', root - 12, t + b * q, q * .5, .8, rel=.05); kick(t + b * q); crash(t + b * q, .35) if k == 3 else None
            for b in [1, 3]: snare(t + b * q) if k < 3 else None
            if k < 3:
                for e in range(8): hat(t + e * q / 2, .7)
            note('str', 'tremolo_strings', root + 36 + iv[1], t, BAR, .25, rel=.1); note('str', 'tremolo_strings', root + 36 + iv[3] - 12, t, BAR, .22, rel=.1)
            if k == 3: fill(t, 1.1)
        bar += 1
# ---- the room, the balance, the loop ----
def room(sec, damp, pre):
    n = int(sec * sr); it = np.arange(n) / sr; irs = []
    for ch in range(2):
        nz = rng.standard_normal(n).astype(np.float32) * np.exp(-it / (sec / 6.9)); nz = lp(nz, damp); p = int(pre * sr); nz = np.concatenate([np.zeros(p, np.float32), nz])[:n]; irs.append(nz / np.sqrt((nz ** 2).sum()))
    return irs
IR = room(2.2, 5000, .02)
# bus balance (dry, reverb send): the soundfont samples sit about 25 dB under the synthesized kit, so most buses are lifted a lot
G = {'kik': (.35, .02), 'snr': (.76, .3), 'hat': (.56, .08), 'cym': (.4, .12), 'tom': (.63, .2), 'gtm': (6.0, .5), 'gto': (5.0, 1.0), 'bas': (5.0, .0),
     'org': (11, 3.5), 'brs': (6.4, 3.2), 'hit': (14, 8), 'str': (7.5, 5.0), 'mel': (10, 4.5), 'lead': (9.2, 3.6), 'aah': (4.2, 4.4), 'tai': (2.2, 1.2),
     'tim': (4.5, 2.8), 'low': (2.1, 1.0)}
if 'gtm' in mix: mix['gtm'] = lp(mix['gtm'], 2400)
if 'bas' in mix: mix['bas'] = lp(mix['bas'], 3200)
dry = np.zeros((L, 2), np.float32); send = np.zeros((L, 2), np.float32)
for nm, B in mix.items(): d, s = G[nm]; dry += B * d; send += B * s
wet = np.stack([sg.fftconvolve(send[:, c], IR[c])[:L] for c in range(2)], 1).astype(np.float32)
out = dry + wet * .5; out = np.tanh(out / np.max(np.abs(out)) * 1.4) / np.tanh(1.4) * .97
LP = int(LOOP * sr); y = out[:LP + int(2 * sr)].copy()
X = int(1.5 * sr); y[:X] += y[LP:LP + X] * np.linspace(1, 0, X)[:, None] ** 2; y = y[:LP]   # the turnaround's tail rings into the top
w.write('battle_raw.wav', sr, (np.clip(y, -1, 1) * 32767).astype(np.int16)); print('len', round(len(y) / sr, 1), 's; buses', sorted(mix))
