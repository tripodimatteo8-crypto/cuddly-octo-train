#!/usr/bin/env python3
# 21Labs: genera su fal.ai le immagini e il video dell'alba per il sito.
# Uso: FAL_KEY="la-tua-chiave" python3 genera.py
# Se lo rilanci non paga due volte: salta quello che ha già scaricato.
import json, os, sys, time, urllib.request

KEY = os.environ.get("FAL_KEY") or sys.exit("Manca FAL_KEY: vedi le istruzioni in cima al file.")
RUN = os.environ.get("FAL_RUN", "https://fal.run")
CODA = os.environ.get("FAL_QUEUE", "https://queue.fal.run")
OUT = "21labs-media"
os.makedirs(OUT, exist_ok=True)

STILE = ("Ultra clean 3D product render in the style of a premium tech keynote. The object is made of "
         "polished black volcanic glass (obsidian) with a thin rim light in rose, peach and warm gold, "
         "like the first light of a sunrise. Soft reflection on a black mirror floor. Pure black #000000 "
         "background, object centered with generous empty space around it. No text, no letters, no numbers, "
         "no logos, no people. ")
OGGETTI = {
    "ecommerce": "Object: a minimal shopping bag, warm light glowing softly from inside.",
    "vetrina": "Object: a map location pin, with a small glowing dot at its center.",
    "prenotazioni": "Object: a minimal desk calendar block with a grid of small squares, one square glowing.",
    "gestionale": "Object: three floating stacked glass panels showing simple glowing bar-chart shapes.",
    "automazioni": "Object: two interlocking gears with a small glowing lightning bolt between them.",
    "app": "Object: a thick rounded-square app icon tile floating slightly above the floor, edges glowing.",
    "contenuti": "Object: a circular play button with a triangle in the middle, glowing softly.",
    "campagne": "Object: a megaphone emitting three soft rings of light.",
    "centralino": "Object: a minimal classic telephone handset floating at a slight angle, with three soft glowing sound-wave arcs coming from the earpiece.",
}
HERO = ("Cinematic wide 3D render, just before sunrise. A volcano with two rounded peaks, sculpted in polished "
        "black volcanic glass, rises on the horizon in the center of the frame, over a perfectly calm black "
        "mirror sea. Behind the crater a thin line of rose, peach and gold light is starting to glow. Deep "
        "navy-to-black sky with a few tiny stars, upper half of the image almost pure black. Minimal, elegant, "
        "premium tech keynote look. No text, no logos, no people, no boats, no buildings.")
ALBA = ("Slow cinematic sunrise. The sun rises gently from behind the volcano's crater, rose and golden light "
        "spreads across the sky and shimmers on the calm black sea, the stars fade. Very slow camera push-in. "
        "No people, no text, no new objects.")

def chiama(url, dati=None):
    corpo = json.dumps(dati).encode() if dati is not None else None
    req = urllib.request.Request(url, data=corpo, headers={
        "Authorization": "Key " + KEY, "Content-Type": "application/json", "User-Agent": "21labs-genera/1.0"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)

def scarica(url, nome):
    req = urllib.request.Request(url, headers={"User-Agent": "21labs-genera/1.0"})
    with urllib.request.urlopen(req, timeout=600) as r, open(os.path.join(OUT, nome), "wb") as f:
        f.write(r.read())
    print("  salvato", nome)

def immagine(nome, prompt, formato, risoluzione):
    if os.path.exists(os.path.join(OUT, nome + ".png")):
        return print("  già fatto", nome)
    print("Immagine:", nome)
    r = chiama(RUN + "/fal-ai/nano-banana-pro", {"prompt": prompt, "aspect_ratio": formato,
               "resolution": risoluzione, "num_images": 1, "output_format": "png"})
    url = r["images"][0]["url"]
    scarica(url, nome + ".png")
    with open(os.path.join(OUT, nome + ".url"), "w") as f:
        f.write(url)

def video(nome, immagine_url):
    if os.path.exists(os.path.join(OUT, nome + ".mp4")):
        return print("  già fatto", nome)
    print("Video:", nome, "(qualche minuto)")
    r = chiama(CODA + "/fal-ai/bytedance/seedance/v1.5/pro/image-to-video", {
        "prompt": ALBA, "image_url": immagine_url, "aspect_ratio": "16:9", "resolution": "1080p",
        "duration": "5", "camera_fixed": False, "generate_audio": False})
    while True:
        time.sleep(float(os.environ.get("FAL_ATTESA", "8")))
        stato = chiama(r["status_url"])["status"]
        if stato == "COMPLETED":
            break
        if stato not in ("IN_QUEUE", "IN_PROGRESS"):
            sys.exit("Video non riuscito: " + stato)
    scarica(chiama(r["response_url"])["video"]["url"], nome + ".mp4")

print("Spesa prevista: circa 1,95 $ (9 immagini a 0,15 $ + 2 video senza audio a circa 0,30 $).")
immagine("hero", HERO, "16:9", "2K")
for nome, oggetto in OGGETTI.items():
    immagine(nome, STILE + oggetto, "1:1", "1K")
hero_url = open(os.path.join(OUT, "hero.url")).read().strip()
video("alba-1", hero_url)
video("alba-2", hero_url)
print("Fatto. Trovi tutto nella cartella", OUT)
