# fb-20261112: some Android keyboards / autofill fire keydown/keyup with no e.key,
# which threw "Cannot read properties of undefined (reading 'toLowerCase')" (crash report v460, Android).
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
for a, b in [
    ('if (typing || e.ctrlKey || e.metaKey || e.altKey) return; const k = e.key.toLowerCase();',
     'if (typing || e.ctrlKey || e.metaKey || e.altKey || !e.key) return; /* fb: no key from IME/autofill */ const k = e.key.toLowerCase();'),
    ('addEventListener("keyup", e => { const k = e.key.toLowerCase(),',
     'addEventListener("keyup", e => { const k = (e.key || "").toLowerCase(),'),
]:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
