## 学习笔记大纲：《Hermes 的规则配置（rules / CLAUDE.md 这类如何配置）》

> 笔记类型：实战笔记（实战配置指南）
> 预计总篇幅：中长（约 6 章）
> 章节数：6
> 读者画像：用过 Claude Code，熟悉 CLAUDE.md / .claude/rules / settings.json / hooks 分层配置
> 贯穿主线：以 Claude Code 配置体系为对照锚点，每个机制都给出对应的 `hermes` 命令验证路径

---

### 第一章：先看地图 — Hermes 规则体系定位与文件地图
- **篇幅**：短
- **覆盖要点**：指令载体两分法（全局 SOUL.md vs 项目上下文文件）、Claude Code 对照总览表、文件位置地图、推荐工作流总览
- **素材引用**：S1, S2, S3, S9
- **代码示例**：有（`~/.hermes/` 与项目根目录结构树）
- **章节结构**：
  - 1.1 两类指令载体：SOUL.md（身份） vs 项目上下文文件（项目知识）
  - 1.2 与 Claude Code 配置体系的对照总览表（CLAUDE.md → AGENTS.md / 全局 CLAUDE.md → SOUL.md / .claude/rules → 优先级链 / settings.json → config.yaml / claude config → hermes config）
  - 1.3 文件位置地图：`~/.hermes/SOUL.md`、项目根上下文文件、`~/.hermes/config.yaml`
  - 1.4 推荐工作流总览（官方 Recommended workflow 扩展版）

### 第二章：全局身份 — 配置 `~/.hermes/SOUL.md`
- **篇幅**：中
- **覆盖要点**：SOUL.md 位置与加载规则、自动 seed 与永不覆盖、职责划分（"跟随你到处走 → SOUL.md"）、内容约束（安全扫描 + 截断）、personality 预设
- **素材引用**：S1, S3
- **代码示例**：有（SOUL.md 内容示例）
- **章节结构**：
  - 2.1 位置与加载：只从 `$HERMES_HOME` 加载、不探测 CWD（身份不随项目漂移）
  - 2.2 自动 seed 与"已有文件永不覆盖"的边界
  - 2.3 该写什么：SOUL.md vs AGENTS.md 职责判断（对照 Claude Code 的全局 vs 项目指令）
  - 2.4 内容约束：注入安全扫描、`context_file_max_chars` 截断（floor 20k / ceiling 500k）、空文件回退默认身份
  - 2.5 personality 预设与自定义 personalities

### 第三章：项目规则 — 配置项目上下文文件（AGENTS.md 系列）
- **篇幅**：长
- **覆盖要点**：上下文文件优先级链（first-match-wins）、AGENTS.override.md 个人化、目录链合并与去重、渐进子目录发现、注入安全扫描、兼容复用已有 CLAUDE.md/.cursorrules
- **素材引用**：S2, S3
- **代码示例**：有（AGENTS.md 示例、monorepo 目录链结构、.hermes.md/override 示例）
- **章节结构**：
  - 3.1 优先级链：`.hermes.md`/`HERMES.md` → `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`
  - 3.2 `AGENTS.override.md`：个人差异又不动仓库文件的方案（对照 `.claude/rules` 个人层）
  - 3.3 目录链合并：git root → CWD 逐层加载、深层优先、相同副本去重；非 git 仓库只看 CWD
  - 3.4 渐进子目录发现：会话中按需注入（每目录至多一次、上溯 5 级、8000 chars 截断）
  - 3.5 注入安全扫描与 `[BLOCKED: ...]` 行为
  - 3.6 兼容复用：已有 CLAUDE.md / .cursorrules 无需改名直接生效

### 第四章：对照迁移 — 从 Claude Code 一键导入
- **篇幅**：中
- **覆盖要点**：`hermes import-agent claude-code` 映射表、导入行为（preview-first / merge-not-replace / 冲突跳过）、Bash 规则转 glob、非 Bash 规则 unmapped、凭证永不导入
- **素材引用**：S9, S7
- **代码示例**：有（`--dry-run` 预览命令、导入报告解读、补密钥方式）
- **章节结构**：
  - 4.1 导入映射表：全局 CLAUDE.md → MEMORY.md / settings.json allow-deny → command_allowlist + approvals.deny / mcpServers → mcp_servers / skills → skills 导入目录
  - 4.2 导入行为：preview-first（非交互停在预览）、merge-not-replace、冲突默认跳过（`--overwrite` 覆盖）
  - 4.3 Bash 前缀规则转 glob（`Bash(npm run test:*)` → `npm run test*`）；非 Bash 权限标记 unmapped
  - 4.4 凭证永不导入：`.credentials.json` 不读、MCP 密钥名剔除；手动补 `~/.hermes/.env` 或 `hermes setup`
  - 4.5 导入后核对清单

### 第五章：自动化与拦截 — 配置 `config.yaml` hooks
- **篇幅**：长
- **覆盖要点**：四类 hook 系统总览、shell hooks 配置 schema、hooks_auto_accept、pre_tool_call 阻塞/改写与 JSON 线协议、Claude-Code 兼容返回形状、实战示例
- **素材引用**：S8, S7
- **代码示例**：有（`config.yaml` hooks 块、hook 脚本 stdin/stdout JSON、block/modify 返回示例）
- **章节结构**：
  - 5.1 四类 hook 系统总览：Gateway `HOOK.yaml`+handler.py / plugin `register_hook()` / shell hooks / outbound webhooks（对照 Claude Code settings.json hooks）
  - 5.2 shell hooks 配置 schema：`hooks.<event>: [{matcher, command, timeout(默认60/上限300), fail_closed(默认false，仅 pre_tool_call)}]`
  - 5.3 `hooks_auto_accept: false` 与首次使用征询同意
  - 5.4 `pre_tool_call` 实战：`block`（需 message）/ `modify`（改写 tool_input）；JSON 经 stdin 进、stdout 出；超时 fail-closed
  - 5.5 Claude-Code 兼容双形状：`{"decision":"block","reason":...}` 与 `{"action":"block","message":...}`
  - 5.6 实战示例：拦截危险命令、自动格式化、pre_llm_call 注入上下文

### 第六章：验证与排错 — 让规则确实生效
- **篇幅**：中
- **覆盖要点**：验证命令族（doctor / config / status / prompt-size）、用 prompt-size 确认规则进入系统提示、隔离开关（--ignore-rules / --ignore-user-config / --safe-mode）、常见坑与"配置→验证"完整工作流
- **素材引用**：S7, S2, S3
- **代码示例**：有（`hermes doctor`、`hermes config check/get`、`hermes prompt-size` 命令与输出解读）
- **章节结构**：
  - 6.1 验证命令族：`hermes doctor [--fix]` / `hermes config show|edit|get|set|unset|check` / `hermes status`
  - 6.2 用 `hermes prompt-size [--platform][--json]` 离线确认 SOUL.md / AGENTS.md 是否进入系统提示
  - 6.3 隔离排错开关：`--ignore-rules`、`--ignore-user-config`、`--safe-mode`（对照 Claude Code 排查法）
  - 6.4 常见坑：规则未生效、优先级/覆盖顺序理解错误、被安全扫描拦截、与内置默认冲突
  - 6.5 一条完整的"配置 → 验证 → 对照 safe-mode"工作流

---

## 素材缺口（写作时需补充）

- hooks 的 `matcher` 正则规则与 `pre_llm_call` 注入上下文的完整示例：P2 素材（S8）只给了 schema，示例细节需在 chapter-writer 阶段补抓 S8 对应小节。
- `.hermes.md` 的 YAML frontmatter"预留未来 config override"能力官方未明确定义，写作时按"当前仅当普通指令读取、不依赖 frontmatter 行为"处理。
- Profiles（per-profile SOUL.md/config）与 Managed Scope（/etc/hermes 叶级合并）未在本轮方向内深读，若用户后续需要可单独补一篇。

## 学习路径说明

### 前置要求
- 用过 Claude Code，熟悉 CLAUDE.md、.claude/rules、settings.json、hooks 分层配置（本笔记全程以其为对照锚点）。
- 本机已安装 Hermes Agent（v0.20.x 附近），或能按笔记内的命令自行安装初始化。
- 知道 `~/.claude` 下自己的配置在哪，方便做对照迁移练习。

### 学完能做什么
- 能在 `~/.hermes/SOUL.md` 写出符合规范的全局身份配置，并理解它何时生效、何时不会生效。
- 能在项目根配置 `AGENTS.md`（及 `.hermes.md` / `AGENTS.override.md`），用优先级链和目录链管理项目级规则，并让已有的 `CLAUDE.md` / `.cursorrules` 直接复用。
- 能用 `hermes import-agent claude-code` 把自己的 Claude Code 配置一键迁入 Hermes，并安全处理密钥。
- 能用 `config.yaml` 的 `hooks:` shell hooks 拦截危险命令、注入上下文、做自动化，并兼容 Claude Code 风格返回。
- 能用 `hermes doctor` / `hermes config check` / `hermes prompt-size` 验证规则确实生效，并用 `--safe-mode` 对照排查问题。

### 建议学习顺序
- 第一章 → 第二章 → 第三章（打好规则体系基础，先全局后项目）
- 第四章 对照迁移可在第三章后随时做（把已有 Claude Code 配置导进来对照学习）
- 第五章 hooks 建议在规则文件都跑通后再上（依赖前三章的 config.yaml 基础）
- 第六章 验证与排错可穿插使用：每配完一章就用对应命令验证，最后再通读全章做系统排查
- 预计总学习时间：约 3–5 小时（含动手配置与验证）
