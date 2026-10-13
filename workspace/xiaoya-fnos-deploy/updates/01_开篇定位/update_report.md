# ch01 更新报告

| 项 | 值 |
| --- | --- |
| note_id | `ch01` |
| 源文件 | `chapters/01_开篇定位.md` |
| 动作 | update |
| 输出模式 | patch-in-place（`updated_note` 即 `chapters/01_开篇定位.md`） |
| 发布副本 | `output/01 开篇定位.md`、`流媒体与影音/小雅 fnOS 单容器部署/01 开篇定位.md` |
| 标题变更 | 无（保持「第 1 章 开篇定位——小雅是什么，这篇要解决什么问题」） |
| 复核查验 | 待 P5 统一执行（`check-md-structure.py` + 引文回源） |

## 完成项

- 1.1 资源层描述换源：不再挂 monlor README 组件注释，改挂官方镜像页（`01_hub_docker_com.md:17-18`：网页访问 + WebDAV 两条取用通道）。
- 1.2 问题二结论措辞修正：「官方安装脚本 / 官方承认的独立装法」→「整合脚本 / 脚本明确支持的独立装法」（README:75-76）。
- 1.3 播放层举例换源：改挂 MediaWarp README（「前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器」，`lens-b/mediawarp/01_github_com.md:51`），使 Emby / Jellyfin / 飞牛影视 三者并列的依据落到可回源处。
- 1.5 「纯净版」来源与措辞修正：「官方来源」→「核对过的来源（整合脚本仓库、官方镜像页等）」；「官方语义上对应」→「脚本菜单里对应」；warning「官方文档里」→「整合脚本的 README 里」。
- 1.5 **新增 `[!note]` 术语校正**：「这套笔记里的『官方』指什么」——官方＝镜像 `xiaoyaliu/alist`（作者 `xiaoyaliu`、内容源 `alist.xiaoya.pro`，hub `:8`、`:10`）；本笔记用的是社区整合脚本 `xiaoyaDev/xiaoya-alist`，它内部才用官方镜像（`all_in_one.sh:1376`）。
- 本章小结由五条增为六条（新增「『官方』= 镜像 `xiaoyaliu/alist`」一条）。
- 引文对照表头补全为「（原文 / 中译 / 出处）」，由 8 条重编为 13 条：新增 hub `:17`/`:18`、mediawarp `:51`、hub `:8`/`:10`、README `:33-34`、`all_in_one.sh:1376`；删除 monlor 组件注释 2 条。

## 遗留 / 风险

| # | 项 | 说明 |
| --- | --- | --- |
| 1 | vault 侧表格列宽由 Obsidian 自动补空格 | `publish_copies.py --check` 在用户打开笔记后可能报 `vault=≠`，属渲染层格式，非内容漂移 |
| 2 | 术语校正 note 的「官方」口径 | 仅在 ch01 正文出现一次完整定义，后续各章按其口径措辞；若各章仍有「官方」二字，均指镜像 `xiaoyaliu/alist`，非整合脚本 |
| 3 | 「纯净版」仍是社区叫法 | 本章明确其为非官方术语、脚本语义约等于菜单「安装 小雅Alist」；未改写为官方产品名 |

## 校验

- `publish_copies.py --check --only 01`：`OK`（output==、vault==）。
- 引文锚点回源：逐条 grep 复核 `01_hub_docker_com.md`（`:8/:10/:17/:18`）、`01_raw_githubusercontent_com.md`（`:33-34/:75/:76`）、`all_in_one.sh`（`:1376`）、`lens-b/mediawarp/01_github_com.md`（`:51/:53`）、`lens-b/fntvproxy/01_github_com.md`（`:266`）、`p2/newzone-xiaoya.md:10`、`forum/tid-73955.md:32`，全部命中。
- 正文残留扫描：`rg -n "monlor|ghcr.io/monlor" chapters/01_开篇定位.md` **仅命中「更新记录」历史行**；正文各节已无 monlor 残留。
