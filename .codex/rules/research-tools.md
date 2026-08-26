---
paths:
  - ".codex/rules"
---

# 资料收集工具指南

本指南只记录当前运行时已验证的能力；不要把示例 MCP 或历史工具当作可调用工具。

## 可用工具

| 能力 | 工具或技能 | 适用场景 |
| --- | --- | --- |
| 网页检索 | `WebSearch`、`mcp__MiniMax__web_search` | 快速查找最新资料、获取标题/URL/摘要 |
| 网页正文阅读 | `WebFetch` | 把公开网页正文转为 Markdown；不支持图片、登录页与鉴权 URL，跨域跳转需重新调用 |
| 动态页面 / 登录交互 | `mcp__browsermcp__browser_navigate`、`browser_snapshot`、`browser_click`、`browser_type`、`browser_screenshot` | 需要登录、滚动、点击、下拉选择或截图核验的页面 |
| 本地图片阅读 | `Read`（PNG/JPG/WebP/GIF） | 读取已在工作区内的图片、图表或截图 |
| 图片理解（本地或 URL） | `mcp__MiniMax__understand_image` | 从图片提取文字、描述图表、核验视觉内容；仅 JPEG/PNG/WebP |
| 视频 / 字幕 / 频道 | `mcp__youtube__search_you_tube`、`video_details`、`list_caption_track`、`get_channel_id_by_handle` | 从视频元数据、字幕和频道获取一手资料 |
| 一次性研究记录 | `research` | 基于一手来源研究问题，并把带引用的结果保存为 Markdown |
| 学习意图澄清 | `research-planner` | 想学、帮我整理、研究一下等学习需求澄清与引导 |
| 工作流内分阶段收集 | `research-collector` | 在 learning-note-flow 的 P1/P2 阶段收集、筛选和溯源资料 |

> 注：`mcp__time__*` 仅用于时区换算，与资料收集无关；`mcp__youtube__*` 的写操作（上传、改标题等）只在确需维护频道内容时使用。

## MCP 状态

- **项目配置**：`.agent-sync/mcp-servers.json` 与 `.mcp.json` 均为空 `{"mcpServers": {}}`，`.codex/config.toml` 无 MCP server，即项目未配置任何 MCP server。
- **宿主应用能力**：本运行时已连接 `browsermcp`（浏览器控制）、`MiniMax`（网页搜索 + 图片理解）、`youtube`（视频/字幕/频道）、`time`（时区）。这些由宿主应用注入，不在项目配置内，不随仓库分发。
- **不可用**：`web__run`、`view_image`、`browser:control-in-app-browser`、`chrome:control-chrome`、`defuddle` 在本运行时不可调用，不作为推荐工具列出。

## 选择顺序

1. 先搜索：`WebSearch` 或 `mcp__MiniMax__web_search` 找候选，再用 `WebFetch` 打开官方文档、论文、规范或一手公告；用页面内的锚点/小节名定位具体主张。
2. 需要登录、动态交互或可视化核验的页面，用 `mcp__browsermcp__*`（snapshot 定位 → click/type → screenshot 核验）。
3. 图片/截图：本地文件用 `Read` 或 `mcp__MiniMax__understand_image`；公开 URL 图片用 `mcp__MiniMax__understand_image`。
4. 需要系统化研究时，使用 `research`；处于学习笔记工作流的 P1/P2 时使用 `research-collector`，遵守状态文件和用户确认点。
5. 记录 URL、发布日期/更新日期、来源层级和支持的主张。不要把完整网页正文重复粘贴进下游提示词。

## 维护

每次新增、移除或连接研究型 MCP、浏览器能力或研究技能后，重新运行 `tool-discovery`。先检查实际运行时和项目 MCP 配置，再更新本文件并经 `.agent-sync` 同步；不得以技能示例代替发现结果。
