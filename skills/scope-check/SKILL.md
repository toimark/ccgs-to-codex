---
name: scope-check
description: "通过将当前范围与原始计划进行对比，分析功能或 Sprint 的范围蔓延（Scope Creep）。标记新增项，量化膨胀程度，并推荐裁剪方案。"
---

# scope-check（Codex 适配薄壳）

本技能是 Codex 端的薄壳，单一事实源在
[.claude/skills/scope-check/SKILL.md](../../.claude/skills/scope-check/SKILL.md)。

当用户请求触发此技能时：

1. 阅读上述 Claude 源文件中的工作流。
2. 把 Claude Code 工具语义映射到 Codex 等价工具：
   - Read / Glob / Grep -> shell_command 加 rg / Get-ChildItem / Get-Content
   - Write / Edit -> apply_patch
   - Bash -> shell_command
   - AskUserQuestion -> 直接向用户提问（Default 模式）或 Plan 模式下 request_user_input
3. 按 [AGENTS.md](../../AGENTS.md) 的协作协议（提问 -> 选项 -> 决定 -> 草稿 -> 审批）执行。
