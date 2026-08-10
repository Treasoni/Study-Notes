---
title: DeepSeek-Reasonix 前缀缓存与成本优化
topic: DeepSeek-Reasonix 配置教程
type: guide
difficulty: 进阶
tags: [DeepSeek-Reasonix, 前缀缓存, 成本优化, 缓存命中率, budget]
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
sources:
  - R1: "架构文档 ARCHITECTURE.md：前缀缓存原理、三区上下文设计（CacheFirstLoop）、命中率公式 (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/v1/docs/ARCHITECTURE.md"
  - R2: "配置示例 reasonix.example.toml：[agent] 压缩比例与 [providers] prices 字段 (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/reasonix.example.toml"
  - R3: "CLI 参考 CLI-REFERENCE.md：--budget、/cost、reasonix stats（v1 口径）(esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/v1/docs/CLI-REFERENCE.md"
  - R4: "Issue #7907：用户实测命中率与成本对账 (esengine/DeepSeek-Reasonix, 2026) https://github.com/esengine/DeepSeek-Reasonix/issues/7907"
  - R5: "智源 BAAI 报道：项目自报命中率与成本数据（非独立评测）(BAAI Hub, 2026) https://hub.baai.ac.cn/view/54971"
concepts:
  - prefix-cache
  - cachefirstloop
  - cache-hit-rate
  - immutable-prefix
  - tool-call-repair
  - budget
  - compaction
related_notes:
  - "[[DeepSeek-Reasonix 是什么]]"
  - "[[reasonix.toml 配置详解]]"
  - "[[DeepSeek-Reasonix 模型与运行模式]]"
  - "[[DeepSeek-Reasonix 自动化与 CI]]"
  - "[[从 Claude Code 迁移到 DeepSeek-Reasonix]]"
---

# DeepSeek-Reasonix 前缀缓存与成本优化

> [!info] 文档定位
> 本文是「03-进阶应用」层的成本优化核心章，把前缀缓存从原理讲到省钱实践：缓存怎么命中、三区上下文设计如何保命中、实测数据怎么读，以及预算控制与调优建议。它承接[[DeepSeek-Reasonix 是什么]]第 3 节的缓存概览，并依赖[[reasonix.toml 配置详解]]里已经讲过的 `[agent]` 压缩字段（这里只讲机制与调法，不重复字段书写）。读完你应能：看懂 TUI 顶栏的缓存命中率、用 `--budget` 设成本上限、按四档压缩比例做缓存友好调优，并且能区分哪些命中率数据是官方口径、哪些是第三方实测。全篇事实以官方 ARCHITECTURE.md、reasonix.example.toml、CLI-REFERENCE 与 Issue #7907 为限，不做超出信源的推测。

本文要解决的核心问题是：**同样一个 DeepSeek API，为什么有人跑出 <20% 的缓存命中率、有人跑出 99%+，账单相差近一个数量级？**

## 一、前缀缓存原理：精确字节前缀 + 命中 ~10% 计费

DeepSeek 的 API 自带**自动前缀缓存**（据官方 ARCHITECTURE.md）：对一串连续的输入 token，若它与上一请求的**精确字节前缀**完全匹配，则命中缓存；前缀内任何一个早期字节发生变化，整段缓存立即失效。

关键计费规则只有一条：**命中缓存的输入 token 按未命中价格的约 10% 计费**。这意味着：

- 上下文越长、前缀越稳定，单轮成本越低；
- 前缀每轮都被改一点，缓存就白搭，成本回到全价。

那「无纪律」的 agent 为什么普遍命中率 **<20%**？官方文档点名了三类高频自毁操作：**重排上下文**（每轮换个顺序）、**重写旧日志**（回头改写前面的对话）、**每轮注入时间戳**（在前缀里混入变化值）。任何一类都会打断精确字节前缀。

> [!tip] 大白话
> 把缓存命中的 token 想成「戴着临时工牌的熟面孔」：系统一眼认出他，进场只收 1 折门票；每次新来的 token 是生面孔，要全价买票。
> 所以「保持前缀稳定」= 让队伍里熟面孔越来越多；反之，你每轮把队伍重新排一遍、把前面的工牌全换掉，熟面孔就全变回生面孔，每轮门票全价买单。

## 二、三区上下文设计（CacheFirstLoop）：把「会变的」和「不变的」分开

Reasonix 的核心工程叫 **CacheFirstLoop**，把上下文切成三个区，各管各的，保证「不变的永远不变」：

| 区域 | 内容 | 行为 |
|------|------|------|
| IMMUTABLE PREFIX 不可变前缀 | system + tool_specs + few_shots | 会话内固定，每会话算一次并「钉住」 |
| APPEND-ONLY LOG 只追加日志 | `[assistant₁][tool₁][assistant₂]...` | 单调追加，绝不重写 |
| VOLATILE SCRATCH 易变草稿 | R1 思维、临时计划 | 每轮重置，永不直接上送，先经 Tool-Call Repair 蒸馏 |

三条不变量把它变成硬约束：

1. **前缀只算一次并固定**：system、工具定义、few-shot 例子进会话即钉住，后续轮次不得改动；
2. **日志按追加顺序序列化、不重写**：每一轮的 assistant 与 tool 结果只往后追加，绝不回头改写；
3. **草稿先蒸馏再折叠进日志**：每轮产生的推理草稿先重置，经 Tool-Call Repair 提炼成干净的工具调用后才落进日志。

命中率由官方公式逐轮计算，并显示在 TUI 顶栏的缓存单元格：

```text
命中率 = prompt_cache_hit_tokens / (hit_tokens + miss_tokens)
```

配套的缓存友好工程实践让三区设计真正落地：

- **并行工具分发**：工具声明 `parallelSafe?: boolean`，用 `Promise.allSettled` 并发执行，但工具结果与历史追加**仍按声明顺序落盘**——顺序稳定是缓存命中的前提。可用环境变量 `REASONIX_PARALLEL_MAX`（默认 3，上限 16）调并发；`REASONIX_TOOL_DISPATCH=serial` 可强制串行。
- **Pillar 2 Tool-Call Repair 四轮修复**：flatten（压平深层 schema）、scavenge（从 reasoning_content 回收漏写的工具调用）、truncation（补不平衡 JSON）、storm（滑动窗口抑制重复 (tool,args) 元组）。它把易变草稿「蒸馏」成稳定的工具调用序列。
- **轮末自动压缩**：日志中超过 `TURN_END_RESULT_CAP_TOKENS`（3000）的工具结果在轮末压缩；读到的那一轮保留全文，后续轮次看到紧凑摘要、可按需重读。既保命中率又控制体积。

> [!tip] 大白话
> 把三区想成「工地的三类文件」：**蓝图**（不可变前缀）贴墙不动，每天只复印一次；**施工日志**（只追加）只往后写、绝不涂改；**便签纸**（易变草稿）用完即扔。
> 所以无论装修队多忙，监理（缓存）永远认得你这套流程——蓝图不换、日志不涂，账就省得下来。

## 三、命中率与成本实测数据（务必看口径）

关于「Reasonix 命中率到底多少」，网上数字从 <20% 到 99.8% 都有，因为它们根本不是同一回事。本节把三组数据按口径拆开，**引用时务必带上出处**：

> [!note] 数据口径说明
> 三组数据来源性质不同，不可混为一谈：①**官方口径**来自官方 ARCHITECTURE.md，描述的是「无纪律 agent 的下限」与「目标用户画像」；②**Issue #7907** 是真实用户在自己环境里做的对账（本地 stats × 计费控制台），可信度最高；③**智源社区报道**转述的是**项目自报数据、非独立评测**，应视为厂商宣传口径。

| 口径 | 关键数据 | 出处 |
|------|----------|------|
| 官方口径 | 无纪律 agent 命中率 **<20%**；前沿模型活跃用户成本约 **$150–250/月**；北极星 =「便宜到可以常开的编码 agent」 | 官方 ARCHITECTURE.md |
| Issue #7907 用户实测 | 8/8 命中率 **99.6%**；全天 158 请求成本 **¥1.37**、单请求 **¥0.00869**（约 1 分钱/轮）；优化后成本 **-55~60%**；最大 miss 约 **2K/请求**、无 >10K 缓存打穿 | [Issue #7907](https://github.com/esengine/DeepSeek-Reasonix/issues/7907) |
| 项目自报（智源报道） | 单日 **4.35 亿输入 token** 命中率 **99.82%**；**$61 → $12**（约 2 折，节省约 80%）；长会话保证命中率 **90%+** | [智源 BAAI 报道](https://hub.baai.ac.cn/view/54971)（非独立评测） |

把三组放在一起，正确的读法是：

1. **<20% 是无纪律 agent 的基线**，不是 Reasonix 的表现；它恰恰是 Reasonix 想解决的问题。
2. **真实用户对账（#7907）是最可靠的第三方数字**：99.6% 命中、单请求约 1 分钱，且优化还能再省一半以上。
3. **99.82% / $61→$12 这类数字来自项目自报**，参考时标注「非独立评测」。

成本侧还有一组官方对比口径值得记住：**DeepSeek 缓存价约 ¥0.02/1M token vs 未缓存 ¥1/1M（约 50 倍单价差）**，结合 Reasonix 项目自报的长会话命中率 94%–99.8%，长会话输入成本大约能压到 1/5。完整的迁移成本对比在[[从 Claude Code 迁移到 DeepSeek-Reasonix]]展开，这里不重复推导。

## 四、成本监控：先能看到钱花在哪，才能谈省

优化之前，先把「看得到」做起来。Reasonix 给了三个观察点：

1. **TUI 顶栏缓存单元格**：每轮实时显示命中率（`hit / (hit + miss)`），是最高频的体检指标。命中率持续偏低，说明前缀被破坏了，应回看第二节的三区约束。
2. **`[ui] show_turn_usage = true`**：在 `reasonix.toml` 里开启后，每次请求都会显示 token 用量与费用，适合逐轮盯着花销：

```toml
[ui]
theme = "auto"
show_turn_usage = true   # 显示每次请求 token 与费用
```

3. **会话内 `/cost`（v1）** 与 **`reasonix stats [transcript]`**：前者在会话内查看累计成本；后者在会话外对（指定）转录做**一次性的 cost/cache 分解**，适合复盘：

```bash
reasonix stats            # 输出 cost / cache 分解
reasonix stats sessions/xxx.jsonl   # 指定某个会话转录
```

> [!tip] 大白话
> 把 `/cost` 和 `stats` 想成「记账 App」：`show_turn_usage` 是每次消费的小票，顶栏缓存命中率是健康手环，`reasonix stats` 是月底对账。
> 所以优化的第一步不是改配置，而是先让这些「仪表盘」亮起来——没有数据，后面所有调优都是盲调。

## 五、预算控制：设上限，而不是靠自律

成本失控最常见于无人值守的长时间任务。Reasonix 提供两层硬约束：

**1. 会话级成本上限 `--budget <usd>`（v1）**：给单次会话设美元上限，**花到 80% 警告、100% 拒绝**继续调用，防止账单爆掉：

```bash
reasonix run "把 main.go 的 TODO 实现掉" --budget 5
```

**2. 自定义计价 `[providers] prices`**：如果用的是非 DeepSeek 端点、或实际计费与内置单价不一致，可在 provider 上声明自定义单价，让 `stats` / `/cost` 的估算贴合你的真实账单：

```toml
[[providers]]
name = "deepseek"
kind = "openai"
base_url = "https://api.deepseek.com"
models = ["deepseek-v4-flash", "deepseek-v4-pro"]
default = "deepseek-v4-flash"
api_key_env = "DEEPSEEK_API_KEY"
# prices 覆盖内置单价，成本测算以这里为准
# prices = { input = ..., output = ..., cache_read = ..., cache_creation = ... }
```

另外一条内置的降本机制是**辅助调用分层定价**：摘要、subagent 生成、截断修复这类辅助请求**一律硬编码 `v4-flash + effort=high`，不随 preset 走**——重活走贵模型、杂活走便宜模型，是成本模型里的隐性设计。

## 六、调优建议：四档压缩比例与缓存命中的关系

`[agent]` 里的四个压缩比例决定「上下文膨胀到什么时候、用什么力度处理」。它们是触发越来越重的四级阈值，直接和缓存命中率相关：

| 参数（默认值） | 触发动作 | 与缓存命中的关系 |
|----------------|----------|------------------|
| `soft_compact_ratio`（0.5） | 缓存优先压缩提示 | 最轻，先动不影响前缀的部分 |
| `tool_result_snip_ratio`（0.6） | 裁剪工具结果 | 把超长工具输出折短，保留可读摘要 |
| `compact_ratio`（0.8） | 完整压缩 | 重排/摘要历史，可能伤及前缀 |
| `compact_force_ratio`（0.9） | 强制压缩 | 上下文爆表兜底，最伤缓存但保运行 |

```toml
[agent]
soft_compact_ratio = 0.5        # 缓存优先压缩提示
tool_result_snip_ratio = 0.6    # 裁剪工具结果
compact_ratio = 0.8             # 完整压缩阈值
compact_force_ratio = 0.9       # 强制压缩阈值
```

字段怎么写在[[reasonix.toml 配置详解]]已讲，这里只讲**怎么调**：

- **默认值就是缓存友好的起点**：0.5 → 0.6 → 0.8 → 0.9 的阶梯刻意让轻量手段先触发，尽量别走到最后两档。
- **保住前缀 = 保住钱**：不要每轮重写前缀；保持 system 提示与工具定义稳定（它们属于不可变前缀区）；让日志只追加、不重排。
- **何时关 compact**：如果任务轮次少、上下文远没到阈值，可以把 `compact_ratio` 调高甚至不触发，避免无谓重排；反之长任务频繁触发 `compact_force_ratio` 时，应优先怀疑是不是工具输出过大（考虑让 `tool_result_snip_ratio` 更激进）或前缀被污染。
- **`reasonix stats` 是验证手段**：调完跑一次 stats，看命中率与 cost 分解是否真的改善，而不是靠感觉。

> [!tip] 大白话
> 把四档压缩想成「冰箱分层收纳」：soft 是先把散装菜装进保鲜盒，snip 是把过长的包装剪短，compact 是换季大扫除，force 是冰箱满了必须扔。
> 所以触发越重的动作，丢的信息越多、越可能伤到缓存前缀——调优的思路永远是「用最轻的手段先解决，别轻易走到扔东西那一步」。

## 七、常见坑

1. **把 <20% 当成 Reasonix 的表现**：<20% 是无纪律 agent 的基线，正是三区设计要解决的问题。看到 99.8% 这类数字时，先确认是「项目自报」还是「独立实测」再引用（见第三节口径表）。

2. **每轮注入时间戳 / 重排上下文**：任何会改变精确字节前缀的操作（重排、重写旧日志、注入动态值）都会把命中率打回 <20%。这是官方点名的最常见自毁行为。

3. **把 `--ablate` 当调优开关**：`--ablate LIST` 是**基准测量工具**（禁用子系统测量影响），不是性能调优参数——禁子系统只会让 Reasonix 更差。

4. **v1 / main-v2 命令差异**：`/cost`、`/budget`、`/preset` 是 **v1 特有**；main-v2 的 CLI.zh-CN **未收录** `/budget`、`/cost` 等命令。写脚本或教程时以应用内 `/help`、`/keys` 为实时权威，别照抄旧文档。

> [!warning] 命中率数据要带口径引用
> 99.82%、$61→$12 是**项目自报**（智源报道转述，非独立评测）；99.6%、¥1.37/全天来自 **Issue #7907 用户对账**。对外引用或做成本决策时务必区分，否则会把「宣传口径」当「实测结论」。

## 常见问题

**Q：缓存命中率低于 20%，最可能的原因是什么？**
A：前缀被破坏了。检查是否每轮重排上下文、重写旧日志或注入时间戳（如把当前时间拼进提示词）。这三类操作都会打断 DeepSeek 的精确字节前缀匹配。

**Q：`--budget` 是全局的还是每次会话的？**
A：是**会话级成本上限**（`--budget <usd>`，v1），花到 80% 警告、100% 拒绝。无人值守的 `reasonix run` 场景建议必带。

**Q：四个压缩比例应该怎么调？**
A：默认 0.5 → 0.6 → 0.8 → 0.9 已是缓存友好的阶梯。优先用轻量的 `soft_compact_ratio` / `tool_result_snip_ratio` 解决问题，避免触发 `compact_ratio` / `compact_force_ratio` 这类会重排历史的压缩。

**Q：怎么验证我的调优有效？**
A：跑 `reasonix stats` 看 cost/cache 分解，或看 TUI 顶栏缓存单元格的逐轮命中率；调优前后做对比，而不是凭感觉。

## 相关文档

- [[DeepSeek-Reasonix 是什么]]：前缀缓存原理的概览与心智模型
- [[reasonix.toml 配置详解]]：`[agent]` 压缩字段、`[providers] prices` 的书写位置
- [[DeepSeek-Reasonix 模型与运行模式]]：profile / effort / 双模型协同与辅助调用分层定价
- [[从 Claude Code 迁移到 DeepSeek-Reasonix]]：成本横向对比与迁移决策
- [[DeepSeek-Reasonix 自动化与 CI]]：`--budget` 在 CI 中的成本与状态约束

## 参考资料

- [esengine/DeepSeek-Reasonix 官方仓库](https://github.com/esengine/DeepSeek-Reasonix)
- `v1/docs/ARCHITECTURE.md`：前缀缓存原理、三区上下文设计（CacheFirstLoop）、命中率公式
- `main-v2/reasonix.example.toml`：`[agent]` 压缩比例与 `[providers] prices` 字段
- `v1/docs/CLI-REFERENCE.md`：`--budget`、`/cost`、`reasonix stats`（v1 口径）
- [Issue #7907](https://github.com/esengine/DeepSeek-Reasonix/issues/7907)：用户实测命中率与成本对账
- [智源 BAAI 报道](https://hub.baai.ac.cn/view/54971)：项目自报命中率与成本数据（非独立评测）

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-10 | 创建初稿（进阶应用篇第 9 章，成本优化核心章） |
