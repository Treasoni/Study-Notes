---
tags:
  - git
  - 版本控制
  - 速查
  - cheat-sheet
cssclass: git-cheatsheet
created: 2026-03-02
updated: 2026-03-02
---

# Git 命令速查表

> 快速查找 Git 命令，无需记忆

> [!tip] 使用方式
> - 按 `Ctrl+F` / `Cmd+F` 搜索关键词
> - 或直接浏览下方的分类命令表

---

## 快速命令查阅

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

## 按场景分类

### 仓库初始化

```bash
git init                    # 初始化新仓库
git clone <url>             # 克隆远程仓库
git remote add origin <url> # 添加远程仓库
git remote -v               # 查看远程仓库
```

### 文件操作

```bash
git add <file>              # 添加文件到暂存区
git add .                   # 添加所有修改
git add -u                  # 只添加已跟踪文件的修改
git reset <file>            # 取消暂存
git rm <file>               # 删除文件
git mv <old> <new>          # 重命名文件
```

### 提交操作

```bash
git commit -m "message"     # 提交更改
git commit -am "message"    # 添加并提交已跟踪文件
git commit --amend          # 修改最后一次提交
git commit --amend -m "new" # 修改提交信息
```

### 查看历史

```bash
git log                     # 完整日志
git log --oneline           # 简洁日志
git log -n 5                # 最近 5 条
git log --graph             # 图形化显示
git log <file>              # 某个文件的历史
git show <commit>           # 查看某次提交
```

### 查看差异

```bash
git diff                    # 工作区 vs 暂存区
git diff --staged           # 暂存区 vs HEAD
git diff HEAD               # 工作区 vs HEAD
git diff <file>             # 某个文件的差异
git diff --name-only        # 只看改了哪些文件
```

### 分支操作

```bash
git branch                  # 查看本地分支
git branch -a               # 查看所有分支
git branch <name>           # 创建分支
git checkout -b <name>      # 创建并切换
git switch -c <name>        # 创建并切换（新命令）
git checkout <name>         # 切换分支
git switch <name>           # 切换分支（新命令）
git branch -d <name>        # 删除已合并分支
git branch -D <name>        # 强制删除分支
```

### 合并操作

```bash
git merge <branch>          # 合并分支
git merge --abort           # 取消合并
git rebase <branch>         # 变基
git rebase -i HEAD~3        # 交互式变基
git rebase --abort          # 取消变基
```

### 远程操作

```bash
git fetch                   # 获取远程更新
git pull                    # 拉取并合并
git pull --rebase           # 拉取并变基
git push                    # 推送到远程
git push -u origin <branch> # 首次推送
git push origin --delete <branch>  # 删除远程分支
```

### 撤销操作

```bash
git checkout -- <file>      # 撤销工作区修改
git reset HEAD <file>       # 取消暂存
git reset --soft HEAD~1     # 撤销提交（保留暂存）
git reset --mixed HEAD~1    # 撤销提交（保留工作区）
git reset --hard HEAD~1     # 撤销提交（丢弃修改）
git revert <commit>         # 反转某次提交
```

### 暂存操作

```bash
git stash                   # 暂存当前修改
git stash save "message"    # 带消息的暂存
git stash list              # 查看暂存列表
git stash pop               # 恢复并删除
git stash apply             # 恢复但不删除
git stash drop              # 删除暂存
git stash clear             # 清空所有暂存
```

### 标签操作

```bash
git tag                     # 查看所有标签
git tag <name>              # 创建标签
git tag -a <name> -m "msg"  # 创建注释标签
git tag -d <name>           # 删除标签
git push origin <name>      # 推送标签
git push origin --tags      # 推送所有标签
```

---

## 常见场景速查

### 场景 1：日常开发

```bash
git checkout main
git pull
git checkout -b feature/new-feature
# ... 开发 ...
git add .
git commit -m "feat: 添加新功能"
git push -u origin feature/new-feature
```

### 场景 2：提交后发现漏了文件

```bash
git add forgotten-file
git commit --amend --no-edit  # 不修改提交信息
git push --force  # 谨慎使用
```

### 场景 3：临时切换分支

```bash
git stash                    # 保存当前工作
git checkout other-branch     # 切换分支
# ... 做其他事 ...
git checkout feature-branch   # 切回原分支
git stash pop                 # 恢复工作
```

### 场景 4：撤销最近一次提交

```bash
git reset --soft HEAD~1       # 保留修改
# 或
git reset --hard HEAD~1       # 丢弃修改
```

### 场景 5：解决合并冲突

```bash
git merge feature-branch      # 出现冲突
# 编辑冲突文件
git add <resolved-files>
git commit
```

### 场景 6：查看某文件历史

```bash
git log --follow <file>       # 包含重命名历史
git log -p <file>            # 显示每次修改的内容
```

### 场景 7：清理无用分支

```bash
git branch -d $(git branch --merged | grep -v "main\|develop")  # 删除已合并的本地分支
git remote prune origin       # 清理已删除的远程分支引用
```

---

## 常用参数速查

| 参数 | 含义 | 示例 |
|------|------|------|
| `-a` | 所有 | `git commit -a` |
| `-m` | 消息 | `git commit -m "msg"` |
| `-u` | 上游 | `git push -u origin main` |
| `-v` | 详细 | `git log -v` |
| `--amend` | 修改 | `git commit --amend` |
| `--hard` | 强制 | `git reset --hard` |
| `--soft` | 软 | `git reset --soft` |
| `--force` | 强制推送 | `git push --force` |
| `--no-verify` | 跳过钩子 | `git commit --no-verify` |

---

## 相关文档

- [[Git/Git 入门教程]] - Git 基础概念和操作
- [[Git 高级技巧]] - Rebase、Stash 等
- [[分支管理最佳实践]] - 团队协作分支策略
- [[Git 常见错误解决方案]] - 错误排查

---

**最后更新**：2026-03-02
