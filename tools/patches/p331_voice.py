import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v331 the Advisor's voice: recorded clips (voice/<key>.mp3, listed in voice/index.json; made with tools/voice_lines.json in
# docs/voicelab.html). Only recorded clips play: no robotic device voice. Off with the 🔊 on her card, Settings › Sound, or mute.
VOICE = r'''
const VOICE = { on: true, clips: null, au: null, lastStep: -1 };
try { VOICE.on = localStorage.getItem("void.voice") !== "0"; } catch (e) {}
const voiceKey = s => hash(String(s)).toString(36);
try { fetch("voice/index.json", { cache: "no-cache" }).then(r => r.ok ? r.json() : null).then(j => { if (j && typeof j === "object") VOICE.clips = j; }).catch(() => {}); } catch (e) {}
function voiceTalk(on) { const a = $("#adv"); if (a) a.classList.toggle("talk", !!on); }
function voiceStop() { voiceTalk(0); try { if (VOICE.au) { VOICE.au.pause(); VOICE.au = null; } } catch (e) {} }
function speak(line) { if (!VOICE.on || (typeof AU !== "undefined" && AU.muted) || !line || !VOICE.clips) return; const k = voiceKey(line); if (!VOICE.clips[k]) return; voiceStop();
  try { const a = new Audio("voice/" + k + ".mp3"); a.volume = Math.min(1, .95 * ((typeof AU !== "undefined" && AU.sfxVol != null) ? Math.max(.4, AU.sfxVol) : 1)); VOICE.au = a;
    a.onplay = () => voiceTalk(1); a.onended = a.onpause = () => voiceTalk(0); a.play().catch(() => voiceTalk(0)); } catch (e) {} }
'''
rep('''function say(lines) {''', VOICE.strip('\n') + '\nfunction say(lines) {')
rep('''Tap to continue</div></div></div></div>`;''', '''Tap to continue</div></div><button class="advv" data-act="voiceToggle" aria-label="Advisor voice">${VOICE.on ? "🔊" : "🔇"}</button></div></div>`;''')
rep('''  $("#advt").textContent = advLines[0];''', '''  $("#advt").textContent = advLines[0]; speak(advLines[0]);''')
rep('''function advNext() { advLines.shift(); if (advLines.length) $("#advt").textContent = advLines[0]; else { advLines = null; $("#adv").remove();''',
    '''function advNext() { advLines.shift(); if (advLines.length) { $("#advt").textContent = advLines[0]; speak(advLines[0]); } else { voiceStop(); advLines = null; $("#adv").remove();''')
rep('''  if (force || html !== coachHtml) { coachHtml = html; w.innerHTML = html; const c = w.querySelector(".cav"); if (c) try { drawAdvisor(c, 0); } catch (e) {} }
}
setInterval(() => { try { coachRender(); } catch (e) {} }, 800);''', '''  if (force || html !== coachHtml) { coachHtml = html; w.innerHTML = html; const c = w.querySelector(".cav"); if (c) try { drawAdvisor(c, 0); } catch (e) {} }
  if (open && !done && VOICE.lastStep !== S.tut.i && !advLines && !$("#celeb") && !battle) { VOICE.lastStep = S.tut.i; speak(st.say); } // v331: each new step, read once as it opens
}
setInterval(() => { try { coachRender(); } catch (e) {} }, 800);''')
rep('''  $("#app").appendChild(w); try { SFX.gong(); } catch (e) {} G.celebNow = c; }''', '''  $("#app").appendChild(w); try { SFX.gong(); } catch (e) {} try { speak(c.say || c.s); } catch (e) {} G.celebNow = c; }''')
rep('''  celebX: () => { const w = $("#celeb"); if (w) w.remove(); G.celebNow = null;''', '''  celebX: () => { const w = $("#celeb"); if (w) w.remove(); G.celebNow = null; voiceStop();''')
rep('''${tglRow("sfxToggle", AU.sfxOn, "Battle, construction and interface effects")}''', '''${tglRow("sfxToggle", AU.sfxOn, "Battle, construction and interface effects")}${tglRow("voiceToggle", VOICE.on, "Advisor voice")}''')
rep('''tg("sfxToggle", AU.sfxOn, "Battle, construction and interface effects")''', '''tg("sfxToggle", AU.sfxOn, "Battle, construction and interface effects")}${tg("voiceToggle", VOICE.on, "Advisor voice")''')
rep('''  sfxToggle: () => {''', '''  voiceToggle: () => { VOICE.on = !VOICE.on; try { localStorage.setItem("void.voice", VOICE.on ? "1" : "0"); } catch (e) {} if (!VOICE.on) voiceStop(); else if (advLines) speak(advLines[0]);
    const b = $("#adv .advv"); if (b) b.textContent = VOICE.on ? "🔊" : "🔇"; toast(VOICE.on ? "Advisor voice on." : "Advisor voice off."); if (sheet) renderSheet(); else render(true); },
  sfxToggle: () => {''')
rep('''#coach.gdhide>*{''', '''#adv .advv{position:absolute;right:10px;top:10px;z-index:3;width:38px;height:38px;border-radius:50%;border:1px solid rgba(85,214,232,.6);background:rgba(4,14,22,.75);color:#bff6ff;font-size:17px;line-height:1;cursor:pointer}
#coach.gdhide>*{''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
