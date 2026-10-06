# 探测原始记录 08：文档化程度与版本门槛

> **性质**：原始证据记录，**不是**阶段 2 的交付物 `02_deep_research.md`，不推进任何阶段状态。
> **来源**：P2 精读子代理 B「docs and version gates」，检索日期 2026-09-18。
> **快照基准**：`NousResearch/hermes-agent` main HEAD `64ea66b03d44ead9ffea48161132e5deca5d255a`（2026-09-17T05:12:02Z）；HA 侧为 docs/博客线上当前版本。
> **本记录解决了 P1 遗留缺口 4、5、6、7**，并给出两处「文档与实现不一致」的源码级证据。
> **引用纪律**：`H-*` / `HA-*` 是本子代理的**局部编号**，与 `01_explore_result.md` 的 `HAS-/HMS-/COM-` 体系不同源。`02_deep_research.md` 会给出统一映射；本文件内引用请只用本文件编号。

---

## 一、来源记录表

| ID | 标题 | URL | 档位 | 发布/更新 | 锚点 | 主张 | 检索日期 |
|---|---|---|---|---|---|---|---|
| H-01 | Creating Skills | `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/developer-guide/creating-skills.md` | 官方文档（仓库内源文件） | 最后提交 2026-06-11T17:23:27Z | `## SKILL.md Format`、`### Conditional Skill Activation`、`### Credential File Requirements`、`## Blueprints` | **路径更正**：该文件**不在** `website/docs/user-guide/features/` 下，上一轮给的路径在仓库中不存在，`user-guide/features/creating-skills` 在站点上返回 GitHub Pages 404。实际路径为 `website/docs/developer-guide/creating-skills.md`（20113 字节）。frontmatter 逐字清单见第二节。 | 2026-09-18 |
| H-02 | Skills System | `.../website/docs/user-guide/features/skills.md` | 官方文档（仓库内源文件） | 最后提交 2026-09-17T06:06:56Z | `## Progressive Disclosure`、`## SKILL.md Format`、`## Skill Directory Structure` | L0/L1/L2 原文：`Level 0: skills_list()  → [{name, description, category}, ...]   (~3k tokens)` / `Level 1: skill_view(name)  → Full content + metadata` / `Level 2: skill_view(name, path)  → Specific reference file`；`The agent only loads the full skill content when it actually needs it.` | 2026-09-18 |
| H-03 | Cron | `.../website/docs/user-guide/features/cron.md` | 官方文档（仓库内源文件） | 最后提交 2026-09-17T05:04:09Z | `## Delivery options` | 全文 67495 字节中出现 `homeassistant` **仅 1 次**，即投递目标表一行：`| "homeassistant" | Home Assistant | |`——**Example 列为空**。全文无 `HASS_TOKEN`/`HASS_URL`、无向 HA 投递的端到端示例。 | 2026-09-18 |
| H-04 | homeassistant adapter | `.../plugins/platforms/homeassistant/adapter.py` | 一手源码 | 最后提交 2026-09-13T04:13:21Z | L268 `send()`、L311 `_standalone_send()`、L350 `register()` | 两条分支确证，条件见第三节。`send()` docstring 原文：`"""Send a notification via HA REST API (persistent_notification.create).` / `REST rather than the WebSocket, to avoid racing the listener loop that reads from the same WS connection.` | 2026-09-18 |
| H-05 | homeassistant plugin.yaml | `.../plugins/platforms/homeassistant/plugin.yaml` | 一手源码 | 最后提交 2026-05-26T08:36:33Z | `description:` | description 原文：`Outbound messages are delivered as HA persistent notifications via the REST API. Out-of-process cron delivery via the ``notify.notify`` service is also supported.`——**只说明有两条路，未给触发条件**。 | 2026-09-18 |
| H-06 | Home Assistant Integration（Hermes 侧） | `.../website/docs/user-guide/messaging/homeassistant.md` | 官方文档（仓库内源文件） | 最后提交 2026-06-18T14:34:59Z | `### Agent Responses`、`### Connection Management` | 原文：`Outbound messages from the agent are delivered as **Home Assistant persistent notifications** (via `persistent_notification.create`). These appear in the HA notification panel with the title "Hermes Agent".` 及 `**REST API** for outbound notifications (separate session to avoid WebSocket conflicts)`。**该页通篇不提 cron / `_standalone_send` / `notify.notify`**。 | 2026-09-18 |
| H-07 | cron/scheduler_delivery.py | `.../cron/scheduler_delivery.py` | 一手源码 | 最后提交 2026-09-16T19:19:51Z | L1759 `_deliver_result` docstring、L1538 `_standalone_send` | `_deliver_result` docstring 原文：`With ``adapters``/``loop`` (gateway running) the live adapter is tried first (E2EE rooms can't use the standalone HTTP path), then standalone fallback.` 这是分支条件的**唯一权威表述**。 | 2026-09-18 |
| H-08 | gateway/platform_registry.py | `.../gateway/platform_registry.py` | 一手源码 | — | L96–L101 | 字段声明原文：`standalone_sender_fn: Optional[Callable[..., Awaitable[dict]]] = None`，注释 `prefer standalone_sender_fn when the standard send contract suffices.` | 2026-09-18 |
| HA-01 | Persistent Notification | `https://www.home-assistant.io/integrations/persistent_notification/` | 官方文档 | 页面无日期 | 首段、`## Use as a notifier` | 原文：`can be used to show a notification on the frontend that has to be dismissed by the user.`；动作表 `Create notification (persistent_notification.create) Creates a persistent notification in the Home Assistant frontend.`；`It is available as notify.persistent_notification.` | 2026-09-18 |
| HA-02 | Notifications | `https://www.home-assistant.io/integrations/notify/` | 官方文档 | 页面无日期 | `## List of actions` 末段 | 三个动作语义原文：`**Send a notification** (notify.notify): shorthand for the first notify action Home Assistant can find. The destination is therefore not explicitly selected and the message might not be sent where you expect. Choose a specific action or notify entity when the destination matters.` | 2026-09-18 |
| HA-03 | Building the AI-powered local smart home | `https://www.home-assistant.io/blog/2025/09/11/ai-in-home-assistant/` | 官方博客 | 2025-09-11 | `## Supercharging voice control with AI`、`## AI-powered suggestions` | 两条待核对原句确证存在于该文。见第五节逐字引用。**注意：该文未标注任何版本号**。 | 2026-09-18 |
| HA-04 | 2025.7: That's the question | `https://www.home-assistant.io/blog/2025/07/02/release-20257/` | 官方 release notes | 2025-07-02 | `## Let Assist ask the questions!` | 原文：`With this release, we're taking a big step forward: meet the new Ask Question action.` 及 `Finally, your voice assistant can take the initiative and ask _you_ what your smart home should do. No more waiting for wake words, your assistant can start the conversation when it makes sense.` 示例动作 `assist_satellite.ask_question`。 | 2026-09-18 |
| HA-05 | 2025.8 release notes | `https://www.home-assistant.io/blog/2025/08/06/release-20258/` | 官方 release notes | 2025-08-06 | `### Work faster with Suggest with AI buttons` | 原文：`This button is not visible by default and will only appear if you enable it in the "AI suggestions" settings. For this release, the button has been added to the save dialog for automations and scripts.` | 2026-09-18 |

已落地文件：`sources/` 下 `raw-creating-skills.md`、`raw-skills.md`、`raw-cron.md`、`raw-ha-adapter.py`、`raw-ha-messaging.md`、`ha-blog-2025-09-11-ai-in-home-assistant.md`、`ha-pn/01_www_home-assistant_io.md`、`relnotes/2025{07,08,09,10,11}/01_www_home-assistant_io.md`。

---

## 二、待确认项 1（原缺口 7）：SKILL.md frontmatter 逐字清单

H-01 L46–L78 的 frontmatter 代码块**逐字**如下（注释与缩进原样保留）：

```markdown
---
name: my-skill
description: Brief description (shown in skill search results)
version: 1.0.0
author: Your Name
license: MIT
platforms: [macos, linux]          # Optional — restrict to specific OS platforms
                                   #   Valid: macos, linux, windows
                                   #   Omit to load on all platforms (default)
metadata:
  hermes:
    tags: [Category, Subcategory, Keywords]
    related_skills: [other-skill-name]
    requires_toolsets: [web]            # Optional — only show when these toolsets are active
    requires_tools: [web_search]        # Optional — only show when these tools are available
    fallback_for_toolsets: [browser]    # Optional — hide when these toolsets are active
    fallback_for_tools: [browser_navigate]  # Optional — hide when these tools exist
    config:                              # Optional — config.yaml settings the skill needs
      - key: my.setting
        description: "What this setting controls"
        default: "sensible-default"
        prompt: "Display prompt for setup"
    blueprint:                              # Optional — marks this skill a runnable automation
      schedule: "0 9 * * *"              #   cron expr / "every 2h" / ISO timestamp
      deliver: origin                    #   optional (default origin)
      prompt: "Task instruction for each run"  # optional
      no_agent: false                    # optional
required_environment_variables:          # Optional — env vars the skill needs
  - name: MY_API_KEY
    prompt: "Enter your API key"
    help: "Get one at https://example.com"
    required_for: "API access"
---
```

**上一轮摘要的四处需修正／确认**（均回原文核实）：

1. `related_skills` — 存在，但**不是顶层字段**，缩进为 `metadata.hermes.related_skills`。且在 H-02 中 `related_skills` 出现 **0 次**，仅 H-01 有。
2. `requires_tools` — 存在，同样在 `metadata.hermes` 下；但上一轮漏了配套的 `requires_toolsets`、`fallback_for_toolsets`、`fallback_for_tools` 三个同级字段。
3. `blueprint.schedule` — 存在，父块为 `metadata.hermes.blueprint`；同级兄弟字段为 `deliver`（注释 `optional (default origin)`）、`prompt`、`no_agent`。
4. `required_credential_files` — 存在，但**不在上述 frontmatter 示例块里**；它只在 H-01 L244 的独立小节 `### Credential File Requirements (OAuth tokens, etc.)` 给出：条目支持 `path`（required，"file path relative to `~/.hermes/`"）与 `description`（optional）。

**正文规范**（H-01）：标题下推荐小节为 `## When to Use` / `## Quick Reference` / `## Procedure` / `## Pitfalls` / `## Verification`。模板 token：`${HERMES_SKILL_DIR}`、`${HERMES_SESSION_ID}`，可用 `skills.template_vars: false` 全局关闭；inline shell `` !`cmd` `` 默认关闭，需 `skills.inline_shell: true`（附 `inline_shell_timeout: 10`，输出上限 4000 字符）。媒体转附件用字面指令 `[[as_document]]`。遗留兼容：`Legacy prerequisites.env_vars remains supported as a backward-compatible alias.`

**交叉核对 H-02 发现的不一致（文档漂移）**：

- H-02 的 `## SKILL.md Format` 块**只列** `name`/`description`/`version`/`platforms`/`metadata.hermes.{tags, category, fallback_for_toolsets, requires_toolsets, config}`，**缺** `author`、`license`、`related_skills`、`requires_tools`、`fallback_for_tools`、`blueprint`、`required_environment_variables`、`required_credential_files`。
- 反向缺口：H-02 示例含 `category: devops`，**H-01 示例没有** `category`；而 H-02 的 L0 定义 `skills_list() → [{name, description, category}, ...]` 说明 `category` 是索引层实字段。
- 两文件的更新时间差 3 个多月（H-01 = 2026-06-11，H-02 = 2026-09-17），H-01 明显滞后。
- 目录树两版也不一致：H-01 的 `## Skill Directory Structure` 树（`skills/<category>/<skill>/{SKILL.md,scripts/,references/}`）是**仓库内 bundled 布局**；H-02 的树（L354 起）是**运行时布局** `~/.hermes/skills/`，含 `references/ templates/ scripts/ examples/ assets/` 五类子目录与 `.hub/{lock.json,quarantine,audit.log}`、`.bundled_manifest`。H-02 另文说明外部目录解析顺序 `project → local (~/.hermes/skills/) → external_dirs`。L0/L1/L2 只在 H-02 有，H-01 无。

---

## 三、待确认项 2（原缺口 4）：两条出站分支的确切条件

**源码事实**（H-04）：

- `send()`（L268）→ `POST {hass_url}/api/services/persistent_notification/create`，payload `{"title": "Hermes Agent", "message": content[:self.MAX_MESSAGE_LENGTH]}`；成功判据 `resp.status < 300`。选择理由写在 docstring：`REST rather than the WebSocket, to avoid racing the listener loop that reads from the same WS connection.`
- `_standalone_send()`（L311）→ `POST {hass_url}/api/services/notify/notify`，payload `{"message": message, "target": chat_id}`；成功判据 `resp.status not in {200, 201}`。docstring 原文：`"""Send via the HA ``notify.notify`` service without a live gateway adapter.` / `Token: ``pconfig.token`` then ``HASS_TOKEN``; URL: ``pconfig.extra["url"]`` then ``HASS_URL``.` / ``thread_id``/``media_files``/``force_document`` are signature parity only (HA has no threads/attachments).`
- 注册处 L350–L351 注释：`standalone_sender_fn=_standalone_send,  # out-of-process cron delivery via notify.notify`

**分支条件**（H-07，唯一权威表述）：调度器 `_deliver_result(job, content, adapters=None, loop=None, ...)`——**有 `adapters`/`loop`（即 gateway 在跑）时先走 live adapter，失败再退到 standalone**；docstring 并注明 `(E2EE rooms can't use the standalone HTTP path)`。H-07 另给出第三种情形：detached worker 场景下 `_HERMES_CRON_EXTERNAL_WORKER` 环境变量命中且 `adapters is None` 时，投递被交给 `cron.delivery_queue.enqueue_and_wait` 持久队列，由当前/替补 gateway 用 live adapter 完成。

**结论**：走哪条不是由消息内容或 HA 配置决定，而由 **cron 执行进程里有没有活的 gateway adapter 对象**决定——在 gateway 进程内执行 → `persistent_notification/create`；脱离 gateway 单独执行（`adapters is None`，如 CLI 侧 tick / detached worker 直发）→ `notify/notify`。

**「是否文档化了该分支」的核查结果**：

- HA 官方两页（HA-01、HA-02）**不可能**也不必描述 Hermes 的内部分支，它们只定义两个 service 的语义。
- Hermes 侧 `website/docs/user-guide/messaging/homeassistant.md`（H-06）**只写了 `persistent_notification.create` 一条路**，明确写 `Outbound messages from the agent are delivered as Home Assistant persistent notifications`，全文无 `notify.notify`／standalone 字样。→ 按该页实现预期，会在 out-of-process cron 场景下得到与文档不一致的投递路径。
- Hermes 侧 cron 页（H-03）全文不含 HA 特例。
- **唯一提到两条路并存的是 `plugin.yaml` 的 description（H-05）**，但它只写 `Out-of-process cron delivery via the ``notify.notify`` service is also supported.`，**未定义 "out-of-process" 的判定条件**。
- 因此：**分支的存在在 plugin.yaml 有半句话，分支的触发条件只存在于源码（H-07 docstring + H-04 注释），任何面向用户的文档页都没有写清。**

**HA 侧对 `notify.notify` 的语义警告（HA-02 原文，值得原样引用）**：`shorthand for the first notify action Home Assistant can find. The destination is therefore not explicitly selected and the message might not be sent where you expect.` 即 `_standalone_send()` 依赖的正是 HA 官方标注为「目标不确定、不建议在意外投递位置时使用」的那个动作；两条分支在 HA 语义上并不同质。

---

## 四、待确认项 3（原缺口 5）：cron→HA 端到端示例

**核查结论：官方 cron 页没有给出向 Home Assistant 投递定时结果的完整示例。**

证据：对 H-03 全文 67495 字节执行 `grep -n -i "hass|Home Assistant|HASS_TOKEN|HASS_URL"`，命中 **1 行**：

```
525:| `"homeassistant"` | Home Assistant | |
```

该行位于 `## Delivery options` 表内，表头为 `| Option | Description | Example |`——**Example 列对 homeassistant 是空的**，而相邻行如 `"telegram"` 给出 `Uses TELEGRAM_HOME_CHANNEL`、`"telegram:123456"` 给出 `Specific Telegram chat by ID`、`"local"` 给出 ``Save to local files only (`~/.hermes/cron/output/`)``。cron 页全文无 `HASS_*` 环境变量、无配置片段、无 `deliver: homeassistant` 的 job 创建示例。

同时确认另一处易混淆项：cron 页 L606 的小节 `### Push notifications (cron.delivery.notify)` 讲的是 `cron: delivery: notify: false` 这个**推送旗标**，与 `notify.notify` service 无关，不构成端到端示例。

**不替它补例子。** 可确认的补充事实仅供上游判断：`cron/scheduler_delivery.py` L31 的 `_KNOWN_DELIVERY_PLATFORMS` frozenset 逐字包含 `"homeassistant"`，与文档表一致；即目标名合法、代码支持，但文档层止于一行表项。

---

## 五、待确认项 4（原缺口 6）：版本门槛

HA-03 博客（2025-09-11）原句（逐字，两句均已回原文核对）：

- (a) 位于 `## Supercharging voice control with AI`：`We have taken this even further than other voice assistants, as you can now have Home Assistant initiate conversations. For example, you could set up an automation that detects when the garage door is open and asks if you'd like to close it`
- (b) 位于 `## AI-powered suggestions`：`When saving an automation or script, users can now leverage the new Suggest button: When clicked, it will send your automation configuration along with the titles of your existing automations and labels to AI to suggest a name, description, category, and labels for your new automation.`

**逐版比对结果**：

| 能力 | 落地版本 | 首发日期 | 原文出处 | 逐字引用 |
|---|---|---|---|---|
| (a) HA 主动发起对话 | **Home Assistant 2025.7** | 2025-07-02 | HA-04 标题 `2025.7: That's the question`，小节 `## Let Assist ask the questions!` | `With this release, we're taking a big step forward: meet the new Ask Question action.` / `Finally, your voice assistant can take the initiative and ask _you_ what your smart home should do. No more waiting for wake words, your assistant can start the conversation when it makes sense.` |
| (b) 自动化编辑器 Suggest 按钮 | **Home Assistant 2025.8** | 2025-08-06 | HA-05 小节 `### Work faster with Suggest with AI buttons` | `This button is not visible by default and will only appear if you enable it in the "AI suggestions" settings. For this release, the button has been added to the save dialog for automations and scripts.` |

**注：博客自身对 (b) 给出了版本指向**——HA-03 该段首句原文 `[Last month](https://www.home-assistant.io/blog/2025/08/06/release-20258/), Home Assistant launched a new opt-in feature to leverage the power of AI when automating with Home Assistant.`，其链接即 2025.8 release notes，与逐版比对一致。博客对 (a) **未给出任何版本号或链接**——这正是「文档没写清」的原始来源。

**排除项**：2025.9（2025-09-03）、2025.10（2025-10-01）、2025.11（2025-11-05）三份 release notes 中检索 `initiate`/`ask_question`/`Suggest button`/`AI suggest` **均无命中**，两项能力均不在这些版本首发。2025.7 原文还含 `assist_satellite.ask_question` 动作与小节 `## Let Assist ask the questions!` 的 YAML 示例（`preannounce`、`question`、`answers[].id`、`answers[].sentences`）。

---

## 矛盾与存疑

1. **同一 frontmatter 两套字段表**：H-01（2026-06-11）与 H-02（2026-09-17）列出的 SKILL.md 字段集互相不覆盖，且各有多余项（H-01 有 `author`/`license`/`blueprint`/`related_skills`/`requires_tools`/`fallback_for_tools`/`required_*`；H-02 有 `category`）。**哪一套是权威未经声明**——两页都无「本表为准」的措辞，也未见仓库内 frontmatter schema 文件。按更新时间 H-02 较新，但 `category` 与 `related_skills` 的取舍无法从文档判定。
2. **`related_skills` 疑似悬空字段**：仅 H-01 出现 1 次，H-02 出现 0 次，H-01 未说明其消费方（是否影响 `skills_list()` 输出、是否参与检索排序均未写）。存疑为文档残留。
3. **`blueprint.schedule` 的注释列出三种格式** `cron expr / "every 2h" / ISO timestamp`，但 H-01 与 H-02 均未给出后两种格式的解析规则或示例；cron 页（H-03）是否接受同三种格式未交叉核对。
4. **出站分支的文档与实现不一致**：H-06 以 `Outbound messages from the agent are delivered as Home Assistant persistent notifications` 作无条件陈述，而源码（H-04/H-07）在 out-of-process 路径改用 `notify.notify`。按 H-06 字面理解会得出错误预期。H-05 虽提到两条路，但表述为 `is also supported`，读起来像可选增强而非环境决定的自动切换。
5. **`notify.notify` 的目标不确定性**：HA-02 官方明确警告该动作的目标「might not be sent where you expect」，而 `_standalone_send()` 只传 `{"message", "target": chat_id}`，未见对 `target` 的取值来源作 HA 侧校验。投递是否真落到预期位置，源码与文档均未保证。
6. **HA-03 无版本标注**：博客通篇不含版本号，两项能力的版本必须靠 release notes 反查；博客 (a) 段甚至给出的是 blueprint 链接（`/blueprints/blog/2025-07/ask_yes_no_question.yaml`）而非功能文档链接，容易误读为「靠 blueprint 实现」。
7. **HA 文档页无发布/更新日期**：HA-01、HA-02 页面正文与 frontmatter（crawler 抓取结果）均无 `updated` 字段，无法给出「发布或更新日期」，只能记「页面无日期」。此非本次疏漏，是站点本身不暴露。

## 未解决项

1. **SKILL.md frontmatter 的机器可读 schema 未定位**：未在 `NousResearch/hermes-agent` 树中找到定义/校验 frontmatter 字段的 schema 或 loader 源码（已排查路径关键词 `skill` × `schema|valid|loader|parse|front`，仅命中无关的第三方 skill 脚本）。因此「哪些字段真正被解析」仍只能靠文档互证，无法用源码定案。H-01 提到的 `skills/productivity/google-workspace/SKILL.md`（"a complete example using both"）**未取回核对**。
2. **`related_skills` 的消费方未找到**，其对 `skills_list()` / L0 索引的实际影响未知。
3. **`blueprint.schedule` 的 `"every 2h"` 与 ISO timestamp 两种写法**未找到语法定义与可运行示例。
4. **`_standalone_send()` 的调用方仍未直接读到**：本次是从 `cron/scheduler_delivery.py` 的 docstring 与 lane 命名（`_deliver_standalone`、`_standalone_send`）推断条件，`_deliver_standalone` 函数体内如何从 registry 取出 `standalone_sender_fn` 并调用，未逐行确认（该文件 94267 字节，仅定点读了 L1–L40、L1750–L1800，及 grep 命中行）。
5. **HA 侧 2025.7 之前是否有更早的「主动对话」雏形**（如 `conversation.process` 或 Voice Chapter 10 博客 2025-06-25 所述内容）未展开；本次只定案 HA-03 原句所指能力＝2025.7 `assist_satellite.ask_question`。
6. **HA 2025.8 release notes 中 Suggest 按钮的「AI suggestions 设置」确切路径**未逐字取回（该页只写 `enable it in the "AI suggestions" settings`，HA-03 写的是 `AI Task preferences pane` under `System -> General`，两处措辞不同，未定论是否为同一入口）。
7. **`cron.md` 的 Example 列空缺是否为作者有意留白**（对比其他平台均有值）无法判定，需上游决定是否作为缺文档证据引用。

**操作提示（供后续采集复用）**：`crawl.sh` 按「序号_主机名」命名输出文件，跨批次对同一主机抓取会**静默覆盖**前一批同名文件（本次 HA 的 `01_www_home-assistant_io.md` 被覆盖一次）。建议每次抓取使用独立 `--output-dir`。另：抓取不存在的 URL 时 crawler 会以 HTTP 200 返回 GitHub Pages 的 404 页面并仅 494 字符，需按体积/标题校验而非退出码判断成功。

---

## 本记录对 P1 遗留缺口的结案状态

| 原缺口 | 状态 | 依据 |
|---|---|---|
| 4 `notify.notify` vs `persistent_notification` 分支条件 | **结案** | 由 gateway adapter 是否存在决定；源码 docstring 为唯一权威表述（H-07 + H-04）；用户文档未写清（H-06 反而误导） |
| 5 cron→HA 端到端示例 | **结案（否定）** | 官方 cron 页无此示例，Example 列空缺（H-03）；**不补编** |
| 6 主动对话 / Suggest 版本门槛 | **结案** | 2025.7 / 2025.8（HA-04 / HA-05），并排除了 2025.9–11 |
| 7 `creating-skills.md` 全文 | **结案** | 路径更正为 `developer-guide/creating-skills.md`；frontmatter 逐字清单已取；并发现与 `skills.md` 的字段表互相不覆盖 |
