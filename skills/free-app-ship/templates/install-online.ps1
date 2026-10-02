# ============================================================
#  <Ten app> — cài bằng 1 lệnh (Windows 10/11)
#
#    irm https://raw.githubusercontent.com/<user>/<repo>/main/install-online.ps1 | iex
#
#  Tải bộ cài mới nhất từ GitHub Releases về %USERPROFILE%\<App>
#  rồi chạy install.bat. Tải bằng PowerShell nên không bị SmartScreen chặn.
#  Chạy lại lệnh này = cập nhật.
# ============================================================
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"   # tắt thanh tiến trình chậm của Invoke-WebRequest

$Repo = "<user>/<repo>"
$Dest = if ($env:APP_INSTALL_DIR) { $env:APP_INSTALL_DIR } else { Join-Path $HOME "<App>" }
$Url  = "https://github.com/$Repo/releases/latest/download/<App>-Windows.zip"
$Tmp  = Join-Path ([IO.Path]::GetTempPath()) ("aias-" + [guid]::NewGuid())

Write-Host "============================================================"
Write-Host "  <Ten app> - cai dat tu dong (Windows)"
Write-Host "  Phat trien boi <tac gia>"
Write-Host "============================================================"
New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
try {
    Write-Host "-> Tai bo cai moi nhat..."
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $Url -OutFile (Join-Path $Tmp "app.zip") -UseBasicParsing

    Write-Host "-> Giai nen vao: $Dest"
    Expand-Archive -Path (Join-Path $Tmp "app.zip") -DestinationPath $Tmp -Force
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    Copy-Item -Path (Join-Path $Tmp "<App>-Windows\*") -Destination $Dest -Recurse -Force
    Get-ChildItem -Path $Dest -Recurse -File | Unblock-File
} finally {
    Remove-Item -Recurse -Force $Tmp -ErrorAction SilentlyContinue
}

if ($env:APP_NO_RUN) { Write-Host "OK: da giai nen (APP_NO_RUN)."; return }
Write-Host ""
Push-Location $Dest
try { & cmd.exe /c "install.bat" } finally { Pop-Location }
