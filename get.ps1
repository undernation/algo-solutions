# 코딩 도구 한 줄 설치 — 새 PC 에서 PowerShell 에 아래 한 줄만 붙여 넣으면 된다.
#
#   iex ([Text.Encoding]::UTF8.GetString((iwr https://undernation.github.io/algo-solutions/get.ps1 -UseBasicParsing).RawContentStream.ToArray()))
#
# ※ 왜 `irm ... | iex` 가 아닌가: Windows 기본 PowerShell 5.1 은 응답에 charset 이
#    없으면 ISO-8859-1 로 읽어서 이 파일의 한글이 전부 깨진다. 위처럼 UTF-8 로
#    직접 디코딩하면 어느 버전에서든 제대로 나온다.
#    PowerShell 7(pwsh) 이나 영어가 깨져도 상관없다면 짧게 써도 동작은 한다:
#       irm https://undernation.github.io/algo-solutions/get.ps1 | iex
#
# 비대화형에서 돌릴 때는 비밀번호를 환경변수로 줄 수 있다:
#       $env:TOOL_PASS="...."; iex (...)
#
# 하는 일: 허브 주소 확인 → 비밀번호 확인 → zip 내려받기 → 압축 해제 →
#          (원하면) setup.bat 실행까지.
#
# 비밀번호는 이 파일에 없다. 실행할 때 물어보고, 입력값은 화면에 찍히지 않으며
# 헤더로만 보낸다(URL 에 실으면 프록시 로그·히스토리에 남는다).
# 이 스크립트 자체는 공개되어 있어도 무해하다 — 비밀번호 없이는 아무것도 못 받는다.

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"   # 진행률 막대가 느려서 끈다

function Say($m, $c = "Gray") { Write-Host $m -ForegroundColor $c }

Say ""
Say "=== 코딩 도구 설치 ===" "Cyan"

# 1) 허브 주소 — 터널 URL 이 바뀌어도 여기서 자동으로 따라간다
$base = "https://undernation.github.io/algo-solutions"
try {
    $ep = Invoke-RestMethod "$base/_meta/endpoint.json?cb=$(Get-Random)"
    $hub = $ep.url.TrimEnd('/')
} catch {
    Say "허브 주소를 읽지 못했습니다: $_" "Red"; return
}
Say "허브: $hub"

# 2) 비밀번호 — 환경변수 TOOL_PASS 가 있으면 그것을 쓰고, 없으면 물어본다.
#    (자동화·비대화형 환경에서도 돌아가게 하려는 것. 평소에는 그냥 물어본다.)
$pw = $env:TOOL_PASS
if (-not $pw) {
    $sec = Read-Host "비밀번호" -AsSecureString      # 입력이 화면에 보이지 않는다
    $pw = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
            [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec))
}
if (-not $pw) { Say "비밀번호가 비었습니다." "Red"; return }
$headers = @{ "X-Tool-Pass" = $pw; "Content-Type" = "application/json" }

# 3) 무엇을 받을지 먼저 확인
try {
    $info = Invoke-RestMethod "$hub/toolinfo" -Method POST -Headers $headers -Body "{}"
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 401) { Say "비밀번호가 틀렸습니다." "Red" }
    elseif ($code -eq 429) { Say "여러 번 틀려 잠겼습니다. 잠시 뒤 다시 시도하세요." "Red" }
    else { Say "허브에 닿지 못했습니다: $_" "Red" }
    return
}
if (-not $info.ok) { Say "받을 파일이 없습니다: $($info.error)" "Red"; return }
Say ("파일: {0}  ({1:N1} KB, {2} 기준)" -f $info.name, ($info.size / 1KB), $info.mtime)

# 4) 내려받기 — 임시 파일로 받고, 압축을 푼 뒤 지운다
$dest = Join-Path (Get-Location) ([IO.Path]::GetFileNameWithoutExtension($info.name))
$tmp = Join-Path ([IO.Path]::GetTempPath()) $info.name
try {
    Invoke-WebRequest "$hub/tool" -Method POST -Headers $headers -Body "{}" -OutFile $tmp
} catch {
    Say "내려받기 실패: $_" "Red"; return
}
$got = (Get-Item $tmp).Length
if ($got -ne $info.size) {
    Say "크기가 다릅니다 ($got / $($info.size)) — 중간에 끊긴 것 같습니다." "Red"
    Remove-Item $tmp -Force; return
}

# 5) 압축 해제
if (Test-Path $dest) {
    $ans = Read-Host "$dest 이(가) 이미 있습니다. 덮어쓸까요? (y/N)"
    if ($ans -ne "y") { Remove-Item $tmp -Force; Say "취소했습니다."; return }
    Remove-Item $dest -Recurse -Force
}
Expand-Archive -Path $tmp -DestinationPath (Get-Location) -Force
Remove-Item $tmp -Force                     # 키가 든 zip 을 임시 폴더에 남기지 않는다
Say "압축 해제: $dest" "Green"

# 6) 준비 실행
$setup = Join-Path $dest "setup.bat"
if (Test-Path $setup) {
    $ans = Read-Host "지금 setup.bat 을 실행할까요? (Y/n)"
    if ($ans -ne "n") {
        Push-Location $dest
        & cmd /c "setup.bat"
        Pop-Location
    }
}

Say ""
Say "끝났습니다." "Green"
Say "  실행    : $dest\start.vbs  (콘솔 없이 백그라운드)"
Say "  콘솔로  : $dest\console.bat"
Say "  자동시작: $dest\install_startup.bat"
Say ""
Say "이 폴더에는 설정과 키가 함께 들어 있습니다. 공용 PC 라면 다 쓴 뒤 폴더를 지우세요." "Yellow"
