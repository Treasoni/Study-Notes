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

```
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
