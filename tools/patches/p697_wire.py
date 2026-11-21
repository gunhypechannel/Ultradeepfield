# v697: making sure an old copy can never overwrite the empire again (owner: "what else can we do to make sure it never happen again?").
# Every save now carries the game version, and the server refuses saves from versions before 697 (the copies that caused both
# rollbacks were old versions waking up on another device). The server also keeps the save that was replaced whenever a different
# device or tab takes over (backups/k0..k7), and the Restore list shows them as "Replaced by another device", so a bad takeover can be
# undone from the game itself.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('await store.db.doc(`data/users/${store.uid}/save`).set({ v: 3, savedAt: S.savedAt, json, sig, sess: SESS, seq, lv: z.lv, ships: z.ships, shrink });',
    'await store.db.doc(`data/users/${store.uid}/save`).set({ v: 3, savedAt: S.savedAt, json, sig, sess: SESS, seq, gv: GAME_V, lv: z.lv, ships: z.ships, shrink }); /* v697 gv: the server refuses saves from versions before 697 */')
rep('label: (d.id[0] === "d" ? "Daily server backup · " : "Hourly server backup · ")', 'label: (d.id[0] === "d" ? "Daily server backup · " : d.id[0] === "k" ? "Replaced by another device · " : "Hourly server backup · ") /* v697 */')
rep('const GAME_V = 696;', 'const GAME_V = 697;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
