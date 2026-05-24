# CodeGraph 参考资料

## 推荐优先级排序

| 优先级 | 来源 | URL | 类型 | 用途 |
|--------|------|-----|------|------|
| ⭐⭐⭐ | CodeGraph GitHub | https://github.com/colbymchenry/codegraph | official | 完整文档、benchmark、CLI/MCP 参考 |
| ⭐⭐⭐ | CodeGraph Documentation | https://codegraph.ru/docs/en/index.html | official | 分类文档、配置指南 |
| ⭐⭐ | dev.to: Understand Anything | https://dev.to/arshtechpro/understand-anything-turn-any-codebase-into-an-interactive-knowledge-graph-37ed | blog | 知识图谱工具对比、Understand Anything 详细介绍 |
| ⭐⭐ | Medium: How I Simplified | https://medium.com/@learn-simplified/how-i-simplified-project-dev-using-code-graph-f94fefb84648 | blog | 实战经验分享 |
| ⭐ | B站: CodeGraph 介绍 | https://www.bilibili.com/video/BV1UwGq6SEiL | video | 中文入门介绍 |
| ⭐ | B站: 三大工具对比 | https://www.bilibili.com/video/BV1S4G66FEoB | video | CodeGraph/GitNexus/Graphify 对比 |

## 性能基准数据来源

官方 Benchmark 详情：

| 测试项目 | 语言 | 文件数 | 指标 |
|----------|------|--------|------|
| VS Code | TypeScript | ~10k | 成本-35%, Token-73%, 时间-41%, 工具调用-72% |
| Excalidraw | TypeScript | ~600 | 成本-47%, Token-73%, 时间-60%, 工具调用-86% |
| Django | Python | ~2.7k | 成本-34%, Token-64%, 时间-59%, 工具调用-81% |
| Tokio | Rust | ~700 | 成本-52%, Token-81%, 时间-63%, 工具调用-89% |
| OkHttp | Java | ~640 | 成本-17%, Token-41%, 时间-36%, 工具调用-64% |
| Gin | Go | ~150 | 成本-22%, Token-23%, 时间-34%, 工具调用-19% |
| Alamofire | Swift | ~100 | 成本-38%, Token-59%, 时间-51%, 工具调用-77% |

**测试方法**：Claude Opus 4.7, Claude Code v2.1.145，`claude -p` 模式，4 次运行中位数

## 支持的 Agent

- Claude Code
- Cursor
- Codex CLI
- opencode
- Hermes Agent

## 支持的语言

TypeScript, JavaScript, Python, Go, Rust, Java, C#, PHP, Ruby, C, C++, Swift, Kotlin, Scala, Dart, Svelte, Vue, Liquid, Pascal/Delphi, Lua, Luau

## 支持的框架路由

Django, Flask, FastAPI, Express, NestJS, Laravel, Drupal, Rails, Spring, Gin/chi/gorilla/mux, Axum/actix/Rocket, ASP.NET, Vapor, React Router/SvelteKit

## 竞品资料

### Understand Anything
- GitHub: 15k+ stars (截至 2026 年 5 月)
- 多 Agent 管道架构
- 支持 14+ AI 编程平台
- MIT 许可证

### GitNexus
- CLI + MCP + Web 可视化
- 支持变更风险分析

### Graphify
- 多模态知识图谱
- 代码 + 文档 + 图片 + 视频全整合
