# v483 Multiplayer plan, phase 1: no boss hit is ever lost. The boss hunt records (world bosses, the Omega Cube, the super bosses) are
# written with compare-and-set: the fleet's resolve reads the record with its version and writes back only if nobody has written since.
# If someone has (two players landing at the same moment, or a lease that ran out during a slow fight), it re-reads and fights again
# from the true hull, up to five times. The lease stays as the first line, so on a quiet boss nothing changes. Needs the doc_cas
# function (supabase/migrations/v483_doc_cas.sql) and udf-supabase.js getV()/cas(); elsewhere (offline, the artifact) it is a plain set.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("/* a fleet reaches a boss: fight it under the shared lock, write the hull it tore off, pay the bounty */",
r"""/* v483 compare-and-set on a shared hunt record: true when written; false when someone wrote first (the caller fights again) */
const CAS_RETRY = { cas: 1 }, casGet = ref => ref.getV ? ref.getV() : ref.get();
async function casSet(ref, snap, data) { if (!ref.cas || !snap || snap.v === undefined) { await ref.set(data); return true; } const ok = await ref.cas(snap.v, data); if (!ok) { try { crumb("cas conflict " + (ref.path || "")); } catch (e) {} } return ok; }
const casAgain = async (f, again) => { if (f.casN >= 5) return false; f.casN = (f.casN || 0) + 1; await sleep(150 + Math.random() * 650); await again(f); return true; };
/* a fleet reaches a boss: fight it under the shared lock, write the hull it tore off, pay the bounty */""")
for fn, norm, lost in [("wbResolve", "const snap = await ref.get(), cur = wbNorm(", 'note("Lost contact with the boss fight. Fleet returning.", "warn"); home(); }'),
                       ("omResolve", "const snap = await ref.get(), cur = omNorm(", 'note("Lost contact with the Omega Cube fight. Fleet returning.", "warn"); home(); }'),
                       ("sbResolve", "const snap = await ref.get(), cur = sbNorm(", "note(`Lost contact with the ${D.n} fight. Fleet returning.`, \"warn\"); home(); }")]:
    i = s.find("async function " + fn); j = s.find("finally {", i); seg = s[i:j]
    assert seg.count(norm) == 1 and seg.count("await ref.set(cur);") == 1 and seg.count("} catch (e) { " + lost) == 1, fn
    seg = seg.replace(norm, norm.replace("await ref.get()", "await casGet(ref)"))
    seg = seg.replace("await ref.set(cur);", "if (!(await casSet(ref, snap, cur))) throw CAS_RETRY; f.casN = 0;")
    seg = seg.replace("} catch (e) { " + lost, "} catch (e) { if (e === CAS_RETRY && await casAgain(f, " + fn + ")) return; " + lost)
    s = s[:i] + seg + s[j:]
s = re.sub(r"GAME_V = 482\b", "GAME_V = 483", s)
open(P, 'w').write(s)
