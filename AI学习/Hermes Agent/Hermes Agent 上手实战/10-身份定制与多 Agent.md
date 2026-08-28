---
title: "身份定制与多 Agent：SOUL.md、Profiles 与 Bot Mode"
tags:
  - AI学习
  - Agent
  - Hermes
  - 上手实战
created: 2026-08-28
updated: 2026-08-28
status: 已完成
source_project: hermes-agent
---

> [[09-常见坑与最佳实践|⬅ 上一章]] · [[README|📖 返回目录]] · [[11-附录-命令速查|下一章 ➡]]

# 身份定制与多 Agent：SOUL.md、Profiles 与 Bot Mode

前九章把 Hermes 当"一个 agent"在用。这一章把它变成"任意多个、每个性格不同"的 agent：用 `SOUL.md` 定义全局人格、用 Profiles 拆出多套完全隔离的实例、用 Bot Mode（v0.20.3+）把这些实例编排成能互相协作的命名 bot。[^c10-1][^c10-2][^c10-3]

## SOUL.md：全局人格定制

Hermes 的"我是谁、怎么说话"由 `SOUL.md` 决定：它作为 system prompt 的 **slot #1** 被**原样注入、无任何包装文字**，并**完全替换**内置默认人格（"You are Hermes Agent..."）。文件缺失、为空或加载失败时才回退内置人格 [^c10-1]。

- **位置**：只读全局文件 `~/.hermes/SOUL.md`（自定义 home 时为 `$HERMES_HOME/SOUL.md`）；Docker 部署对应 `/opt/data/SOUL.md`
- **生命周期**：首次运行自动播种初始文件，之后**永不覆盖**；编辑只在**新会话**生效（进行中的会话不变，保住前缀缓存）
- **安全**：注入前过 prompt-injection 扫描（经典注入、promptware/C2、角色劫持模式一律阻断）
- **与 AGENTS.md 分工**：SOUL.md 放"处处适用"的人格与语气（如"说话直接"、"不写营销腔"）；AGENTS.md 放"只属于某项目"的约定（如"用 pytest 不用 unittest"、"API 跑在 8000 端口"）。规则一句话：**处处适用 → SOUL.md；单项目专属 → AGENTS.md**[^c10-1]

```markdown
# ~/.hermes/SOUL.md（内容示意；以 v0.20.x 文档为准）
你是 Hermes Agent，但说话直接、不写营销腔。
不确定时明确说"我不确定"，并把推测与证据分开。
```

官方提供 4 套起步人格模板：**Pragmatic Engineer**（直接、简洁、拒绝奉承）、**Research Partner**（好奇、诚实标注不确定性）、**Teacher/Explainer**（耐心、从直觉讲到细节）、**Tough Reviewer**（严格、直白优于外交）[^c10-1]。建议流程：先修剪种子文件、写 4-8 行语气与默认值，跑几轮对话再迭代，别一次性堆满。`/personality` 与 SOUL.md 互补：SOUL.md 是持久基线，`/personality` 只做临时切换。

> [!tip] 大白话
> SOUL.md 像"入职时签的性格说明书"：它决定 agent 是毒舌工程师还是耐心老师，全局生效、跨项目不变。想换性格就改这一份文件，重启会话生效；AGENTS.md 则是"每个项目的工作手册"，只在那个项目里生效。

## Profiles：一套 Hermes 变多套

Profiles 让一台机器上跑**多套完全隔离**的 Hermes 实例，每套拥有独立的 `HERMES_HOME` 目录：自己的 config.yaml（模型/工具）、.env（密钥）、SOUL.md（人格），以及 memories/sessions/skills/cron/gateway 状态 [^c10-2][^c10-4]。

```bash
hermes profile create coder               # 新建空白 profile
hermes profile create research --clone    # 复制当前 config / SOUL / .env
hermes profile create writing --clone-all # 全量快照（含记忆 / 技能）
hermes profile use coder                  # 设为默认（粘性生效）
coder chat                                # 直接以该 profile 开聊（自动生成别名）
hermes -p coder chat                      # 或显式指定
hermes profile list | show | rename | delete
hermes profile export coder               # 打包 tar.gz 用于迁移
hermes profile import coder.tar.gz
```

官方推荐的典型组合：`coder`（技术/简洁）、`personal`（日常/友好）、`research`（细致/谨慎）、`writing`（文档创作），每个 profile 配一份契合的 SOUL.md [^c10-4]。

**v0.19 起还能做 profile 级消息路由**：一个 gateway、一个 bot token，把不同 guild/频道/线程路由到不同 profile，彼此 config/技能/记忆/密钥完全隔离——例如同一个 bot 同时服务 `work` 与 `personal` 两套身份 [^c10-2]。

> [!tip] 大白话
> 把 Profiles 想成"同一套软件开多个用户账号"：每个账号有自己的桌面（配置）、钥匙串（密钥）、人设（SOUL.md）和聊天记录（记忆）。想切就切，互不串台；想搬家就 `export` 打个包带走。

## Bot Mode（v0.20.3+）：把 Profiles 变成能协作的 Bot

Bot Mode 从桌面版 v0.20.3 起默认开启：把 Profiles 升级成一张**命名 Bot 花名册**——每个 bot 可设头像、pin 模型、启用技能、配独立 SOUL.md、挂调度计划 [^c10-3]。Bot 之间通过持久的 **Agent Inbox** 通信，支持 2-6 个 bot 的**多 agent 协作房间**，并可跨 bot `@mention` 交接任务：

```bash
hermes -p <bot> chat -c "Agent Inbox"     # 以某 bot 身份进 Inbox 频道协作
```

> [!tip] 大白话
> 把 Bot Mode 想成"给每个分身起名字、发工牌、组项目群"：以前的 Profiles 是互不认识的同事，Bot Mode 让它们能拉群、@人、交接活。

## 本章小结

- `SOUL.md` 是全局人格：system prompt slot #1、原样注入、替换默认身份；只读 `~/.hermes/SOUL.md`，永不覆盖、新会话生效、注入前过扫描。
- SOUL.md 管"处处适用的人格"，AGENTS.md 管"单项目约定"；官方给 4 套人格模板，`/personality` 做临时切换。
- Profiles 是完全隔离的实例：`hermes profile create/use/export/import` 等；v0.19 起支持一个 gateway 按频道路由到不同 profile。
- Bot Mode（v0.20.3+）把 Profiles 变成命名 bot 花名册：头像、模型 pin、SOUL、调度；Agent Inbox + 2-6 bot 协作房间，`@mention` 交接。

下一章是附录：常用命令速查表，把全书高频命令收拢成一张可随时查阅的表。

[^c10-1]: 官方 SOUL.md 指南：https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/use-soul-with-hermes.md
[^c10-2]: Hermes Agent v0.19.0（Quicksilver）发布说明：https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.20
[^c10-3]: Hermes Agent v0.20.x 发布说明（Bot Mode、桌面工作台、A2A、webhook）：https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.27
[^c10-4]: 掘金：Hermes Profiles 多 Agent 配置指南 https://juejin.cn/post/7631497675088740387
