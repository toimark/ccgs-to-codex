#!/usr/bin/env python3
# 修复 .claude/skills/ 下被 cn-localization 翻译流程残留破坏的 5 个 SKILL.md。
# - gate-check: 剥掉外层 "可以将...吗?" + ```markdown 围栏，保留内部已翻译内容。
# - brainstorm / changelog / code-review / design-system:
#     仅有占位说明，无实际内容；从英文原版（donchitos/main）恢复。
#
# 用法：
#   python work/fix_broken_skills.py            # 真改写
#   python work/fix_broken_skills.py --dry-run  # 仅展示将做什么

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ENGLISH_RESTORE = ["brainstorm", "changelog", "code-review", "design-system"]

GATE_CHECK_PATH = REPO_ROOT / ".claude" / "skills" / "gate-check" / "SKILL.md"


def fix_gate_check(dry_run: bool) -> tuple[bool, str]:
    """剥掉 gate-check 外层 ```markdown 围栏 + 前导问句，保留内部翻译。"""
    text = GATE_CHECK_PATH.read_text(encoding="utf-8")

    # 内部 frontmatter 起始
    fm_start = text.find("\n---\nname: gate-check")
    if fm_start == -1:
        return False, "未找到内部 frontmatter，跳过"
    inner = text[fm_start + 1 :]  # 去掉前导换行后的内层 markdown

    # 剥末尾的 ```（只剥一个 fence；原文末尾还有真正的协作协议结尾）
    inner = inner.rstrip()
    if inner.endswith("```"):
        inner = inner[: -len("```")].rstrip() + "\n"
    else:
        return False, "未在末尾发现 ``` 围栏，跳过避免误改"

    if dry_run:
        return True, f"将把 {GATE_CHECK_PATH} 缩减为 {len(inner)} 字节（剥掉外层围栏）"
    GATE_CHECK_PATH.write_text(inner, encoding="utf-8", newline="\n")
    return True, f"已重写 {GATE_CHECK_PATH}（{len(inner)} 字节）"


def restore_from_english(name: str, dry_run: bool) -> tuple[bool, str]:
    """从 donchitos/main 恢复英文原版 SKILL.md。"""
    rel = f".claude/skills/{name}/SKILL.md"
    target = REPO_ROOT / rel
    try:
        content = subprocess.check_output(
            ["git", "show", f"donchitos/main:{rel}"],
            cwd=REPO_ROOT,
            text=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        return False, f"git show 失败: {exc}"

    if dry_run:
        return True, f"将用英文原版覆盖 {rel}（{len(content)} 字节）"
    target.write_text(content, encoding="utf-8", newline="\n")
    return True, f"已用英文原版覆盖 {rel}（{len(content)} 字节）"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("# gate-check（剥外层围栏）")
    ok, msg = fix_gate_check(args.dry_run)
    print(f"  - {'OK' if ok else 'SKIP'}: {msg}")

    print("# 从英文原版恢复（donchitos/main）")
    for name in ENGLISH_RESTORE:
        ok, msg = restore_from_english(name, args.dry_run)
        print(f"  - {name}: {'OK' if ok else 'FAIL'}: {msg}")

    if args.dry_run:
        print("\n[dry-run] 未做改动。去掉 --dry-run 重新运行可应用。")


if __name__ == "__main__":
    main()
