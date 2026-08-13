# 第六章：自定义 provider 与模型路由

上一章把权限系统调到了自己舒服的基线，这一章解决一个更根本的问题：opencode 到底能跑哪些模型？答案比 Claude Code 开放得多——**任何 OpenAI 兼容端点都能接进来**，这正是"模型与框架解耦"卖点的落地。本章通过一个完整示例，带你自定义 provider、理解两个关键约束，并学会用多模型路由控制成本。

## 自定义 OpenAI 兼容 provider：一个示例看懂

在 Claude Code 里，你要换模型基本被锁死在 Anthropic 生态；opencode 则允许你在 `opencode.json` 的 `provider` 键里声明任意 OpenAI 兼容服务商。下面是一个完整示例，接入 Venice AI 的一个 GLM 模型 [Venice AI opencode 集成文档](https://docs.venice.ai/guides/integrations/opencode)：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "venice/zai-org-glm-5-1",
  "provider": {
    "venice": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Venice AI",
      "options": {
        "baseURL": "https://api.venice.ai/api/v1",
        "apiKey": "{env:VENICE_API_KEY}"
      },
      "models": {
        "zai-org-glm-5-1": { "name": "GLM 5.1" }
      }
    }
  }
}
```

逐行拆解：

- `provider.venice`：provider 的**内部 ID**，你自己起名，全局唯一。
- `npm`：告诉 opencode 用哪个 AI SDK 驱动去对话，接 OpenAI 兼容服务一律填 `@ai-sdk/openai-compatible`。
- `options.baseURL`：该服务商**兼容 OpenAI 的 API 根路径**，必须是官方 v1 端点。
- `options.apiKey`：密钥。优先用 `{env:VAR}` 从环境变量读（比把密钥写死在配置里安全得多）。
- `models`：这个 provider 下可用模型的 map。key 是 `model-id`，`name` 只是展示名。

> [!tip] 大白话
> 把 provider 想成「门禁卡办理处」：`npm` 告诉门禁系统读哪种卡格式，`baseURL` 告诉它刷卡机装在哪栋楼，`apiKey` 是发到你手里的门禁卡。三样齐了，任何长得像 OpenAI 的楼你都能刷卡进去——所以「任意 OpenAI 兼容端点」并不是玄学，只是把这套门禁配置标准化了。

## provider 引用格式：provider-id/model-id

配好之后，所有需要指定模型的地方都用**斜杠拼接**的格式：

```bash
opencode run -m venice/zai-org-glm-5-1 "重构 src/lib"
```

其中 `venice` 是上一步你自己起的 provider ID，`zai-org-glm-5-1` 是 `models` map 里的 key。`/models`（或 `ctrl+x m`）切换模型、`opencode models [provider]` 查看可用模型，输出都是这种 `provider/model` 格式 [opencode CLI 文档](https://opencode.ai/docs/cli)。

**命名冲突要注意**：provider ID 是全局命名空间。你自定义的 ID 不能和内置的 `anthropic`、`openai` 等重名，否则会覆盖内置 provider。

## npm 与 baseURL：两个最容易配错的关键约束

自定义 provider 九成的问题出在这两个字段 [opencode 认证与 provider 排错](https://opencode.ai/docs/config)：

| 字段 | 正确写法 | 配错的后果 |
|------|---------|-----------|
| `npm` | 恒为 `@ai-sdk/openai-compatible`（接兼容端点时） | SDK 与端点不匹配，协议解析失败 |
| `baseURL` | 服务商官方的 v1 兼容端点（如 `.../api/v1`） | endpoint 对不上，404 / 401 |

> [!tip] 大白话
> `baseURL` 就像「导航填的收货地址」——差一个 `/v1` 后缀、多个一级目录，包裹就送不到。`npm` 则像「快递公司」，兼容端点统一走 OpenAI 这家快递，别自己换别的公司。

## 认证备选：/connect 图形化配置

不想手写 `apiKey`？TUI 里输入 `/connect`，选 **Other**，填 provider ID，粘贴密钥即可完成认证。此时凭据写入 `~/.local/share/opencode/auth.json`，你就可以把配置里的 `options.apiKey` 删掉，让 provider 回退到已存的凭据。

> [!warning] 两种写法别双写冲突
> `{env:VAR}` 与 `/connect` 二选一即可。混用时若 env 未导出，会被替换成空串 `""`，而 provider 回退逻辑用的是严格相等 `=== undefined`——空串会**吞掉** auth.json 里已存好的凭据，导致 401（issue [#34388](https://github.com/anomalyco/opencode/issues/34388)）。用 `{env:VAR}` 就保证该变量在启动 opencode 的同一个 shell 里已导出。

## 多模型逐步路由控成本

opencode 支持给不同任务配不同模型，从根上控制 token 成本 [opencode vs Claude Code 实测对比](https://www.builder.io/blog/opencode-vs-claude-code)。核心思路是**把贵的推理留给真正需要它的步骤**：

- **规划（plan）**：用强模型做架构分析，只读不写，一次规划价值最高。
- **批量编辑 / 机械重构**：用便宜的小模型（`small_model`），改完靠测试兜底。
- **分诊（triage）/ 摘要 / 日志分析**：最便宜的快模型，量大也不心疼。

```bash
# 一次性计划任务用便宜模型跑（只读分析，风险低）
opencode run --agent plan -m openai/gpt-4o-mini "审计 src/ 的循环依赖"
```

配合第三章讲过的 `small_model`（轻量任务默认模型）和 `--agent plan`，你可以在不降低主任务质量的前提下，把次要步骤的 token 花费降一个数量级。

> [!tip] 大白话
> 逐步路由就像「装修分工」：画图纸请大师傅（强模型，一次到位），砌墙让普通工人干（便宜模型，活干对就行），搬垃圾找临时工（最便宜）。不是所有活都得让顶配专家做——成本瞬间就下来了。

## 模型不出现的排查要点

配完发现 `/models` 里看不到你的模型？按这个顺序查 [opencode provider 排错](https://opencode.ai/docs/config)：

1. **`models` map 是否注册**：没在 `provider.<id>.models` 里声明的模型不会出现在列表里。
2. **API key 是否在同一个 shell 导出**：`{env:VAR}` 读的是启动 opencode 的进程环境，换个 shell 就丢。
3. **是否在项目目录运行**：只有从项目根（最近的 Git 目录）启动，才会加载项目的 `opencode.json`；在别的目录启动只会读到全局配置。
4. **`baseURL` / `npm` 是否配错**：端点对不上，provider 初始化就失败，模型自然不出现。

## 本章小结

- opencode 通过 `provider` 键接入任意 OpenAI 兼容服务商，`npm` 恒填 `@ai-sdk/openai-compatible`，`baseURL` 必须指向官方 v1 端点。
- 模型统一用 `provider-id/model-id` 引用；自定义 provider ID 不能与内置 provider 重名。
- 认证可用 `{env:VAR}` 或 `/connect` 图形化完成，但两者别混用，避免空串吞掉 auth.json 凭据。
- 用「规划用强模型、批量/分诊用便宜模型」的路由思路，可在不降质的前提下显著控制 token 成本。
- 模型不出现时，按「models map → shell 环境变量 → 项目目录 → 端点配置」四步排查。

下一章进入 MCP 集成，看看怎么把外部工具（文件系统、数据库、各种 API）以标准协议接进 opencode，让 agent 的触手伸得更远。
