#!/usr/bin/env python3
"""Review board to pick the ZenityX Class mascot app icon."""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/trin/.claude/skills/internal-board-builder/lib")
from url import furl, html_escape          # noqa: E402
from open_board import open_board          # noqa: E402

BASE = Path("/Volumes/Studio/projects/RustDeck/branding/mascot-options")
OUT = Path("/Volumes/Studio/projects/RustDeck/branding/mascot-board.html")

CARDS = [
    ("m1-robot.png", "1 — หุ่นยนต์ AI", "★ เต็ง — chibi robot ขาว+แดงแบรนด์ ตายิ้มเรืองแสง หน้าจอบนตัว subtly สื่อ screen พรีเมียมสุด", True),
    ("m5-screen.png", "5 — หุ่นอุ้มจอ", "★ เต็ง — หุ่นน่ารัก + ถือจอเรืองแสง = แชร์จอสอนตรงเป๊ะ + หัวใจแดง story ดีสุดสำหรับ use case", True),
    ("m3-owl.png", "3 — นกฮูกครู", "กลิ่น 'ครู/สถาบันสอน' ชัดสุด แดงแบรนด์เด่น ถือไม้ชี้ — เหมาะถ้าอยากเน้น education identity", False),
    ("m2-monitor.png", "2 — มอนิเตอร์มีหน้า", "สื่อ 'จอ/screen control' ตรงสุด น่ารักมาก แต่พื้นฟ้า + แดงแค่ปุ่ม power (แบรนด์เบา)", False),
    ("m4-fox.png", "4 — จิ้งจอก", "น่ารักสุดในเชิงตัวการ์ตูน แต่ off-theme (ไม่โยงกับ remote/teaching) + สีส้มไม่ใช่แดงแบรนด์", False),
]

cards_html = ""
for fn, title, note, fav in CARDS:
    url = furl(BASE / fn)
    star = " fav" if fav else ""
    cards_html += f"""
      <figure class="card{star}">
        <img src="{url}" alt="{html_escape(title)}" loading="lazy"
             data-full="{url}" data-title="{html_escape(title)}" />
        <figcaption><h3>{html_escape(title)}</h3><p>{html_escape(note)}</p></figcaption>
      </figure>"""

html = f"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ZenityX Class — Mascot Options</title><style>
 :root {{ --red:#FF0000; --bg:#0d0d0d; --panel:#1a1a1a; --line:#2a2a2a; --txt:#eee; --mut:#9e9e9e; }}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--txt);
   font-family:-apple-system,BlinkMacSystemFont,"IBM Plex Sans Thai","Segoe UI",sans-serif}}
 header{{padding:32px 40px 12px}} header h1{{margin:0;font-size:26px;font-weight:700}}
 header h1 b{{color:var(--red)}} header .sub{{color:var(--mut);margin-top:6px;font-size:14px}}
 .notes{{margin:18px 40px;padding:16px 20px;background:var(--panel);border-left:4px solid var(--red);
   border-radius:8px;font-size:14px;line-height:1.6}} .notes b{{color:var(--red)}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px;padding:14px 40px 60px}}
 .card{{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;
   transition:transform .12s,border-color .12s}} .card:hover{{transform:translateY(-3px);border-color:var(--red)}}
 .card.fav{{border-color:var(--red);box-shadow:0 0 0 1px var(--red)}}
 .card img{{width:100%;aspect-ratio:1/1;object-fit:contain;background:#000;cursor:zoom-in;display:block}}
 figcaption{{padding:14px 16px}} figcaption h3{{margin:0 0 6px;font-size:15px}}
 figcaption p{{margin:0;color:var(--mut);font-size:13px;line-height:1.5}}
 .ibb-modal{{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;
   justify-content:center;z-index:999;cursor:zoom-out}} .ibb-modal.open{{display:flex}}
 .ibb-modal img{{max-width:94vw;max-height:88vh;object-fit:contain}}
 .ibb-cap{{position:fixed;bottom:22px;left:0;right:0;text-align:center;color:#fff;font-size:14px}}
</style></head><body>
 <header><h1>ZenityX <b>Class</b> — Mascot Options</h1>
 <div class="sub">5 ทิศทางมาสคอต · Nano Banana Pro · 4K square · คลิกซูม · เรียงตามที่ผมแนะนำ</div></header>
 <div class="notes">ทุกตัวน่ารักใช้ได้จริง · <b>ผมแนะนำ #1 (หุ่นยนต์)</b> หรือ <b>#5 (หุ่นอุ้มจอ)</b> —
   เป็นหุ่นแดงแบรนด์ ZenityX, #5 มี story "แชร์จอสอน" ตรง use case ที่สุด ·
   <b>#3 นกฮูก</b> ดีถ้าอยากเน้น identity ครู/สถาบัน · เลือกได้เลยครับ แล้วผมจะรีไฟน์ตัวนั้นต่อ + ทำเป็น .icns</div>
 <div class="grid">{cards_html}
 </div>
 <div class="ibb-modal" id="modal" role="dialog" aria-modal="true"><img id="modal-img" alt=""><div class="ibb-cap" id="modal-cap"></div></div>
 <script>(function(){{var m=document.getElementById('modal'),i=document.getElementById('modal-img'),c=document.getElementById('modal-cap');
  document.querySelectorAll('.card img').forEach(function(x){{x.addEventListener('click',function(){{i.src=x.getAttribute('data-full');c.textContent=x.getAttribute('data-title');m.classList.add('open');}});}});
  function cl(){{m.classList.remove('open');i.src='';}} m.addEventListener('click',cl);
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')cl();}});}})();</script>
</body></html>"""

OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
open_board(OUT)
