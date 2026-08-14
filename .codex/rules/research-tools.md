---
paths:
  - ".codex/rules"
---

# 资料收集工具指南

本指南只记录当前运行时已验证的能力；不要把示例 MCP 或历史工具当作可调用工具。

## 可用工具

| 能力 | 工具或技能 | 适用场景 |
| --- | --- | --- |
| 网页检索与阅读 | `web__run` 的 `search_query`、`open`、`click`、`find` | 查找最新资料、读取原始页面、定位段落和链接 |
| 图片检索与网页截图 | `web__run` 的 `image_query`、`screenshot` | 寻找公开图片，或核验 PDF/网页的视觉内容 |
| 需登录或交互的网站 | `browser:control-in-app-browser`、`chrome:control-chrome` | 仅在公开网页不足且已有登录状态或页面交互必要时使用 |
| 本地图片资料 | `view_image` | 阅读已在工作区内的图片、图表或截图 |
| 一次性研究记录 | `research` | 基于一手来源研究问题，并把带引用的结果保存为 Markdown |
| 工作流内分阶段收集 | `research-collector` | 在 learning-note-flow 的 P1/P2 阶段收集、筛选和溯源资料 |

## MCP 状态

项目 `.agent-sync/mcp-servers.json` 当前没有配置 MCP server。运行时可见的文档模板与插件管理资源不提供网页检索、网页正文提取或图片识别能力，因此不用于研究资料收集。

## 选择顺序

1. 先用 `web__run` 搜索，再 `open` 官方文档、论文、规范或一手公告；用 `find` 定位具体主张。
2. 需要系统化研究时，使用 `research`；处于学习笔记工作流的 P1/P2 时使用 `research-collector`，遵守状态文件和用户确认点。
3. 只有页面需要登录、动态交互或可视化核验时，才使用浏览器控制技能或截图。
4. 记录 URL、发布日期/更新日期、来源层级和支持的主张。不要把完整网页正文重复粘贴进下游提示词。

## 维护

每次新增、移除或连接研究型 MCP、浏览器能力或研究技能后，重新运行 `tool-discovery`。先检查实际运行时和项目 MCP 配置，再更新本文件并经 `.agent-sync` 同步；不得以技能示例代替发现结果。
