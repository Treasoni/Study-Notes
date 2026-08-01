# 第八章 把 skills 应用到自己的项目

第 7 章讲完排错，但到这一步还只是"会用"——能不能把 [[Matt Pocock Skills]] 这套方法论变成你自己的，才是分水岭。这一章是正文的收尾，回答三个实操问题：怎么按自己项目的工作流挑选和裁剪 skill、怎么写第一个自定义 [[Agent Skill]] 并分发出去、以及在一个已经跑着 Claude Code 甚至 Codex 的既有仓库里如何稳妥接入。读完你可以在半小时内给任意项目配上一套"少而精"的 skills 组合。

## 8.1 为自己的项目挑选与裁剪 skill

装 skill 不是把仓库搬过来，而是给项目配流程。最大的坑是全盘照搬：`npx skills@latest add` 后 22 个全选。第 6 章 6.4 已经说过全装的代价——每个 model-invoked 的 description 每轮都进上下文、场景重叠导致误触发、22 个斜杠命令记不住。所以这里给一套三步骤选型思路。

**第一步：先画主工作流。** 别从"仓库里有哪些 skill"出发，从"我的项目反复发生哪几类任务"出发。列出 3~5 类最高频的工作，在下面的表里对号入座：

| 项目主工作流 | 起步 skill | 跑通后按需补 |
|------------|-----------|-------------|
| 新功能从想法到交付 | `/grill-with-docs`（连 `/grilling` + `/domain-modeling`） | `/to-spec`、`/to-tickets`、`/implement` |
| 排查 bug | `/diagnosing-bugs` | `/grill-me` 先问清上下文 |
| 写测试、保证正确性 | `/tdd` | `/code-review` 双路审查 |
| 跨会话长任务 | `/handoff` | `/prototype` 设计验证 |

这四行覆盖了大部分项目的主回路，正好是 6.4 说的"从 4 个核心起步"。注意 `/grill-with-docs` 内部会委托 `/grilling` 和 `/domain-modeling`，起步时连同它们一起装，实际是 6 个 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

**第二步：反选法裁剪。** 列出你**绝不会用**的 skill，直接不装。最实用的裁剪依据是硬依赖——第 1 章说过 `/to-spec`、`/to-tickets`、`/triage` 都依赖 issue tracker 和标签。如果项目不用 GitHub Issues / Linear（比如一个没有 issue 流程的个人项目），这三个 skill 装上去也找不到发布目标，跑完即废，干脆不装。

> [!tip] 裁剪比安装更重要
> 少装的每个 model-invoked skill，都是每轮对话省下的 token 和少一次误触发的机会。宁可用的时候敲 `/ask-matt` 让它推荐，也不要让一个用不到的 skill 常驻上下文。

**第三步：跑一个真实功能再扩展。** 用裁完的起步组合完成一个小功能，然后每遇到"这个场景我缺个 skill"补一个（沿用 6.4 的扩展策略）。这套"少而精、按需补齐"的节奏更接近作者本意——核心 skill 大多只有 12 行左右，作者赌的是"模型大多做对的事"，靠最小锚点而非全量指令 [仓库精读](https://cloud.tencent.com.cn/developer/article/2704288)。

## 8.2 编写自己的第一个 skill 并接入

选型是"用什么"，这一节是"写什么"。第 5 章 5.3 给了 SKILL.md 模板（frontmatter + `# 目标` + `## 步骤` + `## 参考` + `## 依赖`）和六项质量关卡，这里给一个能直接跑起来的完整实例，可以整段复制进自己的仓库。

**实例：一个 model-invoked 的 `draft-release-notes` skill**——用户说"帮我起草发布说明"时自动触发，把两次 tag 之间的 commit 整理成发布说明。

```markdown
---
name: draft-release-notes
description: |
  Use when the user asks to draft release notes or a changelog
  for the upcoming release. Summarizes the git diff since the
  last tag into user-facing change notes.
---

# 目标
把两次 tag 之间的 commit 整理成给用户看的发布说明。

## 步骤
1. 找上一个 tag：`git describe --tags --abbrev=0`
   — 完成标准：拿到一个 tag 名；没有 tag 则提示先打一个。
2. 生成提交清单：`git log <上一个tag>..HEAD --oneline`
   — 完成标准：得到 commit 列表。
3. 按前缀归类：feat / fix / docs / refactor / chore
   — 完成标准：每条 commit 分到一类。
4. 改写成用户视角：feat 写"新增了什么"，fix 写"修好了什么"
   — 完成标准：每类至少一句人话。
5. 输出 Markdown：标题带版本号与日期占位符
   — 完成标准：文档可直接发布。

## 参考
- 类型前缀约定见仓库 CONTRIBUTING.md；没有则按 Conventional Commits 默认归类。

## 依赖
- 可选：运行 `/code-review` 对发布说明做一次双路检查。
```

写完后按 5.3 的六项质量关卡自查，这个实例这样过关：

| 关卡 | 本实例怎么过关 |
|------|--------------|
| description 触发词 | 面向模型的 description 含 "Use when the user asks to draft release notes..." |
| 篇幅 | 约 20 行，远低于 100 行上限 |
| 无时间敏感 | 不写版本号 / 日期，用占位符 |
| 术语一致 | 通篇用 git tag / commit / release notes，不换说法 |
| 含具体示例 | 每一步都给了命令与可检查的完成标准 |
| 引用仅一级深度 | 只在依赖里散文式引用 `/code-review` |

> [!note] 三个字段的意图
> `name` 是触发名；`description` 面向模型、必须写清"什么情境该触发"（第 5 章 5.2 讲过的 model-invoked 写法）；步骤里"完成标准"是 5.3 模板的核心——它让模型知道"做到什么程度算完"，防过早完成。

**三种分发方式，按团队规模选** [plugin-marketplaces 文档](https://code.claude.com/docs/en/plugin-marketplaces)：

| 方式 | 做法 | 适用 |
|------|------|------|
| 仓库内自用 | 放 `.claude/skills/draft-release-notes/SKILL.md` | 单人项目，本仓库立刻可用 |
| GitHub + npx skills | 推到 `your-org/your-skills`，别的仓库执行 `npx skills@latest add your-org/your-skills` | 想分享、允许别人拿到可编辑副本 |
| 团队 Plugin | 加 `.claude-plugin/marketplace.json`（第 5 章 5.3 模板），成员 `/plugin marketplace add your-org/your-skills` | 3 人以上，要求版本一致、自动更新 |

三种方式按第 1 章的互斥规则，同一台机器同一批 skill 只走一种，别混装。单人项目直接用方式一，别为一个小 skill 建整个市场。

## 8.3 与本地/现有框架集成注意事项

真实项目多半不是从零开始的——仓库里可能已经有 CLAUDE.md、甚至同时跑 Codex。接入时注意三件事。

**双分发机制先对齐。** mattpocock/skills 自己就是"npx 可编辑副本 + Plugin 只读自动更新"双轨分发 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。你的自定义 skill 也要在接入时就选好轨道。集成进既有仓库前，先检查 `.claude/skills/` 下是否已有同名 skill——第 7 章 7.1 讲过两条路线重复的排错成本，别让一个仓库里同时躺着同名可编辑副本和同名插件。

**AGENTS.md 是跨平台契约，两边都要同步。** `/setup-matt-pocock-skills` 会把 `## Agent skills` 块同时写进 CLAUDE.md 和 AGENTS.md，因为两者各读各的：Claude Code 读 CLAUDE.md，Codex 读 AGENTS.md，对方默认忽略另一个。所以两块内容必须保持一致——你在 CLAUDE.md 手改 `## Agent skills` 块之外的工程规则时，同步改 AGENTS.md，反过来同理。只改一边，换工具时契约就丢一半。

> [!warning] 别只在一边加规则
> 如果仓库同时被 Claude Code 和 Codex 使用，只在 CLAUDE.md 里写"本仓库用 Vitest"，Codex 侧看不到；只在 AGENTS.md 里写，Claude Code 看不到。规则要么同步写进两份，要么维护一个同步脚本把一份镜像成另一份。

**与 Codex 同步的差异点。** 既有仓库如果像 mattpocock/skills 那样用同步脚本维持 CLAUDE.md / AGENTS.md 镜像，接入 skills 时要注意平台分发能力的不对称。这记在仓库的 [[ADR]]-0002 里：Claude Code 的 plugin.json 接受 skill 路径**数组**，能精确挑选要发布的子集；Codex 只接受单个路径**字符串**，无法从分桶结构中挑子集，所以 Codex Plugin 分发被**推迟**，先发能发的 Claude Code Plugin——这就是 deferred symmetry（刻意的不对称）[github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

对你的直接启示有两点：一是别把 Claude Code 的 plugin 行为迁移到 Codex 侧期待同样结果；二是这类"平台差异导致的延后"不是临时的，把原因、被拒方案写进 ADR，未来的维护者不用重新论证一遍为什么两边不对称。

## 本章小结

- 选型三步：画主工作流 → 从 4 个核心起步 → 反选法裁剪；有硬依赖的 `/to-spec`、`/to-tickets`、`/triage` 在没有 issue tracker 的仓库直接砍。
- 自定义 skill 用第 5 章 5.3 的模板起步，过六项质量关卡；`draft-release-notes` 实例约 20 行，可直接复制。
- 三种分发方式：仓库内 `.claude/skills/`（自用）、GitHub + `npx skills add`（分享）、marketplace.json Plugin（团队版本一致），同一批 skill 只走一种。
- 集成注意：CLAUDE.md / AGENTS.md 各读各的、内容必须同步；平台分发能力不对称（ADR-0002 的 deferred symmetry），把这类决策记成 [[ADR]]。

到这里，正文八章收尾。下一篇附录是命令速查卡，把安装、更新、初始化、触发、排错命令和 22 个 skill 的触发方式汇总成一页，日常随查随用。
