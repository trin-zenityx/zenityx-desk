# ZenityX Desk — Morning Brief (overnight work 2026-05-29)

> สรุปงานที่ทำคืนนี้ขณะคุณนอน + วิธีใช้ + จุดที่ต้องตัดสินใจ

## TL;DR
จากโฟลเดอร์ว่าง → **แอป remote desktop แบรนด์ ZenityX ที่ build + รัน + เชื่อม server ของเราเองได้จริง** ครบวงจร ใน 1 คืน
- ✅ แอป **ZenityX Desk** (macOS, ไอคอนนกฮูกครูพื้นขาว) build จาก source สำเร็จ
- ✅ Self-host **server** บน VPS ของคุณ (194.233.69.204) รันอยู่
- ✅ **ยืนยันแล้ว**: แอปลงทะเบียนกับ server เราจริง (เห็นใน log, ได้ ID `334921886`)
- ✅ Server ฝังเป็น default ในแอป → เปิดแอปปุ๊บใช้ server เราเลย ไม่ต้องตั้งเอง

## ทำงานยังไง (1:1 teaching)
RustDesk = ครูกับนักเรียนต่างก็ลงแอป ZenityX Desk แล้วเชื่อมกันผ่าน server เรา
1. นักเรียนเปิดแอป → เห็น **ID** (เลข 9 หลัก) + รหัสผ่านชั่วคราว
2. นักเรียนส่ง ID+รหัสให้ครู (หรือครูตั้ง unattended password ไว้ล่วงหน้าสำหรับนักเรียนประจำ)
3. ครูใส่ ID นักเรียน → กดเชื่อม → ใส่รหัส → **คุมจอนักเรียนได้เลย**
- ทุกการเชื่อมวิ่งผ่าน relay บน VPS เรา (data อยู่ในมือเราเอง ไม่ผ่าน server ทางการ RustDesk)

## สถานะรายชิ้น
| ส่วน | สถานะ |
|---|---|
| Toolchain (Rust 1.81, Flutter 3.24.5, vcpkg, ffmpeg ฯลฯ) บน SSD | ✅ `/Volumes/Studio/toolchains/` |
| Branding: ชื่อ "ZenityX Desk" + ไอคอนนกฮูกพื้นขาว + APP_NAME | ✅ |
| macOS client build + run | ✅ `flutter/build/macos/Build/Products/Release/ZenityX Desk.app` |
| Self-host server (hbbs+hbbr, Docker) | ✅ VPS 194.233.69.204 |
| เชื่อม client↔server (end-to-end) | ✅ ยืนยันแล้ว |
| ไอคอน Windows/Linux (res/icon.ico) | ✅ เตรียมพร้อม build |
| DMG installer (Mac) | ✅ `ZenityX-Desk.dmg` (26MB, ลากลง Applications ได้) |
| Git commit (preserve work) | ✅ branch `zenityx` (local, ยังไม่ push) |
| **Windows client** | ⏳ ยังไม่ได้ build (build บน Mac ไม่ได้ — ดู "ต้องตัดสินใจ") |
| **Code-signing เพื่อแจก** | ⏳ ยัง ad-hoc (รันเฉพาะเครื่องนี้) |

## ⚠️ ต้องตัดสินใจ/ทำเอง (ผมไม่ทำข้ามคืน)
1. **Windows client** — นักเรียนส่วนใหญ่ใช้ Windows แต่ **build Windows บน Mac ไม่ได้** ตัวเลือก:
   - (ก) ดันโค้ดขึ้น GitHub repo (private ได้) แล้วใช้ GitHub Actions build Windows ให้ (repo มี workflow อยู่แล้ว) — ผมเตรียม workflow ไว้ให้ แต่ยังไม่ push (รอคุณอนุญาต push)
   - (ข) หาเครื่อง Windows + build ตามสูตร
   - branding (ชื่อ/server/ไอคอน) ฝังในโค้ดแล้ว → Windows build จะได้แบรนด์เลย
2. **Code-signing** — ตอนนี้ ad-hoc แจกคนอื่นไม่ได้ (Gatekeeper บล็อก)
   - Mac: ต้อง Apple Developer ID ($99/ปี) + notarize
   - Windows: code-signing cert (ถ้าจะเลี่ยง SmartScreen warning)
3. **bundle id** ยังเป็น `com.carriez.rustdesk` (ไม่โชว์ผู้ใช้ ผูกกับ TCC permission — เปลี่ยนได้แต่ permission reset)
4. **License (AGPL)** — ถ้าแจก binary ให้นักเรียน ต้องเปิด source ที่แก้ให้เขาเข้าถึงได้ด้วย (เช่น repo + ลิงก์ในแอป)

## วิธี rebuild (Mac) — เร็ว, cargo incremental
```bash
cd /Volumes/Studio/projects/RustDeck
source setup-env.sh                 # โหลด toolchain จาก SSD
export PATH="/opt/homebrew/bin:$PATH"
export LIBCLANG_PATH="$(xcode-select -p)/Toolchains/XcodeDefault.xctoolchain/usr/lib"
python3 build.py --flutter --hwcodec --unix-file-copy-paste
# แล้ว ad-hoc sign เพื่อรัน local:
APP="flutter/build/macos/Build/Products/Release/ZenityX Desk.app"
codesign --force --deep --sign - --entitlements /tmp/zenityx_local.entitlements "$APP"
open "$APP"
```

## จัดการ Server (VPS 194.233.69.204)
```bash
ssh root@194.233.69.204
cd /opt/rustdesk-server
docker compose ps          # ดูสถานะ
docker compose logs hbbs   # ดู log การเชื่อม
docker compose restart     # รีสตาร์ท
# Public key (ฝังในแอปแล้ว): FbQAPxazoUCGASq4M16Phxpm6csaoZr7xcR1JTahjyg=
```
- พอร์ตที่เปิด (ufw): TCP 21114-21119, UDP 21116
- ⚠️ บน VPS มี **Caddy** (80/443) + service พอร์ต 4000 ของคุณอยู่ — RustDesk แยกพอร์ต ไม่กระทบกัน

## ไฟล์สำคัญ
- โปรเจค: `/Volumes/Studio/projects/RustDeck/`
- แอปที่ build: `flutter/build/macos/Build/Products/Release/ZenityX Desk.app`
- ไอคอน (สคริปต์): `branding/make_icns_crop2.py` (จาก `branding/owl-white/white-A-pure.png`)
- ตัวเลือกไอคอนทั้งหมด: `branding/*-board.html` (เปิดดูได้)
- จุดแก้ branding: `libs/hbb_common/src/config.rs` (server, key, APP_NAME), `flutter/macos/Runner/Configs/AppInfo.xcconfig` (ชื่อ macОС), `flutter/macos/Runner/AppIcon.icns`

## ✅ ทำเสร็จคืนนี้ (สรุป)
1. แอป **ZenityX Desk** rebrand เต็ม (ชื่อแอป/title/APP_NAME + ไอคอนนกฮูกพื้นขาวขอบเนียน) build + รัน
2. **Server** บน VPS รัน + **ยืนยัน e2e** (แอปลงทะเบียน ID `334921886` กับ hbbs เรา 2 ครั้ง)
3. ฝัง server เป็น default ในแอป (เปิดมาใช้ได้เลย)
4. **DMG installer**: `/Volumes/Studio/projects/RustDeck/ZenityX-Desk.dmg`
5. ไอคอน Windows/Linux (`res/icon.ico` ฯลฯ) พร้อมสำหรับ build ข้ามแพลตฟอร์ม
6. เก็บงานลง git branch **`zenityx`** (master ไม่แตะ)

## 🌅 เช้านี้คุยอะไรต่อ (เรียงตามสำคัญ)
1. **ทดสอบจริง 2 เครื่อง** — ต้องมีเครื่องที่ 2 (หรือลองเชื่อมจากมือถือ/เครื่องอื่น) เพื่อพิสูจน์ครูคุมจอนักเรียนได้
2. **Windows client** — ตัดสินใจ: push ขึ้น GitHub (private) ให้ CI build ให้ ✋(รออนุญาต push) หรือหาเครื่อง Windows
3. **Signing เพื่อแจก** — Apple Developer ID + (Windows cert) — ต้องใช้บัญชี/งบของคุณ
4. ลองเปิดแอป ZenityX Desk ดู UI เต็มๆ ว่าอยากปรับอะไรอีก (เช่น default settings, ซ่อนเมนูบางอัน, ตั้ง unattended password flow สำหรับนักเรียนประจำ)

---
_ทำเสร็จข้ามคืน 2026-05-29 ~05:10. แอปล่าสุดเปิดทิ้งไว้ให้ดู — ลองกดเล่นได้เลยครับ_
