"""v829: the Advisor log reads back every voiced line, at once (owner: "the voice ques thing is kinda laggy when you press a text it
doesn't read it back sometimes"). In the owner's log 5 of 9 lines had no recording, so a tap did nothing with no sign why; the voiced ones
were fetched only on the tap (the lag); Archive entries were logged as "Title: line", so even recorded ones never matched their clip;
and an Archive record with no line was logged as an empty "What They Guard: ".
Now: each row says whether it has her voice (a speaker, or "text only"); the row playing glows and its speaker pulses; the log's voiced
clips are fetched into memory when the page opens (and each queued line's when it is logged), and every play uses the copy in memory; a
tap on a text-only line says so; Archive rows play the line without its title; an Archive record with nothing to say is not logged."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 828;", "const GAME_V = 829;")
# play from memory when we have the clip
rep('''a.src = "voice/" + k + ".mp3?v=" + VOICE.clips[k];''', '''a.src = (VOICE.mem && VOICE.mem[k]) || ("voice/" + k + ".mp3?v=" + VOICE.clips[k]); VOICE.cur = k;''')
# log: no empty Archive entries
rep('''else advLog(`${E.t}: ${(lv === 1 ? E.enc : E.def)[0] || ""}`, "lore"); } /* v820 */''', '''else { const l0 = (lv === 1 ? E.enc : E.def)[0]; if (l0) advLog(`${E.t}: ${l0}`, "lore"); } } /* v820; v829 nothing logged when the record has no line */''')
# fetch a logged line's clip ahead
rep('''  S.advLog.unshift({ t: now(), l: line, k: kind || "note", u: 1 }); if (S.advLog.length > 40) S.advLog.length = 40; dirty(); advBadge(); }''',
    '''  S.advLog.unshift({ t: now(), l: line, k: kind || "note", u: 1 }); if (S.advLog.length > 40) S.advLog.length = 40; dirty(); advBadge(); try { voiceWarm(advVoiceLine(line, kind)); } catch (e) {} }
/* v829 the line her clip was recorded for (an Archive row carries its record's title in front), whether it has one, and the clip fetched into memory ahead of the tap */
function advVoiceLine(l, k) { const has = x => !!(VOICE.clips && VOICE.clips[voiceKey(x)]); if (has(l)) return l; const i = String(l).indexOf(": "); if (i > 0 && has(l.slice(i + 2))) return l.slice(i + 2); return k === "lore" && i > 0 ? l.slice(i + 2) : l; }
function voiceHas(l) { return !!(l && VOICE.clips && VOICE.clips[voiceKey(l)]); }
function voiceWarm(l) { if (!voiceHas(l)) return; const k = voiceKey(l), M = VOICE.mem || (VOICE.mem = {}), P = VOICE.memP || (VOICE.memP = {}); if (M[k] || P[k]) return; const ks = Object.keys(M); if (ks.length > 60) { try { URL.revokeObjectURL(M[ks[0]]); } catch (e) {} delete M[ks[0]]; }
  P[k] = 1; fetch("voice/" + k + ".mp3?v=" + VOICE.clips[k]).then(r => r.ok ? r.blob() : null).then(b => { delete P[k]; if (b && b.size) M[k] = URL.createObjectURL(b); }).catch(() => { delete P[k]; }); }''')
# rows: a speaker or "text only"; warm the clips as the page opens
rep('''L.map((x, i) => `<button class="alrow${x.u ? " new" : ""}" data-act="advLogSay" data-i="${i}"><small>${{ live: "Live", lore: "Archives", news: "News", note: "Note", greet: "Greeting" }[x.k] || "Note"} · ${ago(x.t)}</small><span>${esc(x.l)}</span></button>`).join("")''',
    '''L.map((x, i) => { const vl = advVoiceLine(x.l, x.k), v = voiceHas(vl); if (v) setTimeout(() => voiceWarm(vl), 30 + i * 40); return `<button class="alrow${x.u ? " new" : ""}${v ? " vo" : " tx"}" data-act="advLogSay" data-i="${i}" data-h="${voiceKey(x.l)}"><small>${{ live: "Live", lore: "Archives", news: "News", note: "Note", greet: "Greeting" }[x.k] || "Note"} · ${ago(x.t)}<em>${v ? "🔊" : "text only"}</em></small><span>${esc(x.l)}</span></button>`; }).join("")''')
rep('''  advLogSay: d => { const x = (S.advLog || [])[+d.i]; if (x) { try { speak(x.l); } catch (e) {} } },''',
    '''  advLogSay: d => { const LG = S.advLog || [], x = (d.h && LG.find(y => voiceKey(y.l) === d.h)) || LG[+d.i]; if (!x) return; /* the row's own line, even if the log moved under it */ const vl = advVoiceLine(x.l, x.k); document.querySelectorAll(".alrow.play").forEach(e => e.classList.remove("play"));
    if (!voiceHas(vl)) { toast("No voice recording for this line yet."); return; } if (!VOICE.on || (typeof AU !== "undefined" && AU.muted)) { toast("Her voice is off. Turn it on with the 🔊 in Sound settings."); return; }
    const row = document.querySelector(`.alrow[data-h="${d.h}"]`); try { speak(vl); } catch (e) {} const a = VOICE.au; if (row && a) { row.classList.add("play"); const off = () => row.classList.remove("play"); a.addEventListener("ended", off, { once: true }); a.addEventListener("pause", off, { once: true }); a.addEventListener("error", off, { once: true }); } }, /* v829 */''')
rep('''.alrow small{font-size:11px;color:#7f97a9}''', '''.alrow small{font-size:11px;color:#7f97a9;display:flex;gap:8px;width:100%}.alrow small em{margin-left:auto;font-style:normal;font-size:11px;opacity:.85}.alrow.tx small em{color:#61778a}.alrow.tx span{color:#b9c6d1}.alrow.play{border-color:rgba(200,140,255,.7);background:rgba(160,100,255,.12);box-shadow:0 0 14px rgba(170,110,255,.35)}.alrow.play small em{animation:alpl .8s ease-in-out infinite alternate}@keyframes alpl{from{transform:scale(1);filter:none}to{transform:scale(1.25);filter:drop-shadow(0 0 4px #c890ff)}}''')
rep("""then(j => { if (j && typeof j === "object") VOICE.clips = j; })""", """then(j => { if (j && typeof j === "object") { VOICE.clips = j; try { if (sheet && sheet.type === "advlog") renderSheet(); } catch (e) {} } })""")
open(p, "w", encoding="utf-8").write(s); print("ok")
