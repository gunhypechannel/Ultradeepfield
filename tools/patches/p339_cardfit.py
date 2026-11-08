p="docs/index.html"; h=open(p).read()
def rep(a,b):
    global h
    assert h.count(a)==1,(h.count(a),a[:70]); h=h.replace(a,b)
# v339 the art gap only takes the room that is left over, so a card fits the screen without scrolling
rep('.dgap{height:24vh;flex:none}','.dgap{flex:1 1 0;min-height:0;height:auto}')
# the back bar: no grey band over the card, just the see-through button
rep('padding:10px 16px calc(12px + env(safe-area-inset-bottom,0px));background:linear-gradient(180deg,rgba(10,22,32,0),var(--hull) 26%);z-index:4;display:flex}',
    'padding:8px 16px calc(10px + env(safe-area-inset-bottom,0px));background:none;z-index:4;display:flex;pointer-events:none}.sbk>*{pointer-events:auto}')
rep('.sheet.full.pic .segc,.sheet.full.pic .sbkb{background:rgba(4,14,26,.4);','.sheet.full.pic .segc,.sheet.full.pic .sbkb{background:rgba(4,14,26,.55);')
rep('.sbkb{flex:1;min-height:46px;border-radius:12px;border:1px solid var(--line-hi);background:rgba(18,40,56,.92);','.sbkb{flex:1;min-height:44px;border-radius:12px;border:1px solid var(--line-hi);background:rgba(10,26,40,.6);')
rep('#sheetwrap[data-type="flagship"] .sbk{background:linear-gradient(180deg,rgba(6,18,30,0),rgba(6,18,30,.55) 45%)}','#sheetwrap[data-type="flagship"] .sbk{background:none}')
rep('padding:8px 10px calc(10px + env(safe-area-inset-bottom,0px));background:linear-gradient(180deg,transparent,#020713 34%)}','padding:8px 10px calc(10px + env(safe-area-inset-bottom,0px));background:none}')
open(p,"w").write(h); print("ok")
h=open(p).read()
a='''<p>${esc(desc)}</p>${CLASS_OF[k] ? `<small>${CLS_BY[CLASS_OF[k]].ic} ${CLS_BY[CLASS_OF[k]].n} class · ${CLS_BY[CLASS_OF[k]].perk}</small>` : ""}</div>'''
b='''<div class="dtx${sheet.dmore ? " open" : ""}"><p>${esc(desc)}</p>${CLASS_OF[k] ? `<small>${CLS_BY[CLASS_OF[k]].ic} ${CLS_BY[CLASS_OF[k]].n} class · ${CLS_BY[CLASS_OF[k]].perk}</small>` : ""}</div>${desc.length > 75 || CLASS_OF[k] ? `<button class="dmore" data-act="dMore">${sheet.dmore ? "Less ▴" : "More ▾"}</button>` : ""}</div>'''  # v339: long descriptions fold to a few lines
assert h.count(a)==1; h=h.replace(a,b)
a='.dgap{flex:1 1 0;min-height:0;height:auto}'
assert h.count(a)==1; h=h.replace(a,a+'.dtx:not(.open) p{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:3;overflow:hidden}.dtx:not(.open) small{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden}.dmore{background:none;border:0;color:var(--cyan);font:600 12.5px var(--f-body,inherit);padding:2px 0;cursor:pointer}')
a='  back: () => sheetBack(),'
assert h.count(a)==1; h=h.replace(a,a+'\n  dMore: () => { if (sheet) { sheet.dmore = !sheet.dmore; renderSheet(); } },')
open(p,"w").write(h); print("ok2")
h=open(p).read()
a='.dmore{background:none;'
assert h.count(a)==1
h=h.replace(a,'@media (max-height:800px){.sheet.full.pic{gap:7px}.sheet.full.pic .dp{padding:7px 10px}.sheet.full.pic .dstat .dp{padding:5px 10px}.sheet.full.pic .dstat p{margin:2px 0;font-size:13px}.sheet.full.pic .dqty{gap:4px 8px}.sheet.full.pic .dres h4{margin:0 0 3px;font-size:13px}.sheet.full.pic .dreq td{padding:3px 2px}.sheet.full.pic .dreq th{padding:2px}.sheet.full.pic .sbk{padding-top:5px}.sheet.full.pic .sbkb{min-height:38px}.sheet.full.pic .dhead{grid-template-columns:64px 1fr auto;gap:10px}.sheet.full.pic .dtx:not(.open) p{-webkit-line-clamp:2}.sheet.full.pic .dtx:not(.open) small{-webkit-line-clamp:1}.sheet.full.pic .dhead h2{font-size:19px}.sheet.full.pic .dreq td:first-child{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:0;width:100%}}'+a,1)  # v339: short phones get a tighter card
open(p,"w").write(h); print("ok3")
h=open(p).read()
a='''w.style.bottom = top ? "auto" : (innerHeight - db + 64) + "px"; }'''
assert h.count(a)==1
h=h.replace(a,'''w.style.bottom = top ? "auto" : (innerHeight - db + 64) + "px";
  const dr = !el && $(".sheet.full .dres"); if (dr) { w.style.top = "auto"; w.style.bottom = Math.max(8, innerHeight - dr.getBoundingClientRect().top + 16) + "px"; } /* v339: on a card she stands above the costs, never over Requirements or Build */ }''')
open(p,"w").write(h); print("ok4")
