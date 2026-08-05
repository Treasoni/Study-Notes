# 更新计划：如何使用Claude code.md「二、跳过登录（免认证启动）」

## 更新范围
- **动作**: patch-in-place（局部更新指定章节）
- **目标**: 同步官方最新认证方案，纠正已不可靠的 primaryApiKey，保留原结构与写作风格
- **保留**: 章节标题 `## 二、跳过登录（免认证启动）`（内有双链锚点引用，必须不变）

## 修改项

| # | 操作 | 说明 |
|---|------|------|
| 1 | 重写章节导语 | 4 种 → 6 种方式；新增「官方认证优先级」表（6 层）+ `/status` 自查 tip |
| 2 | 方式一 apiKeyHelper | 保留基础配置；新增 2026 行为 callout（shell 类型、双头发送、TTL、失败报错、适用面） |
| 3 | 方式二 env 字段 | 升级为"⭐ 最常用"；补充 settings `env` 覆盖 shell、`ANTHROPIC_BASE_URL` 副作用；模型示例更新 |
| 4 | 新增方式三 hasCompletedOnboarding | 跳过首启登录引导（`~/.claude.json`，建议同时给 `theme`） |
| 5 | 原方式二 primaryApiKey 降为方式四 | 标注 ⚠️ 旧方案，加 2026 状态 warning，链接 issue #11631 |
| 6 | 新增方式五 claude setup-token | 官方 CI 长期 token + `CLAUDE_CODE_OAUTH_TOKEN` |
| 7 | 方式六 CC-Switch | Star → 124K+、v3.16.1、8 工具、新增功能点、Windows Portable |
| 8 | 章节末尾 | 新增 Desktop Developer Mode 免登录接第三方模型 tip |
| 9 | frontmatter | `updated: 2026-07-31` → `2026-08-03` |
| 10 | 更新记录 | 追加 2026-08-03 变更行 |

## 参考资料
- 官方 Authentication（认证优先级 / apiKeyHelper / setup-token）：https://code.claude.com/docs/en/authentication
- 官方 Settings：https://code.claude.com/docs/en/settings
- 官方 Env Vars（ANTHROPIC_* / CLAUDE_CODE_API_KEY_HELPER_TTL_MS）：https://code.claude.com/docs/en/env-vars
- 官方 LLM Gateway（Desktop Developer Mode / base URL 副作用）：https://code.claude.com/docs/en/llm-gateway-connect
- primaryApiKey 回归 issue：https://github.com/anthropics/claude-code/issues/11631
- CC-Switch 仓库：https://github.com/farion1231/cc-switch
- 社区 hasCompletedOnboarding 方案：阿里云百炼 / ccgo
