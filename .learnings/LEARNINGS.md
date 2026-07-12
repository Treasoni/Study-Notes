# LEARNINGS.md

## [2026-06-01] OpenSpec 学习笔记 - Session Learnings

### 流程方面
- Phase 0 需求发现：对于 GitHub 项目类主题，先快速了解项目基本信息再问问题，能提出更精准的需求问题
- 混合笔记类型 concept + cheat_sheet 适合"入门 + 速查"场景，实战示例部分用教学性场景更灵活
- Canvas 知识地图对项目类笔记很有价值，能直观展示概念关系

### 工具方面
- 对于 GitHub 项目无法用 WebFetch 时，可通过 GitHub API (`api.github.com/repos/...`) 获取项目信息
- opencli 提供丰富的搜索源（google/search, github 等），但 collector subagent 需要明确指定可用源
- beautify 阶段应主动询问用户是否需要 Canvas/Base 作为可选配置

### 内容方面
- OpenSpec 的核心是 Spec-Driven Development（SDD），与当前 Study System 的 phase-based workflow 有理念上的共鸣
- OpenSpec 对比线：vs Spec Kit（重但灵活度低）、vs Kiro（锁定生态）、vs 无规范（不可预测）

## [2026-07-11] Codex 手动配置指南 - Session Learnings

### 流程方面
- `practice + compare` 混合笔记类型在工具对比类主题中效果很好——每个领域同时提供实操步骤和对比表，特别适合有同类工具经验的读者
- Codex 相关资料分布在 `learn.chatgpt.com` 域名下（已从 `developers.openai.com` 迁移），收集时需注意域名变更

### 工具方面
- Codex 官方 hooks 文档缺失，需依赖社区资源（GitHub 仓库），这个缺口应在前置搜索策略中就考虑进去

### 内容方面
- Codex 与 Claude Code 的核心差异：TOML vs JSON 配置格式、AGENTS.md vs CLAUDE.md、不支持自定义 slash 命令、内置 OS 级 sandbox
- Codex 的 Skills 与 Claude Code 格式兼容（Agent Skills 开放标准），这是迁移的重要优势
