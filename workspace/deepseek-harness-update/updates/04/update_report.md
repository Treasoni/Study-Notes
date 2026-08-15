# Update Report · id 04 · DeepSeek-Harness 配置体系.md

## 摘要

- **动作**：update（整篇重写，patch-in-place）
- **新标题**：DeepSeek-Harness 插件开发核心：从 apply(ctx) 到发布
- **新职责**：Ch3 插件开发核心（全书核心，篇幅最大）：插件形态 / 注册 / 生命周期 / 依赖 / 配置 / 工具 / 策略 / 发布 / 提示词子系统
- **frontmatter**：title/tags 更新；`updated: 2026-08-15`；`status: updated`

## 变更点

1. 3.1 插件是什么（apply(ctx) + 三种形态）；3.2 多层 YAML 补丁树注册（开发期 cordis.yml patch，路径必须绝对，--dump-config 排查）。
2. 3.3 Profile 与 Agent Preset 两级配置；3.4 生命周期与 effects（fiber 状态机、ctx.effect 手动资源）。
3. 3.5 服务与依赖（inject 硬依赖 / ctx.get 可选 / Service 类 + declare module 类型）。
4. 3.6 插件配置（Config 接口 + Schemastery，坏配置响亮失败，HMR）。
5. 3.7 defineTool DSL 全解；3.8 工具策略与观察（tools/pre-execute 等 hook 扩展点，含 dsh-hooks-claude-code 桥）。
6. 3.9 打包与安装（bundle vs profile、dsh plugin add、git 安装 prepare + allowBuilds 坑）。
7. 3.10 system-prompt 子系统（PromptSection/order/complete/遮蔽）作为提示词类插件参考。

## 来源

- S1–S11 全量；核心代码来自官方「第一个插件」「开发一个 Tool」「Tool authoring reference」「插件配置」「打包并安装」「Cordis 教程 01–03/05」「扩展插件形态 Cookbook」「system-prompt 子系统」（2026-08-14/15 抓取）。

## 未处理风险

- 原配置体系中的权限/模型/环境变量/CLI 细节在本篇删除，待 Ch5 速查补位（批次 2 处理）。
- 代码片段基于 2026-08-15 文档，developer preview 期签名可能变动。
- 与父级 MOC 描述行待 P5 同步。
