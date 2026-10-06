# 更新报告：小雅 fnOS 单容器部署 · 第 5 章（前端接入）

- 更新日期：2026-10-06
- 目标文件：vault `流媒体与影音/小雅 fnOS 单容器部署/05 前端接入.md`（拆分笔记第 5 章）
- destination_mode：`patch-in-place`，并**同步全部副本**（上游 `chapters/` + `output/` + vault）
- update_goal：回答用户新问题「**依旧用小雅的资源，但用夸克网盘会员**，该怎么办」

## 口径修正（重要）

- 初稿把答案写成「**放弃小雅库、改挂你自己的夸克库**」。
- 用户澄清：「**不是我的意思是，依旧是用小雅的资源，但是我是用夸克网盘会员**」。
- 因此重写 5.6 的**主答案**为：**小雅没有「把小雅资源播放到夸克」这个开关**——小雅的资源现在主要靠 **115** 播放（`ali2115.txt` / 阿里转存 115，需 115 会员；配置项 `ALIYUN_TO_115`），夸克在小雅里只是 `QUARK_COOKIE` 挂载**你自己的夸克**，**不能**把小雅资源转成夸克播放。
- 「改挂自己的夸克库（夸克网盘 TV 驱动 → SmartStrm → fntv-proxy 302）」保留，但**降级为 5.6.5 的备选路线**，不再是主答案。

## 变更摘要

| 位置 | 变更 |
| --- | --- |
| 第 5 章正文 | **重写** `## 5.6 没有阿里云盘会员、只有夸克会员怎么办`（5.6.1–5.6.5） |
| 本章小结 | 改写 1 条「没有阿里云盘会员」，落到「开关只有 115、夸克不能转」 |
| 引文对照 | 新增第 28–35 行（8 条逐字回源；既有 1–27 行保留） |
| 文末 | `## 更新记录`（2026-10-06）改写 |
| frontmatter | `updated` 仍为 2026-10-06（同日，无需改） |

## 5.6 新结构（修正后）

| 小节 | 回答 |
| --- | --- |
| 5.6.1 | 先分清「账号 ≠ 会员」：小雅必填的是阿里云盘**账号**，会员只影响**速度**（不付费即限速，实测 SVIP 仍 380kb/s） |
| 5.6.2 | **关键**：小雅的资源现在主要靠 **115** 播放（阿里转存 115，需 115 会员）；「换播放盘」的开关**只有 115，没有夸克**；两盘都无会员则限速到 ~100k |
| 5.6.3 | 夸克在小雅里是 `quark_cookie.txt` / `QUARK_COOKIE` **挂载你自己的夸克**，不是把小雅资源转成夸克；实测填了仍只有阿里直链 |
| 5.6.4 | 只有夸克会员时实际可选的三条路（忍限速 / 补 115 / 改挂自己的夸克库）+ 115 路线风险警告 |
| 5.6.5 | 备选：改挂**你自己的夸克库**（夸克网盘 TV 驱动 → SmartStrm → fntv-proxy 302）+ HLS 元数据坑 |

## 本次真正新增的知识点（不是只改称呼）

1. **「换播放盘」的开关只有 115**：「阿里转存 115」把小雅资源转存到你自己的 115 绕开阿里限速，**需 115 会员**（`sources/p4/ycyc-2878.md:13`、`:19`）。**没有 `ALIYUN_TO_QUARK`**。
2. **夸克在小雅里 ≠ 转存夸克**：它是「挂你自己的夸克」（`sources/forum/tid-8385880.md:26`），实测**填了夸克 cookie 日志里仍只有阿里直链**（`:30`）。所以「只有夸克会员」想「用小雅资源走夸克播放」**没有现成办法**。
3. **账号 ≠ 会员**：阿里云盘三件套是**必填**（`sources/01_club_fnnas_com.md:32`），但会员只决定速度；两盘都无会员会限速到 ~100k（`sources/forum/tid-21673.md:13`）。
4. **备选链路仍成立**：改挂**你自己的夸克库**时，夸克网盘 TV 驱动 → SmartStrm → fntv-proxy 302 照走（fntv-proxy 本就主要面向夸克），但片源换成「你自己夸克里的片」。
5. **夸克专属坑**：部分片源夸克只给 **HLS 转码流**，飞牛/Emby 取不到时长/码率/分辨率；代理只做 302，不转 mp4、不补元数据 → 用 TMDB 外部刮削。

## 同步范围（无漂移）

| 副本 | 状态 |
| --- | --- |
| `workspace/xiaoya-fnos-deploy/chapters/05_前端接入.md` | 已更新（上游源；309 行） |
| `workspace/xiaoya-fnos-deploy/output/05 前端接入.md` | 已机械重生成（327 行） |
| `workspace/xiaoya-fnos-deploy/output/final_note.md` | 已替换第 5 章块（1258 行） |
| vault `流媒体与影音/小雅 fnOS 单容器部署/05 前端接入.md` | 已同步（与 output/05 逐字一致） |

> 本项目以 `chapters/` 为唯一上游、`output/` 与 vault 为机械产物；本次四处一并更新，**未产生 vault / workspace 漂移**。

## 校验

- `note-citation-check.py workspace/xiaoya-fnos-deploy --vault-note <vault 05> --mode all` → **✅ 无硬失败**（V 逐字回源 4/4 命中；S4 引文对照表 0 处不合格；C 9 份副本 8 组比对 **0 差异**）。
- `check-md-structure.py <vault 05>` → **0 处可疑**（Callout 内无裸空行）。
- `output/05 前端接入.md` 与 vault `05 前端接入.md` → **逐字一致**。

## 追加更新（口径相关的其它副本）

用户手改了 vault `02 选型对比` 的 2.3.4（补「外网远程观影」小节），并同意同步总览与第 6 章指针。本次一并处理：

| 文件 | 变更 | 副本 |
| --- | --- | --- |
| `02_选型对比.md` | 2.3.4 完善「外网远程观影」小节：用对比表区分 **直接挂载（WebDAV）→ NAS 中转载流、吃上行带宽** 与 **STRM + 302 → 客户端直连、不过 NAS**（`sources/lens-b/mediawarp/01_github_com.md:53`），并保留「门牌号」大白话；末尾新增 `## 更新记录` | chapters / output / vault / final_note |
| `06_避坑清单.md` | 6.5 末尾加「→ 第 5 章 5.6」双链指针（回应「依赖阿里云盘」） | chapters / output / vault / final_note |
| `小雅 fnOS 单容器部署（总览）.md` | 章节目录第 5 条补「并单列一节回答『没有阿里云盘会员、只有夸克会员怎么办』」 | output / vault |

> 口径要点：**WebDAV 直接挂载**是另一条播放路径（NAS 拉流再中转，吃家里上行）；**STRM + 302**（第 5 章主线）才是「客户端直连网盘、不占 NAS 上行」的路。这也解释了用户手写那句「NAS 连夸克拉流再上传中转」的来由——它描述的是 **WebDAV 挂载路径**；而小雅库实际挂在阿里 / 115，成稿已按「网盘」泛化。

## 未处理 / 风险

- ~~**总览页**第 5 条未提 5.6~~ → **本次已补**。
- ~~**第 6 章**未加「→ 5.6」交叉指针~~ → **本次已补**。
- 115 / 夸克 路线属**社区实践**：115 转存有「非会员不支持 / >5G 不支持」的实测反馈（`sources/forum/tid-8385880.md:32`、`:34`），随平台策略变化，正文已按来源标注。
- 2.3.4 里「飞牛 WebDAV 挂载通常套不上 302、流量走 NAS 中转」是**用户基于飞牛实机经验的补充**，仓库内暂无第三方逐字来源；成稿已用「通常 / 一般」弱化，未当成定论。
- MOC 无需变更（索引指向总览页，未新增笔记）。

---

# 追加更新（2026-10-06）：夸克口径修正（用户主用夸克网盘）

- 触发：用户「**我主要就是用夸克网盘**，你看看哪些部分需要修改？」→ 选定 scope **B**（补定性 + 补凭据 + 修 5.6），不做全篇夸克化改写。
- destination_mode：`patch-in-place`，**同步全部副本**（上游 `chapters/` + `output/` + vault + `final_note.md`）。
- 新增来源存档：`sources/gh/alist-tvbox-721.md`（GitHub Issue power721/alist-tvbox#721 逐字节选）。

## 口径修正（重要）

上一轮把 5.6 的主答案写成「**小雅没有『把小雅资源播放到夸克』这个开关**」「夸克在小雅里只是挂载你自己的夸克」。**这个说法过于绝对**：
- 小雅**确有**一块**夸克分享区**（挂载目录 `/🌀我的夸克分享`，列表文件 `quarkshare_list.txt`，索引 `index.quark.txt`）——该区**走夸克直链、吃夸克会员速度**（`sources/gh/alist-tvbox-721.md:33`）。
- 修正为：**本体库（阿里 / 115）不能转夸克；但夸克分享区能走夸克**。前一轮「只有 `ALIYUN_TO_115`、没有 `ALIYUN_TO_QUARK`」的结论**只对本体库成立**，本轮已加限定语。
- 同时补「**覆盖以实机为准**」警示：小雅索引**默认只加载一部分**，夸克分享索引很可能不在默认之列，且大量目录路径失效（`sources/gh/alist-tvbox-721.md:16`、`:39`）。

> 用户此前给的「夸克覆盖 85%~90%」数字**无任何来源支撑**，判定为不可采信；正文一律不写覆盖率，只写「以实机为准」。

## 变更摘要

| 位置 | 变更 |
| --- | --- |
| `chapters/05_前端接入.md` | **重写 5.6**（5.6.1–5.6.5）：先分清「账号≠会员」→ 讲「本体库 + 分享区（含夸克）」→ 夸克的两条正路 + 一条走不通的路 + 覆盖警告 → 四条路对照表 → 备选链路；新增 引文对照 36–38 行、`## 更新记录` 加口径修正行 |
| `chapters/01_开篇定位.md` | 「资源在哪」段 + 名词表「小雅」行 + 本章小结：由「阿里云盘」放宽为「网盘（阿里 / 115，另有夸克等分享区）」，并指 5.6 |
| `chapters/03_动手前准备.md` | 3.3 标题 + 章首清单：加「可选夸克 / 115」；正文新增「可选凭据」块（`QUARK_COOKIE` / `quark_cookie.txt` / `PAN115_COOKIE`）；本章小结加 1 条；引文对照加 21–22 行 |
| `chapters/04_部署实战.md` | monlor Compose 块补齐 `QUARK_COOKIE` / `PAN115_COOKIE`（来源本就有，此前遗漏）；要点加 1 条；引文对照加 20 行 |
| `chapters/06_避坑清单.md` | 6.5 指针的可选路补「**用小雅的夸克分享区**」 |
| `流媒体与影音/小雅 fnOS 单容器部署/小雅 fnOS 单容器部署（总览）.md` | 章节目录第 5 条补「（含小雅自带的夸克分享区与备选链路）」 |

## 同步范围（无漂移）

| 副本 | 状态 |
| --- | --- |
| `chapters/{01,03,04,05,06}` | 已更新（上游源） |
| `output/{01,03,04,05,06}  *.md` | 已机械重生成（header + 新章体 + footer） |
| `output/final_note.md` | 已按 7 章重拼（并入新 5.6） |
| vault `流媒体与影音/小雅 fnOS 单容器部署/{01,03,04,05,06} *.md` | 已同步（与 output 逐字一致） |

> 生成前先在 pristine 副本上**验证拼接模型**：对全部 7 章，`output/NN` 与 `final_note.md` 的块用「header + 章体 + footer」重建均**逐字节复现**，再对 01/03/04/05/06 套用同一模型 → 交付时副本零漂移。

## 校验

- `note-citation-check.py workspace/xiaoya-fnos-deploy --vault-note <vault 05> --mode all` → **✅ 无硬失败**（V 英文整句回源 4/4；S4 引文对照表 0 处不合格；C 9 份副本 8 组比对 **0 差异**）。S1=0；S2=8 处 LCS=5「的夸克分享」为同一术语在多副本中的正常重复；S3=2 个为既有专名。
- `check-md-structure.py` × 5 个编辑章 → 均 **0 处可疑**（Callout 内无裸空行）。
- 新增引文的来源行已逐条 `sed -n` 复核（`01_club_fnnas_com.md:48`、`tid-9690.md:48-49`、`tid-8385880.md:26/30`、`gh/alist-tvbox-721.md:16/33/39`）。

## 未处理 / 风险

- 第 2 章「下一章预告」仍写「凭据（阿里云盘三件套 + WebDAV 账号）」——夸克是**可选**项，该措辞不算错，**按 scope 未改**。
- 第 7 章（运维）未动。
- 夸克分享区的**实际片量 / 可搜性无任何来源给出比例**，成稿只写「以实机为准」；用户若实测出稳定数字，可另立来源件后再回写。

---

# 追加更新：小雅 fnOS 单容器部署 · 第 3 章（动手前准备）

- 更新日期：2026-10-06
- 目标文件：vault `流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md`（拆分笔记第 3 章）
- destination_mode：`patch-in-place`，并**同步全部副本**（上游 `chapters/` + `output/` + `final_note.md` + vault）
- update_goal：用户追问「**如何获取这些阿里云盘三件套**」——3.3 原文只写了**文件名与放置位置**，**未写获取方式**

## Stale Map

| 处理 | 内容 |
| --- | --- |
| 保留 | 3.1 / 3.2 / 3.4 / 3.5 全部结构；3.3 既有四张表与全部 Callout；引文对照第 1–22 行 |
| 新增 | 3.3 内「**那么这三样怎么拿到？**」段（三步表 + 对照 + `[!warning]` 两个提醒 + `[!tip]` 大白话）；引文对照第 23–29 行；文末 `## 更新记录` |
| 改写 | 无 |
| 删除 | 无 |

## 本次新增内容（全部回源）

| 论点 | 出处 |
| --- | --- |
| 三步拿法：解码站取 32 位 `mytoken.txt` | `sources/p3/gnz48/01_www_cnblogs_com.md:26-29` |
| `request.html` 扫码取 Open Token（280 位） | `sources/p3/gnz48/01_www_cnblogs_com.md:30` |
| 资源盘建文件夹取 folder id | `sources/p3/gnz48/01_www_cnblogs_com.md:31` |
| 另一份教程「获取方式」对照 + 「先转存小雅分享」 | `sources/p3/z-addone/01_www_cnblogs_com.md:21-25` |
| 论坛楼主答复 = `request.html` | `sources/01_club_fnnas_com.md:904` |
| token 第二天失效（单条用户反馈） | `sources/01_club_fnnas_com.md:157` |

> **未采纳**：上一轮答复里提到过「网页 `F12` → Local Storage → `refresh_token`」这条路，因 `sources/` 无对应来源件，按「出处宁空不猜」**未写入笔记**。

## 同步范围

| 副本 | 状态 |
| --- | --- |
| `workspace/xiaoya-fnos-deploy/chapters/03_动手前准备.md` | 已更新（上游源） |
| `workspace/xiaoya-fnos-deploy/output/03 动手前准备.md` | 已同步 |
| `workspace/xiaoya-fnos-deploy/output/final_note.md` | 已替换第 3 章块 |
| vault `流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md` | 已同步 |

> vault 侧 03 章在本轮之前已带 frontmatter / 导航 / 表格对齐等**美化层**（与 `chapters/` 朴素格式本就不同形态）；本次三处插入的**新增文本一致**。

## 校验

- `note-citation-check.py workspace/xiaoya-fnos-deploy --vault-note <vault 03> --mode all` → **✅ 无硬失败**（V 英文整句回源 4/4；S4 引文对照表 0 处不合格；C 9 份副本 8 组比对 **0 差异**）。S3 新增 1 处 `folder id`（术语保留类，与既有表格写法一致）。
- `check-md-structure.py <vault 03>` → **0 处可疑**。
- 新增 7 条引文均按 `sed -n` 逐字复核（`p3/gnz48/01_www_cnblogs_com.md:26/29/30/31`、`p3/z-addone/01_www_cnblogs_com.md:25`、`01_club_fnnas_com.md:157/904`）。

## 未处理 / 风险

- 总览页第 3 章一句话说明（「凭据文件准备清单」）仍准确，**未改**。
- 第 2 章「下一章预告」「凭据（阿里云盘三件套 + WebDAV 账号）」与本轮一致，**未改**。
- 第 4 / 6 / 7 章未动；第 4 章既有「token 会过期要更新」的说法与新增 `:157` 反馈同向，无需修正。
- 第三方解码站 `media.cooluc.com` 属社区工具，笔记只记「有风险、官方扫码更稳」，**不为其可用性背书**。

---

# 追加更新：第 3 章 · 把「扫码法（方案 A）」写进 3.3

- 更新日期：2026-10-06
- 目标文件：vault `流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md`（拆分笔记第 3 章）
- destination_mode：`patch-in-place`，**同步全部副本**（上游 `chapters/` + `output/` + `final_note.md` + vault）
- update_goal：用户反馈「**还是不会操作，有更简单详细的方法吗？**」→ 选定**方案 A（手机扫码）**，要求「放入笔记」

## 触发与口径

- 上一轮 3.3「怎么拿」第 1 步给的是「登录网页版 → 按 `F12` → 复制 `login.do?appName=aliyun` 响应 → 丢进第三方解码站 `media.cooluc.com/decode_token/` 解码」。这条对新手门槛高，且**已被阿里云盘接口变更淘汰**。
- 本轮改为：**第 1、2 样都走手机扫码**（方案 A，主推）；F12 + 解码站法**降为备选（方案 B）**，并明说它很可能已失效。
- 新增来源件（此前 `sources/` 无对应件，按项目引用规范补档）：
  - `sources/p5/slarker/01_wiki_slarker_me.md:29-31`（「影音资源库 - 小雅部署教程」的准备一节）
  - `sources/p5/wsisp/01_www_wsisp_com.md:11/17/21-25`（「飞牛NAS小雅资源消失？三步搞定Docker配置与阿里云盘Token更新！」）

## 变更摘要（3.3）

| 位置 | 变更 |
| --- | --- |
| 3.3「怎么拿」引言 | 改为「前两样都走**手机扫码**（方案 A，主推）；旧 F12 法（方案 B）已被淘汰」 |
| 3.3 三步表 | 第 1 行 `mytoken.txt` 由「F12 + 解码站」改为「AList 文档阿里云盘页**手机扫码**」（`p5/slarker/01_wiki_slarker_me.md:29`）；第 2 行 `myopentoken.txt` 出处补 slarker:30；第 3 行不变 |
| 3.3 正文 | 新增「近期教程扫码流程细化」段（`p5/wsisp/01_www_wsisp_com.md:21-25`）；原 z-addone 对照段顺移其后并微调引语 |
| Callout | 新增 `[!note]` **位数差异**（token 32 vs 40 位；OpenToken 280 vs 288~335 位，均并列、不裁断）；`[!warning]` 由**两条**改为**三条**：① token 有效期 2~3 个月 + 扫码「二次确认」（`p5/wsisp/01_www_wsisp_com.md:11`）② 旧方法失效（`p5/wsisp/01_www_wsisp_com.md:17`）③ 第三方工具留意；`[!tip]` 改「前两样都靠**手机扫码**换取」 |
| 引文对照 | 新增第 30–37 行（8 条逐字回源；既有 1–29 行保留） |
| 本章小结 | 新增 1 条「**三件套怎么拿**」 |
| 文末 | `## 更新记录` 追加一行 |

## 依据（新增内容全部回源）

| 论点 | 出处 |
| --- | --- |
| 32 位 token 用**手机 App 扫码**获取 | `sources/p5/slarker/01_wiki_slarker_me.md:29` |
| OpenToken 扫码获取（288~335 位） | `sources/p5/slarker/01_wiki_slarker_me.md:30` |
| 中转文件夹目录 ID | `sources/p5/slarker/01_wiki_slarker_me.md:31` |
| **旧「复制网页代码」法已失效** | `sources/p5/wsisp/01_www_wsisp_com.md:17` |
| 扫码流程五步（出二维码 → 扫码 → 授权 → 显示字符串 → 存 `mytoken.txt`） | `sources/p5/wsisp/01_www_wsisp_com.md:21-25` |
| token 有效期 2~3 个月 / 扫码后须二次确认 | `sources/p5/wsisp/01_www_wsisp_com.md:11` |

## 同步范围（无漂移）

| 副本 | 状态 |
| --- | --- |
| `workspace/xiaoya-fnos-deploy/chapters/03_动手前准备.md` | 已更新（上游源） |
| `workspace/xiaoya-fnos-deploy/output/03 动手前准备.md` | 已同步 |
| `workspace/xiaoya-fnos-deploy/output/final_note.md` | 已替换第 3 章块 |
| vault `流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md` | 已同步 |

> 本轮编辑用「标记区间替换 + 同文本追加」在四处写入**逐字相同**的新增文本；vault 侧既有表格由 Obsidian 自动对齐，新增区块保持紧凑写法。

## 校验

- `note-citation-check.py workspace/xiaoya-fnos-deploy --vault-note <vault 03> --mode all` → **✅ 无硬失败**（V 逐字回源 4/4；S4 引文对照表 0 处不合格；C 9 份副本 8 组比对 **0 差异**）。S3 新增/保留 `Open Token`、`folder id` 均为术语保留类。
- `check-md-structure.py <vault 03>` → **0 处可疑**（Callout 内无裸空行）。
- 新增 8 条引文均对文件逐字核对（`p5/slarker/01_wiki_slarker_me.md:29/30`、`p5/wsisp/01_www_wsisp_com.md:11/17/23/24/25`）。

## 未处理 / 风险

- 「AList 文档阿里云盘页」是否稳定提供**扫码**入口，本轮只按 `p5/slarker/01_wiki_slarker_me.md:29` 的记录转述；若该页改版，以实机页面为准。
- 位数差异（32/40、280/288~335）**未裁断**，按项目「来源冲突并列保留」处理。
- 总览页第 3 章一句话说明、第 2 章预告仍准确，**未改**。
- 第 4 / 6 / 7 章未动。

---

# 追加更新：第 3 章 · 3.3「可选凭据」补「夸克 cookie 怎么拿」

- 更新日期：2026-10-06
- 目标文件：vault `流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md`（拆分笔记第 3 章）
- destination_mode：`patch-in-place`，**同步全部副本**（上游 `chapters/` + `output/` + `final_note.md` + vault）
- update_goal：用户「**夸克网盘 cookie 如何的**」→「**放入**」；3.3 原文只写了夸克 cookie **放哪**，没写**怎么拿**

## 依据（新增内容全部回源）

| 论点 | 出处 |
| --- | --- |
| 夸克 cookie 拿法：`F12` → 网络 → 找一个携带 `Cookie` 参数的请求 → 复制 | `sources/p5/alist-docs/01_raw_githubusercontent_com.md:47`（AList 官方文档 `docs/zh/guide/drivers/quark.md` 原文） |
| **必须用 Chrome**：Firefox 取的 cookie 会停在访客态 | `sources/p5/alist-docs/01_raw_githubusercontent_com.md:63` |
| `__puus` 会话 cookie 约 3 小时过期；过期后列表正常、下载 403，重启才恢复 | `sources/gh/alist-9596.md:11`（AlistGo/alist PR #9596 正文） |
| 「填了夸克 cookie 却只有阿里直链」的现场反馈 | `sources/forum/tid-8385880.md:30` |

新增来源存档：
- `sources/p5/alist-docs/01_raw_githubusercontent_com.md`（AList 官方文档夸克驱动页，raw Markdown 逐字存档）
- `sources/gh/alist-9596.md`（AlistGo/alist PR #9596 正文）

## 变更摘要

| 位置 | 变更 |
| --- | --- |
| 3.3「可选凭据」 | 在「夸克 cookie 管的是…」之后新增「**夸克 cookie 怎么拿？**」段（官方文档逐字引用 + 四步操作）与 `[!warning]` **抓夸克 cookie 的两个坑**（Chrome；约 3 小时过期 → 下载 403） |
| 引文对照 | 新增第 38–40 行（38/39 取自 AList 文档，40 为 PR 英文整句 + 中译） |
| 本章小结 | 「夸克 / 115 属可选凭据」条补「用 **Chrome + `F12`** 手抓、约 3 小时会过期」 |
| 文末 | `## 更新记录` 追加一行 |

## 同步范围

| 副本 | 状态 |
| --- | --- |
| `workspace/xiaoya-fnos-deploy/chapters/03_动手前准备.md` | 已更新（上游源） |
| `workspace/xiaoya-fnos-deploy/output/03 动手前准备.md` | 已同步 |
| `workspace/xiaoya-fnos-deploy/output/final_note.md` | 已替换第 3 章块 |
| vault `流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md` | 已同步 |

## 校验

- `note-citation-check.py … --mode all` → **✅ 无硬失败**（V 英文整句回源 **7/7**；S4 引文对照表 0 处不合格；C 9 份副本 8 组比对 **0 差异**）。
- `check-md-structure.py <vault 03>` → **0 处可疑**。

## 过程中的两个坑（已修，记录在案）

1. **引文表反引号嵌套**：第 38 行原文本身含 `` `Cookie` ``，若整格再用单反引号包裹会嵌套破格。已把第 38、40 行的「原文」格改用**双反引号**定界。
2. **vault 漂移（重要）**：第一轮「扫码法」写入后 C 比对曾为 0 差异，但本轮开始时发现 **vault 少了第一轮插入的一整段**（近期教程段 / `[!note]` 位数 / 另一份教程段 / `[!warning]` 三个提醒），而 `chapters/` 与 `output/` 完好——典型是**笔记在 Obsidian 中打开、其内存缓冲回写覆盖了磁盘**。已用「从 `chapters/` 提取同一段落原样补回 vault」的方式修复，并复跑 C 比对至 **0 差异**。
   - 教训：**vault 侧笔记若正在 Obsidian 中打开，多次快速写盘可能被其缓冲回写吞掉**；每轮改完必须跑 C 比对，不能只信当次写入成功。

## 未处理 / 风险

- AList 文档已从 `alist.nn.ci` 307 跳转到 `alistgo.com`；本轮存档取的是 **raw.githubusercontent.com/AlistGo/docs** 的原文，站点改版不影响存档。
- GitHub API 返回的 PR 标题存在**截断伪影**（标题被切在 70 字符处、余下片段落到正文首行）；已按两半拼接还原完整标题，正文引用的关键句（`:11`）未受截断影响。
- 夸克 cookie 的**实际有效期随平台策略变化**，正文按官方 PR 口径写「约 3 小时」，未当定论。
