import asyncio, json, sys, subprocess, time, os
from playwright.async_api import async_playwright
SITE=sys.argv[1]; OUT=sys.argv[2]
MOCK=open(os.path.join(os.path.dirname(__file__),"mock-firebase.js")).read()
CFG='window.UDF_FIREBASE={apiKey:"test-key",authDomain:"udf-test.firebaseapp.com",projectId:"udf-test",appId:"1:1:web:1",ownerUids:[]};'
async def main():
    srv=subprocess.Popen([sys.executable,"-m","http.server","8765","-d",SITE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    try:
      async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox","--use-gl=swiftshader","--enable-unsafe-swiftshader"])
        ctx=await b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=await ctx.new_page(); errs=[]
        pg.on("console",lambda m: errs.append(m.type+": "+m.text) if m.type in("error","warning") else None)
        pg.on("pageerror",lambda e: errs.append("PAGEERROR: "+str(e)))
        async def fb(route):
            u=route.request.url
            await route.fulfill(status=200,content_type="application/javascript",body=MOCK if "app-compat" in u else "/*mock*/")
        await ctx.route("https://www.gstatic.com/firebasejs/**",fb)
        await ctx.route("**/firebase-config.js",lambda r: r.fulfill(status=200,content_type="application/javascript",body=CFG))
        await pg.goto("http://localhost:8765/",wait_until="domcontentloaded")
        await pg.wait_for_selector("#udfAuth",timeout=15000)
        await pg.screenshot(path=f"{OUT}/1-signin.png")
        await pg.click("text=New here? Create account")
        await pg.fill("input[name=n]","Nova")
        await pg.fill("input[name=e]","nova@test.dev")
        await pg.fill("input[name=p]","abc")
        await pg.click("button.p"); await pg.wait_for_timeout(300)
        print("weak pw msg:", await pg.inner_text("#udfAuth .er"))
        await pg.fill("input[name=p]","abcdef"); print("kept name:", await pg.input_value("input[name=n]"))
        await pg.click("button.p")
        await pg.wait_for_selector("#udfAuth",state="detached",timeout=10000)
        await pg.wait_for_timeout(12000)
        await pg.screenshot(path=f"{OUT}/2-game.png")
        keys=await pg.evaluate("Object.keys(window.__store)")
        print("docs:",len(keys)); print(sorted(set(k.split('/')[0] for k in keys)))
        print([k for k in keys if k.startswith(("players","profiles","data"))][:10])
        # deep-merge behaviour of update()
        r=await pg.evaluate("""async()=>{const db=await window.claude.use('db');await db.doc('alliances/t1').set({gifts:{a:{x:1}},name:'A'});
          await db.doc('alliances/t1').update({gifts:{b:{x:2}},help:{u1:{by:{u2:5}}}});await db.doc('alliances/t1').update({help:{u1:{by:{u3:6}}}});
          let miss=null;try{await db.doc('chat/none').update({m:{a:1}})}catch(e){miss=e.code}
          const l=await db.doc('galaxy/join').acquire({holder:'me',ttlMs:5000});
          const u=await window.claude.use('user');
          return {doc:(await db.doc('alliances/t1').get()).data(),miss,lock:l.acquired,me:await u.me(),id:await u.id(),owner:await u.isOwner()}}""")
        print(json.dumps(r))
        # menu text + sign out button
        mode=await pg.evaluate("document.body.innerText.includes('Connecting to the shared galaxy')")
        print("still connecting:",mode)
        print("ERRORS:"); [print("  ",e[:300]) for e in errs[:25]]
        await b.close()
    finally: srv.terminate()
asyncio.run(main())
