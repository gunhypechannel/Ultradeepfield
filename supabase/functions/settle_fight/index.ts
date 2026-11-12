// settle_fight (multiplayer plan, phase 2: shadow). The phone sends the boss fight it just decided (the report's sim: both sides' stacks
// with their stats, the seed, the rules version) and the hull it says is left. The server runs the game's own simulator (sim.js, cut
// from the game by tools/sim_bundle.py) on the same inputs and logs whether the two agree in fight_log. It changes nothing for the
// player yet; phase 3 makes the server's result the one that counts.
import { createClient } from "npm:@supabase/supabase-js@2.45.4";
import { simulate } from "./sim.js";
const URL = Deno.env.get("SUPABASE_URL")!, SVC = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, ANON = Deno.env.get("SUPABASE_ANON_KEY")!;
const admin = createClient(URL, SVC, { auth: { persistSession: false } });
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type", "Access-Control-Allow-Methods": "POST, OPTIONS" };
const out = (o: unknown, st = 200) => new Response(JSON.stringify(o), { status: st, headers: { ...CORS, "Content-Type": "application/json" } });
// deno-lint-ignore no-explicit-any
const hyd = (a: any[]) => a.map(([k, n, atk, sh, hull, own, ab]) => ({ k: String(k), n: +n, atk: +atk, sh: +sh, hull: +hull, own: own == null ? null : String(own), ab: +ab || 0, w: 0 }));
// deno-lint-ignore no-explicit-any
const okStacks = (a: any) => Array.isArray(a) && a.length > 0 && a.length <= 400 && a.every((x: any) => Array.isArray(x) && x.length >= 5 && typeof x[0] === "string" && [1, 2, 3, 4].every(i => Number.isFinite(+x[i]) && +x[i] >= 0));
Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return out({ error: "POST only" }, 405);
  const user = await createClient(URL, ANON, { global: { headers: { Authorization: req.headers.get("Authorization") || "" } }, auth: { persistSession: false } }).auth.getUser();
  const uid = user.data.user?.id; if (!uid) return out({ error: "sign in first" }, 401);
  // deno-lint-ignore no-explicit-any
  let b: any; try { b = await req.json(); } catch { return out({ error: "bad json" }, 400); }
  const sim = b && b.sim; if (!sim || !okStacks(sim.A) || !okStacks(sim.D) || ![3, 4, 5].includes(+sim.v)) return out({ error: "bad sim" }, 400);
  const unit = String(b.unit || "").slice(0, 32), kind = String(b.kind || "").slice(0, 16), n0 = Math.max(0, Math.floor(+b.n0 || 0)), claimed = Math.floor(+b.left);
  const t0 = performance.now(); let r;
  try { r = simulate(hyd(sim.A), hyd(sim.D), { seed: (+sim.seed) >>> 0, doc: sim.doc || null, quick: !!sim.quick, v: +sim.v }); }
  catch (e) { await admin.from("fight_log").insert({ uid, kind, unit, game_v: +b.v || null, ok: null, client: { left: claimed, n0 }, server: { error: String(e).slice(0, 300) } }); return out({ error: "simulator failed" }, 500); }
  const ms = performance.now() - t0, left = Math.min(n0, Math.max(0, Math.round((r.dLeft || {})[unit] || 0))), ok = left === claimed;
  // deno-lint-ignore no-explicit-any
  const aLeft: Record<string, number> = {}; for (const [k, v] of Object.entries(r.aLeft || {})) aLeft[k] = Math.round(v as any);
  await admin.from("fight_log").insert({ uid, kind, unit, game_v: +b.v || null, ok, client: { left: claimed, n0, lossA: b.lossA || null }, server: { left, aLeft, winner: r.winner, rounds: (r.rounds || []).length }, ms: Math.round(ms * 10) / 10 });
  return out({ ok, left });
});
