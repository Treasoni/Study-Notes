# DeepSeek-Harness 教程 · 更新报告（2026-08-14）

## 更新摘要

| 文件 | 变更 | 方式 |
|---|---|---|
| [[DeepSeek-Harness 配置体系]] | 新增 3.8 插件开发基础（第一个插件）、3.9 system-prompt 子系统参考；frontmatter `updated`→2026-08-14、`status`→updated；本章小结追加一行；文末追加更新记录 + 脚注 [^2][^3] | patch-in-place |
| [[DeepSeek-Harness 是什么]] | 1.2 补一句第一个插件开发入口（双链到配置体系 3.8）；frontmatter `updated`→2026-08-14、`status`→updated；文末追加更新记录 | patch-in-place |
| [[DeepSeek-Harness MOC]] | 03 配置体系 描述行追加「插件开发、系统提示词组装」 | patch-in-place |
| [[AI学习 MOC]] | 配置体系索引行说明追加「插件开发、提示词组装」 | patch-in-place |

## 来源

1. https://deepseek-harness.github.io/deepseek-harness/develop/basic/ —— 官方「开发基础：第一个插件」（2026-08-14 抓取）
   - 提取：插件 = 导出 `apply(ctx)` 的 TS 模块；cordis.yml patch 注册（**路径必须绝对**）；启动 `pnpm dsh web --patch ./scratch-plugin/cordis.yml`；自动清理与 `ctx.effect()`；`inject` 依赖；函数/对象/类三种形态。
2. https://deepseek-harness.github.io/deepseek-harness/reference/subsystems/system-prompt —— 官方「system-prompt 子系统参考」（2026-08-14 抓取）
   - 提取：`ctx.systemPrompt` 注册表；PromptSection（name 唯一 / order 升序 / text 可函数+`{{variable}}` / complete）；order 约定（-100 身份、0 人格、100–199 工具指导）；complete 段唯一化与冲突失败；作用域遮蔽 vs 工具共同贡献；assemble/change 事件；knownNames 防错；PromptContext 持久化。

## 未处理风险 / 说明

- **developer preview 变动**：文档 URL 在 `develop/` 分支下，API（Cordis 类型签名）可能随版本变化；已标注来源日期，后续升级需复核。
- **内容颗粒度取舍**：system-prompt 原页面为全量 API 类型参考（由 `scripts/gen-cordis-catalog.ts` 生成），笔记只提炼了读者需要的心智模型与关键防错点，未搬运全部签名。
- **插件开发前提**：3.8 依赖源码运行路径（run from source），与安装章节的 npm 路径不同——已在节内注明，避免读者用 `npx @deepseek-ai/dsh web` 跑插件示例。
- **未改其他章节**：第 2/4/5 章与本次两页文档无直接冲突，保留原样。

## 验证

- 配置体系围栏 14 行全部配对 ✅
- 3.8/3.9/更新记录/脚注 [^2][^3] 均就位 ✅
- 新增双链 `[[DeepSeek-Harness 配置体系|配置体系 3.8 插件开发基础]]` 目标存在 ✅
- MOC 两处描述行已同步 ✅
