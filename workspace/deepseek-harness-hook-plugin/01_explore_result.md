# 探测式收集结果 - 如何写 dsh hook 扩展点插件

> 阶段：P1 · 探测式收集
> 日期：2026-08-16
> 方法：3 个并行透镜（语义模型 / 实战代码 / 迁移对照），每个 3–5 条候选，已逐条核实 URL 可加载

## 去重后源清单（9 条）

| # | 标题 | URL | 层级 | 相关性 | 分 |
|---|------|-----|------|--------|----|
| S1 | dsh-tools 工具作者参考 | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/core/tools/README.md | official | 权威定义 `PreToolDecision`(allow/deny/ask)、`ctx.tools.register()`、完整流水线 pre-execute→guard→execute→post-execute→finalizeContent→result；含 `defineTool` 可运行 TS 示例 | 5 |
| S2 | 扩展插件形态 Cookbook | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/docs/cookbook/extension-cookbook.md | official | permission-gate 示例：`ctx.on('tools/pre-execute')` 返回 `PreToolDecision` 或 `next()`；覆盖 guard/post-execute/result 与 `apply(ctx)`；有中文镜像 extension-cookbook.zh.md | 5 |
| S3 | 工具执行流水线 | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/docs/tool-execution-pipeline.md | official | 固定顺序：pre-execute→monotonic guard→execute→post-execute→finalizeContent→result；前三个 waterfall 可改写，后三者观察/收尾 | 4 |
| S4 | @deepseek-ai/dsh-tools (npm) | https://www.npmjs.com/package/@deepseek-ai/dsh-tools | official | 导出 `PreToolDecision`/`PostToolDecision`/`ToolExecution` 核心类型；npm 页面 403，经 registry API 确认包真实存在（0.1.0-rc.6） | 4 |
| S5 | @deepseek-ai/dsh-hooks-claude-code README | https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/hooks/hooks-claude-code/README.md | official | **官方映射表**：CC `PreToolUse`→`tools/pre-execute`、`PostToolUse`→`tools/post-execute`、`UserPromptSubmit`→`agent/pre-step`、`Stop`→`agent/turn-stopping`、`SessionStart`→`agent/session-start`、`SubagentStart/Stop`→`subagent/start\|end`；其余 23 个 CC 事件不支持被忽略 | 5 |
| S6 | Claude Code Hooks reference | https://code.claude.com/docs/en/hooks | official | 源侧权威参考：30 个 hook 事件、settings.json 三层结构（事件→matcher→handler）、`hookSpecificOutput`（permissionDecision/updatedInput/additionalContext） | 4 |
| S7 | dsh-guardian | https://github.com/lonelymoon87/dsh-guardian | community | 真实 dsh 插件：pre-execute 瀑布 deny/ask + post-execute 输出脱敏；面向 DSH 0.1.0-rc.6 API；README 仅配置 YAML 无 TS 示例 | 3 |
| S8 | dsh-permission-rules (npm) | https://www.npmjs.com/package/dsh-permission-rules | community | 声明式 allow/deny/ask 三态规则插件，pre-execute 按工具名/参数/路径匹配；v0.4.2，registry 确认存在，代码未直接核实 | 3 |
| S9 | dsh-bridges (npm) | https://www.npmjs.com/package/dsh-bridges | community | 第三方插件宣称 CC `settings.json` hooks 无需迁移"原样运行"（覆盖 SessionStart/UserPromptSubmit/Pre/PostToolUse/Stop/SessionEnd）；无逐事件映射表；v0.1.0 发布 2026-08-15 | 3 |

## 方向菜单

- **A. 语义模型主线** — 以 S3 流水线顺序为骨架，讲透 5 个扩展点职责 + `next()` 瀑布 + guard 单调否决语义（配 S1 权威定义）
- **B. 实战代码主线** — 以 S2 permission-gate 为起点，手写 权限门 + guard + post-execute 改写 + result 观察 完整插件 + 验证命令链（配 S7/S8 真实插件佐证）
- **C. 迁移对照主线** — 以 S5 官方映射表为骨架，讲「把 Claude Code hook 配置搬进 dsh」+ 事件支持差异（配 S6 源侧参考）
- **D. 组合（A→B→C）**（★ 推荐）— 先语义模型，再实战落地，最后迁移对照，与意图文件探索方向一致

## 覆盖缺口（P2 需补）

1. **npm 包内部 TS 代码未核实**：S4/S8/S9 的 npm 页面被机器人拦截（403），仅经 registry 元数据确认存在；P2 需用 GitHub 源码或 registry tarball 核实实际代码
2. **`dsh-hooks-codex` 桥**：S5 侧提及其与 claude-code 桥并列，未深挖；可作为对照项补充
3. **验证命令链覆盖确认**：S2 是否含 load→dump-config→headless 验证命令需 P2 确认；无则从既有分册（08 章验证命令链）复用
4. **Claude Code 侧只取映射相关部分**：S6 共 30 事件，P2 只提取与 S5 映射表重叠的 6 个事件做比照

## 预计 P2 范围

- 核心抓取：S1、S2、S3、S5、S6（5 个官方源，claim 级笔记）
- 补充：S7/S8/S9 中至少 1 个真实插件源码（若 tarball/GitHub 可读）
- 产出：`02_deep_research.md`（范围 + 源表 + claim/源映射 + 矛盾 + 实践指引 + 开放问题 + 下游交接）
