# N05 更新报告 — ch04 `### 4.1` 理由一

**批次**：`batch-note-update-flow` / `update-hermes-ha-volume` / batch 2 / item N05
**源文件**：`workspace/hermes-home-assistant/chapters/04-落地-社区ha-mcp.md`（400 行 / 401 split 段）
**产出**：`updated_note.md`（31625 B → 31942 B）

## 改了什么

仅 **source L9** 的一处举证从句：

- Before：`HA 场景下并不存在这样一个 \`ha\` CLI。`
- After：`HA 场景**有**可调的 CLI（\`hass-cli\` 指的是
  \`home-assistant-ecosystem/home-assistant-cli\`，**Home Assistant Ecosystem 组织**维护的
  命令行工具，是社区里的事实标准，**不是 HA core 官方出品**）；Hub 里也**有**封装它的
  skill（\`clawhub/homeassistant-cli\`），但这类 skill 仍然只是知识件，不新增任何工具。`

从句由「不存在」改写为「存在但能力中性」，并显式排除官方归属。

## 没改什么

- 段落主主张三句逐字节保留：`skill 只能教 agent 怎么调**已有**的命令行工具`、
  `剩下能补能力的只有 MCP server 与自定义 plugin`、`默认落点就是 MCP server`。
- 段落其余文字、`### 4.1` 其余理由段、`### 4.2` 及全文件其余 399 行**逐字节相同**。
- 未动标题、编号、`本章来源`、脚注、空白与换行风格。
- 未新增脚注、未新增 wikilink。
- L148 另一处 `不存在`（指 `${env:HA_TOKEN}` 不在 `~/.hermes/.env`）与本次命题无关，未动。

## 验证结果（对 `updated_note.md` 实测）

| 项 | 结果 |
|---|---|
| `\r` 字节数 | **0** |
| BOM | **无**（`f[:3] != EF BB BF`） |
| 结尾 | **恰好一个 `\n`**（不以 `\n\n` 结束） |
| 编码 | UTF-8（`decode('utf-8')` 无异常） |
| 逐行 diff vs 源文件 | 401 段对 401 段，**仅第 9 段不同** |
| `并不存在` 出现次数 | **0** |
| `并不存在这样一个` | **0** |
| `hass-cli` 出现次数 | **1**（落在 L9 修正段内） |
| 脚注定义行 `^\[\^` | 30（原 30，**不变**） |
| 行内脚注引用 | 30（原 30，**不变**） |
| `[[` / `]]` | 0 / 0（原 0 / 0，**不变**） |

## 已读且实际引用的来源

- `workspace/update-hermes-ha-volume/shared_research/source_bank.md`
  — §1（时点限定）、§3（`hass-cli` 锁定措辞、「skill 是知识不是能力」）、
  §6（禁令 1/2）、§7 D-2。
- `workspace/hermes-home-assistant/chapters/01-结论先行与能力地图.md` L44/L47。
- `workspace/hermes-home-assistant/chapters/03-路线选型.md` L55/L126/L170。

## 疑虑

1. **未写入星数与核实日期**。`source_bank.md` D-2 给了 596★ / pushed 2026-08 /
   核实于 2026-09-18，ch03 L126 已承担该举证。本段刻意不写数字，以免触发 §1 的
   时点限定要求；若批次口径要求 ch04 也自证，需补一处时点限定。
2. **`clawhub/homeassistant-cli` 是 ClawHub 开放注册表条目**，§6 注意事项提到该表
   有重复件与凑数件。此处只把它当作「Hub 里有封装该 CLI 的 skill」的存在性举证，
   未评价其质量；若后续 ch04 需要推荐可装条目，应改为 A 级
   `skills-sh/homeassistant-ai/skills/home-assistant-best-practices`。
3. **双破折号**。原句所在句已有一个 `——`，故新从句改用 `（）` 承载，避免嵌套破折号；
   这是本段唯一的形式调整，未改动任何实词位置。
4. 未核实 `home-assistant-ecosystem/home-assistant-cli` 的当下仓库状态（本次不联网，
   沿用 source_bank D-2 的已核验结论）。
