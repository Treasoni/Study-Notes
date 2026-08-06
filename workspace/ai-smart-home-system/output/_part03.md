## 第四章 无头 onboarding：让 HA 首次启动不再需要浏览器

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §2（onboarding 自动化）、§7（待实测 #4）
> 前置关联：[[01_系统架构与部署选型|第一章 系统架构与部署选型]]

> [!summary] 本章回答三个问题
> 1. HA 首次启动的 5 步浏览器向导能不能整段脚本化？（能，两条路径）
> 2. 什么集成可以「停 HA → 写配置 → 重启」自动化，什么必须人工？（token 类 vs OAuth 类）
> 3. 「5 分钟承诺」的技术边界到底划在哪？

第 3 章的 `install.sh` 把 HA 容器拉起来、就绪探测通过之后，用户要面对的下一个东西，是 HA 首次启动自动弹出的 **5 步浏览器向导**：建账号、设位置、选分析、选集成、点完成。对技术人这顺手就能点完，但对「非技术用户」这是第一堵墙——界面是英文、概念陌生、密码没人帮管，一旦卡在这，前面的一键部署就全白做了。本章要解决的就是：把这 5 步也变成可脚本化的后台动作，同时诚实划出「什么能自动化、什么必须人工」的边界。这决定了产品的「5 分钟承诺」到底能承诺到哪一步。

### 4.1 为什么需要无头 onboarding

#### 5 步向导 = 5 个后台动作

HA 首次启动的浏览器向导，本质上是一连串「创建资源 + 打勾」的动作，正好能映射成 5 个后台调用：

| 浏览器向导步骤 | 对应后台动作 | 产物 |
|---------------|-------------|------|
| 建 owner 账号 | 创建用户 | 账号 + 一次性 auth_code |
| 完成首次登录 | 用 auth_code 换令牌 | 长期访问令牌 |
| 设位置/单位 | 写核心配置 | location_name / 单位制 |
| 分析数据选择 | 写分析偏好 | 默认关闭即可 |
| 选集成并收尾 | 标记集成完成 | 向导标记为 done |

#### 非技术用户卡在哪

对非技术用户，向导的每一处都是卡点：要理解 `location_name`、`unit_system` 这种专业词；要自己记住刚设的账号密码；英文界面直接劝退。更麻烦的是它发生在「部署流程」中间——用户正等着「装好了」，屏幕上却跳出「让我回答几个问题」。

#### 5 分钟承诺的技术边界

「5 分钟」承诺的前提是：**拉镜像、起容器、走完 onboarding、配好 token 类集成，全部后台完成，用户零感知**。而凡是涉及品牌账号授权的事（扫码、验证码、跳转品牌页面），都进不了这 5 分钟，只能作为「必须人工」步骤交给向导引导。本章的技术目标就是让「后台完成」的部分尽量大，同时把「必须人工」的部分提前暴露给产品设计[深度收集 §2](../02_deep_research.md)。

实现上有两条路径：

- **路径 A（推荐）**：HA 已经启动，实时调 onboarding API 把向导走完；
- **路径 B（兜底）**：HA 启动前就预置好 `.storage` 文件，让 HA 以为向导已经完成。

> [!warning] 一个必须知道的时效性风险
> onboarding API 是未文档化的接口，社区实证于 HA 2024.11.3；它在 2026 stable（2026.7.x）上是否仍有效，至今仍是待实测项[§7 #4](../02_deep_research.md)。所以两条路径都必须是「先探测、失败回退浏览器向导」，不能写死。

### 4.2 路径 A（推荐）：onboarding API 调用序列

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

### 4.3 路径 B（兜底）：.storage 文件预置

当路径 A 失效（版本过低、接口字段变化）时，改用「启动前预置 `.storage`」：在 HA **首次启动之前**，往 `./config/.storage/` 写入 4 个文件，让 HA 认为向导已经完成。需要预置的文件是 `auth`、`core.config`、`onboarding`、`person` 等，外加用 HA 同一套算法预生成的密码哈希[深度收集 §2](../02_deep_research.md)。

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

### 4.4 config_flow 无头与人工环节分类

onboarding 只是让 HA「能登录」。真正的接入难关在集成层（config_flow）——第 5 章会逐个品牌展开，这里先建立判断框架。按「能不能脚本化」把集成分成两类：

| 类别 | 判断标准 | 典型集成 | 能否无头完成 |
|------|---------|---------|-------------|
| token 类 | 配置项只有 IP / token / key，无账号体系 | 米家 LAN、美的 `midea_ac_lan`、海尔 `hon-revived` | 可：停 HA → 写 `.storage/core.config_entries` → 启动 |
| OAuth 类 | 需要品牌账号授权，含扫码 / CAPTCHA | 官方米家 `xiaomi_home`、涂鸦 `tuya` 云 | 必须人工授权 |

token 类的 config entry 本质上就是一段「设备地址 + 密钥」的数据。对这类集成，可以停掉 HA，往 `.storage/core.config_entries` 里写一条记录（字段含 `domain`、`title`、`data`、`options`、`source`、`entry_id` 等），再启动 HA，它就会像正常添加一样加载[深度收集 §2](../02_deep_research.md)。

OAuth 类为什么必须人工？因为它的凭据不是「一段静态密钥」，而是走完品牌侧授权流程才签发的 **refresh_token + access_token**，授权过程中还有扫码、验证码（CAPTCHA）这类人类动作。脚本既拿不到品牌侧授权页面的验证，也绕不开验证码，所以这一类只能交给用户，产品层能做的是把步骤引导到最简。

### 4.5 产品 UX 三阶段设计

把上面的技术手段翻译成产品体验，就是三个递进的阶段[深度收集 §2](../02_deep_research.md)：

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

### 本章小结

- HA 首次启动的 5 步浏览器向导 = 5 个后台动作，可以整段脚本化：路径 A（onboarding API 序列）优先，路径 B（`.storage` 预置）兜底。
- 路径 A 的 5 个请求顺序是 `users → auth/token → core_config → analytics → integration`；接口未文档化，必须版本探测 + 失败回退浏览器向导。
- 路径 B 在首次启动前预置 `auth` / `core.config` / `onboarding` / `person` 4 个文件，密码哈希用 HA 的 PBKDF2-SHA512 方案预生成；**schema 用标准模板，不要手写**。
- config_flow 按「能否无头」分两类：token 类（米家 LAN / 美的 / 海尔）可写 `.storage/core.config_entries` 自动化；OAuth 类（官方米家 / 涂鸦）必须人工授权。
- 产品 UX 三阶段 = A 后台安装 → B 凭据引导页 → C 品牌接入卡片（纯后台 / 半后台 / 必须人工）；5 分钟承诺只覆盖「纯后台」档，OAuth 类授权不在承诺内。

---

下一章进入全笔记的核心章节：跨品牌接入矩阵。第 4 章阶段 C 的「品牌接入卡片」会变成一张可照着操作的品牌地图——米家、涂鸦、美的、格力、海尔各自怎么接、人工环节在哪一步、时效性风险有多高。

## 第五章 跨品牌接入矩阵

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §3（整节）、§6（#4、#6）、§7（#2、#3、#5、#6）
> 前置关联：[[Home Assistant 三种部署方式对比与选型.md]]

> [!summary] 本章回答三个问题
> 1. 市面主流品牌（米家 / 涂鸦 / 美的 / 格力 / 海尔）能不能接进同一套 HA，各自怎么接？
> 2. 哪些品牌现在能放心承诺、哪些带有「时效性风险」必须在交付前说清楚？
> 3. MVP 阶段应该把哪些组件打进镜像、首次接入要留哪些人工环节？

上一章解决了「系统跑起来」，这一章解决「设备进得来」。这套系统的核心卖点是「跨品牌统一」——不是只服务米家用户，而是市面主流品牌都能收敛进同一个 Home Assistant。但每个品牌的接入方式、人工成本、失效风险完全不同：有的全本地、一次配好永久可用；有的要扫码授权、密钥还会过期；有的干脆没有可靠路径。本章先给你一张接入矩阵总表，再逐个品牌展开「怎么接、哪些环节要人工、会踩什么时效性的坑」，最后落到 MVP 预置清单和首次接入的人工步骤——这正是第 4 章「品牌接入卡片」产品设计的落地依据。

### 5.1 接入矩阵总览

先看全貌。下表是跨品牌接入的完整矩阵，横跨 7 种路径：米家、涂鸦、美的、格力、海尔、华为，以及最后的通用标准兜底[深度收集 §3](../02_deep_research.md)：

| 品牌 | 集成 | 接入方式 | 人工环节 | 时效性风险 |
|------|------|----------|----------|------------|
| 米家 | `xiaomi_home`（小米官方，22k⭐，非 core） | OAuth 2.0 网页登录（2025 起含 CAPTCHA）→ 选家庭/设备 | 小米账号登录 | vacuum `battery_level` 弃用告警截至 v0.4.7 未修复（HA 2026.8 移除）；LAN 控制需中枢网关 |
| 涂鸦 | 官方 `tuya`（云）+ `localtuya`（本地 fork） | 云：App 扫码 + User Code；本地：设备 IP + ID + local_key | 扫码 / 取 key | 涂鸦 IoT 后台密钥限时；门锁/摄像头不再提供 localKey；中国区 `openapi.tuyacn.com` 需 IP 白名单 |
| 美的 | `midea_ac_lan`（30+ 品类，全本地） | V1/V2 自动发现；V3 需云端一次取 token(128hex) + key(64hex) | V3 首次美的账号取 token | **V1 Token API 已关，NetHome Plus 陆续关闭**；新设备可能无法取 token，老 token 必须备份 |
| 格力 | 内置 `gree`（全本地轮询） | 自动发现 LAN | 设备需先经格力+ App 配网 | 低；内置缺 `hvac_action`，增强走社区版 |
| 海尔 | `hon-revived`（hOn 云 fork） | hOn 账号登录（邮箱密码） | hOn 账号 | 云 API 易变，「易碎」，作高级项 |
| 华为 | 无可靠路径 | — | — | 生态封闭；只给指引（Matter / 反向控制） |
| 兜底 | Matter / MQTT / Zigbee | 需 sidecar 容器（Zigbee/Thread 还需 USB 协调器） | 硬件 | 不适合纯云 MVP 默认 |

这张表怎么读？先看两列：「人工环节」决定产品向导要留多少步人工，「时效性风险」决定你能不能对客户做出长期承诺。米家、美的、涂鸦是保有量最大的三个入口，但恰好也是时效性风险最高的三个——这就是「跨品牌统一」看起来美好、落地要逐个排雷的原因。

### 5.2 米家：xiaomi_home（官方，22k⭐）

米家接入走小米官方维护的 `xiaomi_home` 集成，GitHub 约 22k star，但注意它**不是 HA core 内置**，需要作为 custom_component 预置。这也是本项目与桌面报告的一处重要修正：报告原方案预置的是第三方 `xiaomi_gateway3`，实际应采用官方 `xiaomi_home`[深度收集 §6 #4](../02_deep_research.md)。

#### 接入流程要点

- **授权方式**：OAuth 2.0 网页登录。用户用小米账号登录、授权，然后选择要接入的家庭和设备。
- **2025 起的坑**：登录流程加入 CAPTCHA（图形验证码），这一步**无法自动化**，必须由用户本人完成——这是米家接入里不可压缩的人工环节。
- **选家庭/设备**：登录后勾选家庭和具体设备，HA 才会把实体同步进来。

#### 时效性风险

- **vacuum `battery_level` 弃用告警**：截至 v0.4.7，扫地机的 `battery_level` 属性弃用告警尚未修复，而 HA 官方计划在 2026.8 移除该属性。这意味着如果你锁定 v0.4.7，就要留意它和 HA Core 2026.8 之后的兼容性；这也被列进第 8 章的待实测事项（`xiaomi_home` 是否已有 v0.4.8+ 修复，决定 HA Core 版本锁定策略）[深度收集 §7 #2](../02_deep_research.md)。
- **LAN 控制依赖中枢网关**：米家设备走本地局域网控制需要中枢网关（米家中枢网关），没有中枢网关卡点的设备只能走云端，控制链路更慢也更容易受网络影响。

> [!warning] 版本锁定 vs 官方修复
> `xiaomi_home` 无 HACS 自动更新，预置进镜像后只能锁定在某个 tag（本项目锁 v0.4.7）。如果官方在 v0.4.8 修复了 `battery_level` 告警，需要手动升级镜像里的组件——这正是第 7 章「版本锁定防漂移」要解决的工程问题。

### 5.3 涂鸦：官方 tuya（云） vs localtuya（本地）

涂鸦有两套接入路径，对应完全不同的授权模型和风险画像，交付时要帮用户选对。

#### 云（官方 tuya，随 HA Core 内置）

- **接入方式**：App 扫码 + User Code。用户在涂鸦/智慧生活 App 里扫码授权，把云账号接入 HA，设备经涂鸦云端同步过来。
- **优点**：零本地配置，所有云端设备一步到位。
- **风险**：数据走云；涂鸦 IoT 后台的**密钥是限时的**，密钥过期需要重新授权。

#### 本地（localtuya，custom_component）

- **接入方式**：每个设备填 **IP + device_id + local_key**。`local_key` 可从涂鸦 IoT 后台或社区工具（如 tinytuya）提取。
- **优点**：设备控制走局域网，速度快、断网可用。
- **风险**：
  - **门锁 / 摄像头不再提供 localKey**——这类设备从源头就断了本地接入的可能，只能走云或放弃；
  - **中国区后端**：`openapi.tuyacn.com` 需要 **IP 白名单**，首次配置要在涂鸦 IoT 后台把自己公网 IP 加白，否则取 key 失败。

> [!tip] 云还是本地？
> 简单规则：设备本身支持本地取 key、又在同一局域网，优先 `localtuya`（更快更稳）；没有 localKey 能力的设备（门锁/摄像头）或用户接受云端链路，用官方 `tuya` 云。两者可以共存，同一个 HA 里同时接云和本地并不冲突。

### 5.4 美的：midea_ac_lan（30+ 品类，全本地）

美的接入用社区维护的 `midea_ac_lan`（wuwentao/midea_ac_lan），覆盖 30+ 品类，**全本地通信**——这是它最大的卖点：不依赖云、响应快。但它的认证分三代，时效性风险是五个品牌里最需要预警的。

#### V1 / V2：自动发现

老一代美的设备走 V1/V2 协议，集成在局域网自动发现，基本零配置。这一类最省心，但设备在逐年变少。

#### V3：云端一次取 token + key

新一代美的设备走 V3，需要**云端一次性获取**两组密钥：`token`（128 位 hex）+ `key`（64 位 hex）。获取动作需要用户用美的账号完成，取到后写进本地配置，之后就是纯本地控制。

#### 时效性风险（重点）

- **V1 Token API 已关闭**：美的关掉了旧版取 token 的接口，走 V1 的老设备如果当初没留下 token，现在可能已经无法重新获取。
- **NetHome Plus 陆续关闭**：美的的 NetHome Plus 云服务正在逐步下线，V3 新设备取 token 依赖它，中国区新设备 2026 年还能不能取到 token 是**未验证事项**[深度收集 §7 #3](../02_deep_research.md)。
- **老 token 必须备份**：因为接口在关、云在退，一旦取到过 token/key，务必在交付时随 `entity_map.yaml` 一起备份到客户配置目录，否则日后换机、重装可能再也拿不回来。

> [!warning] 美的接入承诺要保守
> 对美的用户，MVP 阶段承诺「尽量接、取 token 失败给回退方案」比承诺「必接」更稳。取 token 失败时产品向导要回退到抓包教程（社区常见做法），而不是卡死。

### 5.5 格力与海尔：内置 gree 与 hon-revived

这两个品牌风险相对温和，一个全本地、一个走云，但都各有取舍。

#### 格力：内置 gree（全本地轮询）

- **接入方式**：HA 内置 `gree` 集成，局域网自动发现，无需额外预置组件。
- **人工环节**：设备必须**先用格力+ App 完成配网**，之后 HA 才能在局域网发现它。
- **取舍**：内置集成缺 `hvac_action`（制热/制冷动作状态），对只看温度/开关的场景够用；想要完整状态，要换社区增强版。时效性风险低。

#### 海尔：hon-revived（hOn 云 fork）

- **接入方式**：`hon-revived` 是 hOn 云的社区 fork，用户用 **hOn 账号（邮箱密码）登录**。
- **定位**：云 API 易变，社区把这类集成称为「易碎」——hOn 官方改接口，fork 就要跟着改，随时可能失效。
- **决策**：本项目把它列为**高级项**，不作为 MVP 主推；预置组件但交付时明确「可用性随上游 hOn 云变动」。

### 5.6 华为与兜底方案

#### 华为：无可靠路径，只给指引

华为智能家居生态封闭，当前**没有可靠的 HA 接入路径**——这是报告 6 处过时修正之一（报告原称华为可接入，实际不可）[深度收集 §6 #6](../02_deep_research.md)。因此：

- **不预置组件**，在文档里给指引而非承诺；
- 指引方向：支持 **Matter** 的华为设备走 Matter 标准协议接入；或走**反向控制**（由 HA 侧/第三方平台反过来被华为生态控制），两者都取决于具体设备和网关，逐台评估，无法作为默认交付项。

#### 兜底：Matter / MQTT / Zigbee

如果某个设备任何品牌集成都接不进，最后还有三条通用标准兜底：

| 标准 | 形态 | 附加硬件 | 说明 |
|------|------|----------|------|
| Matter | 标准协议 | 无需额外（需支持 Matter 的设备/桥） | 跨品牌互操作新标准，华为/SwitchBot 等新设备常用 |
| MQTT | 消息协议 | 无需额外 | 适合 DIY / 已暴露 MQTT 的设备 |
| Zigbee | 无线协议 | **USB 协调器** | 需要 sidecar 容器 + USB 协调器（`--privileged`） |
| Thread | 无线协议 | USB 协调器 | 同 Zigbee，通常伴随 Matter over Thread |

> [!note] 为什么兜底方案不适合纯云 MVP 默认
> Matter / MQTT / Zigbee 三类都要求额外的 sidecar 容器（Zigbee/Thread 还要 USB 协调器），属于**硬件与网络双投入**，超出「一条命令 + 纯云」的 MVP 承诺范围。它们是扩展选项，不是默认项——先通过品牌集成覆盖绝大多数用户，少数接不进的设备再走兜底。

### 5.7 MVP 预置清单与首次人工步骤

#### 无 HACS 预置顺序

本项目承诺「不依赖 HACS」，所有组件在**构建镜像时预置进 `config/custom_components/`**。目录布局遵循 HA 的 custom_component 规范（`__init__.py` + `manifest.json` + `config_flow.py`）[深度收集 §5](../02_deep_research.md)：

```text
config/custom_components/
├── xiaomi_home/        # 米家官方，锁 tag v0.4.7（非 core，需预置）
│   ├── __init__.py
│   ├── manifest.json
│   └── config_flow.py
├── localtuya/          # 涂鸦本地（xZetsubou/hass-localtuya）
├── midea_ac_lan/       # 美的（wuwentao/midea_ac_lan）
└── hon/                # 海尔（mmalolepszy/hon-revived），高级/易碎
```

其中 **`tuya`（云）和 `gree`（格力）是 HA Core 内置**，随官方镜像直接可用，不需要预置。华为**不预置任何组件**，只放文档指引。预置顺序本身就是一个决策：先保保有量最大的米家、涂鸦，再补美的、格力，海尔作高级项，华为只给指引。

各品牌接入参数，汇总成「参数卡」方便你在 configuration.yaml 或配置流里对照（具体键名以各集成当前版本的 config_flow 为准）：

```yaml
# configuration.yaml 接入骨架（示例）
# 注意：主要品牌走 UI config_flow，以下仅为直写式参数示例，
# 具体键名与 protocol_version 以对应集成文档/当前版本为准。

# 涂鸦本地（localtuya）—— 每设备一段：IP + device_id + local_key
localtuya:
  devices:
    - host: 192.168.1.50
      device_id: "<涂鸦后台/tinytuya 提取的 device id>"
      local_key: "<涂鸦后台/tinytuya 提取的 key>"

# 美的（midea_ac_lan）—— V1/V2 自动发现可省配置；V3 需 token + key
midea_ac_lan:
  - host: 192.168.1.60
    token: "<128 位 hex>"
    key: "<64 位 hex>"

# 米家 xiaomi_home / 格力 gree / 海尔 hon：走 UI 登录，无需 YAML 直写
# - 米家：OAuth 网页登录（含 CAPTCHA，必须人工）
# - 格力：自动发现（需先经格力+ App 配网）
# - 海尔：hOn 邮箱密码登录
```

#### 产品向导要覆盖的首次人工步骤

结合第 4 章的「纯后台 / 半后台 / 必须人工」三档分类[深度收集 §2](../02_deep_research.md)，各品牌首次接入的人工环节清单如下，产品向导（阶段 C 的品牌接入卡片）要逐项覆盖：

| 品牌 | 人工环节 | 工具/途径 | 档位 |
|------|----------|-----------|------|
| 米家 | 小米账号 OAuth 登录（含 CAPTCHA） | 浏览器网页登录 | 必须人工 |
| 涂鸦-云 | App 扫码 + User Code | 涂鸦/智慧生活 App | 必须人工 |
| 涂鸦-本地 | 取 device_id + local_key | tinytuya 或 iot.tuya.com（中国区需先加 IP 白名单） | 半后台 |
| 美的 | V3 首次取 token（128hex）+ key（64hex） | 美的账号 + 取 token 工具（失败回退抓包教程） | 半后台 |
| 格力 | 先用格力+ App 给设备配网 | 格力+ App | 人工（一次性，之后自动发现） |
| 海尔 | hOn 邮箱密码登录 | hOn App/网页 | 半后台 |
| 华为 | — | 文档指引（Matter / 反向控制，逐台评估） | 不承诺 |

> [!tip] 人工环节与「5 分钟承诺」的边界
> 第 4 章说得很清楚：**token 类**集成（米家 LAN / 美的 / 海尔）理论上可写 `.storage/core.config_entries` 实现纯后台，但 **OAuth 类（官方米家 / 涂鸦扫码）必须人工授权**。所以「5 分钟承诺」要定义在「系统启动 + 引导到品牌接入卡片」，而不是「全部设备接完」——把必须人工的扫码/登录留给用户自己完成，是诚实且可实现的边界。

### 本章小结

- 接入矩阵 = 米家（`xiaomi_home` OAuth）、涂鸦（云 `tuya` + 本地 `localtuya`）、美的（`midea_ac_lan` 全本地）、格力（内置 `gree` 本地）、海尔（`hon-revived` 云）、华为（无可靠路径只给指引）、兜底（Matter / MQTT / Zigbee）。
- 时效性风险最高的是三个保有量最大的入口：米家 `battery_level` 告警未修复且 LAN 需中枢网关；美的 V1 Token API 已关、NetHome Plus 关闭中、老 token 必须备份；涂鸦密钥限时、门锁/摄像头不再给 localKey、中国区需 IP 白名单。
- 本地优先原则：能走本地（localtuya / midea_ac_lan / gree）就走本地，速度与断网可用性都更好；云端（tuya / hon）作为无本地能力设备的补充。
- MVP 预置顺序（无 HACS）：`xiaomi_home`（锁 v0.4.7）→ 内置 `tuya` + `localtuya` → `midea_ac_lan` → 内置 `gree` → `hon`（高级/易碎）；华为不预置。
- 首次人工步骤集中在 OAuth/扫码/取 key 三件事上，产品向导要按「纯后台 / 半后台 / 必须人工」三档分别设计，这正是「5 分钟承诺」的诚实边界。

---

下一章接入「大脑」：设备都进系统了，怎么用自然语言控制它们？你会基于 FastAPI + DeepSeek Function Calling 实现一个智能体，并避开 DeepSeek V4 的已知坑（tool_choice 必须用 auto、thinking 要关闭）。

## 第六章 AI 智能体：FastAPI + DeepSeek Function Calling

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §4、§6（时效性修正 #2）、§7（#4、#7）
> 前置关联：第一章四层架构中的「智能体层」；`workspace/ai-smart-home-system/agent/` 可运行代码骨架

> [!summary] 本章回答三个问题
> 1. DeepSeek 在 2026-08 的 API 事实是什么？哪些旧教程写法会直接踩 400？
> 2. 一个「自然语言 → 设备控制」的最小 Agent 循环长什么样？
> 3. 把设备控制权交给 AI，怎么设计才不至于开出一个「口子」？

前面几章把 Home Assistant 跑起来、接入了品牌设备，现在系统已经有「耳朵」了，但还缺「大脑」。本章补上四层架构里的智能体层：一个轻量 Python（FastAPI）进程接收用户的自然语言，交给 DeepSeek Function Calling 解析成结构化工具调用，再通过 HA REST API 执行。你会拿到一份能跑的骨架（`workspace/ai-smart-home-system/agent/`），并理解它为什么绕开了 DeepSeek V4 的几个已知坑。

### 6.1 API 事实核对：2026-08 的 DeepSeek 现状

动笔前先核对 API 事实。DeepSeek 在 2026 年对模型命名、思考模式、`tool_choice` 都做了调整，网上大量旧教程会把你直接带进 400。[深度收集 §4](../02_deep_research.md)

| 事实 | 取值 | 为什么必须记住 |
|------|------|----------------|
| 模型名 | `deepseek-v4-flash` | 旧名 `deepseek-chat` / `deepseek-reasoner` 已于 2026-07-24 停用，传旧名直接报错 |
| 价格 | $0.14 / 1M 输入，$0.28 / 1M 输出 | 缓存命中约便宜 50 倍，高频提示词值得做静态化 |
| base_url | `https://api.deepseek.com` | OpenAI 兼容端点，直接用 openai SDK 即可 |
| tool_choice | 统一 `"auto"` | V4 思考模式下传 `"required"` 或指定函数名返回 HTTP 400 |
| thinking | MVP 显式关闭 | V4 默认开启，工具轮次要回传 `reasoning_content` 否则 400；关闭后更快更便宜且允许 `temperature` |

`tool_choice` 这一条最关键。旧教程里「强制模型必须调某个函数」的写法在 V4 思考模式下直接废掉，官方文档与 issue #1376 都确认了这一点。[DeepSeek API 文档](https://api-docs.deepseek.com) 本项目用三层替代「强制工具调用」：`tool_choice="auto"` + 系统提示「可执行指令先调一次工具」+ 应用层 N=1 循环保证最多执行一次。意图由模型自己判断，行为边界由应用层兜底。

### 6.2 Agent 主循环：main.py 的 N=1 tool-calling

主循环的职责很克制：**模型最多发起 1 次工具调用**（`MAX_TOOL_ROUNDS = 1`），执行后把结果回填，再请求一次拿到最终答复，然后收工。不做多步规划、不给模型第二次调工具的机会。对「单条命令控制」这个场景，这是最稳的做法——多步规划看着聪明，但每多一步就多一次幻觉和越权机会。

先看工具白名单，它定义了 Agent 能力的边界：[深度收集 §4](../02_deep_research.md)

```python
ENTITY_ID_RE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z0-9_]+$")
ALLOWED_DOMAINS = {"light", "switch", "fan", "cover", "media_player", "climate"}
ALLOWED_SERVICES: dict[str, set[str]] = {
    "light": {"turn_on", "turn_off", "toggle"},
    "switch": {"turn_on", "turn_off", "toggle"},
    "fan": {"turn_on", "turn_off", "toggle", "set_percentage"},
    "cover": {"open_cover", "close_cover", "stop_cover", "set_cover_position"},
    "media_player": {"turn_on", "turn_off", "toggle", "volume_set"},
    "climate": {"turn_on", "turn_off", "set_temperature", "set_hvac_mode"},
}
```

domain 白名单决定「能碰哪些类型的设备」，service 白名单决定「能对这类设备做什么」。另外还有一份给模型看的结构化元数据 `TOOL_DEFS`（两个工具的 JSON Schema），真正执行的是 `TOOL_HANDLERS`。函数名白名单、domain/service 双层白名单，就是 6.5 安全设计的执行骨架。

N=1 循环的核心逻辑（完整文件见 `agent/main.py` 的 `run_agent`）：

```python
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
messages = _build_messages(user_text)

first = await asyncio.to_thread(
    client.chat.completions.create,
    model=DEEPSEEK_MODEL, messages=messages, tools=TOOL_DEFS,
    tool_choice="auto", temperature=0.2,
    extra_body={"thinking": {"type": DEEPSEEK_THINKING}},   # 关闭思考，见 6.1
)
msg = first.choices[0].message
tool_calls = getattr(msg, "tool_calls", None) or []
if not tool_calls:                       # 模型认为无需调工具（闲聊/询问）
    return (msg.content or "（无回复）"), 0

# ---- N=1：只执行第一个工具调用 ----
tool_call = tool_calls[0]
messages.append({"role": "assistant", "content": msg.content or None,
                 "tool_calls": [tc.model_dump() for tc in tool_calls]})

try:
    args = _validate_tool_call(tool_call.function.name,
                               json.loads(tool_call.function.arguments or "{}"))
    result = await TOOL_HANDLERS[tool_call.function.name](**args)   # 白名单内的真实执行
except ValueError as exc:
    result = f"错误：参数校验未通过：{exc}"          # 校验失败转成模型可读的文本

messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
reply = (await asyncio.to_thread(
    client.chat.completions.create,
    model=DEEPSEEK_MODEL, messages=messages, temperature=0.2,
    extra_body={"thinking": {"type": DEEPSEEK_THINKING}},
)).choices[0].message.content or ""
return (reply, 1)
```

几个值得注意的工程点：

- `asyncio.to_thread` 把 OpenAI 的**阻塞**调用包成非阻塞，避免卡死 FastAPI 事件循环。
- assistant 消息里 `tool_calls` 必须**原样回传**（`tc.model_dump()`），格式不对 API 会拒收。
- 工具执行结果以 `role: "tool"` 回填，靠 `tool_call_id` 关联；下一次请求模型基于真实结果生成最终答复。
- 所有异常（参数校验失败、HA 调用失败、网络错误）都转成**面向模型的中文文本**，模型读得懂就能向用户解释，而不是抛给前端一个裸 500。

#### 本地验证：curl 两个端点

FastAPI 暴露 `/health` 和 `/chat` 两个端点。先起服务，再 curl：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000

curl http://127.0.0.1:8000/health
# {"status":"ok","model":"deepseek-v4-flash","thinking":"disabled","ha_connected":true}

curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "打开客厅灯"}'
# {"reply":"好的，已为你打开客厅灯。","tool_calls":1}
```

`/health` 里的 `ha_connected` 来自 `HomeAssistantClient.ping()`，一上来就能确认 HA 侧认证是否配好。`tool_calls: 1` 表示这一轮真的执行了一次工具调用，是排查「模型是不是在瞎答」的第一信号。

### 6.3 工具层：tools.py 的 Home Assistant REST 封装

工具层把 HA REST API 封装成 `HomeAssistantClient`（httpx.AsyncClient），只暴露 `get_state` / `call_service` / `ping` 三个方法。[深度收集 §4](../02_deep_research.md) [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)

```python
self._headers = {
    "Authorization": f"Bearer {token}",   # 注意：Bearer 后必须有一个空格
    "Content-Type": "application/json",
}

async def call_service(self, domain, service, data=None):
    resp = await client.post(
        f"{self.base_url}/services/{domain}/{service}",
        headers=self._headers, json=data or {},
    )
    return self._handle(resp)             # 成功返回变更后的 state JSON 数组
```

对照官方 REST API 的映射关系：

| Agent 方法 | HTTP 请求 | 作用 |
|------------|-----------|------|
| `get_state(entity_id)` | `GET /api/states/{entity_id}` | 查询单个实体当前状态 |
| `call_service(domain, service, data)` | `POST /api/services/{domain}/{service}` | 调用服务，返回变更后的 state 数组 |
| `ping()` | `GET /api/` | 认证探活，供 `/health` 用 |

两个容易翻车的细节：`Authorization` 是 `Bearer ` 加 token，`Bearer` 后**有空格**，拼错直接 401；调用服务的请求体里必须带 `entity_id`（6.2 里 `control_device` 用 `data.setdefault("entity_id", eid)` 补上）。错误统一抛 `RuntimeError`，message 里带 HA 状态码和响应摘要（最多 500 字符），这样工具结果对模型足够友好——模型能直接读出「401 认证失败」并告诉用户。

### 6.4 实体映射：entity_map.yaml + rapidfuzz 模糊匹配

用户不会说 `light.living_room`，他说「客厅灯」。实体映射层负责把口语别名解析成 HA 实体 ID，避免让模型去猜 entity 命名。[深度收集 §4](../02_deep_research.md)

```yaml
entities:
  - entity_id: light.living_room
    name: 客厅灯
    aliases: [客厅主灯, living room light, living_room]
    domain: light
  - entity_id: climate.bedroom_ac
    name: 卧室空调
    aliases: [空调, bedroom ac]
    domain: climate
```

`EntityResolver.resolve()` 按固定顺序解析（完整逻辑见 `agent/entity_map.py`）：

1. **精确命中 entity_id**：`light.living_room` 直接命中，走 `_by_id` 字典。
2. **精确命中 name / alias**：大小写不敏感，走 `_label_to_id`。
3. **长得像 entity_id 但不在映射表**：直接返回 `None`，不再模糊——避免把乱串文本当实体匹配。
4. **rapidfuzz 模糊匹配**：对 name/alias 标签列表用 `WRatio` 打分，`score_cutoff=80`，低于阈值不认。

第 3 步「先拦截、再模糊」的顺序很关键：它既容忍「客厅的灯」这种口语变体，又不会把「客厅」这种合法前缀误匹配成别的实体。

映射表还反向供给提示词：`run_agent` 里 `SYSTEM_PROMPT.format(entities="、".join(resolver.list_entities()))` 把可用实体清单注入系统提示，并明确要求「提到设备时优先用用户说法，工具会自动解析」。模型负责说人话，解析交给确定性代码——这条分工是全章的核心思想。

### 6.5 安全设计：把「口子」收窄成「接口」

把设备控制权交给 LLM，最怕的不是模型笨，而是模型被**越权诱导**（prompt injection）或**手滑控制错误设备**。项目里的安全设计分层如下：[深度收集 §4](../02_deep_research.md)

- **专用受限 HA 用户 + LLAT**：为 Agent 单独建一个 HA 用户，用它生成 Long-Lived Access Token，不要用管理员主号。注意 LLAT 默认无 scope，**等同全管理员权限**，所以「受限用户」才是真正的隔离手段——让这个用户只能看到、控制这一批设备。`.env` 里的 `HA_TOKEN` 就是它。
- **函数名白名单**：模型返回的工具名只有出现在 `TOOL_HANDLERS` 里的才会被 `_validate_tool_call` 放行，其余一律拒绝。模型最多「提议」，执行权永远在应用层。
- **运行时参数校验**：`_validate_tool_call` 检查 `entity_id` 必须在映射表里、`service` 必须在白名单、`params` 必须是对象；`domain` / `service` 双重白名单在 `control_device` 里再查一遍。
- **控制前查 state（生产必加）**：当前骨架里 `control_device` 直接调 `call_service`。生产版本应在调用前先 `get_state`，若 `state` 为 `unavailable` / `unknown` 则拒绝并提示「设备离线」，避免对离线设备盲发指令。`get_device_state` 已经提供查询能力，把它接到控制路径即可。
- **brightness 量纲 0-255**：`params` 是透传给 HA 的，`light.turn_on` 的 `brightness` 量纲是 **0-255**（不是百分比 0-100）。模型常会输出 50 这种百分数，建议在工具层统一做量纲换算或钳制。
- **密钥不烤进镜像**：`.env` 用 `chmod 600` 保护、`.gitignore` 排除；`Dockerfile` 只 `COPY main.py tools.py entity_map.py entity_map.yaml ./`，密钥靠 `-e` / `--env-file` 注入。`.env.example` 里 `HA_TOKEN` / `DEEPSEEK_API_KEY` 都是占位符。

> [!warning] LLAT 没有 scope 概念
> LLAT 只是一个 token 字符串，默认拥有该用户全部权限。别因为「看起来是个 token」就放松警惕——隔离靠「专用受限 HA 用户」，不靠 token 本身。

容器化与依赖（完整文件见 `agent/` 目录）：

| 文件 | 作用 |
|------|------|
| `requirements.txt` | `fastapi` / `uvicorn[standard]` / `openai` / `httpx` / `pyyaml` / `python-dotenv` / `rapidfuzz` |
| `Dockerfile` | `python:3.12-slim`，`uvicorn main:app --host 0.0.0.0 --port 8000`，`EXPOSE 8000` |
| `.env.example` | `DEEPSEEK_MODEL=deepseek-v4-flash`、`DEEPSEEK_THINKING=disabled`、`HA_BASE_URL=http://127.0.0.1:8123` |

配合第 3 章的 `docker-compose`，Agent 以 sidecar 形式跑在 `network: host` 下，容器内直接 `127.0.0.1:8123` 连 HA，`depends_on: homeassistant: condition: service_healthy` 保证 HA 先就绪。

### 本章小结

- DeepSeek 2026-08 关键事实：模型名是 `deepseek-v4-flash`（旧名 2026-07-24 停用），`tool_choice` 必须用 `"auto"`，MVP 用 `extra_body` 关掉 thinking，否则工具轮次会踩 `reasoning_content` 回传的 400。
- 智能体主循环 = N=1：模型最多提议一次工具调用，应用层校验、执行、回填，再请求一次拿最终答复；不做多步规划。
- 能力边界用白名单收窄：`TOOL_HANDLERS` 函数白名单 + `ALLOWED_DOMAINS` / `ALLOWED_SERVICES` + 运行时参数校验，模型只能「提议」，执行权在代码。
- 口语 → entity 的解析交给确定性的 `entity_map.yaml` + rapidfuzz（WRatio，score_cutoff=80），不交给模型猜。
- 安全靠「专用受限 HA 用户 + LLAT + 白名单 + 控制前查 state」，密钥 `.env` chmod 600、不入镜像；生产必补 unavailable/unknown 拦截与 brightness 量纲换算。

---

下一章进入「场景」：HA 的自动化引擎。你会看到怎么把回家、离家、睡眠这些场景模板化成 packages 与 Blueprint，让整套系统不止会「听指令」，还会「自己判断该做什么」。
