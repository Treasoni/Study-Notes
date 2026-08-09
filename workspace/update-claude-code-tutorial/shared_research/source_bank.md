# 共享资料来源库 — Claude Code 2026-07/08 变更

> 更新：2026-08-10
> 覆盖版本：v2.1.193 ~ v2.1.226（截至 2026-08-10）
> 用途：P4 note-updater 逐篇更新的公共基线。单篇专项资料由 note-updater 补充。

## 主来源

| 来源 | URL | 日期 |
|------|-----|------|
| Claude Code 官方 changelog（docs） | https://code.claude.com/docs/en/changelog | 持续更新 |
| Claude Code What's New（周刊） | https://code.claude.com/docs/en/whats-new | 每周 |
| GitHub CHANGELOG.md（原始） | https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md | 持续更新 |
| Week 28 digest（7/6–7/10） | https://code.claude.com/docs/en/whats-new/2026-w28 | 2026-07-10 |

---

## 1. 模型变化

### [SB-01] Claude Sonnet 5 成为默认模型（1M 上下文）
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.197（2026-06 下旬）
- **适用笔记**: cc01, cc05, cc12, cc19
- **摘要**: Sonnet 5 成为 Claude Code 默认模型，原生 1M token 上下文，促销价 $2/$10 每 Mtok，促销持续至 2026-08-31。影响「模型选择」相关章节的默认值描述。

### [SB-02] Claude Opus 5 成为默认 Opus 模型
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.219（2026-08 上旬）
- **适用笔记**: cc05, cc12
- **摘要**: `claude-opus-5` 成为新默认 Opus 模型，1M 上下文，fast 模式 $10/$50 每 Mtok。之前各篇若写「默认 Opus 4.x」需更新。

### [SB-03] Bedrock/Vertex/AWS 默认 Opus 4.8 + Auto mode 免 opt-in
- **URL**: https://dev.classmethod.jp/en/articles/20260711-cc-updates-v2-1-207/ ；https://code.claude.com/docs/en/changelog
- **日期**: v2.1.207（2026-07-11）
- **适用笔记**: cc05, cc12
- **摘要**: 第三方平台（Bedrock、Vertex、Claude Platform on AWS）默认模型改为 Opus 4.8；Auto mode 无需 `CLAUDE_CODE_ENABLE_AUTO_MODE` 即可用，可用 `disableAutoMode` 关闭。

---

## 2. 权限模式与 CLI

### [SB-04] 权限模式重命名：Default → Manual
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.200
- **适用笔记**: cc02, cc03, cc06
- **摘要**: 「Default」权限模式全面改名「Manual」，CLI 用 `--permission-mode manual`，settings 用 `"defaultMode": "manual"`。旧名描述需替换。

### [SB-05] CLI 新标志与环境变量
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.208–v2.1.223（2026-07/08）
- **适用笔记**: cc03, cc10
- **摘要**: 新增 `--ax-screen-reader`（无障碍屏读）、`--forward-subagent-text`（stream-json 透传子代理文本）、`--max-budget-usd` 停止后台子代理；`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`、`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`（禁用嵌套）、`CLAUDE_CODE_DISABLE_1M_CONTEXT`（强制 1M 模型回 200K 自动压缩）。

---

## 3. Subagents

### [SB-06] Subagents 默认后台运行 + 并发/嵌套规则
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.198 / v2.1.217 / v2.1.219
- **适用笔记**: cc10, cc04, cc12
- **摘要**: 子代理默认在后台运行；并发上限默认 20；v2.1.217 起默认禁止嵌套，v2.1.219 恢复嵌套深度 3；v2.1.224 移除每会话 200 个 spawn 上限。`/subtask` 取代旧的 in-session 子代理；`/tasks` 保留已完成后台代理。

### [SB-07] 子代理文件隔离与安全
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.216 / v2.1.222 / v2.1.225
- **适用笔记**: cc10, cc12
- **摘要**: worktree 隔离的子代理不能再对主 checkout 执行破坏性 git 命令（含 `git -C`/`--git-dir` 重定向）；`EnterWorktree` 对 `.claude/worktrees/` 之外的工作树先确认。

---

## 4. 命令与 Slash Commands

### [SB-08] /fork、/subtask、/resume
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.212
- **适用笔记**: cc04, cc13
- **摘要**: `/fork` 把当前对话复制到新后台会话；旧 in-session 子代理改为 `/subtask`；agent 视图 `/resume` 打开历史会话选择器并以后台会话恢复。`/rewind` 可恢复到 `/clear` 之前的对话。

### [SB-09] /review 变为 /code-review 别名；不再自动执行
- **URL**: https://dev.classmethod.jp/en/articles/20260806-cc-updates-v2-1-223/ ；https://code.claude.com/docs/en/changelog
- **日期**: v2.1.215 / v2.1.218 / v2.1.223
- **适用笔记**: cc13, cc02
- **摘要**: Claude 不再自行运行 `/verify`、`/code-review`，需手动调用；`/code-review` 作为后台子代理运行；`/review` 现在是 `/code-review` 的别名并复用上次 effort 等级。旧 `/simplify` 关系需更新。

### [SB-10] /doctor（=/checkup）全量体检
- **URL**: https://code.claude.com/docs/en/whats-new/2026-w28
- **日期**: v2.1.205/206/210
- **适用笔记**: cc02, cc13
- **摘要**: `/doctor` 是全量环境体检，可诊断并修复：安装健康、未用 skills/MCP/插件（上下文成本）、CLAUDE.md 去重与裁剪建议、慢 hooks 标记；别名 `/checkup`。`/status` 现在显示会话类型（interactive / attached / unattended）。

### [SB-11] Slash/Skill 叠加调用
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.199
- **适用笔记**: cc13, cc15
- **摘要**: 可叠加 `/skill-a /skill-b do XYZ` 形式连续加载最多 5 个前置 skill。`/status`、emoji 自动补全（`:thumbsup:`）等交互细节更新。

---

## 5. settings.json

### [SB-12] settings.json 新增配置键
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.200–v2.1.225
- **适用笔记**: cc06
- **摘要**: 新增 `emojiCompletionEnabled`、`vimInsertModeRemaps`（如 `jj`→Esc）、`axScreenReader`、`sandbox.filesystem.disabled`（跳过文件系统隔离但保留网络出口控制）、`sandbox.network.strictAllowlist`、`disableAutoMode`、`workflowSizeGuideline`（动态工作流规模建议）、`crossSessionInbound`/`dialogExpiry`（跨会话消息）、`autoMode.classifyAllShell`（所有 shell 命令走 auto 分类器）。`"defaultMode"` 值改为 `manual`。

### [SB-13] 沙盒与安全配置
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.216 / v2.1.221 / v2.1.224
- **适用笔记**: cc06, cc12
- **摘要**: 凭据文件 mask 模式新增 `mode: "mask"`；sandbox credential-masking 增加 `extract`/`onExtractNoMatch`、`decode: "jwt"` + `maskClaims`、`awsPairs`/`sigv4`（AWS SigV4 重新签名）。`CLAUDE_CODE_DISABLE_MOUSE_CLICKS` 禁用鼠标点击仅保留滚轮。

---

## 6. 高级功能与 Auto Mode

### [SB-14] Auto mode 行为变化
- **URL**: https://code.claude.com/docs/en/whats-new/2026-w28
- **日期**: v2.1.205 / v2.1.207
- **适用笔记**: cc12
- **摘要**: Auto mode 阻止篡改会话 transcript 文件；对 `$(…)`/backticks/`<(…)` 中的灾难性删除（如 `rm -rf ~`）即使 `--dangerously-skip-permissions` 也会提示；AskUserQuestion 对话框默认不再自动继续。桌面端 Claude Code 内置浏览器（沙盒化，外部站点有安全分类器）。

### [SB-15] 无障碍（Screen reader）
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.208
- **适用笔记**: cc12
- **摘要**: 新增屏幕阅读器模式：`claude --ax-screen-reader` / `CLAUDE_AX_SCREEN_READER=1` / `axScreenReader` 设置，把终端界面转成线性纯文本供 VoiceOver/NVDA 使用；支持删除操作的屏幕播报。

---

## 7. Hooks / MCP / Skills / 插件

### [SB-16] Hooks 更新
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.198 / v2.1.219 / v2.1.214
- **适用笔记**: cc08
- **摘要**: 新增 `Notification` hook 事件（`agent_needs_input` / `agent_completed`）；新增 `DirectoryAdded` hook（`/add-dir` 或 SDK `register_repo_root` 后触发）；单段 `dir/**` hook `if:` 条件只匹配 `<cwd>/dir`；SessionStart hook 在 headless 会话中事件流修复；插件 shell 形式 hooks 拒绝 `${user_config.*}`（注入修复）。

### [SB-17] MCP 更新
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.191 / v2.1.196 / v2.1.203 / v2.1.224
- **适用笔记**: cc14
- **摘要**: MCP capability discovery（`tools/list`、`prompts/list`、`resources/list`）对瞬时网络错误重试；修复 macOS keychain 超时导致的 MCP OAuth 401 突发；`claude mcp list/get` 不再自批准 `.mcp.json` 服务器；会话工作目录加入 MCP `roots/list`。超 2 分钟的 MCP 工具调用自动转后台。

### [SB-18] Skills 更新
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.222 / v2.1.199
- **适用笔记**: cc15, cc13
- **摘要**: skill frontmatter 支持 `disable-model-invocation`（禁止模型自动调用，让用户手动运行）；支持 `disable-model-invocation` 时 Claude 会请你运行该 skill；Slash/Skill 可叠加加载（最多 5 个前置）。

### [SB-19] 插件系统安全变化
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.207 / v2.1.224
- **适用笔记**: cc11
- **摘要**: 插件 shell 形式 `headersHelper:${user_config.*}` 被拒绝（shell 注入修复）；`pluginConfigs` 不再从项目 settings 读取；插件安装新增 `archive` 来源（HTTPS zip + 可选 SHA-256 固定）；外部插件只由项目设置启用时，每个加载路径都要求明确安装同意。

---

## 8. Caching / 会话 / Checkpoints / CLAUDE.md

### [SB-20] 1M 上下文与自动压缩
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.197 / v2.1.223
- **适用笔记**: cc19, cc05, cc04
- **摘要**: Sonnet 5 / Opus 5 原生 1M 上下文；`CLAUDE_CODE_DISABLE_1M_CONTEXT` 扩展为对所有原生 1M 模型强制 200K 自动压缩。Prompt caching 与 1M 上下文配合的命中策略需更新（长上下文分段缓存）。

### [SB-21] 会话管理行为变化
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.200 / v2.1.212 / v2.1.217 / v2.1.221
- **适用笔记**: cc04
- **摘要**: AskUserQuestion 对话框默认不再自动继续（可在 `/config` 选 idle timeout）；transcript 写入失败（如磁盘满）会警告；`/status` 显示会话类型；登录过期警告避免后台会话中断；`/usage` 修复 MCP 归因。

### [SB-22] Checkpoints / Rewind 变化
- **URL**: https://code.claude.com/docs/en/changelog
- **日期**: v2.1.191 / v2.1.216
- **适用笔记**: cc07
- **摘要**: `/rewind` 可恢复到 `/clear` 之前的对话；`/rewind` 不再通过符号链接/硬链接恢复或删除文件（防逃逸）。Checkpoints 时光机概念不变，边界行为更新。

### [SB-23] CLAUDE.md 维护建议
- **URL**: https://code.claude.com/docs/en/whats-new/2026-w28
- **日期**: v2.1.206 / v2.1.210
- **适用笔记**: cc16
- **摘要**: `/doctor` 会提议裁剪已提交的 CLAUDE.md 文件（去重、删除可由工具推导的内容）、合并重复记忆文件，并标记慢 hooks。CLAUDE.md 编写最佳实践增加「保持精简、可推导内容不写」的提示。

---

## 来源可信度备注

- 以上条目以官方 changelog / what's-new 为准；classmethod 文章仅作行为佐证。
- 部分条目（SB-06/09/12/16）跨多个版本，更新笔记时按最终状态为准。
- 若 P4 中官方 docs 页面与本文冲突，以 code.claude.com 现行文档为准并在 `update_report.md` 标注。
