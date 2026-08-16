# 深度收集结果 - 从零搭建 Agent Harness 工程

> 运行：harness-project-setup | 阶段：P2 深度收集 | 日期：2026-08-16
> 方向：A（官方规范 + 本地范本综合实战）

## 一、范围

按用户选择的方向 A，深抓 **5 篇 Claude Code 官方文档**（tier 1 权威基线），叠加本地 vault 活体范本（视角 D 实测），产出"先建哪些文件 + 每个文件怎么填"所需的文件级事实。未抓社区模板（方向 B/C 已由用户排除本轮）。

## 二、源表

| ID | 标题 | URL | 层级 | 抓取日期 |
|----|------|-----|------|----------|
| S1 | Memory — How Claude remembers your project | https://code.claude.com/docs/en/memory | 1 | 2026-08-16 |
| S2 | Set up Claude Code in a monorepo/large codebase | https://code.claude.com/docs/en/large-codebases | 1 | 2026-08-16 |
| S3 | Extend Claude with skills | https://code.claude.com/docs/en/skills | 1 | 2026-08-16 |
| S4 | Claude Code Subagents | https://code.claude.com/docs/en/sub-agents | 1 | 2026-08-16 |
| S5 | Claude Code Hooks reference | https://code.claude.com/docs/en/hooks | 1 | 2026-08-16 |
| D | 本地活体范本（本 vault 实测） | `D:\Study-Notes\` | 2 | 2026-08-16 |

## 三、claim/来源映射（按脚手架主题组织）

### 3.1 指令入口：CLAUDE.md / AGENTS.md / rules

| Claim | 来源 |
|-------|------|
| 加载顺序（广→专）：托管策略 → `~/.claude/CLAUDE.md` → 项目 `./CLAUDE.md` 或 `./.claude/CLAUDE.md` → `./CLAUDE.local.md` | S1 |
| 从 cwd 向上遍历祖先目录，全部拼入上下文而非覆盖；子目录 CLAUDE.md 按需 lazy load | S1/S2 |
| **Claude Code 读 CLAUDE.md 不读 AGENTS.md**；已有 AGENTS.md 用 `@AGENTS.md` import 或符号链接桥接（Windows 建议 import） | S1 |
| `@path` import 相对"含 import 的文件"解析，递归最深 4 层；跳过代码块内内容 | S1 |
| 单文件 CLAUDE.md ≤200 行；`.claude/rules/` 一文件一主题，无 `paths` 的常驻加载，带 `paths:` frontmatter 的按文件匹配触发 | S1 |
| 大型仓库建议两层 CLAUDE.md：根放通用规则，子目录放栈特化 | S2 |
| **项目 `.claude/settings.json` 只从启动目录加载、不随祖先继承**（与 CLAUDE.md 不同） | S2 |
| 本地范本实测：`AGENTS.md` 为 canonical source + `CLAUDE.md` 为 Claude 入口，`CLAUDE.md` 引 `@` 或声明双套隔离；rules 分 `common/` + `obsidian/` + 顶层单文件 | D |

### 3.2 Skills 放置与结构

| Claim | 来源 |
|-------|------|
| 技能 = 目录 + `SKILL.md`；目录名即命令名，`description` 决定自动加载 | S3 |
| 层级：企业 managed → 个人 `~/.claude/skills/` → 项目 `.claude/skills/` → 插件 `skills/`；同名冲突企业>个人>项目 | S3 |
| frontmatter 全可选，仅 `description` 推荐；`allowed-tools` 当轮有效；`context: fork` 独立子代理运行；`disable-model-invocation` / `user-invocable` 控制调用方 | S3 |
| SKILL.md ≤500 行，长参考放 `reference.md`/`examples.md`/`scripts/`；支持 `$ARGUMENTS`/`${CLAUDE_SKILL_DIR}` 等替换与 `` !`cmd` `` 动态注入 | S3 |
| 技能按需加载（正文不在启动时进上下文），与 CLAUDE.md 常驻互补 | S3 |
| 本地范本实测：`.claude/skills/{name}/SKILL.md` + `manifest.yaml`（agent-platform/v1 契约，声明 entrypoint/capabilities/permissions/dependsOn） | D |

### 3.3 Subagents 放置与结构

| Claim | 来源 |
|-------|------|
| 层级（高→低）：托管 settings `.claude/agents/` → `--agents` CLI JSON → 项目 `.claude/agents/` → `~/.claude/agents/` → 插件 `agents/` | S4 |
| 文件为 YAML frontmatter + markdown 正文（正文即系统提示词）；仅 `name`/`description` 必填；name 需小写+连字符 | S4 |
| `tools` 为允许列表（缺省全工具）；`model`（sonnet/opus/haiku/fable/inherit）；`permissionMode`（default/acceptEdits/auto/dontAsk/bypassPermissions/plan） | S4 |
| 子代理上下文干净：只收自身系统提示词+环境，不含完整系统提示词；内置 Explore（只读搜索，跳过 CLAUDE.md）/Plan 等 | S4 |
| 调用：自然语言 / `@agent-<name>` / `claude --agent <name>` / settings.json `"agent"` 字段 | S4 |
| 本地范本实测：`.claude/agents/{name}.md` + `manifest.yaml`；chapter-writer 用 `tools: Read,Write,Edit,Bash` + `model: sonnet` + `color` 收窄 | D |

### 3.4 Hooks 配置

| Claim | 来源 |
|-------|------|
| 注册位置：`~/.claude/settings.json`（全局）、`.claude/settings.json`（项目可提交）、`.claude/settings.local.json`（gitignored）；插件 `hooks/hooks.json`、skill/subagent frontmatter 亦可 | S5 |
| 结构：`hooks.<EventName>[]`，每项 `{matcher, hooks:[handler]}`；handler 键含 `type`(command/http/mcp_tool/prompt/agent)、`if`、`timeout`、`command`、`args`、`async` | S5 |
| 生命周期：SessionStart/SessionEnd 每会话；UserPromptSubmit/Stop 每轮；PreToolUse/PostToolUse 每次工具调用 | S5 |
| **退出码：0=成功；2=阻塞（PreToolUse 阻断工具、UserPromptSubmit 擦除提示、Stop 阻止停止）；其他非零=非阻塞** | S5 |
| 输入经 stdin JSON；输出 stdout 以 `{` 开头解析为 JSON，决策如 `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny",...}}` | S5 |
| exec 形式（`command`+`args`）不经 shell 无分词；shell 形式走 `sh -c`/Git Bash/PowerShell | S5 |
| 本地范本实测：`.claude/settings.json` 注册 SessionStart（read_learnings.py）/Stop（post_conversation.py）/SessionEnd（collect-usage.py）；脚本放 `.claude/hooks/`；`settings.local.json` 配 permissions allow/deny | D |

### 3.5 项目脚手架整体布局（跨源汇总）

| Claim | 来源 |
|-------|------|
| 最小骨架 = 根 `CLAUDE.md`（≤200 行）+ `@AGENTS.md` import + `.claude/rules/` 主题文件 + `.claude/skills/` + `.claude/agents/` + `.claude/settings.json`（hooks） | S1/S3/S4/S5 |
| settings 分层：共享放 `.claude/settings.json`、个人放 `.claude/settings.local.json`、强制放 managed | S5/S2 |
| deny 规则（`permissions.deny`）挡 dist/build/vendor；`claudeMdExcludes` 跳过无关包 CLAUDE.md | S2 |
| 本地范本完整布局：`AGENTS.md`+`CLAUDE.md` / `.claude/{agents,commands,hooks,platform,rules,scripts,skills,workflows}` / `.codex/` 镜像 / `.agent-sync/` 同步脚本 / `workspace/workflow-runs/` 状态文件 | D |

## 四、矛盾与坑

1. **CLAUDE.md vs AGENTS.md**：Claude Code 默认读 CLAUDE.md 不读 AGENTS.md，而 Codex/其他 agent 读 AGENTS.md → 必须用 `@AGENTS.md` import 桥接，避免双份维护（S1）。
2. **settings 不继承**：项目 `.claude/settings.json` 只从启动目录加载，不随祖先继承；而 CLAUDE.md 继承 → monorepo 每个子包 settings 必须自包含（S2）。
3. **版本依赖强**：import 需 v2.1.213+、`/subtask` v2.1.212+、布尔字段 v2.1.218+、exit2+无效JSON阻塞 v2.1.214+ 等 → 脚手架需注明最低版本（S1/S3/S4/S5）。
4. **强制策略必须 exit 2**：静默（exit 0）不自动批准；非零退出码多数事件不阻塞，只有 exit 2 才硬阻断（S5）。
5. **skills 名称来源**：个人/项目技能命令名=目录名（name 仅显示名），插件技能里 name 才改命令末段（S3）。
6. **SessionEnd 预算**：共享 1.5s 预算，脚本需轻量或显式 timeout（S5）。
7. **自动记忆 vs 项目文件**：自动记忆是机器本地不跨机，与走版本控制的 CLAUDE.md 互补（S1）。

## 五、实践指导（脚手架落地清单）

1. **第一步建 4 个文件**：根 `CLAUDE.md`（≤200 行入口）+ `AGENTS.md`（canonical source，被 CLAUDE.md `@import`）+ `.gitignore`（含 `CLAUDE.local.md`、`.claude/settings.local.json`）+ `.claude/settings.json`。
2. **按需加 `.claude/` 子目录**：rules → skills → agents → hooks，不要一次性堆全。
3. **rules 一文件一主题**，无 paths 常驻；文件路径具体化（如 `testing.md`），可建子目录。
4. **skills 目录名即命令名**，description 首句放触发词，长参考放 `scripts/`/`reference.md`。
5. **agents 用 `tools` 收窄 + `model` 控制成本**，正文即系统提示词自足。
6. **hooks 脚本统一 `.claude/hooks/`**，settings 用 `${CLAUDE_PROJECT_DIR}` 引用；安全类必须 `exit 2`。
7. **渐进式披露**：入口文件只做地图，深层拆 rules/skills/docs，防止"陈规坟场"（S1 理论 + D 范本一致）。

## 六、开放问题（大纲阶段需决策）

1. 目标"harness 工程"是**纯 Claude Code** 还是**跨 runtime**（含 .codex/.agent-sync 镜像同步）？本地范本 D 是跨 runtime 双轨，增加复杂度。
2. 是否包含 **workflow 状态机**（`.claude/workflows/` + `todo-state.sh`）？官方文档未覆盖此层，属本范本自研。
3. 是否深入 **manifest.yaml**（agent-platform/v1）？也是本地范本特有、官方无对应。
4. 笔记粒度：骨架清单式（快速上手）还是含每文件示例内容的完整实战？

## 七、下游交接（handoff）

- **大纲生成（P3）**：以 §五 的 7 步落地清单为骨架，逐章展开"先建哪些文件 → skills 放哪 → hooks/subagents/rules/AGENTS 怎么配"。
- **素材引用**：每章用 §三 的 claim 表按主题引用（S1-S5 + D），§四 坑位作为各章"常见坑"。
- **代码示例**：从 D（本地范本实测）提取真实文件结构做目录树，从 S1-S5 提取 frontmatter/JSON 片段做配置样例。
- **待用户确认**：§六 开放问题在 P3 大纲确认时逐项敲定。
