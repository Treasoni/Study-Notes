# N05 过时点映射 — ch04 `### 4.1` 理由一

**目标文件**：`workspace/hermes-home-assistant/chapters/04-落地-社区ha-mcp.md`
**定位**：source L9，段落 `**理由一：它是唯一能一次补齐三类缺口的路。**`
**本单元只动一句从句，段落结论不变。**

## 过时的句子

> …skill 只能教 agent 怎么调**已有**的命令行工具，**HA 场景下并不存在这样一个 `ha` CLI**。…

## 为什么过时

1. **事实错**：HA 场景**有**可调的 CLI。`hass-cli` 指
   `home-assistant-ecosystem/home-assistant-cli`，由 **Home Assistant Ecosystem**
   组织（社区组织）维护，596★、未归档、pushed 2026-08，是社区事实标准。
   证据：`shared_research/source_bank.md` §3 锁定措辞、§7 D-2。
2. **与同册自相矛盾**：ch01 L44 与 ch03 L126 / 3.2 节已按同一套措辞补正过这两处；
   ch04 若保留原句，同一本册里同一事实出现两个版本。
3. **举证方式本身也不对**：原句写成「不存在」（搜不到），而正确形态是
   「搜得到、装得上，但装完不提供新能力」——Hub 里**有**封装它的 skill
   （`clawhub/homeassistant-cli`），问题从来不是找不到。
4. **违反禁令**：`source_bank.md` §6 禁令 1 明列「不得写…『不存在可调的 `ha` CLI』」
   为本次要补正的错误原文。
5. **附带风险**：原句的 `ha` 也会让人误以为 `hass-cli` 是 HA core 官方工具；
   §6 禁令 2 要求显式声明**不是** HA core 官方出品（ClawHub 条目自述
   称其为 "official"，措辞不精确，不沿用）。

## 不受影响（冻结）

- 段落核心主张：自建 `SKILL.md` 不新增能力 → 「要能力」默认落点是 MCP server。
- `### 4.1` 其余理由段、`### 4.2` 及其后全部内容、标题、`本章来源`、脚注。
- 本文件 L148 另一处 `不存在` 指 `${env:HA_TOKEN}` 在 `~/.hermes/.env` 里不存在，
  与 CLI 无关，**不动**。
