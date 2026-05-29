#!/usr/bin/env python3
"""White-bg owl icon v4 — use the GENERATED image directly (keeps the AI's native depth/shading/shadows).
Just: autocrop the outer white canvas to the squircle, square it, round the corners to transparent,
add a small Apple-style margin. No subject cutout, no synthetic background -> full original dimension."""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

SRC = Path("/Volumes/Studio/projects/RustDeck/branding/owl-white/white-A-pure.png")
WORK = Path("/Volumes/Studio/projects/RustDeck/branding/icon-build-white")
ICONSET = WORK / "AppIcon.iconset"
ICONSET.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC).convert("RGBA")
arr = np.array(img)[:, :, :3].astype(int)

# 1) autocrop the pure-white canvas margin -> bounding box of the squircle (its edge/shadow/owl).
nonwhite = np.any(arr < 246, axis=2)
ys, xs = np.nonzero(nonwhite)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
sq = img.crop((x0, y0, x1 + 1, y1 + 1))

# 2) pad to a centered square (extend with white so nothing is distorted; corners get clipped anyway).
w, h = sq.size
side = max(w, h)
sqr = Image.new("RGBA", (side, side), (255, 255, 255, 255))
sqr.paste(sq, ((side - w) // 2, (side - h) // 2), sq)

# 3) resize squircle to the "inner" size, round its corners, place on transparent canvas w/ small margin.
S = 1024
margin = int(S * 0.06)
inner = S - 2 * margin
sqr = sqr.resize((inner, inner), Image.LANCZOS)

radius = int(inner * 0.225)
cmask = Image.new("L", (inner, inner), 0)
ImageDraw.Draw(cmask).rounded_rectangle((0, 0, inner - 1, inner - 1), radius=radius, fill=255)
sqr.putalpha(cmask)  # transparent rounded corners

canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
canvas.alpha_composite(sqr, (margin, margin))
# subtle hairline so the white squircle reads on white backgrounds
ImageDraw.Draw(canvas).rounded_rectangle((margin, margin, S - margin - 1, S - margin - 1),
                                         radius=radius, outline=(208, 208, 214, 255), width=3)
canvas.save(WORK / "master_white_1024.png")

sizes = {"icon_16x16.png":16,"icon_16x16@2x.png":32,"icon_32x32.png":32,"icon_32x32@2x.png":64,
         "icon_128x128.png":128,"icon_128x128@2x.png":256,"icon_256x256.png":256,
         "icon_256x256@2x.png":512,"icon_512x512.png":512,"icon_512x512@2x.png":1024}
for name, px in sizes.items():
    canvas.resize((px, px), Image.LANCZOS).save(ICONSET / name)
icns = WORK / "AppIcon.icns"
r = subprocess.run(["iconutil","-c","icns",str(ICONSET),"-o",str(icns)], capture_output=True, text=True)
print("crop bbox:", (x0, y0, x1, y1), "sq:", sq.size, "| iconutil:", r.returncode, r.stderr.strip(), "| bytes:", icns.stat().st_size if icns.exists() else "MISSING")
