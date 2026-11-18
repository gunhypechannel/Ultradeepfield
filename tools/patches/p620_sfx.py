# v620: recorded battle sounds (owner flagged the laser bolts and both fanfares as "sounds funny" and nine more as "weak"; new takes made
# with ElevenLabs Sound Effects and picked by the owner on the A/B page). The files live in docs/sfx/ (mono mp3, levelled to the old
# sounds' loudness); sbPrep fetches and decodes them with the synthesised bank, and each sound plays its file when it is there (the old
# synthesis stays as the fallback while they load or if a fetch fails). Only the battle uses the new round and end stings: the gong and
# fanfare elsewhere (runes, rewards) are unchanged.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
FILES = json.load(open('tools/patches/p620_sfx.json'))  # {key: gain}
rep('  const step = () => { const j = jobs.shift(); if (!j) return; try { j(); } catch (e) {} setTimeout(step, 24); }; setTimeout(step, 30);\n}',
    '  const step = () => { const j = jobs.shift(); if (!j) return; try { j(); } catch (e) {} setTimeout(step, 24); }; setTimeout(step, 30);\n'
    '  SB.f = SB.f || {}; for (const k of Object.keys(SFX_F)) fetch(`sfx/${k}.mp3?v=620`).then(r => r.ok ? r.arrayBuffer() : null).then(ab => ab && new Promise((ok, no) => c.decodeAudioData(ab, ok, no))).then(b => { if (b) SB.f[k] = [b]; }).catch(() => {}); /* v620 the recorded sounds */\n}\n'
    'const SFX_F = ' + json.dumps(FILES) + '; /* v620 recorded battle sounds and their levels */\n'
    'const sfxF = k => SB.f && SB.f[k] && SFX_F[k] != null ? SB.f[k] : null;')
# the laser bolts
rep('lastZap = t; if (SFX.pb(enemy ? SB.heavy : SB.bolt, t, enemy ? .3 : .24,', 'lastZap = t; { const F = sfxF(enemy ? "laser_e" : "laser"); if (F && SFX.pb(F, t, SFX_F[enemy ? "laser_e" : "laser"], (Math.random() - .5) * .7, .95 + Math.random() * .1, .12)) return; } if (SFX.pb(enemy ? SB.heavy : SB.bolt, t, enemy ? .3 : .24,')
# missile swarm, beam charge, shield
rep('  swarm(n, pan) { if (!SFX.ok() || SFX.busy("swarm", .12)) return; const c = AU.ctx, t = c.currentTime, k = clamp(Math.round(n / 2), 2, 6);',
    '  swarm(n, pan) { if (!SFX.ok() || SFX.busy("swarm", .12)) return; const c = AU.ctx, t = c.currentTime, k = clamp(Math.round(n / 2), 2, 6); if (sfxF("swarm") && SFX.pb(sfxF("swarm"), t, SFX_F.swarm * (n > 6 ? 1.15 : 1), pan, .96 + Math.random() * .08, .25)) return;')
rep('  charge(pan) { if (!SFX.ok() || SFX.busy("charge", .3)) return; const c = AU.ctx, t = c.currentTime,', '  charge(pan) { if (!SFX.ok() || SFX.busy("charge", .3)) return; if (sfxF("charge") && SFX.pb(sfxF("charge"), AU.ctx.currentTime, SFX_F.charge, pan, 1, .3)) return; const c = AU.ctx, t = c.currentTime,')
rep('  shield(pan) { if (!SFX.ok() || SFX.busy("shield", .085)) return; const c = AU.ctx, t = c.currentTime,', '  shield(pan) { if (!SFX.ok() || SFX.busy("shield", .085)) return; if (sfxF("shield") && SFX.pb(sfxF("shield"), AU.ctx.currentTime, SFX_F.shield, pan, .94 + Math.random() * .12, .35)) return; const c = AU.ctx, t = c.currentTime,')
# explosions by size
rep('if (SFX.busy(key, big ? .25 : .06)) return; const c = AU.ctx, t = c.currentTime, dur = .55 + size * .45;',
    'if (SFX.busy(key, big ? .25 : .06)) return; const c = AU.ctx, t = c.currentTime, dur = .55 + size * .45;\n'
    '    { const fk = size < 1.2 ? "blast_s" : size < 2.5 ? "blast_m" : "blast_b", F = sfxF(fk); if (F && SFX.pb(F, t, SFX_F[fk] * clamp(.8 + size * .12, .8, 1.2), pan, (.95 + Math.random() * .1) * (size < .8 ? 1.06 : 1), .4, size < 1 ? 3200 : 0)) return; } /* v620 */')
rep('  boom(big) { if (!SFX.ok()) return; if (SB.boom', '  boom(big) { if (!SFX.ok()) return; { const F = sfxF(big ? "boom" : "blast_m"); if (F && SFX.pb(F, AU.ctx.currentTime, SFX_F[big ? "boom" : "blast_m"], 0, 1, .5)) return; } if (SB.boom')
# the battle's round sting and its end stings
rep('  gong() {', '  round() { if (!SFX.ok()) return; const F = sfxF("gong"); if (F && SFX.pb(F, AU.ctx.currentTime, SFX_F.gong, 0, 1, .35)) return; SFX.gong(); }, /* v620 a new battle round */\n'
    '  battleEnd(win) { if (!SFX.ok()) return; const k = win ? "win" : "loss", F = sfxF(k); if (F && SFX.pb(F, AU.ctx.currentTime, SFX_F[k], 0, 1, .2)) return; SFX.fanfare(win); }, /* v620 the battle\'s victory and defeat stings */\n  gong() {')
rep('if (rnd_ > 1) SFX.gong(); }', 'if (rnd_ > 1) SFX.round(); }')
rep('  SFX.fanfare(o === "win");\n}\nfunction endingFx(', '  SFX.battleEnd(o === "win");\n}\nfunction endingFx(')
rep('if (!b.ending) SFX.fanfare(win);', 'if (!b.ending) SFX.battleEnd(win);')
s2 = re.sub(r"GAME_V = 619\b", "GAME_V = 620", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
