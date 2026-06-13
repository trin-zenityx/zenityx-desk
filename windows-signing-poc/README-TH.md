# ZenityX Desk — ทดสอบ Code Signing (Self-Signed PoC)

**เป้าหมาย:** พิสูจน์บนเครื่อง Windows ของทีมว่า *พอเซ็นไฟล์ + เครื่องเชื่อ cert แล้ว อาการเตือน/Bad Image หายไหม* — ก่อนตัดสินใจลงเงินซื้อ cert จริง หรือทำ Microsoft Store

> ⚠️ **ใช้ทดสอบภายในเท่านั้น** — self-signed cert เชื่อถือได้เฉพาะเครื่องที่ติดตั้ง cert นี้ ห้ามใช้แจกผู้ใช้จริง

---

## วิธีใช้ (เครื่อง Windows ที่เจอปัญหา)

1. **ปิดแอป ZenityX Desk ให้สนิทก่อน** (ไม่งั้นจะเซ็น .dll ที่กำลังถูกใช้อยู่ไม่ได้)
2. โหลดแอปตามปกติ แล้วแตก zip → จะได้โฟลเดอร์ที่มี `rustdesk.exe` + ไฟล์ `*_plugin.dll`
3. วางไฟล์ **`sign-poc.ps1`** ลงใน **โฟลเดอร์เดียวกับ `rustdesk.exe`**
4. คลิกขวาที่ `sign-poc.ps1` → **Run with PowerShell**
   - ถ้าโดนบล็อก execution policy ให้เปิด **PowerShell (Admin)** แล้วพิมพ์:
     ```powershell
     powershell -ExecutionPolicy Bypass -File "C:\path\to\sign-poc.ps1"
     ```
   - กด **Yes** ตอนหน้าต่าง UAC ขอสิทธิ์ Administrator
5. รอจนเห็น **สรุป** (เซ็นสำเร็จกี่ไฟล์ + สถานะ Smart App Control)
6. **ดับเบิลคลิก `rustdesk.exe`** แล้วสังเกตผล 👇

---

## อ่านผล

| สิ่งที่เห็นหลังเซ็น | แปลว่า | ทางแก้จริง |
|---|---|---|
| ✅ เปิดได้เลย ไม่มี Bad Image / ไม่มี "Unknown Publisher" | ปัญหาคือ **signature ธรรมดา** | ซื้อ **OV cert (~$116/ปี)** แล้วเซ็นใน CI = จบ |
| ⚠️ ยังขึ้น **"Smart App Control"** บล็อก (เหมือนเดิม) | ตัวการคือ **SAC** — self-signed/cert ธรรมดาเอาไม่อยู่วันแรก | **Microsoft Store (MSIX)** หรือปิด SAC |

> สรุปในสคริปต์จะบอก **สถานะ Smart App Control** ให้ด้วย:
> - `ปิดอยู่ (Off)` → ถ้ายังเซ็นแล้วหายเตือน = signature ธรรมดาเอาอยู่
> - `เปิดเต็ม (Enforcement)` → ถ้ายังบล็อก = ยืนยันว่า SAC คือปัญหา

### อยากลองปิด Smart App Control เพื่อเทียบ (ทางเลือก)
Windows Security → **App & browser control** → **Smart App Control** → **Off**

> ⚠️ **ปิดแล้วเปิดกลับไม่ได้** จนกว่าจะลง Windows ใหม่ — ทำเฉพาะเครื่องเทสต์เท่านั้น

---

## เลิกทดสอบ / คืนเครื่องให้เหมือนเดิม

รัน **`unsign-poc.ps1`** (คลิกขวา → Run with PowerShell) — จะลบ cert ออกจากเครื่อง
ลายเซ็นบนไฟล์ยังอยู่แต่จะไม่ถูกเชื่อถืออีก (ไม่มีผลเสีย)

---

## สิ่งที่ PoC นี้บอกเราได้

- ถ้า **เซ็นแล้วหาย** → ลงทุน cert จริงคุ้ม จบปัญหาแน่นอน (ทางถูก = OV cloud cert)
- ถ้า **เซ็นแล้วยังโดน SAC** → ยืนยันว่าต้องไป **Microsoft Store (MSIX)** ซึ่ง Microsoft เซ็นให้
  เป็นทางเดียวที่ผ่าน SAC วันแรกโดยไม่ต้องปิด SAC

> หมายเหตุ: cert จริง (OV/EV) ก็ต้อง "สะสมชื่อเสียง" กับ SAC สักพักเช่นกัน —
> ถ้า PoC บอกว่า SAC คือกำแพง **Microsoft Store คือคำตอบที่ตรงที่สุด**
