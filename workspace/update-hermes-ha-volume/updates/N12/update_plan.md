# N12 更新计划

**唯一改动**：向 `Hermes 侧：` 表格插入 1 行。文件其余内容逐字节不变。

## 定位（按锚点文本，行号为交叉校验）

源文件 `workspace/hermes-home-assistant/chapters/10-附录.md`（150 行）：

| 源行 | 内容 |
|---|---|
| L104 | `Hermes 侧：` ← 锚点 |
| L105 | （空行） |
| L106 | `\| ID \| 主题 \| 位置 \|` ← 表头锚点 |
| L107 | `\|---\|---\|---\|` |
| L108 | `HMS-04` 行 |
| L109 | `HMS-07` 行 |
| L110 | `HMS-10` 行 ← **插入点**（插入于其后） |
| L111 | （空行，须保持） |
| L112 | `官方 release notes 里值得单看的两条：…` |

插入后：新行成为**输出 L111**，原 L111 空行顺移为 L112，段落顺移为 L113。

## 插入文本（单行，逐字）

```
| `HMS-13` | Skills Hub **中央索引**（联邦索引，8 类来源：`official` / `skills-sh` / `well-known` / `url` / `github` / `clawhub` / `lobehub` / `browse-sh`；截至 2026-09-18 的 Hub 中央索引快照，明示 Home Assistant 的 skill 64 条） | `nousresearch.github.io/hermes-agent/docs/api/skills.json` |
```

三列形状与既有行一致（4 个 `|`），表格保持连续，无空行插入表内。

## 与任务书字面的一处偏离（已按校验规则处理）

任务书给的时点限定为「截至 2026-09-18 快照」，与 `source_bank.md` §1 锁定的固定写法「**截至 2026-09-18 的 Hub 中央索引快照**」不逐字一致。按任务书「不一致时用资料库措辞」的指示，采用资料库写法；详见 `update_report.md`。

## 复核

`HMS-13` 在 `workspace/hermes-home-assistant/` 与 `AI学习/Hermes Agent/` 下 **grep 零命中**，编号未被占用。
