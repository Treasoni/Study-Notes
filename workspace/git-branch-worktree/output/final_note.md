# git branch 与 worktree 实战指南

> 导读：这本笔记围绕「git branch 与 git worktree 到底有什么区别、各自适合什么场景、AI 开发时该用哪个」展开。建议按顺序阅读：第 1-2 章建立概念与逐项对比，第 3 章给决策框架，第 4 章落到 AI 并行开发实战，第 5 章当作命令手册随时查阅，第 6 章是可直接照做的最终结论。

## 目录

1. [第 1 章 从 branch 到 worktree：两个概念的本质](#第-1-章-从-branch-到-worktree两个概念的本质)
2. [第 2 章 核心差异：branch 与 worktree 逐项对比](#第-2-章-核心差异branch-与-worktree-逐项对比)
3. [第 3 章 决策框架：什么时候用 branch，什么时候用 worktree](#第-3-章-决策框架什么时候用-branch什么时候用-worktree)
4. [第 4 章 AI 开发实战：用 worktree 编排并行 Agent](#第-4-章-ai-开发实战用-worktree-编排并行-agent)
5. [第 5 章 worktree 命令手册与常见坑](#第-5-章-worktree-命令手册与常见坑)
6. [第 6 章 最终结论：AI 开发到底该用哪个](#第-6-章-最终结论ai-开发到底该用哪个)

---

## 第 1 章 从 branch 到 worktree：两个概念的本质

> 前置知识：会用 `add` / `commit` / `branch` / `checkout`，做过分支开发。

你是不是也遇到过这种场景：feature 写到一半，线上 hotfix 来了。`git switch` 一敲，Git 提示"你的本地修改会被覆盖"——于是你手忙脚乱 `git stash`、切分支、修 bug、切回来、`git stash pop`，结果还可能冲突。这一章先解决"这两个概念到底是什么"：branch 和 worktree 各解决哪一类问题，默认仓库为什么只有一个工作树，以及 worktree 是怎么打破这个限制的。

### branch 是什么——指向提交的指针

先从最熟悉的 branch 说起。Git 里的一个分支，本质上**只是一个指向某次提交的指针**。它记录的是"版本分叉"（version divergence），本身不产生任何工作目录：

```bash
git branch
# * main
#   feature-login
```

`feature-login` 这个名字背后，只是一个指向某次提交的引用。它告诉 Git："这条历史走到这里，最新提交是它。" 仅此而已——不占磁盘、不复制代码、不包含工作区。

```bash
git log --oneline -1 feature-login
# a1b2c3d (feature-login) feat: add login page
```

> [!note] 核心概念
> 分支 = 一个指向提交的可移动指针。切换分支只是换一个"指向"，并不创建新的文件副本。

那未提交的改动存在哪？它们"悬浮"（float）在当前检出的分支上——只存在于工作目录和暂存区（index），不属于任何提交。这直接引出下一个限制。

### 默认仓库的单工作树限制

默认情况下，一个仓库只有一个工作树（working tree）——也就是你 checkout 出来、能编辑的那层目录。同一时刻，它只能检出一个分支：

```text
my-project/               <- 全仓库唯一的工作树
├── .git/                 <- 仓库元数据
└── src/
```

你在 `main` 上改了 `src/app.ts`，想切去 `feature-login`？Git 会直接拒绝——未提交改动还悬浮在当前目录里，切过去要么被覆盖，要么被带过去污染别的分支：

```bash
git switch feature-login
# error: Your local changes to the following files would be overwritten by checkout:
#         src/app.ts
# 切换前必须保存当前状态
git stash
git switch feature-login
```

这就是单工作树的代价：**切换 = 先保存 + 换分支 + 再恢复**。切换越频繁，`stash` 丢失、pop 冲突、构建产物重新生成这类"切换税"越重。

> [!warning] 易错点
> 单工作树下，`git switch` / `checkout` 会拒绝"切换时会被覆盖"的未提交改动。你以为的"快速切换"，常常变成 stash → switch → pop → 解决冲突 四步走。

### worktree 是什么——同一仓库的多个工作目录

Git 2.5+ 引入的 `git worktree` 让**同一个仓库拥有多个工作目录**，每个目录检出不同分支，可同时开工。它解决的是"时间并行"（time parallelism）——同一时刻在不同目录并行推进不同任务 [GitHub Blog: What are git worktrees and why should I use them](https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them)。

```bash
# 默认只有一个主工作树
git worktree list
# /path/to/my-project   main   a1b2c3d

# 在仓库同级新建 ../login-work，检出新分支 feature-login
git worktree add -b feature-login ../login-work main

git worktree list
# /path/to/my-project   main           a1b2c3d
# /path/to/login-work   feature-login  b0e4f5a
```

现在 `/path/to/my-project` 和 `/path/to/login-work` 是两个互不干扰的工作目录：一个在 `main`，一个在 `feature-login`。在 `login-work` 里改代码、跑测试，主目录完全不受影响。

那"同一个仓库"为什么能有两个工作目录？底层上，每个 linked worktree 在 `$GIT_DIR/worktrees/<name>`（即 `.git/worktrees/<name>`）下有一份私有元数据，工作树顶层的 `.git` 文件（注意：是文件，不是目录）记录 `$GIT_DIR` 的位置 [git-worktree 官方文档](https://git-scm.com/docs/git-worktree)：

```text
# ../login-work/.git
gitdir: /path/to/my-project/.git/worktrees/login-work
```

而在私有元数据目录里，`commondir` 文件再指向主仓库的 `.git`，供 Git 推导 `$GIT_COMMON_DIR`：

```text
# .git/worktrees/login-work/commondir
../..
```

简单说：**`$GIT_DIR` 私有，`$GIT_COMMON_DIR` 共享**。这正是 worktree 比 `git clone` 轻量的根本原因——它不复制历史，只新增一套"当前状态"。

### 共享与私有的边界

理解了目录结构，共享与私有的边界就清楚了。它决定了哪些操作影响所有 worktree、哪些只影响当前目录：

| 共享（所有 worktree 通用） | 私有（每个 worktree 独立） |
|------|------|
| `refs/`（所有分支、标签引用） | `HEAD`（当前指向哪个分支） |
| 对象库（object database） | `index`（暂存区） |
| packed refs | `refs/bisect` |
| 默认 config（`.git/config`） | `refs/worktree` |
|  | `refs/rewritten` |

几个直观推论：

- 在 A worktree 里 `git commit`，B worktree **立刻能看到**这个新提交——对象库共享。
- 但 B 的 `HEAD` 不会跟着动——每个 worktree 独立持有"我现在在哪个分支、暂存了什么"。
- 在任意 worktree 里 `git config user.name`，写进的是主仓库的 `.git/config`，**影响所有 worktree**（后面章节的坑之一）。

> [!tip] 实践建议
> 记住边界：**引用和对象共享 = 历史互通、切换无痛；HEAD 和 index 私有 = 状态隔离、互不覆盖**。worktree 的本质，就是同一仓库的多套"HEAD + index"私有上下文。

### 一句话记忆

把两个概念钉死，只需要一句话 [GitHub Blog: What are git worktrees and why should I use them](https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them)：

> **Branches solve version divergence. Worktrees solve time parallelism.**
> 分支解决"版本分叉"，worktree 解决"时间并行"。

- branch 是**时间轴上**的版本选择：一个工作树同一时刻只能处于一个分支。
- worktree 是**空间上**的并行展开：不同目录同时跑不同分支。

### 本章小结

- branch 只是指向提交的指针，不产生工作目录；未提交改动悬浮在当前检出的分支上。
- 默认仓库只有一个工作树，同一时刻只能检出一个分支，切换要先 stash/commit。
- worktree（Git 2.5+）让同一仓库拥有多个工作目录，实现"时间并行"。
- linked worktree 通过 `.git/worktrees/<name>` 私有目录 + `commondir` 指向共享对象库，比 clone 轻量得多。
- refs 和对象库共享、HEAD 和 index 私有——这是 worktree 状态隔离的底层来源。

worktree 底层如此优雅，那实际用起来和 branch 到底差在哪？下一章从"工作模型、资源消耗、状态隔离"三个维度逐项对比，把"切换式"和"并行式"这笔账算清楚。

---

## 第 2 章 核心差异：branch 与 worktree 逐项对比

第 1 章讲清了 branch 是"指向提交的指针"、worktree 是"同一仓库的多个工作目录"。但概念清楚不等于会选。这一章把两者放到同一张桌上，从工作模型、资源消耗、与 clone 的关系、状态隔离四个维度逐项对比，把"切换式"和"并行式"的成本结构看清楚——这正是第 3 章决策框架的依据。

### 工作模型对比：切换式 vs 并行式

branch 的工作模型是"切换式"：整个仓库只有一套工作目录，你通过 `checkout`/`switch` 让这套目录在不同分支之间跳。切换前必须先把未提交改动 stash 或 commit 掉，否则 Git 会拒绝。频繁切换时，stash → switch → pop → 解决冲突 的"切换税"会不断累积 [git-worktree 官方文档](https://git-scm.com/docs/git-worktree)。

worktree 的工作模型是"并行式"：每棵树各自检出不同分支，各自独立编辑、独立跑测试，互不打断。你不需要"离开"当前工作，只需再开一个目录 [GitHub Blog: What are git worktrees and why should I use them](https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them)。

| 维度 | branch（切换式） | worktree（并行式） |
|------|----------------|-------------------|
| 同一时刻处理分支数 | 1 个（当前检出分支） | N 个（每树一个） |
| 切换要不要先保存状态 | 要（stash/commit） | 不要（各树独立） |
| 进行中的任务会被打断吗 | 会 | 不会 |
| 心智模型 | 时间轴上的"换挡" | 空间上的"多开几扇门" |

### 资源消耗对比

**磁盘占用**。branch 不复制代码，切换只改引用，几乎零额外磁盘。worktree 则每棵树各装一份依赖——node_modules、虚拟环境、构建缓存都要重新装一遍，多次 `npm/pip install` 会明显吃满磁盘 [GitHub Blog: What are git worktrees and why should I use them](https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them)。一个 2GB 的代码库跑多个并行会话，磁盘消耗可能翻倍到 10GB 级别 [developer.upsun.com: Git worktrees for parallel AI coding agents](https://developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents)。

**并发能力**。branch 受限于单工作树，无法同时跑两套 dev server 或两轮测试——它们会互相抢文件、抢端口。worktree 天然支持并发：每棵树可以各自启动构建、测试、进程。

**切换中断成本**。branch 切换会打断正在跑的构建和绑定在目录上的常驻进程，昂贵构建产物要重新生成；worktree 每个任务在自己的目录里"安家"，换任务不伤当前进度。

> [!tip] 一句话记成本
> branch 省磁盘、费"切换税"；worktree 费磁盘、省"切换税"。当切换税比磁盘贵时，worktree 就划算。

### 与 git clone 的对比

既然要多目录，为什么不直接 `git clone` 几个副本？差别在"共享 vs 复制"：

| 维度 | worktree | git clone |
|------|----------|-----------|
| 历史对象库 | 共享同一个 | 全量复制一份 |
| 分支间历史互通 | 天然互通（同一仓库） | 需 push/fetch 同步 |
| 创建速度 | 秒级（只加一套 HEAD/index） | 看仓库大小 |
| 磁盘成本 | 只多一份工作文件 | 多一份完整历史 + 工作文件 |

worktree 不复制历史，只新增一套"当前状态"，所以轻量得多；clone 是全量复制，历史与工作区都独立，跨目录同步要靠 push/fetch 走一遍 [git-worktree 官方文档](https://git-scm.com/docs/git-worktree)。作为参考，还有第三种"本地 clone 硬链接"方案（`git clone my-project my-project.my-branch-a`），对象文件通过硬链接共享历史、接近瞬时，但它是独立仓库，分支间要手动同步——适合容器化/常迁移的环境，本地常规开发用 worktree 更顺 [avdi.codes: You probably don't need git worktrees](https://avdi.codes/you-probably-dont-need-git-worktrees)。

> [!note] 关键区分
> worktree 是"同一个仓库的多个工作目录"；clone 是"多个仓库"。前者的分支天然互通，后者靠网络同步。

### 状态隔离对比

最后看哪些状态被隔离、哪些被共享——这决定了 worktree 到底"隔离"了什么。

**被隔离**（每棵树私有）：`HEAD`（当前在哪个分支）、`index`（暂存区）、工作目录本身、以及各树独立的依赖副本。所以在一棵树里改到一半、还没 commit 的东西，另一棵树完全看不见，也不会触发"会被覆盖"的切换拒绝。

**被共享**（所有树通用）：`refs/`（全部分支、标签引用）、对象库、默认 config。所以任意一棵树 commit 后，其他树立刻能看到这个新提交；反过来，在一棵树里 `git config`，写进的是主仓库 `.git/config`，影响所有树 [git-worktree 官方文档](https://git-scm.com/docs/git-worktree)。

| 状态 | 隔离？ | 后果 |
|------|-------|------|
| HEAD / index / 工作目录 | 私有 | 未提交改动互不覆盖 |
| 依赖副本（node_modules 等） | 私有 | 每树各装一份，磁盘翻倍 |
| refs / 对象库 | 共享 | 历史天然互通，commit 即时可见 |
| 默认 config | 共享 | 一处改配置，全局生效 |

> [!warning] 别被"隔离"二字骗了
> worktree 隔离的是"工作状态"，不是"环境"。依赖、端口、数据库仍是需要自己处理的现实问题，等第 4 章讲 AI 并行时再展开。

把这四笔账算清楚后，第 3 章就可以给出决策框架：什么场景该用 branch、什么场景该上 worktree。

---

## 第 3 章 决策框架：什么时候用 branch，什么时候用 worktree

前两章把两者的机制和差异算清楚了，但真正到项目里，你还是会停在同一个问题上：**这次到底该开分支，还是建 worktree？** 这一章不给"永远用哪个"的答案，而是给一条可执行的判断准则、几类典型场景，外加一张速查表——看完你就能在 10 秒内做出选择。

### 核心决策准则：「若切换会摧毁状态，就用 worktree」

判断的核心只有一句话 [GitHub Blog: What are git worktrees and why should I use them](https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them)：

> [!note] 核心决策准则
> **若切换会摧毁状态，就用 worktree。** 这里的"状态"，指的是任何"切走再切回来，代价大到不想承受"的东西。

什么是会被切换摧毁的状态？至少这几类：

| 状态类型 | 为什么切换会摧毁它 |
|------|------|
| 未提交改动 | 单工作树下 `switch` 会直接拒绝，逼你先 `stash`；`stash pop` 还可能冲突 |
| 昂贵构建产物 | `node_modules`、`build/`、编译缓存：切回来要重新生成，动辄几分钟到几十分钟 |
| `.env` / 依赖版本 | 环境配置跟着工作目录走，切换后可能不匹配、要重新配置 |
| 目录绑定的常驻进程 | dev server、watch 进程绑定在某个目录上，换分支不一定跟着走 |

只要命中其中任意一条、且你想保留它，branch 的"切换式"工作流就注定要交税（stash → switch → pop → 解决冲突）。这时把任务挪进一个独立 worktree，反而是零成本的解法。

### 用 branch 的场景

反过来，当状态很"干净"时，branch 依然是最轻的选择 [GitHub Blog: What are git worktrees and why should I use them](https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them)：

- **单一短线性任务**：一个分支从头做到尾，没有并发。
- **切换不频繁**：一天切不了几次分支。
- **stash/switch 中断可接受（<30 分钟）**：切走再切回的成本在可容忍范围。
- **短期 spike / 原型分支**：试一两个方案就删，不值得为它单独建目录。

典型流程就是最普通的 Git 日常：

```bash
git switch -c feat-login
# ... 开发、提交 ...
git switch main
git merge feat-login
git branch -d feat-login
```

> [!tip] 实践建议
> 判断标准不是"我有几个分支"，而是"我同一时刻要不要同时动它们"。只有一个任务在线时，branch 就够了——别为了用 worktree 而用 worktree。

### 用 worktree 的场景

只要"并发"两个字出现，worktree 就登场了。以下场景强烈推荐甚至强制用 worktree [developer.upsun.com: Git worktrees for parallel AI coding agents](https://developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents)：

- **紧急 hotfix + 进行中的 feature**：feature 改到一半，线上出了 bug——最经典、最该用 worktree 的场景。
- **多 feature 分支并行开发**：2+ 个并发活跃任务，每个任务一个 worktree。
- **长时重构**：重构动辄数小时，`stash pop` 冲突高频，状态经不起切走。
- **分支间依赖版本不同**：A 分支要装新依赖、B 分支还不能要——两个目录各装各的，互不污染。
- **需要并发跑构建/测试/进程**：两个目录同时 `npm test`，互不阻塞。
- **同一功能基于多个 base 测试**：同时基于 `main` 和 `release` 各检出一份验证。

对应命令，一行解决：

```bash
# 基于 main 新建 hotfix 分支，放到仓库同级目录 ../hotfix
git worktree add -b hotfix ../hotfix main

# 在 ../hotfix 里改完、commit 并合并回主树后，清理：
git worktree remove ../hotfix
git worktree prune   # 手动删过目录时，记得清理残留的管理记录
```

用 branch 表达"我想做这个功能"，用 worktree 表达"我要同时开工"——两者叠加就是完整的多任务布局。

### 适用场景速查表

把上面的判断浓缩成一张表，直接对着查 [git-worktree 官方文档](https://git-scm.com/docs/git-worktree)：

| 场景 | 选择 | 原因 |
|------|------|------|
| 紧急 hotfix + 进行中的 feature | worktree | 不打断进行中的状态 |
| 多 feature 分支并行开发 | worktree | 每任务一个目录，互不干扰 |
| PR review 需本地运行 | worktree（或快速 stash/switch） | 几分钟内可 stash 时 branch 也能顶 |
| 跨分支代码对比与调试 | worktree | 两个目录并排打开，直接看 |
| 长时重构 / 高风险改动隔离 | worktree | stash pop 冲突高频，状态必须保留 |
| 并行跑测试/构建/CI | worktree | 目录级并发，互不阻塞 |
| 单一分支线性开发 | branch 即可 | 没有并发，别过度工程 |
| 项目体积极小 | branch / 直接 clone | worktree 收益可忽略 |
| 容器 / devcontainer 环境 | 谨慎 | 路径硬编码问题，见下节 |

### 何时不需要 worktree

worktree 不是银弹，有两类情况反而该退回更朴素的方案 [avdi.codes: You probably don't need git worktrees](https://avdi.codes/you-probably-dont-need-git-worktrees)：

**容器 / devcontainer 环境**。worktree 的路径是硬编码写进配置的，容器里路径经常和宿主机不一致，环境基本不可用。`worktree.useRelativePaths` 这个配置项要 Git ≥2.48（2025 年）才支持，且 IDE 对它的支持还不成熟 [git-worktree 官方文档](https://git-scm.com/docs/git-worktree)。结论：环境经常迁移或容器化，优先本地 clone。

**替代方案：本地 clone 硬链接**。如果只是想要"一个临时目录能同时开工"，不必上 worktree：

```bash
# 近瞬时，几乎不额外占磁盘：对象文件通过硬链接共享历史
git clone my-project my-project.my-branch-a
# 把新 clone 的 origin 指回真正上游即可
```

这个方案对"环境常迁移"更友好——它就是一个独立仓库，不依赖主仓库的管理元数据。常规本地开发仍推荐 worktree（共享对象库、历史天然互通、一次 fetch 全部更新），但知道这条退路，你就不必在容器里硬刚 worktree。

### 本章小结

- 核心判断只有一句：**切换会摧毁状态（未提交改动、构建产物、`.env`、常驻进程）就用 worktree**。
- 单一短线性任务、切换不频繁、中断 <30 分钟可接受 → 用 branch 就够了。
- hotfix + 进行中 feature、多 feature 并行、长时重构、依赖版本不同、并发跑测试 → 用 worktree。
- 对着速查表查场景即可，别为用而用。
- 容器/devcontainer 路径硬编码，以及"本地 clone 硬链接"，是 worktree 的两条退路。

掌握了"什么时候用哪个"，下一章进入这本笔记的重头戏——AI 开发实战：看 Claude Code 和并行 agent 场景下，worktree 如何成为编排利器，以及有哪些硬伤要提前补。

---

## 第 4 章 AI 开发实战：用 worktree 编排并行 Agent

> 前置知识：第 1 章的 worktree 概念、第 3 章的决策框架。这一章把前几章的判断，落地到「让 AI 帮我写代码」这个真实场景。

前三章算清了 branch 与 worktree 的账，但你最关心的问题很可能是：我让 AI 写代码，到底该用哪个？这一章直接给出答案——当你开多个 AI 会话、多个 agent 并行干活时，**worktree 几乎总是对的选择**。原因不只是「并行」这两个字，而是文件系统级隔离能避免 agent 因为切分支而丢失上下文。顺着这个逻辑，本章会讲清楚 Claude Code 对 worktree 的一等支持、多 agent 的目录布局、完成后的清理，以及 AI 并行工作流最容易被忽略的六个硬伤。

### 为什么 AI 开发优先 worktree

先想一个关键差异：人切分支，靠的是记忆和 stash；AI agent 切分支，靠的是「它打开过的文件 + 对话历史 + 未提交改动」。这三样恰好是 `git switch` 最容易摧毁的东西。

- 一个 agent 正在 `feature-auth` 上改到一半，你让它切到 `main` 去修个 bug——它打开过的文件全部变了，未提交的改动被 stash 或丢弃，它的「工作记忆」就此断裂。
- worktree 给每个 agent 一个**永远不被别人动的目录**。agent 眼里只有自己的目录和分支，不切分支、不 stash、不恢复，上下文自然就不会丢。这就是「文件系统级隔离」在 AI 场景下的真正含义 [Upsun: Git worktrees for parallel AI coding agents](https://developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents)。

这个判断并不是理论推演，AI 生态已经把 worktree 当成了**事实默认** [GitHub Blog: What are git worktrees and why should I use them](https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them)：

- GitHub Copilot App 每个新会话默认「New worktree」。
- Cursor 的 Parallel Agents 直接构建在 worktree 之上。
- incident.io 日常同时跑 4-5 个并行 Claude agent。

> [!note] 核心结论
> 多会话、多 agent 并行的 AI 开发，优先 worktree。Claude Code 的标准动作就是 `claude --worktree`——worktree 已是这个领域的默认基础设施。

### Claude Code 的 worktree 一等支持

Claude Code 把 worktree 做成了内置功能，一条命令即可给 AI 会话开一个独立工作目录 [Claude Code worktrees 官方文档](https://code.claude.com/docs/en/worktrees)：

```bash
# 在仓库根目录，为当前会话建一个独立 worktree
claude --worktree feature-auth
# 等效写法：claude -w feature-auth
```

这条命令做了三件事：

1. 在 `.claude/worktrees/feature-auth/` 建独立工作目录；
2. 自动切到 `worktree-feature-auth` 分支；
3. 会话结束自动清理（除 `-p` 非交互模式——该模式下**不做清理**，需要你手动 `git worktree remove`）。

几个值得记住的细节：

- **不写名字则随机生成**；重跑同名 `claude --worktree feature-auth` = 重开已有的 worktree，而不是新建。
- **`worktree.baseRef`** 控制新 worktree 的起点：`"fresh"`（默认，从远端默认分支拉一个干净树）或 `"head"`（从当前本地 HEAD 分支出发，**携带未提交的工作**）。做实验想干净从 `fresh` 开始；想接着手上的活儿继续，用 `head`。

```json
// Claude Code settings：让新 worktree 基于当前工作继续
{
  "worktree": {
    "baseRef": "head"
  }
}
```

- **`.worktreeinclude`**：用 `.gitignore` 语法，把 `.env` 这类被忽略的配置文件**自动复制进每个新 worktree**——否则每个新树都要手动补环境变量：

```text
# .worktreeinclude
.env
```

- **子代理级并行**：在 agent 的 frontmatter 里加一行 `isolation: worktree`，每次运行都会落在自己的临时 worktree 里，运行期被 lock、结束有改动则按 `cleanupPeriodDays` 清理；它**不会删除用户显式创建的 worktree**：

```markdown
---
description: 专注 auth 模块的并行子代理
isolation: worktree
---
```

- **桌面版**（desktop app）：每个新会话自动获得一个 worktree，无需手动干预。

> [!tip] 实践建议
> 单人用 `claude --worktree <name>` 就够了；要并行多个子代理，靠 `isolation: worktree` 让每个子代理自动隔离，比手动管理一堆目录省心。

### 多 agent 并行布局：一个 agent = 一个 worktree + 一个分支

用 Claude Code 自动建树很省事，但理解手动布局能帮你掌控一切。标准模式是：**一个 agent = 一个 worktree + 一个分支**，目录放在仓库**同级**（sibling 目录），不要放在仓库内部 [Claude Code worktrees 官方文档](https://code.claude.com/docs/en/worktrees)。

```bash
# 在主仓库目录下，为两个并行 agent 分别建树
git worktree add -b feature-auth ../auth-work main
git worktree add -b feature-payment ../payment-work main

git worktree list
# /path/to/my-project     main            a1b2c3d
# /path/to/auth-work      feature-auth    b0e4f5a
# /path/to/payment-work   feature-payment c5d6e7f
```

然后把 agent A 指到 `../auth-work`、agent B 指到 `../payment-work`，两者互不可见、互不干扰。这个布局的收益：

| 收益 | 说明 |
|------|------|
| 上下文隔离 | agent 只见自己目录里的文件，不会被别的分支改动惊扰 |
| 会话历史保留 | 每个 agent 的对话记录与目录绑定，重开目录即重开会话 |
| 安全实验 | worktree 可试、可删、可重建，试错不污染主目录 |
| 一次 fetch 全更新 | 对象库共享，任意树里 `git fetch`，所有 worktree 同时看到新远端 |
| 省磁盘 | 共享对象库，不复制历史，远轻于 `git clone` |

目录命名用 `主仓库名-分支名`（如 `../my-project-feat-login`）或 `wt/<issue-id>-<slug>`，避免 `../test` 这类模糊命名。放在仓库同级还有一个隐藏好处：**不会踩 `.gitignore` 陷阱**——worktree 若建在主仓库目录内部，必须把它加进 `.gitignore`。

### 完成与清理

并行布局容易，「收摊」才是纪律的考验。一个 agent 完成后的完整序列 [Claude Code worktrees 官方文档](https://code.claude.com/docs/en/worktrees)：

```bash
# 1. 在 agent 的 worktree 里提交
cd ../auth-work
git add . && git commit -m "feat: add auth flow"

# 2. 回主仓库合并
cd ../my-project
git merge feature-auth

# 3. 立即删除 worktree —— 注意按目录路径删除，不是分支名
git worktree remove ../auth-work

# 4. 清理残留的管理记录
git worktree prune
```

几条必须养成的纪律：

- **合并后立即 `git worktree remove`**，别留着一堆「也许还要用」的树——它们会持续吃磁盘。
- **手删目录后必须 `prune`**：直接 `rm -rf` 掉目录的话，`.git/worktrees/` 里的管理记录会残留，`prune` 负责清除这些失联记录。
- **`.claude/worktrees/` 加入 `.gitignore`**：Claude Code 自动建的树都在这个目录里，别让它们被 git 跟踪。

> [!tip] 实践建议
> 记住这条收尾咒语：**commit → merge → remove → prune**。四步走完，分支、worktree、管理记录全部归零，不留尾巴。

### AI 并行工作流的六个硬伤与补救

worktree 解决的是「目录隔离」，但它**不解决环境隔离**——端口、依赖、数据库、磁盘这些都要你自己补 [Claude Code worktrees 官方文档](https://code.claude.com/docs/en/worktrees)。下面六个硬伤，是并行 AI 开发最常翻车的地方。

> [!warning] 硬伤一：端口冲突
> 多个 worktree 同时跑 dev server，默认抢 `3000`/`5432`/`8080`。补救：给每个 worktree 一个端口偏移，用公式 `SERVICE_PORT = BASE_PORT + (WORKTREE_INDEX * 10) + SERVICE_OFFSET`。
> ```bash
> # 例：BASE_PORT=3000，第 3 个 worktree（index=2），服务偏移 0
> SERVICE_PORT=$(( 3000 + 2 * 10 + 0 ))   # → 3020
> ```

> [!warning] 硬伤二：依赖不迁移
> 新 worktree 里没有 `node_modules/` 和 `.env`，每棵树都要重装。补救：用 `pnpm`（符号链接共享依赖）代替 `npm`，显著省空间省时间。
> ```bash
> cd ../auth-work && pnpm install   # 符号链接复用，比 npm 的硬拷贝省得多
> ```

> [!warning] 硬伤三：IDE 支持割裂
> JetBrains 没有原生 worktree UI；VS Code 到 2025 年才有正式支持；Claude Code 的 `/ide` 也认不出 worktree 路径。补救：命令行管理 worktree（alias 见第 5 章），IDE 只负责打开具体目录。

> [!warning] 硬伤四：数据库没有隔离
> worktree 共享本地数据库、Docker daemon、缓存——A agent 的 schema 迁移会波及 B。补救：**逐 worktree 建库实例**，volume 名带上 worktree index（如 `pgdata-wt3`），让每个树有自己的数据库世界。

> [!warning] 硬伤五：磁盘翻倍
> 一个 2GB 的代码库，20 分钟会话可能消耗近 10GB；monorepo 的构建缓存还会逐树放大；被遗忘的 worktree 悄悄吃 GB 级空间。补救：定期 `git worktree list` 盘点 + `remove`/`prune`，给磁盘设告警。

> [!warning] 硬伤六：自我制造的 merge conflict
> 并行 agent 碰同一批文件几乎必然冲突，而且 git 不会提前预警。补救：**任务划分 + orchestrator 协调**——尽量让 agent 各管各的模块，合并后立即删 worktree，减少冲突窗口。

> [!note] 一句总结
> worktree 负责「文件系统级隔离」，端口、依赖、数据库、磁盘这些「环境级隔离」要自己补。这也是第 6 章结论里「worktree 不是银弹」的含义。

### 本章小结

- AI agent 的上下文依赖「打开的文件 + 对话历史 + 未提交改动」，切分支会一次性摧毁这三样——worktree 的文件系统级隔离天然规避这一点。
- Claude Code 对 worktree 是一等支持：`claude --worktree <name>`（别名 `-w`）、`worktree.baseRef`（fresh/head）、`.worktreeinclude` 复制 `.env`、子代理 `isolation: worktree`。
- 多 agent 并行标准布局：一个 agent = 一个 worktree + 一个分支，sibling 目录命名（`git worktree add -b feature-auth ../auth-work main`）。
- 收尾咒语：commit → merge → `git worktree remove` → `git worktree prune`，并把 `.claude/worktrees/` 加进 `.gitignore`。
- 六个硬伤要自己补：端口偏移、依赖重装、IDE 割裂、数据库隔离、磁盘翻倍、并行 agent 自我制造的 merge conflict。

这一章的命令只是冰山一角——第 5 章把 worktree 的命令全集和十个最常见坑整理成一份随时可查阅的命令手册，遇到报错直接翻它。

---

## 第 5 章 worktree 命令手册与常见坑

> 前置知识：已通读第 1-4 章，知道 worktree 的本质是「同一仓库的多套 HEAD + index 私有上下文」，并能用 `git worktree add` 建第一个树。

前面几章讲了"为什么"和"什么时候"，这一章落到"怎么敲"：把 `git worktree` 的全套命令、关键参数、命令形态记忆法一次性列成速查手册，然后老老实实排一遍我踩过和看别人踩过的十个坑，最后给一套可以直接抄的最佳实践。建议你把这章当成手册用：用到哪条查哪条，坑和最佳实践部分通读一遍留个印象。

### worktree 命令全集

`git worktree` 一共有 8 个子命令，绝大多数日常操作只用到 add / list / remove / prune 四个 [git-worktree 官方文档](https://git-scm.com/docs/git-worktree)。先给全集总表：

| 命令 | 用途 | 关键参数 |
|------|------|---------|
| `git worktree add <path> [commit-ish]` | 新建并检出 | `-b/-B <branch>` 新建分支（`-B` 已存在则重置）、`-d/--detach` 分离 HEAD、`--orphan` 空树、`--no-checkout` 配合 sparse-checkout、`-f/--force`、`--lock` 创建即锁、`--track`、`--guess-remote` |
| `git worktree list` | 列出所有 worktree | `-v` 显示原因、`--porcelain` 脚本解析、`--expire` 标过期 |
| `git worktree lock/unlock` | 防止被 prune/move/remove | `--reason` 记录原因 |
| `git worktree move` | 移动 worktree | 主树和含 submodule 的树不可移；锁定树需两次 `--force` |
| `git worktree remove [-f]` | 删除（按**目录路径**，不是分支名） | 默认仅干净工作树；`-f` 强制丢弃未提交改动；主树不可删 |
| `git worktree prune [-n] [-v]` | 清理手动删除后残留的管理记录 | `-n` dry-run |
| `git worktree repair` | 修复因移动而失联的管理文件 | 主树移动在根跑，linked 树在其内部跑 |

下面按使用频率逐个演示。`add` 是最常用也是参数最复杂的，四个典型形态：

```bash
# 1. 只给路径，按路径 basename 自动建分支并检出
git worktree add ../hotfix
# 等价于 git worktree add -b hotfix ../hotfix HEAD

# 2. 显式建新分支
git worktree add -b feature-login ../login-work

# 3. 基于某个 base（分支/tag/commit）建分支
git worktree add -b feature-login ../login-work main

# 4. 分离 HEAD，常用于临时调试某个历史提交
git worktree add --detach ../debug a1b2c3d
```

`--no-checkout` 常配合 sparse-checkout 用：只想拿部分文件时，先建空树再 `git sparse-checkout set <dir>`，避免整棵全量检出。`--lock` 会在创建的同时锁上，适合放在网络/可移动磁盘上的树，防 `prune` 误清。

查看和清理：

```bash
git worktree list
# /path/to/my-project   main           a1b2c3d
# /path/to/login-work   feature-login  b0e4f5a

# 脚本解析用 --porcelain，输出更稳定
git worktree list --porcelain

# 手动删了目录后，清理残留管理记录（-n 先预览）
git worktree prune -n
git worktree prune

# 移动 worktree 后修链接；主树移动在仓库根跑，linked 树在其内部跑
git worktree repair
```

### 命令形态记忆

命令不难，难在"哪条命令吃路径、哪条吃分支名"。三个记忆锚点帮你钉死：

**锚点一：`add` 里分支名是"可选增强"，路径才是必填。** 只写路径时，Git 自动取路径 basename 当分支名：

```bash
git worktree add ../hotfix      # 分支 = hotfix
git worktree add ../wt-1234     # 分支 = wt-1234（这就是 wt/<issue-id> 命名的由来）
```

**锚点二：加分支的完整形态是 `-b <branch> <path> <base>`。** 顺序别记反：分支名在 `-b` 后紧跟，然后是目录路径，最后才是 base。想从 `main` 拉分支，就是 `git worktree add -b feature-auth ../auth-work main`。

**锚点三：删除按目录路径，不按分支名。** 这是新手最常卡的一处——`remove` 的入参是你当初 `add` 时给的**路径**：

```bash
# 错：git worktree remove feature-login
git worktree remove ../login-work
```

删完管理记录同步消失，但分支本身还在。分支要单独删：`git branch -d feature-login`（对应 `-b` 建的分支）。

### 十个常见坑

按踩坑频率和杀伤力排序，逐个排雷：

**1. 同分支双检出。** 同一个分支在同一仓库只能被一个 worktree 检出，第二次 `add` 报 `fatal: 'branch-name' is already checked out at 'path'`。解决：删掉旧 worktree，或临时调试用 `--detach`（分离 HEAD 不占分支）。

**2. 目标目录必须为空。** 一个目录只能有一个工作树，`add` 到已有内容的目录会直接报错。要么换个空路径，要么先清空该目录。

**3. `remove` 默认拒绝未提交改动。** 有未提交改动时删除报 `working tree not clean`。先 commit/stash，或明确确认后 `git worktree remove -f` 强制丢弃——注意 `-f` 会丢数据，谨慎用。

**4. 主工作树不可删、不可移。** `remove` / `move` 对主树（你最初 clone 出来的那个目录）都是禁区，这是设计上就锁死的。

**5. 局部配置残留。** 在 worktree 里跑 `git config user.name`，写进的是主仓库 `.git/config`，**影响所有 worktree**，删掉这棵树后也不会自动清理。想按树隔离，要配 `worktree.config` 相关机制，别指望"这棵树自己的配置"会自动跟着树消失。

**6. push 目标缺失。** 主仓库没有配置 remote 时，在 worktree 里 `git push` 报 `No configured push destination`。先回主仓库补 `git remote add origin <url>`，worktree 共享 remote 配置后立刻可用。

**7. 依赖膨胀。** 每个 worktree 各装一份 node_modules / vendor，反复 `npm install` / `pip install` 会把磁盘吃满。这是 worktree 并行的最大隐藏成本，后面最佳实践里会再强调。

**8. `.gitignore` 陷阱。** 若把 worktree 建在主仓库目录**内部**（如 `my-project/.worktrees/xxx`），这些目录必须加进 `.gitignore`，否则会被当成待跟踪内容。更省心的做法是放到主仓库**外**的 sibling 目录，从根上绕开这个问题。

**9. 手动删目录必须 `prune`，手动移动目录必须 `repair`，两者不可混用。** 你手动 `rm -rf` 一个 worktree 目录后，Git 的管理记录还在，`worktree list` 仍会显示它——必须补 `git worktree prune`；同理，手动 `mv` 目录后要用 `git worktree repair` 修复失联。跳过哪个都会留下脏状态。

**10. submodule 多检出仍属实验性。** 含 submodule 的 worktree，`move` 被禁止，`remove` 需要 `--force`。项目里有 submodule 时，对 worktree 要格外保守。

> [!warning] 易错点
> 坑 9 是"手贱后遗症"高发区：`rm -rf` 删了目录却忘了 `prune`，Git 会在 `list` 里显示一个"幽灵 worktree"，第二次 `add` 到同一路径还会莫名报错。养成习惯：手删目录 = 立刻 `git worktree prune`。

### 最佳实践

**目录命名：** 用 `主仓库名-分支名`（如 `../my-project-feat-login`）或 `wt/<issue-id>-<slug>`（如 `../wt-1234-auth`）两种模式，一眼能看出"哪个仓库、哪个任务"。避免 `../test`、`../tmp` 这种模糊命名——多个 worktree 并排时你会完全分不清谁是谁。

**清理时机：** 分支 commit + push 之后**立即** `git worktree remove`，别让树"躺"在那里。被遗忘的 worktree 是磁盘膨胀的主要来源（一个 2GB 代码库可能吃出近 10GB 空间），合并完就删是纪律不是可选优化。

```bash
# 一个完整生命周期
git worktree add -b feature-auth ../auth-work main   # 建树
# ... 开发、commit、push ...
git worktree remove ../auth-work                      # 立即清理
git branch -d feature-auth                            # 分支已合并，顺手删
```

**配置别名：** 手敲 `git worktree` 前缀太长，设一组全局 alias [Git 官方文档：别名](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases)：

```bash
git config --global alias.wt-list   "worktree list"
git config --global alias.wt-add    "worktree add"
git config --global alias.wt-remove "worktree remove"
git config --global alias.wt-prune  "worktree prune"
# 之后：git wt-add -b feature-login ../login-work main
```

**Git 版本：** worktree 需要 2.5+，但 2.5 的 add 形态还很粗糙，建议 2.15+（修复了若干 linked worktree 管理 bug）。macOS 上检查并升级：

```bash
git --version        # 看当前版本
brew update git      # macOS 用 Homebrew 升级到最新
```

**网络/可移动磁盘用 lock：** 放在 U 盘、网络挂载盘上的 worktree，随时可能因为盘暂时不在线被 `prune` 当成"失联"清掉。创建时加 `--lock`，或事后手动锁：

```bash
git worktree lock ../portable-work --reason "U 盘，勿自动清理"
git worktree list -v        # -v 能看到 lock 原因
git worktree unlock ../portable-work
```

> [!tip] 实践建议
> 如果你是 AI 开发为主，最佳实践浓缩成一句话：**sibling 目录 + 命名含分支名 + 合并即删 + 手删即 prune**。这四条能从根上避开坑 7、8、9，也正好是第 4 章多 agent 布局的地基。

### 本章小结

- `git worktree` 共 8 个子命令，日常只靠 add / list / remove / prune 四个就能跑通；`add` 的关键形态是 `-b <branch> <path> <base>`。
- 三个记忆锚点：路径才是必填、分支名在 `-b` 后、**删除按路径不按分支名**。
- 十个坑的高频区：同分支双检出（坑 1）、手删目录忘 `prune`（坑 9）、依赖膨胀（坑 7）、局部配置残留（坑 5）。
- 最佳实践四件套：`主仓库名-分支名` 或 `wt/<issue-id>-<slug>` 命名、合并即 remove、配置 wt-* alias、Git 升到 2.15+。
- 网络盘/U 盘上的树记得 `lock` 防误清。

命令都会了，坑也排过了，最后一步只剩拍板：**AI 开发到底该用 branch 还是 worktree**？下一章给出最终结论、决策矩阵速查和工程纪律清单。

---

## 第 6 章 最终结论：AI 开发到底该用哪个

> 前置知识：已完成第 1-5 章，或至少理解了 branch/worktree 的差异与第 3 章决策框架。

前五章把 branch 和 worktree 的概念、差异、决策框架、AI 实战和命令手册都过了一遍。这一章把它们压缩成可以直接照做的结论：一个默认规则、一个 AI 开发结论、一张决策矩阵速查表、一份工程纪律清单。以后拿不准该用哪个，翻这一章就够了。

### 默认规则与例外

先给最朴素的默认答案 [GitHub Blog: What are git worktrees and why should I use them](https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them)：

- **单一短线性任务 → branch**。只做一件事、切换不频繁、中断可接受（<30 分钟），用一个分支加必要的 stash/switch 就够了，别过度工程。
- **2+ 并发任务 / 需并行跑测试构建 / 切分支会破坏状态 → worktree**。这里的状态指：不想 stash 的未提交改动、昂贵不想重新生成的构建产物、`.env` 与依赖版本等环境配置、绑定在目录上的常驻进程。

**例外**（来自素材的反方观点）：

- **容器 / devcontainer 环境**：worktree 路径硬编码基本不可用，退回本地 clone 硬链接方案（近瞬时、几乎不额外占磁盘）。
- **磁盘或进程受限**：worktree 每树各装一份依赖、各占一份缓存，开太多会吃满磁盘。
- **项目体积极小**：clone 成本可忽略，branch 或直接 clone 即可。

### AI 开发结论

**AI 开发优先 worktree。** 多会话、多 agent 并行时，worktree 提供文件系统级隔离，避免 agent 因切分支丢失上下文——这已是 AI 生态的事实默认（Copilot、Cursor 的并行模式都构建在 worktree 上）。Claude Code 的标准动作就是 `claude --worktree <name>`，一个 agent = 一个 worktree + 一个分支，命名 sibling 目录，任务完成即删 [Claude Code worktree 文档](https://code.claude.com/docs/en/worktrees)。

> [!tip] 最终推荐
> 用 AI 写代码、同时开多个会话/agent 做不同任务 → **每个任务一个 worktree**（`claude --worktree` 或 `git worktree add -b <branch> ../<name> main`），合并后立即删除。只在「单任务、几分钟内、切换无痛」时才退回 branch。

但 worktree 不是银弹：**端口、依赖、数据库、IDE 的环境隔离要自己补**。并行 agent 抢 3000/5432/8080 端口、新 worktree 缺 node_modules/.env、共享本地库无隔离、IDE 对 worktree 路径支持割裂——这些都不会默认帮你解决。

### 决策矩阵速查

| 情形 | 选择 |
|------|------|
| 有未提交工作又需要切换 | worktree |
| 不同分支依赖版本不同 | worktree |
| 需要并行跑测试 / 基于多 base（main/release）测试 | worktree |
| 快速 review（<30 分钟） | branch + stash |
| 磁盘或进程受限 | 少开 worktree，必要时用 clone 硬链接 |
| 普通单 feature 开发 | 一个 branch 即可，别过度工程 |

### 工程纪律清单

- **目录命名**：sibling 目录用 `主仓库名-分支名` 或 `wt/<issue-id>-<slug>`，避免 `../test` 这种模糊名。
- **合并后立即清理**：分支 commit + push 后立刻 `git worktree remove <path>`。
- **手删必须 prune**：手动删了目录必须补 `git worktree prune`；手动移动目录必须 `git worktree repair`。
- **`.claude/worktrees/` 加入 `.gitignore`**：Claude Code 自动建树目录，别让它们混进提交。
- **网络 / 可移动磁盘**：用 `git worktree lock` 防意外 prune。
- **Git 版本**：保持 ≥ 2.15（worktree 稳定版），macOS 用 `brew update git`。

### 收束：整份笔记的闭环

到这里整份笔记闭环了：**第 1-2 章建概念，第 3 章给决策框架，第 4 章讲 AI 实战，第 5 章当命令手册，第 6 章（本章）是最终答案**。把上面的决策矩阵和纪律清单贴到桌面，下次并行开发直接照着执行；真拿不准时，回到第 4 章把 `claude --worktree` 的完整流程敲一遍，比查文档快得多。
