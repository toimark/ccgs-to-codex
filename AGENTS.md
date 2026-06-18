# Codex Game Studios — 游戏工作室代理架构（Codex 适配版）

本仓库最初为 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 设计，
现已开始向 [Codex](https://github.com/openai/codex) 迁移。
本文件是 Codex 在打开仓库时自动读取的主上下文（相当于原 `CLAUDE.md`）。

> 迁移仍在进行中。仍可同时使用 Claude Code（读取 [CLAUDE.md](CLAUDE.md)）。
> 关于完整差异与后续计划，见 [docs/CODEX-MIGRATION.md](docs/CODEX-MIGRATION.md)。

## 技术栈

- **引擎**：[选择：Godot 4 / Unity / Unreal Engine 5]
- **语言**：[选择：GDScript / C# / C++ / Blueprint]
- **版本控制**：Git，基于主干开发
- **构建系统**：[选择引擎后指定]
- **资产管线**：[选择引擎后指定]

> Godot、Unity、Unreal 各自有专属引擎专家代理与子专家。请使用与你引擎匹配的代理集。

## 关键参考文档

Codex 不支持 Claude Code 的 `@path` 自动 import 语法。需要时请按以下索引主动阅读：

- 项目结构：[.claude/docs/directory-structure.md](.claude/docs/directory-structure.md)
- 引擎版本参考：[docs/engine-reference/godot/VERSION.md](docs/engine-reference/godot/VERSION.md)
  （或 [docs/engine-reference/unity](docs/engine-reference/unity)、[docs/engine-reference/unreal](docs/engine-reference/unreal)）
- 技术偏好：[.claude/docs/technical-preferences.md](.claude/docs/technical-preferences.md)
- 协调规则：[.claude/docs/coordination-rules.md](.claude/docs/coordination-rules.md)
- 编码标准：[.claude/docs/coding-standards.md](.claude/docs/coding-standards.md)
- 上下文管理：[.claude/docs/context-management.md](.claude/docs/context-management.md)
- 代理花名册：[.claude/docs/agent-roster.md](.claude/docs/agent-roster.md)
- 委派与上报路径：[.claude/docs/agent-coordination-map.md](.claude/docs/agent-coordination-map.md)

## 协作协议

**用户驱动的协作，而非自主执行。** 每个任务遵循：
**提问 → 选项 → 决定 → 草稿 → 审批**

- 在使用文件写入工具（`apply_patch`、批量重写等）之前，
  先询问"可以将此内容写入 [文件路径] 吗？"，或在草稿基础上征求确认。
- 在请求审批前必须展示草稿或摘要。
- 多文件变更需要明确批准整个变更集。
- 没有用户指示，不要进行任何 `git commit` / `git push`。

完整协议与示例见 [docs/COLLABORATIVE-DESIGN-PRINCIPLE.md](docs/COLLABORATIVE-DESIGN-PRINCIPLE.md)。

## 角色（原 Agents）使用方式

原 `.claude/agents/*.md` 中的 48 份角色定义在 Codex 里**作为提示词文档保留**，
但 frontmatter 中的 `model`、`maxTurns`、`disallowedTools`、`skills` 等字段
对 Codex 不生效。当任务需要某个角色视角时：

1. 主 Codex 先按用户意图判断该交给哪位"代理"。
2. 阅读对应 `.claude/agents/<role>.md`，按其职责与协作协议行事。
3. 跨领域决策需上报至共同上级（设计冲突 → `creative-director`，
   技术冲突 → `technical-director`，跨部门变更协调 → `producer`）。

完整列表与上报路径见 [.claude/docs/agent-roster.md](.claude/docs/agent-roster.md)
与 [.claude/docs/agent-coordination-map.md](.claude/docs/agent-coordination-map.md)。

## 技能（原 Slash Commands）使用方式

Claude Code 的 `/start`、`/code-review` 等斜杠命令在 Codex 中没有 `/` 触发器，
但本仓库已声明为 Codex 本地 plugin（见 [.codex-plugin/plugin.json](.codex-plugin/plugin.json)），
并在 [skills/](skills/) 下为每个技能生成了**薄壳**：仅包含 frontmatter 与
指向 `.claude/skills/<name>/SKILL.md` 单一事实源的链接。Codex 会按薄壳的
`description` 自动匹配触发，不再依赖斜杠命令。

若用户要求执行某个技能而 Codex 未自动匹配，可阅读对应 `SKILL.md` 后按流程执行：

- `/start` → [.claude/skills/start/SKILL.md](.claude/skills/start/SKILL.md)
- `/brainstorm` → [.claude/skills/brainstorm/SKILL.md](.claude/skills/brainstorm/SKILL.md)
- `/sprint-plan` → [.claude/skills/sprint-plan/SKILL.md](.claude/skills/sprint-plan/SKILL.md)
- `/code-review` → [.claude/skills/code-review/SKILL.md](.claude/skills/code-review/SKILL.md)
- `/design-review` → [.claude/skills/design-review/SKILL.md](.claude/skills/design-review/SKILL.md)
- `/project-stage-detect` → [.claude/skills/project-stage-detect/SKILL.md](.claude/skills/project-stage-detect/SKILL.md)
- 其余技能：浏览 [.claude/skills/](.claude/skills) 子目录。

技能 frontmatter 里的 `allowed-tools` 字段（`Read, Glob, Grep, AskUserQuestion` 等）
是 Claude Code 工具名，Codex 中以 `shell_command`、`apply_patch`、`view_image`
等等价工具替代；语义上保持只读探索 vs. 写入修改的区分即可。Codex 端薄壳已
刻意省略此字段，避免对工具集做错误约束。

> **生成 / 重新生成薄壳**：
> ```bash
> python work/generate_codex_skills.py
> ```
> 当上游 `.claude/skills/` 中某个 SKILL.md 的 frontmatter 修复或调整后，
> 重跑此脚本即可同步 `skills/` 端的 `name` 与 `description`。

## 路径范围规则

`.claude/rules/` 中的 11 条规则在 Claude Code 中按文件路径自动注入。
Codex 通过 **子目录 `AGENTS.md`** 等价复刻此机制：在改动对应路径时
Codex 会自动叠加加载该目录的 `AGENTS.md`（链回 `.claude/rules/<rule>.md` 单一事实源）。

对照表：

| 改动路径 | Codex 子目录 AGENTS.md | 单一事实源 |
|---------|----------------------|-----------|
| `src/gameplay/**` | [src/gameplay/AGENTS.md](src/gameplay/AGENTS.md) | [.claude/rules/gameplay-code.md](.claude/rules/gameplay-code.md) |
| `src/core/**` | [src/core/AGENTS.md](src/core/AGENTS.md) | [.claude/rules/engine-code.md](.claude/rules/engine-code.md) |
| `src/ai/**` | [src/ai/AGENTS.md](src/ai/AGENTS.md) | [.claude/rules/ai-code.md](.claude/rules/ai-code.md) |
| `src/networking/**` | [src/networking/AGENTS.md](src/networking/AGENTS.md) | [.claude/rules/network-code.md](.claude/rules/network-code.md) |
| `src/ui/**` | [src/ui/AGENTS.md](src/ui/AGENTS.md) | [.claude/rules/ui-code.md](.claude/rules/ui-code.md) |
| `assets/shaders/**` | [assets/shaders/AGENTS.md](assets/shaders/AGENTS.md) | [.claude/rules/shader-code.md](.claude/rules/shader-code.md) |
| `assets/data/**` | [assets/data/AGENTS.md](assets/data/AGENTS.md) | [.claude/rules/data-files.md](.claude/rules/data-files.md) |
| `design/gdd/**` | [design/gdd/AGENTS.md](design/gdd/AGENTS.md) | [.claude/rules/design-docs.md](.claude/rules/design-docs.md) |
| `design/narrative/**` | [design/narrative/AGENTS.md](design/narrative/AGENTS.md) | [.claude/rules/narrative.md](.claude/rules/narrative.md) |
| `tests/**` | [tests/AGENTS.md](tests/AGENTS.md) | [.claude/rules/test-standards.md](.claude/rules/test-standards.md) |
| `prototypes/**` | [prototypes/AGENTS.md](prototypes/AGENTS.md) | [.claude/rules/prototype-code.md](.claude/rules/prototype-code.md) |

## 钩子与权限（暂未迁移）

`.claude/settings.json` 中的 `hooks`、`permissions`、`statusLine` 是 Claude Code
独有机制，Codex 不会执行。当前替代方案：

- `validate-commit.sh` / `validate-push.sh` 已通过 [.githooks/](.githooks/)
  目录下的 Git hook 包装重新启用。在仓库根目录执行一次：

  ```bash
  git config core.hooksPath .githooks
  ```

  之后普通 `git commit` / `git push` 会自动触发同一份验证逻辑。
- 危险命令的"deny 列表"（`rm -rf`、`git push --force`、读 `.env`）
  在 Codex 中由沙箱与升级审批模型负责；同时本文件再次声明：
  - **不要**执行 `rm -rf`、`git reset --hard`、`git clean -f` 等破坏性命令，
    除非用户明确要求。
  - **不要**执行 `git push --force` / `git push -f`。
  - **不要**读取或写入 `.env*` 文件内容。
  - **不要**执行 `sudo`、`chmod 777` 等提权操作。
- `session-start.sh` 中的"显示分支、最近提交、活跃冲刺、未解决 Bug"逻辑
  Codex 没有等价钩子。需要这些上下文时，请在任务开始时主动运行：
  - `git status -sb`、`git log --oneline -5`
  - 列出 `production/sprints/sprint-*.md`、`production/milestones/*.md` 的最新文件
  - 检查 `production/session-state/active.md` 是否存在并阅读

## 编码与文件约定

- 默认 ASCII；只有当文件本身就用中文/其他 Unicode 时才保留。
- 仓库内大量 Markdown 文档为简体中文，新增文档与之保持一致。
- 改动文件前先阅读邻近文件以理解现有风格与模式，再做最小化变更。
- 修改提交信息、文档时遵循 [CLAUDE.md](CLAUDE.md) 与本文件中的协作协议。

## 第一次使用？

如果项目尚未配置引擎且没有游戏概念，请按 `/start` 技能引导：
阅读 [.claude/skills/start/SKILL.md](.claude/skills/start/SKILL.md) 后逐步与用户对话。
