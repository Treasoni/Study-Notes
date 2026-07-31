## 学习笔记大纲：《Git 安装配置教程》

> 笔记类型：实战笔记
> 预计总篇幅：约 7000-8000 字
> 章节数：7（第 1 章准备 / 第 2-3 章双平台安装 / 第 4-6 章配置与认证 / 第 7 章收尾）
>
> 定位说明：与 vault 内既有 `Git 入门教程.md` 互补，聚焦「平台化安装步骤 + 基础配置闭环」。配置层级（system/global/local）只做一句话速览并指向既有笔记，不展开。

### 第一章：安装前的准备与平台选型
- **篇幅**：短（约 500 字）
- **覆盖要点**：本篇定位与阅读路径（与既有笔记互补关系）、Git 版本现状（2.55.x）与获取渠道、双平台安装策略总览对照表（Windows → Git for Windows；macOS → 推荐 Homebrew）
- **素材引用**：一、二、七
- **代码示例**：无（仅给出安装完成后预期的 `git --version` 输出示例作对照）

### 第二章：Windows 安装与验证
- **篇幅**：中（约 1100 字）
- **覆盖要点**：图形安装向导关键选项（PATH 三选、Git Bash、默认编辑器、符号链接）、命令行安装（winget 官方推荐 / Chocolatey）、安装后验证、PATH 未生效排查（「不是内部命令」）、Windows 安装常见坑
- **素材引用**：一、七
- **代码示例**：
  - `winget install --id Git.Git -e --source winget`
  - `choco install git`
  - `git --version`
  - 手动 PATH 添加说明（`C:\Program Files\Git\cmd`）

### 第三章：macOS 安装与验证
- **篇幅**：中（约 1100 字）
- **覆盖要点**：三种安装方式对照表（官方 pkg / Homebrew / Xcode CLT 的路径与优缺点）、推荐路线（Homebrew）、PATH 顺序修正、验证（`git --version` + `which git`）、CLT 失效修复链、macOS 安装常见坑
- **素材引用**：二、七
- **代码示例**：
  - `brew install git`
  - `echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc`
  - `git --version`、`which git`
  - `xcode-select --install`、`sudo xcode-select --reset`、`sudo xcode-select --switch /Library/Developer/CommandLineTools`、`xcode-select -p`

### 第四章：首次基础配置（通用 + 双平台差异）
- **篇幅**：中（约 1200 字）
- **覆盖要点**：身份信息（user.name / user.email）、默认编辑器与默认分支（core.editor / init.defaultBranch）、配置三层级一句话速览（指向既有笔记）、换行符双平台对照（autocrlf：Windows=true / macOS=input，.gitattributes 跨平台仓库规则）、中文文件名显示（core.quotepath false）、查看配置（--list --show-origin）
- **素材引用**：一、三、七
- **代码示例**：
  - `git config --global user.name "Your Name"`
  - `git config --global user.email "you@example.com"`
  - `git config --global core.editor code --wait`
  - `git config --global init.defaultBranch main`
  - `git config --global core.autocrlf true`（Windows）/ `input`（macOS）
  - `git config --global core.quotepath false`
  - `git config --list --show-origin`
  - `.gitattributes` 片段（`* text=auto`、`*.png binary`）

### 第五章：认证配置——SSH 与 HTTPS
- **篇幅**：长（约 1800 字）
- **覆盖要点**：认证协议选型对照（SSH vs HTTPS）、SSH 密钥生成（ed25519 主 / RSA 备用）、公钥添加至 GitHub / GitLab、SSH Agent 配置（双平台分小节：macOS 钥匙串 / Windows OpenSSH 服务）、连接验证（ssh -T）、HTTPS + 凭据助手（双平台对照：Windows GCM / macOS osxkeychain、PAT）、remote URL 切换（HTTPS ↔ SSH）
- **素材引用**：四、七
- **代码示例**：
  - `ssh-keygen -t ed25519 -C "you@example.com"`
  - macOS：`eval "$(ssh-agent -s)"`、`ssh-add --apple-use-keychain ~/.ssh/id_ed25519`、`~/.ssh/config` 片段
  - Windows：`Get-Service -Name ssh-agent | Set-Service -StartupType Manual`、`Start-Service ssh-agent`、`ssh-add c:/Users/YOU/.ssh/id_ed25519`
  - `git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"`
  - `ssh -T git@github.com`
  - `git config --global credential.helper manager` / `osxkeychain`
  - `git remote add origin <URL>`、`git remote set-url origin <新URL>`、`git remote -v`

### 第六章：实用别名与全局忽略
- **篇幅**：短（约 700 字）
- **覆盖要点**：常用别名（co / br / ci / st / unstage / last）、外部命令别名（visual）、全局 .gitignore（core.excludesFile + 通用忽略示例）
- **素材引用**：五、七
- **代码示例**：
  - `git config --global alias.co checkout`、`alias.br branch`、`alias.ci commit`、`alias.st status`
  - `git config --global alias.unstage 'reset HEAD --'`
  - `git config --global alias.last 'log -1 HEAD'`
  - `git config --global alias.visual '!gitk'`
  - `git config --global core.excludesFile ~/.gitignore_global`
  - `~/.gitignore_global` 内容片段（`.DS_Store`、`Thumbs.db`、`*.log`）

### 第七章：收尾验证与常见问题速查
- **篇幅**：中（约 900 字）
- **覆盖要点**：端到端自检流程（新建仓库 → add → commit → remote → push）、双平台常见问题速查表（PATH 未生效、CLT 失效、换行符重归一化、凭据缓存、中文乱码）、下一步学习指引（衔接既有《Git 入门教程.md》）
- **素材引用**：一、二、四、七
- **代码示例**：
  - `git init`、`git add .`、`git commit -m "init"`、`git remote add origin <URL>`、`git push -u origin main`
  - 换行符重归一化序列：`git add -u` → `git add --renormalize .` → `git commit`

---

## 学习路径说明

### 前置要求
- 会打开和使用终端（Windows 的 PowerShell / cmd，或 macOS 的 Terminal）
- 已了解 add / commit 基本概念（不需要系统安装配置过 Git）
- 有一个 GitHub 或 GitLab 账号（认证章节需要用到）

### 学完能做什么
- 在 Windows 或 macOS 上完成 Git 安装并通过验证
- 完成一套最小但完整的全局配置（身份、编辑器、换行符、中文显示）
- 配置 SSH 或 HTTPS 认证，能正常 clone / push / pull 远程仓库
- 用别名和全局 .gitignore 提升日常使用效率
- 遇到 PATH、CLT 失效、凭据、换行符等常见问题能自主排查

### 建议学习顺序
- 按章节顺序通读，约 1-2 小时
- 只用 Windows：第 2、4、5、6 章为核心，第 3 章可跳过
- 只用 macOS：第 3、4、5、6 章为核心，第 2 章可跳过
- 第 7 章速查表建议收藏，作为日常排错入口
