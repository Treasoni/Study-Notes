# 更新报告：小雅 fnOS 单容器部署 · MediaWarp 302 口径修正（第 5 章 + 第 2 章）

- 更新日期：2026-10-06
- 目标文件：vault `流媒体与影音/小雅 fnOS 单容器部署/05 前端接入.md`、`…/02 选型对比.md`
- destination_mode：`patch-in-place`，并**同步全部副本**（上游 `chapters/` + `output/` + `final_note.md` + vault）
- update_goal：回答用户「**让 302 串起来：MediaWarp 与 fntv-proxy 站在哪一环**」，并落到「**这里我想用 MediaWarp**」

## 触发与决策

- 用户在 `05 前端接入.md` 选中「MediaWarp」，问两者在 302 链路里的**位置关系**，并明确要**用 MediaWarp**。
- 两轮确认（AskUserQuestion）：
  1. 5.4 改法 → **改成以 MediaWarp 为主**（fntv-proxy 降为轻量备选）。
  2. 范围与深度 → **第 5 章 + 第 2 章一起修**（第 2 章建立在同一误判上，否则两章互相矛盾）；**加实操骨架**（官方 compose / `server.type: FNTV` / 端口 / HTTPStrm·AlistStrm 选择）。

## 口径修正（重要）

- 本笔记早前把 MediaWarp README 的「适配 飞牛影视」读成**待办项**，据此在两章判「成熟度未决 / 网盘转码仍是待办」。
- **误判根源**：旧抓取存档 `sources/lens-b/mediawarp/01_github_com.md` 由 GitHub HTML 转文本，TODO LIST 的 checkbox 状态在转换中丢失，`- [x]` 被渲染成裸 `*` 项。
- 核对 raw Markdown 后确认：该行原文是 **`- [x] 适配 飞牛影视`（已完成）**，紧随的 `- [x] 支持播放网盘转码内容（仅飞牛影视 AlistStrm 模式）` 亦已完成。
- **更正结论**：MediaWarp 与 fntv-proxy 站**同一环**（客户端 ↔ 飞牛影视之间的前置反向代理），MediaWarp **已正式支持**飞牛影视。两者差别只在能力与配套：只要 302 选 fntv-proxy；要屏蔽客户端 / 注入脚本 / 飞牛侧网盘转码，选 MediaWarp。

## 新增来源存档

| 文件 | 内容 |
| --- | --- |
| `sources/lens-b/mediawarp/02_readme_todo.md` | README TODO LIST 的 **raw Markdown 重抓**，保留 `- [x]`/`- [ ]` 状态（补正 01 件的 checkbox 丢失） |
| `sources/lens-b/mediawarp/03_blog_akimio_top.md` | 官方教程文档（作者博客）清洗稿，含 compose、`type: FNTV`、HTTPStrm/AlistStrm、Web 不支持 FNTV |

## 变更摘要

| 位置 | 变更 |
| --- | --- |
| `05 前端接入.md` **5.4** | **整节重写**：标题〈让 302 串起来：MediaWarp 与 fntv-proxy 站在哪一环〉；两工具对照表；`[!note]` **一处旧结论的更正**（MediaWarp 已支持飞牛影视） |
| `05` **5.4.1** | 为什么选 MediaWarp：官方定位逐字 + 说人话（能直连就直连、直连不了回退推流）+ 额外能力（屏蔽客户端 / 注入脚本 / AlistStrm 转码）；`[!warning]` **Web 美化对飞牛影视不生效** |
| `05` **5.4.2** | 部署骨架：官方 Compose（0.2.0）+「只支持 YAML」+「以 `config.yaml.example` 为准」+ `server.type: FNTV` |
| `05` **5.4.3** | HTTPStrm vs AlistStrm：对照表（谁需要能访问目标）+ `raw_url: true` 建议 + 选择口诀 |
| `05` **5.4.4** | fntv-proxy 轻量备选：`docker-compose.yml` 节选 + `[!tip]` 快递中转比喻 + `[!warning]` STRM 目录必须挂进容器且前后路径一致 |
| `05` 本章小结 | 「接 302 用中间件」条改写：MediaWarp 作首选（已适配 / `type: FNTV`），fntv-proxy 作备选，点明**同一环** |
| `05` 引文对照 | 原第 14 行改为 `[x]` 口径，新增 15–17（HTTPStrm/AlistStrm、定位话术、Web 不支持 FNTV） |
| `05` 更新记录 | `## 更新记录` 追加口径修正行 |
| `02 选型对比.md` **2.5** | 标题 `## 2.5 飞牛影视可作前端的旁证`；结论由「未决」改为**已确证**；`[!note]` 更正式 |
| `02` **2.2 表** | 「网盘转码支持仍是待办」→「AlistStrm 模式下支持网盘转码内容」 |
| `02` **2.3.3** | 「飞牛侧网盘转码仍是待办」段改写为「MediaWarp 已完成适配」 |
| `02` 小结 | 两条改写：「旁证与未决并列」→「旁证已确证」 |
| `02` 引文对照 | 原第 13 行改为 `[x]` 口径并新增 14 |
| `02` 更新记录 | `## 更新记录` 追加口径修正行 |

## 引用行号修正（本次收尾）

初稿的存档**行号凭印象书写**，与存档实际行号不符。已按存档逐条对齐（**单次正则映射**完成，避免 `33→38` 与 `38→45` 级联）：

| 引用 | 原（错） | 改（实际） |
| --- | --- | --- |
| `02_readme_todo.md` 适配飞牛影视 | `:25` | `:23` |
| `02_readme_todo.md` 网盘转码（AlistStrm） | `:26` | `:24` |
| `02_readme_todo.md` 功能节 | `:33` | `:38` |
| `02_readme_todo.md` HTTPStrm | `:36` | `:44` |
| `02_readme_todo.md` AlistStrm | `:38` | `:45` |
| `03_blog_akimio_top.md` 定位话术 | `:31` | `:34` |
| `03_blog_akimio_top.md` compose | `:62-73` | `:67-77` |
| `03_blog_akimio_top.md` 只支持 YAML | `:76` | `:92` |
| `03_blog_akimio_top.md` config.yaml.example | `:80` | `:86` |
| `03_blog_akimio_top.md` MediaServer.Type | `:96` | `:98` |
| `03_blog_akimio_top.md` `type: FNTV` | `:100` | `:111` |
| `03_blog_akimio_top.md` raw_url 建议 | `:114` | `:133` |
| `03_blog_akimio_top.md` Web 不支持 FNTV | `:129` | `:143` |

> `01_github_com.md:51/53`、`fntvproxy/01_github_com.md:44/45/71/139` 经复核**本就正确**，未改。

## 同步范围（无漂移）

| 副本 | 状态 |
| --- | --- |
| `workspace/xiaoya-fnos-deploy/chapters/{02,05}` | 已更新（上游源） |
| `workspace/xiaoya-fnos-deploy/output/{02,05}  *.md` | 已机械重生成 |
| `workspace/xiaoya-fnos-deploy/output/final_note.md` | 已替换第 2、5 章块 |
| vault `流媒体与影音/小雅 fnOS 单容器部署/{02,05} *.md` | 已同步（与 output 逐字一致） |

## 校验（全部通过）

- `publish_copies.py --check`（7 章）→ **全 `output==` 与 `vault==`**。
- `assemble_final.py --check` → **需更新 0 章**。
- `note-citation-check.py workspace/xiaoya-fnos-deploy --mode all --vault-note <vault 目录>` → **✅ 无硬失败**：V 英文整句逐字回源 **6/6 命中、0 未命中**；S1=0；S4 引文对照表 **0 处不合格**；C **8 份副本、7 组比对、0 差异**。
  - S2=10 处为「适配飞牛影视」「的夸克分享」等**术语/引文在多副本中的正常重复**；S3 去重 4 个为既有专名（`Docker Compose`、`raw Markdown`、`Open Token`、`folder id`），均属保留类。
- `check-md-structure.py`（02/05 + final_note）→ **0 处可疑**（Callout 内无裸空行）。

## 并发说明（已解除）

- 本轮期间同一笔记集上并行运行 `batch-note-update-flow`（run `update-xiaoya-fnos-routes`），该 run **现已完成**（`quality_gate: passed`），不会继续写文件。
- 两者编辑面不重叠（该 run 编辑第 1/3/4/7 章与入口页，05 全程跳过）；共享写点仅合并件 `output/final_note.md`（幂等重装配）。
- 该 run 的日志与本报告互相登记：其「跳过文件」表原称 `02/05` 未触碰，现由本轮改动，已在 `03_batch_update_log.md` 追加**外部改动登记**。

## 未处理 / 风险

- MediaWarp 属**社区工具**（作者 AkimioJR），配置**版本间字段差异较大**、处于初期迭代；正文已用「以发布版本中的 `config.yaml.example` 为准」限定，未对稳定性背书。
- 飞牛影视**不支持 Web 页面美化**（官方原话），已在 5.4.1 `[!warning]` 标注；冲美化去的用户会落空。
- fntv-proxy 端口与「基于飞牛影视 0.9.3」口径来自原帖，**随其版本更新可能变化**，正文按来源标注。
- MOC 无需变更（未新增笔记，索引指向总览页）。
