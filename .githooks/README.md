# Git hooks（Codex 适配）

本目录下的 Git 钩子是 [.claude/hooks/](../.claude/hooks/) 中两个验证脚本的
轻量包装：在普通 `git commit` / `git push` 时复用同一套校验逻辑，
让 Codex（或任何不走 Claude Code 的提交流程）也能享受同样保护。

## 启用

在仓库根目录执行一次：

```bash
git config core.hooksPath .githooks
```

之后 `git commit` / `git push` 会自动触发 [pre-commit](pre-commit) 与
[pre-push](pre-push)。它们最终调用：

- `pre-commit` → [.claude/hooks/validate-commit.sh](../.claude/hooks/validate-commit.sh)
- `pre-push`   → [.claude/hooks/validate-push.sh](../.claude/hooks/validate-push.sh)

## 跳过单次校验

如果你确实需要绕过（极少情况）：

```bash
git commit --no-verify
git push --no-verify
```

## Windows 注意

脚本是 `#!/bin/bash`，需要 Git for Windows 自带的 Git Bash。
如果安装了 Git for Windows，无需额外配置。
