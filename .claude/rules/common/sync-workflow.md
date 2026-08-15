# Claude Code / Claude Code Sync Workflow

本项目以 `.codex/` 作为新功能编辑入口，但 Claude Code 也必须保持可用。

## When To Sync

修改以下内容后必须运行同步：

- `.codex/skills/**`
- `.codex/agents/**`
- `.claude/rules/**`
- `.claude/scripts/**`
- `.codex/platform/**`
- `.claude/workflows/**`
- `CLAUDE.md` 中改变了工作流、skill 路由或规则路径

## Command

```bash
.claude/scripts/sync-codex-to-claude.sh
```

同步后必须验证镜像没有漂移：

```bash
.claude/scripts/sync-codex-to-claude.sh --check
```

## What It Does

1. 将可迁移资源从 `.codex/` 复制到 `.codex/`，并删除非例外的陈旧镜像文件。
2. 自动把复制后文件里的 `.codex` 路径改成 `.codex`。
3. 保留 Claude Code 专属 hooks 文档，不用 Claude Code hooks 覆盖。
4. 保留 Claude Code 专属 `skill-creator`（如存在）。
5. 同步 `.codex/platform/` 到 `.codex/platform/`，保持 manifest 注册表和策略可用。
6. 同步 `.claude/workflows/` 到 `.claude/workflows/`，保持命名工作流定义可用。

`--check` 会在临时目录构建预期镜像并只报告差异，不会修改 `.codex/`。它保留 Claude Code 专属的 `skill-creator` 和 hooks 文件，包括其中的符号链接。

## Boundary

- `.codex/settings.json` 和 `.claude/hooks/` 不同步到 `.codex/`。
- Claude Code hooks 继续由 `.claude/rules/common/hooks.md` 和 Claude Code 自己的 settings 管理。
- 如果用户明确要求 Claude Code hooks 也变更，再单独维护。
