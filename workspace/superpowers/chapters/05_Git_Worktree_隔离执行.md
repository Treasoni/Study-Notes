# 第五章：Git Worktree 隔离执行

## 本章目的

Pipeline 的第 2 阶段是在写任何代码前创建隔离工作区。本章深入 Git Worktree 的 4 步流程：环境检测 → 工作区创建 → 依赖安装 → 基线验证，以及已知问题和规避方案。

---

## 5.1 为什么需要隔离

AI Agent 在同一个仓库中工作时会相互干扰：

| 问题 | 说明 |
|------|------|
| 分支冲突 | Subagent 1 切分支，Subagent 2 的 HEAD 也变了 |
| 脏状态 | 一个 agent 的未提交修改影响另一个的测试 |
| 无法回滚 | 实现出问题时，"撤销"变得复杂 |
| 测试干扰 | 一个 agent 的修改导致另一个的测试失败 |

Git Worktree 解决这些问题：每个 agent 有独立的 HEAD、Index 和分支状态，但共享同一个 `.git` 对象存储。

---

## 5.2 4 步工作流

### Step 0：环境检测

在创建任何东西之前，先检测当前是否已在隔离环境中：

```bash
# 检查是否在 worktree 中
GIT_DIR=$(git rev-parse --git-dir)
GIT_COMMON=$(git rev-parse --git-common-dir)
if [ "$GIT_DIR" != "$GIT_COMMON" ]; then
  # 已经在 worktree 中
fi

# 检查是否在 submodule 中
git rev-parse --show-superproject-working-tree

# 普通 checkout
```

三种情况：

| 当前状态 | 操作 |
|---------|------|
| 已在 Worktree | 跳过创建，直接用 |
| 在 Submodule | 视为普通仓库，不走 worktree |
| 普通 checkout | 请求用户同意后创建 |

### Step 1a：使用原生工具（优先）

如果平台提供原生 Worktree 工具（如 `EnterWorktree`、`WorktreeCreate`、`--worktree` 标志），**优先使用**。手动 `git worktree add` 会创建平台无法管理的"幽灵状态"。

### Step 1b：Git Worktree 回退

当没有原生工具时：

```bash
# 1. 检查目录是否被 gitignore
git check-ignore -q .worktrees
# 如果未被忽略，先添加到 .gitignore 并 commit

# 2. 目录优先级：
#    用户显式指定 > .worktrees/（隐藏，优先） > worktrees/

# 3. 创建 worktree
git worktree add "<path>" -b "<feature-branch>"
cd "<path>"
```

### Step 2：项目设置

自动检测项目类型并安装依赖：

| 检测文件 | 命令 |
|---------|------|
| package.json | npm install / yarn |
| Cargo.toml | cargo fetch |
| requirements.txt / pyproject.toml | pip install / poetry install |
| go.mod | go mod download |

### Step 3：基线验证

运行项目对应的测试命令，确认测试基线是干净的：

```bash
# 根据项目类型选择
npm test / cargo test / pytest / go test ./...

# 如果测试失败 → 报告用户，询问是否继续
# 不能静默地继续
```

### 输出报告

```
Worktree ready at /path/to/.worktrees/feature-x
Tests passing (142 tests, 0 failures)
Ready to implement feature-x
```

---

## 5.3 已知问题与规避

### 问题 1：Worktree 静默回退到父仓库

Claude Code 的 `isolation: "worktree"` 有时会**静默地**在父仓库中工作，而不是创建新的 worktree。Agent 以为自己隔离了，实际上没有。

**规避**：使用 clone 隔离代替 worktree 隔离：
```bash
git clone --dissociate --reference . --single-branch . "../isolated-$BRANCH"
```

### 问题 2：Subagent 分支切换改变父仓库 HEAD

在 worktree 中运行的 subagent 执行分支切换时，可能意外修改父仓库的 HEAD 指针。

**规避**：每个 subagent 创建独立的 worktree，严格隔离。不要共享 worktree。

### 问题 3：Worktree 文件被误提交

如果 `.worktrees/` 目录未被 `.gitignore` 包含，worktree 中的文件可能被意外提交到仓库。

**规避**：创建 worktree 前必须验证：
```bash
git check-ignore -q .worktrees || (echo ".worktrees" >> .gitignore && git add .gitignore && git commit -m "chore: ignore worktrees")
```

### 问题 4：macOS 环境差异

BSD 工具链与 GNU 工具链的差异（如 `date` 命令不支持纳秒），导致测试失败。

**规避**：在设计的早期阶段就识别环境差异，准备 Docker 或 CI 环境用于验证。

---

## 5.4 清理与溯源

### 溯源所有权规则

```
.worktrees/ 或 worktrees/ 下 → Agent 拥有，可以删除
其他位置的 worktree → 宿主环境拥有，不能删除
```

### 清理顺序

```
1. Merge 到目标分支
2. 运行测试确认通过
3. 删除 worktree（cd 回主仓库根目录）
4. git worktree prune
5. 删除分支
```

顺序很重要——如果先删分支再删 worktree，会导致 Git 报错。

---

## 本章小结

- Git Worktree 为每个 Subagent 提供独立的 HEAD、Index 和分支状态
- 原生工具优先，`git worktree add` 是备用方案
- 创建前验证 gitignore 状态，避免污染仓库
- 测试基线验证是门槛——基线不过不能开始实现
- 已知问题：静默回退、分支突变、macOS 差异——有对应的规避方案
- 清理顺序必须正确：merge → 测试 → 删 worktree → 删分支

### 下一章预告

隔离环境准备好后，框架如何在不同平台上工作？下一章看 **Plugin 架构与自举机制**——一个 skills 库如何部署到 10+ 个 AI 平台。
