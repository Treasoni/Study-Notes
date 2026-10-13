# ch04 更新报告

| 项 | 值 |
| --- | --- |
| note_id | `ch04` |
| 源文件 | `chapters/04_部署实战.md` |
| 动作 | update（重写） |
| 输出模式 | patch-in-place（`updated_note` 即 `chapters/04_部署实战.md`） |
| 发布副本 | `output/04 部署实战.md`、`流媒体与影音/小雅 fnOS 单容器部署/04 部署实战.md` |
| 标题变更 | 第 4 章 部署实战——单容器小雅（monlor 镜像） → **第 4 章 部署实战——单容器小雅（一键脚本）** |
| 复核查验 | 待 P5 统一执行 |

## 完成项

- 4.1 整节重写：monlor 五行表 → 六行表 + 「整合脚本 ≠ 官方」note + 新「大白话」比喻。
- 4.2 由「一键脚本 + 手写 Compose」改为「菜单 `1 1` 全程」：新增问答对照表、WebDAV 双分支 note、等价 `docker run`、镜像源与 root 两个 warning。
- 4.3 自检七点重排：就绪判定改为脚本内置等待；WebDAV 改双分支；报错条目换源。
- 章名 + frontmatter title 同步更新（`publish_copies.py --title 04`）。
- 删除 `assets/04 部署实战/file-20261006213730421.png`、`file-20261006213604699.png`（经 Obsidian 移入回收站）。
- 引文对照重编为 18 条。

## 遗留 / 风险

| # | 项 | 说明 |
| --- | --- | --- |
| 1 | `output/final_note.md` 仍含两张已删图的引用（`:633`、`:666`） | 属预期：`final_note.md` 由 `assemble_final.py` 在 P4 收尾时整体重建 |
| 2 | vault 侧表格列宽会被 Obsidian 自动补空格 | 导致 `publish_copies.py --check` 在用户打开笔记后可能报 `vault=≠`，属渲染层格式，非内容漂移 |

## 校验

- `publish_copies.py --check`：`04` 为 `OK`（output==、vault==）。
- 正文残留扫描（本次改后）：`rg -n "monlor|ghcr.io/monlor|EMBY_ENABLED" chapters/04_部署实战.md` 的命中只允许出现在三处**有意保留的对照语境**——4.1 换路线背景段（说明旧路线已停更）、4.1「整合脚本 ≠ 官方」note（`README:295` 把 monlor 列为周边工具）、引文对照第 7 行（同上），以及「更新记录」历史行；正文的部署指令、端口、镜像、凭据部分已无 monlor 残留。
