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
