# Update Report · id 02 · DeepSeek-Harness 是什么.md

## 摘要

- **动作**：update（整篇重写，patch-in-place）
- **新标题**：DeepSeek-Harness 插件开发：心智模型——插件树 vs 单体 + 扩展
- **新职责**：Ch1 心智模型，用 Claude Code 扩展体系作桥，建立「一切皆插件、你写的插件与官方插件对等」的心智
- **frontmatter**：title/tags 更新；`updated: 2026-08-15`；`status: updated`

## 变更点

1. 新增 **1.3 Claude Code 扩展模型对照表**：hooks → 扩展点监听；CLAUDE.md → systemPrompt section；MCP → tools.register；Skills → section+工具；Subagent → ctx.subagents；settings.json → cordis.patch.yml；自定义工具 → defineTool。
2. 新增 1.4「为什么要先转心智模型」：Claude Code 改配置 vs dsh 写代码 + patch。
3. 删除「换还是留/是否竞品」视角。
4. 保留 Model+Harness=Agent、一切皆插件、developer preview 避坑，精简后并入对应小节。

## 来源

- S1（第一个插件）、S10（扩展插件形态 Cookbook）、S11（system-prompt）；官方仓库 README（2026-08-13/15 抓取）。

## 未处理风险

- dsh 处于 developer preview，接口可能变动；对照表基于 2026-08-15 抓取文档。
- 与父级 `AI学习/00-索引/AI学习 MOC.md` 描述行待 P5 同步。
