#!/usr/bin/env python3
"""Turn the chosen owl render into a clean macOS AppIcon.icns + a transparent master."""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

SRC = Path("/Volumes/Studio/projects/RustDeck/branding/owl-v2/owl-v2-1-raised.png")
WORK = Path("/Volumes/Studio/projects/RustDeck/branding/icon-build")
ICONSET = WORK / "AppIcon.iconset"
WORK.mkdir(parents=True, exist_ok=True)
ICONSET.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC).convert("RGBA")
w, h = img.size

# 1) flood-fill the white background (and its soft shadow) to transparent, from all 4 corners.
#    high thresh eats the light shadow gradient; the dark squircle edge is far from white so fill stops there.
for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
    ImageDraw.floodfill(img, seed, (0, 0, 0, 0), thresh=200)

# 2) autocrop to the non-transparent bounding box (the squircle).
alpha = img.split()[3]
bbox = alpha.getbbox()
sub = img.crop(bbox)
sw, sh = sub.size
side = max(sw, sh)

# 3) pad onto a square canvas with ~9% margin (Apple macOS icon convention).
margin = int(side * 0.09)
canvas_side = side + margin * 2
master = Image.new("RGBA", (canvas_side, canvas_side), (0, 0, 0, 0))
master.paste(sub, ((canvas_side - sw) // 2, (canvas_side - sh) // 2), sub)

# keep a 1024 transparent master for later (ico / linux / tray)
master_1024 = master.resize((1024, 1024), Image.LANCZOS)
master_1024.save(WORK / "master_1024.png")

# 4) generate the .iconset
sizes = {
    "icon_16x16.png": 16, "icon_16x16@2x.png": 32,
    "icon_32x32.png": 32, "icon_32x32@2x.png": 64,
    "icon_128x128.png": 128, "icon_128x128@2x.png": 256,
    "icon_256x256.png": 256, "icon_256x256@2x.png": 512,
    "icon_512x512.png": 512, "icon_512x512@2x.png": 1024,
}
for name, px in sizes.items():
    master.resize((px, px), Image.LANCZOS).save(ICONSET / name)

# 5) iconutil -> .icns
icns = WORK / "AppIcon.icns"
r = subprocess.run(["iconutil", "-c", "icns", str(ICONSET), "-o", str(icns)],
                   capture_output=True, text=True)
print("iconutil:", r.returncode, r.stderr.strip())
print("crop bbox:", bbox, "-> master", master.size, "icns:", icns, icns.stat().st_size if icns.exists() else "MISSING")
