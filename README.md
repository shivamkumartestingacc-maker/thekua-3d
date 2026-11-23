# Thekua 3D

Chhath Prasad page: gift box opens with falling marigold/rose petals, then a 3D thekua appears that turns with phone tilt (gyroscope) or drag.

- `index.html` — whole app (three.js from CDN, no build step).
- `assets/thekua-angles.webp` — source angle sheet; `front.png` / `back.png` / `front-cut.png` are cut from it by `python3 tools/make_textures.py`.

## Run

Motion sensors only work over **HTTPS** (or `localhost`). Easiest: enable GitHub Pages on this repo and open the Pages URL on the phone.

Local: `python3 -m http.server 8000`, open `http://localhost:8000`.

Android Chrome: tilt works with no prompt. Shake the phone on the first screen to open the box. iPhone: the "Open" tap asks for motion permission.
