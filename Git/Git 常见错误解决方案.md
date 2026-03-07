---
tags:
  - git
  - 错误解决
  - 故障排查
cssclass: error-solutions
created: 2026-02-25
updated: 2026-02-25
---

# Git 常见错误解决方案

> 遇到 Git 错误时，快速找到解决方案的索引手册

---

# 错误信息速查表

## 按错误信息快速定位

| 错误信息 | 问题描述 | 跳转到解决方案 |
|----------|----------|----------------|
| `Updates were rejected` | 推送被拒绝，远程有新提交 | [推送相关问题](#推送相关问题) |
| `failed to push some refs` | 推送失败 | [推送相关问题](#推送相关问题) |
| `Permission denied (publickey)` | SSH 认证失败 | [配置相关问题](#配置相关问题) |
| `fatal: not a git repository` | 不是 Git 仓库 | [基础问题](#基础问题) |
| `CONFLICT` | 合并冲突 | [合并冲突问题](#合并冲突问题) |
| `fatal: refusing to merge unrelated histories` | 无关历史合并 | [合并冲突问题](#合并冲突问题) |
| `error: failed to push some refs` | 大文件推送失败 | [推送相关问题](#推送相关问题) |

---

## 推送相关问题

### Updates were rejected / 推送被拒绝

#### 错误信息

```text
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '...'
```

#### 原因

远程仓库有本地没有的新提交，直接推送会被拒绝。

#### 解决方案

```bash
# 方案1：拉取并合并（推荐新手）
git pull --rebase
git push

# 方案2：先拉取再合并
git pull origin main
git push

# 方案3：强制推送（谨慎使用！会覆盖远程）
git push --force
# 或更安全的 force-with-lease
git push --force-with-lease
```

> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 确认没有其他人基于该分支工作
> - 团队协作的主分支**禁止**使用

---

### 大文件推送失败

#### 错误信息

```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```

#### 原因

单个文件超过 100MB（GitHub 限制）或网络问题。

#### 解决方案

```bash
# 方案1：使用 Git LFS（推荐）
git lfs install
git lfs track "*.zip"  # 跟踪大文件类型
git add .gitattributes
git commit -m "enable lfs"
git push

# 方案2：从历史中删除大文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch large-file.zip" \
  --prune-empty --tag-name-filter cat -- --all
git push --force
```

> [!tip] 预防大文件问题
> 在 [[git教程#8-高级操作|.gitignore]] 中添加大文件类型

---

## 合并冲突问题

### 完整解决流程

#### 冲突标记格式

```text
<<<<<<< HEAD
main 分支的内容
=======
feature 分支的内容
>>>>>>> feature-branch
```

#### 解决步骤

```bash
# 1. 查看冲突文件
git status

# 2. 手动编辑冲突文件，保留需要的内容
# 删除 <<<<<<< ======= >>>>>>> 标记

# 3. 标记为已解决
git add <conflict-file>

# 4. 完成合并
git commit

# 5. 如果想放弃合并
git merge --abort
```

#### 可视化工具

```bash
# 使用合并工具
git mergetool

# 查看冲突的双方
git diff --ours
git diff --theirs
```

---

### 无关历史合并错误

#### 错误信息

```text
fatal: refusing to merge unrelated histories
```

#### 原因

两个仓库没有共同祖先（如本地初始化后关联远程）。

#### 解决方案

```bash
git pull origin main --allow-unrelated-histories
```

---

## 历史回退问题

### Git reset 后与远程仓库冲突

> [!warning] 常见问题
> 使用 `git reset` 回退版本后，本地历史与远程分叉，推送时会被拒绝。

#### 问题场景

```
┌─────────────────────────────────────────────────────────────┐
│                    历史分叉示意图                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  远程仓库:  A --- B --- C --- D --- E                      │
│                                                             │
│  本地 reset:  A --- B --- C                                    │
│                   ↓                                       │
│  本地落后:     A --- B --- C --- F --- G                      │
│                                                             │
│  推送时被拒绝！                                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 错误信息

```text
! [rejected]        main -> main (fetch first)
error: failed to push some refs to '...'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes before pushing again.
```

#### 原因分析

| 操作 | 结果 |
|------|------|
| `git reset --hard` | 本地历史被改写 |
| 远程仓库有新提交 | 本地落后远程 |
| 直接推送 | Git 安全机制拒绝 |

---

#### 解决方案一：强制推送（个人项目）

> [!danger] 警告
> 此方法会**改写远程历史**，删除被回退的提交。仅适用于：
> - 个人项目
> - 确认没有其他人基于该分支工作
> - 你完全理解后果

```bash
# 1. 本地回退到指定版本
git reset --hard <commit-id>

# 2. 强制推送到远程
git push --force
# 或使用更安全的 force-with-lease
git push --force-with-lease origin main
```

**force vs force-with-lease 对比**：

| 选项 | 安全性 | 说明 |
|------|--------|------|
| `--force` | 低 | 强制覆盖，不管远程是否有新提交 |
| `--force-with-lease` | 高 | 仅在本地基于远程最新状态时才允许推送 |

> [!tip] 推荐使用
> 优先使用 `git push --force-with-lease`，更安全。

---

#### 解决方案二：Revert（团队协作推荐）

> [!tip] 推荐方案
> 适用于已推送的提交，创建新的提交来撤销，保留完整历史。

```bash
# 撤销指定的提交（创建新提交）
git revert <commit-id>

# 如果需要撤销多个提交
git revert <commit-id-1>..<commit-id-2>

# 推送（不需要 force）
git push origin main
```

**Revert 的优势**：
- 不改写历史记录
- 保留所有原始提交
- 团队协作安全

---

#### 解决方案三：Reset + Force（特定场景）

> [!danger] 谨慎使用
> 适用于本地未推送的提交，或确信需要删除远程提交的情况。

```bash
# 1. 确认本地状态
git status
git log --oneline -5

# 2. 回退到指定版本
git reset --hard <commit-id>

# 3. 强制推送
git push --force origin main
```

---

#### 解决方案四：先同步再回退

如果你想在回退的同时保留远程的新提交：

```bash
# 1. 先拉取远程更新
git fetch origin

# 2. 创建备份分支
git branch backup-branch origin/main

# 3. 回退到指定版本
git reset --hard <commit-id>

# 4. 如果需要合并远程的新提交
git rebase origin/main

# 5. 解决冲突后推送
git push origin main --force-with-lease
```

---

#### 完整操作流程（安全版）

```bash
#!/bin/bash
# 安全回退流程脚本

echo "=== Git Reset 安全流程 ==="
echo ""

# 1. 检查当前状态
echo "1. 当前状态："
git status
echo ""

# 2. 查看本地历史
echo "2. 本地最近5次提交："
git log --oneline -5
echo ""

# 3. 查看远程历史
echo "3. 远程最近5次提交："
git log origin/main --oneline -5
echo ""

# 4. 创建备份分支
echo "4. 创建备份分支..."
git branch backup-before-reset-$(date +%Y%m%d)
echo "备份分支: backup-before-reset-$(date +%Y%m%d)"
echo ""

# 5. 执行回退
echo "5. 执行回退到指定版本..."
read -p "输入要回退到的 commit ID: " target_commit
git reset --hard $target_commit
echo ""

# 6. 尝试推送（安全提示）
echo "6. 准备强制推送..."
echo "⚠️  此操作将改写远程历史！"
read -p "确认推送? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    # 使用 force-with-lease 更安全
    git push --force-with-lease origin main
    echo "✅ 推送成功！"
else
    echo "❌ 推送已取消"
    echo "如需恢复，使用: git reset --hard backup-before-reset-$(date +%Y%m%d)"
fi

echo ""
echo "=== 流程完成 ==="
```

---

#### 场景对比表

| 场景 | 推荐方案 | 命令 |
|------|----------|------|
| 本地未提交，个人项目 | Reset + Force | `git reset --hard` + `git push -f` |
| 本地已推送，个人项目 | Reset + Force | `git reset --hard` + `git push -f` |
| 本地已推送，团队协作 | Revert | `git revert` + `git push` |
| 保留远程新提交 | Sync + Reset | `git fetch` + `git rebase` |

---

### 误操作后恢复

#### 使用 reflog 恢复

```bash
# 1. 查看 HEAD 历史记录
git reflog

# 输出示例：
# 1234567 HEAD@{0}: commit: 新功能
# abcdefg HEAD@{1}: reset: moving to HEAD~2
# 8910111 HEAD@{2}: commit: 被误删的提交

# 2. 恢复到指定提交
git reset --hard 8910111

# 3. 如果已推送，需要强制推送（谨慎！）
git push --force
```

#### reset 后后悔了

```bash
# 找到 reset 之前的提交
git reflog

# 恢复
git reset --hard <commit-id>
```

> [!tip] reflog 保存期限
> reflog 默认保留 90 天，足够处理大多数误操作。

---

## 配置相关问题

### SSH 配置失败

#### 错误信息

```text
Permission denied (publickey)
fatal: Could not read from remote repository
```

#### 解决步骤

```bash
# 1. 检查是否有 SSH key
ls ~/.ssh
# 期望看到：id_ed25519 id_ed25519.pub

# 2. 生成新的 SSH key
ssh-keygen -t ed25519 -C "your@email.com"
# 直接回车使用默认路径

# 3. 启动 SSH agent
eval "$(ssh-agent -s)"

# 4. 添加 key
ssh-add ~/.ssh/id_ed25519

# 5. 查看并复制公钥
cat ~/.ssh/id_ed25519.pub

# 6. 添加到 GitHub
# Settings → SSH and GPG keys → New SSH key

# 7. 测试连接
ssh -T git@github.com
```

#### 多 SSH key 管理

```bash
# ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal

Host github.com-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
```

---

### 用户配置错误

#### 问题描述

提交时用户名或邮箱不正确。

#### 解决方案

```bash
# 查看当前配置
git config user.name
git config user.email

# 修改全局配置
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 修改当前项目配置
git config user.name "Your Work Name"
git config user.email "work@company.com"

# 修改最近的提交（未推送）
git commit --amend --author="Your Name <your@email.com>"
```

---

## 基础问题

### 不是 Git 仓库

#### 错误信息

```text
fatal: not a git repository (or any of the parent directories)
```

#### 原因

当前目录不是 Git 仓库。

#### 解决方案

```bash
# 方案1：初始化新仓库
git init

# 方案2：切换到正确的项目目录
cd /path/to/your/project

# 方案3：克隆远程仓库
git clone <url>
```

---

### 文件被忽略但未在 .gitignore 中

#### 原因

文件已被 Git 跟踪，.gitignore 对已跟踪文件无效。

#### 解决方案

```bash
# 从跟踪中删除，但保留本地文件
git rm --cached file.txt

# 或删除整个目录的跟踪
git rm -r --cached directory/

# 提交更改
git commit -m "stop tracking file"

# 确保在 .gitignore 中添加规则
echo "file.txt" >> .gitignore
```

---

## 其他常见错误

### Detached HEAD 状态

#### 问题描述

```text
You are in 'detached HEAD' state.
```

#### 原因

处于某个提交点，而非分支上。

#### 解决方案

```bash
# 方案1：创建新分支保存当前工作
git checkout -b new-branch

# 方案2：回到原来的分支
git checkout main

# 方案3：保存修改后切回分支
git stash
git checkout main
```

---

### 撤销最近的提交（已推送）

#### 方案1：revert（推荐）

```bash
# 创建新提交来抵消旧提交
git revert <commit-id>
git push
```

#### 方案2：reset（谨慎）

```bash
# 仅在个人分支或确认无风险时使用
git reset --hard <commit-id>
git push --force
```

> [!warning] 推荐使用 revert
> - revert 创建新提交，不会改写历史
> - reset 会改写历史，可能影响他人

---

## 预防性检查清单

### 推送前检查

```bash
# 1. 检查状态
git status

# 2. 查看将要推送的内容
git log origin/main..HEAD

# 3. 先拉取远程更新
git fetch
git log HEAD..origin/main

# 4. 如有远程更新，先合并
git pull --rebase

# 5. 确认后再推送
git push
```

### 日常最佳实践

- [ ] 使用 [[git教程#10-最佳实践|规范的提交信息]]
- [ ] 小而频繁的提交，而非大批量
- [ ] 推送前先拉取
- [ ] 使用分支而非直接在 main 开发
- [ ] 定期备份重要分支（打 tag）
- [ ] 使用 `.gitignore` 避免提交不必要的文件

---

## 相关文档

- [[Git/Git MOC]] - Git 知识体系索引
- [[Git 入门教程]] - Git 完整入门教程
- [[Git 入门教程#7-远程仓库与协作|远程仓库与协作]] - SSH 配置详解
- [[分支管理最佳实践]] - 避免冲突的分支策略

---

**最后更新**：2026-02-25
