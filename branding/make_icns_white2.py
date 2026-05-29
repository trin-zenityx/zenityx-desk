#!/usr/bin/env python3
"""White-bg owl icon v2 — use rembg (AI segmentation) to cut the owl cleanly (no leftover box),
then composite onto a fresh white squircle. Fixes the double-box artifact."""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from rembg import remove

SRC = Path("/Volumes/Studio/projects/RustDeck/branding/owl-white/white-A-pure.png")
WORK = Path("/Volumes/Studio/projects/RustDeck/branding/icon-build-white")
ICONSET = WORK / "AppIcon.iconset"
WORK.mkdir(parents=True, exist_ok=True); ICONSET.mkdir(parents=True, exist_ok=True)

# 1) AI segmentation: cut the owl from the white background (semantic, not color-based -> no box leftover).
src_img = Image.open(SRC).convert("RGBA")
cut = remove(src_img)  # RGBA, background alpha=0
cut.save(WORK / "_owl_cut.png")
owl = cut.crop(cut.split()[3].getbbox())

# 2) clean white squircle (Apple-style margin + corner radius, subtle hairline edge).
S = 1024
margin = int(S * 0.07)
radius = int((S - 2 * margin) * 0.225)
canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(canvas)
d.rounded_rectangle((margin, margin, S - margin, S - margin), radius=radius,
                    fill=(255, 255, 255, 255), outline=(224, 224, 224, 255), width=3)

# 3) scale to ~72% of squircle inner width, then center by the owl's ALPHA CENTER-OF-MASS
#    (so the thin pointer doesn't skew placement — the heavy body lands dead center).
inner = S - 2 * margin
tw = int(inner * 0.72)
f = tw / owl.width
owl_r = owl.resize((tw, int(owl.height * f)), Image.LANCZOS)
a = np.array(owl_r.split()[3])
ys, xs = np.nonzero(a > 16)
cx, cy = xs.mean(), ys.mean()              # centroid in resized-owl coords
ox = round(S / 2 - cx)
oy = round(S / 2 - cy)
canvas.alpha_composite(owl_r, (ox, oy))
canvas.save(WORK / "master_white_1024.png")

# 4) iconset + icns
sizes = {"icon_16x16.png":16,"icon_16x16@2x.png":32,"icon_32x32.png":32,"icon_32x32@2x.png":64,
         "icon_128x128.png":128,"icon_128x128@2x.png":256,"icon_256x256.png":256,
         "icon_256x256@2x.png":512,"icon_512x512.png":512,"icon_512x512@2x.png":1024}
for name, px in sizes.items():
    canvas.resize((px, px), Image.LANCZOS).save(ICONSET / name)
icns = WORK / "AppIcon.icns"
r = subprocess.run(["iconutil","-c","icns",str(ICONSET),"-o",str(icns)], capture_output=True, text=True)
print("owl bbox:", owl.size, "| iconutil:", r.returncode, r.stderr.strip(), "| icns bytes:", icns.stat().st_size if icns.exists() else "MISSING")
