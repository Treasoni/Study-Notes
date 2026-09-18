# 学习笔记大纲：《把 SMB/CIFS 共享文件夹挂载到 Linux 服务器》

> 笔记类型：实战笔记（附 SMB/CIFS vs NFS 协议选择对比）
> 结构依据：`02_deep_research.md` §八「下游交接」建议骨架（方向 A，5 章）
> 预计总篇幅：约 9,700–13,000 字
> 章节数：5（第 5 章为**可选小节**，用户不需要时可在组装阶段整章删除）
> 目标读者：有 Debian/Ubuntu 服务器运维经验、要能照做的读者
> 挂载端：Debian/Ubuntu（`cifs-utils` 生态）｜共享端示例：Windows 共享 + 飞牛 FNOS
> 输出目标：先落 `workspace/smb-cifs-mount-linux/output/`，Obsidian 位置待阶段 6 前确认

---

## 全局写作纪律（原样取自 02 §八，不得软化）

- FNOS 段落只能标 community（S10/S11），**不写默认方言值**。
- `mount error(112/115/2)` 写「按 errno 推断」，给可复现的 `dmesg`/`journalctl` 查法。
- `fmask`/`dmask`「已废弃」、`file_mode`/`dir_mode` 默认数值、`nofail` 逐条取消哪些依赖 —— **一律不得写成官方结论**。
- S05（Ubuntu Wiki）含 2008/12.04 遗留内容，引用时注明「官方 wiki，部分内容陈旧」。
- S09（邮件列表）标注「未获上游确认的用户报告」。
- 「官方文档说」类表述必须能回指到 `02_deep_research.md` 的 SID + 锚点。
- **来源台账**：S01a/S01b 双版本、S02 三版本已就绪；**引用选项默认值时必须带版本**（如「cifs-utils 7.4-1」或「systemd 252」）。

### 层级标注符号（全篇统一）

| 标记 | 含义 | 对应 02 §一 的分类 |
| --- | --- | --- |
| `[一手]` | 已确证可写，须带 SID + 锚点 | 「已确证可写的内容」 |
| `[社区]` | 只能标为社区经验 / 未经一手证实 | 「只能标为社区经验/未经一手证实的内容」 |
| `[推断]` | 02 明确要求标为推断，不得写成官方结论 | §六 未解问题 |
| `[缺口]` | 02 无来源，不补写或只能作命令用法出现 | §一 / §六 |

---

## 第一章：协议选型：什么时候该用 SMB/CIFS

- **篇幅**：短（约 800–1,200 字）
- **素材引用**：S16（2007 历史一手）、S04（开头段、`Disable SMBv2 or SMBv3`）、S01a（`vers=`）、S13（`vers=`、`Name`）、S06（`Manual mounting`）
- **代码示例**：无
- **主张层级（本章逐项）**：
  - `[一手]` 协议设计意图与边界：S16 —— **仅此层面可用**，其自述 2007 年，对 SMB3.1.1/NFSv4.2 已过时
  - `[缺口]` 现代 SMB vs NFS vs WebDAV 边界：02 §一 明确归入「只能标为社区经验/未经一手证实」——本章**不得给出选型结论**，只保留判断维度，并把缺口显式写出来
  - `[一手]` Windows 侧方言演进与 SMB1 现状：S04
- **`[!tip] 大白话` 落点**：「方言 = 客户端与服务端商量好用哪一版协议」处 1 个
- **「常见坑」小节**：留（只放认知层面的坑，锚点 S04 开头段）

### 1.1 写作定位：只写「怎么判断」，不写「谁更好」
- 说明为何本章是判断清单而非评测（02 §八 骨架 1：材料薄）
- 明确写出「现代协议边界无一手来源」这一缺口，并说明读者应以共享端实际能力为依据

### 1.2 SMB/CIFS 的协议定位（历史一手层面）
- S16 对 CIFS / NFS / HTTP / WebDAV 的设计意图表述（只引 S16 观点，标 2007 年与作者身份）
- 明确标注该文不能用于现代现状

### 1.3 三个必须先确认的概念
- SMB 版本与方言（S04、S01a `vers=`、S13 `vers=`）
- UNC 路径与共享名写法（S06 `Manual mounting`）
- 挂载点语义：挂载后由谁决定属主与权限（S01a `uid=`、`FILE AND DIRECTORY OWNERSHIP AND PERMISSIONS`，与第 2 章交叉引用）

### 1.4 判断清单：进入第 2 章前的自检项
- 共享端是什么（Windows / NAS / FNOS）、认证方式、是否需要开机自动挂载
- Windows 侧的方言与签名现状（指向 S04、S07，为第 4 章埋伏笔）

---

## 第二章：手动挂载：从零到挂上

- **篇幅**：长（约 3,200–4,200 字）
- **素材引用**：S01a、S01b、S03、S05、S06、S10、S11、S13（S02 `_netdev` 交叉引用至第 3 章）
- **代码示例**：**有**（命令级，见下）
- **主张层级（本章逐项）**：
  - `[一手]` 选项默认值与行为：S01a / S01b / S13 —— **引用必须带版本**（cifs-utils 7.4-1 或 7.0-2）
  - `[社区]` FNOS 段落：S10 / S11，仅 community，**不写默认方言值**
  - `[推断]` `mapposix` 默认状态：02 §四.2 —— 并列 S01a 与 S06，标注「ArchWiki 说法未在 man page 中得到确认」
  - `[缺口]` `file_mode`/`dir_mode` 默认数值：02 §六.7 —— **不写具体数值**
  - `[缺口]` `smbclient`、`findmnt`：00_intent 列为工具链，但 02 未收集到锚点 —— 只能作「社区常用命令」出现，或标注需回补来源
- **`[!tip] 大白话` 落点**：`uid`/`gid` 与 `file_mode`/`dir_mode` 的分工处 1 个；`vers=` 协商处 1 个
- **「常见坑」小节**：留

### 2.1 前置：`cifs-utils` 与版本基线
- 安装包与发行版基线：cifs-utils 7.4-1（trixie）/ 7.0-2（bookworm）（S01a、S01b、S03）
- 为什么本笔记所有选项都要带版本读（02 §八来源台账）

### 2.2 最小可用挂载命令
- `mount -t cifs //服务器/共享名 /挂载点 -o credentials=...` 的完整形态（S01a、S06、02 §五.1）
- 共享名尾随 `/` 的行为（S06 `Manual mounting`）
- `-o` 参数传递与逗号转义的基本约束

### 2.3 选项语义逐项（本章核心，篇幅占比约一半）
- 2.3.1 属主与权限：`uid`/`gid` 及其默认值（S01a `uid=`）；`forceuid`/`forcegid` 与「无选项可覆盖 mode」（S01a `forceuid`、`FILE AND DIRECTORY OWNERSHIP AND PERMISSIONS`）；`perm`/`noperm` 的客户端权限检查（S01a `noperm`）
- 2.3.2 mode 类选项：`file_mode`/`dir_mode` 的生效条件（S01a `file_mode=`）；`fmask`/`dmask` 的争议并列呈现（S05 2008 年段落 vs S01a/S01b 全文无该条目，02 §四.1）；`mapposix` 说法并列（02 §四.2）
- 2.3.3 字符集：`iocharset` 与内核默认（S01a `iocharset`）
- 2.3.4 协议版本：`vers=` 取值集合与协商默认随内核变化的三档对照表（S01a `vers=`、S13 `vers=`）；不写 Windows 侧「协商选中哪个方言」的规则（02 §六.9）
- 2.3.5 安全与加密：`sec=` 默认分界（S01a `sec=`、S13 `sec=`）；`seal` 与 SMB3+ 前提（S13 `seal`）
- 2.3.6 文件系统类型：`smb3` fstype 与 `mount.smb3`（S13 `Name`）；无认证共享的 `username=*`（S06 `Manual mounting`）
- 2.3.7 不提的选项：`serverino`/`noserverino`（02 §六.10 —— 原文未给建议，不提或标「原文未给建议」）

### 2.4 两个落地例
- Windows 共享：只写挂载侧命令与前置条件，服务端条件指向第 4 章（S04、S07）
- 飞牛 FNOS 共享：**整段标 community**（S10、S11）；S10 的 fstab 行可作反面示例引用（其 `password` 为明文），但**不复制其凭据写法**

### 2.5 挂载后核对实际协商到的方言
- 读 `/proc/fs/cifs/DebugData`（S13 `vers=`）
- 为什么不能靠「挂上了」推断方言

### 2.6 常见坑
- 用 `[!warning]` Callout 承载；素材锚点：S01a `BUGS`、S06 `Manual mounting`、S01a `file_mode=`

### 本章需要的代码示例（命令级）
- `mount -t cifs //server/share /mnt/point -o credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8`（S01a、S06、02 §五.1）
- 交互式临时挂载（`-o username=...,password=...`）及含逗号密码的解析限制（S01a `BUGS`）
- `forceuid` / `noperm` / `file_mode=` 变体对照
- `mount -t smb3 //server/share /mnt/point ...`（S13 `Name`）
- 读 `/proc/fs/cifs/DebugData` 确认 Dialect（S13）

---

## 第三章：凭据文件与开机自动挂载

- **篇幅**：长（约 2,800–3,600 字）
- **素材引用**：S01a、S01b、S02（252.36 / 257.13 / 262~rc3）、S03、S05、S06、S09
- **代码示例**：**有**（文件内容 + fstab 行级，见下）
- **主张层级（本章逐项）**：
  - `[一手]` systemd 机制：S02 —— **引用必须带版本**（252 / 257 / 262）
  - `[一手但陈旧]` S05：引用时注明「官方 wiki，部分内容陈旧」（含 2008/9.04/12.04 遗留）
  - `[社区]` S09：标注「未获上游确认的用户报告（邮件列表提问，原帖无任何回复）」
  - `[推断]` 「cifs 会被自动判为网络挂载、`_netdev` 可能冗余」：02 §六.3 明确标 `[推断]`
  - `[不得断言]` `nofail` 究竟取消哪几条依赖：02 §六.4 —— 只写「取消 required 身份与 target 排序」，**不逐条断言**
  - `[缺口]` `mount -a` 与 fstab 的联动语义：02 §六.8 —— 只作命令使用，不展开语义
- **`[!tip] 大白话` 落点**：`_netdev` / `nofail` / `x-systemd.automount` 三者的分工处 1 个
- **「常见坑」小节**：留

### 3.1 凭据文件规范
- 权限与属主：目录 700 / 文件 600 / `root:root`（S06 `Storing share passwords`）；`chmod 600` 的官方依据（S03 `Create a credentials file`、S05）
- 语法限制：等号两侧不留空格、`domain=SALES` 而非 `SALES\`（S03 `Login errors`）
- fstab 中必须写绝对路径、`~` 不展开（S05 `Use of tilde in pathnames`，注明该段落年份与「结论仍有效」的判定）
- 键的版本边界：`password2=` 在 7.0-2（bookworm）超出该版本文档范围（S01a/S01b、02 §四.8）

### 3.2 凭据文件的解析限制
- 以空格开头的用户名或密码不处理（S01a `BUGS`）
- 含逗号密码的三条可用路径（凭据文件 / `PASSWD` 环境变量 / 交互输入）（S01a `BUGS`）

### 3.3 `/etc/fstab` 行写法
- 最小官方形态：`credentials=` + `0 0`（S03 `Mount password-protected network folders`，含其对服务器离线时报错的自承）
- 路径含空格写 `\040`（S03、S06 `As mount entry`）
- 普通用户挂载用 `users`（复数）（S06 `As mount entry`）
- S10 的反面示例：密码明文进 fstab（仅作反例，标 community）

### 3.4 开机顺序机制
- 网络挂载单元自动获得的 `After=`/`Before=`/`Wants=` 依赖，以及 `nofail` 对它的影响（S02 `Default Dependencies`）
- `_netdev` 如何覆盖按 fstype 的自动判定（S02 `_netdev`）
- `nofail` 的 wanted/required 语义与 target 排序变化（S02 `nofail`）

### 3.5 服务器离线时的回落路线（三条并列呈现，02 §四.5）
- 3.5.1 `noauto` + 登录后挂载（S03 `Mount after login instead of boot`、S05）
- 3.5.2 `noauto` + `x-systemd.automount`（S02 `noauto, auto`、S06、S09）；`x-systemd.automount` 下 `auto`/`noauto` 均失效（S02）
- 3.5.3 必须写明的事实：官方指南未覆盖 systemd 原生做法（S03 全文未提 `x-systemd.automount`，02 §四.5）
- 3.5.4 `[社区]` S09 的两条附带报告：`nofail` 关机卸载早于 `After=*-fs.target` 服务停止（含 qBittorrent + CIFS 举例）；`automount` 在服务器不可达时默认停 90 秒 —— 均标「未获上游确认的用户报告」

### 3.6 限制单次等待时间
- `x-systemd.mount-timeout=`：存在性与引入版本（S02 `x-systemd.mount-timeout=`，注意 bookworm 页不显示 `Added in version` 标注行）；**只能写在 fstab**，写进单元文件的 `Options=` 会被忽略
- 超时后的行为落在 `TimeoutSec=`（S02）
- 与 `x-systemd.device-timeout=` 的区别（S02）

### 3.7 按需挂载的其余相关选项
- `x-systemd.idle-timeout=` 与 `TimeoutIdleSec=`（S02）
- `x-systemd.requires=` / `before=` / `after=` 的差异（S02 `x-systemd.requires=`）

### 3.8 其他
- `guest` 选项在开机挂载中的可靠性：并列 S03 与 S05（02 §四.3；S05 那条注明「报告者自认无法解释原因」）

### 3.9 常见坑
- 用 `[!warning]` Callout；锚点：S03、S05、S02 `nofail`、S02 `x-systemd.mount-timeout=`

### 本章需要的代码示例（文件/命令级）
- 凭据文件内容（`username=` / `password=` / `domain=`）+ `chmod 600` + `chown root:root`（S03、S06）
- fstab 行：`//server/share /mnt/point cifs credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8,_netdev,nofail 0 0`（02 §五.3）
- `noauto` + `x-systemd.automount` 变体（S02）
- `x-systemd.mount-timeout=` 写在 fstab 的写法（S02）
- `mount -a`（仅作命令使用，不展开语义，02 §六.8）

---

## 第四章：排错：从错误码回到证据链

- **篇幅**：中（约 2,400–3,200 字）
- **素材引用**：S08、S15、S14、S13、S07、S04、S01a（交叉）
- **代码示例**：**有**（见下）
- **主线要求**：以**可复现的证据链**组织，错误码只作为链条上的节点，**不用错误码清单当骨架**
- **主张层级（本章逐项）**：
  - `[一手]` S08 的 Issue/Environment 小节、S15 的数值↔名称硬对应、S07 的签名分档、S04 的方言现状
  - `[推断]` `mount error(N)` 是否**直接等于** errno：02 §六.1 —— 标 `[推断]`，并说明 cifs-utils 源码抓取三次均被 HTTP 429 拒绝
  - `[缺口]` 红帽 KB 的 Resolution 在订阅墙后：02 §六.2 —— **不补写**，只引用可见小节
  - `[注明]` 引用 S04 时以页面实际标注日期为准（02 §四.7，探测与深读两处日期不一致）
  - `[不写]` Windows 侧协商「在何种条件下选中哪个方言」（02 §六.9）
  - `[社区]` `journalctl` 具体子命令在 02 中无锚点，只能作命令用法出现
- **`[!tip] 大白话` 落点**：证据链读法（`13` 表示「被拒绝」，不等于「网络不通」）处 1 个
- **「常见坑」小节**：留

### 4.1 `mount error(13)` 的完整证据链
- 第一步：`dmesg`/messages 找 `CIFS VFS: cifs_mount failed w/return code = -13`（S08 `Issue`）
- 第二步：同现的 `Status code returned 0xc000006d NT_STATUS_LOGON_FAILURE` 决定方向（凭据/认证 vs 网络）（S08）
- 第三步：手工挂载与 `mount -a`/fstab 两条路径都复现同一错误（S08）
- 第四步：`mount -vvv` 的 `Credential formatted incorrectly: (null)` 与实际下发参数（S08）

### 4.2 errno 名称↔数值对照
- 硬对应表：`ENOENT` / `EACCES` / `EHOSTDOWN` / `EHOSTUNREACH` / `EINPROGRESS` / `EREMOTEIO`（S15 `errno-base.h`、`errno.h`）
- **易错点专门强调**：112 与 113 不是同一个符号（S15）
- 为什么 errno(3) 明确不列数值（S14 `Error numbers and names`）
- 与 4.1 的衔接：数值解读一律写「按 errno 推断」（02 §八）

### 4.3 方言协商的核对方法
- 内核版本与默认协商版本的三档关系（S13 `vers=`）
- 挂载后读 `/proc/fs/cifs/DebugData` 确认实际 Dialect（S13）
- 何时才需要显式 `vers=`（S01a `vers=`）
- SMB1 在 Windows 侧的当前状态（S04 开头段）

### 4.4 Windows 共享连不上时的优先排查方向
- 先查签名，而不是先降协议版本（S04 开头段、S07）
- 签名强制三档（Win11 24H2 企业/专业/教育、Server 2025、24H2 家庭版）（S07 `How SMB signing works`）—— 用 S07 细粒度表述，避免误读（02 §四.6）
- `STATUS_INVALID_SIGNATURE` / `0xc000a000` 的现象与处置方向（S07 `SMB signing behavior`、S04）
- 查法：`Get-SmbClientConfiguration | FL RequireSecuritySignature`（S07 `Verify SMB signing status`）
- 签名与来宾访问的关联（S07 `Disable SMB signing`、`SMB signing behavior`）
- 微软对「关协议/关签名绕过失败」的立场（S04 开头段）

### 4.5 两条必须写明的未闭环
- `mount error(N)` 的数字含义：写「数值与 errno 的对应关系」，把「`mount.cifs` 直接打印 errno」标 `[推断]`（02 §六.1）
- 红帽 KB Resolution 不可读：不补写（02 §六.2）

### 4.6 常见坑
- 用 `[!warning]` Callout；锚点：S15、S07、S04、S08

### 本章需要的代码示例（命令级）
- `dmesg` 过滤 CIFS 行 / `journalctl` 对应查法（S08 锚点为 `dmesg`/messages；`journalctl` 标为命令用法）
- `mount -vvv`（S08）
- `mount -a`（S08 中作为对照路径）
- `Get-SmbClientConfiguration | FL RequireSecuritySignature`（S07）
- 读 `/proc/fs/cifs/DebugData`（S13）

---

## 第五章（可选，单小节）：容器内挂载

> **可选性声明**：本章仅含一个 H3 小节，用户选择「容器为可选小节」；不需要时可在组装阶段整章删除，**不影响第 1–4 章的连贯性**。同章不单列「常见坑」小节。

- **篇幅**：短（约 500–800 字）
- **素材引用**：S12（唯一来源）
- **代码示例**：**有**（形式示意，全部标社区经验）
- **主张层级（本章逐项）**：
  - `[社区]` **整章 100% community**：S12 为 Docker 论坛帖，02 §一、§三.3 末行明确「无 Docker 官方 capability 说明」，且帖内说法互相矛盾
  - `[缺口]` **不写「需要哪些 capability」的确定清单**
  - `[缺口]` 不把 `--privileged` 当作默认方案（S12 中该做法被版主反对）
- **`[!tip] 大白话` 落点**：不需要

### 5.1 容器内直接挂载 CIFS：现象与争议
- S12 中 capability 说法的互相矛盾之处（并列呈现，不作裁决）
- `SYS_ADMIN` + `DAC_READ_SEARCH` 仍可能失败的报告、`--privileged` 可行的报告与被反对的理由（S12）

### 5.2 更稳妥的替代路径
- 宿主机挂载 + bind mount（S12）
- 本地驱动 named volume（S12）
- 结尾一句：本小节所有结论均为社区经验，生产环境请自行验证

---

## 学习路径说明

### 前置要求
- 会用 shell 与 `sudo`，能编辑 `/etc/fstab`，了解 systemd 基本命令（`systemctl`、`systemd-analyze` 之类）
- 共享端已建好共享，并知道共享端地址、共享名、账号密码（Windows 或 FNOS 侧）
- 有一台能连通共享端的 Debian/Ubuntu 机器；第 3 章的 fstab 改动建议先在可回滚/有快照的机器上做
- 不需要预先懂 SMB 协议内部细节（第 1 章会补概念，但只在设计意图层面）

### 学完能做什么
- 能用一条 `mount -t cifs` 把共享挂到指定挂载点，并说清 `uid`/`gid`/`file_mode`/`iocharset`/`vers`/`sec` 的语义**与各自的边界**
- 能把密码从 `/etc/fstab` 移入凭据文件并设对权限，避开凭据文件的两个解析限制
- 能写出带 `_netdev`/`nofail`/`noauto`+`x-systemd.automount` 的持久化方案，并解释三者各自换来的代价
- 能按证据链读懂 `mount error(13)` 与 errno 数值，判断问题在认证、网络还是方言协商
- 能在 Windows 共享连不上时**先**排查签名，而不是先降协议版本
- （可选）能判断容器内挂载是否值得做，知道更稳妥的替代路径

### 建议学习顺序
- 第 1 章 → 第 2 章 → 第 3 章 → 第 4 章：**顺序不可换**（第 3 章依赖第 2 章建立的命令与选项上下文；第 4 章同时依赖第 2 章的方言知识与第 3 章的持久化上下文）
- 第 5 章可选，可在读完第 3 章后的任意时点插入，也可跳过
- 第 2 章建议边读边在非生产环境敲一遍；第 3 章建议先改一份 fstab 副本再落地
- 预估耗时：第 1 章约 10 分钟；第 2 章约 45–60 分钟（含实操）；第 3 章约 40–50 分钟；第 4 章约 30 分钟；第 5 章约 10 分钟

---

## 来源缺口清单（写作时不得补写）

| 缺口 | 02 依据 | 本章处理 |
| --- | --- | --- |
| 现代 SMB/NFS/WebDAV 边界 | §一 | 第 1 章只保留判断维度，不写选型结论 |
| FNOS 默认方言 / SMB1 状态 / 签名默认值 | §一、§六.5 | 第 2 章 FNOS 段落只标 community，不写默认值 |
| Docker 内挂载所需 capability | §一、§六.6 | 第 5 章标社区经验，不写清单 |
| `file_mode`/`dir_mode` 默认数值 | §六.7 | 第 2 章不写具体数值 |
| `mount.cifs` 打印的错误码是否等于 errno | §六.1 | 第 4 章标 `[推断]` |
| 红帽 KB Resolution 步骤 | §六.2 | 第 4 章不补写 |
| 哪些 fstype 被 systemd 判为网络挂载 | §六.3 | 第 3 章标 `[推断]` |
| `nofail` 逐条取消哪些依赖 | §六.4 | 第 3 章只写「取消 required 身份与 target 排序」 |
| `mount -a` 与 fstab 联动语义 | §六.8 | 第 3 章只作命令使用 |
| Windows 侧协商选择规则 | §六.9 | 第 2/4 章不写 |
| `serverino`/`noserverino` 使用建议 | §六.10 | 第 2 章不提或标「原文未给建议」 |
| `smbclient` / `findmnt` 无一手锚点 | 00_intent 列出，02 未收集 | 只能作「社区常用命令」出现 |
