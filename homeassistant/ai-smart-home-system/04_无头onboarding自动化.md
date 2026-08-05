---
title: "第四章 无头 onboarding：让 HA 首次启动不再需要浏览器"
type: chapter
chapter: 4
tags:
  - Home-Assistant
  - 部署
  - onboarding
created: 2026-08-05
updated: 2026-08-05
status: 已完成
source_project: ai-smart-home-system
---

# 第四章 无头 onboarding：让 HA 首次启动不再需要浏览器

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §2（onboarding 自动化）、§7（待实测 #4）
> 前置关联：[[01_系统架构与部署选型|第一章 系统架构与部署选型]]

> [!summary] 本章回答三个问题
> 1. HA 首次启动的 5 步浏览器向导能不能整段脚本化？（能，两条路径）
> 2. 什么集成可以「停 HA → 写配置 → 重启」自动化，什么必须人工？（token 类 vs OAuth 类）
> 3. 「5 分钟承诺」的技术边界到底划在哪？

第 3 章的 `install.sh` 把 HA 容器拉起来、就绪探测通过之后，用户要面对的下一个东西，是 HA 首次启动自动弹出的 **5 步浏览器向导**：建账号、设位置、选分析、选集成、点完成。对技术人这顺手就能点完，但对「非技术用户」这是第一堵墙——界面是英文、概念陌生、密码没人帮管，一旦卡在这，前面的一键部署就全白做了。本章要解决的就是：把这 5 步也变成可脚本化的后台动作，同时诚实划出「什么能自动化、什么必须人工」的边界。这决定了产品的「5 分钟承诺」到底能承诺到哪一步。

## 4.1 为什么需要无头 onboarding

### 5 步向导 = 5 个后台动作

HA 首次启动的浏览器向导，本质上是一连串「创建资源 + 打勾」的动作，正好能映射成 5 个后台调用：

| 浏览器向导步骤 | 对应后台动作 | 产物 |
|---------------|-------------|------|
| 建 owner 账号 | 创建用户 | 账号 + 一次性 auth_code |
| 完成首次登录 | 用 auth_code 换令牌 | 长期访问令牌 |
| 设位置/单位 | 写核心配置 | location_name / 单位制 |
| 分析数据选择 | 写分析偏好 | 默认关闭即可 |
| 选集成并收尾 | 标记集成完成 | 向导标记为 done |

### 非技术用户卡在哪

对非技术用户，向导的每一处都是卡点：要理解 `location_name`、`unit_system` 这种专业词；要自己记住刚设的账号密码；英文界面直接劝退。更麻烦的是它发生在「部署流程」中间——用户正等着「装好了」，屏幕上却跳出「让我回答几个问题」。

### 5 分钟承诺的技术边界

「5 分钟」承诺的前提是：**拉镜像、起容器、走完 onboarding、配好 token 类集成，全部后台完成，用户零感知**。而凡是涉及品牌账号授权的事（扫码、验证码、跳转品牌页面），都进不了这 5 分钟，只能作为「必须人工」步骤交给向导引导。本章的技术目标就是让「后台完成」的部分尽量大，同时把「必须人工」的部分提前暴露给产品设计深度收集 §2。

实现上有两条路径：

- **路径 A（推荐）**：HA 已经启动，实时调 onboarding API 把向导走完；
- **路径 B（兜底）**：HA 启动前就预置好 `.storage` 文件，让 HA 以为向导已经完成。

> [!warning] 一个必须知道的时效性风险
> onboarding API 是未文档化的接口，社区实证于 HA 2024.11.3；它在 2026 stable（2026.7.x）上是否仍有效，至今仍是待实测项§7 #4。所以两条路径都必须是「先探测、失败回退浏览器向导」，不能写死。

## 4.2 路径 A（推荐）：onboarding API 调用序列

路径 A 的核心是 5 个请求的固定顺序：

1. `POST /api/onboarding/users` — 创建 owner 账号，返回一次性 `auth_code`；
2. `POST /auth/token` — 用 `auth_code` 换长期访问令牌（这一步用表单编码，不是 JSON）；
3. `POST /api/onboarding/core_config` — 标记核心配置完成；
4. `POST /api/onboarding/analytics` — 提交分析数据偏好（建议默认关闭）；
5. `POST /api/onboarding/integration` — 标记集成步骤完成，向导收尾。

因为接口未文档化、字段随版本可能变化，脚本必须在最前面做版本探测，任何一步失败都转浏览器向导：

```python
#!/usr/bin/env python3
"""
无头 onboarding（路径 A）：HA 首次启动后，用 5 个接口走完浏览器向导。
用法：python3 headless_onboarding.py <用户名> <密码>
"""
import json
import sys
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8123"  # 与 install.sh 的就绪探测同一地址


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

# 0) 版本探测：接口未文档化，先看版本，兼容不了就退回浏览器向导
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
    print("[fallback] 建号失败，转浏览器向导:", BASE, created)
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

# 4) 校验：能读到 config 说明向导已走完
_, config = call("GET", "/api/config", token=access_token)
print("[ok] onboarding done. location:", config.get("location_name"))
```

预期输出：

```text
[probe] HA version: 2026.7.2
[ok] onboarding done. location: My Home
```

两点说明：**第一**，`/api/onboarding/users` 的请求体（尤其 `client_id`）在不同版本可能有差异，脚本里的字段是便于理解的形态，上线前必须在目标版本上实测一遍；**第二**，脚本打印出的令牌只是登录态令牌，第 6 章会讲：Agent 真正使用的应该是为它单独创建的 **Long-Lived Access Token（LLAT）**，而不是复用这个登录令牌。

## 4.3 路径 B（兜底）：.storage 文件预置

当路径 A 失效（版本过低、接口字段变化）时，改用「启动前预置 `.storage`」：在 HA **首次启动之前**，往 `./config/.storage/` 写入 4 个文件，让 HA 认为向导已经完成。需要预置的文件是 `auth`、`core.config`、`onboarding`、`person` 等，外加用 HA 同一套算法预生成的密码哈希深度收集 §2。

操作顺序：**停 HA → 写 `.storage` → 启动 → 用 admin 账号登录校验**。以下是便于理解的最小结构：

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
> `.storage` 是 HA 的内部状态文件，schema 随版本演进，手写极易出错。工程上正确的做法是：**先在一台干净的 HA 上手动跑完一次向导，把生成的 `.storage` 导出为标准模板**，再按模板替换用户名、密码哈希、位置等字段。这样拿到的 schema 必然与目标版本一致，而不是靠猜。

密码哈希必须用 HA 自己的密码哈希算法（PBKDF2-SHA512）预生成，rounds / salt 策略随版本可能变化，直接用标准模板里已有的哈希格式改内容，比从零生成更稳。

## 4.4 config_flow 无头与人工环节分类

onboarding 只是让 HA「能登录」。真正的接入难关在集成层（config_flow）——第 5 章会逐个品牌展开，这里先建立判断框架。按「能不能脚本化」把集成分成两类：

| 类别 | 判断标准 | 典型集成 | 能否无头完成 |
|------|---------|---------|-------------|
| token 类 | 配置项只有 IP / token / key，无账号体系 | 米家 LAN、美的 `midea_ac_lan`、海尔 `hon-revived` | 可：停 HA → 写 `.storage/core.config_entries` → 启动 |
| OAuth 类 | 需要品牌账号授权，含扫码 / CAPTCHA | 官方米家 `xiaomi_home`、涂鸦 `tuya` 云 | 必须人工授权 |

token 类的 config entry 本质上就是一段「设备地址 + 密钥」的数据。对这类集成，可以停掉 HA，往 `.storage/core.config_entries` 里写一条记录（字段含 `domain`、`title`、`data`、`options`、`source`、`entry_id` 等），再启动 HA，它就会像正常添加一样加载深度收集 §2。

OAuth 类为什么必须人工？因为它的凭据不是「一段静态密钥」，而是走完品牌侧授权流程才签发的 **refresh_token + access_token**，授权过程中还有扫码、验证码（CAPTCHA）这类人类动作。脚本既拿不到品牌侧授权页面的验证，也绕不开验证码，所以这一类只能交给用户，产品层能做的是把步骤引导到最简。

## 4.5 产品 UX 三阶段设计

把上面的技术手段翻译成产品体验，就是三个递进的阶段深度收集 §2：

```text
install.sh 起容器
   → A 后台安装（无可感知人工，5 分钟内）
      → B Agent 后台生成 admin 凭据 + 引导页
         → C 品牌接入卡片（纯后台 / 半后台 / 必须人工）
```

| 阶段 | 内容 | 人工量 |
|------|------|--------|
| A 后台安装 | install.sh + 路径 A onboarding，全程后台 | 无可感知人工 |
| B 凭据引导页 | Agent 在后台生成 admin 随机强密码，渲染「访问地址 + 账号 + 密码」到引导页 | 用户只读不填 |
| C 品牌接入卡片 | 按品牌分三档，把第 5 章的接入动作做成卡片 | 分档：纯后台 / 半后台 / 必须人工 |

阶段 C 的三档划分，直接决定产品承诺怎么写：

- **纯后台**：token 类集成，install 阶段直接写 `.storage/core.config_entries`，用户无感知；
- **半后台**：需要用户少量输入（如涂鸦扫码、美的取 token），但通过向导卡片引导，不暴露原始技术细节；
- **必须人工**：OAuth 品牌登录（官方米家、涂鸦云），跳转品牌页面人工授权，这一档**不进 5 分钟承诺**，只承诺「向导指到哪、用户点到哪」。

> [!note] 5 分钟承诺的最终边界
> 承诺 = 阶段 A + B + 阶段 C 的「纯后台」档全部自动；「半后台」档承诺被引导完成而不是无人值守；「必须人工」档（OAuth 登录）不在 5 分钟内，属于第 5 章要重点规划人力的部分。上线前必须先实测 onboarding API 在 2026.7.x 的有效性（§7 #4），否则路径 A 一旦失效，阶段 A 就退化成阶段 B 引导用户开浏览器——5 分钟承诺要据此重新表述。

## 本章小结

- HA 首次启动的 5 步浏览器向导 = 5 个后台动作，可以整段脚本化：路径 A（onboarding API 序列）优先，路径 B（`.storage` 预置）兜底。
- 路径 A 的 5 个请求顺序是 `users → auth/token → core_config → analytics → integration`；接口未文档化，必须版本探测 + 失败回退浏览器向导。
- 路径 B 在首次启动前预置 `auth` / `core.config` / `onboarding` / `person` 4 个文件，密码哈希用 HA 的 PBKDF2-SHA512 方案预生成；**schema 用标准模板，不要手写**。
- config_flow 按「能否无头」分两类：token 类（米家 LAN / 美的 / 海尔）可写 `.storage/core.config_entries` 自动化；OAuth 类（官方米家 / 涂鸦）必须人工授权。
- 产品 UX 三阶段 = A 后台安装 → B 凭据引导页 → C 品牌接入卡片（纯后台 / 半后台 / 必须人工）；5 分钟承诺只覆盖「纯后台」档，OAuth 类授权不在承诺内。

---

下一章进入全笔记的核心章节：跨品牌接入矩阵。第 4 章阶段 C 的「品牌接入卡片」会变成一张可照着操作的品牌地图——米家、涂鸦、美的、格力、海尔各自怎么接、人工环节在哪一步、时效性风险有多高。

---

> [[03_一键部署install脚本与docker编排|⬅ 第三章]] · [[基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统|返回索引]] · [[05_跨品牌接入矩阵|第五章 ➡]]
