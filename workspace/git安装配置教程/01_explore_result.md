# git安装配置教程 - 探测式收集结果

收集时间: 2026-07-31
搜索关键词: [Git Windows 安装, Git for Windows PATH, autocrlf/quotepath, macOS brew/xcode-select, SSH key, credential helper, git alias]

---

## 方向 A：Windows 平台安装与配置（5 条）

| # | 标题 | 来源 | 评分 |
|---|------|------|------|
| 1 | [Git for Windows 官方下载页](https://git-scm.com/download/win) | 官方文档 | 5/5 |
| 2 | [Configuring Git to handle line endings](https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings) | 官方文档 | 5/5 |
| 3 | [Pro Git — Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) | 官方文档 | 4/5 |
| 4 | [Why the git command is unknown in PowerShell](https://learn.microsoft.com/en-us/answers/questions/2032440/why-the-git-command-is-unknown-in-powershell) | 社区 | 4/5 |
| 5 | [git-config 官方手册](https://git-scm.com/docs/git-config) | 官方文档 | 4/5 |

**要点**：官方安装器 Git-2.55.x（64-bit/arm64，winget 可装 `winget install --id Git.Git`）；安装向导选「Git from command line」把 git 加入 PATH；`git 不是内部命令` = PATH 未生效，需重开终端；Windows 配 `core.autocrlf true` + `core.quotepath false` 防换行与中文乱码。

## 方向 B：macOS 平台安装与配置（5 条）

| # | 标题 | 来源 | 评分 |
|---|------|------|------|
| 1 | [git-scm 官方下载页 macOS](https://git-scm.com/download/mac) | 官方文档 | 5/5 |
| 2 | [Caching your GitHub credentials in Git](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git) | 官方文档 | 5/5 |
| 3 | [Homebrew git 公式页](https://formulae.brew.sh/formula/git) | 官方文档 | 5/5 |
| 4 | [Pro Git — Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) | 官方文档 | 4/5 |
| 5 | [Command Line Tools not working (xcrun 修复)](https://stackoverflow.com/questions/32893412/command-line-tools-not-working-os-x-el-capitan-sierra-high-sierra-mojave) | 社区 | 5/5 |

**要点**：三种方式——官方 .pkg / `brew install git`（推荐，Apple Silicon 在 `/opt/homebrew/bin/git`，Intel 在 `/usr/local/bin`）/ `xcode-select --install`；首次运行或系统更新后 Git 失效 = 重装 CLT + `sudo xcodebuild -license accept`；凭据用 `credential.helper osxkeychain`。

## 方向 C：基础配置与认证（5 条）

| # | 标题 | 来源 | 评分 |
|---|------|------|------|
| 1 | [Pro Git — First-Time Git Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) | 官方文档 | 5/5 |
| 2 | [Generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) | 官方文档 | 5/5 |
| 3 | [About remote repositories (HTTPS vs SSH)](https://docs.github.com/en/get-started/git-basics/about-remote-repositories) | 官方文档 | 4/5 |
| 4 | [Caching your GitHub credentials](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git) | 官方文档 | 5/5 |
| 5 | [Pro Git — Git Aliases](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases) | 官方文档 | 4/5 |

**要点**：配置三层级 system/global/local，优先级 local > global > system，文件 `/etc/gitconfig`、`~/.gitconfig`、`.git/config`；SSH 用 `ssh-keygen -t ed25519` + ssh-agent，HTTPS 配 credential helper（Windows=Git Credential Manager，macOS=osxkeychain）；GitHub 一律用 PAT；别名 + `init.defaultBranch main` 写入 `~/.gitconfig`。

---

## 综合分析

- **平台差异集中在安装环节**（Windows 安装器 vs macOS brew/CLT），配置环节大同小异，可合并成一个「通用基础配置」章节。
- **必写的坑**：Windows PATH 未生效、autocrlf 换行符、中文乱码；macOS CLT 失效。
- **认证是配置闭环的关键**：SSH key + credential helper + PAT，两个平台都涉及。
- 信源以 git-scm.com / GitHub Docs / Pro Git 官方为主，权威且稳定。
