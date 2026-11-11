# v414 (1): live updates by topic. The client joins private Realtime Broadcast topics fed by the docs_broadcast trigger
# (supabase/migrations/v414_broadcast.sql): udf:pub (shared world records), udf:u:<me> (my inbox and DMs), udf:in:<me> (my inbound
# fleets) and udf:in:<ally> for each ally whose inbound it watches. The server checks the right to a topic once, at join, instead of a
# read rule per player per change. If the shared topic cannot be joined within 12 s, or is refused, the client falls back to the old
# postgres_changes feed, so nothing goes quiet.
p = "docs/udf-supabase.js"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""  function addL(map, k, fn) { (map[k] = map[k] || []).push(fn); return function () { var a = map[k]; if (!a) return; var i = a.indexOf(fn); if (i >= 0) a.splice(i, 1); if (!a.length) delete map[k]; }; }""",
"""  function addL(map, k, fn) { (map[k] = map[k] || []).push(fn); var tp = map === docL && /^inbound\\/[^/]+$/.test(k) ? "udf:in:" + k.split("/")[1] : null; if (tp && liveMode === "topics") join(tp); /* v414 an ally's inbound fleets: its own topic */
    return function () { var a = map[k]; if (!a) return; var i = a.indexOf(fn); if (i >= 0) { a.splice(i, 1); if (tp && liveMode === "topics") leave(tp); } if (!a.length) delete map[k]; }; }""")
rep("""  function startLive() {
    if (chan) return;
    chan = sb.channel("udf-docs")""", """  /* v414 live updates by topic (Realtime Broadcast from the database): each change is sent once to its topic */
  var topics = {}, liveMode = null;
  function onBc(m) { var p = m && m.payload; if (!p || !p.operation) return; onChange({ eventType: p.operation, new: p.record, old: p.old_record }); }
  function join(topic) { var T = topics[topic]; if (T) { T.n++; return; } T = topics[topic] = { n: 1, ok: false, down: false };
    T.c = sb.channel(topic, { config: { private: true } }).on("broadcast", { event: "*" }, onBc).subscribe(function (st) {
      if (st === "SUBSCRIBED") { if (T.down) refreshers.slice().forEach(function (f) { try { f(); } catch (e) {} }); T.ok = true; T.down = false; } /* back online: catch up */
      else if (st === "CHANNEL_ERROR" || st === "TIMED_OUT" || st === "CLOSED") { T.down = true; if (topic === "udf:pub" && !T.ok) fallback(); } }); }
  function leave(topic) { var T = topics[topic]; if (!T) return; if (--T.n <= 0) { try { sb.removeChannel(T.c); } catch (e) {} delete topics[topic]; } }
  function fallback() { if (liveMode === "pg") return; liveMode = "pg"; Object.keys(topics).forEach(function (k) { try { sb.removeChannel(topics[k].c); } catch (e) {} }); topics = {}; window.__udfLive = "pg"; startPg(); }
  function startLive() {
    if (liveMode) return; liveMode = "topics"; window.__udfLive = "topics";
    sb.auth.getSession().then(function (r) { var s = r && r.data && r.data.session; if (s && s.access_token) try { sb.realtime.setAuth(s.access_token); } catch (e) {} }, function () {}).then(function () {
      if (liveMode !== "topics") return; var id = me && me.id; join("udf:pub"); if (id) { join("udf:u:" + id); join("udf:in:" + id); }
      Object.keys(docL).forEach(function (k) { if (/^inbound\\/[^/]+$/.test(k)) join("udf:in:" + k.split("/")[1]); });
      setTimeout(function () { var T = topics["udf:pub"]; if (liveMode === "topics" && (!T || !T.ok)) fallback(); }, 12000); }); }
  function startPg() {
    if (chan) return;
    chan = sb.channel("udf-docs")""")
open(p, "w").write(t); print("ok")
