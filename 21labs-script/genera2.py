#!/usr/bin/env python3
# 21Labs v2: ritocca su fal.ai le immagini già fatte, in chiave più scura e petrolio (palette «Your Mom»).
# Uso: FAL_KEY=... python3 genera2.py nome1 nome2 ...   (salta i file già fatti)
import json, os, sys, urllib.request
KEY = os.environ.get("FAL_KEY") or sys.exit("Manca FAL_KEY")
SRC, OUT = "21labs-media", os.environ.get("OUT", "21labs-media/v2")
os.makedirs(OUT, exist_ok=True)
OGGETTO = ("Edit this image. Keep exactly the same object, shape, angle, framing and the pure black #000000 background. "
           "Make the mood darker and more refined: low-key studio lighting, the black volcanic glass body deeper and more matte. "
           "Replace the rose, peach and gold rim light with a thin, cool deep-teal rim light (#275B66 to #6FB3C2) and only a very faint "
           "warm off-white highlight. Subtle reflection on the black mirror floor. No text, no letters, no numbers, no logos.")
HERO = ("Edit this image. Keep the same volcano with two rounded peaks, the calm sea, the horizon and the framing. "
        "Make it darker and moodier, the last minutes before dawn: the sky a deep warm charcoal (#201D1C) fading to a muted dark teal "
        "near the horizon; the glow behind the crater reduced to a thin, soft, cool teal light with only a faint warm hint at the very center. "
        "Calm black mirror sea with a subtle teal reflection. Premium, minimal, cinematic. No text, no logos, no people.")
FIGO = ("Edit this image into a cinematic hero shot. Keep the same object, the same shape and the same angle, centered, with a pure black #000000 background at the borders. "
        "Material: deep black obsidian glass with fine micro-scratches, edges slightly translucent and glowing. "
        "Lighting: dramatic low-key, a single cool teal rim light (#275B66 to #6FB3C2) tracing the silhouette, a soft volumetric teal haze just behind the object, "
        "tiny floating dust particles catching the light, subtle reflection on a black glossy floor. Ultra detailed, premium tech keynote look. "
        "No text, no letters, no numbers, no logos.")
if os.environ.get("STILE") == "figo": OGGETTO = FIGO
def chiama(url, dati):
    req = urllib.request.Request(url, data=json.dumps(dati).encode(), headers={"Authorization": "Key " + KEY, "Content-Type": "application/json", "User-Agent": "21labs-genera/1.0"})
    with urllib.request.urlopen(req, timeout=600) as r: return json.load(r)
for nome in sys.argv[1:]:
    dest = os.path.join(OUT, nome + ".png")
    if os.path.exists(dest): print("già fatto", nome); continue
    src_url = open(os.path.join(SRC, nome + ".url")).read().strip()
    hero = nome == "hero"
    r = chiama("https://fal.run/fal-ai/nano-banana-pro/edit", {"prompt": HERO if hero else OGGETTO, "image_urls": [src_url],
        "aspect_ratio": "16:9" if hero else "1:1", "resolution": "2K" if hero else "1K", "num_images": 1, "output_format": "png"})
    url = r["images"][0]["url"]
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "21labs-genera/1.0"}), timeout=600) as f, open(dest, "wb") as o: o.write(f.read())
    open(os.path.join(OUT, nome + ".url"), "w").write(url)
    print("salvato", nome)
