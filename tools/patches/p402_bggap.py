# fb-20261110 (owner's choice): report "Restarted after N min in the background" only when away under 30 min.
# Longer gaps are phones/Chrome clearing idle apps, which is normal; short ones are the iOS memory kills worth seeing.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
a = 'if (gone < 6 * 3600e3) hqPush({ kind: "crash", status: "new", at: Date.now(), now: typeof GAME_V !== "undefined" ? GAME_V : 0, bg: 1,'
b = 'if (gone < 30 * 60e3) hqPush({ kind: "crash", status: "new", at: Date.now(), now: typeof GAME_V !== "undefined" ? GAME_V : 0, bg: 1,'
assert t.count(a) == 1
t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
