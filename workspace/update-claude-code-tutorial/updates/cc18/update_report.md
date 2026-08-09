# 更新报告 — cc18 Claude Code Dynamic Workflows 使用指南

## 基本信息

| 项 | 值 |
|----|----|
| note_id | cc18 |
| 原文件 | `C:\note\Study-Notes\AI学习\Claude Code 教程\04-高级功能\Claude Code Dynamic Workflows 使用指南.md` |
| 输出目录 | `C:\note\Study-Notes\workspace\update-claude-code-tutorial\updates\cc18\` |
| 原状态 | updated（updated 2026-07-12） |
| 新状态 | updated（updated 2026-08-10） |
| MOC | none（P5 统一处理） |

## 更新摘要

- **frontmatter**：`updated: 2026-07-12 → 2026-08-10`；`status: updated` 保持；追加 R10 来源（changelog v2.1.198–v2.1.225）。
- **规模建议（新增小节）**：核心概念新增「工作流规模（Dynamic workflow size）」——`workflowSizeGuideline`（`unrestricted` / `small`<5 / `medium`<15 / `large`<50，默认 `medium`，v2.1.219+）；`/config`「Dynamic workflow size」+ `/config workflowSizeGuideline=small`；settings 键优先于 `/config` 且隐藏对应行；规模是建议非硬上限（SB-12 + 官方文档核实）。
- **可观测性（新增）**：运行时特征补 OTel bullet——workflow 派生 agent 带 `workflow.run_id` / `workflow.name` 属性（任务项 2）。
- **后台与跨会话通信（新增）**：关键要点 4 补「子代理默认后台运行（v2.1.198+）」；关键要点 6 补「`SendMessage` 可跨会话/跨机器，`ListAgents` 按名称发现」（任务项 3 + SB-06）。
- **限制更新**：关键限制表新增「脚本不能加载模块（含 `import()` 直接失败）」；新增 `[!note]` `Large workflow` 预警（v2.1.203+：>25 agent 或 >1.5M token，仅提示）。
- **嵌套规则**：5 层 → v2.1.219 恢复的默认 **3 层**（v2.1.217 曾默认禁用），`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 可禁用——覆盖关键要点 4、关键要点 6、速查关键限制（SB-06）。
- **`/deep-research`**：v2.1.218 起仅在主动调用时运行，Claude 不再自行启动（核心触发方式 + 速查触发表）。
- **并发/上限经核实保留**：16 并发 / 每 run 1000 经官方现行文档核实**仍准确**，未改为 SB-06 的「20」（20 是普通 subagent 并发，不适用于 workflow）。
- **速查补全**：监控控制补 `f`（按状态过滤）；新增「规模设置速查」子节；版本时间线追加 v2.1.198/202/203/217/219/224 六行；参考资料补 R10。
- **大白话**：一句话定义新增 `[!tip] 大白话`（自动化流水线脚本）；规模子节补 `[!tip] 大白话`。
- **更新记录**：文末追加 2026-08-10 条目。
- 未重写未过时段落（诞生背景、对比表、关闭方法、成本章节、思考题、实操示例等均保留原文）。

## 引用来源

| 来源 | 用途 |
|------|------|
| SB-06（Subagents 默认后台 + 并发/嵌套规则） | 默认后台 v2.1.198+、v2.1.217 禁用嵌套→v2.1.219 恢复深度 3、v2.1.224 移除每会话 200 spawn 上限 |
| SB-12（settings.json 新增配置键） | `workflowSizeGuideline` 规模建议 |
| 官方 workflows 文档（2026-08-10 现场核实） | size guideline 四档数值与默认 `medium`、`Large workflow` 预警、模块加载限制、16 并发 / 1000 per-run、`/deep-research` v2.1.218、symlink 保护、`f` 键 |
| R10（changelog v2.1.198–v2.1.225） | 版本时间线补充来源标注 |

> 以 code.claude.com 现行文档为准（来源库约定：若与本文冲突，以官方文档为准；本次已直接核实官方 workflows 页面）。

## 未处理风险

1. **OTel 属性与 SendMessage 跨机器为任务 spec 转述**：官方 workflows 文档页面未直接提及 `workflow.run_id`/`workflow.name` 与 `SendMessage` 跨会话/跨机器；这两条按 batch 计划 update_goal（任务项 2/3）写入，写回前建议对照 changelog 原文或 Agent SDK 参考核实。
2. **版本日期为近似值**：v2.1.198/202/203/217/219/224 的具体日期来自来源库区间推断（2026-07/08），时间线中以月份呈现，未逐一抓取 changelog 原始条目。
3. **「6 种模式 / JS 脚本生成」章节不存在**：update_goal 提到「核对 6 种模式、JS 脚本生成章节（pipeline/parallel）」，但当前笔记**没有**该章节——它只有「核心触发方式」「实操示例（`args` + 循环委派）」。官方文档现行通过 `agent()` / `pipeline()` 帮助函数 + 示例 prompt（fan-out / 反复修复 / 并行迁移 / 汇总 review 等）描述编排形态，并无正式「6 种模式」taxonomy。若需新增「编排模式」章节，属新增内容，超出局部 patch 范围。
4. **SB-13 / SB-14 判定不适用**：本笔记无 sandbox 凭据掩码 / Auto mode AskUserQuestion 相关段落，审阅后未改动。
5. **workflow 内嵌套精确语义**：SB-06 的「默认 3 层」是普通 subagent 规则；workflow 内 subagent 的嵌套当前按同一规则更新，写回前可再对照官方 Subagents 文档确认。
6. **未大范围联网**：仅核实官方 workflows 文档一页 + 共享来源库；未逐一抓取 changelog / settings 原始条目。

## 结论

- 发现过时点：**10 处**（5 组过时修正：frontmatter 日期、`/deep-research` 自动启动行为、嵌套规则 5→3 层×3 处文本、缺模块加载限制、缺 Large workflow 预警；5 处新增缺失项：OTel 属性、默认后台、SendMessage 跨会话、symlink 保护、`f` 键）+ **2 个新增小节**（工作流规模、规模设置速查）+ 时间线/来源/更新记录补全。
- **是否需要 needs-review：是**。OTel 属性与 SendMessage 跨机器为任务 spec 转述、版本日期为近似值，且「6 种模式」章节属预期外缺失；建议用户审阅 `updated_note.md` 并对照官方 changelog / Agent SDK 文档后，再写回原 vault 文件。
