---
title: SMB/CIFS 挂载到 Linux · 第 3 册 凭据与开机自动挂载
tags:
  - SMB
  - CIFS
  - Linux
  - 挂载
  - fstab
  - systemd
  - 凭据管理
  - 实战笔记
  - SMB挂载
created: 2026-09-18
updated: 2026-09-18
status: 已完成
source_project: smb-cifs-mount-linux
series: SMB/CIFS 共享文件夹挂载到 Linux 服务器
volume: 3/5
---

# 第三章：凭据文件与开机自动挂载

> 🧭 分册导航 ｜ 总目录：[[SMB挂载-00-总目录]] ｜ 上一册：[[SMB挂载-02-手动挂载]] ｜ 下一册：[[SMB挂载-04-排错]]

手动挂载能用了，接下来要解决两个新问题：密码不能再出现在命令行和 `/etc/fstab` 里，以及——服务器重启时，如果共享端没开机、网络还没起来，你的机器会不会卡在开机界面。这一章先把凭据收进一个权限正确的文件，再逐层拆开 systemd 处理网络挂载的开机顺序，最后给出服务器离线时的三条回落路线。

## 3.1 凭据文件规范

**第一条原则：不要把密码写进 `/etc/fstab`。** 理由很直接——fstab 是人人可读的；正确做法是密码放进凭据文件，再 `chmod 600`（S03 `Create a credentials file`、S05）。社区帖 S10 里那种把 `password` 明文写进 fstab 的做法，就是本章通篇要你避开的反面示例（S10，[社区]）。

凭据文件的内容如下（三行，等号两侧不留空格）：

```ini
# /root/.smbcred
username=smbuser
password=your-password-here
domain=SALES
```

权限与属主：

```bash
# 文件 600，属主 root:root；存放目录建议 700（S06 Storing share passwords）
sudo chmod 600 /root/.smbcred
sudo chown root:root /root/.smbcred
sudo chmod 700 /root
```

两条语法硬约束（S03 `Login errors`）：

- **等号两侧不能有空格**：写 `password=x`，不能写 `password = x`。
- **域写在 `domain=` 键里**，而不是塞进用户名：写 `domain=SALES`，不要写成 `SALES\username` 那种形式。

一条容易被忽略的路径约束：**fstab 里的 `credentials=` 必须写绝对路径，`~` 不会被展开**（S05 `Use of tilde in pathnames`）。这条出自 S05 的 2008 年段落，但结论至今仍有效——systemd 解析 fstab 时不会替你做 shell 的波浪号展开。注意 S05 是官方 wiki，**部分内容陈旧**（含 2008/9.04/12.04 遗留），引用时以此为前提。

[缺口] 还有一个版本边界要记住：`password2=` 键在 **7.4-1（trixie）** 中受支持，但在 **7.0-2（bookworm）** 上**超出该版本文档范围**，只有 `username`/`password`/`domain` 三项（S01a / S01b `credentials=`、`02_deep_research.md` §四.8）。以 Debian 12 为目标时，别用 `password2=`。

### 3.1.1 三个键分别填什么（FNOS / Windows 对照）

三行里最常填错的是 `username`：**它是共享端（SMB 服务器）上的账号，不是这台 Linux 的本地用户**。三个键的值都来自共享端，一个都不来自挂载端。

| 键 | 填什么 | 怎么查到 |
| --- | --- | --- |
| `username` | 共享端上的账号 | Windows：平时映射网络驱动器用的那个账号；FNOS：NAS 后台建的**共享用户**（不是 NAS 管理员账号） |
| `password` | 该账号的密码，明文（所以必须 `chmod 600`） | — |
| `domain` | 域环境填 AD 域名；非域环境填工作组名或共享端机器名 | Windows：cmd 里 `echo %USERDOMAIN%`；FNOS：后台「文件服务 / SMB」里的工作组名 |

在 Windows 侧一次把两个值查齐：

```cmd
whoami
echo %USERDOMAIN%
```

`whoami` 的输出形如 `DESKTOP-ABC\zhq`，**反斜杠后面那半截**就是 `username=`；`echo %USERDOMAIN%` 的输出就是 `domain=`。

> [!warning] 两条是实操惯例，本笔记没有为它们挂来源
> 1. **非域环境**的 `domain` 填 `WORKGROUP`、共享端机器名，或整行删掉——这是通行做法，素材中没有对应的官方锚点（FNOS 默认值相关的问题本来就在「已知缺口」里，见 `02_deep_research.md` §六.5）。
> 2. **用微软账号登录的 Windows**，`%USERDOMAIN%` 常显示为 `MicrosoftAccount`，照抄即可，同样无来源支撑。
>
> 之所以不用 `[社区]`/`[缺口]` 标记：这两条既不是社区帖里的说法，也不属于「素材未覆盖、正文不写」，而是本节新增的实操惯例，故以文字声明其来源状态。

填完先用手工挂载验证，成功了再写 fstab（fstab 行见 3.3）：

```bash
sudo chmod 600 /root/.smbcred && sudo chown root:root /root/.smbcred

# 手工试挂（//服务器/共享名 换成自己的）
sudo mount -t cifs //server/share /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8
```

注意这里 `uid`/`gid` 填的是**挂载端**的本地用户（`id -u` / `id -g` 的输出，第一个普通用户通常是 `1000`），与上面三个「来自共享端」的键方向相反；不填则默认 `0`（见第 2 册 2.4.1）。

## 3.2 凭据文件的解析限制

凭据文件不是万能容器，它有两个已记录的解析限制（S01a `BUGS`，7.0-2 与此一致）：

1. **以空格开头的用户名或密码不被处理**。你的密码如果以空格打头，写进凭据文件不会得到你想要的结果（S01a `BUGS`）。
2. **含逗号的密码不能写在 `-o password=` 里**，会解析失败。可用的路径有三条：写进凭据文件、用 `PASSWD` 环境变量、或改成交互式输入（S01a `BUGS`）。

```bash
# 含逗号密码的可用路径之一：凭据文件（内容见 3.1）
sudo mount -t cifs //server/share /mnt/share -o credentials=/root/.smbcred

# 路径之二：PASSWD 环境变量
sudo PASSWD='pa,ss' mount -t cifs //server/share /mnt/share -o username=smbuser

# 路径之三：交互输入（不给 password= 时由 mount.cifs 提示）
sudo mount -t cifs //server/share /mnt/share -o username=smbuser
```

## 3.3 `/etc/fstab` 行写法

Ubuntu 官方文档给出的最小示例，形态是**只有 `credentials=` 加结尾的 `0 0`**，完全没有 `_netdev`/`nofail`/`x-systemd.*` 这些选项（S03 `Mount password-protected network folders`）。而且该文档**自承**：服务器离线时，开机可能报错（S03 `Mount password-protected network folders`）。

```ini
# /etc/fstab —— 官方最小形态：只有 credentials= 和结尾 0 0
//server/share  /mnt/share  cifs  credentials=/root/.smbcred  0  0
```

要写完整一点、覆盖开机场景时，本笔记采用的形态是（`02_deep_research.md` §五.3）：

```ini
# /etc/fstab
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8,_netdev,nofail  0  0
```

几个写法细节：

- **路径含空格写成 `\040`**（S03 `Mount unprotected (guest) network folders`、S06 `As mount entry`）。fstab 用空格分隔字段，所以路径里的空格必须转义。
- **让普通用户挂载要用 `users`（复数）**，其他文件系统才是 `user`（S06 `As mount entry`）。
- 改完 fstab 先校验再重启：`findmnt --verify` 会检查 fstab 的**可解析性与可用性**，加 `--verbose` 可看细节；`-s` 用于在 `/etc/fstab` 中搜索条目（S17b `-x|--verify`、`-s|--fstab`）。

```bash
# 改完 fstab 先校验可解析性，再考虑重启
sudo findmnt --verify --verbose
```

> [!warning] `--verify` 不验证远端共享能不能挂上
> `findmnt --verify` 原文只说校验 "parsability and usability"，**未列具体检查项**；它**不会**替你验证远端共享是否真的能挂上（S17b `-x|--verify` → [推断]）。所以通过校验不等于挂载会成功，别把它当验收。

## 3.4 开机顺序机制

fstab 里的条目会被 systemd 生成挂载单元，而 systemd 对「网络挂载」有一整套默认依赖安排。先看默认行为：

**网络挂载单元会自动获得**以下依赖关系——`After=remote-fs-pre.target`、`network.target`、`network-online.target`，以及 `Before=remote-fs.target`（并带相应的 `Wants=`）；**除非你设了 `nofail`**（S02 `Default Dependencies`，systemd 252.36）。

**`_netdev` 的作用是「覆盖」按 fstype 的自动判定**：它让该挂载被排在 `remote-fs-pre` → `remote-fs` 之间，并 pull in `network-online.target`（S02 `_netdev`）。

[推断] 这里有一个必须标为推断的点：**「cifs 会被 systemd 自动识别为网络挂载、因而 `_netdev` 可能冗余」这个说法没有一手依据**。`systemd.mount(5)` 只说「按文件系统类型规范区分」，**全文未出现 cifs/smbfs**（`02_deep_research.md` §六.3）。所以：**`_netdev` 用不用，属于 `[推断]` 层面的选择**，不要当成官方定论。

**`nofail` 的语义**：它让该挂载**只 wanted、不 required**，并且**不再被排到 target 之前**，于是服务器离线时开机可以继续走过去（S02 `nofail`）。

[推断] 关于 `nofail`「取消依赖」的粒度，`02_deep_research.md` §六.4 明确要求：**只写「取消 required 身份与 target 排序」，不逐条断言它到底取消了哪几条依赖**。原因是 systemd 252 与 257/262 的措辞不同（后者扩为 `nofail`/`x-systemd.wanted-by=`/`x-systemd.required-by=`），原文从未逐条说明（`02_deep_research.md` §六.4）。本笔记严格按这个粒度写。

把三个选项的分工整理成一张对照表：

| 选项 | 它解决的问题 | 代价 / 边界 |
| --- | --- | --- |
| `_netdev` | 明确声明这是网络挂载，覆盖按 fstype 的自动判定（S02 `_netdev`） | 「cifs 是否已被自动判定为网络挂载」本身无一手依据（`[推断]`，§六.3） |
| `nofail` | 服务器离线时开机不卡住，挂载只 wanted 不 required，且不再排到 target 之前（S02 `nofail`） | 精确取消了哪几条依赖原文未逐条说明（§六.4）；关机阶段存在社区报告的顺序问题（见 3.5.4） |
| `noauto` + `x-systemd.automount` | 彻底改成按需挂载，不用等开机（S02 `noauto, auto`） | 此时 `auto`/`noauto` 均失效，target 依赖由 automount 单元接管（S02 `noauto, auto`）；另有社区报告的 90 秒等待问题（见 3.5.4） |

> [!tip] 大白话
> 把开机想成早上给一整栋楼开门：
> **`_netdev`** 是跟门卫说「这间屋子要等网络线路通了才进去检查」——只是**调整做事顺序**。
> **`nofail`** 是说「这间屋子检查不了就先跳过，别把整栋楼的门都堵着不让开」——**降低这间屋子的重要性**。
> **`noauto` + `x-systemd.automount`** 更彻底：**早上压根不查这间屋子**，谁要进去谁再刷门禁卡现开——把「开机时做」改成「用时才做」。
> 三者不是叠加越多越好：它们各自换来的代价写在右列，选哪个取决于是「顺序不对」「怕卡住」还是「根本不想在开机时做」。

## 3.5 服务器离线时的回落路线

### 3.5.1 `noauto` + 登录后挂载

官方文档给出的**唯一**回落策略是：加 `noauto`，把挂载从开机阶段改到登录后（或改用 libpam-mount）（S03 `Mount after login instead of boot`；S05 同）。

```ini
# /etc/fstab —— noauto：开机不挂，登录后手动 mount
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,noauto  0  0
```

```bash
# 登录后手动挂上
sudo mount /mnt/share
```

### 3.5.2 `noauto` + `x-systemd.automount`

更彻底的做法是改用 systemd 原生的按需挂载：`noauto` 配合 `x-systemd.automount`（S02 `noauto, auto`、S06、S09）。

```ini
# /etc/fstab —— 按需挂载：访问挂载点时才真正挂载
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,noauto,x-systemd.automount  0  0
```

关键约束：**使用 `x-systemd.automount` 时，`auto`/`noauto` 均失效**，target 依赖由 automount 单元接管（S02 `noauto, auto`）。也就是说这个组合里的 `noauto` 不再按字面意义起作用，挂载时机完全由 automount 单元决定。

### 3.5.3 必须写明的事实：官方指南未覆盖 systemd 原生做法

这一点不能含糊：**Ubuntu 官方文档全文未提 `x-systemd.automount`**（S03 全文未提，`02_deep_research.md` §四.5）。所以 3.5.2 的做法虽然更彻底，但它**不是官方指南给出的路线**——官方给的只有 3.5.1。两条路线并列呈现，读者自行取舍（`02_deep_research.md` §四.5）。

### 3.5.4 `[社区]` 两条附带报告

以下两条来自 systemd-devel 邮件列表的一封**提问帖**，**原帖归档后没有任何回复**，属于**未获上游确认的用户报告**（S09，secondary）：

- 带 `nofail` 的挂载，在关机时可能在 `After=*-fs.target` 的服务停止**之前**就被卸载，导致这些服务挂起甚至数据丢失；原帖举的例子是 qBittorrent + CIFS。发帖人的建议是改用 `noauto` + `x-systemd.automount`（S09）。
- `x-systemd.automount` 虽然规避了 `nofail` 的问题，但当**服务器不可达时默认停 90 秒**，如果在开机期触发，可能造成永久挂起（S09）。

> [!warning] 证据强度说明
> 上面两条**均为未获上游确认的用户报告**（原帖是提问，无任何回复），**不能当作 systemd 的既定行为**。它们只说明「有人报告过这个现象」，是否复现取决于你的环境。

## 3.6 限制单次等待时间：`x-systemd.mount-timeout=`

这个选项用于配置 **systemd 等待 `mount` 命令完成的时长**，超时即放弃该 fstab 条目（S02 `x-systemd.mount-timeout=`）。

关于它的存在性与引入版本（S02）：

- 选项**存在且长期存在**，`Added in version 233`，在 257 / 262 / 252 三版中均有定义（S02 `x-systemd.mount-timeout=`）。
- 但要注意：**bookworm 页面不显示 `Added in version` 标注行**。所以「这个选项何时引入」的判定，在 bookworm 页上只能靠三版对照得出（`02_deep_research.md` §七.2 也记录了这类标注行「存在性因文档而异」的规律）。

**最关键的约束：它只能写在 `/etc/fstab`。写进单元文件的 `Options=` 会被忽略**（S02 `x-systemd.mount-timeout=`）。

```ini
# /etc/fstab —— 只等 30 秒，超时放弃该条目
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,_netdev,nofail,x-systemd.mount-timeout=30  0  0
```

超时之后发生什么？实际行为落在 `TimeoutSec=` 上：该挂载被视为失败并被关闭，流程是 SIGTERM → 再等同样长的时间 → SIGKILL；默认值取自 `DefaultTimeoutStartSec=`（S02 `TimeoutSec=`）。

还要区分一个名字相近但作用不同的选项：`x-systemd.device-timeout=` 管的是**「等设备出现」**，与 `mount-timeout` 不是一回事（S02）。

## 3.7 按需挂载的其余相关选项

- **`x-systemd.idle-timeout=`**：配置 automount 的空闲超时，对应单元侧的 `TimeoutIdleSec=`（S02 `x-systemd.idle-timeout=`）。
- **`x-systemd.requires=`**：同时建立 `Requires=` 与 `After=` 两种依赖；而 `x-systemd.before=` / `x-systemd.after=` **只建排序**（S02 `x-systemd.requires=`）。

```ini
# /etc/fstab —— 按需挂载 + 空闲 10 分钟后卸载
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,noauto,x-systemd.automount,x-systemd.idle-timeout=10  0  0
```

值得注意的一点：man page **明说**这三个选项适合处理**带 `nofail` 的异步挂载**的排序问题（S02 `x-systemd.requires=`）。也就是说，官方给它们的使用场景描述里，「配合 `nofail` 使用」是被点名的。

## 3.8 其他：`guest` 在开机挂载中的可靠性

这个问题存在一份**互相冲突**的材料，按 `02_deep_research.md` §四.3 并列呈现：

| 说法 | 出处 | 具体内容 |
| --- | --- | --- |
| `guest` 可行 | S03 | 把 `guest,uid=1000` 当作可行做法（S03 `Mount unprotected (guest) network folders`） |
| `guest` 开机不挂载 | S05 | 报告称 guest 在开机时不挂载，但 `mount -a` 却成功；改用 `username=guest,password=` 后解决 |

[社区] 关于 S05 那一条，必须**注明「报告者自认无法解释原因」**（`02_deep_research.md` §四.3）——它是一个现象报告，不是一个有机制解释的结论。另外 S05 为官方 wiki 且**部分内容陈旧**，引用时同样要带这个前提。

## 3.9 常见坑

> [!warning] fstab 与凭据的五个高频坑
> 1. **密码写进 `/etc/fstab`**：fstab 人人可读，必须改用凭据文件 + `chmod 600`（S03 `Create a credentials file`、S05）。
> 2. **凭据文件里等号两侧留了空格**：`password = x` 不生效，必须写 `password=x`；域要写 `domain=SALES`，不能写成 `SALES\username`（S03 `Login errors`）。
> 3. **fstab 里 `credentials=` 用了 `~`**：不会展开，必须写绝对路径（S05 `Use of tilde in pathnames`）。
> 4. **以为 `x-systemd.mount-timeout=` 写哪都行**：只能写在 `/etc/fstab`，写进单元文件的 `Options=` 会被忽略（S02 `x-systemd.mount-timeout=`）。
> 5. **以为加了 `nofail` 就万事大吉**：它解决的是开机不被卡住（S02 `nofail`），但关机阶段的顺序问题有社区报告，且 `x-systemd.automount` 路线在服务器不可达时有 90 秒等待的报告（均为未获上游确认的用户报告，S09）。

## 本章小结

- 凭据文件的规范是：等号两侧不留空格、域写 `domain=`、目录 700 / 文件 600 / 属主 `root:root`，fstab 中必须写绝对路径（S03、S05、S06）。
- 两个解析限制：以空格开头的用户名或密码不被处理；含逗号的密码不能用 `-o password=`，要走凭据文件 / `PASSWD` / 交互输入（S01a `BUGS`）。
- Ubuntu 官方最小 fstab 形态只有 `credentials=` + `0 0`，且**自承服务器离线时开机可能报错**；官方给的唯一回落策略是 `noauto` + 登录后挂载（S03）。
- 开机顺序三件套的分工：`_netdev` 覆盖按 fstype 的自动判定；`nofail` 让挂载只 wanted 不 required 且不再排到 target 之前；`noauto` + `x-systemd.automount` 改成按需挂载（此时 `auto`/`noauto` 均失效）（S02）。
- `x-systemd.mount-timeout=` 存在且长期存在（`Added in version 233`），**只能写在 fstab**；超时后的行为落在 `TimeoutSec=`（S02）。
- 两处证据强度提醒：`_netdev` 对 cifs 是否冗余属 `[推断]`（§六.3）；`nofail` 关机顺序与 automount 90 秒等待是未获上游确认的用户报告（S09）。

下一章换一个方向：不再追求「挂上」，而是当它挂不上时，怎么从错误码一步步回溯到证据。我们会从 `mount error(13)` 的完整证据链讲起，并纠正一个普遍误解——`13` 表示「被拒绝」，不等于「网络不通」。

## 本章来源

| SID | 本章用途 |
| --- | --- |
| S01a | 凭据文件解析限制（`BUGS`：空格开头、含逗号密码）；`password2=` 的版本边界（7.4-1） |
| S01b | 7.0-2 的 `credentials=` 键集合（`password2=` 超出该版本文档范围） |
| S02 | 网络挂载默认依赖（252.36）；`_netdev`；`nofail`；`noauto, auto` 与 `x-systemd.automount`；`x-systemd.mount-timeout=` 与 `Added in version 233`；`TimeoutSec=`；`x-systemd.device-timeout=`；`x-systemd.idle-timeout=`；`x-systemd.requires=` |
| S03 | 凭据文件与 `chmod 600`；`Login errors`；fstab 最小形态与其离线自承；`noauto` 回落；`guest,uid=1000` |
| S05 | `~` 不展开（2008 年段落，官方 wiki 部分内容陈旧）；`guest` 开机挂载失败报告；`noauto` 回落 |
| S06 | 凭据文件权限建议；`\040`；`users` 复数；`x-systemd.automount` |
| S09 | `nofail` 关机乱序与 automount 90 秒等待（未获上游确认的用户报告） |
| S10 | fstab 密码明文反面示例（[社区]） |
| S17b | `findmnt --verify` 校验 fstab、`-s` 搜索条目 |

> 标注说明：3.5.4 与 3.8 的 S05 条目为 `[社区]` / 未获上游确认；3.4 中「cifs 自动判为网络挂载」为 `[推断]`；`nofail` 逐条依赖未写；`password2=` 为 `[缺口]`（bookworm 超范围）；`findmnt --verify` 不验证远端共享为 `[推断]`。

## 相关笔记

- [[linux的文件权限]] —— 凭据文件 `chmod 600` 与目录 700 的权限模型
- [[Linux的文件系统结构]] —— `/etc/fstab` 在本机文件系统里的角色

---

> 🧭 分册导航 ｜ 总目录：[[SMB挂载-00-总目录]] ｜ 上一册：[[SMB挂载-02-手动挂载]] ｜ 下一册：[[SMB挂载-04-排错]]
