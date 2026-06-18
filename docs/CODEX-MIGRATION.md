# Codex 迁移说明

本仓库最初为 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 设计，
正在向 [Codex](https://github.com/openai/codex) 迁移。本文档记录差异、
当前迁移进度与后续优化项。

## 当前状态

- ✅ 第 1 步：建立 `AGENTS.md`，作为 Codex 主上下文，替换 `CLAUDE.md` 的
  `@import` 引用为普通 Markdown 链接，并加入"角色 / 技能 / 规则"使用说明。
- ✅ README 入门段补充 Codex 用法（`codex` CLI），保留原 Claude Code 路径。
- ✅ 第 2 步：在 [.githooks/](../.githooks/) 中提供 `pre-commit` / `pre-push`
  包装，复用原 `validate-*.sh` 的逻辑。启用：
  `git config core.hooksPath .githooks`。
- ✅ 第 3 步：在 11 个目标子目录下放置薄壳 `AGENTS.md`，链回
  `.claude/rules/<rule>.md` 单一事实源；Codex 在编辑这些路径时会
  自动叠加加载，等价复刻 Claude Code 的"路径范围自动注入"。
- ✅ 第 4 步：仓库已声明为 Codex 本地 plugin
  （[.codex-plugin/plugin.json](../.codex-plugin/plugin.json)），
  并通过 [work/generate_codex_skills.py](../work/generate_codex_skills.py)
  在 [skills/](../skills/) 下生成 37 个薄壳 SKILL.md（仅 frontmatter +
  指回 `.claude/skills/<name>/SKILL.md` 链接）。已通过
  `validate_plugin.py` 与 `quick_validate.py` 校验。

## 已知遗留

- 已修复：上游 fork 的 `.claude/skills/{brainstorm,changelog,code-review,design-system,gate-check}/SKILL.md` 原本被翻译流程残留的占位文字覆盖。通过 [work/fix_broken_skills.py](../work/fix_broken_skills.py) 修复：`gate-check` 剥掉外层 markdown 围栏后保留中文翻译；其余 4 个从上游英文原版（`Donchitos/Claude-Code-Game-Studios:main`，作为 remote `donchitos` 拉入）恢复。修复后重跑了 Codex 薄壳生成器，37 个 SKILL.md 与 plugin manifest 全部通过校验。
  > 副作用：这 4 个文件目前是英文，与仓库其余中文 cn-localization 风格不一致；如果需要中文版可后续单独翻译，再重跑生成脚本。
- agent / skill frontmatter 中 Codex 不识别的字段（`model`、`maxTurns`、
  `disallowedTools`、`allowed-tools`、`argument-hint`、`user-invocable`）
  目前保留在原 `.claude/` 文件中，Codex 不会读取也不会报错；如果未来
  完全弃用 Claude Code，可批量清理。

## 关键差异速查

| Claude Code | Codex 对应 | 迁移做法 |
|------------|-----------|---------|
| `CLAUDE.md`（自动加载） | `AGENTS.md`（自动加载） | 已新增 `AGENTS.md`，原 `CLAUDE.md` 保留以兼容 Claude Code |
| `@path/to/file.md` 自动 import | 无 | 改为普通 Markdown 链接，由模型按需阅读 |
| `.claude/agents/*.md` 子代理 | 无一等子代理；可作角色提示词使用 | 文件保留；`AGENTS.md` 中说明使用方式 |
| `.claude/skills/*/SKILL.md` 斜杠命令 | Codex skills（按描述匹配，无 `/` 触发） | 暂保留原结构；后续可迁至 `.codex/skills/` 或 `$CODEX_HOME/skills/` |
| `.claude/rules/` 路径范围规则 | 子目录 `AGENTS.md` 叠加 | 暂以索引表方式声明；后续可拆分为多个 `AGENTS.md` |
| `.claude/hooks/*.sh`（SessionStart / PreToolUse 等） | 无对应生命周期钩子 | 提交/推送类改造为 Git hook；其余在 `AGENTS.md` 中以"任务开始时主动检查"形式表达 |
| `settings.json` 的 `permissions.allow / deny` | Codex sandbox + 升级审批 | `AGENTS.md` 中声明禁用清单；真正约束由 sandbox 提供 |
| `statusLine`（自定义状态栏） | 无 | 已停用，无需迁移 |
| `AskUserQuestion` 工具 | Plan 模式下的 `request_user_input`，Default 模式下直接提问 | 在技能/代理描述中提到时按场景替换 |

## 工作流提示

- 在 Codex 中开新会话时，主代理会自动读取 `AGENTS.md`。
- 需要执行某个原斜杠命令工作流时，向 Codex 直接说明意图，例如：
  "请按 `/sprint-plan` 技能流程，帮我做下个冲刺规划。"
- 涉及编辑代码或文档前，Codex 会按 `AGENTS.md` 中声明的协作协议
  （提问 → 选项 → 决定 → 草稿 → 审批）行事。

## 反馈

如果在使用过程中发现 Claude Code 行为与 Codex 行为出现明显不一致，
请在仓库 issue 中记录，便于后续完善迁移。
