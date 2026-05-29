#!/usr/bin/env python3
"""White-bg owl icon v5 — same direct-crop (no subject cutout, keeps AI dimension) but with
4x SUPERSAMPLED rounded-corner masking + hairline so the edges are smooth/anti-aliased."""
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

# autocrop pure-white canvas -> squircle bbox
nonwhite = np.any(arr < 246, axis=2)
ys, xs = np.nonzero(nonwhite)
sq = img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
w, h = sq.size
side = max(w, h)
sqr = Image.new("RGBA", (side, side), (255, 255, 255, 255))
sqr.paste(sq, ((side - w) // 2, (side - h) // 2), sq)

# --- work at 4x for smooth (anti-aliased) edges, then downsample once ---
SS = 4
S = 1024 * SS                      # 4096 working canvas
margin = int(S * 0.06)
inner = S - 2 * margin
radius = int(inner * 0.225)

sqr = sqr.resize((inner, inner), Image.LANCZOS)
cmask = Image.new("L", (inner, inner), 0)
ImageDraw.Draw(cmask).rounded_rectangle((0, 0, inner - 1, inner - 1), radius=radius, fill=255)
sqr.putalpha(cmask)                 # mask edge = the icon edge everywhere -> uniform smooth boundary

big = Image.new("RGBA", (S, S), (0, 0, 0, 0))
big.alpha_composite(sqr, (margin, margin))
ImageDraw.Draw(big).rounded_rectangle((margin, margin, S - margin - 1, S - margin - 1),
                                      radius=radius, outline=(206, 206, 212, 255), width=SS * 3)

# downsample the whole composite -> anti-aliased corners, sides, and hairline
master = big.resize((1024, 1024), Image.LANCZOS)
master.save(WORK / "master_white_1024.png")

sizes = {"icon_16x16.png":16,"icon_16x16@2x.png":32,"icon_32x32.png":32,"icon_32x32@2x.png":64,
         "icon_128x128.png":128,"icon_128x128@2x.png":256,"icon_256x256.png":256,
         "icon_256x256@2x.png":512,"icon_512x512.png":512,"icon_512x512@2x.png":1024}
for name, px in sizes.items():
    big.resize((px, px), Image.LANCZOS).save(ICONSET / name)   # each size downsampled from 4096 = crisp
icns = WORK / "AppIcon.icns"
r = subprocess.run(["iconutil","-c","icns",str(ICONSET),"-o",str(icns)], capture_output=True, text=True)
print("sq:", sq.size, "| iconutil:", r.returncode, r.stderr.strip(), "| bytes:", icns.stat().st_size if icns.exists() else "MISSING")
