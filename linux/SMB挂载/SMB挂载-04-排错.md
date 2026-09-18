---
title: SMB/CIFS 挂载到 Linux · 第 4 册 排错
tags:
  - SMB
  - CIFS
  - Linux
  - 挂载
  - 排错
  - errno
  - SMB签名
  - 实战笔记
  - SMB挂载
created: 2026-09-18
updated: 2026-09-18
status: 已完成
source_project: smb-cifs-mount-linux
series: SMB/CIFS 共享文件夹挂载到 Linux 服务器
volume: 4/5
---

# 第四章：排错：从错误码回到证据链

> 🧭 分册导航 ｜ 总目录：[[SMB挂载-00-总目录]] ｜ 上一册：[[SMB挂载-03-凭据与开机自动挂载]] ｜ 下一册：[[SMB挂载-05-容器内挂载]]

`mount error(13)` 是这套工具链里最会误导人的一行输出：它看起来像结论，实际上只是入口。数字本身不携带原因，原因分散在三条不同的证据带上——内核日志、同现的 NT 状态码、以及 `mount -vvv` 暴露的实际下发参数。本章按「从现象到证据」的顺序组织，错误码只作为链条上的节点：跑完这条链，你要能判断问题落在认证、网络还是方言协商上，而不是背下一张错误码清单。

> [!note] 核心概念：证据链
> 「证据链」指从现象出发、每一步都落在一个可复现的命令输出上，直到方向被唯一确定。它的反面是「错误码清单」：把 `13` 当结论背下来，换个内核、换个服务器就不适用了。

## 4.1 `mount error(13)` 的完整证据链

### 第零步：先确认共享名真的存在

很多「认证失败」其实是共享名写错。挂载前先用 `smbclient` 列一次服务器上的共享：

```bash
# 在 Debian/Ubuntu 上列出 //server 提供的共享（包名 smbclient，属 Samba 套件）
smbclient -L //server -N
```

`-L` 用于列出服务器上的共享，确认目标共享名存在；当 NetBIOS 名与 DNS 名不一致或跨网段时，补 `-I <ip>`（S17a `-L|--list`）。服务端确实不需要密码时**必须显式加 `-N`**，否则客户端仍会提示输入密码；命令行同时给出密码与 `-N` 时，命令行上的密码会被静默忽略（S17a `-N|--no-pass`）。

如果目标是「是不是以匿名身份进去了」，连上共享后在 `smb:\>` 提示符下执行 `posix_whoami`，它会显示服务端认定的 guest 状态与用户（S17a `OPERATIONS`）。

### 第一步：在内核日志里找到 CIFS 那一行

挂载报错的用户态输出很短，真正的现场记录在内核日志里。红帽 KB 的 Issue 小节记录的现象是 `mount error(13)`，内核侧留下的原文形态是 `CIFS VFS: cifs_mount failed w/return code = -13`（S08 `Issue`）。

```bash
# 查看内核环形缓冲区中的 CIFS 记录
dmesg | grep -i cifs

# 若 dmesg 已被轮转/清空，换 messages 日志
grep -i cifs /var/log/messages
```

期望输出（形态取自 S08 `Issue`）：

```text
CIFS VFS: cifs_mount failed w/return code = -13
```

注意搜的是 `-13` 这种带负号的内核写法，而不是 `13`：内核侧与用户态的这两处数字是同一个现象的两端，只 `grep 13` 很容易漏掉（S08 `Issue`）。

```bash
# journalctl 形态——本笔记素材未收录 journalctl 的手册锚点，
# 此行仅作命令用法出现，不作为官方依据
journalctl -k --since "10 min ago" | grep -i cifs
```

### 第二步：看同现的状态码，它决定方向

这是本章最有价值的一条：如果内核日志里同时出现 `Status code returned 0xc000006d NT_STATUS_LOGON_FAILURE`，方向就是**凭据 / 认证**，而不是网络（S08 `Issue`）。很多人看到 `13` 第一反应是去 ping 服务器，方向从第一步就错了。

> [!warning] 素材的边界
> S08 的 Issue 小节列出的是**伴随** `NT_STATUS_LOGON_FAILURE` 的情形（S08 `Issue`）。如果内核日志里只有 `cifs_mount failed w/return code = -13` 而没有这条 NT 状态码，本笔记素材没有给出进一步的官方判据——此时不要自己补一个结论，继续走第三步取证据。

### 第三步：手工挂载与 `mount -a` 两条路径都复现

S08 的 Issue 小节记录：同一错误在手工挂载与经由 fstab / `mount -a` 两条路径上都出现（S08 `Issue`）。这条对照的意义是把两类怀疑分开：如果问题只出现在开机流程里（例如 `credentials=` 写了相对路径、`~` 未展开，见第 3 章），手工挂载会成功；两边都失败，说明问题在下发的参数本身，与「是否开机」无关。

```bash
# 路径 A：手工前台挂载，看即时输出
mount -t cifs //server/share /mnt/share -o credentials=/root/.smbcred

# 路径 B：按 fstab 走一遍，作为对照
mount -a
```

### 第四步：`mount -vvv` 看实际下发的参数

`mount -vvv` 会打印 `Credential formatted incorrectly: (null)`，并暴露真正传给内核的参数（如 `ver=1`、`prefixpath=DOMAIN/USER`）（S08 `Issue`）。

```bash
mount -t cifs //server/share /mnt/share -o credentials=/root/.smbcred -vvv
```

期望输出（形态取自 S08 `Issue`）：

```text
Credential formatted incorrectly: (null)
...
ver=1
prefixpath=DOMAIN/USER
```

> [!example] 这两行怎么用
> `(null)` 说明凭据没有被解析出内容，`prefixpath=DOMAIN/USER` 说明域与用户名被拼进了路径——这两处都值得回头核对第 3 章的凭据文件语法限制（等号两侧不留空格；域写 `domain=SALES` 而不是 `SALES\`）。这个「回头核对」是排查动作，不是对成因的官方解释：S08 记录的是输出形态本身（S08 `Issue`，并见 S03 `Login errors`）。

## 4.2 errno 名称↔数值对照

在解读任何数字之前先钉死前提：本笔记能确证的只有**符号名↔数值**的硬对应，来自内核 uapi 头文件（S15 `errno-base.h` / `errno.h`）。`mount.cifs(8)` 全文没有任何「`mount error` 后面的数字 = errno 数字」的映射表；本轮素材收集中，cifs-utils 源码的三次抓取均被 HTTP 429 拒绝（02 §六.1）。因此**下文所有数值解读都写作「按 errno 推断」**，不写成官方定义。

| 符号名 | 数值 | 语义 | 来源 |
| --- | --- | --- | --- |
| `ENOENT` | 2 | No such file or directory（无此文件或目录） | S15（硬对应）／S14（语义） |
| `EACCES` | 13 | Permission denied（权限不足） | S15／S14 |
| `EHOSTDOWN` | **112** | Host is down（主机已关闭） | S15／S14 |
| `EHOSTUNREACH` | **113** | No route to host（无路由到主机） | S15／S14 |
| `EINPROGRESS` | **115** | Operation now in progress（操作正在进行） | S15／S14 |
| `EREMOTEIO` | 121 | Remote I/O error（远端 I/O 错误） | S15／S14 |

> [!warning] 112 与 113 不是同一个符号
> `EHOSTDOWN` 是 **112**，`EHOSTUNREACH` 是 **113**（S15）。两个数字相邻、字面相近，是本章最容易记错的一处：把 112 读成「no route to host」会把排查方向带到路由上，而它对应的名称是「host is down」。挂载日志里出现 112 或 115 时，请一律按 errno 推断来表述，并回到 4.1 的第一步取 `dmesg` 证据（02 §八）。

为什么 `errno(3)` 明确不列数值？因为同一个符号名在不同 UNIX 系统与架构上的编号并不相同，手册只保证名称与语义，把数值交给各平台的头文件（S14 `Error numbers and names`）。这也是「背数字」在本主题里格外不可靠的原因。

> [!tip] 大白话
> 把 `mount error(13)` 想成小区保安对你说「你不能进」。这句话只说明**被拒绝**，完全没说清是「你证件不对」（认证问题）还是「门根本锁着」（网络问题）。所以别看到 13 就去 ping 服务器，先去门卫室（`dmesg`）翻当天的登记本，看保安写下的理由是哪一条；登记本上那句 `NT_STATUS_LOGON_FAILURE`，才是「证件不对」的签名。

## 4.3 方言协商的核对方法

「挂上了」不等于「用对了方言」。判断当前连接实际谈成了哪一版，要分两步：先知道默认会谈到哪，再读内核给出的实际结果。

第一步是默认值随内核变化的三档关系（S13 `vers=`）：

| 内核版本 | 未指定 `vers=` 时的行为 |
| --- | --- |
| < 4.13 | 默认 1.0 |
| 4.13 – 4.13.5 | 默认 3.0 |
| ≥ 4.13.5 | 协商 ≥ 2.1 的最高版本 |

第二步是读实际结果：挂载成功后查 `/proc/fs/cifs/DebugData`，可以确认这条连接实际协商到的 Dialect（S13 `vers=`）。

```bash
# 在内核导出的 CIFS 调试信息里找协商结果
# 字段名与取值以本机内核的实际输出为准（本笔记素材未抄录样本输出）
grep -i dialect /proc/fs/cifs/DebugData
```

什么时候才需要显式写 `vers=`？`vers=` 的取值集合是 1.0 / 2.0 / 2.1 / 3.0 / 3.02 / 3.1.1 / 3 / default，不指定即 `vers=default`（S01a `vers=`、S13 `vers=`）；换句话说，只有在服务端是老系统、协商结果不理想时，才需要手工指定（02 §五.4）。旧内核（< 4.13）默认 1.0，是常见失败根因（S13 `vers=`）。

另一头是 Windows 侧的现状：SMBv1 在 Windows 11 与 Server 2019+ 的所有 SKU 中**默认不安装**（S04 开头段）。所以「老服务端只支持 SMB1」这类假设，放到今天的 Windows 共享上基本不成立。

核对挂载本身用 `findmnt`（S17b）：

```bash
# 按挂载点逐级向上回溯查询（-T），或严格匹配挂载点（-M）
findmnt -T /mnt/share
findmnt -M /mnt/share

# 只看 cifs 类型的挂载（-t 过滤时输出会自动切为 list 格式）
findmnt -t cifs
```

判定存在性可以直接读退出码：0 表示有内容可显示，1 表示任何错误（含按过滤条件无匹配、设备或挂载点不存在）（S17b `EXIT STATUS`）。这条在脚本化的排错里比解析输出文本更稳。

## 4.4 Windows 共享连不上时的优先排查方向

优先级只有一句话：**先查签名，而不是先降协议版本**（S04 开头段、S07）。

签名强制是三档，不要合并成一句「Windows 默认要求签名」（S07 `How SMB signing works`）：

| Windows 版本 | 出站签名 | 入站签名 |
| --- | --- | --- |
| Windows 11 24H2 企业版 / 专业版 / 教育版 | 要求 | 要求 |
| Windows Server 2025 | 要求 | 不要求 |
| Windows 11 24H2 家庭版 | 不要求 | 不要求 |

按 S07 的细粒度表述读这张表：Server 2025 要求的是**出站**签名，不要求入站（02 §四.6）。如果只记得「Win11 24H2 / Server 2025 默认要求签名」这种粗粒度说法（S04 开头段），很容易误判方向。

签名机制本身是把整条消息的哈希写入 SMB 头，用于防中继与欺骗（S07 `How SMB signing works`）。当 Linux 客户端连的是不支持签名的第三方 SMB 服务器时，会报 `0xc000a000` / `STATUS_INVALID_SIGNATURE`；**改协议版本不能绕过**（S07 `SMB signing behavior`、S04 开头段）。处置方向是在远端服务器启用签名，而不是关掉客户端签名或降协议（02 §五.10、S04 开头段）——微软明确反对用关闭协议版本或签名来绕过连接失败（S04 开头段）。

在 Windows 侧确认客户端是否要求签名：

```powershell
# Windows PowerShell：查看客户端签名要求（True 即启用）
Get-SmbClientConfiguration | FL RequireSecuritySignature
```

（S07 `Verify SMB signing status`）

还有一条容易漏的连带效应：要求签名会**同时禁用来宾访问**，来宾路径可能报 `0x80070035`（S07 `Disable SMB signing`、`SMB signing behavior`）。也就是说，你在 4.1 里用 `smbclient -N` 能列出的匿名共享，未必能被 Windows 客户端以同样方式访问。

> [!note] 引用 S04 时的版本标注
> S04 页面标注为 2025-03-12；02 记录的探测阶段（`ms.date` 2025-02-28 / updated 2026-09-08）与深读阶段（2025-03-12）两处日期不一致，本章引用一律以页面实际标注的 2025-03-12 为准（02 §四.7）。

## 4.5 两条必须写明的未闭环

排错这一章有两处**不能闭环**，写清楚比补一个漂亮结论更有用。

**其一：`mount error(N)` 的数字是否直接等于 errno。** 未证实。`mount.cifs(8)` 全文没有映射表；cifs-utils 源码三次抓取都被 HTTP 429 拒绝（02 §六.1）。本笔记因此把「`mount.cifs` 直接打印 errno」标为 `[推断]`——能写的是「数值与 errno 的对应关系」，判断时以同现的内核日志为准（S08 `Issue`），不靠数字本身。

**其二：红帽 KB 的 Resolution 步骤在订阅墙后**，不可读（02 §六.2）。本章只引用其 Issue / Environment 可见小节（S08），不补写墙后的处置步骤。

## 4.6 常见坑

> [!warning] 排错时最容易踩的四处
> - **看到 13 就去查网络**：先看内核日志里同现的状态码，`NT_STATUS_LOGON_FAILURE` 指向凭据/认证（S08 `Issue`）。
> - **把 112 记成 `EHOSTUNREACH`**：112 是 `EHOSTDOWN`，`EHOSTUNREACH` 是 113（S15）。
> - **把 errno 数值当官方映射表背**：`errno(3)` 明确不列数值，因为同一符号名在不同 UNIX/架构上编号不同（S14 `Error numbers and names`）。
> - **Windows 连不上先降 `vers=`**：签名才是优先方向，且 `STATUS_INVALID_SIGNATURE` / `0xc000a000` 改协议版本绕不过去（S07 `SMB signing behavior`、S04 开头段）。

## 本章小结

- 排错的主线是证据链：`dmesg` 找 `cifs_mount failed w/return code = -13` → 看同现的 NT 状态码定方向 → 手工挂载与 `mount -a` 两条路径对照 → `mount -vvv` 看实际下发参数（S08 `Issue`）。
- 数值只是节点：`ENOENT`=2、`EACCES`=13、`EHOSTDOWN`=112、`EHOSTUNREACH`=113、`EINPROGRESS`=115、`EREMOTEIO`=121 是硬对应；112 与 113 不是同一个符号，且一切数值解读都按 errno 推断（S15、S14、02 §六.1）。
- 方言要核对而不是猜：默认协商随内核三档变化（<4.13 → 1.0；4.13–4.13.5 → 3.0；≥4.13.5 → 协商 ≥2.1），挂载后读 `/proc/fs/cifs/DebugData` 看实际 Dialect（S13 `vers=`）。
- Windows 连不上先查签名：三档强制粒度不同（Server 2025 要求出站、不要求入站），`0xc000a000` 的处置在远端服务器开签名，不是降协议版本（S07、S04 开头段）。
- 两处不闭环要记住：`mount error(N)` 是否直接等于 errno 仍是推断（源码抓取被 429 拒绝），红帽 KB 的 Resolution 在订阅墙后、本章不补写（02 §六.1、§六.2）。

到这一章为止，共享都挂在宿主机上。如果真正要用这个共享的是容器里的服务，问题会变成另一个样子——下一章（可选小节）把 Docker 论坛里的社区经验摆出来，并给出比「给容器加权限」更稳妥的两条替代路径。

## 本章来源

- **S08** → `mount error(13)` 的证据链四步（`dmesg`/messages 的 `cifs_mount failed w/return code = -13`、同现的 `NT_STATUS_LOGON_FAILURE`、手工挂载与 `mount -a` 双路径复现、`mount -vvv` 的 `Credential formatted incorrectly: (null)` 与 `ver=1`/`prefixpath=DOMAIN/USER`）；红帽 KB 的 Issue 小节。
- **S15** → errno 名称↔数值硬对应表（2/13/112/113/115/121）；112 与 113 非同一符号的易错点。
- **S14** → `errno(3)` 明确不列数值的原因（跨 UNIX/架构编号不同）；表中语义列。
- **S13** → 协商默认随内核变化的三档关系、`vers=` 取值集合、`/proc/fs/cifs/DebugData` 确认 Dialect。
- **S01a** → `vers=` 取值集合与「未指定即 `vers=default`」（与 S13 并列引用）。
- **S17a** → `smbclient -L` / `-N` / `-I` 用法、`posix_whoami` 判定匿名身份。
- **S17b** → `findmnt -T` / `-M` / `-t cifs` 用法与退出码语义（0 = 有内容，1 = 任何错误）。
- **S07** → 签名强制三档粒度、签名机制、`STATUS_INVALID_SIGNATURE` / `0xc000a000`、签名与来宾访问的关联、`Get-SmbClientConfiguration | FL RequireSecuritySignature`。
- **S04** → SMBv1 在 Windows 11 / Server 2019+ 默认不安装；微软反对用关协议/关签名绕过连接失败；页面日期标注 2025-03-12。
- **S03** → 凭据文件语法限制（`Login errors` 小节，作为 `mount -vvv` 输出后的核对方向）。

## 相关笔记

- [[网络协议详解-WebDAV_Samba_FTP_iSCSI]] —— 想换协议栈时，先看这份横向对比

---

> 🧭 分册导航 ｜ 总目录：[[SMB挂载-00-总目录]] ｜ 上一册：[[SMB挂载-03-凭据与开机自动挂载]] ｜ 下一册：[[SMB挂载-05-容器内挂载]]
