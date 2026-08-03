# 第 2 章：原理基础——su、sudo 与组机制

**结论先行**：第 3 章的标准三步里，第一步 `su -` 和第三步「加 sudo 组」背后各藏一个原理坑——`su` 不带 `-` 会保留一个"脏环境"，导致切到 root 后命令找不到；而 Debian 的授权不是逐用户写规则，而是靠 `sudo` 组批量生效。本章把这两块地基打牢。

## 2.1 `su` 与 `su -`：一个 `-` 决定环境

**结论**：用 `su` 切用户必须带 `-`（即 `su -` / `su --login`）。man 手册明确建议**总是用 `--login`**，避免混合环境副作用 [su(1) manual](https://man7.org/linux/man-pages/man1/su.1.html)。

原因在于两者对环境的处理完全不同：

| 行为 | `su`（非登录 shell） | `su -`（登录 shell） |
|------|---------------------|---------------------|
| 环境变量 | 只设 HOME、SHELL（目标非 root 时再加 USER、LOGNAME），**其余原样保留** | 清空除 TERM 等白名单外的全部变量，重建 HOME/SHELL/USER/LOGNAME/PATH |
| 工作目录 | 不切换 | 切到目标用户主目录 |
| 污染风险 | 调用者的 `LD_PRELOAD`、`LD_LIBRARY_PATH` 会被带进 root 会话 | 无 |

「脏环境」的直接后果是 **PATH 没有重建**。普通用户 PATH 默认只有 `/usr/local/bin:/bin:/usr/bin`，而 root 走 ENV_SUPATH，默认是 `/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin`。系统管理命令（如 `/usr/sbin`、`/usr/local/sbin` 下的工具）在普通用户 PATH 里根本不存在：

```plaintext
# 普通用户 PATH
/usr/local/bin:/bin:/usr/bin
# root PATH（su - 后）
/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
```

这正是「su 切 root 后 apt 找不到」「PATH 没有 /sbin」这类坑的通用根因——第 3 章第一步必须用 `su -`。

## 2.2 `su` 与 `sudo`：切换身份 vs 单条提权

**结论**：日常提权用 `sudo`，不用 `su`。`su` 是**切换身份**——开一个目标用户的交互式 shell；`sudo` 是**以目标身份执行单条命令**，命令跑完就回到原用户 [Debian Wiki — sudo](https://wiki.debian.org/sudo)。

在最小化安装场景，`su` 只是**安装 sudo 的前置手段**：sudo 包还没装，只能先用 root 身份把它装上。

sudo 相比 su 的三个核心优势：

| 能力 | 说明 |
|------|------|
| 凭据缓存 | 默认 15 分钟（`timestamp_timeout`），期间免密重复执行 |
| 审计日志 | 每次提权都被记录，可追溯谁干了什么 |
| 细粒度授权 | 精确到「哪个用户、哪台主机、以谁执行、哪条命令」 |

## 2.3 Debian 的 sudo 组机制

**结论**：Debian 默认不写用户级规则，而是用 `sudo` 组批量授权——**入组即获完整 sudo 权限** [Debian Wiki — sudo](https://wiki.debian.org/sudo)。

- `sudo` 组 GID 为 **27**。
- Debian 默认 sudoers 里已内置一条 `%sudo ALL=(ALL:ALL) ALL`，`%` 前缀表示"组"；所以 `adduser <用户> sudo`（等价 `usermod -aG sudo <用户>`）后，用户自动套上这条完整规则，无需再改 sudoers。
- 验证入组是否成功：`id` / `groups` 输出里应看到 `27(sudo)`。

管理组命名在不同发行版/文档间有差异：

| 发行版 | 管理组 | 备注 |
|--------|--------|------|
| Debian / Ubuntu | `sudo`（GID 27） | 默认 sudoers 已含 `%sudo` 授权行 |
| RHEL 系 | `wheel` | 对应约定，规则格式相同 |
| 旧文档 / 部分镜像 | `admin` | 旧式约定（如 Rackspace 旧文档），现代 Debian 已弃用 |

注意：加组只改 `/etc/group`，**不碰 sudoers**——这也是第 6 章排错时「先验组、再查 `%sudo` 行」顺序的依据。

## 本章小结

- `su` 保留调用者环境、不切目录；`su -` 清环境重建 PATH 并切主目录，切 root 务必用 `su -`。
- root 的 PATH 含 `/usr/sbin`、`/usr/local/sbin`，普通用户没有——「切 root 后命令找不到」的通用根因。
- `su` 切换身份，`sudo` 单条提权；sudo 凭据缓存 15 分钟、有审计日志、支持细粒度授权。
- Debian 用 `sudo` 组（GID 27）配合默认 `%sudo ALL=(ALL:ALL) ALL` 实现「入组即授权」；RHEL 系是 `wheel`，旧文档是 `admin`。
- 加组只改组文件、不写 sudoers；组身份在登录时读取，改完要重新登录才生效。

下一章就动手：`su -` → `apt update && apt install sudo` → `usermod -aG sudo`，三步完成配置并用 `27(sudo)` 与 `sudo whoami` 验证。
