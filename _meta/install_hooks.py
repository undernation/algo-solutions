"""
git pre-commit 훅 설치 — 커밋할 때마다 🔒 공개 금지 검사 + 잔디/인덱스 자동 갱신.

    python _meta/install_hooks.py

.git/hooks 는 push 되지 않으므로 **PC마다 한 번씩** 실행해야 한다.
(GitHub Actions 는 로컬 실수노트를 못 읽으므로, 볼트가 있는 PC에서는 이 훅이 있어야 완전하다.)
⚠️ git worktree 들은 훅 폴더를 본 저장소와 같이 쓴다. 어느 체크아웃에서 설치하든 전부에 걸린다.

훅이 커밋을 **막는** 경우는 하나뿐이다 — 공개하면 안 되는 것이 커밋에 들어가려 할 때
(selfcheck.py --leak-only --staged): 코드트리 유형 태그·진행상태(항상), judge_config.json 의
privateSites 에 든 사이트의 지문·예제, TC 보관소(_meta/tc_store/). repo 는 public 이라 한 번
push 하면 되돌릴 수 없다. 빌드 단계는 예전처럼 실패해도 커밋을 통과시킨다.
"""
import os, io, stat, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOOK = r"""#!/bin/sh
# algo-solutions pre-commit — 🔒 공개 금지 검사 + 잔디/인덱스 자동 갱신
# 해제: git commit --no-verify  또는  이 파일 삭제

PY=$(command -v python || command -v python3)
[ -z "$PY" ] && { echo "[hook] python 없음 — 건너뜀 (⚠️ 공개 금지 검사도 못 했음)"; exit 0; }

export PYTHONIOENCODING=utf-8

# ── 🔒 공개 금지 검사 — 이 단계만은 커밋을 막는다 ──
# 코드트리 유형 태그·진행상태(항상) / judge_config.json privateSites 사이트의 지문·예제 /
# TC 보관소(_meta/tc_store/). repo 는 public 이라 push 하면 히스토리·포크·캐시에 남는다.
# 이번 커밋에 들어갈 내용(스테이징본)만 본다. 통과하면 조용히(경고 줄만) 지나간다.
# selfcheck.py 에 --leak-only 가 없는 옛 브랜치에서는 건너뛴다 — 모르는 옵션을 무시하고
# 전체 점검을 돌려, 공개와 상관없는 오류로 커밋이 막히기 때문이다(훅은 worktree 끼리 공유).
if grep -q -e "--leak-only" _meta/selfcheck.py 2>/dev/null; then
  out=$("$PY" _meta/selfcheck.py --leak-only --staged 2>&1)
  rc=$?
  if [ $rc -eq 0 ]; then
    printf '%s\n' "$out" | grep "⚠" || :
  else
    printf '%s\n' "$out"
    echo ""
    if [ $rc -eq 1 ]; then
      echo "[hook] ⛔ 공개하면 안 되는 내용이 커밋에 들어가려 해서 커밋을 멈췄습니다."
      echo "[hook]    위 파일에서 그 필드를 빼거나 스테이징에서 내린 뒤"
      echo "[hook]    (git reset -q -- <파일>) 다시 커밋하세요."
    else
      echo "[hook] ⛔ 공개 금지 검사 자체가 실패해서 커밋을 멈췄습니다 (rc=$rc)."
      echo "[hook]    python _meta/selfcheck.py --leak-only --staged 로 원인을 확인하세요."
    fi
    echo "[hook]    문제가 아닌 게 확실할 때만: git commit --no-verify"
    exit 1
  fi
fi

"$PY" _meta/build_probindex.py >/dev/null 2>&1 || echo "[hook] 문제색인 생성 실패(무시)"
"$PY" _meta/build_heatmap.py >/dev/null 2>&1 || echo "[hook] heatmap 생성 실패(무시)"
"$PY" _meta/build_index.py   >/dev/null 2>&1 || echo "[hook] index 생성 실패(무시)"

# 갱신된 산출물을 이번 커밋에 포함.
# ⚠️ 방금 만든 것을 하나라도 빠뜨리면 안 된다. index.html 과 _meta/built.json 이
#    서로 다른 빌드에서 나오면 브라우저가 짝을 비교해 "새 기록이 있습니다" 팝업을
#    잘못 띄우고, 워킹트리도 커밋 직후부터 계속 더러운 채로 남는다(2026-08-26).
git add README.md HEATMAP.md index.html assets/heatmap.svg assets/heatmap.html \
        _meta/history.json _meta/built.json problems/index.json 2>/dev/null
exit 0
"""


def main():
    try:
        hooks = subprocess.run(["git", "rev-parse", "--git-path", "hooks"],
                               cwd=ROOT, capture_output=True, text=True,
                               check=True).stdout.strip()
    except Exception as e:
        print("❌ git 저장소가 아님:", e)
        sys.exit(1)

    hooks = os.path.join(ROOT, hooks) if not os.path.isabs(hooks) else hooks
    os.makedirs(hooks, exist_ok=True)
    path = os.path.join(hooks, "pre-commit")

    io.open(path, "w", encoding="utf-8", newline="\n").write(HOOK)
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    print("✅ pre-commit 훅 설치:", path)
    print("   이제 커밋할 때마다 잔디·인덱스가 자동 갱신됩니다.")
    print("   🔒 공개하면 안 되는 것(코드트리 유형 태그·진행상태, 비공개 사이트 지문, TC 보관소)이")
    print("      스테이징돼 있으면 커밋을 막습니다. 그 외엔 막지 않습니다.")
    print("   해제하려면 이 파일을 지우거나 git commit --no-verify")


def setup_identity():
    """커밋 작성자를 GitHub 계정에 연결된 주소로 맞춘다(PC마다 1회).

    다른 주소로 커밋하면 GitHub 가 작성자를 못 알아봐 프로필 잔디에 안 찍힌다.
    """
    import subprocess
    subprocess.run(["git", "config", "user.name", "undernation"], cwd=ROOT)
    subprocess.run(["git", "config", "user.email", "solomon2752@naver.com"], cwd=ROOT)
    print("✅ 커밋 작성자: undernation <solomon2752@naver.com>")


def setup_merge_driver():
    """.gitattributes 의 merge=ours 가 동작하려면 드라이버 등록이 필요하다(PC마다 1회)."""
    import subprocess
    subprocess.run(["git", "config", "merge.ours.driver", "true"], cwd=ROOT)
    print("✅ merge=ours 드라이버 등록 (생성물 충돌 방지)")


if __name__ == "__main__":
    main()
    setup_merge_driver()
    setup_identity()
