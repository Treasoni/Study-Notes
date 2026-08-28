---
title: "模型 Provider 配置：打破模型锁定"
tags:
  - AI学习
  - Agent
  - Hermes
  - 上手实战
created: 2026-08-28
updated: 2026-08-29
status: 已完成
source_project: hermes-agent
---

> [[02-安装与第一跑|⬅ 上一章]] · [[README|📖 返回目录]] · [[04-记忆与学习闭环|下一章 ➡]]

# 模型 Provider 配置：打破模型锁定

用 agent 的人最烦被一家模型绑死：换供应商就得重配一遍。Hermes 把模型层做成了可插拔的——配置只认两个文件，Provider 全家桶覆盖云端、本地与自建端点，任何 OpenAI-compatible 服务都能接入。本章讲清配置唯一来源、六类 Provider 的接法，以及 WSL2 下连 Windows 宿主模型服务的网络细节。

## 配置唯一来源：config.yaml + .env，密钥永不混进配置

Hermes 的模型配置只有一个权威位置：`~/.hermes/config.yaml`。三个文件分工明确：`config.yaml` 只写"模型在哪、怎么连"（模型名、provider、base_url）；API key 一律放 `~/.hermes/.env`，密钥不会暴露给模型；OAuth 登录凭据由程序自动写入 `~/.hermes/auth.json`，通常无需手工编辑。旧的环境变量 `LLM_MODEL` 已被移除，不要再依赖它（来源 S5）。

```yaml
# ~/.hermes/config.yaml（最小示意，键名以 hermes doctor 输出为准）
model:
  default: my-default-model   # 默认模型名
  provider: nous              # 走哪个 provider（Nous Portal 的 ID 是 nous）
  base_url: ""                # custom / 直连端点时填
```

```bash
# ~/.hermes/.env（密钥清单，与 config 分离）
OPENROUTER_API_KEY=sk-or-xxxx
OPENAI_API_KEY=sk-xxxx
ANTHROPIC_API_KEY=sk-ant-xxxx
```

> [!tip] 大白话
> 把 config.yaml 想成「装修图纸」（模型在哪、怎么连），把 .env 想成「保险箱」（只放钥匙）。钥匙从不混进图纸，换机器、同步、备份都只操心这两个文件。

这套"配置与密钥分离"的设计，是后面容器化、远程后端部署安全基线的前提。配置排错从 `hermes doctor` 开始，它会诊断配置与密钥是否齐全（来源 S5）。

## Provider 全家桶：一条命令接六种模型来源

至少要配一个 LLM provider 才能跑。官方推荐首选项是 Nous Portal：一次 OAuth 登录覆盖 300+ 模型，还捆绑了 Tool Gateway，一条龙最省事。其余选择（来源 S5）：

| Provider | 配置要点 |
|---|---|
| Nous Portal | OAuth 登录，推荐；覆盖 300+ 模型 + Tool Gateway；provider 用 `nous` |
| OpenRouter | `.env` 放 `OPENROUTER_API_KEY` |
| OpenAI 直连 | `.env` 放 `OPENAI_API_KEY`，provider 用 `openai-api` |
| Anthropic | 三种认证：Claude Max OAuth / `ANTHROPIC_API_KEY` / `ANTHROPIC_TOKEN`；**Claude Pro 订阅不能走 OAuth** |
| custom | 任意 OpenAI-compatible 端点，配 `base_url` |
| 本地 Ollama | 本质是 `provider: custom` + `base_url: http://localhost:11434/v1`，`context_length ≥ 64000`；需在服务端设 `OLLAMA_CONTEXT_LENGTH`（API 设不了） |

选型没有对错，只有场景：追求省事选 Nous Portal；已有 OpenAI / OpenRouter 额度直接填 key；隐私敏感或离线场景用本地 Ollama；公司自建网关只要是 OpenAI-compatible 就能当 custom 接进来。注意 Anthropic 的认证分三种，Claude Max 订阅可走 OAuth，Claude Pro 不行，得用 `ANTHROPIC_API_KEY` 或 `ANTHROPIC_TOKEN`。

> [!tip] 大白话
> 把 provider 想成「加油站」：同一套 OpenAI-compatible 格式就像同一种油，可以加中石油、加壳牌、加自家发电机（Ollama）。Hermes 不绑死一家——换油只改配置文件，不换车。

## 会话外向导 vs 会话内切换

两个入口要分清（来源 S5）：会话外运行 `hermes model`，是完整向导，可增删 provider、改默认模型；会话内输入 `/model`，只在"已配置项"之间快速切换，不能新增。换句话说，`hermes model` 是"配管工"（新增、删除、设默认），`/model` 是"换开关"（已装好的水龙头之间切换）。新 provider 配好后，会话内就能立刻用 `/model` 切过去。

## 实战：新增一个 Provider（Docker 三步走）

把「加一个新模型」拆成可照做的三步。宿主机 `~/.hermes/` 就是容器里的 `/opt/data/`，以下命令都在宿主机执行。

**第一步：放钥匙到 `.env`**

```bash
echo 'OPENAI_API_KEY=sk-xxxx' >> ~/.hermes/.env   # 以 OpenAI 为例，其余 provider 的 key 变量名见上方「Provider 全家桶」表
```

钥匙只进 `.env`，永远不写进 `config.yaml`。

**第二步：跑向导新增 provider**

```bash
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent model
```

交互式选 provider、填模型名、设默认模型，向导写回 `config.yaml`。这是唯一能「新增」provider 的入口；已配好的项之间切换用会话内 `/model`。

**第三步：验证配置齐全**

```bash
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent doctor
```

`hermes doctor` 同时诊断 config 与密钥是否齐全：缺 key、provider 拼写错都会在这里暴露。

> [!tip] 大白话
> 三步对应三件事：先往保险箱放钥匙（.env），再在图纸上画新水管（`hermes model`），最后请师傅检查全屋水路（`hermes doctor`）。不想跑向导也可以：直接在宿主机改 `~/.hermes/config.yaml` 加 provider 段 + `~/.hermes/.env` 加 key，效果一样，只是容易手滑。

## 实战：中转站 / custom 端点

第三方 API 中转站本质就是一个 OpenAI-compatible 端点，对应上面的 `custom` provider：只要给你 `Base URL`、`API Key`、`模型 ID` 三样就能接。以中转站 `https://api.中转域名.com/v1`、key `sk-xxxx`、模型 `gpt-4o` 为例：

**第一步：放钥匙到 `.env`（用自定义变量名）**

```bash
echo 'ZHONGZHUAN_API_KEY=sk-xxxx' >> ~/.hermes/.env
```

> ⚠️ 别把中转站 key 放 `OPENAI_API_KEY`。custom provider 下 Hermes 可能把 `OPENAI_API_KEY` 当占位符发送，结果 401；用自定义名 + 显式引用最稳。

**第二步：config.yaml 配 custom 端点**

```yaml
# ~/.hermes/config.yaml
model:
  api_mode: chat_completions   # 中转站基本都走 chat_completions
  provider: custom
  base_url: https://api.中转域名.com/v1   # 一定要带 /v1
  default: gpt-4o              # 中转站文档给的模型 ID
  context_length: 128000       # 建议手填；Hermes 也能通过 /models 自动探测
  api_key: ${ZHONGZHUAN_API_KEY}
```

（键名以 `hermes doctor` 输出为准。）

**第三步：验证 + 会话内切换**

```bash
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent doctor
```

`hermes doctor` 过了之后，进对话输 `/model` 选 `gpt-4o` 即可。

| 坑 | 说明 |
|---|---|
| `base_url` 漏 `/v1` | 中转站端点通常是 `https://域名/v1`，漏了连不上 |
| `context_length` 不填 | 部分端点/代理不暴露 `/models` 时无法自动探测，建议手填；agent 功能建议 ≥ 64000 |
| key 放 `OPENAI_API_KEY` | 部分版本对 custom provider 不读它，会 401；用 `api_key: ${XXX_API_KEY}` 显式指定 |
| 模型名 | 用中转站文档给的 ID，填错会 404 / model not found |

> [!tip] 大白话
> 中转站相当于「第三方加油站，但也是同一种油」——格式还是 OpenAI-compatible，只是站不归你管。配法和自建 custom 端点完全一样：base_url 填它家地址、key 用自定义变量名、模型名照它招牌点单。

## WSL2 访问 Windows 宿主模型服务

在 WSL2 里跑 Hermes、想连 Windows 上运行的 Ollama 等服务时（来源 S5）：

- Win11 22H2+ 推荐开 **mirrored 模式**，网络共享，直接 `localhost` 即可，无需改配置；
- NAT 模式要用**主机 IP**（不是 localhost），且服务必须绑定 `0.0.0.0` 才能被 WSL2 访问，例如启动 Ollama 时设 `OLLAMA_HOST=0.0.0.0`（端口默认 11434）。

```yaml
# ~/.hermes/config.yaml（WSL2 → Windows 宿主 Ollama，NAT 模式）
model:
  provider: custom
  base_url: http://<主机IP>:11434/v1
  context_length: 64000
```

注意两处 `base_url` 不同：纯 Linux 本机是 `localhost:11434`；WSL2 连 Windows 宿主时要用主机 IP。mirrored 模式省心但要求 Win11 22H2+；NAT 模式通用性更强，代价是多配一步。

> [!tip] 大白话
> 把 WSL2 想成「隔壁房间」：mirrored 模式像打通隔断墙，说 localhost 就能串门；NAT 模式像还得报出整栋楼门牌号（主机 IP），并让服务把门开在 0.0.0.0 才对整栋楼可见。

## 本章小结

- 配置唯一来源是 `~/.hermes/config.yaml` + `~/.hermes/.env`，密钥永不进配置文件；`LLM_MODEL` 已移除。
- Nous Portal OAuth 一条龙最省事；OpenRouter / OpenAI / Anthropic / custom / Ollama 各有接法，Claude Pro 不能走 OAuth。
- 会话外 `hermes model` 管增删与默认，会话内 `/model` 管快速切换。
- 新增 Provider 实操（Docker 三步）：`.env` 放 key → `hermes model` 向导 → `hermes doctor` 验证 → 会话内 `/model` 切换。
- 中转站 / custom 端点：`base_url` 带 `/v1` + 显式 `api_key: ${XXX_API_KEY}` + `context_length` 建议手填；key 别放 `OPENAI_API_KEY`。
- WSL2 连 Windows 模型服务：mirrored 模式直连 localhost；NAT 模式用主机 IP + 服务绑 0.0.0.0（如 `OLLAMA_HOST`）。

下一章进入 Hermes 最核心的差异化——记忆与学习闭环，看它如何跨会话"用着用着自己变强"。
