# 01 探测结果 — 把 SMB/CIFS 共享文件夹挂载到 Linux 服务器

- **运行标识**: smb-cifs-mount-linux
- **阶段**: P1 探测式收集（未完成，等待用户选定方向）
- **检索日期**: 2026-09-18
- **透镜**: A 手动挂载实操 ／ B 持久化与无人值守 ／ C 排错与协议选型
- **原始记录**: 15 条 → **去重后 12 条**（3 条跨透镜重复）

---

## 来源总表（去重后）

| ID | 标题 | URL | 层级 | 日期 | 分 | 透镜 | 相关性 / 支持的主张 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | mount.cifs(8) 手册（cifs-utils） | https://manpages.debian.org/trixie/cifs-utils/mount.cifs.8.en.html ／ bookworm 版 https://manpages.debian.org/bookworm/cifs-utils/mount.cifs.8.en.html | official | trixie 版 cifs-utils 2:7.4-1；bookworm 版 2:7.0-2 | 5 | A+B+C | 逐项定义 `vers`/`uid`/`gid`/`forceuid`/`file_mode`/`dir_mode`/`iocharset`/`credentials` 的语义与默认值；列全 `vers=` 取值与引入版本（1.0/2.0/2.1/3.0/3.02/3.1.1/3/default）；`credentials=` 文件格式与两条解析限制；`sec=` 默认 ntlmssp；**该手册不含错误码表** |
| S02 | systemd.mount(5) 手册 | https://manpages.debian.org/bookworm/systemd/systemd.mount.5.en.html | official | n/a | 5 | B | 一手定义 fstab 专有选项 `_netdev`（覆盖网络挂载判定）、`nofail`（只 Wants 不 Before）、`x-systemd.automount`/`requires`/`after`/`device-timeout`，以及网络挂载在 `remote-fs-pre`→`remote-fs` 间的排序与 `network-online.target` 拉取 |
| S03 | How to mount CIFS shares permanently（Ubuntu Server Docs） | https://ubuntu.com/server/docs/how-to/samba/mount-cifs-shares-permanently/ | official | n/a | 5 | A | 发行版官方最小可用路径：`cifs-utils` 安装、`guest`+`uid=1000`、`.smbcredentials` 凭据文件与 fstab 条目；Debian/Ubuntu 挂 Windows 共享的官方写法 |
| S04 | Detect, enable, and disable SMBv1, SMBv2, and SMBv3 in Windows | https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3 | official | ms.date 2025-02-28（updated 2026-09-08） | 5 | C | 微软官方：Win11 与 Server 2019+ 默认不安装 SMB1；SMB2/3 共用协议栈并自动协商至 3.1.1；`Get-SmbServerConfiguration` 检测法、禁用命令、SMB1 访问审计事件 ID 3000 |
| S05 | Ubuntu Wiki — MountWindowsSharesPermanently | https://wiki.ubuntu.com/MountWindowsSharesPermanently | official | 2024-04-18 | 4 | A+B | 发行版官方 wiki（内容含 12.04 时代遗留）：credentials 文件 `chmod 600` 的理由、fstab 中 `~` 不展开须写绝对路径、开机失败用 `noauto` 退回、`file_mode`/`dir_mode` 替代废弃的 `fmask`/`dmask`；未演示 `mount -t cifs` 命令行 |
| S06 | Samba — ArchWiki（客户端手动挂载一节） | https://wiki.archlinux.org/title/Samba | official | n/a | 4 | A | `mount -t cifs -o` 实例、`iocharset`/`vers` 用法、fstab+credentials 写法；说明 `uid`/`gid` 会隐含 `forceuid`/`forcegid` |
| S07 | Control SMB signing behavior | https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing | official | ms.date 2025-08-13（updated 2025-09-15） | 4 | C | 微软官方：Win11 24H2 专业/企业/教育版默认强制入站+出站 SMB 签名，Server 2025 仅强制出站；连不支持签名的第三方 SMB 服务器报 `0xc000a000`/`STATUS_INVALID_SIGNATURE`，改协议版本无法绕过 |
| S08 | Diagnosing CIFS "Permission denied" / `cifs_mount failed w/return code = -13` | https://access.redhat.com/solutions/450913 | official | 2025-12-03 | 4 | C | 红帽官方 KB：`mount error(13)` 的证据链 —— `dmesg` 同时出现 `NT_STATUS_LOGON_FAILURE` 与 `cifs_mount failed w/return code = -13`，据此把「权限被拒」拆成认证失败与共享权限问题两类（正文需订阅） |
| S09 | [systemd-devel] mounts with "nofail" can be unmounted on shutdown before "After=*-fs.target" units | https://lists.freedesktop.org/archives/systemd-devel/2024-June/050463.html | secondary | 2024-07-01 | 4 | B | 上游邮件列表实测（DietPi 维护者）：`nofail` 失败会连带 `remote-fs.target` 失败并丢失关机排序；`x-systemd.automount` 虽规避 nofail，但服务器不可达时默认停 90 秒、开机期触发可永久挂起 |
| S10 | 飞牛OS开机自动挂载SMB（jishuzhan.net，作者「好奇心害死薛猫」） | https://jishuzhan.net/article/2010524115405946881 | community | 2026-01-12 | 3 | A | 唯一实测贴合飞牛端的例子：fstab cifs 行含 `iocharset`/`uid`/`gid`/`file_mode`/`dir_mode`，配 `mount -a` 与 `@reboot` 延迟补挂；**密码明文、未用凭据文件**（反面示例） |
| S11 | 请问，LINUX系统下如何挂载NAS上的文件夹？（飞牛官方论坛） | https://club.fnnas.com/forum.php?mod=viewthread&tid=2318 | community | n/a | 3 | C | 飞牛官方论坛问答帖，讨论 Linux 端挂载 FNOS 共享的路径写法与权限排查；FNOS 挂载侧目前少见的社区经验 |
| S12 | Best Solution to Mount a Windows Share within a Container（Docker 社区论坛） | https://forums.docker.com/t/best-solution-to-mount-a-windows-share-within-a-container/65424 | community | 2018-12-19（续帖至 2026-01-07） | 3 | B | 容器内挂载 CIFS 的实战经验：`SYS_ADMIN`+`DAC_READ_SEARCH` 仍可能 `mount error 13`，`--privileged` 可行但被版主明确反对；推荐改为宿主机挂载后 bind mount 或用本地驱动 named volume |

> 层级分布：official 8 ｜ secondary 1 ｜ community 3

---

## 跨透镜重复合并说明

| 合并前 | 合并后 | 合并理由 |
| --- | --- | --- |
| A2（trixie manpage）+ B1（bookworm manpage）+ C1（bookworm manpage） | **S01** | 同一份 `mount.cifs(8)`，不同 Debian suite/版本；两个透镜分别从「选项语义」和「`vers=` 取值」两个角度切入同一文档 |
| A3 + B3（Ubuntu Wiki MountWindowsSharesPermanently） | **S05** | 同一 URL，A 关注 fstab/凭据文件写法，B 关注 `chmod 600` 与 `~` 不展开 |
| C5（飞牛论坛帖）与 A5（飞牛第三方教程） | S10 / S11 保留为两条 | URL 不同、作者不同，同属 community 层，可互为交叉印证，不合并 |

---

## 覆盖缺口（P2 前需向用户报备，不得在正文里当成官方口径）

1. **`mount error(112)` / `(115)` / `(2)` 无一手指南** — `mount.cifs(8)` 明确不提供错误码表；红帽与 NetApp 的相关 KB 正文需登录。只能自行对照 `errno.h`（`EACCES`/`EHOSTDOWN`/`EINPROGRESS`/`ENOENT`），或标为「按 errno 推断」。
2. **飞牛 FNOS 侧无官方文档** — 未找到飞牛官方说明其 SMB 默认方言、是否启用 SMB1、签名/加密默认值的页面。FNOS 部分只能写成「社区经验」，且需在笔记里显式标注来源层级。
3. **Docker 容器内挂载 CIFS 缺官方 capability 说明** — 现有说法（`SYS_ADMIN`、`DAC_READ_SEARCH`、seccomp）互相不一致，只有论坛与 issue 经验，无 Docker 官方确认。
4. **`x-systemd.mount-timeout` 一手口径存疑** — 在 bookworm 版 `systemd.mount(5)` 中未能确认到定义，仅见二手博客反复引用；需查新版 man page 或 systemd 源码后再写。
5. **Debian 侧无 CIFS 客户端挂载官方条目** — `wiki.debian.org/Samba` 正在重构，客户端挂载内容指向子页且无法确认；Debian 专属 fstab 示例目前全来自二手。
6. **协议选型边界与掉线重连缺一手来源** — NFS/SMB/WebDAV 适用场景只有营销博客与无署名对比文；「掉线重连 / 服务端休眠」只有 `_netdev`、`x-systemd.automount`、`soft`/`hard`、`nofail` 的二手教程。

---

## 方向菜单（请用户选一项后 P1 才可完成）

| 选项 | 方向 | 章节预估 | 主要依据 |
| --- | --- | --- | --- |
| **A（推荐）** | 均衡实战：协议选型 → 手动挂载 → 凭据文件与 fstab 持久化 → 排错 → （可选）容器场景 | 5 章 | S01–S09 覆盖主干，全为一手；缺口 4/5/6 作为「待确认」小节或省略 |
| B | 最小可用路径：怎么挂 + 怎么排错，两章速查 | 2 章 | S01 + S03 + S05 + S08 |
| C | 机制深挖：SMB 方言协商 / 签名 / 错误码原理为主，fstab 降为附录 | 3–4 章 | S01 + S02 + S04 + S07 + S08 |
| D | 在 A 基础上加「Docker 容器内挂载共享」独立一章 | 6 章 | A 的全部 + S12，**该章必须标注为社区经验**（缺口 3） |

### 无论选哪项都要遵守的来源纪律
- FNOS 相关段落只能标 community（S10/S11），不得写成官方口径。
- `mount error(112/115/2)` 的语义若无一手来源，正文写「按 errno 推断」并给出可复现的 `dmesg`/`journalctl` 证据链查法。
- S05 的 Ubuntu Wiki 页含 12.04 时代遗留内容，引用时须注明「官方 wiki，部分内容陈旧」，并与 S01/S02 交叉核对。

---

## P2 预估规模

- **深读核心来源**: 建议 4–5 个 —— S01（选项与 `vers=` 判据）、S02（fstab 选项一手定义）、S03 或 S05（发行版官方最小路径）、S04+S07（Windows 侧方言与签名）、S08（错误码 13 证据链）
- **补源方向**: 缺口 1/4/6 各需 1–2 次定向检索；缺口 2/3 预计无法补到一手来源，直接按「标注二手」处理
- **代理编排**: ≤3 个深读代理（一个来源组一个），不按来源逐个派
- **产出**: `02_deep_research.md`（范围 / 来源表 / 主张-来源映射 / 冲突 / 实操指引 / 待确认问题 / 下游交接）
