# Codex / Claude Code Sync Workflow

本项目以 `.codex/` 作为新功能编辑入口，但 Claude Code 也必须保持可用。

## When To Sync

修改以下内容后必须运行同步：

- `.codex/skills/**`
- `.codex/agents/**`
- `.codex/rules/**`
- `.codex/scripts/**`
- `AGENTS.md` 中改变了工作流、skill 路由或规则路径

## Command

```bash
.codex/scripts/sync-codex-to-claude.sh
```

## What It Does

1. 将可迁移资源从 `.codex/` 复制到 `.claude/`。
2. 自动把复制后文件里的 `.codex` 路径改成 `.claude`。
3. 保留 Claude Code 专属 hooks 文档，不用 Codex hooks 覆盖。
4. 保留 Claude Code 专属 `skill-creator`（如存在）。

## Boundary

- `.codex/hooks.json` 和 `.codex/hooks/` 不同步到 `.claude/`。
- Claude Code hooks 继续由 `.claude/rules/common/hooks.md` 和 Claude Code 自己的 settings 管理。
- 如果用户明确要求 Claude Code hooks 也变更，再单独维护。
