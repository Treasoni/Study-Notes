# 过时分析：如何使用Claude code.md「二、跳过登录（免认证启动）」

## 基本信息
- **文件**: `AI学习/Claude Code 教程/01-入门/如何使用Claude code.md`
- **目标章节**: `## 二、跳过登录（免认证启动）`（L147-255）
- **本次更新**: 2026-08-03
- **核对依据**: 官方文档 code.claude.com/docs/en/{authentication,settings,env-vars,llm-gateway-connect}

## 过时内容清单

| # | 位置 | 过时内容 | 处理 |
|---|------|---------|------|
| 1 | 章节导语 | "有 4 种方式" — 现已不止 4 种，且缺少官方认证优先级 | 🔄 更新导语 + 新增优先级表 |
| 2 | 方式一 apiKeyHelper | 缺少 2026 新增行为：Windows 用 cmd、TTL 刷新（`CLAUDE_CODE_API_KEY_HELPER_TTL_MS`）、失败报错（v2.1.208+ `Your apiKeyHelper script is failing`）、同时发 `X-Api-Key` + `Authorization: Bearer`、适用面（CLI/VS Code/SDK/GitHub Actions，不含 Desktop） | 🔄 补充 |
| 3 | 方式二 primaryApiKey | ⭐ 标记为官方推荐；但**不在官方 6 层认证优先级中**，v2.0.37+ 多版本不读取（issue #11631），Docker 沙箱报"凭据冲突" | 🔄 降级为「旧方案，已不可靠」并加 warning |
| 4 | 方式三 env 字段 | 缺少 `ANTHROPIC_BASE_URL` 指向非官方域名的副作用（Remote Control 关闭 v2.1.196+、MCP 工具搜索默认关闭）；未说明 settings `env` 覆盖 shell export；模型名 `claude-3.5-sonnet` 过时 | 🔄 补充说明 + 更新模型示例 |
| 5 | 方式四 CC-Switch | "50K+ Star" → 实际 **123.9K**；支持工具由 4 种增至 **8 种**（含 Grok Build / OpenClaw / Hermes Agent）；新增 v3.16.1、MCP/Skills 统一管理、本地代理自动熔断、Session 管理、Deep Link 导入、Windows Portable 版 | 🔄 更新 |
| 6 | 整章 | 未提「跳过首启引导」`hasCompletedOnboarding`（`~/.claude.json`） | ➕ 新增方式 |
| 7 | 整章 | 未提官方 CI 长期 token：`claude setup-token` + `CLAUDE_CODE_OAUTH_TOKEN` | ➕ 新增方式 |
| 8 | 整章 | 未提 `/status` 查看当前认证方式、`/config` 的 "Use custom API key" 开关 | ➕ 补充 tip |

## 保留不动
- 方式一 apiKeyHelper 基础 JSON 配置、脚本示例
- 方式三 env 字段的 OpenRouter / LiteLLM+Ollama 两组配置结构
- 方式四 CC-Switch 安装表、配置步骤、冲突 warning 的主体
- permissions 可选值说明

## 风险
- 模型名为动态示例（OpenRouter ID 可能变化），已加"按当前模型填写"说明
- 版本号/Star 数为动态值，报告标注自检方式
