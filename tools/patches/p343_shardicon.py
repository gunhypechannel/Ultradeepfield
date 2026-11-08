# v343: the owner's Void Shard painting replaces the ◆ glyph on screen. A MutationObserver swaps ◆ in visible text for a small inline
# image (an <i class="shi">), so every one of the ~115 places that print ◆ (buttons, costs, rewards, toasts) gets it without
# touching their code. Text inputs and the message log's plain text stay as they are. The claude.ai artifact copy keeps the glyph.
p="docs/index.html"; h=open(p).read()
a=".shard{color:#c9a6ff}"
assert h.count(a)==1
h=h.replace(a,a+".shi{display:inline-block;width:1.15em;height:1.15em;vertical-align:-.2em;margin:0 .06em;background:url(icons/shard.webp?v=1) center/contain no-repeat;filter:drop-shadow(0 0 3px rgba(190,110,255,.7));font-style:normal}",1)
b="if (RI_IMG) for (const k of [\"m\", \"c\", \"g\", \"e\"])"
assert h.count(b)==1
h=h.replace(b,'''if (RI_IMG) { const SKIP = new Set(["SCRIPT", "STYLE", "TEXTAREA", "INPUT", "OPTION", "TITLE"]);
  const swap = root => { const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: n => n.nodeValue.includes("\\u25c6") && n.parentNode && !SKIP.has(n.parentNode.nodeName) && !n.parentNode.closest("[aria-hidden=true] svg") ? 1 : 2 }), L = [];
    while (w.nextNode()) L.push(w.currentNode);
    for (const n of L) { const f = document.createDocumentFragment(), parts = n.nodeValue.split("\\u25c6"); parts.forEach((t, i) => { if (t) f.appendChild(document.createTextNode(t)); if (i < parts.length - 1) { const e = document.createElement("i"); e.className = "shi"; e.setAttribute("aria-label", "Void Shards"); f.appendChild(e); } }); n.parentNode.replaceChild(f, n); } };
  const mo = new MutationObserver(ms => { for (const m of ms) { if (m.type === "characterData") { if (m.target.nodeValue && m.target.nodeValue.includes("\\u25c6") && m.target.parentNode) swap(m.target.parentNode); } else for (const n of m.addedNodes) { if (n.nodeType === 3) { if (n.nodeValue.includes("\\u25c6") && n.parentNode) swap(n.parentNode); } else if (n.nodeType === 1) swap(n); } } });
  const go = () => { swap(document.body); mo.observe(document.body, { childList: true, subtree: true, characterData: true }); }; if (document.body) go(); else addEventListener("DOMContentLoaded", go); }
'''+b)
open(p,"w").write(h); print("ok")
