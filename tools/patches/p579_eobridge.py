"""v579 — the Empire Origins bridge (owner request, 2026-11-14: "bridge these two games, Empire Origins is the back story").
Empire Origins (EO) is the last Eclipse; Ultra Deep Field is the next one. In EO the Advisor is an echo in the Architects'
Echo Stones and calls the player "Founder"; its Space Age record "Beyond the Stars" links here with
?eo=EO1-<10 chapter results H/C/-><-5 seal strengths 0..a (flame, light, root, storm, void)>.
This patch reads that code once, keeps it in S.eo (synced with the save), cleans the URL, unlocks the Ages of the Deep record
"The Founder's Echo", and the Advisor recognises the player with two voiced lines: a greeting and a "Previously…" that
depends on how many of the age-of-empires seals held.
Usage: python3 tools/patches/p576_eobridge.py docs/index.html"""
import sys, json
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)
rep("const GAME_V = 578;", "const GAME_V = 579;")
L = {
 "found": "Founder... no. Commander. You found my stones once, a long time ago. I remember your voice.",
 "held": "In the age of empires, your people held the seals. That's why there is still a door to guard.",
 "mixed": "In the age of empires, some seals held and some cracked. I remember every one of them.",
 "cracked": "In the age of empires, the seals cracked. We've been paying for it ever since. Let's do better this time.",
}
REC = {"l_founder": {"cat": "ages", "t": "The Founder's Echo", "era": "The age of empires", "civ": "The Echo Stones", "loc": "The Ages of the Deep",
  "img": "art/season/s1-adv.webp", "th": "The canon",
  "frag": "Keep walking, Founder. There are more of me.",
  "interp": "Long before the Concord, in the age of empires, the Architects' voice spoke from obelisks called Echo Stones. The empire builders who listened called her nothing at all; she called them Founders. The ones who held their seals built the arks, and their children became the Concord. She remembers every Founder who reached the stars.",
  "adv": "You heard me in the stone, Commander. That was the first time anyone listened to the end.", "enc": [], "def": []}}
rep("function advOnce(k) {", """/* v579 the Empire Origins bridge: ?eo=EO1-<10 x H/C/-><-5 seal digits> from Empire Origins' "Beyond the Stars" */
Object.assign(ARCH, %s);
const EO_IN = (() => { try { const m = location.search.match(/[?&]eo=(EO1-[HC-]{10}-[0-9a]{5})(?:&|$)/); if (!m) return null; try { const u = new URL(location.href); u.searchParams.delete("eo"); history.replaceState(null, "", u.pathname + u.search + u.hash); } catch (e) {} return m[1]; } catch (e) { return null; } })();
const EO_L = %s;
function eoBridge() { if (!S || !G.ready) return; if (EO_IN && (!S.eo || S.eo.code !== EO_IN)) { const r = EO_IN.slice(4, 14); S.eo = { code: EO_IN, at: now(), held: (r.match(/H/g) || []).length, cracked: (r.match(/C/g) || []).length, said: 0 }; dirty(); }
  const E = S.eo; if (!E || E.said || tutOn() || battle) return; E.said = now(); dirty();
  try { archUnlock("l_founder", 2, true); } catch (e) {}
  const n = E.held + E.cracked, tail = !n ? null : E.held >= n * .7 ? EO_L.held : E.held <= n * .3 ? EO_L.cracked : EO_L.mixed;
  setTimeout(() => { try { advHolo(EO_L.found, true); } catch (e) {} }, 2500);
  if (tail) setTimeout(() => { try { advHolo(tail, true); } catch (e) {} }, 10500); }
setInterval(() => { try { eoBridge(); } catch (e) {} }, 3000);
function advOnce(k) {""" % (json.dumps(REC, ensure_ascii=False), json.dumps(L, ensure_ascii=False)))
open(p, "w", encoding="utf-8").write(s)
# the Advisor's four new lines for the voice lab
def h(t):
    x = 2166136261
    for ch in t:
        x ^= ord(ch); x = (x * 16777619) & 0xffffffff
    return x
def b36(n):
    d = "0123456789abcdefghijklmnopqrstuvwxyz"; o = ""
    while True:
        n, r = divmod(n, 36); o = d[r] + o
        if not n: return o
json.dump([{"key": b36(h(t)), "where": "eo bridge " + k, "line": t, "mood": "tender" if k == "found" else "grave"} for k, t in L.items()],
          open("tools/patches/p579_lines.json", "w"), indent=1, ensure_ascii=False)
print("ok v579")
