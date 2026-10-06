# N05 更新计划 — ch04 `### 4.1` 理由一

## 定位

- **锚文本**：`**理由一：它是唯一能一次补齐三类缺口的路。**`
- **源文件行号**：**L9**（1-indexed，按 `\n` 切分；source-file numbering）
- **交叉核对**：任务给的 L9 与实际逐字节扫描一致，未出现 +15 偏移（+15 是
  published-volume 口径，本文件用的是 source 口径）。
- 候选断言：全文件 `hass-cli` = 0 处、`并不存在` = 1 处、目标从句唯一（`count == 1`）。

## Before → After（从句级）

**Before**
> ……怎么调**已有**的命令行工具，HA 场景下并不存在这样一个 `ha` CLI。剩下能补能力的……

**After**
> ……怎么调**已有**的命令行工具，HA 场景**有**可调的 CLI（`hass-cli` 指的是
> `home-assistant-ecosystem/home-assistant-cli`，**Home Assistant Ecosystem 组织**
> 维护的命令行工具，是社区里的事实标准，**不是 HA core 官方出品**）；Hub 里也**有**
> 封装它的 skill（`clawhub/homeassistant-cli`），但这类 skill 仍然只是知识件，
> 不新增任何工具。剩下能补能力的……

## 依据（实际打开过的文件）

- `shared_research/source_bank.md` §1 时点限定、§3 锁定措辞（`hass-cli` 段、
  「skill 是知识，不是能力」段）、§6 禁令 1/2、§7 D-2。
- `chapters/01-结论先行与能力地图.md` L44（house style 术语）、L47。
- `chapters/03-路线选型.md` L55、L126、L170。

## 三条硬要求的落点

1. `home-assistant-ecosystem/home-assistant-cli` — 逐字出现。
2. **Home Assistant Ecosystem 组织** / 社区事实标准 / **不是 HA core 官方出品** — 三项齐全，
   且未复用 ClawHub 的 "the official hass-cli tool" 自述。
3. 落点写「有 CLI、Hub 有封装 skill、但**不新增任何工具**」——
   不是「找不到」，是「找得到、装得上、能力中性」。

## 不改动确认

段落主主张未动：`skill 只能教 agent 怎么调**已有**的命令行工具` 与
`剩下能补能力的只有 MCP server 与自定义 plugin` / `默认落点就是 MCP server`
三句逐字节保留。仅 `——` 改为 `（）` 承载从句，避免与首个 `——` 形成嵌套破折号。

## 未采纳的写法（避免与别章重复且可能引入新数字）

- 未写入 `596★` / `pushed 2026-08` / `核实于 2026-09-18`：非必需，写入会触发
  `source_bank.md` §1 的时点限定义务，且 ch03 L126 已承担该举证。
- 未新增脚注、未新增 `[[wikilink]]`（会破坏 `publish_volume.py` 的目标存在性断言）。
