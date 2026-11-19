  mimOpen: () => openSheet({ type: "mimic" }), /* v663 */
  mimFind: () => { const x = mimNearest(now()); if (x) mimGo(x); else toast("No hive within reach right now."); },
  mimPrev: d => { if (!ownerFree()) return; const w = +d.w; S.mimPrev = w ? { w, at: now() } : null; dirty(); toast(w ? `Previewing week ${w} of the Mimic Protocol.` : "Preview off."); renderSheet(); },
  mimClaim: d => { const w = +d.w, M = mimS(), o = MIM_OBJ[w - 1]; if (!o || M.got["w" + w] || mimObjN(w) < o[1]) return; M.got["w" + w] = 1; S.shards = (S.shards || 0) + o[2]; M.m.tis = (M.m.tis || 0) + o[3]; dirty(); toast(`+◆${o[2]} and ${o[3]} Mimic Tissue`, "win"); try { logReward(`Mimic Protocol · week ${w} objective`, null, { shards: o[2], kind: "event" }); } catch (e) {} renderSheet(); },
