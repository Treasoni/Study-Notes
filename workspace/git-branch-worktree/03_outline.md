# git branch 与 worktree 实战指南

> 笔记类型：实战笔记（含对比要素）
> 预计总篇幅：约 6-8 页
> 章节数：6

## 第 1 章 从 branch 到 worktree：两个概念的本质
- 篇幅：中
- 素材引用：一、核心机制对比
- 代码示例：有
- 小节：
  - ### branch 是什么——指向提交的指针：分支只是指针、本身不产生工作目录；未提交改动「悬浮」在当前检出分支上
  - ### 默认仓库的单工作树限制：同一仓库只有一个工作树，同一时刻只能检出一个分支；切换需先 stash 或 commit
  - ### worktree 是什么——同一仓库的多个工作目录：Git 2.5+ 带来的「时间并行」能力；linked worktree 在 `$GIT_DIR/worktrees/<name>` 有私有目录，顶层 `.git` 文件记录 `$GIT_DIR` 与 `$GIT_COMMON_DIR`
  - ### 共享与私有的边界：refs、对象库、packed refs、默认 config 共享；HEAD、index、refs/bisect、refs/worktree、refs/rewritten 私有
  - ### 一句话记忆：Branches solve version divergence. Worktrees solve time parallelism.

## 第 2 章 核心差异：branch 与 worktree 逐项对比
- 篇幅：中
- 素材引用：一、核心机制对比；三、使用场景与决策框架
- 代码示例：无
- 小节：
  - ### 工作模型对比：切换式 vs 并行式——checkout/switch 在同一目录换分支，worktree 在不同目录同时跑不同分支
  - ### 资源消耗对比：磁盘占用（每树一份依赖）、并发跑构建/测试/进程的能力、切换中断成本
  - ### 与 git clone 的对比：worktree 共享对象库所以轻量得多，分支间历史天然互通；clone 是全量复制
  - ### 状态隔离对比：哪些被隔离（HEAD/index、工作目录、依赖副本）、哪些被共享（refs/对象库/config）

## 第 3 章 决策框架：什么时候用 branch，什么时候用 worktree
- 篇幅：中
- 素材引用：三、使用场景与决策框架；四、常见坑与最佳实践
- 代码示例：有
- 小节：
  - ### 核心决策准则：「若切换会摧毁状态，就用 worktree」——状态包括未提交改动、昂贵构建产物、.env/依赖版本、目录绑定常驻进程
  - ### 用 branch 的场景：单任务线性开发、切换不频繁、可接受 stash/switch 中断（<30 分钟）、短期 spike/原型分支
  - ### 用 worktree 的场景：紧急 hotfix + 进行中的 feature、多 feature 并行、长时重构、分支间依赖版本不同、并发跑测试/构建、基于多个 base 测试
  - ### 适用场景速查表：hotfix、多 feature、PR review、跨分支对比、并行 CI、容器环境的取舍
  - ### 何时不需要 worktree：路径硬编码的容器/devcontainer 环境（`worktree.useRelativePaths` 需 Git ≥2.48 且 IDE 支持不成熟）；本地 clone 硬链接替代方案

## 第 4 章 AI 开发实战：用 worktree 编排并行 Agent
- 篇幅：长
- 素材引用：五、AI 开发工作流；六、综合分析
- 代码示例：有
- 小节：
  - ### 为什么 AI 开发优先 worktree：文件系统级隔离，避免 agent 因切分支丢失上下文；AI 生态已把 worktree 当事实默认（Copilot/Cursor 都基于它）
  - ### Claude Code 的 worktree 一等支持：`claude --worktree <name>`（别名 `-w`）、`worktree.baseRef`（fresh/head）、`.worktreeinclude` 复制 .env、子代理级 `isolation: worktree`、桌面版自动建 worktree
  - ### 多 agent 并行布局：一个 agent = 一个 worktree + 一个分支；sibling 目录命名；示例 `git worktree add -b feature-auth ../auth-work main`
  - ### 完成与清理：合并后立即 `git worktree remove` + `git worktree prune`；一次 `git fetch` 更新所有 worktree
  - ### AI 并行工作流的六个硬伤与补救：端口冲突（偏移公式）、依赖不迁移、IDE 支持割裂、数据库无隔离、磁盘翻倍、并行 agent 自我制造的 merge conflict

## 第 5 章 worktree 命令手册与常见坑
- 篇幅：长
- 素材引用：二、worktree 命令全集；四、常见坑与最佳实践
- 代码示例：有
- 小节：
  - ### worktree 命令全集：add / list / lock / unlock / move / remove / prune / repair 及关键参数（-b/-B、--detach、--orphan、--no-checkout、--force、--porcelain 等）
  - ### 命令形态记忆：按路径 basename 自动建分支、`-b <branch> <path> <base>` 基于 base 建分支、删除按目录路径而非分支名
  - ### 十个常见坑：同分支双检出、目标目录非空、remove 拒绝未提交改动、主树不可删/移、局部配置残留、push 目标缺失、依赖膨胀、.gitignore 陷阱、手动删目录必须 prune、submodule 多检出实验性
  - ### 最佳实践：目录命名（`主仓库名-分支名` / `wt/<issue-id>-<slug>`）、清理时机、配置 alias、Git 版本要求（2.5+，建议 2.15+）、网络/可移动磁盘用 lock

## 第 6 章 最终结论：AI 开发到底该用哪个
- 篇幅：短
- 素材引用：六、综合分析
- 代码示例：无
- 小节：
  - ### 默认规则与例外：单一短线性任务 → branch；2+ 并发任务 / 需并行跑测试构建 / 切分支会破坏状态 → worktree
  - ### AI 开发结论：多会话、多 agent 并行优先 worktree（Claude Code 标准动作是 `claude --worktree`）；worktree 不是银弹，环境隔离要自己补
  - ### 决策矩阵速查：未提交工作需切换 / 不同依赖版本 / CI 并行测试 / 快速 review / 磁盘进程受限 / 普通单 feature 六种情形的选择
  - ### 工程纪律清单：sibling 目录命名、合并后立即 remove、手删后 prune、`.claude/worktrees/` 加入 .gitignore

## 学习路径说明

### 前置要求
- 会用 add / commit / branch / checkout / switch，做过分支开发
- 了解 stash、merge/rebase 的基本概念
- Git 版本 2.5+（建议 2.15+，macOS 用 `brew update git`）

### 学完能做什么
- 遇到具体场景能快速判断该用 branch 还是 worktree，并说出判断依据
- 能独立创建、列出、锁定、移动、删除、清理多个 worktree（add/list/lock/move/remove/prune/repair）
- 能搭起 Claude Code / 多 agent 并行开发环境，规避端口冲突、依赖迁移、磁盘膨胀、merge conflict 等硬伤
- 能写出可复制的 AI 并行开发命令序列（建树 → 开发 → 合并 → 清理）

### 建议学习顺序
- 第 1-2 章：建立概念与逐项对比（约 30-40 分钟）
- 第 3 章：掌握决策框架与场景速查（约 20 分钟）
- 第 4 章：AI 实战，跟着命令在真实仓库敲一遍（约 40-60 分钟）
- 第 5 章：当作命令手册查阅，重点记 10 个坑（约 30 分钟）
- 第 6 章：结论与决策矩阵，贴到日常工作流中随时查
