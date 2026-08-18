# 01 探测结果 · 如何写 subagent（DeepSeek-Harness）

> 项目：deepseek-harness-subagent ｜ 阶段：P1 探测式收集 ｜ 检索日期：2026-08-16
> 视角：官方文档与架构 / 实战示例与开发指南 / 坑与生态·社区实践（3 个并行 subagent）

---

## 方向菜单

| 选项 | 方向 | 内容 | 素材适配 |
|---|---|---|---|
| **A（推荐）** | 全流程：概念 → 写 provider → 工具化 | 心智模型（ctx.subagents 三层结构）→ 写一个最小 SubagentProvider 插件 → dsh-tool-subagent 绑定成工具 → control/report 补全 | 最贴合「概念理解+上手」，产出可直接照抄的完整链路 |
| **B** | 深度聚焦：写 provider 插件 | SubagentProvider 契约、capabilities、start/prepareContinuable、in-process vs out-of-process（acp/dsh-sdk 样板）、深度机制 | 以「能写第二个 provider」为目标，代码占比最高 |
| **C** | 配置优先：用现成 provider + 对照 Claude Code | 概念 + 如何选 provider、cordis.patch.yml 挂载、dsh-tool-subagent 全配置、与 Claude Code subagent 映射 | 不深入写 provider，偏概念与迁移 |
| **D** | 生态与坑：社区实践 + 边界 | 第三方插件（dsh-background-agents / product-subagents / dsh-subagent-max）、已知坑清单、讨论区边界提醒 | 偏「别人怎么用 + 别踩什么坑」 |

---

## 去重后候选源

### 官方（Tier: official）

| # | 标题 | URL | 评分 | 相关性 |
|---|---|---|---|---|
| 1 | Subagent 子系统设计文档（EN） | https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/subagent.md | 5 | 最权威：SubagentProvider 契约、ctx.subagents 注册表、capabilities、one-shot/continuable、delegationDepth、事件模型 |
| 2 | Subagent 子系统设计文档（中文） | https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/subagent.zh.md | 5 | 同源中文版 + 最权威坑清单（spawn/fork 无父上下文、UNSUPPORTED_CAPABILITY、outputSchema 不保证、深度不可降等） |
| 3 | @deepseek-ai/dsh-subagent 核心包 README | https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/subagent/README.md | 5 | 一手代码包：注册/委托/续写语义、prepareContinuable 即能力、sandbox 策略、已知限制 |
| 4 | Three-role capability design（官方开发者实践教程） | https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/practice/index.md | 5 | 官方「怎么写 provider」教程：Service Definition → Service Provider → Consumer 三段式 + defineTool + ctx.tools.register |
| 5 | dsh-subagent-acp provider README | https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/subagent-acp/README.md | 5 | 可运行的官方跨进程 provider 样板：start/dispose、stop-reason 映射、providerName 注册、完整 config 表 |
| 6 | dsh-tool-subagent README | https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/tool-subagent/README.md | 4 | 模型面委托工具：provider 绑定、toolName、backgroundMode、maxDepth 默认 3 |
| 7 | dsh-subagent-dsh-sdk provider README | https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/subagent-dsh-sdk/README.md | 4 | 第二个 out-of-process provider 样板：能力声明、inheritsParentContext:false、maxDepth: provider-managed |
| 8 | dsh 扩展 Cookbook | https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cookbook/extension-cookbook.md | 4 | feature→mechanism 表：Sub-agent delegation 条目（provider registry + dsh-tool-subagent），放进「一切皆插件」全景 |
| 9 | subagent-spawn-in-process README | https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/subagent-spawn-in-process/README.md | 4 | in-process provider：fresh child、四项能力全支持、providerName 默认 spawn |
| 10 | tool-subagent-control / -report README | https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/tool-subagent-control/README.md | 4 | 控制工具（send_message/interrupt_agent/list_agents）+ 子代理汇报方向（-report） |

### 社区（Tier: community，仅作经验标注）

| # | 标题 | URL | 评分 | 相关性 |
|---|---|---|---|---|
| 11 | dsh-plugin-product-subagents（npm 0.2.0） | https://www.npmjs.com/package/dsh-plugin-product-subagents | 4 | 第三方完整 provider 插件：Codex/Claude Code/ACP 包装，含 cordis.patch.yml insert 挂载示例 + 声明式 config.providers |
| 12 | dsh-background-agents（PerryLink） | https://github.com/PerryLink/dsh-background-agents | 4 | 针对「one-shot 后台结果走 task 工具」痛点：可消息/中断/恢复的续跑子代理，官方 seam 的社区补强 |
| 13 | Discussion #1477（社区实战指南共建） | https://github.com/deepseek-ai/deepseek-harness/discussions/1477 | 4 | 聚合 9 类问题与实测 workaround（prepare undefined、Windows 目录、intranet crypto、UTF-8 BOM 等） |
| 14 | Discussion #2053（模型路由无权威查询接口） | https://github.com/deepseek-ai/deepseek-harness/discussions/2053 | 3 | 边界提醒：无法权威查询子代理最终解析的模型档位 |
| 15 | @aaravarr/dsh-subagent-max（npm 0.1.1） | https://www.npmjs.com/package/@aaravarr/dsh-subagent-max | 3 | 插件侧 wrapper + 多面板可视化，偏「围绕 subagent 的工具」 |

---

## 覆盖缺口

- **官方没有独立「SubagentProvider 教程」文档**：最接近的是 `docs/user/develop/practice/index.md`（三段式 capability 设计）+ `subagent-acp` / `subagent-dsh-sdk` 两个官方 provider 源码样板 → P2 以这三者为主干。
- `deepseek-harness.github.io/cookbook/extension-cookbook` 已 404，canonical 在 GitHub `docs/cookbook/extension-cookbook.md`。
- 中文资料稀缺：官方仅 `subagent.zh.md`；社区中文主要在 Discussion #1477。中文笔记以官方 zh 文档 + 自译为准。
- 「dsh 无内置 subagent 数量限制」仅见论坛二手说法（已 403），未经官方/Discussion 核实 → 笔记中不写或标注「未经证实」。
- 所有文档无显式发布日期，唯一时间锚点是「developer preview 2026-08-13 发布」。

## 预估 P2 范围

- **必取（3-5 核心）**：#2（或 #1 二选一，优先中文）、#3、#4、#5、#6
- **补充（按方向选）**：#9、#10（写 provider / 工具化必读）；#8（心智模型）
- **社区补充（可选）**：#11（cordis.patch.yml 部署样板）、#12（坑 workaround）、#13（实测问题聚合）
- 产出 `02_deep_research.md`：scope + 来源表 + claim/source 映射 + 矛盾 + 实操指南 + 开放问题 + 下游交接
