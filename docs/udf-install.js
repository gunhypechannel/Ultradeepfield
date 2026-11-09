/* v361 Ultra Deep Field: "Add to Home Screen" guide. A short animated walkthrough on a drawn phone, for iPhone (Safari) and Android
   (Chrome), opened from the install button on the sign-in screen (or window.udfInstallGuide() from the game). On Android Chrome, when
   the browser offers it, an "Install now" button installs straight away. */
(function () {
  var UA = navigator.userAgent, IOS = /iPad|iPhone|iPod/.test(UA) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1), AND = /Android/i.test(UA);
  var STANDALONE = !!(navigator.standalone || (window.matchMedia && matchMedia("(display-mode: standalone)").matches));
  var deferred = null; window.addEventListener("beforeinstallprompt", function (e) { e.preventDefault(); deferred = e; var b = document.querySelector("#udfInst .now"); if (b) b.hidden = false; });
  window.addEventListener("appinstalled", function () { deferred = null; var o = document.getElementById("udfInst"); if (o) o.remove(); });
  var css =
    "#udfInstBtn{position:fixed;top:calc(env(safe-area-inset-top,0px) + 12px);right:12px;z-index:5;display:flex;align-items:center;gap:8px;padding:6px 12px 6px 6px!important;width:auto!important;border-radius:16px!important;border:1px solid rgba(110,200,255,.55)!important;background:linear-gradient(180deg,rgba(10,30,52,.78),rgba(3,12,24,.9))!important;color:#e8f6ff!important;font:700 13px 'Oxanium',sans-serif!important;letter-spacing:.03em;box-shadow:0 0 18px rgba(60,160,255,.3);cursor:pointer;animation:udfInsP 2.8s ease-in-out infinite}" +
    "#udfInstBtn i{width:30px;height:30px;border-radius:8px;background:url(icons/icon-192.png) center/cover;box-shadow:0 0 0 1px rgba(255,255,255,.25)}" +
    "#udfInstBtn b{display:block;font-size:9.5px;font-weight:600;color:#8fe6f5;letter-spacing:.06em;text-transform:uppercase;line-height:1}" +
    "@keyframes udfInsP{0%,100%{box-shadow:0 0 14px rgba(60,160,255,.25)}50%{box-shadow:0 0 26px rgba(85,214,232,.65)}}" +
    "#udfInst{position:fixed;inset:0;z-index:500;display:flex;align-items:center;justify-content:center;padding:14px;background:rgba(2,6,12,.88);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);font-family:'Barlow Semi Condensed',Arial,sans-serif;color:#d5e4ec}" +
    "#udfInst .card{width:min(400px,100%);max-height:100%;overflow:auto;display:flex;flex-direction:column;align-items:center;gap:10px;padding:16px 14px 12px;border-radius:22px;background:linear-gradient(180deg,#0b1d30,#050c16);border:1px solid rgba(110,200,255,.4);box-shadow:0 0 40px rgba(40,140,255,.25)}" +
    "#udfInst h2{margin:0;font:800 19px 'Oxanium',sans-serif;color:#eaf6fb;text-align:center}" +
    "#udfInst .tabs{display:flex;gap:6px;background:#06111d;border-radius:999px;padding:4px;border:1px solid #1d3647}" +
    "#udfInst .tabs button{border:0;border-radius:999px;padding:7px 16px;background:none;color:#8fb2c8;font:700 14px 'Oxanium',sans-serif;cursor:pointer}#udfInst .tabs button.on{background:#1f6fd0;color:#fff}" +
    "#udfInst .ph{position:relative;width:210px;height:430px;flex:none;border-radius:34px;background:#000;padding:9px;box-shadow:0 0 0 2px #3a4652,0 0 0 4px #10161d,0 18px 40px rgba(0,0,0,.6)}" +
    "#udfInst .sc{position:relative;width:100%;height:100%;border-radius:26px;overflow:hidden;background:#05090f;font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:#111}" +
    "#udfInst .notch{position:absolute;top:6px;left:50%;transform:translateX(-50%);width:62px;height:17px;border-radius:10px;background:#000;z-index:9}" +
    "#udfInst .page{position:absolute;inset:0;background:url(art/login.webp) center top/cover}" +
    "#udfInst .ibar{position:absolute;left:8px;right:8px;bottom:12px;height:36px;border-radius:18px;background:rgba(245,245,247,.92);display:flex;align-items:center;gap:6px;padding:0 6px 0 12px;font-size:11px;color:#333;box-shadow:0 2px 10px rgba(0,0,0,.35)}" +
    "#udfInst .ibar .u{flex:1;text-align:center;white-space:nowrap;overflow:hidden}#udfInst .dots3{width:26px;height:26px;border-radius:13px;background:#e3e3e8;display:grid;place-items:center;font-weight:900;letter-spacing:1px;color:#222;font-size:13px}" +
    "#udfInst .abar{position:absolute;left:0;right:0;top:26px;height:40px;background:#202124;display:flex;align-items:center;gap:6px;padding:0 6px 0 10px;font-size:11px;color:#ddd}" +
    "#udfInst .abar .u{flex:1;background:#303134;border-radius:16px;padding:7px 10px;white-space:nowrap;overflow:hidden}#udfInst .kebab{width:22px;height:28px;display:grid;place-items:center;color:#eee;font-size:18px;font-weight:900;line-height:1}" +
    "#udfInst .menu{position:absolute;border-radius:14px;background:rgba(250,250,252,.97);box-shadow:0 8px 30px rgba(0,0,0,.45);overflow:hidden;font-size:12px;transform-origin:bottom right;animation:udfInsPop .35s ease-out both}" +
    "#udfInst .menu div{padding:9px 12px;border-bottom:1px solid #e5e5ea;display:flex;justify-content:space-between;gap:10px;white-space:nowrap}#udfInst .menu div:last-child{border-bottom:0}" +
    "#udfInst .menu.dk{background:#2d2e31;color:#e8eaed;transform-origin:top right}#udfInst .menu.dk div{border-bottom-color:#3c4043}" +
    "#udfInst .hl{background:rgba(0,122,255,.16);font-weight:700}#udfInst .menu.dk .hl{background:rgba(138,180,248,.22)}" +
    "@keyframes udfInsPop{from{opacity:0;transform:scale(.85)}to{opacity:1;transform:none}}" +
    "#udfInst .sheet{position:absolute;left:0;right:0;bottom:0;border-radius:16px 16px 0 0;background:#f2f2f7;box-shadow:0 -6px 30px rgba(0,0,0,.4);padding:10px 10px 18px;font-size:12px;animation:udfInsUp .4s ease-out both}" +
    "@keyframes udfInsUp{from{transform:translateY(100%)}to{transform:none}}" +
    "#udfInst .sheet .apps{display:flex;gap:8px;margin:6px 0 10px}#udfInst .sheet .apps span{width:34px;height:34px;border-radius:9px;flex:none}" +
    "#udfInst .row2{background:#fff;border-radius:10px;overflow:hidden}#udfInst .row2 div{padding:9px 11px;border-bottom:1px solid #e5e5ea;display:flex;justify-content:space-between}#udfInst .row2 div:last-child{border-bottom:0}" +
    "#udfInst .ah{display:flex;justify-content:space-between;align-items:center;white-space:nowrap;gap:4px;font-size:10.5px;padding:2px 2px 10px;font-weight:600}#udfInst .ah .add{color:#007aff;font-weight:800;padding:3px 6px;border-radius:6px}" +
    "#udfInst .appic{width:46px;height:46px;border-radius:11px;background:url(icons/icon-192.png) center/cover;flex:none}" +
    "#udfInst .tg{width:34px;height:20px;border-radius:10px;background:#34c759;position:relative;flex:none}#udfInst .tg:after{content:'';position:absolute;right:2px;top:2px;width:16px;height:16px;border-radius:8px;background:#fff}" +
    "#udfInst .dlg{position:absolute;left:14px;right:14px;top:34%;border-radius:20px;background:#2d2e31;color:#e8eaed;padding:16px 14px 10px;font-size:12px;box-shadow:0 10px 40px rgba(0,0,0,.6);animation:udfInsPop .35s ease-out both}" +
    "#udfInst .dlg .bt{display:flex;justify-content:flex-end;gap:14px;margin-top:14px;font-weight:700;color:#8ab4f8}#udfInst .dlg .bt span{padding:4px 6px;border-radius:6px}" +
    "#udfInst .home{position:absolute;inset:0;background:radial-gradient(120% 80% at 30% 10%,#3b4f9a,#141a3a 60%,#0a0d1e);display:grid;grid-template-columns:repeat(4,1fr);align-content:start;gap:16px 0;padding:46px 12px 0}" +
    "#udfInst .home .ic{display:flex;flex-direction:column;align-items:center;gap:3px;font-size:8.5px;color:#fff}#udfInst .home .ic span{width:38px;height:38px;border-radius:10px}" +
    "#udfInst .home .new span{background:url(icons/icon-192.png) center/cover;animation:udfInsDrop .6s cubic-bezier(.3,1.6,.5,1) both .3s}" +
    "@keyframes udfInsDrop{from{transform:scale(0);opacity:0}to{transform:none;opacity:1}}" +
    "#udfInst .open{position:absolute;inset:0;background:url(art/login.webp) center top/cover;animation:udfInsOpen .45s ease-out both}@keyframes udfInsOpen{from{clip-path:inset(30% 40% 55% 40% round 12px);opacity:.4}to{clip-path:inset(0 round 0);opacity:1}}" +
    "#udfInst .fin{position:absolute;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;background:rgba(255,255,255,.55);border:2px solid rgba(255,255,255,.95);box-shadow:0 2px 10px rgba(0,0,0,.5);z-index:20;transition:left .7s cubic-bezier(.4,0,.2,1),top .7s cubic-bezier(.4,0,.2,1),transform .15s,opacity .3s;pointer-events:none}" +
    "#udfInst .fin.dn{transform:scale(.72)}#udfInst .rip{position:absolute;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;border:2px solid #fff;z-index:19;animation:udfInsRip .5s ease-out forwards;pointer-events:none}@keyframes udfInsRip{to{transform:scale(4);opacity:0}}" +
    "#udfInst .cap{min-height:44px;text-align:center;font-size:15px;line-height:1.3;color:#eaf6fb}#udfInst .cap b{color:#55d6e8;font-family:'Oxanium',sans-serif}" +
    "#udfInst .pips{display:flex;gap:6px}#udfInst .pips button{width:9px;height:9px;padding:0;border-radius:50%;border:0;background:#2c5468;cursor:pointer}#udfInst .pips button.on{background:#55d6e8}" +
    "#udfInst .note{font-size:12.5px;color:#8fb2c8;text-align:center;line-height:1.35;margin:0}" +
    "#udfInst .acts{display:flex;gap:8px;width:100%}#udfInst .acts button{flex:1;border-radius:12px;padding:11px;font:700 14px 'Oxanium',sans-serif;cursor:pointer;border:1px solid #55d6e8;background:rgba(85,214,232,.14);color:#8fe6f5}" +
    "#udfInst .acts .now{background:linear-gradient(180deg,#5ab8ff,#1f6fd0);border:0;color:#fff}" +
    "@media (prefers-reduced-motion:reduce){#udfInst *{animation-duration:.01s!important;transition-duration:.01s!important}#udfInstBtn{animation:none}}";
  var cssOn = false; function addCss() { if (cssOn) return; cssOn = true; var s = document.createElement("style"); s.textContent = css; document.head.appendChild(s); }
  var fakes = ["#ff9f0a", "#30d158", "#0a84ff", "#ff375f", "#bf5af2", "#64d2ff", "#ffd60a", "#5e5ce6", "#ff453a", "#32ade6", "#a2845e", "#66d4cf"];
  function homeGrid() { var h = ""; for (var i = 0; i < 11; i++) h += '<div class="ic"><span style="background:linear-gradient(160deg,' + fakes[i] + ',' + fakes[(i + 5) % 12] + ')"></span>App</div>'; return h + '<div class="ic new"><span></span>Deep Field</div>'; }
  /* each step: what the screen shows, the caption, and where the finger taps (percent of the screen) */
  var STEPS = {
    ios: [
      { cap: "In <b>Safari</b>, tap the <b>\u2022\u2022\u2022</b> button next to the address.", tap: [86, 92.5], html: function () { return '<div class="page"></div><div class="ibar"><span class="u">deep-field game</span><span class="dots3">\u2022\u2022\u2022</span></div>'; } },
      { cap: "Tap <b>Share</b>.", tap: [50, 81], html: function () { return '<div class="page"></div><div class="ibar"><span class="u">deep-field game</span><span class="dots3">\u2022\u2022\u2022</span></div><div class="menu" style="right:8px;bottom:56px;width:150px"><div>Add Bookmark<span>\u2606</span></div><div>New Tab<span>\uff0b</span></div><div class="hl">Share<span>\u21ea</span></div></div>'; } },
      { cap: "Scroll down and tap <b>Add to Home Screen</b>.", tap: [45, 92], html: function () { return '<div class="page"></div><div class="sheet"><div style="display:flex;gap:8px;align-items:center"><span class="appic" style="width:30px;height:30px;border-radius:7px"></span><b>Ultra Deep Field</b></div><div class="apps"><span style="background:#30d158"></span><span style="background:#0a84ff"></span><span style="background:#ff9f0a"></span><span style="background:#bf5af2"></span><span style="background:#ff375f"></span></div><div class="row2"><div>Copy<span>\u29c9</span></div><div>Add to Favorites<span>\u2606</span></div><div class="hl">Add to Home Screen<span>\u229e</span></div></div></div>'; } },
      { cap: "Keep <b>Open as Web App</b> on, then tap <b>Add</b>.", tap: [88, 60.5], html: function () { return '<div class="page"></div><div class="sheet" style="top:56%"><div class="ah"><span style="color:#007aff">Cancel</span><span>Add to Home Screen</span><span class="add hl">Add</span></div><div class="row2"><div style="justify-content:flex-start;gap:10px;align-items:center"><span class="appic"></span><span><b>Deep Field</b><br><span style="color:#888;font-size:10px">deep-field game</span></span></div><div style="align-items:center">Open as Web App<span class="tg"></span></div></div></div>'; } },
      { cap: "Done! Tap the <b>Deep Field</b> icon to play full screen.", tap: [87.5, 15.5], html: function () { return '<div class="home">' + homeGrid() + '</div>'; }, open: 1 }
    ],
    android: [
      { cap: "In <b>Chrome</b>, tap the <b>\u22ee</b> menu at the top right.", tap: [91, 11], html: function () { return '<div class="page" style="top:66px"></div><div class="abar"><span class="u">deep-field game</span><span class="kebab">\u22ee</span></div>'; } },
      { cap: "Tap <b>Add to Home screen</b> (or <b>Install app</b>).", tap: [50, 42.5], html: function () { return '<div class="page" style="top:66px"></div><div class="abar"><span class="u">deep-field game</span><span class="kebab">\u22ee</span></div><div class="menu dk" style="right:6px;top:30px;width:160px"><div>New tab</div><div>History</div><div>Downloads</div><div>Bookmarks</div><div class="hl">Add to Home screen</div><div>Settings</div></div>'; } },
      { cap: "Tap <b>Install</b>.", tap: [82, 61], html: function () { return '<div class="page" style="top:66px"></div><div class="abar"><span class="u">deep-field game</span><span class="kebab">\u22ee</span></div><div class="dlg"><b style="font-size:14px">Install app</b><div style="display:flex;gap:10px;align-items:center;margin-top:12px"><span class="appic"></span><span><b>Deep Field</b><br><span style="color:#9aa0a6;font-size:10px">deep-field game</span></span></div><div class="bt"><span>Cancel</span><span class="hl">Install</span></div></div>'; } },
      { cap: "Done! Tap the <b>Deep Field</b> icon to play full screen.", tap: [87.5, 15.5], html: function () { return '<div class="home">' + homeGrid() + '</div>'; }, open: 1 }
    ]
  };
  function guide(which) {
    addCss(); var old = document.getElementById("udfInst"); if (old) old.remove();
    var o = document.createElement("div"); o.id = "udfInst"; o.setAttribute("role", "dialog"); o.setAttribute("aria-label", "Add to Home Screen guide"); document.body.appendChild(o);
    var os = which || (AND ? "android" : "ios"), i = 0, timers = [], gone = false;
    o.innerHTML = '<div class="card"><h2>Play from your Home Screen</h2><div class="tabs"><button data-os="ios">iPhone</button><button data-os="android">Android</button></div>' +
      '<div class="ph"><div class="sc"><div class="notch"></div><div class="scr"></div><div class="fin"></div></div></div><div class="cap" aria-live="polite"></div><div class="pips"></div>' +
      '<p class="note"></p><div class="acts"><button class="now" hidden>Install now</button><button class="rp">Replay</button><button class="x">Close</button></div></div>';
    var scr = o.querySelector(".scr"), fin = o.querySelector(".fin"), cap = o.querySelector(".cap"), pips = o.querySelector(".pips"), note = o.querySelector(".note"), sc = o.querySelector(".sc");
    function clear() { timers.forEach(clearTimeout); timers = []; }
    function later(f, ms) { timers.push(setTimeout(function () { if (!gone) f(); }, ms)); }
    function show(n) {
      clear(); var S = STEPS[os]; i = (n + S.length) % S.length; var st = S[i];
      scr.innerHTML = '<div style="position:absolute;inset:0">' + st.html() + '</div>'; cap.innerHTML = '<span style="color:#7d95a5">Step ' + (i + 1) + ' of ' + S.length + ':</span> ' + st.cap;
      pips.innerHTML = S.map(function (_, k) { return '<button aria-label="Step ' + (k + 1) + '"' + (k === i ? ' class="on"' : "") + ' data-k="' + k + '"></button>'; }).join("");
      fin.style.opacity = 1; fin.classList.remove("dn"); if (i === 0) { fin.style.left = "50%"; fin.style.top = "62%"; }
      later(function () { fin.style.left = st.tap[0] + "%"; fin.style.top = st.tap[1] + "%"; }, 450);
      later(function () { fin.classList.add("dn"); var r = document.createElement("div"); r.className = "rip"; r.style.left = st.tap[0] + "%"; r.style.top = st.tap[1] + "%"; sc.appendChild(r); setTimeout(function () { r.remove(); }, 600); }, 1500);
      later(function () { fin.classList.remove("dn"); }, 1700);
      if (st.open) { later(function () { var d = document.createElement("div"); d.className = "open"; scr.firstChild.appendChild(d); fin.style.opacity = 0; }, 1850); later(function () { show(0); }, 4600); }
      else later(function () { show(i + 1); }, 2900);
    }
    function setOs(v) { os = v; o.querySelectorAll(".tabs button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-os") === os); });
      note.textContent = os === "ios" ? "Use Safari. On older iPhones the Share button is in the bar at the bottom of the screen. The icon keeps its own sign-in, so sign in again from the icon." : "Use Chrome. Samsung Internet: tap \u2261 (bottom right), then Add page to, then Home screen.";
      o.querySelector(".now").hidden = !(os === "android" && deferred); show(0); }
    o.addEventListener("click", function (e) {
      var t = e.target.closest("button"); if (!t) { if (e.target === o) close(); return; }
      if (t.hasAttribute("data-os")) setOs(t.getAttribute("data-os")); else if (t.hasAttribute("data-k")) show(+t.getAttribute("data-k"));
      else if (t.classList.contains("rp")) show(0); else if (t.classList.contains("x")) close();
      else if (t.classList.contains("now") && deferred) { deferred.prompt(); deferred.userChoice.then(function (c) { if (c && c.outcome === "accepted") close(); deferred = null; t.hidden = true; }); }
    });
    function close() { gone = true; clear(); o.remove(); document.removeEventListener("keydown", esc); }
    function esc(e) { if (e.key === "Escape") close(); } document.addEventListener("keydown", esc);
    setOs(os);
  }
  /* the button on the sign-in screen: only in a browser tab, never inside the installed app */
  function button(host) { if (STANDALONE || !host || host.querySelector("#udfInstBtn")) return; addCss();
    var b = document.createElement("button"); b.type = "button"; b.id = "udfInstBtn"; b.setAttribute("aria-label", "How to add the game to your Home Screen");
    b.innerHTML = '<i></i><span>Get the app<b>Add to Home Screen</b></span>'; b.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); guide(); }); host.appendChild(b); }
  window.udfInstallGuide = guide; window.udfInstallButton = button; window.udfStandalone = STANDALONE;
})();
