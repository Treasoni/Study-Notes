# Superpowers - References

## 贡献指南要点（来自 CLAUDE.md）

### 94% PR 拒绝率

几乎所有被拒 PR 都是 AI Agent 提交的，没有阅读或遵循贡献指南。维护者会公开评论"This pull request is slop that's made of lies"。

### Agent 贡献前必须做的事

1. 读完 PR 模板并填写每个部分（真实具体答案，不是摘要）
2. 搜索已有的 Open 和 Closed PR
3. 验证这是真实问题（不是"帮我修一些 issue"）
4. 确认改动属于 core（不是特定领域/工具）
5. **身份披露**：必须说明模型、harness、版本、所有已安装插件
6. **让 human partner 审阅完整 diff 并明确批准**

### 不接受的 PR 类型

| 类型 | 原因 |
|------|------|
| 第三方依赖 | Superpowers 零依赖设计 |
| "合规"改动 | 内部 Skill 哲学与 Anthropic 官方不同 |
| 项目特定配置 | 应该作为独立插件发布 |
| 批量/撒网式 PR | 每个 PR 需要真正的理解 |
| 推测性修复 | 必须解决真实问题 |
| 领域特定 Skill | 核心只包含通用 Skill |
| Fork 特定改动 | 不要把 fork 改动推到上游 |
| 虚构内容 | 立即关闭 |
| 捆绑无关改动 | 拆分为独立 PR |

### Skill 改动需要评估

- 用 `superpowers:writing-skills` 开发和测试改动
- 跨多个会话运行对抗性压力测试
- 在 PR 中展示前后评估结果
- 不要修改精心调优的内容（红旗表、合理化列表、"human partner"用语）

## 项目元信息

| 属性 | 值 |
|------|-----|
| 作者 | Jesse Vincent (obra) |
| 组织 | Prime Radiant |
| License | MIT |
| Discord | https://discord.gg/35wsABTejz |
| Issue Tracker | https://github.com/obra/superpowers/issues |
| 发布公告 | https://primeradiant.com/superpowers/ |
| 博客公告 | https://blog.fsck.com/2025/10/09/superpowers/ |

## 相关概念

| 概念 | 说明 |
|------|------|
| YAGNI | You Aren't Gonna Need It — 不写当前不需要的功能 |
| DRY | Don't Repeat Yourself — 不重复 |
| TDD | Test-Driven Development — 测试驱动开发 |
| Socratic Method | 苏格拉底式提问 — 通过提问引导思考 |
| Subagent | 子代理 — 由主代理派发的独立执行单元 |
| Harness | 平台/宿主 — AI 代理运行的 IDE/CLI 环境 |
| CSO | Claude Search Optimization — 优化 Skill 的可发现性 |
| Human Partner | 人类伙伴 — Superpowers 刻意使用的协作术语 |
