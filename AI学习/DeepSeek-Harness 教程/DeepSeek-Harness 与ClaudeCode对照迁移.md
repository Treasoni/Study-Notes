---
title: "DeepSeek-Harness 与ClaudeCode对照迁移"
tags: [deepseek-harness, claude-code, ai, agent, 教程, 对比, 迁移]
created: 2026-08-13
updated: 2026-08-13
status: new
source_project: deepseek-harness
---

# DeepSeek-Harness 与 Claude Code 对照迁移：换还是留？

> [!summary] 本章导读
> 上一章讲完 [[DeepSeek-Harness 配置体系|配置体系]]，本章解决最实际的问题：**到底换不换？** 用三张表（概念 / 成本 / 性能）把 [[Claude Code MOC|Claude Code]] 与 dsh 摆在一起，再给三选迁移策略与选择建议。

## 4.1 概念对照表

| 维度 | Claude Code | deepseek-harness (dsh) |
|---|---|---|
| 定位 | 开箱即用的闭源 CLI 成品 | 开源（MIT）可组装的 agent 运行时 |
| 架构 | 单体核心 + 扩展 | 一切皆插件，无特权核心 |
| 一次性任务 | `claude -p "..."` | `dsh --profile headless "..."` |
| 配置文件 | `settings.json` / `CLAUDE.md` / `.mcp.json` | YAML 补丁树（bundle / `cordis.patch.yml` / `--patch`）+ Profile + Agent Preset |
| 权限模式 | 权限提示 + 命令行 flag | `workspace-write` 默认预设 + `DSH_PERMISSION_MODE` |
| 工作区根 | 启动目录 | 调用目录（所有模式） |
| 上下文文件 | 自动加载 `CLAUDE.md` | 自动加载 `AGENTS.md` 或 `CLAUDE.md`（65,536 字节预算） |
| 模型 | 绑定 Claude | 默认 DeepSeek V4，可换 ~40 家 + OpenAI-compatible |
| MCP | 成熟支持 | 仅桥 tools（stdio + streamable-http），Resources/Prompts 尚无消费者 |
| 成熟度 | 成熟稳定 | developer preview，有破坏性变更 |

## 4.2 成本对比

假设 90% 输入缓存命中、每任务 80K 输入 + 20K 输出[^1]：

| 模型 | 输入价 /1M | 输出价 /1M | 每任务成本 | 每 $100 任务数 |
|---|---|---|---|---|
| Claude Opus 4.8 | $5.00 | $25.00 | ~$0.54 | ~185 |
| Claude Sonnet 4.6 | — | — | ~$0.13 | ~770 |
| DeepSeek V4 Pro | $0.435 | $0.87 | ~$0.021 | ~4,760 |
| DeepSeek V4 Flash | $0.14 | $0.28 | ~$0.007 | ~14,300 |

- 输出定价差距约 **28 倍**（V4 Pro $0.87 vs Opus $25.00 /1M）；
- 规模化：每天 5,000 任务，Opus 月成本约 $79,000 vs V4 Pro 约 $3,150。

> [!tip] 大白话
> 同样跑 100 美金，Claude Opus 只够约 185 个任务，V4 Flash 能跑约 14,300 个——差了两个数量级。

## 4.3 性能对比

| 基准 | Claude Opus 4.8 | DeepSeek V4 Pro |
|---|---|---|
| SWE-bench Pro（仓库级） | 69.2% | 55.4% |
| SWE-bench Verified | 88.6% | 80.6% |
| LiveCodeBench Pass@1 | 88.8% | 93.5% |
| Terminal-Bench | 65.4% | 67.9% |
| MCPAtlas Public（工具调用） | ~73.6 | 73.6（平手） |

> [!note] 表注：V4 Pro vs V4 Pro Max
> 表中 SWE-bench Verified（80.6%）与 LiveCodeBench（93.5%）两个数据点来自 **V4 Pro Max**（V4 Pro 的高配置档位），其余来自 V4 Pro 本体。列头统一写作 V4 Pro，对比时留意该档位差异。

结论：**harness 与工具 schema 设计比模型选择更重要**；Opus 在仓库级多文件架构一致性领先，V4 Pro 在有界算法任务与终端代理任务上反超[^1]。

## 4.4 三选迁移策略

1. **整体换 harness**：`npx @deepseek-ai/dsh web` 直接上手 dsh，配置从 `settings.json` / `CLAUDE.md` 迁移到 `cordis.patch.yml` / Agent Preset；
2. **DeepClaude 模式（保留 Claude Code，换底模）**——DeepSeek 官方支持[^1]：

```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_API_KEY="your-deepseek-api-key"
```

结构性便宜 10–25 倍。权衡：失去 Opus 特有推理行为，部分 Anthropic API 参数映射不完整；

3. **按复杂度路由**（核心建议）：
- 琐碎改动/样板/单文件修复/测试编写 → **V4 Flash**；
- 标准功能实现与调试 → **V4 Pro**；
- 多文件架构重构、安全敏感变更 → **Opus**；
- 默认用 DeepSeek 后端跑所有会话，保留 Anthropic key 供显式升级（"95% 任务不付 Opus 价"）。

## 4.5 选择建议

- **选 Claude Code**：跨模块仓库级重构、团队已有 Claude Code 肌肉记忆、安全审计/支付系统/生产数据库迁移等高风险任务、需要 Anthropic 专属功能（子代理、上下文压缩、安全对齐）[^1]；
- **选 DeepSeek/dsh**：高频低成本循环（PR 审查、测试生成、文档更新）、并行子代理（16 个 V4 Flash worker 经济可行）、自托管/数据主权（V4 权重 MIT 可下载）、构建非编码类自定义 agent、非开发者想要 GUI。

## 4.6 迁移前置提醒

> [!warning] V4 协议差异先看这里
> DeepSeek V4 协议差异详见 [[DeepSeek-Harness 常见坑与速查|第五章 5.3]]：thinking 默认开启（烧 token）、多轮必须回传 `reasoning_content`、必须设 `max_tokens`、thinking 下 `tool_choice` 只能 `auto`。

---

## 本章小结

> [!summary]
> - 概念上 dsh 是「开源可组装运行时」，Claude Code 是「闭源成品」，配置文件与权限模型差异最大；
> - 成本上 V4 Flash/Pro 相对 Claude 有 7–77 倍优势——**7 倍下限来自 Sonnet ~$0.13 vs V4 Pro ~$0.021 ≈ 7×，77 倍上限来自 Opus ~$0.54 vs V4 Flash ~$0.007 ≈ 77×**，「每 $100 任务数」差两个数量级；
> - 性能上 Opus 领先仓库级重构，V4 Pro 反超有界算法与终端任务；
> - 三选策略：整体换 / DeepClaude 保留界面换底模（便宜 10–25 倍）/ 按复杂度路由（推荐）；
> - 高风险与仓库级重构留 Claude Code，高频低成本循环与并行子代理适合 dsh。

下一章收尾：[[DeepSeek-Harness 常见坑与速查|常见坑与速查]]。

---

[^1]: 素材来源：DeepSeek Harness 官方仓库与文档（2026-08-13 收集）。
