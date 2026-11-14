# v544 share a battle as a video (owner: "Do it all", idea #3; his TikTok/Instagram plan). The battle replay's toolbar gets ⏺ Clip:
# the replay restarts at 2× and is recorded into a vertical 720×1280 video (the battle fills the frame, cropped to fit) with the game's
# name and the battle's title at the top, and the result plus "Play free" and the game's address at the bottom. Recording stops 2.5 s
# after the result (or at 45 s, or when the replay is closed). Then a card shows the clip with Share (the phone's share sheet, straight
# to TikTok/Instagram/Messages) and Save. MP4 where the browser can make it (Safari, recent Chrome), WebM otherwise. Video only.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
JS = r'''
/* ---------- v544 share a battle as a vertical video ---------- */
const CLIP_URL = "gunhypechannel.github.io/Ultradeepfield";
function clipMime() { if (!window.MediaRecorder) return null; for (const m of ["video/mp4;codecs=avc1", "video/mp4", "video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm"]) try { if (MediaRecorder.isTypeSupported(m)) return m; } catch (e) {} return null; }
function battleClip() { const b0 = battle, cv0 = $("#bcv"), mime = clipMime(); if (!b0 || G.clip) return; if (!cv0 || !mime || !document.createElement("canvas").captureStream) return toast("This browser can't record clips. Try Safari or Chrome on your phone.", "warn");
  const r = b0.r; ACT.breplay(); const b = battle; b.speed = 2; battleCtl(); const W = 720, H = 1280, oc = document.createElement("canvas"); oc.width = W; oc.height = H; const x = oc.getContext("2d");
  const title = String(r.title || "Battle").slice(0, 60), who = `${r.aName || "Attackers"} vs ${r.dName || "Defenders"}`.slice(0, 60), chunks = [];
  let rec; try { rec = new MediaRecorder(oc.captureStream(30), { mimeType: mime, videoBitsPerSecond: 4500000 }); } catch (e) { return toast("Couldn't start recording on this device.", "warn"); }
  rec.ondataavailable = e => { if (e.data && e.data.size) chunks.push(e.data); };
  const C = G.clip = { rec, t0: performance.now(), doneAt: 0 }; const pill = document.createElement("div"); pill.id = "clippill"; pill.innerHTML = "<i></i>REC · recording your clip"; document.body.appendChild(pill);
  const wrap = (txt, maxW, font) => { x.font = font; const out = [], ws = txt.split(" "); let ln = ""; for (const w of ws) { const t2 = ln ? ln + " " + w : w; if (x.measureText(t2).width > maxW && ln) { out.push(ln); ln = w; } else ln = t2; } if (ln) out.push(ln); return out; };
  const frame = () => { if (G.clip !== C) return; const cv = $("#bcv");
    x.fillStyle = "#03060c"; x.fillRect(0, 0, W, H);
    if (cv && cv.width && cv.height) { const sc = Math.max(W / cv.width, H / cv.height), dw = cv.width * sc, dh = cv.height * sc; try { x.drawImage(cv, (W - dw) / 2, (H - dh) / 2, dw, dh); } catch (e) {} }
    let g = x.createLinearGradient(0, 0, 0, 260); g.addColorStop(0, "rgba(3,6,12,.92)"); g.addColorStop(1, "rgba(3,6,12,0)"); x.fillStyle = g; x.fillRect(0, 0, W, 260);
    g = x.createLinearGradient(0, H - 300, 0, H); g.addColorStop(0, "rgba(3,6,12,0)"); g.addColorStop(1, "rgba(3,6,12,.95)"); x.fillStyle = g; x.fillRect(0, H - 300, W, 300);
    x.textAlign = "center"; x.fillStyle = "#ffcf5a"; x.shadowColor = "#ffcf5a"; x.shadowBlur = 18; x.font = "800 46px 'Orbitron','Rajdhani',sans-serif"; x.fillText("ULTRA DEEP FIELD", W / 2, 78); x.shadowBlur = 0;
    x.fillStyle = "#e9f6ff"; const tl = wrap(title, W - 80, "700 30px 'Rajdhani',sans-serif"); tl.slice(0, 2).forEach((l, i) => x.fillText(l, W / 2, 128 + i * 36));
    x.fillStyle = "#9fdcff"; x.font = "500 24px 'Rajdhani',sans-serif"; x.fillText(who, W / 2, 128 + Math.min(2, tl.length) * 36 + 6);
    const b2 = battle; if (b2 && (b2.done || b2.ending)) { const win = r.winner === "draw" ? "DRAW" : repWin(r) ? "VICTORY" : "DEFEAT"; x.fillStyle = win === "VICTORY" ? "#5dff9a" : win === "DEFEAT" ? "#ff6b5a" : "#ffcf5a"; x.shadowColor = x.fillStyle; x.shadowBlur = 24; x.font = "900 84px 'Orbitron','Rajdhani',sans-serif"; x.fillText(win, W / 2, H - 170); x.shadowBlur = 0; if (!C.doneAt) C.doneAt = performance.now(); }
    x.fillStyle = "#ffffff"; x.font = "700 30px 'Rajdhani',sans-serif"; x.fillText("Play free · build your empire", W / 2, H - 96); x.fillStyle = "#7af4ff"; x.font = "600 26px 'Rajdhani',sans-serif"; x.fillText(CLIP_URL, W / 2, H - 56);
    const el = performance.now() - C.t0; if (!battle || battle !== b || (C.doneAt && performance.now() - C.doneAt > 2500) || el > 45000) return clipStop(C, mime, title); requestAnimationFrame(frame); };
  rec.onstop = () => { pill.remove(); const blob = new Blob(chunks, { type: mime.split(";")[0] }); G.clip = null; if (blob.size < 2000) return toast("The clip came out empty. Try again with the replay open.", "warn"); clipCard(blob, mime, title); };
  rec.start(500); requestAnimationFrame(frame); crumb("battle clip recording"); }
function clipStop(C, mime, title) { try { if (C.rec.state !== "inactive") C.rec.stop(); } catch (e) { G.clip = null; } }
function clipCard(blob, mime, title) { const ext = /mp4/.test(mime) ? "mp4" : "webm", name = `udf-battle-${Date.now().toString(36)}.${ext}`, file = new File([blob], name, { type: blob.type }), url = URL.createObjectURL(blob);
  let w = $("#clipcard"); if (w) w.remove(); w = document.createElement("div"); w.id = "clipcard";
  const canShare = !!(navigator.canShare && navigator.canShare({ files: [file] }));
  w.innerHTML = `<div class="clipbx"><b>Your battle clip</b><video src="${url}" controls playsinline loop muted autoplay></video><small>${(blob.size / 1048576).toFixed(1)} MB · ${ext.toUpperCase()} · vertical 9:16, ready for TikTok, Reels and Shorts</small><div class="clipbt">${canShare ? '<button class="btn amber" data-clip="share">Share</button>' : ""}<a class="btn ${canShare ? "ghost" : "amber"}" href="${url}" download="${name}">Save</a><button class="btn ghost" data-clip="close">Close</button></div></div>`;
  document.body.appendChild(w);
  w.addEventListener("click", e => { const a = e.target.closest("[data-clip]"); if (!a) { if (e.target === w) { w.remove(); URL.revokeObjectURL(url); } return; } if (a.dataset.clip === "close") { w.remove(); URL.revokeObjectURL(url); } else navigator.share({ files: [file], title: "Ultra Deep Field", text: `${title} · Play free: https://${CLIP_URL}/` }).catch(() => {}); });
  crumb("battle clip ready"); }
'''
rep('function battleCtl() {', JS + 'function battleCtl() {')
rep('<button data-act="breplay" aria-label="Replay from the start">⟲</button>', '<button data-act="breplay" aria-label="Replay from the start">⟲</button><button data-act="bclip" aria-label="Record this battle as a video to share" class="${G.clip ? "on" : ""}">⏺</button>')
rep('  breplay: () => {', '  bclip: () => battleClip(), /* v544 */\n  breplay: () => {')
css = '''
/* v544 battle clips */
#clippill{position:fixed;top:calc(env(safe-area-inset-top,0px) + 10px);left:50%;transform:translateX(-50%);z-index:9999;display:flex;align-items:center;gap:8px;padding:6px 14px;border-radius:20px;background:rgba(20,4,8,.85);border:1px solid #ff4d5a;color:#fff;font-size:12.5px;font-weight:700;letter-spacing:.06em;pointer-events:none}
#clippill i{width:10px;height:10px;border-radius:50%;background:#ff4d5a;box-shadow:0 0 10px #ff4d5a;animation:clipb 1s ease-in-out infinite}@keyframes clipb{50%{opacity:.3}}
#clipcard{position:fixed;inset:0;z-index:9998;display:grid;place-items:center;background:rgba(2,5,10,.78);padding:16px}
.clipbx{display:flex;flex-direction:column;gap:8px;width:min(360px,100%);padding:14px;border-radius:16px;border:1px solid rgba(85,214,232,.5);background:#08121c}.clipbx video{width:100%;max-height:62vh;border-radius:10px;background:#000;object-fit:contain}.clipbx small{font-size:11.5px;color:var(--muted)}
.clipbt{display:flex;gap:8px;flex-wrap:wrap}.clipbt>*{flex:1 0 auto;text-align:center;text-decoration:none}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 543\b", "GAME_V = 544", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
