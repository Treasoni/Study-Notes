# git branch 与 worktree — 探测式收集结果

- 主题: git branch vs worktree 区别与使用场景，AI 开发该用哪个
- 阶段: 阶段 1（探测式收集）
- 探测时间: 2026-08-05
- 探测方式: 3 个并行 subagent（机制对比 / 使用场景 / AI 开发实战）

## 探测汇总

### 1. 核心区别（机制维度）

- **branch 是「引用指针」维度**：只是一个指向某次提交的指针，记录版本分叉，不产生工作目录。
- **worktree 是「工作目录」维度**：Git 2.5+ 让同一仓库拥有多个工作目录，各自检出不同分支，共享 objects/refs/config。
- 未提交改动「悬浮」在当前检出分支上；默认单工作树同一时刻只能检出一个分支。
- 每个 linked worktree 在 `$GIT_DIR/worktrees/<name>` 有私有目录，HEAD/index 按工作树隔离；同一分支只能在一个 worktree 检出（除非 `--force`）。
- 一句话：**Branches solve version divergence. Worktrees solve time parallelism.**

### 2. 使用场景（取舍维度）

| 场景 | 选择 |
|------|------|
| 单任务、线性短流程 | branch + 单工作目录（stash/switch 成本低） |
| 2+ 并发任务、并行跑测试/构建 | worktree |
| hotfix 不打断当前开发 | worktree（`git worktree add ../hotfix -b hotfix main`） |
| PR review 需本地运行 | worktree |
| 高风险重构 / 长期 feature 隔离 | worktree |
| 容器/devcontainer 环境 | worktree 有路径硬编码问题（Git≥2.48 才支持 useRelativePaths），可用本地 clone 替代 |

**worktree 的坑**：依赖各装一份（磁盘膨胀）、同一分支不可双检出、未跟踪文件/node_modules/.env 不共享、手删目录后需 `git worktree prune`、局部配置残留。

### 3. AI 开发实战（决策维度）

- **Claude Code** 官方一等支持 worktree：`claude --worktree <name>` 在 `.claude/worktrees/` 建隔离目录+独立分支，多会话并行；子代理可用 `isolation: worktree`。
- **Copilot**（GitHub Blog）近年因 AI 并行开发而流行 worktree。
- **决策框架**：单一短线性任务用 branch；**出现第二个活跃任务 / 需要并行跑测试构建 / 切分支会破坏状态时，升级到 worktree**。
- **工具趋势**：一任务一 worktree 正被工具链标准化（dmux、agent-worktree、clawt 等）。
- **成本**：worktree 创建近乎即时（共享对象库，无需 re-clone）；但磁盘翻倍、端口冲突、IDE 支持不一致。

## 关键信源

| 来源 | 类型 | 相关性 |
|------|------|--------|
| git-scm.com/docs/git-worktree | 官方文档 | 5 |
| github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them | 技术博客(官方) | 5 |
| code.claude.com/docs/en/worktrees | 官方文档(AI 工具) | 5 |
| manpages.debian.org/testing/git-man/git-worktree.1.en.html | 官方文档 | 5 |
| stackoverflow.com/questions/31935776 | 社区讨论 | 4 |
| cloud.tencent.com.cn/developer/article/2653851 | 技术博客 | 4 |
| avdi.codes/you-probably-dont-need-git-worktrees | 技术博客(反方观点) | 4 |
| developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents | 技术博客 | 4 |
| grizzlypeaksoftware.com/library/git-worktrees-for-parallel-development | 技术博客 | 4 |

## 待用户选择：学习方向

A. **完整实战**：概念对比 → 决策框架 → AI 开发工作流（推荐）
B. **机制优先**：深挖 branch/worktree 底层原理
C. **命令优先**：以 git worktree 命令集为主线 + 坑与清理
D. **AI 工作流专篇**：只聚焦 AI 编程工具的 worktree/分支用法
