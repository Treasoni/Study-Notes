# Stale Map · id 04 · DeepSeek-Harness 配置体系.md

> 更新目标：从「配置体系（权限/模型/环境变量/CLI）」改为「插件开发核心」（Ch3，全书核心）
> 日期：2026-08-15

## 处理方式：整篇重写（patch-in-place）

| 原段落 | 判定 | 处置 |
|---|---|---|
| 配置体系的系统化讲解 | 重构 | 原 3.8 插件开发一节扩展为全书核心主线 |
| 多层 YAML 补丁树 | 保留 | 3.2 作为「插件注册机制」讲解 |
| Profile / Agent Preset 两级配置 | 保留 | 3.3 |
| （新增）插件是什么：apply(ctx)+三种形态 | 新增 | 3.1 |
| （新增）生命周期与 effects：fiber 状态机 | 新增 | 3.4 |
| （新增）服务与依赖：inject / Service / declare module | 新增 | 3.5 |
| （新增）插件配置：Config schema + Schemastery | 新增 | 3.6 |
| （新增）开发一个 Tool：defineTool DSL | 新增 | 3.7 |
| （新增）工具策略与观察：hook 扩展点 | 新增 | 3.8 |
| （新增）打包与安装：bundle vs profile | 新增 | 3.9 |
| system-prompt 子系统 | 保留 | 3.10（提示词类插件直接相关） |
| 权限 / 模型 / 环境变量 / CLI 细节 | 删除 | 精简移入第 5 章速查（Ch5） |

## 链接影响

- 文件名不变，wikilink 不断。
- 结尾下一章指针改为 Ch4 实战项目。
