# 更新报告：Strm 流文件与 302 播放详解

- 更新日期：2026-10-04
- 目标文件：`Strm流文件与302播放详解.md`（vault 根目录）
- destination_mode：`patch-in-place`（原地更新）
- update_goal：内容面向小白，更适合初学者阅读和理解

## Stale Map

| 处理 | 内容 |
| --- | --- |
| 保留 | Strm 定义与特点、302 定义与流程、两者关系、IPTV 案例、全部代码示例、FAQ（Q1–Q7）、总结 |
| 新增 | YAML frontmatter；「三分钟速览（零基础先读）」；「名词扫盲表」（16 个术语）；生活化比喻；「我什么时候会用到它」使用场景表；相关笔记双链；「更新记录」 |
| 改写 | 各节开头的解释改为「先比喻、后术语」，术语首次出现即解释；FAQ 答案转为大白话 |
| 重排 | 零散代码集中到第 7 节「动手实践（进阶，新手可跳过）」 |
| 修正 | 7.6 Flask 案例补回缺失的 `request` 导入（原代码会 `NameError`） |
| 未删除 | 无（技术内容与代码示例零删减） |

## 结构与阅读路径

新结构：`速览 → 名词扫盲 → Strm → 302 → 两者配合 → 使用场景 → 动手实践 → FAQ → 总结`。

新手可按顺序读并在第 7 节前停下；进阶读者直接跳第 7 节。

## Obsidian 适配

- 补齐 frontmatter：`title / aliases / tags / created / updated / status / source_project`。
- 新增 1 条高价值双链 `[[硬件解码vs软件解码]]`（同库存在）。
- 未引入 Dataview/Bases，保持普通 Markdown。

## 未处理 / 风险

- 未找到对应 MOC，未做索引同步；如需可调用 `moc-organizer`。
- 未发现同名 workspace 副本，无 vault/workspace 漂移。
