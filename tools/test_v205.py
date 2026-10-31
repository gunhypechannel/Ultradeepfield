import asyncio, json, sys, subprocess, time, os
from playwright.async_api import async_playwright
SITE=sys.argv[1]; OUT=sys.argv[2]
MOCK=open(os.path.join(os.path.dirname(__file__),"mock-firebase-slow.js")).read()
H=json.load(open(f"{OUT}/heal.json"))
CFG='window.UDF_FIREBASE={apiKey:"test-key",authDomain:"udf-test.firebaseapp.com",projectId:"udf-test",appId:"1:1:web:1",ownerUids:[]};'
SEED="window.__seed={'data/users/uid_novatestdev_test/save':"+json.dumps(H["cloud"])+"};try{if(!sessionStorage.getItem('seeded')){localStorage.setItem('novaDominion.save.v1',"+json.dumps(H["local"])+");localStorage.setItem('novaDominion.save.v1.sig',"+json.dumps(H["localSig"])+");sessionStorage.setItem('seeded','1')}}catch(e){}"
RULE="""window.__rule=function(p,old,n){ if(!/\\/save$/.test(p)||!old) return true;
 if('seq' in old && (n.seq||0)!==old.seq+1) return false;
 if('lv' in old && old.lv>=10 && n.shrink!==true && (n.lv||0)*2<old.lv) return false; return true; };"""
K="data/users/uid_novatestdev_test/save"

async def page(b):
    ctx=await b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True)
    await ctx.add_init_script(SEED); await ctx.add_init_script(RULE)
    pg=await ctx.new_page(); errs=[]
    pg.on("pageerror",lambda e: errs.append((e.stack or str(e))[:400]))
    await ctx.route(lambda u: not u.startswith("http://localhost") and "gstatic.com/firebasejs" not in u, lambda r: r.abort())
    await ctx.route("https://www.gstatic.com/firebasejs/**",lambda r: r.fulfill(status=200,content_type="application/javascript",body=MOCK if "app-compat" in r.request.url else "/**/"))
    await ctx.route("**/firebase-config.js",lambda r: r.fulfill(status=200,content_type="application/javascript",body=CFG))
    await pg.goto("http://localhost:8774/",wait_until="domcontentloaded")
    await pg.wait_for_selector("#udfAuth",timeout=15000)
    await pg.fill("input[name=e]","nova@test.dev"); await pg.fill("input[name=p]","abcdef"); await pg.click("button.p")
    await pg.wait_for_timeout(9000)
    await pg.evaluate("(()=>{for(let i=0;i<20&&document.querySelector('#adv .adv');i++)document.querySelector('#adv .adv').click(); const s=document.querySelector('#sheetwrap .scrim'); if(s) s.click();})()")
    return ctx,pg,errs
SV="(()=>{const d=window.__store['"+K+"']; return d?{seq:d.seq,lv:d.lv,sess:d.sess===__T.store.seq?0:d.sess&&d.sess.slice(0,6),shrink:d.shrink}:null})()"
async def save(pg): await pg.evaluate("(async()=>{__T.dirty(); await __T.flush();})()"); await pg.wait_for_timeout(1500)
async def main():
    srv=subprocess.Popen([sys.executable,"-m","http.server","8774","-d",SITE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    try:
      async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        # A: saves go in order; alliance membership comes from the alliance
        ctx,pg,errs=await page(b)
        s1=await pg.evaluate("__T.store.seq"); await save(pg); await save(pg)
        print("A seq before/after 2 saves:", s1, await pg.evaluate("__T.store.seq"), "| server:", await pg.evaluate(SV))
        await pg.evaluate("(()=>{__T.S.ally=null; const me=__T.G.me; firebase.firestore().doc('alliances/al_test').set({name:'Deep Fielders',tag:'DFX',leader:me,members:{[me]:Date.now()},at:Date.now()});})()")
        await pg.wait_for_timeout(2500)
        print("A save said no alliance, alliance lists me -> S.ally:", await pg.evaluate("__T.S.ally"))
        await pg.evaluate("__T.ACT.allyLeave()"); await pg.wait_for_timeout(3000)
        print("A after leaving -> S.ally:", await pg.evaluate("__T.S.ally"), "| doc exists:", await pg.evaluate("!!window.__store['alliances/al_test']"))
        print("A errors:", errs[:3]); await ctx.close()
        # B: another device saved first (no live update reached us): the server refuses ours, we pause
        ctx,pg,errs=await page(b)
        await save(pg)
        await pg.evaluate("(()=>{const d=window.__store['"+K+"']; d.seq+=1; d.sess='otherdev';})()")
        before=await pg.evaluate(SV); await save(pg)
        print("B server unchanged:", before==await pg.evaluate(SV), "| overlay:", await pg.evaluate("document.querySelector('#sessw b') && document.querySelector('#sessw b').textContent"), "| paused:", await pg.evaluate("!!__T.store.paused"))
        await save(pg); print("B still unchanged after more play:", before==await pg.evaluate(SV))
        print("B errors:", errs[:3]); await ctx.close()
        # C: this copy is a near-wipe of a big saved empire: refused
        ctx,pg,errs=await page(b)
        await save(pg); await pg.evaluate("(()=>{window.__store['"+K+"'].lv=100000;})()")
        await save(pg)
        print("C overlay:", await pg.evaluate("document.querySelector('#sessw b') && document.querySelector('#sessw b').textContent"), "| server lv:", await pg.evaluate("window.__store['"+K+"'].lv"))
        print("C errors:", errs[:3]); await ctx.close()
        # D: starting over on purpose is allowed
        ctx,pg,errs=await page(b)
        await save(pg); await pg.evaluate("(()=>{window.__store['"+K+"'].lv=100000;})()")
        await pg.evaluate("__T.ACT.resetYes()"); await pg.wait_for_timeout(2500)
        print("D after Start over: server lv", await pg.evaluate("window.__store['"+K+"'].lv"), "| overlay:", await pg.evaluate("!!document.querySelector('#sessw')"), "| shrinkOk cleared:", not await pg.evaluate("__T.store.shrinkOk"))
        await save(pg); print("D later save shrink flag:", await pg.evaluate("window.__store['"+K+"'].shrink"))
        print("D errors:", errs[:3]); await ctx.close()
        await b.close()
    finally: srv.terminate()
asyncio.run(main())
