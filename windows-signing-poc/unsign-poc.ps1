#requires -version 5.1
<#
  ZenityX Desk — ถอนคืน PoC (cleanup)
  ลบ self-signed cert ออกจาก Trusted Root / Trusted Publisher / Personal
  ทำให้เครื่องกลับมาเหมือนเดิม (ไฟล์ที่เซ็นไว้จะกลายเป็น "ไม่เชื่อถือ" อีกครั้ง)
#>
[CmdletBinding()] param()
$ErrorActionPreference = 'Stop'
$CertFriendly = 'ZenityX Desk PoC Code Signing'
$CertSubject  = 'CN=ZenityX Desk (Self-Signed PoC)'

function Assert-Admin {
  $id = [Security.Principal.WindowsIdentity]::GetCurrent()
  $pr = New-Object Security.Principal.WindowsPrincipal($id)
  if (-not $pr.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
  }
}
Assert-Admin

$stores = @('Cert:\LocalMachine\Root','Cert:\LocalMachine\TrustedPublisher','Cert:\CurrentUser\My')
$removed = 0
foreach ($s in $stores) {
  Get-ChildItem $s -ErrorAction SilentlyContinue |
    Where-Object { $_.FriendlyName -eq $CertFriendly -or $_.Subject -eq $CertSubject } |
    ForEach-Object {
      Remove-Item $_.PSPath -Force -ErrorAction SilentlyContinue
      Write-Host ("ลบจาก {0}: {1}" -f $s, $_.Thumbprint) -ForegroundColor Green
      $removed++
    }
}
Write-Host ''
Write-Host ("ถอนคืนเรียบร้อย — ลบ cert ไป {0} รายการ" -f $removed) -ForegroundColor Cyan
Write-Host '(ลายเซ็นบนไฟล์ยังอยู่ แต่จะไม่ถูกเชื่อถือแล้ว — ไม่มีผลเสีย)' -ForegroundColor DarkGray
Read-Host 'กด Enter เพื่อปิด'
