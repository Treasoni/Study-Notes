# 过时映射（Stale Map）— cc18 Claude Code Dynamic Workflows 使用指南

> 更新目标：同步到 2026-08 现状（覆盖 v2.1.198–v2.1.225）。来源库适用条目：SB-06、SB-12（SB-13/SB-14 审阅后判定不适用）。
> 补充核实：官方 workflows 文档（2026-08 现行版）——size guideline、Large workflow 预警、16 并发 / 1000 per-run 上限。

## 保留（Keep）

| 位置 | 理由 |
|------|------|
| frontmatter `title` / `topic` / `type` / `difficulty` / `tags` / `created` / `status` / `source_project` | 未过时；仅 `updated` 需推进 |
| §一句话定义（JS 脚本 + 类比） | 概念性内容仍准确；补 `[!tip] 大白话` |
| §它诞生的背景（v2.1.154 发布、Mermaid） | 历史背景未过时 |
| §与其它概念的对比表 + `[!tip] 关键洞察` | 调度者差异仍准确 |
| §核心触发方式（4 种，`ultracode:` 关键词等） | 主流程仍准确；仅 `/deep-research` 补 v2.1.218 不再自行启动 |
| §运行时特征（隔离运行时、Mermaid、`/workflows` 视图） | 仍准确；补 OTel 属性一条 |
| §关键限制表主体（16 并发 / 1000 per-run / 无用户输入 / 无 IO） | **经官方文档核实仍为现行数值**；补「不能加载模块」一行 + Large workflow 预警 |
| §保存位置（`.claude/workflows/`、v2.1.178 沿路径查找、项目优先） | 仍准确；补 v2.1.216 符号链接保护一条 |
| §关键要点 1/2（成本风险案例、成本控制） | 社区案例与官方建议未过时 |
| §关键要点 3（与相关概念边界表 + Mermaid + 关键边界） | 未过时 |
| §关键要点 5（关闭 workflow 三种方法） | 未过时 |
| §关键要点 7（args 全局变量 + 示例） | 官方文档仍为结构化对象，未过时 |
| 速查清单：触发方式 / 监控控制 / 保存位置 / 关闭 workflow 各表 | 大部分仍准确；监控控制补 `f` 键、触发方式补 `/deep-research` 行为 |
| 思考题 / 参考资料 / 文档元信息 | 未过时（参考资料追加 R10） |
| 原结构与写作风格、Callout 用法、列表/表格排版 | 保留 |

## 更新（Update）

| 位置 | 现状 | 改为 |
|------|------|------|
| frontmatter `updated` | 2026-07-12 | 2026-08-10 |
| §核心触发方式 触发方式 1（`/deep-research`） | 未提 v2.1.218 行为 | 补「v2.1.218 起只在主动调用时运行，Claude 不再自行启动」 |
| §运行时特征 | 无可观测性描述 | 补 OTel 属性：`workflow.run_id` / `workflow.name` |
| §关键限制表「最多 16 个并发 agent」 | 写「16」 | 保留数值，补「CPU 核少的机器更少」（官方原文）；并发/上限经核实未过时 |
| §关键限制表 | 无模块加载限制 | 新增「脚本含 `import()` 在 run 开始前失败」 |
| §关键限制区 | 无大型 run 预警 | 新增 `[!note]`：v2.1.203+ `Large workflow` 预警（>25 agent 或 >1.5M token） |
| §保存位置 | 无符号链接保护 | 补 v2.1.216 起保存前检查 symlink，拒写入 |
| §关键要点 4「v2.1.172 之前不能派生嵌套」 | 写「v2.1.172 之前」 | 改为 v2.1.217 默认禁用 → v2.1.219 恢复默认 3 层；附 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 禁用 |
| §关键要点 4 | 未提默认后台 | 补「workflow 派生 subagent 默认后台运行（v2.1.198+）」 |
| §关键要点 6「5 层嵌套 subagent 都支持」 | 写「5 层」 | 改为「3 层（v2.1.219 起默认深度）」 |
| §关键要点 6 worker 通信 | 未提跨会话消息 | 补 `SendMessage` 跨会话/跨机器 + `ListAgents` 按名称发现 |
| 速查清单·监控控制表 | 缺 `f` 键 | 补「按状态过滤 agent 列表 `f`」 |
| 速查清单·关键限制表「嵌套 subagent 5 层」 | 写「5 层（v2.1.172+）」 | 改为「3 层（v2.1.219 恢复；v2.1.217 曾默认禁用）」；补模块加载 / Large workflow 预警两行 |
| 速查清单·触发方式一览 `/deep-research` 行 | 只写「需要 WebSearch」 | 补「v2.1.218 起仅主动调用」 |
| 版本时间线表 | 止于 2.1.178 | 追加 v2.1.198 / v2.1.202 / v2.1.203 / v2.1.217 / v2.1.219 / v2.1.224 行 |
| 参考资料表 | R1–R9 | 追加 R10（changelog v2.1.198–v2.1.225） |

## 删除（Delete）

无。未发现正文中仍在使用、但已被官方废弃的字段或命令（`ultracode` 关键词 / `/effort ultracode` / 保存位置均现行）。

## 新增（Add）

| 小节/位置 | 新增内容 | 来源 |
|------|---------|------|
| §核心概念 → 新增「工作流规模（Dynamic workflow size）」子节 | `workflowSizeGuideline`（`unrestricted`/`small`<5/`medium`<15/`large`<50，默认 `medium`，v2.1.219+）；`/config`「Dynamic workflow size」+ `/config workflowSizeGuideline=small`；settings 键优先于 `/config`；规模是建议非硬上限；附 `[!tip] 大白话` | SB-12, R1, R10 |
| §一句话定义 → 新增 `[!tip] 大白话` | 「自动化流水线脚本」比喻，补核心概念大白话 | 完整性补全 |
| §运行时特征 → 新增 OTel bullet | `workflow.run_id` / `workflow.name` 属性 | R10（任务项 2） |
| §关键要点 6 → 新增跨会话通信 bullet | `SendMessage` 跨会话/跨机器，`ListAgents` 按名称发现 | R10（任务项 3） |
| 速查清单 → 新增「规模设置速查」子节 | 四档规模表 + 设置方式 + 优先级说明 | R1, R10 |
| 文末 → 新增「更新记录」 | 2026-08-10 条目，记录本次 6 类变更 | 更新留痕 |
