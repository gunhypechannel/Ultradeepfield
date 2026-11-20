# v684: fallen super bosses stay down (Khezaroth and Medusara stood back up when their death pose ended, while the Advisor said only the
# glyph was left); a phone never renders the map below 1x (after crashes the lightest memory tier let it drop to 0.6x: blocky);
# The Shadow at the Wall: the Leviathan swims the wall laid out (as on the map since v617) instead of the old coil, without its debris
# (tinted black, they read as black squares), and the event band no longer repeats its name
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('b.drive("die", dd < 1 ? dd : -1)', 'b.drive("die", Math.min(1, dd)) /* v684 stays fallen */', 4)
rep('floor = WEAK || gfx("detail") === 0 ? .6 :', 'floor = WEAK || gfx("detail") === 0 ? (MOBILE ? Math.min(max, 1) /* v684 a phone never below 1x: 0.6x on a 3x screen is blocky, and 1x costs about 1 MB */ : .6) :')
rep('.omb.fin b{color:var(--fc)}', '.omb.fin b{color:var(--fc);white-space:nowrap}\n.omb.fin span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}')
rep('<span>${esc(D.st[F.si][2])}</span>${up ?', '<span>${esc(D.n.toLowerCase().includes(D.st[F.si][2].toLowerCase()) ? "Happening now" : D.st[F.si][2])}</span>${up ? /* v684 not "The Shadow at the Wall · The Shadow" */')
rep('o.material = Array.isArray(o.material) ? o.material.map(one) : one(o.material); });\n    X.back = finSpr(W, X, "255,110,30", 0xff6a2a);',
    'o.material = Array.isArray(o.material) ? o.material.map(one) : one(o.material); });\n    if (X.b) X.b.grp.traverse(o => { if (o.isInstancedMesh && o.geometry && /Dodecahedron/.test(o.geometry.type)) o.visible = false; }); /* v684 no debris on the shadow */\n    X.back = finSpr(W, X, "255,110,30", 0xff6a2a);')
rep('if (X.b) { X.b.grp.visible = sc > .03; X.b.grp.position.copy(X.pos); X.b.grp.scale.setScalar(Math.max(.01, sc)); X.b.grp.rotation.y = -a - Math.PI / 2; X.b.tick(t); if (t > X.nx) { X.b.act(Math.random() < .5 ? "coil" : "sweep"); X.nx = t + 7000 + Math.random() * 5000; } }',
    'if (X.b) { X.b.grp.visible = sc > .03; if (X.b.N) { const R0 = X.R + 60; X.b.ring = { R0, Rh: r, a, y: 30 - 300 * sink, yh: y, k: Math.max(.04, sc / 7), s: TAU * .465 * R0 / X.b.N * .57 }; X.b.grp.position.set(0, 0, 0); X.b.grp.rotation.set(0, 0, 0); X.b.grp.scale.setScalar(1); } else { X.b.grp.position.copy(X.pos); X.b.grp.scale.setScalar(Math.max(.01, sc)); X.b.grp.rotation.y = -a - Math.PI / 2; } /* v684 it swims the wall laid out, as on the map (v617), not coiled */ X.b.tick(t); if (t > X.nx) { X.b.act("sweep"); X.nx = t + 7000 + Math.random() * 5000; } }')
rep('const GAME_V = 683;', 'const GAME_V = 684;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
