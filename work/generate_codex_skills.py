#!/usr/bin/env python3
# 一次性脚本：根据 .claude/skills/<name>/SKILL.md 生成 Codex 端薄壳
# 输出位置：ccgs-to-codex/skills/<name>/SKILL.md
# 每个薄壳只含 frontmatter + 指向 Claude 源文件的链接，避免重复内容。

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / ".claude" / "skills"
DST_ROOT = REPO_ROOT / "skills"

# 允许文件开头是 ```markdown 围栏或其他空白
FM_RE = re.compile(r"(?ms)^---\s*\r?\n(.*?)\r?\n---")
NAME_RE = re.compile(r"(?m)^name:\s*(.+?)\s*$")
DESC_QUOTED_RE = re.compile(r'(?m)^description:\s*"(.+?)"\s*$')
DESC_PLAIN_RE = re.compile(
    r"(?ms)^description:\s*(.+?)\s*(?=\r?\n[a-zA-Z\-]+:|\Z)"
)


def parse_frontmatter(text: str) -> tuple[str | None, str | None]:
    m = FM_RE.search(text)
    if not m:
        return None, None
    fm = m.group(1)
    name_m = NAME_RE.search(fm)
    name = name_m.group(1).strip() if name_m else None
    desc = None
    qm = DESC_QUOTED_RE.search(fm)
    if qm:
        desc = qm.group(1).strip()
    else:
        pm = DESC_PLAIN_RE.search(fm)
        if pm:
            d = pm.group(1).strip()
            if len(d) >= 2 and d[0] == '"' and d[-1] == '"':
                d = d[1:-1]
            desc = d
    return name, desc


def render(name: str, desc: str, src_rel: str) -> str:
    desc_escaped = desc.replace('"', '\\"')
    return (
        "---\n"
        f"name: {name}\n"
        f'description: "{desc_escaped}"\n'
        "---\n\n"
        f"# {name}（Codex 适配薄壳）\n\n"
        "本技能是 Codex 端的薄壳，单一事实源在\n"
        f"[{src_rel}](../../{src_rel})。\n\n"
        "当用户请求触发此技能时：\n\n"
        "1. 阅读上述 Claude 源文件中的工作流。\n"
        "2. 把 Claude Code 工具语义映射到 Codex 等价工具：\n"
        "   - Read / Glob / Grep -> shell_command 加 rg / Get-ChildItem / Get-Content\n"
        "   - Write / Edit -> apply_patch\n"
        "   - Bash -> shell_command\n"
        "   - AskUserQuestion -> 直接向用户提问（Default 模式）或 Plan 模式下 request_user_input\n"
        "3. 按 [AGENTS.md](../../AGENTS.md) 的协作协议（提问 -> 选项 -> 决定 -> 草稿 -> 审批）执行。\n"
    )


def main() -> None:
    DST_ROOT.mkdir(parents=True, exist_ok=True)
    total = 0
    broken = []
    for sub in sorted(SRC_ROOT.iterdir()):
        if not sub.is_dir():
            continue
        src = sub / "SKILL.md"
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        name, desc = parse_frontmatter(text)
        is_broken = False
        if not name or not desc:
            is_broken = True
            name = sub.name
            desc = (
                f"（占位）原 .claude/skills/{sub.name}/SKILL.md frontmatter 缺失或损坏，"
                "请修复后再更新此薄壳。"
            )
        body = render(name, desc, f".claude/skills/{sub.name}/SKILL.md")
        dst_dir = DST_ROOT / sub.name
        dst_dir.mkdir(parents=True, exist_ok=True)
        (dst_dir / "SKILL.md").write_text(body, encoding="utf-8", newline="\n")
        total += 1
        if is_broken:
            broken.append(sub.name)

    print(f"总计: {total} 个 Codex 薄壳已生成。")
    if broken:
        print(f"占位（原 frontmatter 损坏，共 {len(broken)} 个）: {', '.join(broken)}")
    else:
        print("所有 frontmatter 解析正常。")


if __name__ == "__main__":
    main()
