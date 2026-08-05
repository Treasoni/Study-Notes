# 更新报告

## 笔记信息
- **标题**: Claude Code 使用指南
- **路径**: `AI学习/Claude Code 教程/01-入门/如何使用Claude code.md`
- **目标章节**: `## 二、跳过登录（免认证启动）`
- **前次更新**: 2026-07-31
- **本次更新**: 2026-08-03
- **动作**: patch-in-place（局部更新）

## 更新摘要

| 类型 | 内容 | 说明 |
|------|------|------|
| 🔄 更新 | 章节导语 | 4 种 → 6 种方式；新增官方认证优先级表（6 层）+ `/status` 自查 tip |
| 🔄 更新 | 方式一 apiKeyHelper | 保留基础配置，新增「2026 新增行为」callout：shell 类型（Win 用 cmd）、双头发送（`X-Api-Key` + `Authorization: Bearer`）、`CLAUDE_CODE_API_KEY_HELPER_TTL_MS` 刷新间隔、v2.1.208+ 失败报错 `Your apiKeyHelper script is failing`、适用面（CLI/VS Code/SDK/GitHub Actions，不含 Desktop） |
| 🔄 更新 | 原方式三 env 字段 → 方式二 | 升级为「⭐ 最常用」；补充 settings `env` 覆盖 shell export、`ANTHROPIC_BASE_URL` 指向非官方域名的副作用（Remote Control 关闭 v2.1.196+、MCP 工具搜索默认关闭需 `ENABLE_TOOL_SEARCH=true`）；OpenRouter 模型示例更新 |
| ➕ 新增 | 方式三 hasCompletedOnboarding | 跳过首启登录引导（`~/.claude.json`，建议同时给 `theme` 值）；注明 ccgo 同款机制 |
| 🔄 更新 | 原方式二 primaryApiKey → 方式四 | 降级为「旧方案，已不可靠」⚠️；加 2026 状态 warning：不在官方优先级、v2.0.37+ 多版本失效（issue #11631）、Docker 凭据冲突警告 |
| ➕ 新增 | 方式五 claude setup-token | 官方 CI 长期 token（`CLAUDE_CODE_OAUTH_TOKEN`，1 年有效期，`--bare` 不读） |
| 🔄 更新 | 方式六 CC-Switch | Star 50K+ → 124K+；新增 v3.16.1、8 种工具（+Grok Build/OpenClaw/Hermes Agent）、MCP/Skills 统一管理、本地代理自动熔断、Session 管理、Deep Link 导入、Windows Portable 版 |
| ➕ 新增 | 章节末尾 tip | Claude Code Desktop Developer Mode 免登录接第三方模型（Help → Troubleshooting → Enable Developer Mode → Developer → Configure Third-Party Inference） |
| 🔄 更新 | frontmatter `updated` | 2026-07-31 → 2026-08-03 |
| ➕ 新增 | 更新记录 | 追加 2026-08-03 变更行 |

## 关键事实核对（来源）
- **官方认证优先级 6 层**：云厂商 > `ANTHROPIC_AUTH_TOKEN` > `ANTHROPIC_API_KEY` > `apiKeyHelper` > `CLAUDE_CODE_OAUTH_TOKEN` > 订阅 OAuth（[官方 Authentication](https://code.claude.com/docs/en/authentication)）
- **`apiKeyHelper` 仍为官方推荐**，settings 文档含 `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`（[官方 Settings](https://code.claude.com/docs/en/settings)）；v2.1.208+ 失败报错、双头发送（[官方 Gateway 文档](https://code.claude.com/docs/en/llm-gateway-connect)）
- **`primaryApiKey` 不再列入官方认证**；回归 issue：[anthropics/claude-code#11631](https://github.com/anthropics/claude-code/issues/11631)；Docker 官方排障文档对 `.claude.json` 中的 `primaryApiKey` 报「凭据冲突」警告
- **`ANTHROPIC_BASE_URL` 副作用**：Remote Control 关闭（v2.1.196 起）、MCP 工具搜索默认关闭（[官方 Env Vars](https://code.claude.com/docs/en/env-vars)）
- **`claude setup-token`**：官方长期 token，1 年有效期，需订阅（[官方 Authentication](https://code.claude.com/docs/en/authentication)）
- **`hasCompletedOnboarding`**：社区通用方案（阿里云百炼、ccgo），非官方正式文档条目，标注为「跳过首启引导」辅助手段
- **CC-Switch**：[GitHub 仓库](https://github.com/farion1231/cc-switch) 实测 Star 123.9K、v3.16.1、支持 8 工具、Windows 提供 .msi + Portable

## 未处理事项 / 风险
- `ANTHROPIC_MODEL` 为平台相关示例名，已注明「按你当前可用的模型名填写」；OpenRouter 具体 ID 以平台为准。
- Star 数、版本号、工具支持列表为动态值，建议以官方仓库/自检为准。
- 桌面端 Developer Mode 为可选附加 tip，未深挖 Desktop 端完整配置（本笔记定位为 CLI 速查）。
- 未处理章节之外的其他过时内容（如版本号 v2.1.220 为动态值），非本次范围。

## MOC 同步
- **MOC 文件**: `AI学习/Claude Code 教程/Claude Code MOC.md`、`AI学习/00-索引/AI学习 MOC.md`
- **操作**: 索引条目描述「安装、免登录、配置、日常速查、记忆系统」仍准确，无需修改。

## 资料来源
- [Claude Code 官方 Authentication](https://code.claude.com/docs/en/authentication)
- [Claude Code 官方 Settings](https://code.claude.com/docs/en/settings)
- [Claude Code 官方 Env Vars](https://code.claude.com/docs/en/env-vars)
- [Claude Code 官方 LLM Gateway](https://code.claude.com/docs/en/llm-gateway-connect)
- [anthropics/claude-code issue #11631](https://github.com/anthropics/claude-code/issues/11631)
- [farion1231/cc-switch](https://github.com/farion1231/cc-switch)
- [阿里云百炼 Claude Code 配置](https://help.aliyun.com/zh/model-studio/claude-code)
