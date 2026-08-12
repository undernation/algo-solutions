"""
git pre-commit 훅 설치 — 커밋할 때마다 잔디/인덱스 자동 갱신.

    python _meta/install_hooks.py

.git/hooks 는 push 되지 않으므로 **PC마다 한 번씩** 실행해야 한다.
(GitHub Actions 는 로컬 실수노트를 못 읽으므로, 볼트가 있는 PC에서는 이 훅이 있어야 완전하다.)
"""
import os, io, stat, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOOK = r"""#!/bin/sh
# algo-solutions pre-commit — 잔디/인덱스 자동 갱신
# 해제: git commit --no-verify  또는  이 파일 삭제

PY=$(command -v python || command -v python3)
[ -z "$PY" ] && { echo "[hook] python 없음 — 건너뜀"; exit 0; }

export PYTHONIOENCODING=utf-8
"$PY" _meta/build_probindex.py >/dev/null 2>&1 || echo "[hook] 문제색인 생성 실패(무시)"
"$PY" _meta/build_heatmap.py >/dev/null 2>&1 || echo "[hook] heatmap 생성 실패(무시)"
"$PY" _meta/build_index.py   >/dev/null 2>&1 || echo "[hook] index 생성 실패(무시)"

# 갱신된 산출물을 이번 커밋에 포함
git add README.md assets/heatmap.svg _meta/history.json 2>/dev/null
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
