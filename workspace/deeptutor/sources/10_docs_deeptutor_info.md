---
url: "https://docs.deeptutor.info/zh-cn/explore/subagents/"
title: "我的智能体 | DeepTutor"
scraped_at: 2026-09-01T15:28:58+00:00
---

[跳转到内容](https://docs.deeptutor.info/zh-cn/explore/subagents/#_top)
# 我的智能体
**My Agents** （我的智能体）把其他智能体变成 DeepTutor 的上下文。它做两件不同的事：让你在一轮聊天里**实时咨询一个活的智能体** （本机九种受支持的 harness 之一，或你的某个伙伴），以及把 **Claude Code / Codex 历史对话导入** 为有名字、可搜索、可续聊的智能体。
## 它在哪里
[Section titled “它在哪里”](https://docs.deeptutor.info/zh-cn/explore/subagents/#%E5%AE%83%E5%9C%A8%E5%93%AA%E9%87%8C)
点击左侧栏的 **My Agents** （我的智能体）。在聊天里你也有两条捷径触达活的智能体：输入框工具栏上的 **Agent 胶囊** （机器人图标），或在消息框里输入 。
页面分为两节，正好对应这两个概念。
## 连接的智能体——咨询一个活的智能体
[Section titled “连接的智能体——咨询一个活的智能体”](https://docs.deeptutor.info/zh-cn/explore/subagents/#%E8%BF%9E%E6%8E%A5%E7%9A%84%E6%99%BA%E8%83%BD%E4%BD%93%E5%92%A8%E8%AF%A2%E4%B8%80%E4%B8%AA%E6%B4%BB%E7%9A%84%E6%99%BA%E8%83%BD%E4%BD%93)
**连接的智能体** （connected agent）是 DeepTutor 能实时对话的真实智能体。点击 **Connect agent** ，从下面三种里选一个：
  * 本机的一个 agent harness——**Claude Code** 、**Codex** 、**Antigravity CLI** 、**Kimi CLI** 、**opencode** 、**MiMo Code** 、**Hermes Agent** 、**OpenClaw** 或 **DeepSeek Harness** ，或
  * 你的某个**伙伴** （Partner）。


咨询一个连接的智能体时，DeepTutor 不是把对话记录粘进来——它真的 _运行_ 那个智能体并把它的工作流式回传。在底层，连接的智能体是第三类上下文来源，拥有一项独有能力：聊天循环里的 `consult_subagent` 工具会多轮驱动该智能体，并在活动面板里实时展示它的完整运行过程。
### 在聊天里咨询
[Section titled “在聊天里咨询”](https://docs.deeptutor.info/zh-cn/explore/subagents/#%E5%9C%A8%E8%81%8A%E5%A4%A9%E9%87%8C%E5%92%A8%E8%AF%A2)
用 **Agent 胶囊** 选中智能体，然后设置 **Max rounds DeepTutor may ask** （DeepTutor 最多可追问的轮数）——也就是这次咨询里来回轮次的上限。
或者直接输入 ，为单轮就地 @ 一个智能体。
### 一次实时咨询长什么样
[Section titled “一次实时咨询长什么样”](https://docs.deeptutor.info/zh-cn/explore/subagents/#%E4%B8%80%E6%AC%A1%E5%AE%9E%E6%97%B6%E5%92%A8%E8%AF%A2%E9%95%BF%E4%BB%80%E4%B9%88%E6%A0%B7)
咨询一个 **Claude Code** 智能体时，它会在自己的工作目录里运行——读取文件、grep、对着真实仓库推理。它的工具调用会流式进入活动面板，同时 DeepTutor 把结论收拢进你的答复。
咨询一个**伙伴** 时，DeepTutor 把问题送进那个伙伴自己的会话——于是伙伴会用它的灵魂（soul）、它的资料库、它私有的记忆工具（`partner_search`、`partner_read`）以及技能（`read_skill`）来作答。一个聊天线程会绑定到一个伙伴会话，因此追问会延续同一段对话。
## 导入的对话——来自你历史记录的智能体
[Section titled “导入的对话——来自你历史记录的智能体”](https://docs.deeptutor.info/zh-cn/explore/subagents/#%E5%AF%BC%E5%85%A5%E7%9A%84%E5%AF%B9%E8%AF%9D%E6%9D%A5%E8%87%AA%E4%BD%A0%E5%8E%86%E5%8F%B2%E8%AE%B0%E5%BD%95%E7%9A%84%E6%99%BA%E8%83%BD%E4%BD%93)
页面的下半部分会导入你已有的 **Claude Code 与 Codex 对话** ，并把每个来源呈现为一个**有名字的智能体** ，可搜索、可打开、可继续聊，或在聊天里引用。
点击 **Add agent** 导入历史。先给智能体起个名字，然后**选择要导入哪些天** ——之后刷新会重新同步这些天，并拉进当天的新对话。这种「按天选择」是刻意为之：你能精确地决定终端历史里哪些片段成为 DeepTutor 的上下文。
导入的智能体会显示来源、对话数量与上次同步时间。在这里你可以：
  * **打开一段对话** ，在 DeepTutor 里继续聊。
  * **刷新** 某个智能体，拉进新增天数的对话。
  * 在任意一轮聊天里，通过 **`+`→ My Agents** **引用** 一段导入的对话——DeepTutor 会把它当作第三方对话记录来读（它仍是「他们的」对话，DeepTutor 不会以第一人称代入）。


## 两者的区别
[Section titled “两者的区别”](https://docs.deeptutor.info/zh-cn/explore/subagents/#%E4%B8%A4%E8%80%85%E7%9A%84%E5%8C%BA%E5%88%AB)  
| 连接的智能体  | 导入的对话  |  
| --- | --- |  
| **是什么**  | DeepTutor 实时运行并对话的活智能体  | 作为命名智能体引入的只读历史  |  
| 九种本地 harness 之一（Claude Code / Codex / Antigravity / Kimi / opencode / MiMo / Hermes / OpenClaw / DeepSeek Harness），或某个伙伴  | 过去的 Claude Code / Codex 会话  |  
| **在聊天里**  | 用 Agent 胶囊或 `@` 咨询；运行实时流式  | 用 `+` → My Agents 引用，或打开续聊  |  
| **新鲜度**  | 实时，每次咨询都是  | 快照；用 **Refresh** 重新同步所选天数  |  
## 另见
[Section titled “另见”](https://docs.deeptutor.info/zh-cn/explore/subagents/#%E5%8F%A6%E8%A7%81)
  * [主页](https://docs.deeptutor.info/zh-cn/explore/chat-workspace/)——在这里咨询与引用智能体
  * [伙伴](https://docs.deeptutor.info/zh-cn/explore/partners/)——把一个伙伴连接成可咨询的智能体
  * [记忆](https://docs.deeptutor.info/zh-cn/explore/memory/)——导入的上下文如何与 DeepTutor 自己的声音保持区隔


