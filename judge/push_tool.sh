#!/bin/sh
# 배포용 도구 zip 을 클라우드 허브에 올린다.
#
#   sh judge/push_tool.sh                    # 릴리스에서 받아 올린다
#   sh judge/push_tool.sh ./some-tool.zip    # 로컬 파일을 그대로 올린다
#
# 대시보드 #tools 화면이 여기 올린 파일을 내려준다(토큰 보유자만).
#
# 🚩 파일은 repo 밖(VM 의 ~/algo-tools)에 둔다. 이 저장소는 public 이라
#    repo 안에 넣으면 GitHub Pages 로 그대로 공개된다. 배포 zip 에는
#    보통 설정·자격증명이 함께 들어가므로 이 구분이 곧 보안선이다.
#
# 환경변수로 바꿀 수 있는 것:
#   ALGO_TOOL_REPO   릴리스를 받아올 비공개 저장소 (owner/repo)
#   ALGO_VM          접속 대상 (기본 ubuntu@134.185.106.155)
#   ALGO_VM_KEY      SSH 키   (기본 ~/.ssh/oracle_judge)
set -e

VM="${ALGO_VM:-ubuntu@134.185.106.155}"
KEY="${ALGO_VM_KEY:-$HOME/.ssh/oracle_judge}"
SRC="$1"

if [ -z "$SRC" ]; then
  REPO="${ALGO_TOOL_REPO:-}"
  if [ -z "$REPO" ]; then
    echo "올릴 파일을 지정하거나 ALGO_TOOL_REPO 를 설정하세요." >&2
    echo "  예) ALGO_TOOL_REPO=owner/repo sh judge/push_tool.sh" >&2
    exit 1
  fi
  TMP="$(mktemp -d)"
  echo "[*] $REPO 최신 릴리스에서 zip 을 받는다"
  gh release download --repo "$REPO" --pattern '*.zip' --dir "$TMP" --clobber
  SRC="$(ls "$TMP"/*.zip | head -1)"
fi

[ -f "$SRC" ] || { echo "파일이 없다: $SRC" >&2; exit 1; }
echo "[*] 올린다: $(basename "$SRC")  ($(wc -c < "$SRC") bytes)"

ssh -i "$KEY" "$VM" 'mkdir -p ~/algo-tools && chmod 700 ~/algo-tools'
scp -i "$KEY" "$SRC" "$VM:~/algo-tools/"
# 자격증명이 들어 있을 수 있으므로 본인만 읽게 막아 둔다
ssh -i "$KEY" "$VM" 'chmod 600 ~/algo-tools/*.zip; ls -la ~/algo-tools/'

echo
echo "[OK] 대시보드 → 도구 메뉴에서 받을 수 있다 (토큰 필요)."
