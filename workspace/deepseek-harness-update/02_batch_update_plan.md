# 批量更新计划 · DeepSeek-Harness 教程重写（插件开发导向）

## 更新目标与判断依据

- **目标**：把整套《DeepSeek-Harness 教程》从「快速上手 + 换还是留」重构为「从 Claude Code 视角学会写自己的 dsh 插件」。
- **依据**：用户明确「主要想写自己的插件」，且「主要用 Claude Code 用得熟」。重写主线 = 用 Claude Code 扩展模型（settings.json / CLAUDE.md / hooks / MCP / skills）作桥，讲清 dsh 的插件开发。
- **手法**：patch-in-place 覆盖 7 篇，但**保留文件名**，避免破坏既有双链与父级 MOC 索引。

## 笔记分组与动作

| 组 | id | 文件 | 动作 | 新职责 |
|---|---|---|---|---|
| 核心（Ch1–Ch3） | 02 | DeepSeek-Harness 是什么.md | update | Ch1 心智模型：dsh 插件树 vs Claude Code 单体+扩展 |
| 核心 | 03 | DeepSeek-Harness 安装与快速上手.md | update | Ch2 环境准备：源码运行路径（写插件前提）+ 基础配置 |
| 核心 | 04 | DeepSeek-Harness 配置体系.md | update | Ch3 插件开发核心：apply(ctx) / cordis.yml patch / 三种形态 / inject / 工具注册（全书核心，篇幅最大） |
| 应用（Ch4–Ch5） | 05 | DeepSeek-Harness 与ClaudeCode对照迁移.md | update | Ch4 实战项目：写一个完整示例插件（Claude Code 逐项对照） |
| 应用 | 06 | DeepSeek-Harness 常见坑与速查.md | update | Ch5 插件开发速查与排错 |
| 收尾 | 01 | README.md | update | 系列导览：插件开发导向 |
| 收尾 | 07 | DeepSeek-Harness MOC.md | update | 索引更新 |

## 各篇 stale map 要点（重写核心）

1. **02 是什么**：删「换不换/是否竞品」重心；保留 Model+Harness=Agent、一切皆插件；新增「Claude Code 扩展模型回顾」对照小节；结尾指向「写插件」而非「安装上手」。
2. **03 安装**：把 npm 快跑降为次选；**源码构建路径升级为主路径**（官方插件开发文档要求 run from source）；保留 Web UI 首次配置与 headless 作为验证手段。
3. **04 配置体系**（全书核心，重构幅度最大）：把 3.8 插件开发从「一节」扩展为「主线」；保留多层 YAML 补丁树作为「插件注册的机制」讲解；新增工具注册、ctx 生命周期、inject 依赖、发布/管理；保留 3.9 system-prompt（与写提示词类插件直接相关）。
4. **05 对照迁移**：删成本/性能对比表重心（不再是「换还是留」）；改为**实战项目 walkthrough**——选一个具体插件目标（如自定义工具插件 / 提示词段落插件），从零到跑通，每步给「这在 Claude Code 里相当于」。
5. **06 常见坑**：坑清单重排为插件开发优先（路径必须绝对、ERESOLVE、Windows ctx.bash、热重载端口、编译/加载报错）；命令速查补 `dsh plugin` 全家族。
6. **01 README**：导览更新为新主线与章节职责。
7. **07 MOC**：索引行更新为新章节职责。

## 是否需要共享资料包

**需要（shared_research: yes）**。三篇核心章节（Ch2/Ch3/Ch4）共用插件开发官方素材。P3 将收集：

- 官方「开发基础：第一个插件」（已有 2026-08-14 抓取，需复核）
- 官方 developer guide 索引（是否还有 tools / services / lifecycle 页面）
- 工具注册 API 与 Service 类形态（`inject` / `ctx.effect()` / 提供服务给其他插件）
- 一个真实示例插件（repo 内 examples 或发布包）
- 发布/安装流程（`dsh plugin --profile <name> add <package>` 的机制）

## 第一批处理列表（batch_size=3）

批次 1（核心）：02 → 03 → 04
批次 2（应用）：05 → 06
批次 3（收尾）：01 → 07

## 目标输出模式与覆盖风险

- **destination_mode**：`patch-in-place`（已确认）。
- **覆盖风险**：旧版内容不可恢复（git 已跟踪，可从历史恢复）。
- **链接风险**：保留文件名 → 无断链；但每篇标题/章节职责变化，需同步父级 `AI学习/00-索引/AI学习 MOC.md` 中的描述行。
- **内容时效**：dsh 处于 developer preview，插件 API（Cordis 类型签名）可能变动；所有素材标注来源日期。

## 需用户确认项

- [x] 目标与分组（本计划）
- [ ] 是否按上述新章节职责执行（尤其是 Ch4「对照迁移」→「实战项目」的定位变化）
- [ ] 批次划分与顺序
