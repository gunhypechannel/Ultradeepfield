# v678 cinematic replays (see p678_cine.js); the Mimic "ASSIMILATED" label is drawn directly (replays clear b.nums since v603)
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
rep('function spawnVolley(b, v) {', R('p678_cine.js') + 'function spawnVolley(b, v) {')
rep('intro: reduced ? 0 : bIntroMs(R.squads), intro0: reduced ? 0 : bIntroMs(R.squads),', 'intro: reduced ? 0 : cineIntro(bIntroMs(R.squads)), intro0: reduced ? 0 : cineIntro(bIntroMs(R.squads)), cine: !reduced && cineOn(), /* v678 */')
rep('b.simT = Math.min(b.end + (b.ending ? 0 : 1.5), b.simT + real / 1000 * b.speed * BATTLE_PACE * (t < b.slowUntil ? .3 : 1));', 'b.simT = Math.min(b.end + (b.ending ? 0 : 1.5), b.simT + real / 1000 * b.speed * BATTLE_PACE * (t < b.slowUntil ? .3 : 1) * (b.cine ? CINE_PACE : 1)); /* v678 */')
rep('if (b.intro <= 0) while (b.vi < b.R.vols.length && b.R.vols[b.vi].t <= T) spawnVolley(b, b.R.vols[b.vi++]);', 'if (b.intro <= 0) while (b.vi < b.R.vols.length && cineDue(b, b.R.vols[b.vi], T)) spawnVolley(b, b.R.vols[b.vi++]); /* v678 volleys on the beat */')
rep('if (vw.mode === "auto") { const fo = b.focus && t < b.focus.until ? b.focus : null;', 'if (vw.mode === "auto") { if (b.cine) try { cineDirect(b, t, T, W, H); } catch (e) {} /* v678 the director */ const fo = b.focus && t < b.focus.until ? b.focus : null;')
rep('const ke = reduced ? 1 : Math.min(1, real / (vw.mode === "auto" ? 520 : 70));', 'const ke = reduced ? 1 : Math.min(1, real / (vw.mode === "auto" ? (b.cine ? 950 : 520) : 70));')
rep('ctx.drawImage(b.fgL.grade, 0, 0, W, H); }', 'ctx.drawImage(b.fgL.grade, 0, 0, W, H); } if (b.cine) try { cineLook(ctx, b, W, H, top, bot, t, lo); } catch (e) {} /* v678 */')
rep('<button data-act="bcam" class=', '<button data-act="bcine" class="${b.cine ? "on" : ""}" aria-label="${b.cine ? "Cinematic replay: slower, directed. Tap for quick" : "Quick replay. Tap for cinematic"}">${b.cine ? "🎞" : "⚡"}</button><button data-act="bcam" class=')
rep('  bview: () => {', '  bcine: () => { const b = battle; if (!b) return; b.cine = !b.cine; try { localStorage.setItem("udf.cineRep", b.cine ? "1" : "0"); } catch (e) {} if (!b.cine && b.focus && b.focus.cine) b.focus = null; toast(b.cine ? "Cinematic replays: slower, with a director camera." : "Quick replays: full speed, fixed camera."); battleCtl(); }, /* v678 */\n  bview: () => {')
# the Mimic label (b.nums is cleared every frame in replays)
rep('(b.nums || (b.nums = [])).push({ x: E0.x, y: E0.y - 26 * d, t, txt: "ASSIMILATED", col: "#5fd8ff", big: 1 });', 'm.asT = t;')
rep('''    if (u > 1) continue;
    if (MIM_TENT[m.a] && alive)''', '''    if (m.asT && t - m.asT < 1500) { const k = (t - m.asT) / 1500; ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = Math.min(1, (1 - k) * 2); ctx.font = `italic 800 ${13 * d}px Oxanium, sans-serif`; ctx.textAlign = "center"; ctx.fillStyle = "#5fd8ff"; ctx.strokeStyle = "rgba(0,0,0,.8)"; ctx.lineWidth = 3 * d; ctx.strokeText("ASSIMILATED", E0.x, E0.y - (26 + 16 * k) * d); ctx.fillText("ASSIMILATED", E0.x, E0.y - (26 + 16 * k) * d); ctx.restore(); } /* v678 */
    if (u > 1) continue;
    if (MIM_TENT[m.a] && alive)''')
# owner: slow the Mimics' motion down, it reads more real: their loop plays at half speed (6 s a sway) in battle
rep('P[i] = ((P[i] == null ? (i * .37) % 1 : P[i]) + Math.min(80, real || 16) / 1000 / MBF_P * (moving ? 1.35 : 1)) % 1;', 'P[i] = ((P[i] == null ? (i * .37) % 1 : P[i]) + Math.min(80, real || 16) / 1000 / MBF_P * (moving ? 1.35 : 1) * (MIM_D[k] ? .5 : 1)) % 1; /* v678 the Mimics move slower and heavier */')
rep('const GAME_V = 677;', 'const GAME_V = 678;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
