---
title: "第四章 首次启动：HAOS 引导 / onboarding / Add-on 安装"
type: chapter
chapter: 4
tags:
  - Home-Assistant
  - 部署
  - onboarding
  - HAOS
  - Add-on
created: 2026-08-05
updated: 2026-08-06
status: 已完成
source_project: ai-smart-home-system
---

# 第四章 首次启动：HAOS 引导 / onboarding / Add-on 安装

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：深度收集 §2（onboarding 自动化 / Add-on）、§7（待实测 #4）
> 前置关联：[[01_系统架构与部署选型|第一章 系统架构与部署选型]]

> [!summary] 本章回答三个问题
> 1. HAOS 开机引导（浏览器访问 `homeassistant.local:8123` 的建账号 / 位置 / 分析）能不能整段脚本化？（能，onboarding API）
> 2. Agent 是怎么靠 Add-on 一键装进 HAOS 的？「5 分钟承诺」的技术边界到底划在哪？
> 3. 什么集成可以「停 HA → 写配置 → 重启」自动化，什么必须人工？（token 类 vs OAuth 类）

第 1、2 章确定了交付形态是「HAOS 为主 + Container 为辅」，第 3 章把它落成预建镜像 / 预刷主机 / 定制盒子。用户把盒子插电开机之后，面对的第一样东西，是 HAOS 的首次启动引导：浏览器打开 `homeassistant.local:8123`，一路建账号、设位置、选分析。对技术人这顺手就能点完，但对「非技术用户」这是第一堵墙——界面是英文、概念陌生、密码没人帮管，一旦卡在这，前面的一键交付就全白做了。本章以 HAOS 为主场景，讲清楚三件事：开机引导如何自动化、Agent 如何靠 Add-on 一键装、以及「5 分钟承诺」到底能承诺到哪一步。

## 4.1 HAOS 首次启动：开机引导与 Supervisor 托管

HAOS 是「专机专用」的官方路径：镜像刷进设备（或直接买预刷盒子）后开机即起，系统由 Supervisor 全权托管。首次启动的浏览器引导，本质上是一连串「创建资源 + 打勾」的动作，正好能映射成 5 个后台调用：

| 开机引导问题（用户可见） | 对应后台动作 | 产物 |
|--------------------------|-------------|------|
| 创建 owner 账号 | `POST /api/onboarding/users` | 账号 + 一次性 auth_code |
| 完成首次登录 | `POST /auth/token` | 长期访问令牌 |
| 设置位置 / 单位制 | `POST /api/onboarding/core_config` | location_name / 单位制 |
| 分析数据选择 | `POST /api/onboarding/analytics` | 分析偏好（默认关闭） |
| 集成步骤收尾 | `POST /api/onboarding/integration` | 向导标记为 done |

对非技术用户，引导的每一处都是卡点：要理解 `location_name`、`unit_system` 这种专业词；要自己记住刚设的账号密码；英文界面直接劝退。更麻烦的是它发生在「开机即用」的中间——用户正等着「装好了」，屏幕上却跳出「让我回答几个问题」。

好在 HAOS 给自动化留了入口：Supervisor 托管的系统自带 `ha` CLI，通过 SSH 或 Advanced SSH & Web Terminal add-on 就能进入本机；下面要讲的 onboarding API 调用，就是从这个入口在后台跑完引导。

## 4.2 主路径：onboarding API 自动化（HAOS 与 Container 通用）

把引导搬进后台的关键，是一组固定的 onboarding API 调用序列：

1. `POST /api/onboarding/users` — 创建 owner 账号，返回一次性 `auth_code`；
2. `POST /auth/token` — 用 `auth_code` 换长期访问令牌（这一步用表单编码，不是 JSON）；
3. `POST /api/onboarding/core_config` — 标记核心配置完成；
4. `POST /api/onboarding/analytics` — 提交分析数据偏好（建议默认关闭）；
5. `POST /api/onboarding/integration` — 标记集成步骤完成，向导收尾。

这条序列不挑部署形态：HAOS 上从 SSH / Web Terminal 进入本机跑，Container 部署（第 3 章 docker-compose）同样适用。因为接口未文档化、字段随版本可能变化，脚本必须在最前面做版本探测，任何一步失败都转浏览器引导：

```python
#!/usr/bin/env python3
"""
首次启动 onboarding 自动化（HAOS 与 Container 通用）：
在 HAOS 的 SSH / Web Terminal 或 Container 宿主上，用 5 个接口走完开机引导。
用法：python3 headless_onboarding.py <用户名> <密码>
"""
import json
import sys
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8123"  # 本机回环；浏览器侧访问地址是 homeassistant.local:8123


def call(method, path, data=None, token=None, form=False):
    headers = {}
    body = None
    if token:
        headers["Authorization"] = "Bearer " + token
    if data is not None:
        if form:  # /auth/token 用表单编码，其余用 JSON
            body = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, body, timeout=10) as resp:
            raw = resp.read() or b"{}"
            return resp.status, json.loads(raw)
    except Exception as exc:
        return None, {"error": str(exc)}


username, password = sys.argv[1], sys.argv[2]

# 0) 版本探测：接口未文档化，先看版本，兼容不了就退回浏览器引导
status, meta = call("GET", "/api/")
version = meta.get("version", "?")
print("[probe] HA version:", version)
if not version or int(version.split(".")[0]) < 2024:
    print("[fallback] 版本过低，请在浏览器完成初始化:", BASE)
    sys.exit(1)

# 1) 创建 owner 用户 -> 一次性 auth_code（字段随版本变化，以实测为准）
status, created = call("POST", "/api/onboarding/users", {
    "client_id": f"{BASE}/",
    "name": "Administrator",
    "username": username,
    "password": password,
})
if not status or status >= 400:
    print("[fallback] 建号失败，转浏览器引导:", BASE, created)
    sys.exit(1)
auth_code = created["auth_code"]

# 2) 用 auth_code 换长期令牌（表单提交）
_, tok = call("POST", "/auth/token",
              {"grant_type": "authorization_code",
               "code": auth_code,
               "client_id": f"{BASE}/"},
              form=True)
access_token = tok["access_token"]

# 3) 依次标记核心配置、分析偏好、集成收尾
call("POST", "/api/onboarding/core_config", {}, access_token)
call("POST", "/api/onboarding/analytics", {"user_analytics": False}, access_token)
call("POST", "/api/onboarding/integration", {}, access_token)

# 4) 校验：能读到 config 说明引导已走完
_, config = call("GET", "/api/config", token=access_token)
print("[ok] onboarding done. location:", config.get("location_name"))
```

预期输出：

```text
[probe] HA version: 2026.7.2
[ok] onboarding done. location: My Home
```

两点说明：**第一**，`/api/onboarding/users` 的请求体（尤其 `client_id`）在不同版本可能有差异，脚本里的字段是便于理解的形态，上线前必须在目标版本上实测一遍；**第二**，脚本打印出的令牌只是登录态令牌，第 6 章会讲：Agent 真正使用的应该是为它单独创建的 **Long-Lived Access Token（LLAT）**，而不是复用这个登录令牌。

> [!warning] 一个必须知道的时效性风险
> onboarding API 是未文档化的接口，社区实证于 HA 2024.11.3；它在 2026 stable（2026.7.x）上是否仍有效，至今仍是待实测项（深度收集 §7 #4）。所以无论 HAOS 还是 Container，都必须「先探测、失败回退浏览器引导」，不能写死。

## 4.3 Add-on 一键安装：Agent 上线的关键一步

HAOS 上 Agent 的交付形态是 Add-on（第 3 章已把 Agent 打包为自定义 Add-on），而不是 Container 里的 sidecar 容器。对非技术用户，这一步是一键的：

```text
Add-on Store 添加自定义仓库
   → 仓库里出现 Agent add-on
      → 一键安装
         → 填 .env（DEEPSEEK_API_KEY / TZ）
            → Agent 上线
```

在 HAOS 上，Add-on 由 Supervisor 托管，好处是用户不需要碰任何命令行：装完 add-on 只填一次 `.env`（DEEPSEEK_API_KEY / TZ），后续自动更新和快照备份都由 Supervisor 兜底。这也是「5 分钟承诺」能对完全非技术用户成立的原因之一：不只是「装好」，而是「以后不用管」。

> [!note] Add-on 与 Container 的分工
> 主交付形态（HAOS）里，Agent 是 Add-on，随系统自动更新；次级交付形态（Container）里，Agent 是 compose 里的 sidecar 容器，靠 install.sh 维护。两者的 onboarding API 自动化逻辑完全一致（见 4.2）。

## 4.4 次级场景：Container 的 onboarding 兜底（.storage 预置）

Container 是本产品的次级交付形态（第 3 章 docker-compose）。4.2 的 onboarding API 序列在 Container 上同样适用；而当 API 失效（版本过低、字段变化）时，Container 比 HAOS 多一个更底层的兜底：直接在文件系统上预置 `.storage`——因为 `./config` 是宿主目录，可以「停 HA → 写配置 → 启动」，让 HA 认为引导已经完成。HAOS 上 Supervisor 托管文件系统，走这条路要绕 SSH / `ha` CLI，不自然，所以 HAOS 优先用 4.2 的 API 路径。

需要预置的文件是 `auth`、`core.config`、`onboarding`、`person` 等，外加用 HA 同一套算法预生成的密码哈希（深度收集 §2）。以下是便于理解的最小结构：

```json
// .storage/auth：预置 owner 用户 + 预生成密码哈希
{
  "version": 1,
  "key": "auth",
  "data": {
    "auth_providers": [
      { "type": "homeassistant", "id": null, "data": {} }
    ],
    "users": [
      {
        "id": "owner-id",
        "name": "Administrator",
        "is_owner": true,
        "is_active": true,
        "group_ids": ["group-admin"],
        "credentials": [
          {
            "auth_provider_type": "homeassistant",
            "auth_provider_id": null,
            "data": {
              "hash": "pbkdf2-sha512$100000$<salt>$<derived>"
            }
          }
        ]
      }
    ]
  }
}
```

```json
// .storage/core.config：位置、单位制、时区
{
  "version": 1,
  "key": "core.config",
  "data": {
    "location_name": "My Home",
    "latitude": 31.2304,
    "longitude": 121.4737,
    "elevation": 4,
    "unit_system": { "length": "km", "mass": "kg", "temperature": "°C", "volume": "L" },
    "time_zone": "Asia/Shanghai",
    "currency": "CNY"
  }
}
```

```json
// .storage/onboarding：把 5 步向导全部标记为 done
{
  "version": 1,
  "key": "onboarding",
  "data": {
    "done": ["user", "core_config", "analytics", "integration"],
    "integrations": []
  }
}
```

```json
// .storage/person：可为空，但文件要存在
{
  "version": 1,
  "key": "person",
  "data": { "persons": [] }
}
```

> [!warning] 别手写 schema
> `.storage` 是 HA 的内部状态文件，schema 随版本演进，手写极易出错。工程上正确的做法是：**先在一台干净的 HA 上手动跑完一次引导，把生成的 `.storage` 导出为标准模板**，再按模板替换用户名、密码哈希、位置等字段。这样拿到的 schema 必然与目标版本一致，而不是靠猜。

密码哈希必须用 HA 自己的密码哈希算法（PBKDF2-SHA512）预生成，rounds / salt 策略随版本可能变化，直接用标准模板里已有的哈希格式改内容，比从零生成更稳。

## 4.5 config_flow 无头与人工环节分类

onboarding 只是让 HA「能登录」。真正的接入难关在集成层（config_flow）——第 5 章会逐个品牌展开，这里先建立判断框架。按「能不能脚本化」把集成分成两类：

| 类别 | 判断标准 | 典型集成 | 能否无头完成 |
|------|---------|---------|-------------|
| token 类 | 配置项只有 IP / token / key，无账号体系 | 米家 LAN、美的 `midea_ac_lan`、海尔 `hon-revived` | 可：停 HA → 写 `.storage/core.config_entries` → 启动 |
| OAuth 类 | 需要品牌账号授权，含扫码 / CAPTCHA | 官方米家 `xiaomi_home`、涂鸦 `tuya` 云 | 必须人工授权 |

token 类的 config entry 本质上就是一段「设备地址 + 密钥」的数据。对这类集成，可以停掉 HA，往 `.storage/core.config_entries` 里写一条记录（字段含 `domain`、`title`、`data`、`options`、`source`、`entry_id` 等），再启动 HA，它就会像正常添加一样加载（深度收集 §2）。

OAuth 类为什么必须人工？因为它的凭据不是「一段静态密钥」，而是走完品牌侧授权流程才签发的 **refresh_token + access_token**，授权过程中还有扫码、验证码（CAPTCHA）这类人类动作。脚本既拿不到品牌侧授权页面的验证，也绕不开验证码，所以这一类只能交给用户，产品层能做的是把步骤引导到最简。

## 4.6 产品 UX 三阶段设计与 5 分钟承诺边界

把上面的技术手段翻译成产品体验，就是三个递进的阶段（深度收集 §2）：

```text
插盒子开机（HAOS 启动）
   → A 后台初始化（无可感知人工，5 分钟内）
      → B Agent 后台生成 admin 凭据 + 引导页
         → C 品牌接入卡片（纯后台 / 半后台 / 必须人工）
```

| 阶段 | 内容 | 人工量 |
|------|------|--------|
| A 后台初始化 | 开机引导 API 自动化 + Add-on 一键装 Agent，全程后台 | 无可感知人工 |
| B 凭据引导页 | Agent 在后台生成 admin 随机强密码，渲染「访问地址 + 账号 + 密码」到引导页 | 用户只读不填 |
| C 品牌接入卡片 | 按品牌分三档，把第 5 章的接入动作做成卡片 | 分档：纯后台 / 半后台 / 必须人工 |

阶段 C 的三档划分，直接决定产品承诺怎么写：

- **纯后台**：token 类集成，install 阶段直接写 `.storage/core.config_entries`，用户无感知；
- **半后台**：需要用户少量输入（如涂鸦扫码、美的取 token），但通过向导卡片引导，不暴露原始技术细节；
- **必须人工**：OAuth 品牌登录（官方米家、涂鸦云），跳转品牌页面人工授权，这一档**不进 5 分钟承诺**，只承诺「向导指到哪、用户点到哪」。

> [!note] 5 分钟承诺的最终边界
> 承诺 = HAOS 开机引导（可 API 自动化）+ Add-on 一键装 Agent + 阶段 C 的「纯后台」档全部自动；「半后台」档承诺被引导完成而不是无人值守；「必须人工」档（OAuth 登录）不在 5 分钟内，属于第 5 章要重点规划人力的部分。上线前必须先实测 onboarding API 在 2026.7.x 的有效性（深度收集 §7 #4），否则引导自动化一旦失效，阶段 A 就退化成让用户开浏览器——5 分钟承诺要据此重新表述。HAOS 的自动更新 + 快照备份负责的是「承诺之后长期不用管」，不改变承诺本身的范围。

## 本章小结

- HAOS 首次启动的浏览器引导（建账号 / 位置 / 分析）= 5 个后台动作，可以用 onboarding API 整段脚本化；HAOS 与 Container 通用，接口未文档化，必须版本探测 + 失败回退浏览器引导。
- HAOS 是主交付形态：开机引导（可 API 自动化）→ Add-on Store 一键装 Agent → 填 `.env` → 配品牌；自动更新 + 快照保证后续稳定。
- Container 是次级场景：4.2 的 onboarding API 同样适用，另有一个更底层的 `.storage` 预置兜底（auth / core.config / onboarding / person + PBKDF2 密码哈希），schema 用标准模板，不要手写。
- config_flow 按「能否无头」分两类：token 类（米家 LAN / 美的 / 海尔）可写 `.storage/core.config_entries` 自动化；OAuth 类（官方米家 / 涂鸦）必须人工授权。
- 产品 UX 三阶段 = A 后台初始化（引导 + Add-on）→ B 凭据引导页 → C 品牌接入卡片（纯后台 / 半后台 / 必须人工）；5 分钟承诺只覆盖「纯后台」档，OAuth 类授权不在承诺内。

---

下一章进入全笔记的核心章节：跨品牌接入矩阵。第 4 章阶段 C 的「品牌接入卡片」会变成一张可照着操作的品牌地图——米家、涂鸦、美的、格力、海尔各自怎么接、人工环节在哪一步、时效性风险有多高。

---

> [[03_一键部署install脚本与docker编排|⬅ 第三章]] · [[基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统|返回索引]] · [[05_跨品牌接入矩阵|第五章 ➡]]
