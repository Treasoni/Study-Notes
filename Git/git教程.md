---
tags:
  - git
  - 版本控制
  - 教程
cssclass: git-tutorial
created: 2026-01-30
updated: 2026-02-05
---

# Git 完整教程

> Git 是一个「版本控制工具」，相当于给代码装了一个「无限撤销 + 时间机器 + 协作系统」

---

# 📑 目录

- [快速命令查阅](#快速命令查阅)
- [1. Git 基础概念](#1-git-基础概念)
- [2. Git 配置](#2-git-配置)
- [3. 创建仓库](#3-创建仓库)
- [4. Git 的区域与状态](#4-git-的区域与状态)
- [5. 基础操作](#5-基础操作)
- [6. 分支管理](#6-分支管理)
- [7. 远程仓库与协作](#7-远程仓库与协作)
- [8. 高级操作](#8-高级操作)
- [9. 常见问题](#9-常见问题)
- [10. 最佳实践](#10-最佳实践)

---

# 快速命令查阅

| 操作 | 命令 | 说明 |
|------|------|------|
| **初始化** | `git init` | 创建新仓库 |
| **克隆** | `git clone <url>` | 克隆远程仓库 |
| **状态** | `git status` | 查看当前状态 |
| **添加** | `git add .` | 添加所有修改 |
| **提交** | `git commit -m "msg"` | 提交更改 |
| **推送** | `git push` | 推送到远程 |
| **拉取** | `git pull --rebase` | 拉取并合并 |
| **日志** | `git log --oneline` | 查看提交历史 |
| **差异** | `git diff` | 查看未暂存差异 |
| **分支** | `git branch` | 查看分支 |
| **切换** | `git checkout -b <name>` | 创建并切换分支 |
| **合并** | `git merge <branch>` | 合并分支 |

---

# 1. Git 基础概念

## Git 是什么？

> [!info] 三大核心功能
> - **保存代码的历史版本**：可以回到任何一个过去的状态
> - **多人协作不冲突**：每个人都能同时改代码
> - **安全地实验新功能**：用分支，不怕改坏

## Git 的核心思想

### 本地优先

> [!summary] 与 SVN 最大的区别
> - 所有历史记录都在你电脑上
> - 不联网也能提交、回退、切换分支

### Git 管理的是「快照」，不是「差异」

每次 commit 会记录**整个项目当时的状态**，内部会智能复用没变的文件（不浪费空间）。

---

# 2. Git 配置

## 配置层级

| 级别 | 作用范围 | 文件位置 | 命令格式 |
|------|----------|----------|----------|
| **system** | 整台电脑 | `/etc/gitconfig` | `git config --system` |
| **global** | 当前用户 | `~/.gitconfig` | `git config --global` |
| **local** | 当前项目 | `.git/config` | `git config` |

## 常用配置命令

```bash
# 设置用户名和邮箱（必须）
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 查看所有配置
git config --list --show-origin

# 设置默认分支名为 main
git config --global init.defaultBranch main

# 开启颜色输出
git config --global color.ui true
```

> [!tip] 建议
> - 使用 `--global` 配置个人信息（90% 的配置都在这里）
> - 使用 `--local` 为特定项目设置不同身份（如公司项目）

---

# 3. 创建仓库

## 创建仓库的三种方式

### 方式一：从零开始

```bash
mkdir my-project && cd my-project
git init
touch README.md
git add README.md
git commit -m "initial commit"
```

### 方式二：克隆远程仓库

```bash
git clone https://github.com/user/repo.git
cd repo
```

### 方式三：已有代码转为 Git 仓库

```bash
cd existing-project
git init
git add .
git commit -m "initial commit"
```

## .git 目录结构

```
.git/
├── config      # 当前仓库配置
├── HEAD        # 当前分支指针
├── objects/    # Git 核心数据（存储所有对象）
└── refs/       # 分支、标签引用
```

---

# 4. Git 的区域与状态

## 四个区域

```mermaid
flowchart LR
    A[工作区<br>Working Directory] -->|git add| B[暂存区<br>Staging Area]
    B -->|git commit| C[本地仓库<br>Local Repository]
    C -->|git push| D[远程仓库<br>Remote Repository]
    D -->|git pull| A
```

| 区域 | 说明 | 对应命令 |
|------|------|----------|
| **工作区** | 你正在写代码的地方 | 直接编辑 |
| **暂存区** | 临时存放"下一次要提交的内容" | `git add` |
| **本地仓库** | 你电脑上的 Git 历史库 | `git commit` |
| **远程仓库** | GitHub/GitLab 上的仓库 | `git push` |

## 四种文件状态

| 状态 | 所在区域 | 说明 | 如何处理 |
|------|----------|------|----------|
| **Untracked** | 工作区 | 新文件，Git 不知道 | `git add` |
| **Modified** | 工作区 | 已跟踪文件被修改 | `git add` |
| **Staged** | 暂存区 | 已添加到暂存区 | `git commit` |
| **Committed** | 本地仓库 | 已提交到历史 | 可回退/推送 |

## 状态变化示例

```bash
# 完整生命周期
touch app.js          # → Untracked
git add app.js        # → Staged
git commit            # → Committed
vim app.js           # → Modified
git add app.js        # → Staged
git commit            # → Committed
```

---

# 5. 基础操作

## 添加文件

```bash
git add main.py              # 添加单个文件
git add a.txt b.txt         # 添加多个文件
git add .                   # 添加所有修改（最常用）
git add -u                  # 只添加已跟踪文件的修改
```

> [!warning] 重要细节
> `git add` 不会自动跟踪后续修改！如果你 add 后又改了文件，需要再次 add。

## 提交文件

```bash
git commit -m "添加用户登录功能"      # 最常用方式
git commit -am "修复登录 bug"            # 跳过 add，直接提交已跟踪文件
git commit --amend -m "修改提交说明"     # 修改最后一次提交
```

## 查看版本历史

```bash
git log                              # 完整日志
git log --oneline                     # 简洁显示（推荐）
git log -n 5                        # 只看最近 5 条
git log --graph --oneline --decorate  # 图形化显示分支
git log README.md                    # 查看某个文件的历史
```

## 查看差异

```bash
git diff                    # 工作区 vs 暂存区
git diff --staged          # 暂存区 vs HEAD（即将提交什么）
git diff HEAD              # 工作区 vs HEAD（所有改动）
git diff app.js            # 只看某个文件
git diff --name-only       # 只看改了哪些文件
```

## 删除文件

```bash
git rm file.txt           # 删除并暂存（推荐）
git rm --cached file.txt  # 从 Git 删除，但保留本地文件
```

> [!tip] 普通删除方式
> 如果用 `rm file.txt`，还需要运行 `git add file.txt` 来通知 Git。

## 回退版本

| 模式 | HEAD | 暂存区 | 工作区 | 使用场景 |
|------|------|--------|--------|----------|
| `--soft` | 回退 | 保留 | 保留 | 想重新组织提交 |
| `--mixed`（默认） | 回退 | 清空 | 保留 | 回退但保留代码 |
| `--hard` | 回退 | 清空 | 丢弃 | 确认不要所有改动 |

```bash
git reset --soft HEAD~1        # 回退 1 次，改动保留在暂存区
git reset --mixed HEAD~1       # 回退 1 次，改动保留在工作区（默认）
git reset --hard HEAD~1        # 回退 1 次，丢弃所有改动

git reset --hard b91e7a2      # 回退到指定提交
```

> [!warning] reset 后悔了？
> ```bash
> git reflog                    # 查看 HEAD 历史记录
> git reset --hard <commit-id>   # 恢复到之前的提交
> ```

---

# 6. 分支管理

## 分支基本操作

```bash
git branch                    # 查看本地分支（* 表示当前）
git branch -a                 # 查看所有分支（含远程）
git branch feature-login        # 创建分支
git checkout -b feature-login  # 创建并切换分支
git switch -c feature-login    # 新版本命令（同上）
git checkout main              # 切换到 main 分支
git branch -d feature-login    # 删除已合并的分支
git branch -D feature-login    # 强制删除分支
```

## 分支命名规范

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| 新功能 | `feature/功能名` | `feature/user-login` |
| 修复 bug | `bugfix/问题描述` | `bugfix/login-timeout` |
| 紧急修复 | `hotfix/问题描述` | `hotfix/security-fix` |
| 重构 | `refactor/模块名` | `refactor/api-module` |
| 文档 | `docs/内容` | `docs/readme-update` |

## 合并分支

```bash
# 1. 切换到目标分支
git checkout main

# 2. 合并其他分支
git merge feature-login

# 3. 解决冲突后
git add <conflict-file>
git commit

# 4. 删除已合并的分支
git branch -d feature-login
```

> [!tip] 推荐工作流
> ```bash
> # 先 rebase 保持历史线性
> git checkout feature-login
> git rebase main
> git checkout main
> git merge feature-login
> ```

---

# 7. 远程仓库与协作

## SSH 配置

### 检查现有 SSH Key

```bash
ls ~/.ssh
# 如果看到 id_ed25519 和 id_ed25519.pub，说明已有
```

### 生成新的 SSH Key

```bash
ssh-keygen -t ed25519 -C "your@email.com"
# 直接回车使用默认路径， passphrase 可以留空
```

### 添加公钥到 GitHub

```bash
cat ~/.ssh/id_ed25519.pub  # 复制输出内容
# GitHub → Settings → SSH and GPG keys → New SSH key
```

### 验证 SSH 连接

```bash
ssh -T git@github.com
# 成功会看到：Hi username! You've successfully authenticated...
```

## 远程仓库操作

```bash
git remote add origin git@github.com:user/repo.git  # 添加远程仓库
git remote -v                                        # 查看远程仓库
git remote show origin                                 # 查看远程仓库详情
git remote set-url origin <new-url>                   # 修改远程仓库地址
git remote remove origin                              # 删除远程仓库关联
```

## 推送与拉取

```bash
# 推送
git push                           # 推送当前分支
git push -u origin main             # 首次推送并建立跟踪关系
git push origin --delete branch-name  # 删除远程分支

# 拉取
git fetch                          # 只下载，不合并（安全）
git pull                           # Fetch + Merge
git pull --rebase                  # Fetch + Rebase（推荐）
```

> [!warning] git pull 失败？
> ```bash
> # 错误：Updates were rejected
> git pull --rebase  # 或 git pull
>
> # 错误：Permission denied (publickey)
> ssh -T git@github.com  # 检查 SSH 配置
> ```

---

# 8. 高级操作

## Rebase 变基

### Rebase vs Merge

| 场景 | 推荐使用 |
|------|----------|
| 个人整理提交记录 | `rebase` |
| 拉取远程代码 | `rebase` |
| 功能分支合并到 main | `merge` |
| 团队协作已 push 的提交 | `merge` |

### 常用 Rebase 操作

```bash
# 拉取时使用 rebase（保持历史线性）
git pull --rebase

# 分支合并前 rebase
git checkout feature-login
git rebase main

# 交互式 rebase（整理提交）
git rebase -i HEAD~3  # 打开编辑器，可以选择 pick/squash/drop
```

> [!danger] Rebase 禁忌
> **绝对不要 rebase 已经 push 的公共提交！**
> - rebase 会改写历史
> - 别人基于旧历史的工作会出问题
> - 只在"本地、个人、未 push"的提交上使用

## Revert 反转提交

```bash
git revert <commit-id>  # 创建新提交来抵消旧提交
```

> [!info] 什么时候用 revert？
> 当提交已经 push 到远程，不想改写历史时使用 revert。

## .gitignore 忽略文件

### 常用规则

```
# 注释
*.log                  # 忽略所有 .log 文件
node_modules/          # 忽略目录
config.json            # 忽略具体文件
temp-*.txt            # 忽略匹配的文件
**/*.log              # 忽略多级目录中的文件

# 反向规则（不忽略）
!important.log
```

### 常见问题

```bash
# 文件已被跟踪，想忽略
git rm --cached file.txt
git commit -m "stop tracking file.txt"
```

## Stash 暂存

```bash
git stash                      # 暂存当前修改
git stash save "message"        # 带消息的暂存
git stash list                  # 查看暂存列表
git stash pop                  # 恢复并删除
git stash apply                # 恢复但不删除
git stash drop                 # 删除暂存
```

---

# 9. 常见问题

## 合并冲突

### 冲突标记

```text
<<<<<<< HEAD
main 分支的内容
=======
feature-login 分支的内容
>>>>>>> feature-login
```

### 解决步骤

```bash
# 1. 查看冲突文件
git status

# 2. 手动编辑冲突文件，删除标记

# 3. 标记为已解决
git add <conflict-file>

# 4. 完成合并
git commit

# 或者放弃合并
git merge --abort
```

> [!tip] 更多问题解决方案
> 遇到其他 Git 错误？查看 [[Git 常见错误解决方案]] 按错误信息快速定位解决方案。

## 其他常见错误

| 错误信息 | 原因 | 解决方法 |
|----------|------|----------|
| `fatal: not a git repository` | 当前目录不是 Git 仓库 | `cd` 到项目目录或 `git init` |
| `Updates were rejected` | 远程有新提交，本地落后 | `git pull --rebase` |
| `Permission denied (publickey)` | SSH 配置有问题 | 检查 `ssh -T git@github.com` |
| `fatal: refusing to merge unrelated histories` | 两个仓库没有共同祖先 | `git pull --allow-unrelated-histories` |

> [!info] 完整错误解决方案
> 查看 [[Git 常见错误解决方案]] 获取完整的错误排查指南。

---

# 10. 最佳实践

## 提交信息规范

### 格式：类型(范围): 描述

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档更改 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具相关 |

### 示例

```bash
git commit -m "feat(login): 添加用户登录功能"
git commit -m "fix(api): 修复接口超时问题"
git commit -m "docs(readme): 更新安装说明"
git commit -m "refactor(auth): 简化认证逻辑"
```

## 每日工作流

```bash
# 1. 开始新任务
git checkout main
git pull
git checkout -b feature/new-task

# 2. 开发、提交
git add .
git commit -m "feat: 添加新功能"

# 3. 同步最新代码
git fetch
git rebase origin/main

# 4. 推送分支
git push -u origin feature/new-task

# 5. 合并到 main（PR/MR 审核通过后）
git checkout main
git pull
git branch -d feature/new-task
```

## 学习建议

> [!summary] 推荐学习路径
> 1. 掌握基本操作：init, add, commit, push, pull
> 2. 理解 4 个区域和 4 种状态
> 3. 学会分支操作
> 4. 学会解决冲突
> 5. 进阶学习 rebase、reset 高级用法

## 专题笔记

> [!tip] 深入学习
> - [[Git/Git MOC]] - Git 知识体系索引
> - [[分支管理最佳实践]] - 团队协作中的分支策略和工作流程
> - [[Git 常见错误解决方案]] - 按错误信息快速定位解决方案

## 推荐阅读

- [Git 官方文档](https://git-scm.com/doc)
- [Pro Git 中文版](https://git-scm.com/book/zh/v2)
- [GitHub 官方教程](https://docs.github.com/zh/get-started/getting-started-with-git)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

## 相关文档
- [[AI学习/02-工具使用/如何使用Claude code]] - Git 安装与环境变量配置

---

**最后更新**：2026-02-25
