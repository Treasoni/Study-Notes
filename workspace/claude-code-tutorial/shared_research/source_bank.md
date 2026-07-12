# 共享资料库

> 收集时间：2026-07-12
> 来源：官方文档、官方博客、社区权威指南
> 目标版本：Claude Code v2.1.207（2026-07-11）

---

## 一、版本与更新总览

### S01: Claude Code 2026 版本更新时间线
- **来源**: [code.claude.com/docs/en/whats-new](https://code.claude.com/docs/en/whats-new)（官方 What's New）
- **日期**: 2026 全年
- **适用范围**: 所有笔记
- **摘要**:
  - **最新版 v2.1.207**（2026-07-11）：Auto mode 在 Bedrock/Vertex AI/Foundry 可用；默认模型改为 Opus 4.8；终端卡顿修复；插件安全修复
  - **v2.1.205**（2026-06-30）：`/checkup` 自诊断工具（清理无用 skills/MCPs/插件，重构特大 CLAUDE.md，禁用慢 hooks）
  - **Q2 2026**：Dynamic Workflows（5月28日GA）；Claude Opus 4.8（Week 22）；Auto mode Pro 计划支持；Computer use CLI（研究预览）；Artifacts；`/cd` 命令；`/code-review`；`/usage`；`claude agents`；Ultraplan；`--safe-mode`；Fallback 模型
  - **Q1 2026**：Auto mode 研究预览（3月）；Claude Opus 4.7（Week 16）；Agent teams 预览；LSP 工具；Auto-memory；`claude remote-control`；`--worktree`；Windows ARM64 原生支持

### S02: Claude Code CLI 命令参考
- **来源**: 官方文档 + 社区整理
- **日期**: 2026-07
- **适用范围**: 批次1（CLI 完整参考、如何使用）
- **摘要**:
  - 启动：`claude`（交互）、`claude -p "query"`（打印模式）、`claude -c`（继续）、`claude --resume <name>`（恢复）、`claude --from-pr <number>`（从 PR 恢复）、`claude agents`（视图）
  - 核心 Slash 命令：`/init`、`/compact`、`/clear`、`/context`、`/cost`、`/model`、`/plan`、`/memory`、`/rewind`、`/diff`、`/fork`、`/todos`、`/goal`、`/cd`、`/fast`、`/usage`、`/code-review`、`/effort`、`/checkup`
  - 2026 年新增命令：`/cd`（切换工作目录）、`/code-review`（正确性审查）、`/usage`（配额明细）、`/effort`（努力级别）、`/checkup`（自诊断）、`/fast`（速度优化）
  - 重要 Flag：`--model`、`--dangerously-skip-permissions`、`--output-format json`、`--allowedTools`、`--max-turns`、`--max-budget-usd`、`--safe-mode`、`--bare`、`--worktree`/`-w`

---

## 二、配置与定制

### S03: CLAUDE.md 最佳实践
- **来源**: [claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)（官方博客）
- **日期**: 2026-07
- **适用范围**: 批次5（CLAUDE.md 指南）
- **摘要**:
  - **限制 200 行以内**——超长降低依从性
  - **层次**：组织管理 → `~/.claude/CLAUDE.md`（用户）→ `./CLAUDE.md`（项目）→ `./CLAUDE.local.md`（本地）
  - **子目录 CLAUDE.md**：仅当 Claude 读取目录内文件时加载——适合 monorepo
  - **`@import`**：拉入其他文件（最多 4 层嵌套）
  - **`.claude/rules/` + `paths:` 元数据**：路径范围规则，触及时才加载——节省上下文预算

### S04: Hooks 完整参考
- **来源**: [ThamJiaHe/claude-code-handbook](https://github.com/ThamJiaHe/claude-code-handbook/blob/main/docs/hooks-guide.md) + 官方文档
- **日期**: 2026-03（v2.1.83+）
- **适用范围**: 批次3（Hooks 指南）
- **摘要**:
  - **Hook 类型**：`command`、`http`、`mcp_tool`、`prompt`、`agent`（新增）
  - **24+ 事件**，7 类别：会话生命周期、工具执行、Agent/团队、上下文压缩、通知/MCP、版本控制、文件系统
  - **事件**：SessionStart/End、UserPromptSubmit、PreToolUse、PermissionRequest、PostToolUse、PostToolUseFailure、SubagentStart/Stop、Stop、CwdChanged、FileChanged（v2.1.83+）
  - **Matcher 模式**：`"Edit|Write"`、`"mcp__github__.*"`、`"^Bash$"`、`""/通配符`
  - **退出码**：0 = 允许（stdout 进入上下文）；2 = 阻止（stderr 反馈给 Claude）；其他 = 非阻止错误
  - **配置作用域**：`~/.claude/settings.json`（全局）→ `.claude/settings.json`（项目）→ `.claude/settings.local.json`（本地）→ managed-settings.d/（企业）
  - **v2.1.83+** 新增：CwdChanged、FileChanged 事件、managed-settings.d/ 目录
  - **"永不"放 CLAUDE.md**的事项，必须通过 Hooks 或权限强制执行

### S05: Skills（Agent Skills 标准）
- **来源**: 官方文档 + [agentskills.io](https://agentskills.io)
- **日期**: 2026-07
- **适用范围**: 批次5（Skills 编写指南）
- **摘要**:
  - **Agent Skills 开放标准**，可移植（Claude Code、Cowork 等）
  - 目录：`.claude/skills/<skill-name>/SKILL.md`
  - **关键 frontmatter**：`name`、`description`（最重要——触发）、`allowed-tools`、`context: fork`、`model: haiku`、`argument-hint`、`disable-model-invocation`
  - **描述要 "pushy"**——列出具体触发词提高自动调用率
  - **SKILL.md < 500 行**——参考资料放单独文件
  - **命名参数**（v2.1.199+）；`disallowed-tools` 字段
  - Skills vs Subagents：Skill 在主线程执行（可观察）；Subagent 隔离执行（不污染上下文）

---

## 三、高级功能

### S06: Subagents 完整指南
- **来源**: [claude.com/blog/subagents-in-claude-code](https://claude.com/blog/subagents-in-claude-code)（官方博客） + 社区实践
- **日期**: 2026-06
- **适用范围**: 批次1（Subagents 指南）、批次6（实战练习、多Agent）
- **摘要**:
  - **内置类型**：Explore（阅读/搜索，2026 年新增）、Plan（架构规划）、General-purpose（编码）
  - **自定义**：`.claude/agents/*.md`——`description` 字段决定自动路由
  - **调用方式**：自动委托、自然语言、@-mention、`--agent` 标志
  - **什么时候用**：需阅读 10+ 文件、多个独立子任务、需要无偏见审查、提交前审查
  - **模型策略**：Haiku（搜索/文档生成）→ Sonnet（代码实现/重构）→ Opus（安全审计/架构评审）
  - **最佳实践**：范围精确、明确输出格式、使用隔离上下文（fork）、只读审查者不写权限
  - **不要过度委托**：单文件读取不划算
  - 2026 年新特性：默认后台运行，嵌套最多 5 层

### S07: Dynamic Workflows
- **来源**: [claude.com/blog/introducing-dynamic-workflows-in-claude-code](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code)（官方博客）
- **日期**: 2026-05-28（GA）
- **适用范围**: 批次4（Dynamic Workflows 指南）、批次6（多Agent 流程设计）
- **摘要**:
  - **Claude 自行编写多 Agent 编排脚本**——运行时生成 JavaScript 编排器
  - **6 种模式**：Classify-and-act、Fan-out-and-synthesize、Adversarial verification、Generate-and-filter、Tournament、Loop-until-done
  - **适用场景**：跨仓库迁移、批量重构、安全审计、日志分析——大规模并行化
  - **不适合**：小功能、单文件、顺序简单任务、token 预算紧张
  - **真实案例**：Bun 迁移（Zig→Rust）75 万行、99.8% 测试通过率、11 天完成

### S08: Claude Code Memory 机制
- **来源**: 官方文档 + 社区整理
- **日期**: 2026
- **适用范围**: 批次2（Memory 指南）
- **摘要**:
  - **CLAUDE.md** 是项目级持久化记忆（显示管理，每次加载）
  - **Auto-memory**（2026 Q1 新增）：Claude 自动保存/回忆有用上下文
  - **`/memory`**：不离开会话编辑 CLAUDE.md
  - **`/compact`**：压缩会话上下文释放空间
  - **Session context** 约 200K tokens（取决于模型）
  - 1M token 上下文窗口（Sonnet 5/Opus 4.8）

### S09: Checkpoints
- **来源**: 官方文档
- **日期**: 2026
- **适用范围**: 批次4（Checkpoints 指南）
- **摘要**:
  - **`/rewind`**：将对话/代码回滚到检查点
  - **`/fork`**：创建临时会话分支
  - **`claude --resume <name>`**：恢复命名会话
  - **`claude -c`**：继续最近的会话
  - Checkpoints 是自动的还是在关键状态保存——与 /rewind 配合使用可安全实验

### S10: 会话管理与工作流
- **来源**: 官方文档
- **日期**: 2026
- **适用范围**: 批次4（会话管理）、批次6（定时任务）
- **摘要**:
  - **`claude agents`**（2026 Q2 新增）：统一视图——所有会话（运行中、阻塞、已完成）
  - **Background agents**：新版安装后自动升级
  - **`/todos`**：跨会话持久化任务列表
  - **`/goal`**：保持工作直到完成条件满足
  - **`--worktree`/`-w`**：隔离 git worktree
  - **`claude remote-control`**：将会话暴露给外部构建
  - **`Ultraplan`**：云中起草计划，Web 编辑器中查看/编辑，远程运行或拉回本地

---

## 四、MCP 协议

### S11: MCP (Model Context Protocol) 完整指南
- **来源**: [modelcontextprotocol.io](https://modelcontextprotocol.io) + 社区指南
- **日期**: 2026-07
- **适用范围**: 批次7（MCP 指南）
- **摘要**:
  - MCP 已从 Anthropic 倡议演变为 **Linux Foundation AI Foundation (AAIF)** 治理的行业标准
  - **社区服务器数万**，官方集成 50+，插件中心 9,000+
  - **传输方式**：stdio（默认，本地进程）、streamableHttp（推荐远程，取代 SSE）、WebSocket
  - **配置加载**：7 个作用域（local、user、project、enterprise、managed、claudeai、dynamic）
  - **工具包装**：名称规范化→描述截断（2048 字符上限）→Schema 透传→注解映射
  - **OAuth 2.0 + PKCE**：完整支持，含 RFC 发现链
  - **超时**：连接 30s、请求 60s、工具调用 ~27.8h、OAuth 30s
  - **MCP CLI v0.3.0**：3 子命令架构（info、grep、call），连接池减少 40-60% 调用开销
  - **MCP Tool Search**：按需加载工具定义，减少约 85% 上下文消耗
  - **远程 MCP 原生支持**：零安装连接远程 URL，支持浏览器 OAuth 认证
  - 推荐保持 5-8 个 MCP 服务器

---

## 五、模型配置

### S12: 模型与推理设置
- **来源**: [support.claude.com](https://support.claude.com/en/articles/11940350-claude-code-model-configuration)（官方）
- **日期**: 2026-07
- **适用范围**: 批次2（模型与推理设置）
- **摘要**:
  - **支持的模型**：Sonnet 5（默认 1M 上下文）、Fable 5、Opus 4.8（Max/Team Premium 默认）、Opus 4.7、Sonnet 4.6、Opus 4.6、Haiku 4.5
  - **`--model <name>`**：会话开始时覆盖模型
  - **`/model`**：会话中切换模型
  - **Fallback 模型**（2026 Q2 新增）：最多配置 3 个 fallback 模型按顺序尝试
  - **`/effort`**：设置努力级别（standard/high/xhigh）
  - **`/fast`**：速度优化 API 设置切换
  - 不同模型适合不同任务类型——Haiku（快速搜索）、Sonnet（日常工作）、Opus（复杂推理）
