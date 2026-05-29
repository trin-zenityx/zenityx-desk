#!/usr/bin/env python3
"""White-bg owl icon v3 — restore DIMENSION: gradient squircle + soft contact shadow under the owl.
Reuses the clean rembg cutout (_owl_cut.png) so the owl keeps its own 3D shading, but the flat-white
background gets depth (top-lit gradient + grounding shadow + hairline edge)."""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

WORK = Path("/Volumes/Studio/projects/RustDeck/branding/icon-build-white")
ICONSET = WORK / "AppIcon.iconset"
ICONSET.mkdir(parents=True, exist_ok=True)

owl = Image.open(WORK / "_owl_cut.png").convert("RGBA")
owl = owl.crop(owl.split()[3].getbbox())

S = 1024
margin = int(S * 0.07)
radius = int((S - 2 * margin) * 0.225)
box = (margin, margin, S - margin, S - margin)

# rounded-square mask
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)

# top-lit vertical gradient (white -> very light cool gray) for subtle depth
top = np.array([255, 255, 255]); bot = np.array([233, 233, 238])
col = (top[None, :] * (1 - np.linspace(0, 1, S)[:, None]) + bot[None, :] * np.linspace(0, 1, S)[:, None]).astype(np.uint8)
grad = np.repeat(col[:, None, :], S, axis=1)
grad_img = Image.fromarray(grad, "RGB").convert("RGBA")

canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
canvas.paste(grad_img, (0, 0), mask)

# scale owl to ~72% inner width, center by alpha centroid
inner = S - 2 * margin
tw = int(inner * 0.72)
owl_r = owl.resize((tw, int(owl.height * tw / owl.width)), Image.LANCZOS)
oa = np.array(owl_r.split()[3])
ys, xs = np.nonzero(oa > 16)
ox = round(S / 2 - xs.mean()); oy = round(S / 2 - ys.mean())

# soft contact shadow: owl silhouette, dark, blurred, nudged down, low opacity, clipped to squircle
shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
dark = Image.new("RGBA", owl_r.size, (35, 30, 45, 255)); dark.putalpha(owl_r.split()[3])
shadow.alpha_composite(dark, (ox, oy + int(S * 0.018)))
shadow = shadow.filter(ImageFilter.GaussianBlur(S * 0.02))
sa = shadow.split()[3].point(lambda p: int(p * 0.30))          # 30% opacity
sa = ImageChops.multiply(sa, mask)                              # keep shadow inside the squircle
shadow.putalpha(sa)
canvas.alpha_composite(shadow)

# owl on top
canvas.alpha_composite(owl_r, (ox, oy))

# subtle hairline edge so the squircle reads on white backgrounds
ImageDraw.Draw(canvas).rounded_rectangle(box, radius=radius, outline=(210, 210, 216, 255), width=3)

canvas.save(WORK / "master_white_1024.png")

sizes = {"icon_16x16.png":16,"icon_16x16@2x.png":32,"icon_32x32.png":32,"icon_32x32@2x.png":64,
         "icon_128x128.png":128,"icon_128x128@2x.png":256,"icon_256x256.png":256,
         "icon_256x256@2x.png":512,"icon_512x512.png":512,"icon_512x512@2x.png":1024}
for name, px in sizes.items():
    canvas.resize((px, px), Image.LANCZOS).save(ICONSET / name)
icns = WORK / "AppIcon.icns"
r = subprocess.run(["iconutil","-c","icns",str(ICONSET),"-o",str(icns)], capture_output=True, text=True)
print("iconutil:", r.returncode, r.stderr.strip(), "| icns bytes:", icns.stat().st_size if icns.exists() else "MISSING")
