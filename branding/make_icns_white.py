#!/usr/bin/env python3
"""White-background owl icon: extract owl from white gen, composite onto a clean white squircle, build .icns."""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

SRC = Path("/Volumes/Studio/projects/RustDeck/branding/owl-white/white-A-pure.png")
WORK = Path("/Volumes/Studio/projects/RustDeck/branding/icon-build-white")
ICONSET = WORK / "AppIcon.iconset"
WORK.mkdir(parents=True, exist_ok=True); ICONSET.mkdir(parents=True, exist_ok=True)

# 1) extract the owl: flood-fill white (canvas + white squircle + soft shadow) -> transparent.
#    owl is dark/red, far from white, so fill stops at the owl. internal eye/glasses whites are enclosed -> safe.
img = Image.open(SRC).convert("RGBA")
w, h = img.size
for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
    ImageDraw.floodfill(img, seed, (0, 0, 0, 0), thresh=170)
owl = img.crop(img.split()[3].getbbox())

# 2) build a clean white squircle canvas (Apple-style: ~7% outer transparent margin, ~22% corner radius).
S = 1024
margin = int(S * 0.07)
sq_box = (margin, margin, S - margin, S - margin)
radius = int((S - 2 * margin) * 0.225)
canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)
draw.rounded_rectangle(sq_box, radius=radius, fill=(255, 255, 255, 255),
                       outline=(224, 224, 224, 255), width=3)  # subtle hairline so it reads on white bg

# 3) scale owl to ~76% of the squircle inner width, center it (nudged up slightly).
inner = (S - 2 * margin)
target_w = int(inner * 0.76)
scale = target_w / owl.width
owl_r = owl.resize((target_w, int(owl.height * scale)), Image.LANCZOS)
ox = (S - owl_r.width) // 2
oy = (S - owl_r.height) // 2 - int(S * 0.01)
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
print("iconutil:", r.returncode, r.stderr.strip(), "| icns bytes:", icns.stat().st_size if icns.exists() else "MISSING")
