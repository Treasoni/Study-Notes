---
tags:
  - git
  - 版本控制
  - 高级
  - 技巧
cssclass: git-advanced
created: 2026-03-02
updated: 2026-04-05
---

# Git 高级技巧

> ⚡ 掌握这些技巧，让你的 Git 使用更加高效
>
> 📋 **前置要求**：学习本章前，请先掌握 [[Git 入门教程]] 的基础内容

---

## 📑 目录

| 技巧 | 用途 | 难度 |
|------|------|------|
| [[#1-rebase-变基]] | 整理提交历史、保持线性 | ⭐⭐ |
| [[#2-revert-反转提交]] | 安全撤销已推送的提交 | ⭐⭐ |
| [[#3-stash-暂存]] | 临时保存工作进度 | ⭐⭐ |
| [[#4-gitignore-忽略文件]] | 排除不需要跟踪的文件 | ⭐ |
| [[#5-交互式添加]] | 部分提交文件内容 | ⭐⭐ |
| [[#6-搜��代码]] | 在历史中查找代码 | ⭐⭐ |
| [[#7-cherry-pick-精选提交]] | 选择性应用提交 | ⭐⭐⭐ |
| [[#8-bisect-二分查找]] | 定位引入 bug 的提交 | ⭐⭐⭐ |
| [[#9-reflog-恢复]] | 恢复误操作 | ⭐⭐ |
| [[#10-子模块]] | 管理项目依赖 | ⭐⭐⭐ |

---

# 1. Rebase 变基

> 🎯 **一句话定义**：Rebase = 重新整理提交历史，让分支看起来像是"基于最新代码开发��"
>
> 📦 **通俗比喻**：就像重新整理一摞纸牌，把你的提交"移动"到最新的基础之上

## Rebase vs Merge 对比

| 场景 | 推荐 | 原因 |
|------|------|------|
| 个人整理提交记录 | `rebase` | 保持历史线性整洁 |
| 拉取远程代码 | `rebase` | 避免无意义的合并提交 |
| 功能分支合并到 main | `merge` | 保留完整历史 |
| 团队协作已 push 的提交 | `merge` | 不改写公共历史 |

## ⚡ 常用操作

### 拉取时使用 rebase

```bash
git pull --rebase
# 等价于：
git fetch
git rebase origin/main
```

### 分支合并前 rebase

```bash
git checkout feature-login
git rebase main
# 现在 feature-login 包含了 main 的最新更改
git checkout main
git merge feature-login
```

### 交互式 rebase（整理提交）

```bash
git rebase -i HEAD~3  # 最近 3 次提交
```

打开编辑器后，可以看到类似：

```
pick abc1234 第一个提交
pick def5678 第二个提交
pick ghi9012 第三个提交
```

**操作命令**：

| 命令 | 作用 |
|------|------|
| `pick` | 保留该提交 |
| `squash` / `s` | 合并到前一个提交 |
| `drop` / `d` | 删除该提交 |
| `reword` / `r` | 修改提交信息 |
| `edit` | 停下来修改该提交 |

**示例：合并多个提交**

```
pick abc1234 第一个提交
squash def5678 第二个提交
squash ghi9012 第三个提交
```

保存后，会打开编辑器让你输入合并后的提交信息。

## ⚠️ Rebase 的危险

> [!danger] Rebase 禁忌
> **绝对不要 rebase 已经 push 的公共提交！**

### 为什么危险？

1. **改写历史**：rebase 会创建新的提交，旧的提交被丢弃
2. **影响他人**：别人基于旧历史的工作会出问题
3. **难以恢复**：一旦其他人基于新历史工作，很难恢复

### ✅ 安全使用原则

```bash
# ✅ 安全：本地、个人、未 push 的提交
git rebase -i HEAD~3

# ❌ 危险：已经 push 的提交
git push
git rebase -i HEAD~3  # 不要这样做！
```

---

# 2. Revert 反转提交

> 🎯 **一句话定义**：创建一个新提交来"撤销"某个旧提交的效果
>
> 📦 **通俗比喻**：就像撤销操作，但是会留下"撤销记录"

## 何时使用 Revert

| 情况 | 使用命令 | 原因 |
|------|----------|------|
| 已 push 到远程 | `revert` | 不改写历史 |
| 本地未 push | `reset` | 直接回退更简单 |

## ⚡ 常用操作

```bash
# 反转某个提交（创建新提交来抵消旧提交）
git revert abc1234

# 反转最近一次提交
git revert HEAD

# 反转多个提交
git revert def5678..abc1234  # 注意范围是反的

# 自动解决冲突（放弃冲突内容）
git revert --no-commit abc1234
git commit -m "Revert abc1234"
```

## Revert vs Reset 对比

| 特性 | Revert | Reset |
|------|--------|-------|
| 创建新提交 | ✅ 是 | ❌ 否 |
| 改写历史 | ❌ 否 | ✅ 是 |
| 可用于公共提交 | ✅ 是 | ❌ 否 |
| 撤销多个提交 | 需多次执行 | 一次完成 |

---

# 3. Stash 暂存

> 🎯 **一句话定义**：临时保存当前工作进度，让你可以切换分支做其他事
>
> 📦 **通俗比喻**：就像把当前工作"放进抽屉"，等会儿再拿出来继续

## ⚡ 基本用法

```bash
git stash                      # 暂存当前修改
git stash save "message"       # 带消息的暂存
git stash list                 # 查看暂存列表
git stash show                 # 查看暂存内容
git stash pop                  # 恢复并删除
git stash apply                # 恢复但不删除
git stash drop                 # 删除指定暂存
git stash clear                # 清空所有暂存
```

## 🔧 高级用法

```bash
# 暂存包括未跟踪的文件
git stash -u

# 暂存所有文件（包括忽略的文件）
git stash -a

# 恢复指定暂存
git stash apply stash@{2}

# 从暂存创建分支
git stash branch feature-branch stash@{1}
```

## 📋 使用场景

### 场景 1：紧急修复

```bash
# 正在开发新功能，需要紧急修复 bug
git stash                    # 保存当前工作
git checkout main
git checkout -b hotfix/critical-bug
# ... 修复 ...
git checkout main
git merge hotfix/critical-bug
git checkout feature-new
git stash pop                 # 恢复新功能开发
```

### 场景 2：切换分支但不想提交

```bash
git stash
git checkout other-branch
# ... 做其他事 ...
git checkout feature-branch
git stash pop
```

---

# 4. .gitignore 忽略文件

> 🎯 **一句话定义**：告诉 Git 哪些文件不需要跟踪
>
> 📦 **通俗比喻**：就像给 Git 一个"黑名单"，名单里的文件不会被管理

## ⚡ 常用规则

```gitignore
# 注释

*.log                  # 忽略所有 .log 文件
node_modules/          # 忽略目录
config.json            # 忽略具体文件
temp-*.txt            # 忽略匹配的文件
**/*.log              # 忽略多级目录中的文件

# 反向规则（不忽略）
!important.log

# 目录下的所有文件，但不忽略目录本身
dir/*

# 忽略所有 .txt 文件，但保留 important.txt
*.txt
!important.txt
```

## 📦 常见模板

### Node.js 项目

```gitignore
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.env
.env.local
dist/
build/
```

### Python 项目

```gitignore
__pycache__/
*.py[cod]
*$py.class
.env
venv/
env/
.venv/
*.egg-info/
dist/
build/
```

### 通用项目

```gitignore
# 操作系统
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# 日志
*.log
logs/

# 临时文件
*.tmp
*.bak
*.cache
```

## ❓ 常见问题

### 文件已被跟踪，想忽略

```bash
# 从跟踪中删除，但保留本地文件
git rm --cached file.txt
git commit -m "stop tracking file.txt"

# 确保在 .gitignore 中添加规则
echo "file.txt" >> .gitignore
```

### 清理缓存

```bash
# 清除所有缓存
git rm -r --cached .

# 重新添加
git add .
git commit -m "update .gitignore"
```

---

# 5. 交互式添加

> 🎯 **一句话定义**：选择性地添加文件的部分修改，而非全部

## ⚡ 基本用法

```bash
# 交互式添加（逐块选择）
git add -p

# 交互式添加（逐文件选择）
git add -i
```

### `git add -p` 常用命令

| 命令 | 作用 |
|------|------|
| `y` | 添加这块 |
| `n` | 不添加这块 |
| `s` | 分割成更小的块 |
| `e` | 手动编辑这块 |

## 📋 使用场景

```bash
# 修改了一个文件，但只想提交部分修改
git add -p file.js
# 会显示每个修改块，让你选择是否添加
```

---

# 6. 搜索代码

> 🎯 **一句话定义**：在 Git 历史中查找代码变更

## 🔍 搜索提交内容

```bash
# 搜索包含某字符串的提交
git log -S "functionName"

# 搜索包含某字符串的提交（显示差异）
git log -p -S "functionName"

# 搜索包含某字符串的提交（只显示匹配行）
git log -G "functionName"
```

## 📄 搜索文件

```bash
# 按文件名搜索
git log --follow -- filename

# 按内容搜索
git grep "searchTerm"
git grep -e "pattern1" --and -e "pattern2"
```

---

# 7. Cherry-pick 精选提交

> 🎯 **一句话定义**：从其他分支"摘取"特定的提交应用到当前分支
>
> 📦 **通俗比喻**：就像从一棵树上摘下特定的果实，而不是整棵树

## ⚡ 基本用法

```bash
# 将某个提交应用到当前分支
git cherry-pick abc1234

# 应用多个提交
git cherry-pick def5678..abc1234

# 应用但不自动提交
git cherry-pick -n abc1234

# 应用并继续（解决冲突后）
git cherry-pick --continue

# 跳过当前提交
git cherry-pick --skip

# 取消 cherry-pick
git cherry-pick --abort
```

## 📋 使用场景

```bash
# 在 bugfix 分支修复了问题，想单独应用到 main
git checkout main
git cherry-pick abc1234  # bugfix 分支的提交 ID
```

---

# 8. Bisect 二分查找

> 🎯 **一句话定义**：用二分法快速定位引入 bug 的提交
>
> 📦 **通俗比喻**：就像猜数字游戏，每次排除一半的可能性

## ⚡ 使用方法

```bash
# 开始二分查找
git bisect start

# 标记当前为坏的版本
git bisect bad

# 标记已知好的版本
git bisect good abc1234

# Git 会自动切换到中间的提交，测试后标记
git bisect good  # 或 git bisect bad

# 重复直到找到问���提交
git bisect reset  # 结束查找
```

---

# 9. Reflog 恢复

> 🎯 **一句话定义**：记录 HEAD 的所有移动，用于恢复误操作
>
> 📦 **通俗比喻**：就像浏览器的"历史记录"，可以回到任意之前的状态

## ⚡ 基本用法

```bash
# 查看 reflog
git reflog

# 恢复到某个状态
git reset --hard HEAD@{2}

# 查看特定分支的 reflog
git reflog show main
```

> [!tip] Reflog 保留期限
> reflog 默认保留 90 天，足够处理大多数误操作。

---

# 10. 子模块

> 🎯 **一句话定义**：在一个 Git 仓库中包含另一个 Git 仓库
>
> 📦 **通俗比喻**：就像在项目中引用一个独立的组件库

## ⚡ 基本用法

```bash
# 添加子模块
git submodule add https://github.com/user/repo.git path/to/submodule

# 初始化子模块
git submodule init

# 更新子模块
git submodule update

# 克隆包含子模块的项目
git clone --recursive https://github.com/user/repo.git
```

---

## 📎 相关文档

| 想要... | 查看文档 |
|--------|----------|
| 学习 Git 基础 | [[Git 入门教程]] |
| 快速查找命令 | [[Git 命令速查]] |
| 团队协作策略 | [[分支管理最佳实践]] |
| 解决 Git 错误 | ~~Git 常见错误解决方案~~ *(已删除)* |
| 知识体系索引 | [[Git MOC]] |

---

**最后更新**：2026-04-05
