#!/usr/bin/env python3
"""Build a local review board to pick the ZenityX Class app icon."""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/trin/.claude/skills/internal-board-builder/lib")
from url import furl, html_escape          # noqa: E402
from open_board import open_board          # noqa: E402

BASE = Path("/Volumes/Studio/projects/RustDeck/branding/icon-options")
OUT = Path("/Volumes/Studio/projects/RustDeck/branding/icon-board.html")

CARDS = [
    ("concept1-boldX-dark.png", "Concept 1 — Bold X (ดำ)",
     "X แดงเรขาคณิตคม บนพื้นดำ มินิมอลพรีเมียม อ่านเป็น 'แบรนด์มาร์ค' ชัด"),
    ("concept2-X-white.png", "Concept 2 — X บนพื้นขาว",
     "สะอาด สว่าง แต่ขาว+X แดง = อ่านเป็นปุ่ม close/error มากที่สุด generic"),
    ("concept3-X-monitor.png", "Concept 3 — X + จอมอนิเตอร์",
     "ตรง use case (remote desktop) แต่ 'X ทับจอ' = สื่อ disconnect/no-signal — แนะนำน้อยสุด"),
    ("concept4-connection.png", "Concept 4 — เส้นเชื่อมต่อ + โหนด",
     "นีออน X จากเส้น network link โหนดเรืองแสง เทคๆ distinctive (ขอบล่างซ้ายมี artifact เล็กน้อย)"),
    ("concept5-gradientX.png", "Concept 5 — Gradient X (glossy)",
     "X ไล่สีแดงเงา 3D สไตล์ macOS Big Sur ดูพรีเมียมสุด"),
]

cards_html = ""
for fn, title, note in CARDS:
    src = BASE / fn
    url = furl(src)
    cards_html += f"""
      <figure class="card">
        <img src="{url}" alt="{html_escape(title)}" loading="lazy"
             data-full="{url}" data-title="{html_escape(title)}" />
        <figcaption>
          <h3>{html_escape(title)}</h3>
          <p>{html_escape(note)}</p>
        </figcaption>
      </figure>"""

html = f"""<!doctype html>
<html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ZenityX Class — App Icon Options</title>
<style>
  :root {{ --red:#FF0000; --bg:#0d0d0d; --panel:#1a1a1a; --line:#2a2a2a; --txt:#eee; --mut:#9e9e9e; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--txt);
    font-family:-apple-system,BlinkMacSystemFont,"IBM Plex Sans Thai","Segoe UI",sans-serif; }}
  header {{ padding:32px 40px 12px; }}
  header h1 {{ margin:0; font-size:26px; font-weight:700; }}
  header h1 b {{ color:var(--red); }}
  header .sub {{ color:var(--mut); margin-top:6px; font-size:14px; }}
  .notes {{ margin:18px 40px; padding:16px 20px; background:var(--panel);
    border-left:4px solid var(--red); border-radius:8px; font-size:14px; line-height:1.6; }}
  .notes b {{ color:var(--red); }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
    gap:22px; padding:14px 40px 60px; }}
  .card {{ margin:0; background:var(--panel); border:1px solid var(--line);
    border-radius:14px; overflow:hidden; transition:transform .12s, border-color .12s; }}
  .card:hover {{ transform:translateY(-3px); border-color:var(--red); }}
  .card img {{ width:100%; aspect-ratio:1/1; object-fit:contain; background:#000;
    cursor:zoom-in; display:block; }}
  figcaption {{ padding:14px 16px; }}
  figcaption h3 {{ margin:0 0 6px; font-size:15px; }}
  figcaption p {{ margin:0; color:var(--mut); font-size:13px; line-height:1.5; }}
  /* modal */
  .ibb-modal {{ position:fixed; inset:0; background:rgba(0,0,0,.92);
    display:none; align-items:center; justify-content:center; z-index:999; cursor:zoom-out; }}
  .ibb-modal.open {{ display:flex; }}
  .ibb-modal img {{ max-width:94vw; max-height:88vh; object-fit:contain; }}
  .ibb-cap {{ position:fixed; bottom:22px; left:0; right:0; text-align:center;
    color:#fff; font-size:14px; }}
</style></head>
<body>
  <header>
    <h1>ZenityX <b>Class</b> — App Icon Options</h1>
    <div class="sub">5 คอนเซ็ปต์ · Nano Banana Pro · 4K square · คลิกที่ภาพเพื่อซูมเต็มจอ</div>
  </header>
  <div class="notes">
    ทั้ง 5 แบบคมใช้ได้จริงทั้งหมด · <b>ข้อสังเกต UX:</b> ตัว "X" สีแดงโดยทั่วไปคนอ่านเป็น
    error/close/delete — <b>แต่</b> X แดงคือลายเซ็นแบรนด์ ZenityX จริง จึง defensible ·
    <b>Concept 3</b> (X ทับจอ) สื่อ "disconnect/no-signal" แรงสุด → แนะนำน้อยที่สุด ·
    <b>Concept 1 / 4 / 5</b> อ่านเป็นแบรนด์มาร์คมากที่สุด
  </div>
  <div class="grid">{cards_html}
  </div>

  <div class="ibb-modal" id="modal" role="dialog" aria-modal="true">
    <img id="modal-img" alt="">
    <div class="ibb-cap" id="modal-cap"></div>
  </div>
  <script>
    (function() {{
      var modal = document.getElementById('modal');
      var mimg = document.getElementById('modal-img');
      var mcap = document.getElementById('modal-cap');
      document.querySelectorAll('.card img').forEach(function(img) {{
        img.addEventListener('click', function() {{
          mimg.src = img.getAttribute('data-full');
          mcap.textContent = img.getAttribute('data-title');  // XSS-safe
          modal.classList.add('open');
        }});
      }});
      function close() {{ modal.classList.remove('open'); mimg.src=''; }}
      modal.addEventListener('click', close);
      document.addEventListener('keydown', function(e) {{ if (e.key==='Escape') close(); }});
    }})();
  </script>
</body></html>"""

OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
open_board(OUT)
