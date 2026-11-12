# v503 (1) the Archives show the owner's full paintings (docs/art/arch/<k>.webp, from assets/bosses/*/reference and the super
# boss art; the five Elementals cut from their sheet along its panel lines), never the cut-out model skins, and never cropped.
# (2) the owner's ultimate-attack warnings from the Archives brief, on the live map: Vaelthar's charge, Khezaroth's singularity,
# Medusara's gaze, Aexion's Warform.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function archImg(E, lv) { if (!E.img) return `<div class="arimg glyph">${E.cat === "cube" ? "◼" : "✦"}</div>`; return `<div class="arimg${lv >= 2 ? " full" : ""}"><img src="art/boss/${E.img}.webp" alt="" loading="lazy"></div>`; }',
    'function archImg(E, lv, k) { if (k === "testament" || k === "cube") return `<div class="arimg glyph">${k === "cube" ? "◼" : "✦"}</div>`; return `<div class="arimg${lv >= 2 ? " full" : ""}"><img src="art/arch/${k}.webp" alt="" loading="lazy"></div>`; } // v503 the full paintings')
rep('${lv ? archImg(E, lv) : `<div class="arimg glyph lock">🔒</div>`}', '${lv ? archImg(E, lv, id).replace(\'class="arimg\', \'class="arimg big\') : `<div class="arimg glyph lock">🔒</div>`}')
rep('${lv ? archImg(E, lv) : `<div class="arimg glyph lock">?</div>`}', '${lv ? archImg(E, lv, k) : `<div class="arimg glyph lock">?</div>`}')
rep('.arimg img{width:100%;height:100%;object-fit:contain;', '.arimg.big{aspect-ratio:auto;display:block;background:#0e0b07}.arimg.big img{height:auto!important;display:block}.arimg img{width:100%;height:100%;object-fit:contain;')
rep('filter:sepia(1) saturate(.55) contrast(1.15) brightness(.85);mix-blend-mode:luminosity}', 'filter:sepia(.85) saturate(.6) contrast(1.08) brightness(.9)}')
rep('.arimg.full img{filter:none;mix-blend-mode:normal}', '.arimg.full img{filter:none}')
# the warnings
rep('say(k + ce + "f", "It\'s firing! Divine Annihilation is sweeping across the galaxy!"); }',
    'say(k + ce + "f", "It\'s firing! Divine Annihilation is sweeping across the galaxy!"); if (res !== "interrupted") { if (f > .22 && f < .4) say(k + ce + "u1", "The outer ring is accelerating. Multiple energy channels are activating."); if (f > .44 && f < .58) say(k + ce + "u2", "Energy output is exceeding our instruments\' calibrated range."); if (f > .6 && f < .66) say(k + ce + "u3", "Commander, MOVE THE FLEET! NOW!"); if (f > .93) say(k + ce + "u4", "The energy discharge has ended. I\'m analyzing the damage."); } }')
rep('if (f > .3 && f < .7 && res !== "interrupted") say(k + ce + "w2", "The starlight is bending into it... it\'s pulling everything in!");',
    'if (f > .3 && f < .7 && res !== "interrupted") say(k + ce + "w2", "The starlight is bending into it... it\'s pulling everything in!"); if (f > .1 && f < .28 && res !== "interrupted") say(k + ce + "u1", "The sphere between its paws is developing an event horizon."); if (f > .6 && f < .74 && res !== "interrupted") say(k + ce + "u2", "Destroy the gravity anchors before the singularity expands!");')
rep('if (res !== "interrupted" && f > .76 && f < .9) say(k + ce + "f", "Her gaze is sweeping the field... our ships are turning to stone!"); }',
    'if (res !== "interrupted" && f > .76 && f < .9) say(k + ce + "f", "Her gaze is sweeping the field... our ships are turning to stone!"); if (res !== "interrupted") { if (f > .1 && f < .3) say(k + ce + "u1", "Massive energy accumulation detected within both ocular structures."); if (f > .64 && f < .76) say(k + ce + "u2", "BREAK FORMATION! HER EYES ARE CHARGING!"); if (f > .93) say(k + ce + "u3", "Commander... the ancient accounts said her gaze turned armies to stone. We\'ve just witnessed the technological equivalent."); } }')
rep('if (xf && T - xf > 32000 && T - xf < 90000) say(k + xf + "c", "It\'s standing up. That thing is a Warform!");',
    'if (xf && T - xf > 32000 && T - xf < 90000) say(k + xf + "c", "It\'s standing up. That thing is a Warform!"); if (xf && T - xf > 66000 && T - xf < 180000) say(k + xf + "u1", "Holographic shield detected. Heavy weapons active. Avoid its frontal attack arc.");')
s2 = re.sub(r"GAME_V = 502\b", "GAME_V = 503", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
