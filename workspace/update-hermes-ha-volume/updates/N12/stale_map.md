# N12 过时点定位

**目标文件**：`workspace/hermes-home-assistant/chapters/10-附录.md`
**触及区域**：附录 C → C.1 官方文档索引 → `Hermes 侧：` 表格（原仅 3 行：`HMS-04` / `HMS-07` / `HMS-10`）

## 过时的是什么

该表的 3 条目**全部指向 Hermes 仓库内的 `website/docs/` 页面**（mcp-config-reference、cli-commands、use-mcp-with-hermes），即只覆盖了 Hub 的 `official` 那一支的自述文档。

它漏掉了**原册自己的来源 HMS-05 已经写明、却被读漏的那一半**：Hub 的搜索由一份**联邦索引**回答，覆盖 `official` 之外的外部注册表。这份中央索引本身就是一个**可引用的一手来源**（`nousresearch.github.io/hermes-agent/docs/api/skills.json`），却未进入附录 C 的来源清单。

## 为什么现在算过时

- 原册「Hub 里没有现成 HA skill」的结论，只从 `official` 支（150 条）推出；而据**截至 2026-09-18 的 Hub 中央索引快照**，索引共 97,986 条，明示 Home Assistant 的 skill 有 **64 条**（`source_bank.md` §2 / §7 D-1）。
- 结论的核心（skill 是知识不是能力）不变，但**举证面**变了：附录 C 作为来源索引，缺一条指向该索引本身的条目。

## 依据

- `shared_research/source_bank.md` §1（时点限定写法）、§2（锁定数字：8 类来源、64 条）、§7 D-1（URL 与快照说明）。
- 未读取其他新来源；本项为 app 级、纯索引补录，不引入新事实断言。
