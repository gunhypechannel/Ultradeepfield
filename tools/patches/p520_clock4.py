# v520 the event clock only for the six Wednesday great events (owner), each in its own colour: Cube Devastation (green), Vaelthar's
# Cosmic Anomaly (lavender), Aexion's Aeon (blue), Khezaroth (amber), Medusara (red) and the Pentarch Convergence. Not the Saturday
# world bosses. The Convergence clock is special: its runes and
# the letters of its title glow in the five Elementals' colours (one tinted copy of the glyph atlas per Elemental).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
i = s.index('function evCdNext(T) {'); j = s.index('function dvCountdown(W, t, T, live)')
s = s[:i] + '''function evCdNext(T) { let best = null; const M = { dv: ["Cube Devastation", "#5dff6a"], vae: ["Vaelthar · Cosmic Anomaly", (SBX.vae || {}).col || "#c890ff"], aex: ["Aexion · The Aeon", (SBX.aex || {}).col || "#7ac8ff"], khz: ["Khezaroth · The Sphinx", "#ffb340"], med: ["Medusara · Petrified Star", (SBX.med || {}).col || "#ff5a4a"], conv: ["Pentarch Convergence", "#ffffff"] };
  for (const k in M) { const s0 = rotNextOf(k, T); if (s0 > T && s0 - T <= 7 * 864e5 && (!best || s0 < best.s0)) best = { k, s0, n: M[k][0], col: M[k][1], multi: k === "conv" ? WB_EL.map(e => WB[e].col) : null }; } return best; }
const evCdLive = T => { try { return wbGroupOn(3, T); } catch (e) { return false; } };
''' + s[j:]
rep('  C.at = at; C.GS = GS; C.kinds = kinds; C.ang = [0, 0, 0, 0];', '''  C.at = at; C.GS = GS; C.kinds = kinds; C.ang = [0, 0, 0, 0];
  if (N.multi) C.atC = N.multi.map(col => { const c2 = document.createElement("canvas"); c2.width = at.width; c2.height = at.height; const q = c2.getContext("2d"); q.drawImage(at, 0, 0); q.globalCompositeOperation = "multiply"; q.fillStyle = col; q.fillRect(0, 0, c2.width, c2.height); q.globalCompositeOperation = "destination-in"; q.drawImage(at, 0, 0); return c2; }); /* v520 the Convergence: runes in the five Elementals' colours */''')
rep('for (const ch of txt) { p.save();', 'let ci = 0; for (const ch of txt) { p.save(); if (N.multi && ch !== " ") p.fillStyle = p.shadowColor = N.multi[ci++ % N.multi.length];')
rep('g.drawImage(A, (Math.abs(k | 0) % C.kinds) * GS', 'g.drawImage(C.atC ? C.atC[Math.abs(k | 0) % C.atC.length] : A, (Math.abs(k | 0) % C.kinds) * GS')
s2 = re.sub(r"GAME_V = 519\b", "GAME_V = 520", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
