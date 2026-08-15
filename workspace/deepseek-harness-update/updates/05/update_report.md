# Update Report · id 05 · DeepSeek-Harness 与ClaudeCode对照迁移.md

## 摘要

- **动作**：update（整篇重写，patch-in-place）
- **新标题**：实战：从零写一个自定义工具插件（每一步对照 Claude Code）
- **新职责**：Ch4 实战项目——走完骨架/工具/配置/加载/发布的完整示例，把前 3 章零件组装成车
- **frontmatter**：title/tags 更新；`updated: 2026-08-15`；`status: updated`

## 变更点

1. 删除成本/性能对比表与三选迁移策略（「换还是留」定位移除）。
2. 五步 walkthrough：4.2 骨架（apply + cordis.yml patch 绝对路径）→ 4.3 greet 最小工具 → 4.4 自定义 `repo_status` 工具 → 4.5 `Config` schema 配置 + HMR → 4.6 bundle 打包 + `dsh plugin add` + git 安装坑。
3. 每步附「这在 Claude Code 里相当于」；4.7 给完整 Claude Code → dsh 对照表。
4. V4 协议信息移交 Ch5 5.5。

## 来源

- S1（第一个插件）、S2（greet 工具）、S3（Tool authoring reference）、S4（插件配置）、S5（打包并安装）、S9（Cordis 配置）（2026-08-15 抓取）。

## 未处理风险

- `repo_status` 示例基于官方 greet 结构扩展；工具 API 在 developer preview 期可能变动。
- 与父级 MOC 描述行待 P5 同步。
