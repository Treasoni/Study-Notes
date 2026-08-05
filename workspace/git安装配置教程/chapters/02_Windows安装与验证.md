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
