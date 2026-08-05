# 第 6 章：排错——「user is not in the sudoers file」（zhq 实战案例）

按第 3 章做完 `usermod -aG sudo`，满心期待地敲下 `sudo whoami`，屏幕却弹出一句 `<user> is not in the sudoers file. This incident will be reported.` 很多人第一反应是「我被系统拉黑了吗」。这句报错是 Debian 上最常见的 sudo 故障。本章用 zhq 的真实排错过程，把它拆开讲清：它到底在说什么、有哪几类根因、按什么顺序查。

## 6.1 错误原文解读

这句话可以拆成两半看：

- `<user> is not in the sudoers file`——sudo 在 `/etc/sudoers`（及 `/etc/sudoers.d/`）里**找不到这个用户的授权**，这是真正的问题描述。
- `This incident will be reported`——只是说「这次失败的提权尝试已被记入本地审计日志」，通常写在 `/var/log/auth.log`。它是**本地日志警告，不是封禁**：系统不会因此拉黑账号或锁死你 [Unix & Linux SE — Debian 12 sudoers 配置坑](https://unix.stackexchange.com/questions/772500/)。

同样「sudo 不可用」还有另外两句常见变体，含义不同，别混为一谈 [RHEL9 — 管理 sudo 访问](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-sudo-access_configuring-basic-system-settings)：

| 错误原文 | 含义 |
| --- | --- |
| `<user> is not in the sudoers file. This incident will be reported.` | **无授权**：用户不在组、或规则缺失 |
| `is not allowed to run sudo on <host>` | **配置未完成**（host 段没匹配上） |
| `Sorry, user ... is not allowed to execute '...' as root on ...` | **命令不在规则中**：用户有 sudo 权限，但这条命令没被授权 |

区分思路：报错越具体，越说明「规则存在但没覆盖到」；而第一句「not in the sudoers file」通常指向「规则压根没有」。

## 6.2 根因清单与排查顺序

三类根因，**先验证、再改配置**，按下面顺序走，不要一上来就改文件 [Unix & Linux SE](https://unix.stackexchange.com/questions/772500/)：

| 步 | 动作 | 目的 |
| --- | --- | --- |
| 1 | `id <用户>` 或 `groups` | 确认已在 `sudo` 组（输出应含 `27(sudo)`） |
| 2 | 注销重登 / `su - $USER` / `newgrp sudo` | 刷新会话组身份 |
| 3 | `sudo visudo` 查 `%sudo ALL=(ALL:ALL) ALL` | 确认授权行存在且未注释 |
| 4 | `sudo -l` | 验证规则生效 |

**根因一：已入组但当前会话未刷新（最常见）**。组身份只在登录时读取，刚加组的旧会话还带着旧身份。先看第 1 步：

```bash
id zhq
# 成功在组：uid=1001(zhq) gid=1001(zhq) groups=1001(zhq),27(sudo)
# 没有 27(sudo)：说明根本没加进组，回头补 usermod -aG sudo zhq
```

输出有 `27(sudo)` 却仍报错，才是会话问题，走第 2 步刷新。

**根因二：sudoers 缺 `%sudo` 授权行或被注释**。入组只是「成为组员」，真正给权限的是 sudoers 里这行 [Debian Wiki — sudo](https://wiki.debian.org/sudo)：

```text
%sudo   ALL=(ALL:ALL) ALL
```

用 `sudo visudo` 打开确认它存在且行首没有 `#`。被注释或缺失，组员身份就毫无用处。

**根因三：`@includedir` 片段干扰**。`/etc/sudoers.d/` 里若有不兼容的片段，可能覆盖主配置；把片段文件暂时改名排除测试。

## 6.3 zhq 案例复盘

zhq 的真实场景是这样：`usermod -aG sudo zhq` 加组、注销重登后 `id` 确认 `27(sudo)` 已在，但 `sudo whoami` 依旧报 `zhq is not in the sudoers file`。按 6.2 逐条走：组没问题、会话已刷新，查到第 3 步——sudoers 里缺 `%sudo ALL=(ALL:ALL) ALL`。此时有两条路：

| 做法 | 示例 | 取舍 |
| --- | --- | --- |
| 加组管理（推荐） | 补上 `%sudo ALL=(ALL:ALL) ALL` 行，维持 `usermod -aG sudo` | 可逆、易审计、可批量撤销；但要先修好配置 |
| 逐用户写规则 | `zhq ALL=(ALL:ALL) ALL` 直接写进 sudoers | 直观、当场生效；绕过组机制、逐人维护麻烦 |

实际排错中 zhq 最终落到了**直接写用户规则**——它能立刻解燃眉之急，但也绕过了「组」这个统一授权层。从审计与撤销的角度，长期应回补 `%sudo` 行、回到加组管理 [RHEL9](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-sudo-access_configuring-basic-system-settings)、[Rackspace](https://docs.rackspace.com/FI/docs/grant-sudo-access-in-debian-and-the-ubuntu-operating-system)。

## 本章小结

- `is not in the sudoers file` 只表示「找不到授权」，`This incident will be reported` 只是本地审计日志警告，不是封禁。
- 三句报错要区分：无授权 / 配置未完成 / 命令不在规则中。
- 排查顺序：验组 → 刷新会话 → 查 `%sudo` 行 → `sudo -l` 验证，先验证再改配置。
- 最常被忽视的根因是「入组了但旧会话没刷新」，先看 `id` 里的 `27(sudo)`。
- 临时直接写 `zhq ALL=(ALL:ALL) ALL` 可用，但长期应回补 `%sudo` 行、回归加组管理。

下一章处理另两类故障：`sudo: command not found` 和 sudoers 文件损坏后的恢复。
