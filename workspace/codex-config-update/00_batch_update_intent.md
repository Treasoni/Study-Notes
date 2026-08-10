# 批量更新意图 - Codex 笔记重构为 Claude Code 教程风格

> 工作流：batch-note-update-flow
> 运行标识：update-codex-config
> 项目标识：codex-config-update
> 创建时间：2026-08-10

## 意图 YAML

```yaml
source_path: "AI学习/Codex/"
source_scope: all
source_glob: "*.md"
update_goal: "结构镜像 AI学习/Claude Code 教程/ 子目录（01-入门/02-基础功能/03-进阶应用/04-高级功能），每篇按 Claude Code 教程模板完整重排，文件名去序号改描述性名称；内容保留，仅重排结构与排版"
destination_mode: patch-in-place   # 就地改 vault 内笔记，移动+改名
batch_size: 3
shared_research: no                 # 纯排版重构，无需新资料
moc_path: "AI学习/Codex/Codex MOC.md"
```

## 目标结构（镜像 Claude Code 教程）

```
AI学习/Codex/
├── Codex MOC.md                  # ← Codex 配置体系 MOC.md 重命名 + 重写
├── sortspec.md                   # 新建
├── 01-入门/
│   └── Codex 配置哲学概览.md      # ← 01 配置哲学概览.md
├── 02-基础功能/
│   ├── config.toml 核心配置.md    # ← 02 config.toml 核心配置.md
│   └── Codex CLI 与调试.md        # ← 07 CLI 与调试.md
├── 03-进阶应用/
│   ├── AGENTS.md 分层体系.md      # ← 03 AGENTS.md 分层体系.md
│   ├── Skills 技能系统.md         # ← 04 Skills 技能系统.md
│   ├── Agents 与 MCP.md           # ← 05 Agents 与 MCP.md
│   └── Hooks 与插件.md            # ← 06 Hooks 与插件.md
└── 04-高级功能/
    ├── 对照表与迁移实战.md        # ← 08 对照表与迁移实战.md
    └── 快速参考卡片.md            # ← 附录 快速参考卡片.md
```

## 分级逻辑

配置哲学 → 入门；核心配置 + CLI → 基础功能；AGENTS/Skills/Agents/MCP/Hooks → 进阶应用；对照迁移 + 速查 → 高级功能。

## 范围边界

- 不触碰 `AI学习/Claude Code 教程/` 与 `AI学习/01-基础概念/` 等无关笔记。
- `AI学习/03-技术专题/Codex手动配置指南.md` 不在本次范围。
- 不修改 `workspace/codex-config/` 里的旧章节文件（保留作为历史产物）。
