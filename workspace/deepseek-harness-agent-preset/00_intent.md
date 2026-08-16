# 意图文件：写自己的 DeepSeek-Harness Agent Preset

## 用户原始请求
- "如何写自己的（Agent Preset），我有相关的笔记吗？"
- "需要"（确认新建实操专册形态，选「新建实操专册（推荐）」）

## 意图澄清
- **笔记类型**：实战专册（选→换→造 全流程 + 真实自定义示例 + 验证步骤）
- **学习深度**：上手（会复制/自定义 preset 并用起来，不深入插件源码开发）
- **用户基础**：熟悉 Claude Code + 已通读 DeepSeek-Harness 系列（尤其《配置体系》§2.1）
- **核心问题**：如何写自己的 Agent Preset？机制是什么？步骤是什么？写完后如何选用/验证？

## 已确定的关键结论（官方 preset 文档 + 内置 preset 源码核对）
1. **preset = 一个目录**：`agent.cordis.yml`（必需，插件行装配清单）+ 可选 `preset.yml`（只放展示文本 name/description）；id = 目录名
2. **写自己的 = 复制 → 改清单 → 改展示名**：官方 preset 只读，复制到用户根 `~/.dsh/.agent-presets/<id>/` 再改
3. **官方 4 preset 真实身份**：`standard`（母版）/ `code`（standard 完整副本，Code Mode SDK）/ `cordis`（standard 完整副本 + 自指创作能力）/ `minimal`（双工具极简，persona `complete: true`）
4. **规范创作 API**：`ctx.agentPresets.copy(from, id, name?)` 是唯一创作写入；`cordis` 创造模式专门干这个
5. **生效方式**：会话选择器选用 / 配置层 `agent-presets: { default: <id> }` / `mount(agentCtx, id?)`；发现不缓存，写完立即可见

## 输出位置策略
- 系列目录：`AI学习/DeepSeek-Harness 教程/`（零散分册模式，独立单篇）
- 文件名：`DeepSeek-Harness Agent Preset 实操.md`
- MOC：更新 `AI学习/DeepSeek-Harness 教程/DeepSeek-Harness MOC.md`
- Vault：用户 Obsidian vault（`AI学习/` 即 vault 内路径）

## 模式
- 单篇独立分册 → **freeform 模式**（跳过 P3 大纲 / P4 逐章写作，直接产出单篇）
