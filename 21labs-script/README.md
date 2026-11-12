# Script 21Labs

- `genera.py`: prima generazione su fal.ai (hero, 8 oggetti, 2 video). Uso: `FAL_KEY=... python3 genera.py`
- `genera2.py`: ritocco delle immagini in chiave scura e petrolio. Uso: `OUT=21labs-media/v3 STILE=figo FAL_KEY=... python3 genera2.py ecommerce vetrina ...`
- `logo.py`: crea gli SVG del logo (servono `fonttools` e i font Anton in WOFF).
- `stampa.py` + `stampa.js`: creano biglietto e adesivi in PDF con QR (servono `segno` e Playwright).
- `svg2png.js`: converte un SVG in PNG.

La chiave fal.ai non è salvata da nessuna parte: si passa solo come variabile d'ambiente `FAL_KEY`.
Gli script saltano i file già generati, quindi rilanciarli non costa.
