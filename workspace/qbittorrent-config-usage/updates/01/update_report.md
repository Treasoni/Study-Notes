---
note_set: qBittorrent 配置与使用（三册 + 总览）
run: qbittorrent-config-usage
date: 2026-10-16
mode: patch-in-place
status: 已完成（workspace 同步方向已定：明确弃用 `chapters/`）
---

# update_report — qBittorrent 配置与使用

## 一句话摘要

按用户确认的「第 0 步（补实）+ 第 1 步（归位）+ 第 2 步（去重）」执行：**中册 §4.4 代理一节从「只给接入点」补成「字段以源码为准」；顶层散乱的 `qBittorent/` 迁入分册目录并标记归档；孤儿附件去重**。其后按用户追加确认，做**增量 2**：**下册 §5.3 补入「界面上的 Tracker 状态对照表」**（补 `Tracker error`/`Unreachable` 两档、纠正 `Updating...` 非状态）；再做**增量 3**：**上册新增 §2.5「WebUI 的对外访问与安全」**（把原 §2.6 的 LA-4 社区经验升格为源码口径，给出四个默认开启的防护开关）。四份成品在 vault 与 workspace 两处仍逐字节一致。

## 改动明细

### A. 中册 `02 qBittorrent 配好.md`（vault + workspace output 同步）

| 位置 | 前 | 后 |
| --- | --- | --- |
| 目录 4.4 条目 | 代理：接入点在这里，字段来源薄弱（标注） | 代理：字段以源码为准，取值只长在你自己的环境里 |
| §4.4 正文 | 3 行：入口句 + 一条 `[!warning]`「本册不给具体字段」 | 三张表 + 2 处 `[!warning]` + 1 处 `[!tip] 大白话`：① 界面字段全表 ② 可照抄取值表（标注为**他人实测**）③ 生效判据表 |
| §4.6 | 只有 ①–④ | 新增 **⑤ 代理要不要手改配置文件？**（`Network/Proxy/*` 键表 + 「默认值 ≠ 推荐值」提示） |
| 本章小结 | 1 条（代理只给接入点） | 2 条（字段以源码为准 / 作用范围） |
| 引文对照 | — | 追加 10 行（英→中 + 出处 `LB-7 · sources/l2-7_proxy-official-source.md:NN`） |
| 脚注 | 66 定义 | 94 定义（新增 `[^c4-lb7-*]` 22 条、`[^c4-lb8-*]` 6 条） |
| frontmatter | `updated: 2026-10-07` | `updated: 2026-10-16` |
| 文末 | — | 新增 `## 更新记录`（1 行：2026-10-16 / LB-7 + LB-8） |

总览同批：`updated: 2026-10-07` → `2026-10-16`，文末新增 `## 更新记录`（1 行）。

量化：汉字 5,447 → 6,793（**+1,346**）；字符 20,801 → 28,813（**+8,012**）；字节 33,992 → **45,334**；
Callout 16 → 20；脚注引用 84 → 114、定义 66 → 94。

**关键纠错（口径）**：旧散记把「**P2P 数据下载通常不经过代理**」写成**无条件结论**。官方源码 tooltip
（`optionsdialog.ui:2314`：`Otherwise, the proxy server is only used for tracker connections`）表明
**只有不勾 `Use proxy for peer connections` 时，代理才仅用于 tracker 连接**。中册正文已按此限定作用范围，
并用 `[!warning]` 明确写出「**不要**记成『qBittorrent 的代理一概不管 P2P』」。

**配方取值纪律**：`Type / Host / Port` 的**具体取值**只有 LB-8（作者本人环境）一个来源，正文里
逐句标注「这是**别人的**实测值，照抄一定不通」；**未编造** `qBittorrent.conf` 代码块，§4.6 只给配置键与
工厂默认值（`8080` / `0.0.0.0` / `ProxyType::None` / `HostnameLookupEnabled=true`），并提示默认值不是推荐值。

### B. 总览 `qBittorrent 配置与使用（总览）.md`（vault + workspace output 同步）

- 「另有一组更早的散记」Callout 重写：从「仓库顶层 `qBittorent/`…**保持原位不动**，只在新篇给一句指引」
  改为「本目录 `旧散记/` 子文件夹 + **4 条双链** + 已归档口径」。
- 汉字 758 → **904**（含新增 `## 更新记录`）；双链 6 → 10（+4）。

### C. 旧散记归位（`qBittorent/` → `流媒体与影音/qBittorrent 配置与使用/旧散记/`）

- **移动方式**：Obsidian `app.fileManager.renameFile`（`move` 子命令不支持文件夹），拼写
  `qBittorent` → `qBittorrent` 一并修正；`assets/` 与 `sortspec.md` 随文件夹整体搬迁，
  4 篇正文里的 7 处 `![](assets/…)` 相对路径**全部保持可解析**（CLI `links` 逐条复核，0 未解析）。
- **归档标记**：4 篇文首各加 `> [!warning] 已归档（旧散记）`，含指向总览的双链 + **各自的具体过时点**
  （版本号停在 v5.1.x / 代理作用范围写错 / Tracker 列表计数未复核 / 站点规则表属站点特定）；
  frontmatter 加 `status: archived`、`updated: 2026-10-16`。
- **修错**：
  - `qBittorrent的Tracker.md` 的图片引用含 **U+FFFD 乱码**（`截��2026-02-05…`），已修为 `截屏2026-02-05 21.08.11.png`；
  - `qBittorrent配置代理.md` 的 `[[docker进行代理#2.3 …]]` **目标笔记从未发布进 vault**（仅 `workspace/update-docker/` 有草稿），
    属悬空双链 → 改为白话表述「看你的 Clash 有没有开局域网鉴权」。

### D. MOC

`流媒体与影音 MOC.md`：在 `## 部署与配置` 的 qBittorrent 条目下追加 **1 条归档索引**（4 个双链，
指向 `旧散记/` 四篇）；`updated: 2026-10-08` → `2026-10-16`。校验：MOC 全部双链 0 未解析。

### E. 附件去重（第 2 步）

| 目录 | 处理 | 依据 |
| --- | --- | --- |
| `assets/qBittorent配置代理/`（2 张） | 先复制进 `旧散记/assets/qBittorrent配置代理/`（旧笔记的引用路径一直指不到这里，属历史断链），再经 Obsidian 回收站删除原目录 | 复制后全库零引用 |
| `assets/qBittorent的Tracker/`（1 张 `file-20260202223827013.png`） | 经 Obsidian 回收站删除 | 全库零引用（孤儿；2026-02-02 的旧截图，已被 02-05 版取代） |

删除均走 Obsidian `fileManager.trashFile`（非永久删除）；三张图在 git 中为已跟踪文件，可随时 `git checkout` 恢复。

### F. 顺手清理

- 删除 `sources/_raw/proxyconfigurationmanager.h`（14 B，内容为 `404: Not Found` 的抓取残留）。
- **回滚了一次 Obsidian 的越界改写**：搬迁文件夹时 Obsidian 把证据快照
  `sources/l2-8_proxy-user-practice.md` 里的**逐字引文**中的图片路径改写成了新的相对路径
  （`../../../流媒体与影音/…`），破坏证据链，已改回原文 `assets/qBittorrent配置代理/file-20260202223705113.png`。
  （vault 根 = 项目根，`workspace/` 也在 Obsidian 索引范围内，这是本仓库的已知副作用。）

### G. 增量 2：下册 §5.3 新增「界面上的 Tracker 状态对照表」（vault + workspace output 同步）

第二个增量，针对旧散记《qBittorrent的Tracker》里**唯一一处「有内容但成品没有」**的实料：Tracker 状态表。用户选定「先做低风险的那个 Tracker 状态表（纯 UI 枚举、可逐字取证）」。

| 位置 | 前 | 后 |
| --- | --- | --- |
| §5.3 标题 / 目录条目 | `Tracker：公告地址与公共列表（F11）` | `Tracker：公告地址、公共列表与界面状态（F11）`（不改编号，避免 5.4/5.5 连带重排） |
| §5.3 末尾（公共列表代码块之后） | 直接结束，接 §5.4 | 新增 7 行状态对照表 + 1 处 `[!warning]`「别漏 `Tracker error` 与 `Unreachable`」+ 1 处 `[!note]`「桌面版还多两条说明串」+ 1 处 `[!tip] 大白话`（快递轨迹类比） |
| 本章小结 | 5 条 | 6 条（新增「状态是五档枚举 / `Updating...` 是标记 / 别漏 5 与 6」） |
| 脚注 | 第 5 章 19 条定义 | 新增 `[^c5-lb9-*]` 4 条 |
| frontmatter | `updated: 2026-10-07` | `updated: 2026-10-16` |
| 文末 | — | 新增 `## 更新记录`（1 行：2026-10-16 / LB-9） |

**本增量纠正的口径错**（旧散记的表本身有缺漏）：旧散记列 `Working / Updating / Not Working / Not Contacted / Disabled`，**漏了 `Tracker error`（枚举 5）与 `Unreachable`（枚举 6）**，并把 `Updating` 当成一种状态。按源码 `trackerentrystatus.h:40-47`，状态枚举只有五档 `1 / 2 / 4 / 5 / 6`（`0` 是 WebUI 侧的 `Disabled`，`3` 未被使用）；`Updating...` 是 `isUpdating` 标记，为真时**先于** `switch` 返回（`trackerlistmodel.cpp:218-219`、`prop-trackers.js:47-48`），不是状态。桌面版另有 `Disabled for this torrent` 与 `This torrent is private` 两条说明串（`trackerlistmodel.cpp:68-69`），已单列并注明**仅桌面版**。

**新增来源件 LB-9**（primary，qBittorrent 源码 @ `df402f91d456`）：`sources/l3-9_tracker-status-official-source.md`，逐字留档 `trackerentrystatus.h`（枚举）、`trackerlistmodel.cpp`（桌面版状态串 + `statusText()`）、`prop-trackers.js`（WebUI 状态串与数值映射）三处片段。**未**写入任何「某状态该怎么办」的处置建议——那属教程性建议，无来源，故不写。

> [!warning] 一处自查纠正（本增量开工时）
> LB-9 首次生成时**片段标题与片段正文错位**（`## 片段 3` 标题压在 `trackerlistmodel.cpp` 正文之上）；已按「片段 1 = 枚举 / 片段 2 = 桌面版 / 片段 3 = WebUI / 读法」重排，并补齐标题前空行。

### H. 增量 3：上册新增 §2.5「WebUI 的对外访问与安全」（vault + workspace output 同步）

用户确认做原先提议的**块 3**。核心不是「新塞一章」，而是**把上册 §2.6 里那条以社区经验身份出现的 LA-4 提示升格为可核对的官方口径**——那条提示只说「关掉 `HostHeaderValidation` / `CSRFProtection` 可以绕开强制 https」，**从没给默认值与语义**。

| 位置 | 前 | 后 |
| --- | --- | --- |
| 目录 / 标题 | `2.5 动手实践（新手可跳过）` | 新增 `2.5 WebUI 的对外访问与安全：默认防护是开着的`；原 2.5 顺延为 `2.6` |
| 上册 §2.5（新） | — | 两张对照表（WebUI 页字段 / 四个防护开关，均含「界面原文 · 配置键 · 源码默认 · 说人话」）+ `[!warning]`（别为绕 https 关防护）+ `[!tip] 大白话`（门的比喻）+ `[!tip] 新手可跳过`（HTTPS / 反向代理） |
| 上册 §2.6 的 LA-4 提示 | 只写「关掉可绕强制 https」 | 末尾加「这两个键的**默认值与语义**见 §2.5」 |
| 本章小结 | 5 条 | 6 条（新增「四个防护开关默认都开着，公网访问请走 HTTPS / 反向代理」） |
| 脚注 | 第 2 章 45 条定义 | 新增 `[^c2-lb10-*]` 14 条 |
| frontmatter | `updated: 2026-10-07` | `updated: 2026-10-16` |
| 文末 | — | 新增 `## 更新记录`（1 行：2026-10-16 / LB-10） |

**补实/纠错的口径**（全部有源码默认值可核）：

- `WebUI\HostHeaderValidation` 默认 **`true`**（`preferences.cpp:1025`）、`WebUI\CSRFProtection` 默认 **`true`**（`:999`）——**关掉它们 = 拆掉默认开启的防护**。同时补上 `ClickjackingProtection`（`:986`）与 `SecureCookie`（`:1012`）两个同组开关，默认同样为 `true`。
- `WebUI\Address` 默认 `*`（`:855`，官方 tooltip 写明 `*` = IPv4 与 IPv6 都监听，`optionsdialog.ui:3777-3779`）；`WebUI\Port` 默认 `8080`（`:868`）；`WebUI\Username` 默认 `admin`（`:895`）。
- `HostHeaderValidation` 的用途有官方 tooltip 兜底：**防 DNS rebinding**（`optionsdialog.ui:4225-4229`）——此前只有「关掉可绕 https」这一面，现在有了「它本来在防什么」。
- HTTPS 默认**关**（`WebUI\HTTPS\Enabled`, `:1038`）、反向代理支持默认**关**（`WebUI\ReverseProxySupportEnabled`, `:1129`，官方 tooltip 说明是为了取 `X-Forwarded-For`，`optionsdialog.ui:4285-4287`）。
- `WebUI\Enabled` 的默认值由构建传入（`preferences.cpp:776` 为 `value(…, defaultValue)`），**未见固定常量，故写「不猜」**，未编造。

**新增来源件 LB-10**（primary，qBittorrent 源码 @ `df402f91d456`）：`sources/l1-10_webui-access-security-official-source.md`，逐字留档 `optionsdialog.ui` 的 WebUI 页字段串（含**完整多行 tooltip**）与 `preferences.cpp` 的 22 个 WebUI 配置键默认值。

> [!warning] 一处自查纠正（本增量开工时）
> LB-10 首次生成时，**多行 `<string>` 只截到第一行**（如 `IP address that the Web UI will bind to.` 之后的两行被丢掉，留下未闭合的 `<string>`）。已改为「进入 `<string>` 后一直取到 `</string>`」重生成。

## 校验

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 逐字引文回源（含新增 10 处） | `python3.12 .claude/scripts/note-citation-check.py workspace/qbittorrent-config-usage --mode verbatim --file "<vault 中册绝对路径>"` | 英文整句 **105** 处，原始来源命中 **105** / 仅中间产物 0 / **未命中 0** |
| 脚注配对（中册） | python 复核 | 引用 114 / 定义 94（去重 94/94）；lb7 22/22、lb8 6/6；无未定义、无孤立 |
| 结构自检 | `python3 .claude/scripts/check-md-structure.py <分册目录> <MOC>` | 扫描 10 个文件，**0 处可疑** |
| 双链解析 | `obsidian vault="项目" links path=…` | 总览 10 条、旧散记互链与图片全部解析；**0 未解析**（改前有 1 条悬空） |
| 副本一致性 | python `read_bytes()` 全量比对 4 组 | **4/4 逐字节一致**（vault ↔ `workspace/.../output/`） |

**增量 2（下册 §5.3）复核**

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 逐字引文回源（下册） | `python3 .claude/scripts/note-citation-check.py workspace/qbittorrent-config-usage --mode verbatim --file "<vault 下册绝对路径>"` | 英文整句 **89** 处，原始来源命中 **89** / 仅中间产物 0 / **未命中 0** |
| 脚注配对（下册，全文） | python 复核 | 引用 76 / 定义 76（去重）；新增 `c5-lb9-24 / 37 / 42 / 62` 定义 4/4 全被引用；无未定义、无孤立 |
| 结构自检（下册） | `python3 .claude/scripts/check-md-structure.py "<下册绝对路径>"` | 扫描 1 个文件，**0 处可疑** |
| 双链解析（下册） | `obsidian vault="项目" links path=…` | 出链 2 条全部解析；**0 未解析** |
| 副本一致性 | python `read_bytes()` | 下册 vault ↔ output **逐字节一致**（35,077 B） |

**增量 3（上册 §2.5）复核**

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 逐字引文回源（上册） | `python3 .claude/scripts/note-citation-check.py workspace/qbittorrent-config-usage --mode verbatim --file "<vault 上册绝对路径>"` | 英文整句 **82** 处，原始来源命中 **82** / 仅中间产物 0 / **未命中 0** |
| 脚注配对（上册） | python 复核 | 引用 59 / 定义 59（去重）；新增 `c2-lb10-*` 定义 **14/14** 全被引用；无未定义、无孤立 |
| 结构自检 | `python3 .claude/scripts/check-md-structure.py "<分册目录>"` | 扫描 9 个文件，**0 处可疑** |
| 双链解析（上册） | `obsidian vault="项目" links path=…` | 出链 2 条全部解析；**0 未解析** |
| 小节编号一致性 | `grep -rn "2\\.5\\|2\\.6"`（排除旧散记） | 目录 / 两处标题 / 两处正文引用 / 更新记录 **全部一致**，无残留「§2.5 动手实践」 |
| 副本一致性 | python `read_bytes()` | 上册 vault ↔ output **逐字节一致**（34,610 B） |

## 未处理风险 / 遗留

1. **`chapters/` 未同步**：`workspace/qbittorrent-config-usage/chapters/` 是**组装前形态**，
   与发布件本就不同形（六个章文件 + 引文对照在章末）。本次 §4.4 的改动**没有**回写章文件，
   因为回写需要重跑 `note-assembler` 才能保持 `output/` 一致；已按 note-updater 的边界如实留在沉默之外——
   若日后有人从 `chapters/` 重新组装，会**丢掉**本次 §4.4/§4.6 的全部补实、增量 2 的 §5.3 状态表，以及增量 3 的 §2.5 WebUI 安全节。
2. **workspace 同步方向已定：明确弃用 `chapters/`**（2026-10-16 用户确认，方案 B）。本次 vault 与
   `output/` 两侧都改了，`chapters/` 与 `_merge/` 未改，且**今后也不再追平**——已在
   `workspace/qbittorrent-config-usage/chapters/_RETIRED.md` 放下三行面包屑，写明「组装前形态 /
   自 2026-10-16 停止维护 / 权威稿见 `../output/` 与 vault / 要从头重装请以 `output/` 为源」。
   弃用而非回灌的理由：回灌要重做组装阶段的 16 处跨册引用改写 + 12 处 `##→###` 层级归一，
   等于把已验收的发布字节重新生成一遍，且追平后 `chapters/` **依然不是**发布源。
   该 run 已是 `current_phase: done`，`output/` 不会再被任何流程写；两边同名文件极易被误当权威稿，
   故在此登记。
3. **`workspace/music-tag-web/output/series/MusicTagWeb-06-附录A-播放侧与生态.md:221`** 有一条
   `[[qBittorrent的使用]]` 指向旧散记。该文件是**未发布的 workspace 草稿**，且其改动是用户既有未提交改动，
   本次**未动**。若它以后发布进 vault，该双链会落到 `旧散记/` 里的归档稿上。
4. **孤立内容未清理**：旧散记 `qBittorrent的使用.md` 的 frontmatter `tags` 里带 `MOC`，属历史遗留，
   未改（非本次范围）。
5. **`assets/` 下其它目录**（`SMB挂载-02-手动挂载`、`Tailscale子网路由器部署教程`、`linux如何修改网络信息`、
   `外网如何使用代理进行翻墙`、`硬盘教程和NAS硬盘知识讲解`）不在本次范围，未核查其引用。
6. **全库另有悬空双链**：多个已发布笔记引用 `[[docker/docker进行代理]]`，但该笔记在 vault 中不存在
   （只有 `workspace/update-docker/` 的草稿）。这是**跨分册**问题，本次只修了 qBittorrent 归档稿里的那一条。

## 来源件（新增）

| ID | 文件 | tier |
| --- | --- | --- |
| LB-7 | `sources/l2-7_proxy-official-source.md` | primary（qBittorrent 源码 @ `df402f91d456`） |
| LB-8 | `sources/l2-8_proxy-user-practice.md` | 用户自测（第一手，**非官方**） |
| LB-9 | `sources/l3-9_tracker-status-official-source.md` | primary（qBittorrent 源码 @ `df402f91d456`：Tracker 状态枚举 / 桌面版状态串 / WebUI 数值映射） |
| LB-10 | `sources/l1-10_webui-access-security-official-source.md` | primary（qBittorrent 源码 @ `df402f91d456`：WebUI 页字段串 + 22 个 WebUI 配置键默认值） |
