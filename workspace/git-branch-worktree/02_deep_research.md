# git branch 与 worktree — 深度收集素材

- 主题: git branch vs worktree 区别与使用场景，AI 开发该用哪个
- 收集时间: 2026-08-05
- 方向: 完整实战（概念对比 → 决策框架 → AI 开发工作流）
- 收集方式: 3 个并行精读 subagent + 前期探测结果

## 一、核心机制对比（branch vs worktree）

### branch 是什么
- 分支只是**指向某次提交的指针**，记录版本分叉（version divergence），本身**不产生工作目录**。
- 未提交改动「悬浮」在当前检出分支上；默认仓库只有一个工作树，同一时刻只能检出一个分支。
- 同一工作目录在不同分支间切换（`checkout`/`switch`），切换前要么 stash 要么 commit。

### worktree 是什么
- Git 2.5+ 让**同一仓库拥有多个工作目录**，各自检出不同分支，实现「时间并行」（time parallelism）。
- 每个 linked worktree 在 `$GIT_DIR/worktrees/<name>` 有私有目录；顶层的 `.git` 文件记录 `$GIT_DIR`（指向私有目录）和 `$GIT_COMMON_DIR`（指向主 `.git`）。
- **共享内容**：所有 `refs/`、对象库、packed refs、默认 config。
- **私有内容**：`HEAD`、`index`，以及 `refs/bisect`、`refs/worktree`、`refs/rewritten`。
- 一句话：**Branches solve version divergence. Worktrees solve time parallelism.**
- 本质：worktree = 同一仓库的多套「HEAD + index」私有上下文，引用/对象库/config 全局共享，因此比 `git clone` 轻量得多，分支间历史天然互通。

## 二、worktree 命令全集

| 命令 | 用途 | 关键参数 |
|------|------|---------|
| `git worktree add <path> [commit-ish]` | 新建并检出 | `-b/-B <branch>` 新建分支（`-B` 已存在则重置）、`-d/--detach` 分离 HEAD、`--orphan` 空树、`--no-checkout` 配合 sparse-checkout、`-f/--force`、`--lock` 创建即锁、`--track`、`--guess-remote` |
| `git worktree list` | 列出所有 worktree | `-v` 显示原因、`--porcelain` 脚本解析、`--expire` 标过期 |
| `git worktree lock/unlock` | 防止被 prune/move/remove | `--reason` 记录原因 |
| `git worktree move` | 移动 worktree | 主树和含 submodule 的树不可移；锁定树需两次 `--force` |
| `git worktree remove [-f]` | 删除（按**目录路径**，不是分支名） | 默认仅干净工作树；`-f` 强制丢弃未提交改动；主树不可删 |
| `git worktree prune [-n] [-v]` | 清理手动删除后残留的管理记录 | `-n` dry-run |
| `git worktree repair` | 修复因移动而失联的管理文件 | 主树移动在根跑，linked 树在其内部跑 |

**命令形态记忆**：
- `git worktree add ../hotfix` → 按路径 basename 自动建分支
- `git worktree add -b new-branch path/to/folder/` → 显式新建分支
- `git worktree add -b new-branch path/to/folder/ <base>` → 基于某分支/tag/commit 建分支
- 删除按**目录路径**而非分支名

## 三、使用场景与决策框架

### 决策主线
1. **「若切换会摧毁状态，就用 worktree」**：状态 = 不想 stash 的未提交改动、昂贵不想重新生成的构建产物、`.env`/依赖版本等环境配置、绑定在目录上的常驻进程。
2. **「单任务、切换不频繁 → branch；2+ 个并发活跃任务 → 每任务一个 worktree」**。
3. **stash/switch 可接受**（<30 分钟中断、简单顺序队列、短期 spike/原型分支）→ 用 branch。
4. **worktree 强制/强烈推荐**：长时重构（stash pop 冲突高频）、分支间依赖版本不同、需要并发跑构建/测试/进程、同一功能要基于多个 base（main/release）测试、数小时以上的中断。

### 适用场景速查
| 场景 | 选择 |
|------|------|
| 紧急 hotfix + 进行中的 feature | worktree |
| 多 feature 分支并行开发 | worktree |
| PR review 需本地运行 | worktree（或快速 stash/switch） |
| 跨分支代码对比与调试 | worktree |
| 长时重构 / 高风险改动隔离 | worktree |
| 并行跑测试/构建/CI | worktree |
| 单一分支线性开发 | branch 即可 |
| 项目体积极小（clone 成本可忽略） | branch / 直接 clone |
| 容器/devcontainer 环境 | 注意 worktree 路径硬编码问题 |

## 四、常见坑与最佳实践

### 坑
1. **同分支双检出**：`fatal: 'branch-name' is already checked out at 'path'` → 删旧 worktree 或用 `--detach` 临时调试。
2. **目标目录必须为空**，否则报错；一个目录只能有一个工作树。
3. **`remove` 默认拒绝未提交改动**（`working tree not clean`），需 commit/stash 或谨慎 `--force`。
4. **主工作树不可 remove/move**。
5. **局部配置残留**：worktree 内 `git config user.name` 实际写入主仓库 `.git/config`，删除后不自动清理。
6. **push 目标缺失**：主仓库无 remote 时 worktree push 报 `No configured push destination`，需先 `git remote add origin`。
7. **依赖膨胀**：每个 worktree 各装一份依赖，多次 `npm/pip install` 吃满磁盘。
8. **`.gitignore` 陷阱**：worktree 建在主仓库目录内必须加入 `.gitignore`；建议放主仓库外（sibling 目录）。
9. **手动删目录必须 `prune`，手动移动目录必须 `repair`**，两者不可混用。
10. **submodule 多检出仍属实验性**：含 submodule 的 worktree move 被禁、remove 需 `--force`。

### 最佳实践
- **目录命名**：`主仓库名-分支名`（如 `../my-project-feat-login`），或 `wt/<issue-id>-<slug>`；避免 `../test` 模糊命名。
- **清理时机**：分支 commit+push 后立即 `git worktree remove`；手删目录后补 `git worktree prune`。
- **配置别名**：`git config --global alias.wt-list "worktree list"` 及 wt-add/wt-remove/wt-prune。
- **Git 版本**：worktree 需 2.5+，建议 2.15+（macOS `brew update git`）。
- **锁定**：网络/可移动磁盘上用 `git worktree lock` 防意外 prune。

### 反方观点（何时不需要 worktree）
- **路径硬编码**：worktree 路径写进配置文件，容器/devcontainer 环境基本不可用；`worktree.useRelativePaths` 需 Git ≥2.48（2025）且 IDE 支持不成熟。
- **替代方案：本地 clone 硬链接**：`git clone my-project my-project.my-branch-a` —— 近瞬时、几乎不额外占磁盘（对象文件硬链接共享历史），把新 clone 的 origin 指回真正上游即可。
- 结论：环境经常迁移/容器化 → 优先本地 clone；常规本地开发 → worktree。

## 五、AI 开发工作流（本笔记重点）

### Claude Code 的 worktree 一等支持
- `claude --worktree <name>`（别名 `-w`）在 `.claude/worktrees/<name>/` 建独立工作目录 + 自动切到 `worktree-<name>` 分支；不写名字随机生成；重跑同名=重开已有 worktree。
- `-p` 非交互模式不做清理，需手动 `git worktree remove`。
- `worktree.baseRef`：`"fresh"`（默认，从远端默认分支拉干净树）或 `"head"`（从当前本地 HEAD 分支，携带未提交工作）。
- `.worktreeinclude`（.gitignore 语法）把 `.env` 等被忽略文件自动复制进新 worktree。
- 子代理级并行：agent frontmatter 加 `isolation: worktree`，每次运行在自己的临时 worktree；运行期被 lock，结束有改动则按 `cleanupPeriodDays` 清理；不会删用户显式建的 worktree。
- 桌面版（desktop app）每个新会话自动获得一个 worktree。

### Copilot / 生态
- GitHub Copilot App 每个新会话默认「New worktree」，worktree 已是 AI 并行开发的事实默认（VS Code 支持）。
- Cursor Parallel Agents 直接构建在 worktree 上；incident.io 日常跑 4-5 个并行 Claude agent。

### 多 agent 并行布局
- 模式：**一个 agent = 一个 worktree + 一个分支**，sibling 目录命名。
- 示例：`git worktree add -b feature-auth ../auth-work main`。
- 优点：上下文隔离（agent 只见自己目录）、保留会话历史、安全实验（可试可删）、一次 `git fetch` 更新所有 worktree、省磁盘（共享对象库）。
- 完成：`git worktree remove ../auth-work` + `git worktree prune`。

### AI 并行工作流的硬伤（要自己补环境隔离）
1. **端口冲突**：dev server 默认抢 3000/5432/8080 → 端口偏移公式 `SERVICE_PORT = BASE_PORT + (WORKTREE_INDEX * 10) + SERVICE_OFFSET`。
2. **依赖不迁移**：新 worktree 没有 node_modules/.env，每树重装；`pnpm`（符号链接）可缓解。
3. **IDE 支持割裂**：JetBrains 无原生 UI；VS Code 2025 才支持；Claude Code `/ide` 认不出 worktree 路径。
4. **无数据库隔离**：worktree 共享本地库/Docker daemon/缓存 → 逐 worktree 建库实例 + worktree 索引化 volume 名。
5. **磁盘翻倍**：2GB 代码库 20 分钟会话可能消耗近 10GB；monorepo 构建缓存逐树放大；被遗忘的 worktree 吃 GB 级空间。
6. **自我制造的 merge conflict**：并行 agent 碰同一批文件几乎必然冲突且无预警 → 靠任务划分和 orchestrator 协调，合并后立即删 worktree。

## 六、综合分析（用于「该用哪个」结论）

1. **默认规则**：单一短线性任务 → branch；**2+ 并发任务 / 需并行跑测试构建 / 切分支会破坏状态 → worktree**。
2. **AI 开发**：多会话、多 agent 并行时优先 worktree（文件系统级隔离，避免 agent 因切分支丢失上下文）。Claude Code 标准动作是 `claude --worktree`。
3. **worktree 不是银弹**：环境隔离（端口/依赖/数据库）要自己补；容器环境可退回本地 clone 硬链接方案。
4. **工程纪律**：sibling 目录命名、合并后立即 remove、手删后 prune、`.claude/worktrees/` 加 .gitignore。
5. **决策矩阵速查**：
   - 未提交工作 + 需切换 → worktree
   - 不同依赖版本 → worktree
   - CI 并行测试 / 多 base 测试 → worktree
   - 快速 review（<30min）→ branch + stash
   - 磁盘/进程受限 → 别开太多 worktree
   - 普通单 feature 开发 → 一个 branch 即可，别过度工程

## 关键信源清单

| 来源 | 类型 | 相关性 |
|------|------|--------|
| https://git-scm.com/docs/git-worktree | 官方文档 | 5 |
| https://github.blog/ai-and-ml/github-copilot/what-are-git-worktrees-and-why-should-i-use-them | 技术博客(官方) | 5 |
| https://code.claude.com/docs/en/worktrees | 官方文档(AI 工具) | 5 |
| https://manpages.debian.org/testing/git-man/git-worktree.1.en.html | 官方文档 | 5 |
| https://moltq.chat/questions/.../when-should-coding-agents-use-git-worktrees-vs-branching-for-parallel-feature-de | 社区讨论 | 5 |
| https://developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents | 技术博客 | 4 |
| https://www.gitkraken.com/learn/git/git-worktree | 技术博客 | 4 |
| https://cloud.tencent.com.cn/developer/article/2653851 | 技术博客 | 4 |
| https://avdi.codes/you-probably-dont-need-git-worktrees | 技术博客(反方) | 4 |
| https://stackoverflow.com/questions/31935776 | 社区讨论 | 4 |
