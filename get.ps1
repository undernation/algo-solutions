# One-line installer for the coding tool. On a new PC, paste this into PowerShell:
#
#   irm https://undernation.github.io/algo-solutions/get.ps1 | iex
#
# This script is ASCII-only on purpose: Windows PowerShell 5.1 mangles non-ASCII
# text when a web response has no charset, so keeping it ASCII lets the short
# `irm | iex` form work everywhere (5.1 and 7 alike).
#
# Non-interactive: pass the password via env var.
#   $env:TOOL_PASS="...."; irm https://undernation.github.io/algo-solutions/get.ps1 | iex
#
# What it does: find hub -> ask password -> download zip -> extract -> (optionally) run setup.bat.
# The password is NOT in this file. It is asked at run time, never echoed, and sent
# only as a header (never in the URL). This script is harmless if public: without the
# password it can download nothing.

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"   # progress bar is slow; turn it off

function Say($m, $c = "Gray") { Write-Host $m -ForegroundColor $c }

Say ""
Say "=== Coding tool installer ===" "Cyan"

# 1) Hub address (auto-follows even when the tunnel URL changes)
$base = "https://undernation.github.io/algo-solutions"
try {
    $ep = Invoke-RestMethod "$base/_meta/endpoint.json?cb=$(Get-Random)"
    $hub = $ep.url.TrimEnd('/')
} catch {
    Say "Could not read hub address: $_" "Red"; return
}
Say "Hub: $hub"

# 2) Password (use env var TOOL_PASS if set, otherwise prompt)
$pw = $env:TOOL_PASS
if (-not $pw) {
    $sec = Read-Host "Password" -AsSecureString      # input is not shown on screen
    $pw = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
            [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec))
}
if (-not $pw) { Say "Password was empty." "Red"; return }
$headers = @{ "X-Tool-Pass" = $pw; "Content-Type" = "application/json" }

# 3) Check what will be downloaded
try {
    $info = Invoke-RestMethod "$hub/toolinfo" -Method POST -Headers $headers -Body "{}"
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 401) { Say "Wrong password." "Red" }
    elseif ($code -eq 429) { Say "Too many attempts - locked. Try again later." "Red" }
    else { Say "Could not reach hub: $_" "Red" }
    return
}
if (-not $info.ok) { Say "Nothing to download: $($info.error)" "Red"; return }
Say ("File: {0}  ({1:N1} KB, as of {2})" -f $info.name, ($info.size / 1KB), $info.mtime)

# 4) Download to a temp file, extract, then delete the temp file
$dest = Join-Path (Get-Location) ([IO.Path]::GetFileNameWithoutExtension($info.name))
$tmp = Join-Path ([IO.Path]::GetTempPath()) $info.name
try {
    Invoke-WebRequest "$hub/tool" -Method POST -Headers $headers -Body "{}" -OutFile $tmp
} catch {
    Say "Download failed: $_" "Red"; return
}
$got = (Get-Item $tmp).Length
if ($got -ne $info.size) {
    Say "Size mismatch ($got / $($info.size)) - download looks truncated." "Red"
    Remove-Item $tmp -Force; return
}

# 5) Extract
if (Test-Path $dest) {
    $ans = Read-Host "$dest already exists. Overwrite? (y/N)"
    if ($ans -ne "y") { Remove-Item $tmp -Force; Say "Cancelled."; return }
    Remove-Item $dest -Recurse -Force
}
Expand-Archive -Path $tmp -DestinationPath (Get-Location) -Force
Remove-Item $tmp -Force                     # don't leave the key-bearing zip in temp
Say "Extracted to: $dest" "Green"

# 6) Run setup
$setup = Join-Path $dest "setup.bat"
if (Test-Path $setup) {
    $ans = Read-Host "Run setup.bat now? (Y/n)"
    if ($ans -ne "n") {
        Push-Location $dest
        & cmd /c "setup.bat"
        Pop-Location
    }
}

Say ""
Say "Done." "Green"
Say "  run        : $dest\start.vbs   (background, no console)"
Say "  console    : $dest\console.bat"
Say "  autostart  : $dest\install_startup.bat"
Say ""
Say "This folder holds settings and an API key. On a shared PC, delete it when done." "Yellow"
