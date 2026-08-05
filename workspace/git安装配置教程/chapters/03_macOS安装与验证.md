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
