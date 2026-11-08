p='docs/index.html'; t=open(p,encoding='utf-8').read()
a='  if (!top) return 0; if (top === el || el.contains(top)) return 1; if (top.closest("#coach")) return 3; // 3: under the Academy panel'
b='  if (!top) return 0; if (top === el || el.contains(top)) return 1; if (top.closest("#coach")) return 3; // 3: under the Academy panel\n  if (top.closest(".sheet, .scrim") && !el.closest(".sheet")) return 0; /* v338: covered by an open card: never ring it through the card (a ghost box) */'
assert t.count(a)==1; t=t.replace(a,b); open(p,'w',encoding='utf-8').write(t)
