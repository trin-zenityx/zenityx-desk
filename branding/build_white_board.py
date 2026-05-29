#!/usr/bin/env python3
"""Review board: owl mascot on white vs cream for ZenityX Desk icon."""
import sys
from pathlib import Path
sys.path.insert(0, "/Users/trin/.claude/skills/internal-board-builder/lib")
from url import furl, html_escape          # noqa: E402
from open_board import open_board          # noqa: E402

BASE = Path("/Volumes/Studio/projects/RustDeck/branding/owl-white")
DARK = Path("/Volumes/Studio/projects/RustDeck/branding/owl-v2/owl-v2-1-raised.png")
OUT = Path("/Volumes/Studio/projects/RustDeck/branding/white-board.html")

CARDS = [
    ("white-A-pure.png", str(BASE), "A — พื้นขาวล้วน", "★ ขาวสว่าง #FFFFFF คมสุด นกฮูกเด่น สื่อการศึกษาชัด", True),
    ("white-B-cream.png", str(BASE), "B — ครีมนุ่ม", "off-white อุ่น มีขอบเทาบางๆ ดูพรีเมียม", True),
    ("owl-v2-1-raised.png", str(DARK.parent), "เดิม — พื้นดำ", "ตัวเดิมที่ build ไปแล้ว (เผื่อเทียบ)", False),
]
cards = ""
for fn, base, title, note, fav in CARDS:
    url = furl(Path(base) / fn)
    cards += f"""<figure class="card{' fav' if fav else ''}"><img src="{url}" alt="{html_escape(title)}" loading="lazy" data-full="{url}" data-title="{html_escape(title)}"><figcaption><h3>{html_escape(title)}</h3><p>{html_escape(note)}</p></figcaption></figure>"""

html = f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ZenityX Desk — Icon BG</title><style>
 :root{{--red:#FF0000;--bg:#0d0d0d;--panel:#1a1a1a;--line:#2a2a2a;--txt:#eee;--mut:#9e9e9e}}
 *{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,"IBM Plex Sans Thai",sans-serif}}
 header{{padding:32px 40px 12px}}h1{{margin:0;font-size:26px;font-weight:700}}h1 b{{color:var(--red)}}.sub{{color:var(--mut);margin-top:6px;font-size:14px}}
 .notes{{margin:18px 40px;padding:16px 20px;background:var(--panel);border-left:4px solid var(--red);border-radius:8px;font-size:14px;line-height:1.6}}.notes b{{color:var(--red)}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px;padding:14px 40px 60px}}
 .card{{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;transition:transform .12s,border-color .12s}}.card:hover{{transform:translateY(-3px);border-color:var(--red)}}
 .card.fav{{border-color:var(--red);box-shadow:0 0 0 1px var(--red)}}
 .card img{{width:100%;aspect-ratio:1/1;object-fit:contain;background:#f3f3f3;cursor:zoom-in;display:block}}
 figcaption{{padding:14px 16px}}figcaption h3{{margin:0 0 6px;font-size:15px}}figcaption p{{margin:0;color:var(--mut);font-size:13px}}
 .ibb-modal{{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:999;cursor:zoom-out}}.ibb-modal.open{{display:flex}}
 .ibb-modal img{{max-width:94vw;max-height:88vh;object-fit:contain}}.ibb-cap{{position:fixed;bottom:22px;left:0;right:0;text-align:center;color:#fff;font-size:14px}}
</style></head><body>
 <header><h1>ZenityX <b>Desk</b> — ไอคอนพื้นขาว</h1><div class="sub">นกฮูกครู (ตัวเดิม) บนพื้นสว่าง · คลิกซูม</div></header>
 <div class="notes">พื้นสว่างสื่อการศึกษาดีกว่าพื้นดำตามที่คุณบอก · <b>A ขาวล้วน</b> คมสว่างสุด · <b>B ครีม</b> อุ่นพรีเมียม · เลือก A/B ได้เลย</div>
 <div class="grid">{cards}</div>
 <div class="ibb-modal" id="modal" role="dialog" aria-modal="true"><img id="modal-img" alt=""><div class="ibb-cap" id="modal-cap"></div></div>
 <script>(function(){{var m=document.getElementById('modal'),i=document.getElementById('modal-img'),c=document.getElementById('modal-cap');document.querySelectorAll('.card img').forEach(function(x){{x.addEventListener('click',function(){{i.src=x.getAttribute('data-full');c.textContent=x.getAttribute('data-title');m.classList.add('open');}});}});function cl(){{m.classList.remove('open');i.src='';}}m.addEventListener('click',cl);document.addEventListener('keydown',function(e){{if(e.key==='Escape')cl();}});}})();</script>
</body></html>"""
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT}")
open_board(OUT)
