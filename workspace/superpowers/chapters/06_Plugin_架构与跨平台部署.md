# 第六章：Plugin 架构与跨平台部署

## 本章目的

Superpowers 的 skills 是平台无关的，但 Agent 平台有完全不同的能力、工具和集成方式。本章看 Plugin-per-Harness 模式如何用"同一份 skills + 不同平台引导"支持 10+ 个平台。

---

## 6.1 三组件架构

整个跨平台方案基于三个不变的组件：

```
┌──────────────────────────────────────────────────────────┐
│                     Skills（平台无关）                      │
│  skills/*/SKILL.md — 描述"动作"，从不命名具体工具          │
│  在所有平台上完全相同                                     │
├──────────────────────────────────────────────────────────┤
│                    Tool Mapping（每平台）                   │
│  references/<harness>-tools.md                            │
│  将动作词汇翻译为平台的真实工具名称                          │
├──────────────────────────────────────────────────────────┤
│                    Bootstrap（每平台）                      │
│  每会话开始时将 using-superpowers + tool mapping 注入      │
│  包裹在 <EXTREMELY-IMPORTANT> 标签中                       │
└──────────────────────────────────────────────────────────┘
```

### 两条不变的规则

**规则 1：技能命名动作，不是工具**
```
✅ skills/SKILL.md 中写："派发一个 subagent"
❌ skills/SKILL.md 中写："使用 Task 工具"
```
工具映射在 references/ 中按平台解析，技能主体从不需要编辑来适配平台。

**规则 2：通过平台自身安装机制发布**
```
✅ .claude-plugin/plugin.json → Claude Code 市场
✅ .codex-plugin/plugin.json → Codex 插件系统
❌ 编辑用户的 ~/.claude/settings.json
❌ 手动复制文件到项目目录
```

---

## 6.2 Plugin-per-Harness 目录

```
superpowers/
├── .claude-plugin/plugin.json      # Claude Code
├── .codex-plugin/plugin.json       # Codex CLI
├── .cursor-plugin/plugin.json      # Cursor
├── .kimi-plugin/plugin.json        # Kimi Code
├── .opencode/plugins/superpowers.js # OpenCode
├── .pi/extensions/superpowers.ts   # pi
├── gemini-extension.json           # Gemini CLI
├── hooks/
│   ├── hooks.json                  # 钩子配置
│   └── session-start              # 自举脚本
├── references/                     # 各平台工具映射
└── skills/                         # 共享技能（14个）
```

### 平台注册差异

**Claude Code**（`.claude-plugin/plugin.json`）：

```json
{
  "name": "superpowers",
  "version": "6.1.1",
  "description": "Core skills library for Claude Code...",
  "keywords": ["skills", "tdd", "debugging"]
}
```

Claude Code 自动扫描 skills/ 目录和 hooks/hooks.json——不需要显式声明路径。

**Codex**（`.codex-plugin/plugin.json`）：

```json
{
  "name": "superpowers",
  "version": "6.1.1",
  "skills": "./skills/",
  "hooks": {},
  "interface": {
    "displayName": "Superpowers",
    "description": "...",
    "category": "Developer Tools"
  }
}
```

差异：

| 维度 | Claude Code | Codex |
|------|-------------|-------|
| 技能发现 | 自动扫描 | 需显式声明 skills 路径 |
| 钩子 | hooks/hooks.json 自动加载 | 空 hooks 对象，主动抑制钩子 |
| 界面 | 无 interface 块 | 有 interface 块用于市场展示 |
| 子 Agent | Task 工具 + 命名 agent 类型 | spawn_agent + worker 角色 |
| 安装 | 市场安装 | 市场安装 |

---

## 6.3 三种集成形态

### 形态 A：Shell-hook

**适用平台**：Claude Code、Cursor、Copilot CLI

**机制**：会话启动时运行 shell 命令，读取 stdout 注入上下文

```
用户启动会话
    ↓
平台触发 SessionStart 事件
    ↓
hooks/hooks.json 匹配 → 运行 hooks/session-start
    ↓
session-start 读取 using-superpowers/SKILL.md
    ↓
输出 JSON（含转义后的技能内容）
    ↓
平台将内容注入模型 system prompt
```

**实现要点**：
- 钩子匹配 `startup|clear|compact`（每次上下文重置时重新注入）
- 使用 `async: false` 同步执行，确保模型收到内容
- 输出 JSON 形状因平台而异（`hookSpecificOutput` vs `additionalContext`）

### 形态 B：进程内插件

**适用平台**：OpenCode、pi

**机制**：JS/TS 插件，具有会话/消息生命周期回调。在代码中构建引导内容，作为用户角色消息注入。

**实现要点**：
- 读取 SKILL.md → 去除 YAML frontmatter → 组装 `<EXTREMELY-IMPORTANT>` 标签
- 作为**用户角色消息**注入（不是系统消息——多系统消息会破坏一些模型）
- 每次 agent 步骤时检查去重标记，避免重复注入
- 压缩事件时重新注入（确保内容不被丢失）

### 形态 C：说明文件

**适用平台**：Gemini CLI

**机制**：扩展声明的上下文文件，平台始终加载。文件使用 `@`-include 语法拉入 SKILL.md 和工具映射。

**实现要点**：
- 上下文文件中 `@`-include 指向 `using-superpowers/SKILL.md`
- SKILL.md 自身携带 `<EXTREMELY-IMPORTANT>` 块
- 前端内容不去除（与形态 B 不同）
- 验证：确认 `@` 语法是保证的内联扩展，不是模型可能选择读取的文件引用

---

## 6.4 无技能工具平台的降级策略

如果平台没有原生 Skill 工具（Claude Code 的 `Skill` 工具不可用），降级方案：

1. **技能发现** → 直接读取对应 `SKILL.md` 文件
2. **技能调用** → 将读到的内容作为当前上下文的一部分
3. **文件操作** → 必要能力，无可替代
4. **Shell 命令** → 必要能力，无可替代
5. **Subagent 派发** → 可降级为内联执行或报告缺失能力

---

## 本章小结

- 三组件架构：Skills（平台无关）+ Tool Mapping（每平台）+ Bootstrap（每平台）
- 两条不变规则：技能命名动作不命名工具、通过平台安装机制发布
- Plugin-per-Harness：每个平台有独立的插件目录，共享 skills/
- 三种集成形态：Shell-hook（Claude Code）、进程内（OpenCode）、说明文件（Gemini）
- Claude Code vs Codex 核心差异：技能发现、钩子系统、Subagent 派发方式
- 无原生 Skill 工具时，可降级为直接读取 SKILL.md 文件

### 下一章预告

Plugin 架构中的核心入口——**启动钩子与自举机制**。下一章深入 hooks/session-start 脚本，看它是如何读取技能内容、转义 JSON、注入上下文的。
