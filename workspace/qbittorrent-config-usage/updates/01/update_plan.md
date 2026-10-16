---
note_set: qBittorrent 配置与使用（三册 + 总览）
run: qbittorrent-config-usage
date: 2026-10-16
destination_mode: patch-in-place（vault 成品就地改；workspace output 同步镜像）
moc_path: 流媒体与影音/流媒体与影音 MOC.md
---

# update_plan — qBittorrent 配置与使用

## 形态判定

**拆分笔记集合**：1 总览 + 3 册（上册 第 1–2 章 / 中册 第 3–4 章 / 下册 第 5–6 章），
发布位置 `流媒体与影音/qBittorrent 配置与使用/`，项目内镜像在
`workspace/qbittorrent-config-usage/output/`。

**本次受影响文件集**

| 文件 | 动作 |
| --- | --- |
| `02 qBittorrent 配好.md`（中册） | **改写** §4.4 / §4.6 / 本章小结 / 引文对照 / 脚注 / `updated` / 新增 `## 更新记录` |
| `qBittorrent 配置与使用（总览）.md` | **改写**「另有一组更早的散记」Callout（改为双链 + 归档口径） |
| `01 qBittorrent 是什么与装起来.md`（上册） | **不改**——其措辞不因本次代理口径而错；代理字段不在上册 |
| `03 qBittorrent 用起来.md`（下册） | **不改**——同上；下册的分享率 / 排错不涉代理字段 |
| `旧散记/`（4 篇，由 `qBittorent/` 迁入） | **新增归档标记** + 拼写/乱码/悬空双链修复 |
| `流媒体与影音 MOC.md` | 追加 1 条归档索引（挂在 qBittorrent 分册条目下） |
| `workspace/.../chapters/*.md` | **不动**（组装前形态；改动需重跑 note-assembler，本次不重跑） |
| `workspace/.../output/*` | 与 vault 逐字节同步（4/4） |

## stale map

### 保留

- 中册 §4.1–4.3、§4.5：与本次口径无关。
- 三册 frontmatter 除 `updated` 外全部字段。
- 旧散记的正文与结构：**只加归档提示与修错，不重写**（`note-style.md`「更新不降级」）。

### 需要更新

| # | 位置 | 过时点 | 处置 |
| --- | --- | --- | --- |
| U1 | 中册 §4.4 | 标题与正文写「字段来源薄弱（标注）」，只给「接入点在哪」，**不给任何字段** | 改为**以源码为准**：补 ① 界面字段全表（类型四选一、主机、端口、认证组、hostname 回查、四类用途开关）+ ② 可照抄取值表（且明确是**别人环境的实测值**）+ ③ 生效判据表 |
| U2 | 中册 §4.4 的定性结论 | 旧散记把「P2P 数据下载通常不经过代理」写成**无条件结论** | 按官方源码 tooltip 口径限定作用范围：「只有**不勾** `Use proxy for peer connections` 时，代理才仅用于 tracker 连接」 |
| U3 | 中册 §4.6 | 「可以照填」的清单里没有代理，读者不知道该不该手改 `qBittorrent.conf` | 新增 ⑤ 代理的配置键表（`Network/Proxy/*`、`Profiles/BitTorrent|RSS|Misc`）+ 默认值≠推荐值的提示 |
| U4 | 中册本章小结 | 有一条「代理只给接入点（来源薄弱）」 | 换成两条（字段以源码为准 / 作用范围） |
| U5 | 中册 `updated` | `2026-10-07` | → `2026-10-16`；并追加 `## 更新记录` |
| U6 | 总览「另有一组更早的散记」 | 写「仓库顶层 `qBittorent/`…**保持原位不动**」 | 改为本目录 `旧散记/` 子文件夹 + 4 条双链 + 已归档口径 |
| U7 | 旧散记 4 篇 | 无归档标识，与成品口径冲突 | 文首加 `> [!warning] 已归档（旧散记）`（含指向总览的双链 + 各自的具体过时点）；frontmatter 加 `status: archived`、`updated: 2026-10-16` |
| U8 | 散点（结构性） | 笔记「散」的根因是**缺互链**：MOC 无索引、旧散记无回链 | 旧散记迁入分册目录；总览加双链；MOC 加 1 条归档索引 |

### 需要删除

| # | 位置 | 理由 |
| --- | --- | --- |
| D1 | `qBittorent/`（顶层，拼写有误） | 迁入 `流媒体与影音/qBittorrent 配置与使用/旧散记/`，同时修拼写 |
| D2 | `assets/qBittorent的Tracker/` | 其中 `file-20260202223827013.png` 全库零引用（孤儿） |
| D3 | `assets/qBittorent配置代理/` | 2 张图已复制到 `旧散记/assets/qBittorrent配置代理/`（原引用路径一直指不到这里，属历史断链），原目录随后零引用 |
| D4 | `旧散记/qBittorrent配置代理.md` 里的 `[[docker进行代理#2.3 …]]` | 目标笔记**从未发布进 vault**（只在 `workspace/update-docker/` 有草稿），悬空双链 → 改为白话表述 |
| D5 | `sources/_raw/proxyconfigurationmanager.h`（14 B） | 内容为 `404: Not Found` 的抓取残留 |

### 需要新增

| # | 位置 | 内容 |
| --- | --- | --- |
| N1 | `sources/l2-7_proxy-official-source.md` | 代理字段与配置键的**官方源码逐字片段**（LB-7，primary） |
| N2 | `sources/l2-8_proxy-user-practice.md` | 旧散记《qBittorrent配置代理》的**逐字留档**（LB-8，用户自测，非官方） |
| N3 | 中册 §4.4 的三张表 + 引文对照 10 行 + 脚注 28 条（lb7×22 / lb8×6） | 见 U1–U4 |
| N4 | 中册文末 `## 更新记录` | 本次变更留痕 |

## 最小资料收集

只补代理字段这一处缺口，**不为其它章节再搜**。

| 来源 ID | 载体 | 用途 | 层级 |
| --- | --- | --- | --- |
| LB-7 | `qbittorrent/qBittorrent` @ master `df402f91`：`src/gui/optionsdialog.ui`（4454 行）、`src/base/net/proxytype.h`（48 行）、`src/base/net/proxyconfigurationmanager.cpp`（106 行）、`src/base/preferences.cpp`（2222 行） | 字段名、下拉取值、配置键、工厂默认值、四类用途开关 | primary |
| LB-8 | 旧散记 `qBittorent/qBittorrent配置代理.md`（逐字截取） | 唯一有「可照抄取值」的一手材料（作者本人环境） | 用户自测（非官方） |
| 既有 `l2-1_options-explained.md:105` | 官方选项说明页 | **反证**：该页只给一句说明句、**不列字段**，故字段一律回源码 | primary |

## 口径纪律

- 字段名 / 配置键 / 默认值：**只写 LB-7 逐字给出的**（例：默认端口 `8080`、默认主机 `0.0.0.0`、`ProxyType::None`、`HostnameLookupEnabled` 默认 `true`）。
- 具体填什么值：**只有 LB-8 这一个合法来源**，且必须在正文里标注「这是**别人的**实测值，照抄一定不通」。
- 不编造 INI 片段：§4.6 只给配置键 + 默认值，**不给**「照抄就能用」的 `qBittorrent.conf` 代码块。
- 定性结论一律把**作用范围写进句子本身**。

## 增量 2（2026-10-16）：下册 §5.3 Tracker 状态表

用户在「第 0/1/2 步」之后追加确认：先做**低风险、可逐字取证**的那一项——把旧散记《qBittorrent的Tracker》里的**状态表**补进成品。

| # | 位置 | 处置 |
| --- | --- | --- |
| V1 | 下册 §5.3 标题 / 目录条目 | 由 `Tracker：公告地址与公共列表（F11）` 改为 `…公告地址、公共列表与界面状态（F11）`。**不改小节编号**——新增独立小节会连带把 5.4/5.5 重排，并牵动 §5.1 表格与 §5.1 提示里对「5.4」的两处交叉引用，风险高于收益 |
| V2 | 下册 §5.3 末尾 | 新增状态对照表（7 行）+ `[!warning]` 补漏 + `[!note]` 桌面版两条说明串 + `[!tip] 大白话` |
| V3 | 下册 本章小结 / 脚注 / `updated` / `## 更新记录` | 各追加 1 条 / 4 条 `c5-lb9-*` / 改日期 / 新增 1 行 |
| V4 | `sources/l3-9_tracker-status-official-source.md` | 新增来源件 LB-9（primary，三处逐字片段） |

**口径纪律（本增量）**：状态串、枚举数值、`Updating` 的标记性质，**只写 LB-9 逐字给出的**；**不写**任何「某状态该怎么办」的处置建议（无来源，故不写）。桌面版独有的两条说明串必须写明「仅桌面版」。
