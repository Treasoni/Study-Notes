---
title: DeepSeek-Reasonix 模型与运行模式
topic: DeepSeek-Reasonix 配置教程
type: guide
difficulty: 进阶
tags:
  - DeepSeek-Reasonix
  - profile
  - effort
  - 双模型协同
  - planner_model
  - subagent
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
sources:
  - R1: "DeepSeek-Reasonix 官方仓库（README.zh-CN / GUIDE.zh-CN / reasonix.example.toml / CLI 参考）(esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix"
  - R2: "配置示例 reasonix.example.toml：[[providers]] effort、[agent] planner_model / subagent_model 字段来源 (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/reasonix.example.toml"
  - R3: "配置指南 GUIDE.zh-CN：profile 三档（economy/balanced/delivery）与双模型协同语义 (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/GUIDE.zh-CN.md"
  - R4: "CLI 参考 CLI-REFERENCE / CLI.zh-CN：--profile、--effort、--model 等启动参数 (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/blob/v1/docs/CLI-REFERENCE.md"
  - R5: "Claude Code 对齐 PR #6431：/model、/provider、/resume 与 picker 交互对齐 (esengine, 2026) https://github.com/esengine/DeepSeek-Reasonix/pull/6431"
concepts:
  - profile
  - effort
  - model-switching
  - planner-model
  - dual-model-collaboration
  - subagent-model
  - preset
related_notes:
  - "[[reasonix.toml 配置详解]]"
  - "[[DeepSeek-Reasonix CLI 完整参考]]"
  - "[[DeepSeek-Reasonix 会话与交互]]"
  - "[[DeepSeek-Reasonix 前缀缓存与成本优化]]"
  - "[[从 Claude Code 迁移到 DeepSeek-Reasonix]]"
---

# DeepSeek-Reasonix 模型与运行模式

> [!info] 文档定位
> 这是进阶应用篇第 7 章。本章回答「模型和运行模式怎么管」：官方的工作档位到底是哪几档、怎么切换、推理深度（effort）怎么调、执行器与规划器双模型怎么协同、subagent 怎么选模型。读完你可以不看文档地在启动参数、会话内命令和 `reasonix.toml` 三处自由控制模型与运行模式。配置字段的书写位置见 [[reasonix.toml 配置详解]]，命令全集见 [[DeepSeek-Reasonix CLI 完整参考]]，成本影响见 [[DeepSeek-Reasonix 前缀缓存与成本优化]]。

先给一个总览：Reasonix 对「模型与运行」的控制分散在三层——**运行模式（profile）**、**推理深度（effort）**、**模型选择（model/provider）**，再叠加一个可选的双模型协同（planner）。这三件事经常被混为一谈，本章先把它们掰开，再逐个展开。

## 一、运行模式体系澄清：profile ≠ effort ≠ preset

社区里最常出现的三个词是 `smart/fast/max`。先说结论，再展开。

> [!warning] 常见误解：官方没有 smart/fast/max 三档
> 网上流传的 `smart/fast/max` 三档**不是官方的运行模式**。官方的工作模式（profile）只有 **`economy | balanced | delivery`** 三档；而 `smart/fast/max` 是社区对 `/effort`（推理深度）的通俗说法。换句话说，`smart/fast/max` 既不等于 profile，也不是官方 effort 档位名——官方 effort 档位是 `high|max`（DeepSeek）。引用任何教程时，先分辨它说的是 profile、effort 还是 v1 的 preset，再对号入座。

三者对照如下：

| 概念 | 是什么 | 官方取值 | 控制入口 |
|------|--------|----------|----------|
| **profile**（工作模式） | 工具面与交付合约的档位 | `economy` / `balanced` / `delivery` | `--profile`、TUI `/work-mode`（`/profile` 为兼容别名） |
| **effort**（推理深度） | 单次请求思考多深 | DeepSeek：`high` / `max`；Anthropic 兼容端点：`low` / `medium` / `high` / `xhigh` / `max` | `--effort`、TUI `/effort`、provider 配置 `effort` 字段 |
| **preset**（v1 术语） | v1 会话内的预设档 | `auto` / `flash` / `pro` | v1 `/preset` |

> [!tip] 大白话
> 把 profile 想成「工作台的装备配置」：economy 是只摆最常用的 9 件工具、其他工具要用再拿；balanced 是全套工具都摆好；delivery 是全套工具加一个「稳定交付助手」并强制按交付标准交活。
> 所以 profile 管「带多少工具、以什么标准交付」，**不是**管「模型思考多深」——思考深度是另一回事（effort），别混在一起。

## 二、Profile 三档详解

官方 profile 三档的差异集中在「初始工具面」和「交付合约」上：

| 档位 | 工具面 | 核心特征 | 适合场景 |
|------|--------|----------|----------|
| `economy` | 初始只带 9 个工具 | 其余工具按需连接，启动更轻 | 轻量问答、快速任务、想省 token 的场景 |
| `balanced` | 完整工具面 | 默认档，无额外合约 | 日常编码，多数时候用它 |
| `delivery` | 完整工具面 | 增加稳定能力代理 `use_capability`，**强制交付合约** | 需要稳定交付的长任务、生产级输出 |

三个档位共享同一个本地引擎，切换只是改变会话的运行时行为，不是换模型。

### 启动时用 `--profile`

```bash
# 以 delivery 档启动，进 TUI
reasonix code --profile delivery .

# 无头执行也用 profile
reasonix run --profile economy "总结一下 TODO"
```

### 会话内热切换 `/work-mode`

启动后可以在 TUI 里热切换，不用重启：

```text
/work-mode balanced      # 切回默认档
/work-mode delivery      # 切到交付档
```

`/work-mode` 是 main-v2 的命令名，`/profile` 是它的兼容别名。注意：不同版本对这两个名字的收录不同（见[[DeepSeek-Reasonix 会话与交互]]第 4 章版本差异），以应用内 `/help` 为准。

## 三、effort 推理深度

`effort` 控制**单次请求思考多深**，与 profile 相互独立。官方档位按端点类型分两套：

| 端点类型 | 档位 | 备注 |
|----------|------|------|
| DeepSeek（`kind = "openai"`） | `high` / `max` | **思考恒开**，两档控制思考强度上限 |
| Anthropic 兼容端点（`kind = "anthropic"`） | `low` / `medium` / `high` / `xhigh` / `max` | 五档，走 Messages API |

三个入口，从高到低覆盖：

1. **provider 配置默认**：在 `reasonix.toml` 的 `[[providers]]` 里写 `effort = "high"` 作为该 provider 的默认推理深度；可选字段 `supported_efforts` / `default_effort` 可进一步声明支持的档位集合与默认值。
2. **启动参数覆盖**：`--effort LEVEL` 在启动时覆盖 provider 默认。
3. **会话内实时调**：`/effort` 在会话中随时切换。

```bash
# 启动时把推理深度拉到 max
reasonix code --effort max .
```

```toml
[[providers]]
name = "deepseek"
kind = "openai"
models = ["deepseek-v4-flash", "deepseek-v4-pro"]
effort = "high"          # 默认推理深度；可选 supported_efforts/default_effort 细化
```

覆盖关系一句话：**flag（`--effort`）> 会话内（`/effort`）> provider 配置 `effort` 字段**——这也是全系列配置优先级（flag > 项目配置 > 全局 > 内置默认）在模型维度的体现。

> [!tip] 大白话
> 把 effort 想成「答题时打草稿的详细程度」：high 是把关键步骤写在草稿纸上再誊写答案，max 是每一步都验证一遍。DeepSeek 的思考恒开，意味着它每次都打草稿，`high`/`max` 只是控制草稿能打多细。
> 所以调 effort 是在「更省 token 的浅思考」和「更稳但更贵的深思考」之间做权衡，和选哪档 profile 是两码事。

## 四、模型切换

模型选择的入口也分三处，均引用 provider 名或 `provider/model`：

| 入口 | 作用 | 示例 |
|------|------|------|
| `/model` | 会话内切换模型（main-v2） | 参数写法同 `--model` |
| `/provider` | 会话内切换 provider（main-v2） | `/provider <provider 名>` |
| `--model NAME` | 启动时指定 | `--model deepseek`（provider 名）或 `--model deepseek/deepseek-v4-pro`（精确到模型） |
| `default_model`（顶层） | 配置默认模型 | `default_model = "deepseek"` |

`--model` 与顶层 `default_model` 都支持两种写法：

```bash
reasonix code --model deepseek                  # 写法一：按 provider 名选，用其 default 模型
reasonix code --model deepseek/deepseek-v4-pro  # 写法二：provider/model 精确指定
```

```toml
default_model = "deepseek"           # 顶层默认：provider 名，或 "provider/model"
```

优先级同样是 flag 覆盖配置：`--model` 启动参数 > `default_model` 顶层字段。会话内 `/model`、`/provider` 的切换只对当前会话生效，下次启动仍按配置与参数走。

## 五、双模型协同：执行器 + 规划器

默认情况下 Reasonix 只有一个「执行器」负责干活。启用双模型后，会多出一个「规划器」，形成「规划 + 执行」两条腿。启用方式只需在 `[agent]` 里写一行：

```toml
[agent]
planner_model = "deepseek-pro"   # 双模型协同：指定规划器模型
```

启用后的分工很明确：

| 角色 | 模型来源 | 能看什么 | 能写什么 |
|------|----------|----------|----------|
| **规划器**（planner） | `planner_model` 指定 | `REASONIX.md` / `AGENTS.md` 记忆 + **只读研究工具** | **无写入工具** |
| **执行器**（executor） | 默认/当前模型 | 完整上下文 | 全部写入工具 |

关键语义：

- 规划器**只读**记忆与只读研究工具，负责把任务拆成方案；**写入工具只给执行器**，真正改文件、跑命令的是执行器。这样规划阶段不会污染工作区，方案先行、执行跟上。
- 记忆文件（`REASONIX.md`/`AGENTS.md`，`/init` 生成）是规划器的「工作简报」——它靠这份记忆理解项目背景再出方案（记忆机制见[[DeepSeek-Reasonix 会话与交互]]）。
- 路由是**确定性的**：规划器固定由 `planner_model` 承担，不额外调用分类器（classifier）来判断谁来干活，因此不会引入额外一次模型调用的成本。

> [!tip] 大白话
> 把双模型协同想成「项目经理 + 施工队」：项目经理（planner）只看图纸和需求文档（记忆 + 只读研究），负责出施工方案，但他没有电钻、不能动手；施工队（executor）拿着全部工具按方案施工。
> 好处是方案阶段不会把工地搞乱（规划器没有写权限），且不额外花钱请「监工分类器」来决定谁干活——分工写死，路由确定。

## 六、preset 与 subagent 模型

### preset：v1 的预设档

`/preset auto|flash|pro` 是 **v1 特有**命令，属于 v1 的预设档概念。main-v2 的 CLI 文档未收录 `/preset`，对应能力由 `/work-mode` 承担。引用社区教程看到 `/preset` 时，先确认你所在版本的 `/help` 是否支持。

### subagent 模型：子代理怎么选模型

Reasonix 支持子代理（subagent）机制，子代理的模型可以在 `[agent]` 里单独指定：

```toml
[agent]
subagent_model = "deepseek-pro"    # 所有子代理的默认模型
subagent_models = {                # 按角色单独指定，覆盖上面的默认
  review = "deepseek-pro",
  security_review = "deepseek-pro",
}
max_subagent_concurrency = 6       # 子代理并发上限
```

- `subagent_model` 设置全部子代理的默认模型；
- `subagent_models` 用表对 `review`、`security_review` 等特定角色单独指定，更精细；
- `max_subagent_concurrency` 控制同时跑多少个子代理，限制并发即限制峰值成本。

### 辅助调用的分层定价

有一类调用不随 preset 走，也**不随你换 profile / effort 而变**：摘要生成、subagent 生成、截断修复这些「辅助调用」，Reasonix 一律硬编码为 `v4-flash + effort=high`。这是刻意的成本设计——辅助环节用轻量模型 + 固定思考深度，把大头预算留给真正干活的主调用。成本测算与命中率的影响在[[DeepSeek-Reasonix 前缀缓存与成本优化]]展开。

> [!tip] 大白话
> 把辅助调用的分层定价想成「打包发货时，面单打印、胶带、包装盒这类耗材永远用最便宜的标准件」——不管你这单货值多少，耗材固定按低价档走。
> 所以你在会话里怎么调 profile、怎么调 effort，都不会影响辅助调用的定价，它们恒定是 `v4-flash + effort=high`。

## 七、常见坑

1. **把 `smart/fast/max` 当官方档位**。官方 profile 只有 `economy|balanced|delivery`；`smart/fast/max` 是社区对 `/effort` 的俗称，而官方 effort 档位是 `high|max`（DeepSeek）。对着 `--profile smart` 敲会直接报参数错误。

> [!warning] 坑点：profile 与 effort 混淆
> `--profile` 管工具面与交付合约，`--effort` 管推理深度，两者独立、入口不同。改 profile 不会改变思考深度，改 effort 不会改变工具面。想「快」先想清楚是要少带工具（economy）还是浅思考（`effort high`）。

2. **`/preset` 在 main-v2 敲不出来**。`/preset auto|flash|pro` 是 v1 命令，main-v2 未收录，对应能力用 `/work-mode`。命令报不存在时先敲 `/help` 看实时权威，别急着怀疑装坏了。

3. **`--model` 两种写法别混**。`--model deepseek` 是选 provider（用其 default 模型）；`--model deepseek/deepseek-v4-pro` 是精确到模型。只写模型名（不带 provider 前缀）时，语义按你当前配置解析，不确定就写成 `provider/model` 最保险。

4. **开了 `planner_model` 却指望规划器写文件**。规划器**没有写入工具**，只有执行器能写。想调整「谁能写」，改的是权限与工具分配，不是给 planner 换更强的模型。

5. **调辅助调用定价白费力气**。摘要、subagent 生成、截断修复硬编码 `v4-flash + effort=high`，改 preset、profile、effort 都不影响它们。想省这部分钱，方向是优化缓存命中率，不是换模型。

## 常见问题

**Q：官方到底有没有 `smart/fast/max`？**
A：没有。官方工作模式是 `economy|balanced|delivery`；`smart/fast/max` 是社区对 `/effort` 的通俗说法，而官方 effort 档位是 `high|max`（DeepSeek）或 `low|medium|high|xhigh|max`（Anthropic 兼容端点）。

**Q：`--profile` 和 `--effort` 能同时用吗？**
A：可以，它们管两件独立的事：profile 管工具面与交付合约，effort 管推理深度。两者可以任意组合。

**Q：切换 `/model` 后重启会保留吗？**
A：不会。会话内 `/model`、`/provider` 只对当前会话生效；下次启动按 `--model` 启动参数与 `default_model` 顶层字段决定。

**Q：双模型协同怎么启用？**
A：在 `[agent]` 里加一行 `planner_model = "deepseek-pro"` 即可。规划器只读记忆与只读研究工具，写入工具只给执行器，路由确定、不额外调分类器。

**Q：subagent 的模型怎么单独控制？**
A：`subagent_model` 设所有子代理的默认模型；`subagent_models = { review = "..." }` 按角色覆盖；`max_subagent_concurrency` 控制并发上限。

## 相关文档

- [[reasonix.toml 配置详解]] — `[[providers]] effort` 字段、`[agent] planner_model/subagent_model` 的书写位置
- [[DeepSeek-Reasonix 会话与交互]] — `/work-mode`、`/model`、`/provider`、`/effort` 与 v1/main-v2 版本差异
- [[DeepSeek-Reasonix CLI 完整参考]] — `--profile`、`--effort`、`--model` 等启动参数全集
- [[DeepSeek-Reasonix 前缀缓存与成本优化]] — 辅助调用分层定价、effort 与缓存命中率的关系

## 参考资料

- [esengine/DeepSeek-Reasonix 官方仓库（README.zh-CN / GUIDE.zh-CN / reasonix.example.toml / CLI-REFERENCE / CLI.zh-CN）](https://github.com/esengine/DeepSeek-Reasonix)
- `main-v2/reasonix.example.toml`：`[[providers]] effort`、`[agent] planner_model / subagent_model / subagent_models / max_subagent_concurrency` 字段来源
- `main-v2/docs/GUIDE.zh-CN.md`：profile 三档（economy/balanced/delivery）与双模型协同语义
- [Claude Code 对齐 PR #6431](https://github.com/esengine/DeepSeek-Reasonix/pull/6431)

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-10 | 初稿：profile 三档澄清、effort 推理深度、模型切换、双模型协同、preset/subagent 与常见坑 |
