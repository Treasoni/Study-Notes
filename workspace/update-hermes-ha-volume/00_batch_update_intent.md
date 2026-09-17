# Hermes × Home Assistant 实战 分册 — 批量更新意图

## 基本信息

- **运行标识**：`update-hermes-ha-volume`
- **工作流**：`batch-note-update-flow`
- **创建时间**：2026-09-18
- **当前阶段**：阶段 0

```yaml
source_path: "AI学习/Hermes Agent/Hermes × Home Assistant 实战/"
source_scope: all                      # 该目录下全部 .md（README + 10 篇）
source_glob: "*.md"
update_goal: "修正『Skills Hub 里没有现成 HA skill』这一事实性错误结论，并在第 3 章新增 Hub 现成 HA skill 清单"
destination_mode: patch-in-place        # 用户已确认（选项 A）
batch_size: 2
shared_research: yes                    # 已就绪，见下
moc_path: "AI学习/Hermes Agent/Hermes Agent MOC.md"
stale_threshold: "contains:Skills Hub 里没有现成的 Home Assistant skill"
```

## 触发来源

用户提问：「在 hermes 的 skill hub 中不是有 homeassistant 相关的 skills 吗？」

核验后确认**用户是对的、原册结论是错的**，故启动本批量更新。用户已确认按推荐方案（选项 A）执行：
逐处补正 + 第 3 章新增一节 + 研究档勘误。

## 错误内容（原文逐字）

1. `01-结论先行与能力地图.md` L55：**结论二：「装个现成 skill 就能用」在 HA 场景不成立。**
   - L57 依据：「Hermes 官方 optional skills 目录的 smart-home 分类下**只有一个条目**，是 `openhue`……而技能系统的说明页 `website/docs/user-guide/features/skills.md`（HMS-05）全文未出现 Home Assistant。」
   - L63 推论：「**skill 不是能力，是知识**……而 HA 场景并不存在一个可以让 skill 去指挥的 `ha` CLI。所以「搜一个 HA skill 装上」这条路，在能搜到的那一刻之前就已经断了。」
   - L267 本章小结：「「装个现成 HA skill」这条路不存在：官方 optional skills 的 smart-home 分类下只有 `openhue` 一个，而 skill 本身也不提供新能力。」
2. `03-路线选型.md` L34：「有一个前提在第 1 章已经确认过，这里要重申，因为它是本章的出发点：**Skills Hub 里没有现成的 Home Assistant skill**。……所以「装个现成 skill 就能控制 HA」这条路根本不成立——不是效果不好，是**没有可装的东西**。」
3. `03-路线选型.md` 3.2 节：「那 `openhue` 为什么可以只靠一份 SKILL.md 就干活？因为**它描述的 CLI 真实存在**。」——同一节随后断言 HA 侧不存在这样的 CLI。

## 错在哪（两层）

**第一层：把「official optional skills 目录」当成了「整个 Skills Hub」。**
`HMS-05`（同一册的既有来源，`website/docs/user-guide/features/skills.md`）原文就写着 Hub 的搜索由一份**联邦索引**回答，
覆盖 `skills.sh` / ClawHub / LobeHub / browse.sh / well-known 端点 / GitHub taps；`official` 只是其中一支。
证据一直在手边，只读了 optional-skills 一支就下了全称结论。

**第二层（更实质）：`hass-cli` 存在。**
`home-assistant-ecosystem/home-assistant-cli`（596★，pushed 2026-08-04，未归档；PyPI `homeassistant-cli` 1.0.0，
自述 "Command-line tool for Home Assistant"）就是「可以让 skill 去指挥的 HA CLI」。
Hub 里的 `clawhub/homeassistant-cli` 正是包它的 skill。所以 3.2 节那句断言不成立。

## 核验证据（2026-09-18）

| 项 | 结果 | 取回方式 |
|---|---|---|
| Hub 中央索引条目总数 | **97,986** | `curl https://nousresearch.github.io/hermes-agent/docs/api/skills.json`（60.8 MB 单行 JSON） |
| 源分布 | ClawHub 75,785 / skills.sh 20,000 / GitHub 513 / LobeHub 505 / browse.sh 469 / NVIDIA 365 / **official 150** / built-in 58 / gstack 53 / OpenAI 44 / HuggingFace 25 / Anthropic 19 | 同上 |
| **明示 Home Assistant 的 skill** | **64 条**（ClawHub 52 + skills.sh 12） | 同上；快照 `sources/HUB-homeassistant-skills.json`（56,846 B，含完整记录） |
| smart-home 分类、未点名 HA | 13 条（含 `optional/openhue`） | 同上 |
| official 支的 HA skill | **确实只有 `openhue`**（原册这一层事实成立） | 同上 |
| `hass-cli` | `home-assistant-ecosystem/home-assistant-cli`，596★，2026-08-04 更新 | GitHub API |
| `homeassistant-ai/skills` | 749★，pushed 2026-09-16，自述 "Home Assistant skills for agents"，含 `home-assistant-best-practices`，走开放 Agent Skills 标准（agentskills.io） | GitHub API + README 原文 |

> 60.8 MB 原始索引**未保留**（避免进 git）；重取约 9 分钟。抽取脚本 `workspace/hermes-home-assistant/extract_hub_ha.py` 可复现。

## 值得保留的部分

「**skill 是知识，不是能力**」这条洞察**依然成立**，而且是本册第 3 章的骨架——不能一起否掉。
补正方向是把它用在正确的地方：正因为 skill 只提供知识，Hub 里的 HA skill 主要是**知识件与既有能力路径的封装**
（最佳实践、`hass-cli` 封装、Assist API 封装、MCP 桥、HAOS 运维），而不是「凭空补能力」。
其中 `homeassistant-ai/skills` 与第 4 章主角 `homeassistant-ai/ha-mcp` **是同一个组织**——
第 4 章只讲了它的 MCP server（服务件），漏了它的 skills 仓库（知识件），补上即构成完整答案。

## 附带范围（研究档，非笔记正文）

- `workspace/hermes-home-assistant/02_deep_research.md`：B-1 结论改判、新增来源条目、新增工具坑一条
- `workspace/hermes-home-assistant/01_explore_result.md` L31 同一处

## 输出模式

`patch-in-place`：直接修改已发布分册中的相关段落 + 第 3 章新增一节；原文其余部分不动。
第 4 章正文不因本次更新而改写（仅可能新增一条与 `homeassistant-ai/skills` 的互见）。

## 覆盖风险

1. 分册已发布并被 MOC 索引；改动段落若与前后文失去衔接，会产生新的不一致（须逐处读上下文再落笔）。
2. 索引是**联邦缓存、随时变化**：文中所有数字必须带「截至 2026-09-18 索引快照」的时点限定。
3. ClawHub 是开放注册表：有重复件与明显凑数件，清单必须做**质量分级**并标注「装前先 `hermes skills inspect` + 跑自带安全扫描」。
4. skills.sh 那 12 条在索引里**只有名字与作者、无描述**，不得据索引推断其内容质量。
