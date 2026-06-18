---
name: setup-engine
description: "配置项目的游戏引擎和版本。将引擎锁定到 CLAUDE.md 中，检测知识缺口，当版本超出 LLM 训练数据时通过 WebSearch 填充引擎参考文档。"
---

# setup-engine（Codex 适配薄壳）

本技能是 Codex 端的薄壳，单一事实源在
[.claude/skills/setup-engine/SKILL.md](../../.claude/skills/setup-engine/SKILL.md)。

当用户请求触发此技能时：

1. 阅读上述 Claude 源文件中的工作流。
2. 把 Claude Code 工具语义映射到 Codex 等价工具：
   - Read / Glob / Grep -> shell_command 加 rg / Get-ChildItem / Get-Content
   - Write / Edit -> apply_patch
   - Bash -> shell_command
   - AskUserQuestion -> 直接向用户提问（Default 模式）或 Plan 模式下 request_user_input
3. 按 [AGENTS.md](../../AGENTS.md) 的协作协议（提问 -> 选项 -> 决定 -> 草稿 -> 审批）执行。
