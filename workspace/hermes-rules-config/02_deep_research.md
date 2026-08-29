# Hermes 规则配置 - 阶段 2 深度素材

> 主题：Hermes 的规则配置（rules / CLAUDE.md 这类如何配置）
> 运行：hermes-rules-config · P2 深度收集
> 日期：2026-08-30
> 聚焦方向：A（规则文件体系）+ B（Claude Code 对照迁移）+ D（实战配置与验证）
> 版本锚定：Hermes Agent v0.20.x

---

## 一、范围

围绕"Hermes 如何配置类似 Claude Code 的 rules / CLAUDE.md"这一目标，精读 6 篇官方文档（全部 tier 1，Nous Research 官方）。覆盖：规则文件体系（SOUL.md + 项目上下文文件 + 系统提示组装）、Claude Code 对照迁移（import-agent）、hooks 实战、验证命令。本地缓存位于 `research-sources/`（crawl4ai 抓取）。

## 二、来源表

| ID | 来源 | Tier | 抓取说明 |
| --- | --- | --- | --- |
| S1 | [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality) | 官方 | SOUL.md 身份机制、personality 预设、自定义 personalities |
| S2 | [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files) | 官方 | 项目上下文文件优先级、目录链、渐进子目录发现、安全扫描 |
| S3 | [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) | 官方 | 系统提示 10 层组装、stable/context/volatile 缓存、platform_hints |
| S7 | [CLI Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md) | 官方 | config/doctor/status/prompt-size/hooks 等验证命令 |
| S8 | [Event Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) | 官方 | 四类 hook 系统、shell hooks schema、JSON 线协议、pre_tool_call 阻塞/改写 |
| S9 | [Import from other agents](https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents) | 官方 | `hermes import-agent claude-code` 映射表与行为 |

> P1 候选中的 S4（configuration）、S5（managed-scope）、S6（profiles）本阶段未深读；managed-scope/profiles 已在 P1 有摘要，如需可补抓。

---

## 三、Claim / Source 映射

### A. 规则文件体系

| # | Claim | Source |
| --- | --- | --- |
| A1 | Hermes 指令载体分两类：**全局 `SOUL.md`（身份，系统提示 slot #1）** 与 **项目级上下文文件（Context Files）** | S1, S2, S3 |
| A2 | `SOUL.md` 位于 `~/.hermes/SOUL.md`（或 `$HERMES_HOME/SOUL.md`）；缺省自动 seed；已有文件**永不被覆盖**；**只从 HERMES_HOME 加载，不探测 CWD**（身份不会随项目漂移） | S1, S2, S3 |
| A3 | SOUL.md 内容注入前经**安全扫描 + 截断**（上限 `context_file_max_chars`，否则随模型窗口动态，floor 20k / ceiling 500k）；空/空白/不可读 → 回退内置默认身份 | S1, S3 |
| A4 | SOUL.md 职责 = 身份/语气/风格/沟通默认；AGENTS.md 职责 = 项目架构/约定/工具偏好/命令/端口/路径。判断规则：**"跟随你到处走 → SOUL.md；属于某个项目 → AGENTS.md"** | S1 |
| A5 | 项目上下文文件优先级（**每次会话只加载一种**，first-match-wins）：`.hermes.md`/`HERMES.md`（沿 git root 上溯）→ `AGENTS.override.md`（个人、gitignored，替代 AGENTS.md）→ `AGENTS.md` → `CLAUDE.md` → `.cursorrules`/`.cursor/rules/*.mdc` | S2, S3 |
| A6 | `AGENTS.override.md` 存在时**替代**已提交的 AGENTS.md —— 想个人差异又不动仓库文件时的方案 | S2 |
| A7 | AGENTS.md **目录链**：git 仓库内从 git root → CWD 合并加载，深层文件在后（更具体优先）；相同副本去重；**非 git 仓库只看 CWD**，父目录不泄漏 | S2 |
| A8 | **渐进子目录发现**：session 中 agent 进入子目录时按需注入该目录 AGENTS.md/CLAUDE.md/.cursorrules（每目录至多一次、上溯至多 5 级、单文件 8000 chars 截断），避免系统提示膨胀、保住 prompt 缓存 | S2 |
| A9 | 所有上下文文件都过**注入安全扫描**（指令覆盖、隐藏 HTML/div、凭据外泄、零宽字符等），命中即 `[BLOCKED: ...]` 不加载 | S2 |
| A10 | 系统提示组装（10 层，stable→context→volatile 三档缓存）：①SOUL.md 身份 → ②工具行为引导 → ③Honcho 静态块 → ④可选 system_message → ⑤MEMORY 快照 → ⑥USER 快照 → ⑦skills index → ⑧项目上下文文件 → ⑨时间戳/会话 → ⑩platform hint | S3 |
| A11 | `platform_hints` 可在 config.yaml 按平台 `append`/`replace`（裸字符串=append），随系统提示重建生效，不破坏缓存 | S3 |

### B. Claude Code 对照迁移

| # | Claim | Source |
| --- | --- | --- |
| B1 | `hermes import-agent claude-code` 一键导入 `~/.claude`：全局 CLAUDE.md → `MEMORY.md` 记忆条目；`settings.json` permissions.allow `Bash(...)` → `command_allowlist`；permissions.deny → `approvals.deny`；mcpServers → `mcp_servers`；`skills/<name>/` → `~/.hermes/skills/claude-code-imports/<name>/`；`commands/*.md` → **跳过**（建议转成 skill） | S9 |
| B2 | Bash 前缀规则转 glob（`Bash(npm run test:*)` → `npm run test*`）；非 Bash 权限规则（`Read(...)`、WebFetch）→ 报告为 unmapped | S9 |
| B3 | **凭证永不导入**：`.credentials.json` 不读；MCP 密钥名（`*_TOKEN`/`*_API_KEY`/`Authorization`）被剔除并在报告中列出，需手动补 `~/.hermes/.env` 或 `hermes setup` | S9 |
| B4 | 导入行为：**preview-first**（先打印计划，非交互停在预览，除非 `--yes`）；**merge-not-replace**（记忆去重、allow/deny 合并）；冲突默认跳过（`--overwrite` 覆盖）；坏文件只报错不中止 | S9 |
| B5 | 隔离/排查开关：`--ignore-rules`（跳过 AGENTS.md/SOUL.md/.cursorrules/memory/preloaded skills 注入）、`--ignore-user-config`（忽略 `~/.hermes/config.yaml`，`.env` 凭证仍加载）、`--safe-mode`（禁用全部自定义，隐含两者 + 插件/hooks/MCP） | S7 |

### D. 实战配置与验证

| # | Claim | Source |
| --- | --- | --- |
| D1 | 四类 hook 系统：①Gateway `HOOK.yaml`+`handler.py`；②plugin `ctx.register_hook()`；③**shell hooks**（config.yaml `hooks:` 块，CLI+Gateway，可阻塞工具/注入上下文）；④outbound webhooks（config.yaml `hooks.outbound:` 推送到外部 HTTP） | S8 |
| D2 | Shell hooks 配置 schema：`hooks.<event>: [{matcher, command, timeout(默认60/cap300), fail_closed(默认false, 仅 pre_tool_call)}]`；顶层 `hooks_auto_accept: false`（首次使用按 (event, command) 对征询同意） | S8 |
| D3 | Shell hook 运行：`shlex.split` + `shell=False` 子进程；**JSON 经 stdin 进、stdout 出**；`pre_tool_call` 可 `block`（需 message）/`modify`（改写 tool_input）；超时 **fail-closed** 阻塞工具 | S8 |
| D4 | `pre_tool_call` 返回兼容双形状：Claude-Code 风格 `{"decision":"block","reason":...}` 与 Hermes 规范 `{"action":"block","message":...}`，内部归一化 | S8 |
| D5 | 验证命令族：`hermes doctor [--fix]`（诊断配置/依赖，--fix 自动修复）；`hermes config show/edit/get/set/unset/path/env-path/check/migrate`（get 支持 dotted key 与 `--json`，unset 恢复默认）；`hermes status`；`hermes prompt-size [--platform][--json]`（**离线**查看系统提示+工具 schema 字节构成：skills index/memory/profile）；`hermes hooks list/test/revoke/doctor`；`hermes dump`/`debug` | S7 |

---

## 四、矛盾点 / 文档差异

1. **`AGENTS.override.md` 在优先级链中的位置**：user-guide（S2）明确列为 `.hermes.md` 之后第二优先；而 developer-guide 的 `build_context_files_prompt()` 代码片段（S3）未列出 override（仅 .hermes.md→AGENTS.md→CLAUDE.md→.cursorrules）。→ 以 user-guide 为准（override 为较新特性，代码为简化示意）。
2. **AGENTS.md 发现范围**：prompt-assembly（S3）写 "AGENTS.md (cwd only)"，但 user-guide context-files（S2）明确 git 仓库内做目录链合并 + 会话中渐进子目录发现。→ 两者描述的机制不同（启动 vs 会话中）；以 S2 的完整描述为准。
3. **personality 页 vs context-files 页的 SOUL.md 位置表述**：一致（均为 HERMES_HOME），无冲突。

## 五、实践指导（面向：上手、用过 Claude Code、实战配置指南）

**推荐工作流**（官方 Recommended workflow 的扩展版）：
1. **全局身份**：编辑 `~/.hermes/SOUL.md`（缺省已 seed）——放语气/风格/立场，别放项目细节。
2. **项目规则**：在项目根写 `AGENTS.md`（monorepo 可在子目录逐层加）；想个人差异写 gitignored 的 `AGENTS.override.md`。
3. **兼容复用**：已有的 `CLAUDE.md` / `.cursorrules` 会被 Hermes 直接识别，无需改名（优先级低于 `.hermes.md`/AGENTS.md）。
4. **需要拦截/自动化工**：config.yaml 加 `hooks:` shell hooks（block 危险命令、自动格式化、pre_llm_call 注入上下文）。
5. **迁移**：`hermes import-agent claude-code --dry-run` 预览 → 确认后导入 → 按报告补密钥。
6. **验证**：`hermes doctor` → `hermes config check` → `hermes prompt-size` 看规则是否进入系统提示；怀疑被注入干扰时用 `--safe-mode` 对照。

**对照速查表**（写入最终笔记核心）：
| Claude Code | Hermes |
| --- | --- |
| `CLAUDE.md`（项目根指令） | `AGENTS.md` / `.hermes.md`（项目上下文文件，优先级更高） |
| 全局 `CLAUDE.md` / 记忆 | `SOUL.md`（身份 slot #1）+ `MEMORY.md` 记忆 |
| `.claude/rules/` 分层规则 | 项目上下文文件优先级链 + 目录链/渐进子目录 |
| `settings.json` 权限 | `config.yaml` `command_allowlist` / `approvals.deny` + `.env` 密钥 |
| `settings.json` hooks | config.yaml `hooks:` shell hooks（Claude-Code 兼容 JSON 形状） |
| `claude config` | `hermes config set/get/check` |
| 迁移 | `hermes import-agent claude-code` |

## 六、开放问题

- **Profiles 深读**（P1 S6）：per-profile SOUL.md/config 的完整语义，未在本次深读范围（方向 A 未选 C）。
- **Managed Scope**（P1 S5）：`/etc/hermes` 叶级合并的实操示例，未深读。
- `.hermes.md` 的 YAML frontmatter 被剥离且"预留未来 config override"，具体能力未定。
- `hermes config migrate` 交互式新增选项的具体键，未逐一展开。
- hooks `matcher` 正则与 `pre_llm_call` 注入上下文的完整示例，建议写作时补抓 S8 对应小节。

## 七、下游交接（→ outline-generator / chapter-writer）

- 大纲建议：①定位与文件地图（SOUL.md vs Context Files vs config）→ ②SOUL.md 实战 → ③项目上下文文件（AGENTS.md 优先级/目录链/渐进发现）→ ④Claude Code 对照迁移（含 import-agent）→ ⑤hooks 实战 → ⑥验证与排错命令。
- 素材定位：`workspace/hermes-rules-config/research-sources/`（本地缓存，含 S1/S2/S3/S7/S8/S9 全文）。
- 强调：**面向"用过 Claude Code"的用户**，用对照锚点贯穿全文；每个机制给 `hermes` 命令验证路径。
