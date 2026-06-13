#requires -version 5.1
<#
  ZenityX Desk — Windows code-signing PoC (self-signed)
  ------------------------------------------------------
  พิสูจน์ว่า "พอเซ็น + เครื่องเชื่อ cert แล้ว ไฟล์หายเตือนไหม" ก่อนตัดสินใจ
  ซื้อ cert จริง / ลง Microsoft Store

  สคริปต์นี้จะ:
    1) สร้าง self-signed code-signing certificate (ถ้ายังไม่มี)
    2) ติดตั้ง cert เข้า Trusted Root + Trusted Publisher ของ"เครื่องนี้"
    3) เซ็น rustdesk.exe และ .dll ที่ "ยังไม่ได้เซ็น" ทุกตัวในโฟลเดอร์แอป
       (ข้าม DLL ที่ Microsoft เซ็นมาแล้ว เช่น vcruntime — ไม่ทับลายเซ็นเดิม)
    4) รายงานสถานะ Smart App Control

  ⚠ ใช้ทดสอบภายในเท่านั้น — self-signed เชื่อถือได้เฉพาะเครื่องที่ติดตั้ง cert นี้
     ห้ามใช้แจกจริงต่อสาธารณะ
#>

[CmdletBinding()]
param(
  # โฟลเดอร์แอป (ค่าเริ่มต้น = โฟลเดอร์ที่วางสคริปต์นี้ไว้)
  [string]$AppPath = $PSScriptRoot
)

$ErrorActionPreference = 'Stop'

$CertSubject   = 'CN=ZenityX Desk (Self-Signed PoC)'
$CertFriendly  = 'ZenityX Desk PoC Code Signing'
$TimeStampUrls = @(
  'http://timestamp.digicert.com',
  'http://timestamp.sectigo.com',
  'http://time.certum.pl'
)

# ---------- ขอสิทธิ์ Administrator ----------
function Assert-Admin {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  $pr = New-Object Security.Principal.WindowsPrincipal($id)
  if (-not $pr.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    Write-Host 'ต้องรันเป็น Administrator — กำลังเปิดใหม่พร้อมสิทธิ์...' -ForegroundColor Yellow
    $a = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -AppPath `"$AppPath`""
    Start-Process -FilePath 'powershell.exe' -Verb RunAs -ArgumentList $a
    exit
  }
}
Assert-Admin

Write-Host ''
Write-Host '===== ZenityX Desk — Self-Signed Code-Signing PoC =====' -ForegroundColor Cyan
Write-Host "โฟลเดอร์แอป : $AppPath"
Write-Host ''

if (-not (Test-Path $AppPath)) { throw "ไม่พบโฟลเดอร์: $AppPath" }

# ---------- 1) สร้าง / ใช้ cert เดิม ----------
$cert = Get-ChildItem Cert:\CurrentUser\My |
        Where-Object { $_.FriendlyName -eq $CertFriendly } |
        Select-Object -First 1

if ($cert) {
  Write-Host "ใช้ cert เดิม: $($cert.Thumbprint)" -ForegroundColor DarkGray
} else {
  Write-Host '-> สร้าง self-signed code-signing certificate...'
  $cert = New-SelfSignedCertificate `
            -Type CodeSigningCert `
            -Subject $CertSubject `
            -FriendlyName $CertFriendly `
            -KeyUsage DigitalSignature `
            -KeySpec Signature `
            -KeyExportPolicy Exportable `
            -HashAlgorithm SHA256 `
            -CertStoreLocation Cert:\CurrentUser\My `
            -NotAfter (Get-Date).AddYears(3)
  Write-Host "   สร้างแล้ว: $($cert.Thumbprint)" -ForegroundColor Green
}

# ---------- 2) ทำให้ "เครื่องนี้" เชื่อ cert ----------
Write-Host '-> ติดตั้ง cert เข้า Trusted Root + Trusted Publisher (LocalMachine)...'
$cerFile = Join-Path $env:TEMP 'zenityx-desk-poc.cer'
Export-Certificate -Cert $cert -FilePath $cerFile -Force | Out-Null
foreach ($store in @('Root','TrustedPublisher')) {
  Import-Certificate -FilePath $cerFile -CertStoreLocation "Cert:\LocalMachine\$store" | Out-Null
  Write-Host "   เพิ่มเข้า LocalMachine\$store แล้ว" -ForegroundColor Green
}
Remove-Item $cerFile -ErrorAction SilentlyContinue

# ---------- 3) เซ็นไฟล์ที่ยังไม่ได้เซ็น ----------
Write-Host ''
Write-Host '-> กำลังหาไฟล์ .exe / .dll ...'
$files = Get-ChildItem -Path $AppPath -Recurse -File -Include *.exe,*.dll -ErrorAction SilentlyContinue
Write-Host "   พบ $($files.Count) ไฟล์"

$signed = 0; $skipped = 0; $failed = 0
foreach ($f in $files) {
  $existing = Get-AuthenticodeSignature -FilePath $f.FullName
  if ($existing.Status -eq 'Valid') {
    # มีลายเซ็นที่ใช้ได้อยู่แล้ว (เช่น DLL ของ Microsoft) — ข้าม ไม่ทับ
    $skipped++
    continue
  }

  $ok = $false
  foreach ($ts in $TimeStampUrls) {
    try {
      $r = Set-AuthenticodeSignature -FilePath $f.FullName -Certificate $cert `
             -HashAlgorithm SHA256 -TimestampServer $ts -ErrorAction Stop
      if ($r.Status -eq 'Valid') { $ok = $true; break }
    } catch { }
  }
  if (-not $ok) {
    # timestamp ล่ม -> เซ็นแบบไม่มี timestamp (พอสำหรับ PoC)
    try {
      $r = Set-AuthenticodeSignature -FilePath $f.FullName -Certificate $cert -HashAlgorithm SHA256 -ErrorAction Stop
      if ($r.Status -eq 'Valid') { $ok = $true }
    } catch { }
  }

  if ($ok) { $signed++; Write-Host ("   [เซ็น] " + $f.Name) -ForegroundColor Green }
  else     { $failed++; Write-Host ("   [พลาด] " + $f.Name + " (ไฟล์อาจถูกเปิดใช้อยู่ — ปิดแอปก่อน)") -ForegroundColor Red }
}

# ---------- 4) สถานะ Smart App Control ----------
Write-Host ''
$sacText = 'อ่านไม่ได้'
try {
  $sac = (Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\CI\Policy' -Name 'VerifiedAndReputablePolicyState' -ErrorAction Stop).VerifiedAndReputablePolicyState
  switch ($sac) {
    0 { $sacText = 'ปิดอยู่ (Off) — ดีสำหรับเทสต์' }
    1 { $sacText = 'เปิดเต็ม (Enforcement) — อาจยังบล็อก self-signed!' }
    2 { $sacText = 'โหมดประเมิน (Evaluation)' }
    default { $sacText = "ค่า=$sac" }
  }
} catch { }

Write-Host '===== สรุป =====' -ForegroundColor Cyan
Write-Host ("  เซ็นสำเร็จ : {0}" -f $signed) -ForegroundColor Green
Write-Host ("  ข้าม (เซ็นอยู่แล้ว) : {0}" -f $skipped) -ForegroundColor DarkGray
Write-Host ("  พลาด : {0}" -f $failed) -ForegroundColor ($(if($failed){'Red'}else{'DarkGray'}))
Write-Host ("  Smart App Control : {0}" -f $sacText) -ForegroundColor Yellow
Write-Host ''
Write-Host 'ขั้นต่อไป: ดับเบิลคลิก rustdesk.exe แล้วสังเกต' -ForegroundColor White
Write-Host '  - ไม่มี Bad Image / ไม่มี Unknown Publisher  => signature ธรรมดาเอาอยู่ (cert จริงจบแน่)' -ForegroundColor Gray
Write-Host '  - ยังโดน "Smart App Control" บล็อก          => SAC คือตัวการ self-signed เอาไม่อยู่' -ForegroundColor Gray
Write-Host '    => ต้องลง Microsoft Store หรือปิด SAC (ดู README)' -ForegroundColor Gray
Write-Host ''
Read-Host 'กด Enter เพื่อปิด'
