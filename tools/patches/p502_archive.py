# v502 The Ancient Archives (owner's brief): the archive data, unlock triggers and the Archives screen live in p502_archive.js.
import sys, re, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p502_archive.js'), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const DEMO_ALLY = { a: {', JS + 'const DEMO_ALLY = { a: {')
# the first sight of an entity plays its discovery instead of the usual one-liner
JS2 = 'function archSheetSeen(s) { try { if (!s) return; if (s.type === "wboss" && s.id) archUnlock(archKeyOf(s.id), 1); else if (s.type === "sboss" && s.id) archUnlock(s.id, 1); else if (s.type === "nexus" || (s.type === "events" && s.ev === "cube")) archUnlock("cube", 1); } catch (e) {} }'
rep(JS2, 'function archSheetSeen(s) { try { if (!s) return false; const k = s.type === "wboss" && s.id ? archKeyOf(s.id) : s.type === "sboss" && s.id ? archKeyOf(s.id) : s.type === "nexus" || (s.type === "events" && s.ev === "cube") ? "cube" : null; if (!k || archLv(k)) return false; archUnlock(k, 1); return true; } catch (e) { return false; } }')
rep('function openSheet(s) { try { if (!sheet || sheet.type !== (s && s.type) || sheet.id !== (s && s.id)) bossHolo(s); } catch (e) {}',
    'function openSheet(s) { try { if (!sheet || sheet.type !== (s && s.type) || sheet.id !== (s && s.id)) { if (!archSheetSeen(s)) bossHolo(s); } } catch (e) {}')
rep('advHolo(WB_SCAN_SAY[D.con != null ? "con" : key]); }, 900); }', '{ const ak = archKeyOf(key); if (ak && !archLv(ak)) archUnlock(ak, 1); else advHolo(WB_SCAN_SAY[D.con != null ? "con" : key]); } }, 900); }')
rep('''function playBattle(r) {
  if (battle) closeBattle();''', '''function playBattle(r) {
  if (battle) closeBattle(); archFromRep(r);''')
# where to find it: the Game Menu and the toolbar
rep('${gl("mastery", ic2(TRAY_I.path), "Mastery", "", mastN)}', '${gl("mastery", ic2(TRAY_I.path), "Mastery", "", mastN)}${gl("archOpen", \'<span style="font-size:18px;line-height:1;color:#e2c48a">📜</span>\', "Archives", "", archUnread())}')
rep('["mastery", ic(TRAY_I.path), "Mastery", mastN, ""],', '["mastery", ic(TRAY_I.path), "Mastery", mastN, ""], ["archOpen", \'<span style="font-size:18px;line-height:1">📜</span>\', "Archives", archUnread(), ""],')
rep('ach: shAch,', 'ach: shAch, archives: shArch,')
rep('SHEET_NAME = { shop: "shop",', 'SHEET_NAME = { archives: "the Archives", shop: "shop",')
rep('  achOpen: () => openSheet({ type: "ach" }),', '''  achOpen: () => openSheet({ type: "ach" }),
  archOpen: () => { G.trayOpen = false; try { trayRender(); } catch (e) {} openSheet({ type: "archives" }); },
  archEntry: d => openSheet({ type: "archives", id: d.id }),
  archPlay: d => { const E = ARCH[d.id]; if (E) archSeq(E.enc.concat(E.def)); },''')
CSS = '''
.argrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin:6px 0 14px}
.arcard{position:relative;display:flex;flex-direction:column;text-align:left;padding:0;border-radius:12px;overflow:hidden;border:1px solid rgba(226,196,138,.28);background:linear-gradient(180deg,#1a1610,#0e0c09);color:#efe3c8;min-width:0}
.arcard span{display:flex;flex-direction:column;gap:3px;padding:8px 10px 10px;min-width:0}.arcard b{font:600 13px/1.25 Georgia,"Times New Roman",serif;color:#f3e2b8}.arcard small{font-size:11px;color:#b9a888;line-height:1.3}
.arcard em{font-style:normal;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#e2c48a}.arcard.lv0{opacity:.62}.arcard.lv0 em{color:#8d8170}
.arnew{position:absolute;top:6px;right:6px;font:700 9px/1 system-ui;letter-spacing:.1em;padding:4px 6px;border-radius:6px;background:#e2c48a;color:#1a1408;font-style:normal}
.argrid,.arcard,.arimg,.arfrag,.arint,.aradv{flex-shrink:0}
.arimg{position:relative;aspect-ratio:4/3;max-width:100%;background:radial-gradient(ellipse at 50% 60%,#3a2c18,#120e08 72%);display:flex;align-items:center;justify-content:center;overflow:hidden}
.arimg img{width:100%;height:100%;object-fit:contain;filter:sepia(1) saturate(.55) contrast(1.15) brightness(.85);mix-blend-mode:luminosity}
.arimg.full img{filter:none;mix-blend-mode:normal}.arimg.glyph{font-size:42px;color:#e2c48a;text-shadow:0 0 18px rgba(226,196,138,.6)}.arimg.lock{color:#7d6f58;text-shadow:none}
.sheet .arimg{border-radius:12px;margin:4px 0 12px;border:1px solid rgba(226,196,138,.25)}
.arfrag{margin:8px 0 12px;padding:14px 16px;border-radius:10px;background:linear-gradient(180deg,#2a2114,#1b150c);border:1px solid rgba(226,196,138,.35);box-shadow:inset 0 0 30px rgba(0,0,0,.45)}
.arfrag small,.arint small{display:block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#c9ab72;margin-bottom:6px}
.arfrag p{margin:0;font:italic 15px/1.55 Georgia,"Times New Roman",serif;color:#f1e2bf}
.arint{margin:0 0 12px;padding:12px 14px;border-radius:10px;background:rgba(90,170,255,.07);border:1px solid rgba(120,190,255,.25)}.arint p{margin:0;line-height:1.5}.arint.lock{opacity:.6}
.aradv{display:flex;gap:10px;align-items:flex-start;margin:0 0 12px;padding:10px 12px;border-radius:10px;background:rgba(80,220,255,.06);border:1px solid rgba(80,220,255,.22)}.aradv img{width:44px;height:44px;border-radius:50%;object-fit:cover;object-position:top;flex:none}.aradv p{margin:0;line-height:1.45;min-width:0}.aradv b{display:block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#7fe6ff;margin-bottom:3px}
.arth{color:#ff9a6a;font-weight:700}.arsec{color:#e2c48a}'''
rep('.mcard.tpcall h3{color:#ffb070}', '.mcard.tpcall h3{color:#ffb070}' + CSS)
s2 = re.sub(r"GAME_V = 501\b", "GAME_V = 502", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
