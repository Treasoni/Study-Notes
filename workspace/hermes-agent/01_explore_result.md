# Hermes Agent（Nous Research）— 探测式收集结果

> 阶段 1 · 2026-08-28 · 项目 `workspace/hermes-agent/`

## 方向菜单

| 方向 | 说明 | 素材充足度 |
|------|------|-----------|
| **A. 定位与核心机制** | 是什么、学习闭环、skill 自改进、记忆/检索、Honcho 用户建模、与 Claude Code / OpenClaw 差异 | 高（tier1 官方 + 联创专访） |
| **B. 安装与第一跑** | Windows 原生 / WSL2 / Linux / Termux 安装、模型 Provider、CLI/TUI、多平台网关 | 高（tier1 官方文档） |
| **C. 核心机制实战** | skill 创建/自改进工作流、记忆与跨会话检索、定时任务、subagent/RPC | 中（部分待 P2 专项补采） |
| **D. 部署进阶** | 七种终端后端、serverless 休眠、Docker 加固、远程凭据安全 | 中高（官方 + 实战教程） |
| **E. 常见坑与最佳实践** | Windows 坑、杀软误报、API key、版本漂移 | 中（issue + 社区） |

## 候选来源（去重后 14 条）

### Tier 1（官方 / 一手，10 条）

1. **GitHub README** — 定位、特性、安装、平台支持 — 5 分
   https://github.com/NousResearch/hermes-agent
2. **官方安装文档** — 各平台安装、`hermes setup` / `hermes model` / `hermes gateway setup` — 5 分
   https://hermes-agent.nousresearch.com/docs/getting-started/installation/
3. **Memory Providers 文档** — MEMORY.md / USER.md 字符限制、SQLite FTS5 session_search — 5 分
   https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
4. **Terminal Backends 文档** — 7 种后端、TERMINAL_ENV 配置、Docker 安全加固 — 5 分
   https://hermes-agent.nousresearch.com/docs/user-guide/features/terminal-backends
5. **Issue #16201** — Windows / Git Bash 已知问题、杀软实时扫描持锁（os error 5） — 5 分
   https://github.com/NousResearch/hermes-agent/issues/16201
6. **Honcho Memory 文档** — dialectic 用户建模、5 工具、context/tools/hybrid 召回 — 4 分
   https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho
7. **integrations/providers.md** — Nous Portal / OpenRouter / OpenAI / 自建端点配置 — 4 分
   https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md
8. **messaging/index.md** — 统一 gateway、20+ 平台、systemd/launchd、Docker 持久化 — 4 分
   https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/index.md
9. **Termux 指南** — Android 安装路径与能力限制（voice/Playwright 不支持） — 4 分
   https://hermes-agent.nousresearch.com/docs/getting-started/termux
10. **commit febc4cf（v0.15.0）** — 移除 Vercel Sandbox、后端数量 7→6 再回 7 的版本漂移证据 — 4 分
    https://github.com/NousResearch/hermes-agent/commit/febc4cfec0a79b175a430304765473c97e10622f

### Tier 2（可靠实现/报道，3 条）

11. **DevelopersIO（Classmethod）** — 从源码读"自我改进"：成长的是技能层而非模型权重；v0.16 转向技能筛选与折叠 — 4 分
    https://dev.classmethod.jp/en/articles/hermes-agent-self-improving-code-reading/
12. **ZDNet 中国专访** — Nous 联创谈与 Claude Code / Codex 的差异化、对齐哲学、harness 与权重 — 4 分
    https://www.zhiding.cn/models/2026/0804/3195327.shtml
13. **阿里云开发者社区** — 多后端（local/Docker/SSH/Modal/Daytona）选型与运维、SSH 同步、凭据 ignore 策略 — 4 分
    https://developer.aliyun.com/article/1758830

### Tier 3（社区实操，1 条）

14. **CSDN** — Windows 上 7 个坑：杀软误删 uv-trampoline、白名单整个 `%LOCALAPPDATA%\hermes` 目录 — 3 分
    https://xdr630.blog.csdn.net/article/details/163467493

## 覆盖缺口

- **定时任务（cron）与 subagent / Python RPC** 的实操细节分散，P2 需专项补采
- **skill 创建/自改进的完整用户侧工作流**：需深读官方文档 + 代码阅读文章
- **Windows 原生安装完整步骤**：官方标注 early beta，需社区文章补充

## 已知冲突（写笔记时需标注版本依赖）

- **后端数量**：v0.15.0 曾移除 Vercel Sandbox（7→6），后续文档又对齐回 7。涉及 Vercel Sandbox 的配置（VERCEL_TOKEN 等）随版本失效。
- **发布时间线**：仓库创建 2025-07-22，公开产品化发布约 2026-02/03（v0.2.0 于 2026-03-12）。引用时应区分"仓库创建"与"公开发布"。
- **"唯一带学习循环"**：官方营销表述；联创访谈承认主要竞品为 OpenClaw / Claude Code / Codex。

## P2 预估范围

- 深读 3-5 个核心来源：README、安装文档、memory-providers、terminal-backends、providers
- 按用户所选方向补齐缺口来源
- 产出 `02_deep_research.md`：scope / source table / claim-map / 矛盾 / 实战指引 / 开放问题
