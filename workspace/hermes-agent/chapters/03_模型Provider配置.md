# 模型 Provider 配置：打破模型锁定

用 agent 的人最烦被一家模型绑死：换供应商就得重配一遍。Hermes 把模型层做成了可插拔的——配置只认两个文件，Provider 全家桶覆盖云端、本地与自建端点，任何 OpenAI-compatible 服务都能接入。本章讲清配置唯一来源、六类 Provider 的接法，以及 WSL2 下连 Windows 宿主模型服务的网络细节。

## 配置唯一来源：config.yaml + .env，密钥永不混进配置

Hermes 的模型配置只有一个权威位置：`~/.hermes/config.yaml`。三个文件分工明确：`config.yaml` 只写"模型在哪、怎么连"（模型名、provider、base_url）；API key 一律放 `~/.hermes/.env`，密钥不会暴露给模型；OAuth 登录凭据由程序自动写入 `~/.hermes/auth.json`，通常无需手工编辑。旧的环境变量 `LLM_MODEL` 已被移除，不要再依赖它（来源 S5）。

```yaml
# ~/.hermes/config.yaml（最小示意，键名以 hermes doctor 输出为准）
model: my-default-model   # 默认模型名
provider: nous-portal     # 走哪个 provider
base_url: ""              # custom / 直连端点时填
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
| Nous Portal | OAuth 登录，推荐；覆盖 300+ 模型 + Tool Gateway |
| OpenRouter | `.env` 放 `OPENROUTER_API_KEY` |
| OpenAI 直连 | `.env` 放 `OPENAI_API_KEY`，provider 用 `openai-api` |
| Anthropic | 三种认证：Claude Max OAuth / `ANTHROPIC_API_KEY` / `ANTHROPIC_TOKEN`；**Claude Pro 订阅不能走 OAuth** |
| custom | 任意 OpenAI-compatible 端点，配 `base_url` |
| 本地 Ollama | `base_url: http://localhost:11434/v1`，且 `context_length ≥ 64000` |

选型没有对错，只有场景：追求省事选 Nous Portal；已有 OpenAI / OpenRouter 额度直接填 key；隐私敏感或离线场景用本地 Ollama；公司自建网关只要是 OpenAI-compatible 就能当 custom 接进来。注意 Anthropic 的认证分三种，Claude Max 订阅可走 OAuth，Claude Pro 不行，得用 `ANTHROPIC_API_KEY` 或 `ANTHROPIC_TOKEN`。

> [!tip] 大白话
> 把 provider 想成「加油站」：同一套 OpenAI-compatible 格式就像同一种油，可以加中石油、加壳牌、加自家发电机（Ollama）。Hermes 不绑死一家——换油只改配置文件，不换车。

## 会话外向导 vs 会话内切换

两个入口要分清（来源 S5）：会话外运行 `hermes model`，是完整向导，可增删 provider、改默认模型；会话内输入 `/model`，只在"已配置项"之间快速切换，不能新增。换句话说，`hermes model` 是"配管工"（新增、删除、设默认），`/model` 是"换开关"（已装好的水龙头之间切换）。新 provider 配好后，会话内就能立刻用 `/model` 切过去。

## WSL2 访问 Windows 宿主模型服务

在 WSL2 里跑 Hermes、想连 Windows 上运行的 Ollama 等服务时（来源 S5）：

- Win11 22H2+ 推荐开 **mirrored 模式**，网络共享，直接 `localhost` 即可，无需改配置；
- NAT 模式要用**主机 IP**（不是 localhost），且服务必须绑定 `0.0.0.0` 才能被 WSL2 访问，例如启动 Ollama 时设 `OLLAMA_HOST=0.0.0.0:11434`。

```yaml
# ~/.hermes/config.yaml（WSL2 → Windows 宿主 Ollama，NAT 模式）
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
- WSL2 连 Windows 模型服务：mirrored 模式直连 localhost；NAT 模式用主机 IP + 服务绑 0.0.0.0（如 `OLLAMA_HOST`）。

下一章进入 Hermes 最核心的差异化——记忆与学习闭环，看它如何跨会话"用着用着自己变强"。
