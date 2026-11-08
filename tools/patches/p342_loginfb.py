p="docs/udf-supabase.js"; s=open(p).read()
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)
rep("""          (mode === "in" && resendOn ? '<div class="row"><button type="button" class="l" data-a="resend">Resend confirmation email</button></div>' : "") + '</form>';""",
"""          (mode === "in" && resendOn ? '<div class="row"><button type="button" class="l" data-a="resend">Resend confirmation email</button></div>' : "") +
          (np ? "" : '<div class="row fbrow"><button type="button" class="l" data-a="fb">Trouble signing in? Send feedback</button></div>') + '</form>';""")
rep("""        else if (a === "eye") { var pi = w.querySelector("input[name=p]"); if (pi)""","""        else if (a === "fb") loginFeedback();
        else if (a === "eye") { var pi = w.querySelector("input[name=p]"); if (pi)""")
rep("""  function signInScreen(startMode) {""","""  /* v342: feedback from the sign-in screen, before there is an account (server function login_feedback; it lands in the owner's feedback inbox) */
  function loginFeedback() {
    var o = document.createElement("div"); o.id = "udfFb"; o.className = "udfa"; document.body.appendChild(o);
    var em = lastEmail();
    o.innerHTML = '<form class="bx" novalidate><h2>Send feedback</h2><p>Tell us what went wrong signing in or creating your account. Add your email if you\\'d like a reply.</p>' +
      '<textarea name="t" rows="5" maxlength="2000" placeholder="What happened?"></textarea><input name="e" type="email" autocomplete="email" inputmode="email" placeholder="Email (optional)" value="' + esc(em) + '">' +
      '<div class="er" role="alert"></div><button type="submit" class="p">Send</button><button type="button" class="l" data-a="x">Cancel</button></form>';
    var f = o.querySelector("form"), er = o.querySelector(".er"), busyFb = false;
    o.addEventListener("click", function (e) { var b = e.target.closest("[data-a=x]"); if (b) { e.preventDefault(); o.remove(); } });
    f.addEventListener("submit", function (e) { e.preventDefault(); if (busyFb) return; var t = (f.t.value || "").trim(); if (t.length < 3) { er.textContent = "Type a few words first."; return; }
      busyFb = true; er.className = "er ok"; er.textContent = "Sending…";
      loadSdk().then(function () { return run(sb.rpc("login_feedback", { p_text: t, p_email: (f.e.value || "").trim(), p_device: navigator.userAgent.slice(0, 200) })); })
        .then(function () { er.className = "er ok"; er.textContent = "Thanks! Your feedback was sent."; setTimeout(function () { o.remove(); }, 1600); },
          function (x) { busyFb = false; er.className = "er"; er.textContent = /busy/.test((x && x.message) || "") ? "Lots of feedback right now. Try again in a little while." : "Couldn't send it. Check your connection and try again."; });
    });
    setTimeout(function () { try { f.t.focus(); } catch (x) {} }, 50);
  }
  function signInScreen(startMode) {""")
rep(".udfa .row{display:flex;justify-content:space-between}",".udfa .row{display:flex;justify-content:space-between}.udfa .fbrow{justify-content:center}#udfFb{position:fixed;inset:0;z-index:300;display:flex;align-items:center;justify-content:center;padding:20px;background:#02060c;font-family:\x27Barlow Semi Condensed\x27,Arial,sans-serif;color:#d5e4ec}#udfFb textarea{width:100%;box-sizing:border-box;border-radius:10px;border:1px solid rgba(85,214,232,.4);background:rgba(0,0,0,.35);color:#e8f6ff;padding:10px;font:inherit;font-size:15px;resize:vertical;margin-bottom:8px}")
open(p,"w").write(s); print("ok")
