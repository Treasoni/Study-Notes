---
title: Git 安装配置教程
tags:
  - git
  - 版本控制
  - 教程
  - 安装配置
created: 2026-07-31
updated: 2026-07-31
status: 已完成
source_project: learning-note-flow
---

# Git 安装配置教程

## 前言

这份笔记与 vault 内既有的 [[Git 入门教程]] 互补——后者讲分支、提交等「用起来」的概念，本篇聚焦「平台化安装步骤 + 基础配置闭环」，用最小步骤把 Git 装好、配好、跑通。适合已经知道 add/commit 基本概念、但还没系统安装配置过 Git 的读者。阅读路径：只装 Windows 读第 1、2 章后直接跳到第 4 章；只装 macOS 读第 1、3 章后跳到第 4 章；第 4 至 7 章（配置、认证、别名、排错）双平台通用。

## 目录

1. [[#第一章：安装前的准备与平台选型|第一章：安装前的准备与平台选型]]
2. [[#第二章：Windows 安装与验证|第二章：Windows 安装与验证]]
3. [[#第三章：macOS 安装与验证|第三章：macOS 安装与验证]]
4. [[#第四章：首次基础配置（通用 + 双平台差异）|第四章：首次基础配置（通用 + 双平台差异）]]
5. [[#第五章：认证配置——SSH 与 HTTPS|第五章：认证配置——SSH 与 HTTPS]]
6. [[#第六章：实用别名与全局忽略|第六章：实用别名与全局忽略]]
7. [[#第七章：收尾验证与常见问题速查|第七章：收尾验证与常见问题速查]]

---

## 第一章：安装前的准备与平台选型

动手下载安装包前，先花两分钟确认两件事：这篇笔记补的是哪块能力，你的平台该走哪条安装路线。平台选错，后面 PATH、换行符、凭据配置会连环踩坑。

### 本篇定位：与《Git 入门教程》互补

vault 里已有的 [[Git 入门教程]] 覆盖 add/commit、分支等「用起来」的概念。本篇不重复这些，只补它没覆盖的两块：**平台化的安装步骤** 与 **一套最小可用的基础配置闭环**。

> [!note] 阅读路径
> 只装 Windows 读第 2 章，只装 macOS 读第 3 章；第 4-6 章为通用配置与认证，第 7 章为排错速查。配置层级（system/global/local）本篇只一句话带过，细节见 [[Git 入门教程]] 第 2 章。

### 版本现状与获取渠道

Git 迭代较快，当前稳定版为 **2.55.x 或更新**，直接到 [git-scm.com 官方下载页](https://git-scm.com/download/win) 下载即可，不必追每个小版本 [Pro Git — Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)。命令行安装便于后续升级：Windows 用官方推荐的 winget，macOS 用 Homebrew。

### 双平台安装策略总览

| 平台 | 推荐路线 | 备选方案 | 关键注意点 |
|------|---------|---------|-----------|
| Windows | Git for Windows 安装包，或 `winget install --id Git.Git -e --source winget` | Chocolatey（社区维护） | 向导中 PATH 选「Git from the command line and also from 3rd-party software」 |
| macOS | Homebrew：`brew install git` [Homebrew git 公式](https://formulae.brew.sh/formula/git) | 官方 pkg / Xcode CLT | 装完确认 `which git` 指向 brew 路径，否则 PATH 顺序有误 |

> [!tip] 安装完成的对照标准
> 无论哪个平台，装完后在终端执行：
>
> ```bash
> git --version
> ```
>
> 预期输出形如 `git version 2.55.x`（小版本以实际装到为准）。看到该输出即代表 PATH 已生效，可以进入第 4 章做首次配置。

下一章从 Windows 的图形安装向导与 winget 命令行安装讲起，并解决最常见的「git 不是内部命令」。

---

## 第二章：Windows 安装与验证

Windows 没有系统自带的 Git，装错选项就会遇到「git 不是内部命令」这道第一道坎。本章覆盖图形安装向导的关键选项、winget / Chocolatey 两种命令行安装、安装后验证，以及最常见的 PATH 排查。

### 图形安装向导：四个关键选项

从 [git-scm.com 官方下载页](https://git-scm.com/download/win) 下载 x64 Setup（当前稳定版 **2.55.x 或更新**），一路 Next 时只需盯住四个选项 [Pro Git — Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)：

1. **PATH 三选（最关键）**：默认（也是推荐）选 **「Git from the command line and also from 3rd-party software」**，让 cmd、PowerShell 以及第三方软件都能直接用 `git`。如果选了「只从 Git Bash 使用 Git」，装完在 PowerShell 里就会报「不是内部命令」。
2. **Git Bash**：保持勾选。它自带一套 Unix 风格命令行，是 Windows 上新手最省心的入口。
3. **默认编辑器**：默认 vim 可以留着，想用 VSCode 就改选 Visual Studio Code——这决定 `git commit` 时打开哪个编辑器。
4. **符号链接（symlink）**：默认关闭。开启需要管理员权限，普通用户不必打开。

> [!note] 核心概念：PATH 决定 `git` 能不能被找到
> 终端输入 `git` 时，系统按 PATH 里列出的目录逐个查找 `git.exe`。PATH 没配好，等于没装。

> [!tip] 实践建议
> 除上述四项外，向导其余选项（如 Windows Explorer 集成）保持默认即可，不勾选也不影响命令行使用。

### 命令行安装：winget 官方推荐 / Chocolatey

不想点图形向导，可用包管理器安装，后续升级也更省事。官方推荐 winget：

```powershell
winget install --id Git.Git -e --source winget
```

社区维护的 Chocolatey 是备选：

```powershell
choco install git
```

> [!note] 核心概念：图形向导与命令行安装二选一
> 两者安装的都是同一套 Git for Windows，只是入口不同。不要既跑向导又跑命令，避免覆盖各自的配置默认值。

### 安装后验证

装完**重开终端**（关键），执行：

```bash
git --version
```

预期输出形如 `git version 2.55.x`（小版本以实际装到为准）。看到该输出即代表 PATH 已生效，可以进入后续章节做首次配置。

### 排查：「git 不是内部命令」

若提示 `git 不是内部或外部命令`（PowerShell 下是 `git : 无法将“git”项识别为 cmdlet...`），说明 PATH 未配置或未刷新 [Why the git command is unknown in PowerShell](https://learn.microsoft.com/en-us/answers/questions/2032440)。按顺序排查：

1. **先重开终端**——环境变量在终端启动时读取，旧终端不会自动刷新。
2. **重跑安装向导**，把 PATH 选项改回推荐项。
3. **手动加入 PATH**：设置 → 系统 → 关于 → 高级系统设置 → 环境变量，在「系统变量」的 `Path` 中追加：

```text
C:\Program Files\Git\cmd
```

> [!warning] 易错点
> 手动加完 PATH 必须重开终端才生效；若装的是 32 位版，默认路径是 `C:\Program Files (x86)\Git\cmd`，按实际安装路径核对。

### Windows 安装常见坑

| 现象 | 原因 | 解决 |
|------|------|------|
| `git` 不是内部命令 | PATH 未配置/未刷新 | 重跑安装器改 PATH，或手动加 `C:\Program Files\Git\cmd`，重开终端 |
| push 反复要密码 | GCM 未启用或版本过旧 | 升级 Git for Windows，确认 `credential.helper manager` [Caching your GitHub credentials in Git](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git) |
| 改换行符后整库文件显示被修改 | autocrlf 触发重归一化 | `git add . -u` → `git add --renormalize .` → 提交 |
| 缓存了错误旧密码导致 push 失败 | 凭据管理器存了旧凭据 | 控制面板 → 凭据管理器 → 删除 GitHub 条目后重新认证 |
| 图片等二进制被 git 改坏 | 文本转换误伤二进制 | `.gitattributes` 加 `*.png binary`（binary = `-text -diff`） |

### 本章小结

- 图形向导只需盯住 PATH 三选、Git Bash、默认编辑器、符号链接四项，其余保持默认。
- 命令行安装：`winget install --id Git.Git -e --source winget` 官方推荐，`choco install git` 社区备选。
- 验证标准：`git --version` 输出 `git version 2.55.x`。
- 「不是内部命令」= PATH 问题：重开终端 → 重跑向导 → 手动加 `C:\Program Files\Git\cmd`。
- Windows 常见坑集中在 PATH 与凭据（GCM），确认 `credential.helper manager` 即可避免反复要密码。

下一章进入 macOS：三种安装方式对比与 Homebrew 推荐路线。

---

## 第三章：macOS 安装与验证

macOS 虽然自带 git，但那是 Apple 维护的旧版，升级和排查都不太顺手。本章把三种安装方式放在一张表里对比，给出推荐路线（Homebrew），并解决装完后最常撞上的两个问题：`which git` 仍指向系统路径、Xcode CLT 失效。

### 三种安装方式对照

在动手之前，先看清三条路各自通向哪里 [git-scm 官方下载页 macOS](https://git-scm.com/download/mac) [Homebrew git 公式](https://formulae.brew.sh/formula/git)：

| 方式 | 命令 | git 路径 | 优缺点 |
|------|------|----------|--------|
| 官方 .pkg | git-scm.com 下载 macOS 安装包 | `/usr/local/git/bin/git` | 独立、版本较新；升级麻烦，易与 brew 版 PATH 冲突 |
| **Homebrew（推荐）** | `brew install git` | Apple Silicon `/opt/homebrew/bin/git`；Intel `/usr/local/bin/git` | 升级省心（`brew upgrade git`）、生态完整 |
| Xcode CLT | `xcode-select --install` | `/usr/bin/git`（Apple 旧版约 2.39.x，随系统更新而变） | 零安装、随系统更新；版本落后，够入门 |

> [!note] 核心概念：macOS 上可能同时存在多个 git
> 系统、CLT、brew 各装一套 git，命令行最终用哪套由 PATH 顺序决定。装完后必须确认 `which git` 指向你想要的那套，否则你「以为在升级」其实还在用旧版。

### 推荐路线：Homebrew

三选一选 Homebrew：升级一条命令搞定，路径清晰，且自带完整的 git 附属工具（含 `git-credential-osxkeychain`）。若还没装 Homebrew，先按官网脚本装好，再执行：

```bash
brew install git
```

> [!tip] 实践建议
> 用 CLT 版 git 入门没问题；但要长期使用或需要较新特性时，尽早切到 Homebrew 版，省得日后路径冲突再折腾一次。

### PATH 顺序修正与验证

装完**新开一个终端标签页**，验证：

```bash
git --version
which git
```

预期 `git --version` 输出 `git version 2.55.x 或更新`（以实际装到为准），`which git` 指向 `/opt/homebrew/bin/git`（Apple Silicon）或 `/usr/local/bin/git`（Intel）。

如果 `which git` 仍是 `/usr/bin/git`，说明 `/usr/bin` 排在 PATH 前面，把 brew 路径放到最前（zsh 默认 shell）：

```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

> [!warning] 易错点
> Intel 机器把上面路径换成 `/usr/local/bin`；改完 `.zshrc` 后要 `source` 或重开终端才生效。若此前装过官方 pkg，可再补 `brew link git --overwrite` 清理冲突。

### CLT 失效修复链

`xcode-select --install` 会触发图形安装弹窗；用全量 Xcode 的机器还需 `sudo xcodebuild -license accept`。当 CLT 损坏或缺失，终端会报 `xcrun: invalid active developer path`，按顺序执行修复 [Command Line Tools not working (xcrun 修复)](https://stackoverflow.com/questions/32893412)：

```bash
xcode-select --install
sudo xcode-select --reset
sudo xcode-select --switch /Library/Developer/CommandLineTools
xcode-select -p   # 验证，应输出 /Library/Developer/CommandLineTools
```

仍失败时，最后的手段是删除后重装：`sudo rm -rf /Library/Developer/CommandLineTools`，再执行 `xcode-select --install`。

### macOS 安装常见坑

| 现象 | 原因 | 解决 |
|------|------|------|
| `which git` 仍是 `/usr/bin/git` | PATH 顺序，`/usr/bin` 在前 | brew 路径加到最前；或 `brew link git --overwrite` |
| `xcrun: invalid active developer path` | CLT 缺失/损坏 | 按 CLT 失效修复链依次执行，最后 `xcode-select -p` 验证 |
| `git-credential-osxkeychain: command not found` | helper 不在 PATH | 用 brew 版 git（自带该 helper），或用 `/usr/bin/git-credential-osxkeychain` |
| push 反复要密码 | 没用 PAT（GitHub 已禁账户密码） | 生成 PAT 作为密码输入，不是账户密码 |

### 本章小结

- 三种方式：官方 pkg 独立但升级麻烦；Homebrew 推荐，路径清晰、`brew upgrade git` 省心；CLT 零安装但版本落后（约 2.39.x，随系统更新而变）。
- 安装后验证：`git --version` + `which git`，后者必须指向 brew 路径而非 `/usr/bin/git`。
- PATH 顺序修正：把 `/opt/homebrew/bin`（Intel 为 `/usr/local/bin`）加到 PATH 最前，改完 `.zshrc` 记得 `source`。
- CLT 失效修复合集：`xcode-select --install` → `--reset` → `--switch` → `xcode-select -p` 验证，最后手段是删除重装。
- 常见坑集中在 PATH 顺序与 CLT 损坏，对照表格现象排查即可。

下一章进入通用的首次基础配置：身份、默认编辑器、换行符与中文显示，双平台差异一并对照。

---

## 第四章：首次基础配置（通用 + 双平台差异）

装完 Git 只是第一步。如果不先配好身份、换行符和中文显示，第一次 commit 就会撞上「提交者身份未设置」「整库文件全被标记修改」这类问题。本章做一套一次性全局配置，双平台差异集中在换行符一处，其余全部通用，是「装完能跑」的核心。

### 身份信息：user.name / user.email

Git 每次 commit 都要记录作者。不设置时提交会报错 `Please tell me who you are`，并且提交是匿名的。用 `--global` 写入当前用户级别 [Pro Git — First-Time Git Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)：

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

> [!note] 核心概念：身份写入每一次提交
> `user.name` 是展示名，`user.email` 关联你的 GitHub / GitLab 账号。邮箱写错，提交会归到错误的账号名下，事后改历史很麻烦。

> [!tip] 实践建议
> 邮箱用与 GitHub 账号绑定的地址（或用 GitHub 提供的 noreply 隐私邮箱），姓名用常用网名即可。若某个仓库想用不同身份，在该仓库内执行不带 `--global` 的 `git config` 覆盖。

### 默认编辑器与默认分支

`git commit` 时会打开编辑器写提交信息，默认 vim 对新手不友好；同时新仓库默认分支名仍是 `master`，主流平台已切到 `main`。两条命令一次配好：

```bash
git config --global core.editor code --wait
git config --global init.defaultBranch main
```

> [!warning] 易错点
> `code --wait` 依赖系统装好 VSCode 且 `code` 命令在 PATH 中；Windows 上若 `code` 不在 PATH，可写成 VSCode 的完整路径，或退回 `vim`。`init.defaultBranch` 只影响之后 `git init` 的新仓库，对已有仓库不生效。

### 配置三层级：一句话速览

Git 配置分 system（整台机器）/ global（当前用户，存 `~/.gitconfig`）/ local（当前仓库，存 `.git/config`）三层，优先级 **local > global > system** [git-config 官方手册](https://git-scm.com/docs/git-config)。本篇只需 `--global` 就够，层级细节不展开，见既有笔记 [[Git 入门教程]] 第 2 章。

### 换行符：双平台对照

Windows 文本用 CRLF 换行，macOS / Linux 用 LF。混用会让 diff 看起来整文件都被改动。`core.autocrlf` 让 Git 在提交时统一存成 LF、检出时按平台转回本地格式 [Configuring Git to handle line endings](https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings)：

| 平台 | 命令 | 行为 |
|------|------|------|
| Windows | `git config --global core.autocrlf true` | 提交转 LF、检出转 CRLF |
| macOS | `git config --global core.autocrlf input` | 提交转 LF、检出保持 LF（不额外转换） |

> [!tip] 跨平台仓库：用 `.gitattributes` 统一规则
> 团队同时有 Windows 和 macOS 成员时，只靠个人配置仍可能不一致。更稳的做法是在仓库根目录放 `.gitattributes`，让所有协作者遵循同一套规则：

```text
* text=auto
*.png binary
```

`* text=auto` 让 Git 自动识别文本文件并统一成 LF；`*.png binary` 把图片等二进制标记为 `-text -diff`，防止文本转换误伤文件。

### 中文文件名显示

Windows 终端默认会把中文文件名转义成 `\346\265\213` 这样的八进制序列。关闭转义即可正常显示：

```bash
git config --global core.quotepath false
```

> [!tip] 实践建议
> 这条对 Windows 中文用户几乎是必配。macOS 默认显示正常，通常无需设置；设置后也无副作用。

### 查看配置

配完后用一条命令核对全部配置，并确认每项来自哪个文件 [git-config 官方手册](https://git-scm.com/docs/git-config)：

```bash
git config --list --show-origin
```

> [!note] 核心概念：--show-origin 显示来源
> 输出会标注每行配置来自 `/etc/gitconfig`、`~/.gitconfig` 还是仓库的 `.git/config`。当「配置了却没生效」时，靠它定位是哪一层级的哪个值覆盖了你的设置。

### 本章小结

- 身份：`git config --global user.name / user.email`，邮箱关联账号，写错改历史很麻烦。
- 编辑器与分支：`core.editor code --wait`、`init.defaultBranch main` 各配一次即可。
- 三层级：system / global / local，优先级 local > global > system；本篇只用 `--global`，细节见 [[Git 入门教程]]。
- 换行符：Windows `core.autocrlf true`、macOS `core.autocrlf input`；跨平台仓库在根目录加 `.gitattributes`（`* text=auto`、`*.png binary`）。
- 中文与查看：`core.quotepath false` 关闭转义；`git config --list --show-origin` 核对所有配置及其来源。

下一章进入认证：用 SSH 或 HTTPS 让本机与 GitHub / GitLab 真正打通。

---

## 第五章：认证配置——SSH 与 HTTPS

前四章装好并配好了 Git，但 clone / push / pull 远程仓库时还要过「认证」这一关。不配认证，要么每次都输密码，要么干脆连不上 GitHub / GitLab。本章把两种主流认证方式——SSH 与 HTTPS——完整走一遍：选型、密钥生成、SSH Agent、连接验证、HTTPS 凭据助手，并拆解双平台各自的坑。

### SSH 与 HTTPS 怎么选

先说结论：两种协议都能 clone / push / pull，区别在于「怎么证明是你」。

| 维度 | SSH | HTTPS |
|------|-----|-------|
| URL 形态 | `git@github.com:user/repo.git` | `https://github.com/user/repo.git` |
| 首次配置 | 生成密钥 + 配置 Agent | 装好 Git 即基本可用 |
| 认证凭据 | 密钥对 + passphrase | PAT / GCM 浏览器登录 |
| 典型场景 | 频繁 push 的长期开发 | 一次性 clone、防火墙严格环境 |
| 备注 | port 22 被墙时可走 SSH over HTTPS 443 | 通用、防火墙友好 |

[About remote repositories (HTTPS vs SSH)](https://docs.github.com/en/get-started/git-basics/about-remote-repositories) 的说明里，SSH 的优势是配置一次后长期免密，HTTPS 的优势是零前置配置。对大多数读者，**建议优先配 SSH**，之后 clone 远程仓库时统一用 SSH URL；HTTPS 作为备选通道保留。

### SSH 密钥生成（ed25519 主 / RSA 备用）

密钥是「你是你」的凭证，只需生成一次：公钥交给平台，私钥留在本机 [Generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)：

```bash
ssh-keygen -t ed25519 -C "you@example.com"
# 旧系统 / 老旧服务器备用：
ssh-keygen -t rsa -b 4096 -C "you@example.com"
```

> [!note] 核心概念：ed25519 是当前推荐的主算法
> `-t` 指定算法，`-C` 加注释（常用邮箱标识这把密钥）。ed25519 更短更快，是 GitHub 推荐的新默认；RSA 4096 留给仍不支持 ed25519 的旧系统。GitHub 已于 2022-03-15 弃用 DSA，RSA 也需 SHA-2 签名。

按提示一路回车使用默认路径 `~/.ssh/id_ed25519`，并设置一个 passphrase（类似密码，保护私钥）。之后用 `cat ~/.ssh/id_ed25519.pub` 查看公钥内容，把公钥加到 GitHub / GitLab——**只贴 `.pub` 文件内容**，绝不要把 `id_ed25519`（私钥）发出去：

```text
GitHub:  Settings → SSH and GPG keys → New SSH key → 粘贴公钥 → Add
GitLab:  Settings → SSH Keys → Key → 粘贴公钥 → Add key
```

### 配置 SSH Agent

密钥生成后，每次连接仍要输 passphrase。SSH Agent 是「帮你记住 passphrase」的守护进程：把私钥交给它托管后，本次会话内不再重复输入。双平台配置方式不同，分小节说明。

#### macOS：钥匙串托管

macOS 启动 Agent，并让私钥进入钥匙串（Keychain），passphrase 交给系统记住 [Generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)：

```bash
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/id_ed25519   # Monterey 之前用 -K
```

再编辑 `~/.ssh/config`，让 Agent 连接 github.com 时自动加载密钥：

```text
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

#### Windows：启用 OpenSSH 服务

Windows 的 Agent 是系统服务，默认未启动，需用**管理员权限**的 PowerShell 开启 [Generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)：

```powershell
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent
ssh-add c:/Users/YOU/.ssh/id_ed25519
```

> [!warning] Windows 高频坑：git 自带的 ssh 不走 ssh-agent
> 装 Git for Windows 后，`git` 默认用的是它自带的 ssh.exe，而不是系统 OpenSSH，于是「ssh-agent 配好了，git push 还是要 passphrase」。解决办法是强制 git 改用系统 OpenSSH：
>
> ```bash
> git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
> ```

### 验证连接

密钥与 Agent 配好后，用一条命令验证与 GitHub 的连通 [Generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)：

```bash
ssh -T git@github.com
```

预期输出：

```text
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
```

看到 `successfully authenticated` 即代表认证打通。GitLab 同理，把主机名换成 `gitlab.com` 再验一次。

### HTTPS + 凭据助手

不想配密钥时，HTTPS 是零配置的选择：GitHub 已禁用密码认证，HTTPS 一律用 **PAT（Personal Access Token）** 作为密码 [Caching your GitHub credentials in Git](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)。凭据助手负责「记住」它，双平台设置如下：

| 平台 | 命令 | 行为 |
|------|------|------|
| Windows | `git config --global credential.helper manager` | Git Credential Manager（GCM），首次 HTTPS 自动弹浏览器 OAuth 登录，支持 2FA |
| macOS | `git config --global credential.helper osxkeychain` | 钥匙串存储，macOS 默认即此值 |

> [!warning] 易错点：输 PAT 而不是账户密码
> macOS 上首次 HTTPS push 提示输入用户名和密码时，密码框填的是 PAT，不是账户密码。Git for Windows ≥2.29 自带 GCM，首次 clone 走浏览器登录，一般无需手动建 PAT；旧版「GCM for Windows」已废弃。

### remote URL 切换（HTTPS ↔ SSH）

clone 时 Git 按 URL 自动识别走哪种认证。对已有仓库，`origin` 指向的 URL 形态决定了认证通道。查看与切换 [About remote repositories (HTTPS vs SSH)](https://docs.github.com/en/get-started/git-basics/about-remote-repositories)：

```bash
git remote -v                                          # 查看当前 origin URL
git remote set-url origin git@github.com:user/repo.git          # HTTPS → SSH
git remote set-url origin https://github.com/user/repo.git      # SSH → HTTPS
```

新仓库首次关联用 `git remote add origin <REMOTE_URL>`，URL 形态决定通道。切到 SSH 后若仍反复要 passphrase，回头检查上面的 Agent 与 `core.sshCommand` 配置是否完整。远程仓库的 add / push / pull 基础操作见既有笔记 [[Git 入门教程]]，本章只补认证这一环。

### 本章小结

- 选型：SSH 配置一次长期免密，适合频繁 push；HTTPS 零前置配置、防火墙友好，凭据一律用 PAT。
- 密钥：`ssh-keygen -t ed25519` 生成，旧系统用 RSA 4096 备用；公钥只贴 `.pub`，加到 GitHub / GitLab。
- Agent：macOS 用钥匙串（`ssh-add --apple-use-keychain` + `~/.ssh/config`）；Windows 需先启用 ssh-agent 服务，`core.sshCommand` 强制走系统 OpenSSH 是高频修复。
- 验证：`ssh -T git@github.com` 看到 `successfully authenticated` 即通。
- HTTPS 凭据：Windows `credential.helper manager`（GCM）、macOS `osxkeychain`；GitHub 禁密码，一律输 PAT。
- 切换：`git remote -v` 查看、`git remote set-url origin <新URL>` 在 HTTPS 与 SSH 之间切换。

认证打通后，下一章用别名和全局忽略把高频命令变短、把临时文件挡在仓库外。

---

## 第六章：实用别名与全局忽略

前五章把 Git 装好、配好身份与认证，日常操作已经能跑通。但高频命令反复敲 `git checkout`、`git status` 又长又容易打错，而且每个仓库都可能混入 `.DS_Store`、`Thumbs.db` 这类系统垃圾文件。本章配一套常用别名把命令变短，再用全局忽略把垃圾文件统一挡在仓库外。

### 常用别名：把高频命令变短

别名的核心语法是 `git config --global alias.<短命令> '<原命令参数>'`——注册一个短命令，让 git 执行时把它替换成后面的完整命令 [Pro Git — Git Aliases](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases)。下面一次注册四个最常用的别名：

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```

| 别名 | 展开后的命令 | 效果 |
|------|-------------|------|
| `git co` | `git checkout` | 切换分支 / 恢复文件 |
| `git br` | `git branch` | 查看 / 管理分支 |
| `git ci` | `git commit` | 提交 |
| `git st` | `git status` | 查看工作区状态 |

分支、提交的具体含义见既有笔记 [[Git 入门教程]]，本章只做「缩短命令」。另有两条更「动作化」的别名，一条撤销暂存、一条查看最近一次提交：

```bash
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
```

- `git unstage fileA` 等价于 `git reset HEAD -- fileA`，把误 `add` 进暂存区的文件退出来。
- `git last` 等价于 `git log -1 HEAD`，只显示最近一条提交记录。

> [!tip] 实践建议
> 别名本质是「字符串替换」：别名后追加的参数会接在展开结果的末尾，例如 `git st -s` 会变成 `git status -s`。所有别名都保存在 `~/.gitconfig` 的 `[alias]` 段，想反悔直接打开文件删掉对应行即可。

### 外部命令别名：`!` 前缀

普通别名展开的是 git 子命令；以 `!` 开头的别名则让 Git 把后面的字符串**原样交给 shell 执行** [Pro Git — Git Aliases](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases)，因此可以调用任意外部程序：

```bash
git config --global alias.visual '!gitk'
```

执行 `git visual` 时，Git 不再尝试把 `gitk` 当作子命令，而是直接启动 `gitk` 图形查看器。`!` 前缀就是「逃出 git 命令系统、执行外部命令」的信号。

### 全局忽略：core.excludesFile

仓库里的 `.gitignore` 会随仓库提交、和协作者共享，适合放「项目级」忽略规则。但 `.DS_Store`（macOS）、`Thumbs.db`（Windows）这类系统文件只属于你个人，不该污染每个仓库。Git 提供全局忽略：把 `core.excludesFile` 指向一个你自己的忽略文件 [git-config 官方手册](https://git-scm.com/docs/git-config)：

```bash
git config --global core.excludesFile ~/.gitignore_global
```

再创建 `~/.gitignore_global`，语法与 `.gitignore` 完全一致，写上通用的系统垃圾文件：

```text
.DS_Store
Thumbs.db
*.log
```

> [!warning] 易错点：全局忽略只作用于本地
> `core.excludesFile` 指向的文件只在本机生效，不会随仓库提交、也不会同步给协作者。它和 `.gitignore` 的分工是：**个人系统垃圾放全局忽略，项目级规则放仓库 `.gitignore`**。

### 本章小结

- 别名语法：`git config --global alias.<短命令> '<原命令参数>'`，保存到 `~/.gitconfig` 的 `[alias]` 段。
- 常用别名：`co / br / ci / st` 覆盖 checkout / branch / commit / status；`unstage` 撤销暂存；`last` 查看最近一次提交。
- 外部命令：别名以 `!` 开头时由 shell 直接执行，`git visual` 即启动 `gitk`。
- 全局忽略：`core.excludesFile ~/.gitignore_global` 指定个人忽略文件，通用示例 `.DS_Store`、`Thumbs.db`、`*.log`。
- 作用范围：全局忽略只作用于本机、不随仓库提交，与 `.gitignore` 按「个人 vs 项目」分工。

至此本机配置闭环完成，下一章用一条完整流程做端到端收尾验证，并给出双平台常见问题速查表。

---

## 第七章：收尾验证与常见问题速查

前六章把安装、配置、认证、别名全部落地。收尾这章做两件事：先用一条可复制的完整命令序列把整个流程端到端跑通一次，确认每个环节真的生效；再给一张双平台常见问题速查表，作为以后遇到问题时的第一排查入口。

### 端到端自检：从 init 到 push

自检的意义在于「一次跑通验证全部环节」——命令本身你大概率已经会，重点看每一行对应的预期输出是否符合。新建一个临时仓库，把第四章配好的身份、换行符、中文显示，以及第五章配好的认证全部真实走一遍：

```bash
# 1. 新建仓库并初始化
mkdir demo-repo && cd demo-repo
git init

# 2. 添加文件并提交
echo "# Demo" > README.md
git add .
git commit -m "init"

# 3. 关联远程仓库（URL 换成你在 GitHub / GitLab 新建的空仓库地址）
git remote add origin <你的远程仓库URL>

# 4. 推送并绑定上游分支
git push -u origin main
```

各步骤的预期结果：

- `git init` 输出 `Initialized empty Git repository in .../demo-repo/.git/`。
- `git commit -m "init"` 输出 `[main (root-commit) <短哈希>] init`。若提示身份缺失，说明第四章的 `user.name / user.email` 没配好。
- `git remote add` 正常无输出；可接着用 `git remote -v` 确认 origin 地址已写入。
- `git push -u origin main` 出现进度条和 `main -> main` 即成功。若弹出认证，说明第五章的 SSH 或 HTTPS 凭据未生效，回到对应小节补配。

> [!note] 核心概念
> `-u`（`--set-upstream`）把本地 `main` 与远程 `origin/main` 建立上下游绑定，之后 `git push`、`git pull` 都不用再写分支名。这是一次性建立关系、长期受益的参数 [About remote repositories](https://docs.github.com/en/get-started/git-basics/about-remote-repositories)。

### 双平台常见问题速查

把本篇素材里反复出现的坑按「现象 → 平台 → 解决」收拢成一张表，来源对应前几章的排查路径 [Microsoft Q&A — Why the git command is unknown in PowerShell](https://learn.microsoft.com/en-us/answers/questions/2032440)、[Command Line Tools not working](https://stackoverflow.com/questions/32893412)、[Caching your GitHub credentials in Git](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)：

| 现象 | 平台 | 解决 |
|------|------|------|
| `git` 不是内部命令 | Windows | PATH 未配 / 未刷新。重跑安装器把 PATH 选为「Git from the command line...」，或手动把 `C:\Program Files\Git\cmd` 加入系统 PATH，**重开终端** |
| `which git` 仍是 `/usr/bin/git` | macOS | PATH 顺序问题。把 brew 路径 `/opt/homebrew/bin` 加到 `~/.zshrc` 最前并 `source ~/.zshrc` |
| `xcrun: invalid active developer path` | macOS | CLT 失效。按 `xcode-select --install` → `sudo xcode-select --reset` → `sudo xcode-select --switch /Library/Developer/CommandLineTools` 依次修复，最后 `xcode-select -p` 验证 |
| 改换行符后整库文件显示被修改 | 双平台 | autocrlf 触发重归一化，执行下方命令序列 |
| push 反复要密码或报错 | 双平台 | 凭据缓存了旧密码 / 未用 PAT。Windows 在控制面板「凭据管理器」删除 GitHub 旧条目后重新认证；macOS 输入 PAT 而非账户密码 |
| 中文文件名显示成 `\346\265\213` 转义码 | Windows | 执行 `git config --global core.quotepath false` |

**换行符重归一化**：当把 `core.autocrlf` 从 `input` 改为 `true`（或引入 `.gitattributes`）后，Git 可能把全库文件都标记为已修改。此时不要逐个提交，按序执行一次规范化即可 [Configuring Git to handle line endings](https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings)：

```bash
git add -u
git add --renormalize .
git commit -m "normalize line endings"
```

`git add -u` 先暂存已跟踪文件的改动，`git add --renormalize .` 强制按当前换行规则重写全部文件，最后提交一次完成全库换行符统一。

> [!tip] 实践建议
> 把这张速查表当作「排错首页」：先定位现象在哪一行，再对号入座。Windows 的 PATH 与中文乱码、macOS 的 CLT 失效，是两类最高频的启动问题。

### 下一步学习指引

本篇的定位是把 Git「装好、配好、跑通」：双平台安装与验证、首次基础配置、SSH / HTTPS 认证、别名与全局忽略，最后用端到端自检闭环。它刻意没有展开 Git 的核心概念——分支、合并、提交历史、远程协作这些，交给既有笔记 [[Git 入门教程]] 系统讲解（第四章提到配置三层级时，也已指向那里）。

- 想理解「配置层级」全貌、分支与合并、Rebase 与 PR 协作：从 [[Git 入门教程]] 对应章节开始。
- 日常按场景查命令、快速定位：见 [[Git 命令速查]]；进阶 Rebase、Stash、.gitignore：见 [[Git 高级技巧]]。
- 想深入工程化：继续研究 `.gitattributes` 全量规则、Git hooks、子模块（submodule）与 Git LFS。

> [!summary] 全篇总结
> 你已完成：Windows / macOS 任一平台的安装与验证，身份、编辑器、换行符、中文显示等基础配置，SSH 或 HTTPS 认证打通，别名与全局忽略提升日常效率，并用「init → add → commit → remote → push」全流程验证了整条链路。今后遇到的大多数问题，都能在本章速查表找到定位入口。

### 本章小结

- 端到端自检序列：`git init` → `git add .` → `git commit -m "init"` → `git remote add origin <URL>` → `git push -u origin main`，逐行核对预期输出。
- `-u` 一次性绑定本地分支与远程上游，之后 push / pull 免写分支名。
- 速查表覆盖双平台六大高频坑：PATH、`which git` 路径、CLT 失效、换行符重归一化、凭据缓存旧密码、中文乱码。
- 换行符重归一化序列：`git add -u` → `git add --renormalize .` → `git commit`。
- 进阶内容衔接既有 [[Git 入门教程]]，本篇到此收尾。

---

*本笔记由学习笔记工作流（learning-note-flow）生成。*
