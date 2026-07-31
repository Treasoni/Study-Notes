# git安装配置教程 - 深度收集结果

收集时间: 2026-07-31
搜索关键词: [Git Windows 安装, Git for Windows PATH, autocrlf/quotepath, macOS brew/xcode-select, SSH key, credential helper, git alias, init.defaultBranch]
信源: 官方文档为主（git-scm.com / GitHub Docs / Pro Git / Homebrew），社区为辅（Microsoft Q&A / Stack Overflow）

---

## 一、Windows 平台安装与配置

### 1. 安装步骤
- **下载**：git-scm.com/download/win → 选 x64 Setup（当前最新 **2.55.x**，2026-07 发布）；另有 ARM64 版与 Portable 便携版。
- **命令行安装**（官方推荐）：`winget install --id Git.Git -e --source winget`；Chocolatey 为社区维护：`choco install git`。
- **安装向导关键选项**（安全默认值）：
  - PATH 选择：**「Git from the command line and also from 3rd-party software」**（任何终端可用 git）
  - 勾选 **Git Bash**（自带 Bash）
  - 默认编辑器可留 vim（或改 VSCode）
  - 符号链接默认关闭（需管理员权限，普通用户不必开）

### 2. 安装后验证
```bash
git --version
```
- 「git 不是内部命令」= PATH 未配好 → 重跑安装程序改 PATH 选项，或手动把 `C:\Program Files\Git\cmd`（和 `bin`）加入系统 PATH，**重开终端**。

### 3. 必须配置项（Windows 特有）
```bash
git config --global core.autocrlf true      # 换行符：提交转 LF、检出转 CRLF
git config --global core.quotepath false    # 中文文件名不转义 \346\265\213
git config --global credential.helper manager  # Git Credential Manager
```
- **换行符**：Windows 用 `true`，macOS/Linux 用 `input`；跨平台仓库在根目录放 `.gitattributes`（首行 `* text=auto`）统一规则。
- **凭据**：Git for Windows ≥2.29 自带 Git Credential Manager（GCM），首次 HTTPS clone 自动弹浏览器 OAuth 登录（支持 2FA），无需手动建 PAT；旧版「GCM for Windows」已废弃。
- **中文乱码**：`core.quotepath false` 让中文文件名正常显示。

### 4. 常见坑清单（Windows）
| 现象 | 原因 | 解决 |
|------|------|------|
| `git` 不是内部命令 | PATH 未配置/未刷新 | 重跑安装器改 PATH，或手动加 `C:\Program Files\Git\cmd`，重开终端 |
| push 反复要密码 | GCM 未启用或版本过旧 | 升级 Git for Windows，确认 `credential.helper manager` |
| 改换行符后整库文件显示被修改 | autocrlf 触发重归一化 | `git add . -u` → `git add --renormalize .` → 提交 |
| 缓存了错误旧密码导致 push 失败 | 凭据管理器存了旧凭据 | 控制面板 → 凭据管理器 → 删除 GitHub 条目后重新认证 |
| 图片等二进制被 git 改坏 | 文本转换误伤二进制 | `.gitattributes` 加 `*.png binary`（binary = `-text -diff`） |

---

## 二、macOS 平台安装与配置

### 1. 三种安装方式对比
| 方式 | 命令 | git 路径 | 优缺点 |
|------|------|----------|--------|
| 官方 .pkg | git-scm.com/download/mac | `/usr/local/git/bin/git` | 独立、较新；升级麻烦，易与 brew 版 PATH 冲突 |
| **Homebrew（推荐）** | `brew install git` | Apple Silicon `/opt/homebrew/bin/git`；Intel `/usr/local/bin/git` | 升级省心（`brew upgrade git`）、生态完整 |
| Xcode CLT | `xcode-select --install` | `/usr/bin/git`（Apple 旧版，约 2.39.x） | 零安装、随系统更新；版本落后，够入门 |

**推荐**：Homebrew 版（升级简单、路径清晰）；偶尔用且不想装 brew 时，CLT 够用。

### 2. 安装后验证
```bash
git --version
which git        # 应指向 brew 路径，不是 /usr/bin/git
```
- PATH 中 `/usr/bin` 常在前 → 把 brew 路径提前：
```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

### 3. 首次使用注意
- CLT：`xcode-select --install` 触发图形安装；全量 Xcode 需 `sudo xcodebuild -license accept`。
- **CLT 失效修复链**：
```bash
xcode-select --install
sudo xcode-select --reset
sudo xcode-select --switch /Library/Developer/CommandLineTools
# 仍失败：sudo rm -rf /Library/Developer/CommandLineTools 后重装
xcode-select -p   # 验证
```
- **凭据**：`git config --global credential.helper osxkeychain`（macOS 默认即此值）；GitHub 已禁密码认证，prompt 时输入 **PAT**。

### 4. 常见坑清单（macOS）
| 现象 | 原因 | 解决 |
|------|------|------|
| `which git` 仍是 `/usr/bin/git` | PATH 顺序 | brew 路径加到最前；或 `brew link git --overwrite` |
| `xcrun: invalid active developer path` | CLT 缺失/损坏 | 按修复链依次执行，最后 `xcode-select -p` 验证 |
| `git-credential-osxkeychain: command not found` | helper 不在 PATH | 用 brew 版 git（自带），或用 `/usr/bin/git-credential-osxkeychain` |
| push 反复要密码 | 没用 PAT | 生成 PAT 作为密码输入（非账户密码） |

---

## 三、通用基础配置（首次配置）

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor code --wait     # 或 vim；Windows 需完整路径
git config --global init.defaultBranch main      # 2.28+，新库默认 main
```

### 配置三层级
| 级别 | 作用范围 | 文件 | 命令 |
|------|----------|------|------|
| system | 整台电脑 | `[path]/etc/gitconfig` | `git config --system` |
| global | 当前用户 | `~/.gitconfig` | `git config --global` |
| local | 当前仓库 | `.git/config` | `git config`（默认） |

优先级：**local > global > system**。

### 查看配置
```bash
git config --list --show-origin    # 列出全部配置及来源文件
git config user.name               # 查单个键
git config --show-origin user.name # 查最终值来自哪个文件
```

---

## 四、认证

### 1. SSH 认证完整流程
```bash
ssh-keygen -t ed25519 -C "you@example.com"   # 回车默认路径，可设 passphrase
# 旧系统备用：ssh-keygen -t rsa -b 4096 -C "you@example.com"
```
- 公钥添加到 GitHub（Settings → SSH and GPG keys → New SSH key）或 GitLab；**只贴 `.pub` 文件内容**。
- **macOS**：
```bash
eval "$(ssh-agent -s)"
# ~/.ssh/config 加入：
#   Host github.com / AddKeysToAgent yes / UseKeychain yes / IdentityFile ~/.ssh/id_ed25519
ssh-add --apple-use-keychain ~/.ssh/id_ed25519   # Monterey 前用 -K
```
- **Windows**（管理员 PowerShell）：
```powershell
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent
ssh-add c:/Users/YOU/.ssh/id_ed25519
```
- 若 `git push` 仍反复要 passphrase → 强制用系统 OpenSSH：
```bash
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
```
- **验证**：`ssh -T git@github.com` → `Hi <username>! You've successfully authenticated...` 即成功。
- GitHub 已于 2022-03-15 弃用 DSA；RSA 需 SHA-2 签名。

### 2. HTTPS + 凭据管理
- **选型**：HTTPS URL（`https://github.com/user/repo.git`）通用、防火墙友好、用 PAT；SSH URL（`git@github.com:user/repo.git`）需先配密钥。port 22 被墙可改用 SSH over HTTPS 443。
- **remote 操作**：
```bash
git remote add origin <REMOTE_URL>
git remote set-url origin <新URL>   # HTTPS↔SSH 切换
git remote -v
```
- **凭据**：Windows → GCM（`credential.helper manager`）；macOS → 钥匙串（`credential.helper osxkeychain`）；HTTPS 一律用 PAT。

---

## 五、别名与全局配置

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'   # git unstage fileA
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'            # ! 开头执行外部命令
git config --global core.excludesFile ~/.gitignore_global
```
- `~/.gitignore_global` 写通用忽略（`.DS_Store`、`Thumbs.db`、`*.log` 等）。

---

## 六、信源清单（粗筛）

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | Git for Windows 官方下载页 | https://git-scm.com/download/win | 5/5 | 官方 |
| 2 | Configuring Git to handle line endings | https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings | 5/5 | 官方 |
| 3 | Pro Git — Installing Git | https://git-scm.com/book/en/v2/Getting-Started-Installing-Git | 4/5 | 官方 |
| 4 | Why the git command is unknown in PowerShell | https://learn.microsoft.com/en-us/answers/questions/2032440 | 4/5 | 社区 |
| 5 | git-config 官方手册 | https://git-scm.com/docs/git-config | 4/5 | 官方 |
| 6 | git-scm 官方下载页 macOS | https://git-scm.com/download/mac | 5/5 | 官方 |
| 7 | Homebrew git 公式页 | https://formulae.brew.sh/formula/git | 5/5 | 官方 |
| 8 | Caching your GitHub credentials in Git | https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git | 5/5 | 官方 |
| 9 | Command Line Tools not working (xcrun 修复) | https://stackoverflow.com/questions/32893412 | 5/5 | 社区 |
| 10 | Pro Git — First-Time Git Setup | https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup | 5/5 | 官方 |
| 11 | Generating a new SSH key | https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent | 5/5 | 官方 |
| 12 | About remote repositories (HTTPS vs SSH) | https://docs.github.com/en/get-started/git-basics/about-remote-repositories | 4/5 | 官方 |
| 13 | Pro Git — Git Aliases | https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases | 4/5 | 官方 |

---

## 七、综合分析

- **平台差异集中在安装环节**（Windows 安装器/winget vs macOS brew/pkg/CLT）；配置与认证基本通用，可合并章节。
- **必备章节骨架建议**：
  1. 安装前须知（版本、包管理器、平台选型）
  2. Windows 安装（向导 + winget + 验证 + 坑）
  3. macOS 安装（三种方式对比 + 验证 + CLT 排错 + 坑）
  4. 首次基础配置（三层级 + user/email/editor/init.defaultBranch）
  5. 认证（SSH 全流程 + HTTPS/PAT + 凭据，含双平台差异）
  6. 实用别名与全局 .gitignore
  7. 验证总检 + 常见问题速查
- **必写的坑**：Windows PATH 未生效、autocrlf 换行符、中文乱码、GCM；macOS CLT 失效、which git 路径、osxkeychain、PAT。
- **素材质量**：官方文档 11/13，社区 2/13；覆盖安装/配置/认证/排错全闭环，足以支撑章节写作。
