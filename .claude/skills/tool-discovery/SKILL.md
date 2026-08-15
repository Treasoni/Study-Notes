---
name: tool-discovery
description: 发现当前运行时可用于资料收集的网页、浏览器、MCP 与研究技能，并刷新项目资料工具指南。用于询问可用工具、搜索工具、研究能力或资料收集方案时。
---

# Tool Discovery

生成基于当前运行时的资料收集能力清单；示例工具和历史配置不构成可用性证据。

## Workflow

1. 读取项目路由规则并确认请求不命中必经业务工作流；检查 `git status --short`。
2. 检查实际可调用工具：`web__*`、浏览器控制能力和 `mcp__*`；如有 MCP，读取其资源和模板。
3. 读取项目 `.agent-sync/mcp-servers.json`、`.mcp.json` 与 `.codex/config.toml`，区分项目已配置 server 和宿主应用能力。
4. 扫描 `.claude/skills/*/SKILL.md`，只列出研究、资料收集、浏览器或本地资料阅读直接相关的技能。
5. 更新 `.claude/rules/research-tools.md`：列出已验证工具、适用边界、推荐选择顺序和不可用的研究型 MCP 状态。不要列出未安装工具。
6. 同步 `skills` 与 `rules` 到 Claude Code，更新 manifest 版本，并验证同步与 manifest。

## Completion Criteria

- 工具列表与当前运行时、项目 MCP 配置和已安装技能一致。
- 指南优先推荐一手来源、可追溯 URL 与按需加载，而非复制网页正文。
- `.claude/rules/research-tools.md` 与 Claude Code 生成副本无漂移。
