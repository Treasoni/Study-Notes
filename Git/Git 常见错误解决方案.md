---
tags:
  - git
  - 错误解决
  - 故障排查
cssclass: error-solutions
created: 2026-02-25
updated: 2026-04-05
---

# Git 常见错误解决方案

> 🆘 遇到 Git 错误时，快速找到解决方案的索引手册

---

## 📑 目录

| 技巧 | 用途 | 难度 |
|------|------|------|
| [[#1-rebase-变基]] | 整理提交历史、保持线性 | ⭐⭐ |
| [[#2-revert-反转提交]] | 安全撤销已推送的提交 | ⭐⭐ |
| [[#3-stash-暂存]] | 临时保存工作进度 | ⭐⭐ |
| [[#4-gitignore-忽略文件]] | 排除不需要跟踪的文件 | ⭐ |
| [[#5-交互式添加]] | 部分提交文件内容 | ⭐⭐ |
| [[#6-搜索代码]] | 在历史中查找代码 | ⭐⭐ |
| [[#7-cherry-pick-精选提交]] | 选择性应用提交 | ⭐⭐⭐ |
| [[#8-bisect-二分查找]] | 定位引入 bug 的提交 | ⭐⭐⭐ |
| [[#9-reflog-恢复]] | 恢复误操作 | ⭐⭐ |
| [[#10-子模块]] | 管理项目依赖 | ⭐⭐⭐ |

| [[#其他常见错误]] | 其他错误场景 | ⭐⭐ |

| [[#预防性检查清单]] | 推送前和日常最佳实践 | ⭐ |
| [[#相关文档]] | 扩展阅读 | ⭐⭐ |
| [[#git MOC]] | 返回知识索引 | ⭐ |
| [[#Git 入门教程]] | 复习基础概念 | ⭐ |
| [[#Git 高级技巧]] | 学习进阶技巧 | ⭐⭐ |

| [[#分支管理最佳实践]] | 学习团队协作规范 | ⭐⭐⭐ |

| [[#Git 常见错误解决方案]] | 解决实际问题 | ⭐⭐ |
| [[#Git 命令速查]] | 速查常用命令 | ⭐ |

| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | 深入学习 | ⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh/get-started/getting-started-with-git | GitHub 指南 | ⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | PDF 速查表 | ⭐ |

| [[#Git 官方文档]] | https://git-scm.com/doc | 官方权威文档 | ⭐ |
| [[#GitHub 指南]] | https://docs.github.com/zh | GitHub 特定指南 | ⭐⭐ |
| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | 免费完整教程 | ⭐⭐ |
| [[#Git Cheat Sheet PDF]] | https://education.github.com/git-cheat-sheet-education.pdf | 可打印速查 | ⭐⭐ |

| [[#GitHub 指南]] | https://docs.github.com/zh | GitHub 特定指南 | ⭐⭐⭐ |

| [[#Git 官方文档]] | https://git-scm.com/doc | 最权威、参考资料 | ⭐⭐⭐ |
| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | 免费深入学习 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | 可打印速查表 | ⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐ |

| [[#Git 官方文档]] | https://git-scm.com/doc | 最权威 | ⭐⭐⭐ |

| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | 最全面的免费教程 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | 可打印速查表 | ⭐⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐ |
| [[#Git 官方文档]] | https://git-scm.com/doc | 最权威 | ⭐⭐⭐ |
| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | 深入学习 Git 的权威书籍 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | 可打印速查表 | ⭐⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐ |
| [[#Git 官方文档]] | https://git-scm.com/doc | 官方文档 | ⭐⭐⭐ |
| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | 免费完整教程 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | PDF 速查表 | ⭐⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐ |

| [[#Git 官方文档]] | https://git-scm.com/doc | 官方文档 | ⭐⭐⭐ |
| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | Pro Git 电子书 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | 可打印速查 | ⭐⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐ |
| [[#Git 官方文档]] | https://git-scm.com/doc | 官方文档 | ⭐⭐⭐ |

| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | Pro Git 电子书 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | 可打印速查表 | ⭐⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐ |
| [[#Git 官方文档]] | https://git-scm.com/doc | 官方文档 | ⭐⭐⭐ |
| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | Pro Git 电子书 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | 可打印速查表 | ⭐⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐ |
| [[#Git 官方文档]] | https://git-scm.com/doc | 官方文档 | ⭐⭐⭐ |
| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | Pro Git 电子书 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | PDF 速查表 | ⭐⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐ |
| [[#Git 官方文档]] | https://git-scm.com/doc | 官方文档 | ⭐⭐⭐ |
| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | Pro Git 电子书 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | PDF 速查表 | ⭐⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐ |
| [[#Git 官方文档]] | https://git-scm.com/doc | 官方文档 | ⭐⭐⭐ |
| [[#Pro Git 中文版]] | https://git-scm.com/book/zh/v2 | Pro Git 电子书 | ⭐⭐⭐ |
| [[#Git Cheat Sheet]] | https://education.github.com/git-cheat-sheet-education.pdf | PDF 速查表 | ⭐⭐⭐ |
| [[#GitHub 官方教程]] | https://docs.github.com/zh | GitHub 官方教程 | ⭐⭐⭐
| [[#Git 官方文档]] | https://git-scm.com/doc | 官方文档 | ⭐⭐⭐
> [!tip] 推荐使用
> - 只在**个人分支**上使用 `--force`
> - 煤人已经确认没有其他人基于该分支工作
 **--force-with-lease** 更安全

 > - 团队协作的主分支**禁止**使用

 >
> - 大文件推送失败

>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```

#### 原因

单个文件超过 100MB（GitHub 限制）或网络问题。

#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型

---

> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。

#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型

---

> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用

 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```

#### 原因
单个文件超过 100MB（GitHub 限制)或网络问题。

#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用

 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制)或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型

---

> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用

 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用

 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型

---

> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用

 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型

---

> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用

 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制)或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---

> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文��推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
---
> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用
 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
 `*.zip`

 ---

> [!warning] 何时使用 force push
> - 只在**个人分支**上使用
> - 煤人需要确认没有其他人基于该分支工作
 **--force-with-lease** 更安全
 > - 团队协作的主分支**禁止**使用

 >
> - 大文件推送失败
>
> #### 错误信息
```text
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```
#### 原因
单个文件超过 100MB（GitHub 限制）或网络问题。#### 解决方案
```bash
# 方案1：使用 Git LFS（推荐)
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
 在 [[Git 高级技巧#4-gitignore-忽略文件|.gitignore]] 中添加大文件类型
```
#### 儿子模块
```

> [!tip] 鄿子模块常用命令速查
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
| | 学习 Git 基础 | [[Git 入门教程]] |
| | 快速查找命令 | [[Git 命令速查]] |
| | 团队协作策略 | [[分支管理最佳实践]] |
| | 解决 Git 错误 | [[Git 常见错误解决方案]] |
| | 知识体系索引 | [[Git MOC]] |

---

**最后更新**： 2026-04-05
