# 第 4 章：Config Flow 配置流程

第 3 章我们把 `manifest.json` 骨架和 `__init__.py` 搭好了，集成能被 HA 识别并加载。但现在的它还是一个「哑配置」集成——用户只能靠 `configuration.yaml` 写死配置。这一章我们用 Config Flow（配置流程）给它装上「设置界面」：用户在「设置 → 设备与服务 → 添加集成」里填写表单，HA 校验通过后生成一条 config entry，整个集成才真正可配置、可复用。为什么这章值得放慢速度？因为**表单 + 异常映射 + 唯一性**这三件事，是后续每一章（设备接入、数据轮询、测试）的地基。

> [!tip] 大白话
> 把 Config Flow 想成「门禁卡申请流程」。用户填一张申请表（表单），系统校验信息没问题后，发一张门禁卡（config entry）。这张卡就是 HA 记住「这个集成在这台设备上配置过」的凭证——以后每次加载都靠它。没有这张卡，集成就只是个「能加载但没法被用户配置」的空壳。

## 4.1 让 config flow 生效：两处开关

Config flow 不是魔法，它需要两处配合才能被 HA 唤起：

1. `manifest.json` 里加一行 `"config_flow": true`，告诉 HA「我这个集成支持 UI 配置」。
2. 新增 `custom_components/<domain>/config_flow.py`，在里面定义一个继承 `ConfigFlow` 的类，并把类属性 `domain` 指向我们的 `DOMAIN`。

目录结构上，它和其他文件平级：

```text
custom_components/hello_world/
├── __init__.py
├── const.py
├── config_flow.py   # 本章主角
├── manifest.json
└── strings.json
```

### 最小 config_flow.py 骨架

```python
from homeassistant import config_entries

from .const import DOMAIN


class HelloWorldConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1
    MINOR_VERSION = 1
```

几个关键点：

- **`config_entries.ConfigFlow` 是基类**：HA 在「设置 → 设备与服务 → 添加集成」里点到你的集成时，会实例化这个类，然后调用它的各个 `async_step_*` 方法。你写的不是「按钮点击逻辑」，而是「每一步显示什么表单、填完怎么处理」的声明。
- **`domain = DOMAIN`**：把流程绑定到你的集成 domain，与 manifest 的 `domain`、目录名三方必须一致。
- **`VERSION` / `MINOR_VERSION`**：默认都是 1。`VERSION` 是配置数据结构的主版本，当你的集成升级导致 `data` 结构不兼容时，把主版本 +1 并实现 `async_migrate_entry` 做迁移；`MINOR_VERSION` 是较新 HA 引入的次版本号，用于不破坏兼容的小改动。上手阶段记住「有这两个属性、保持默认」即可。

> [!note] 素材对齐
> 官方脚手架 `python3 -m script.scaffold integration` 选 config flow 时，会自动生成 `config_flow.py` + `strings.json` 并改写 manifest——正好就是我们这一章要写的三个文件 [官方开发环境文档](https://developers.home-assistant.io/docs/development_environment/)。

## 4.2 async_step_user：表单流程的两段式

`async_step_user` 是用户进入流程后看到的**第一个步骤**（step）。它的写法遵循一个「两段式」套路：

- **第一次进入**：`user_input` 为 `None`，此时只是**展示表单**，调用 `async_show_form`。
- **用户填完提交**：`user_input` 带着数据进来，此时**校验 + 建条目**，成功则 `async_create_entry`，失败则带着 `errors` 重新 `async_show_form`。

表单用什么描述？**voluptuous schema**（HA 内部大量使用的 Python 校验库，惯例别名 `vol`）。它声明「这个表单有哪些字段、哪些必填、什么类型」。

官方示例 `detailed_hello_world_push` 的表单就是这个模式（稍作裁剪以便聚焦）：

```python
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CannotConnect(HomeAssistantError):
    """无法连接到设备时抛出。"""


class InvalidHost(HomeAssistantError):
    """主机地址非法时抛出。"""


DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def validate_input(hass, data):
    """真正去连一次设备，连不上就抛自定义异常。"""
    if not looks_like_hostname(data[CONF_HOST]):  # 示意性检查
        raise InvalidHost
    hub = YourHubClass(hass, data[CONF_HOST], data[CONF_USERNAME], data[CONF_PASSWORD])
    if not await hub.authenticate():
        raise CannotConnect
    # 返回给 async_create_entry 用的信息
    return {"title": hub.name, "unique_id": hub.mac}


class HelloWorldConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidHost:
                errors["host"] = "invalid_host"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
```

这里还有两个「潜规则」值得记下（完整可运行版本见官方示例仓库 [example-custom-config](https://github.com/home-assistant/example-custom-config) 的 `detailed_hello_world_push`）：

- **`step_id` 必须与方法名对应**：`async_step_user` 里的表单 `step_id="user"`，因为 HA 就是按「`async_step_` + step_id」去找下一个方法。方法名改错了，流程会找不到下一步。
- **`async_show_form` 的核心参数**：`step_id`（对应哪个方法）、`data_schema`（表单长什么样）、`errors`（要不要回显错误）、`description_placeholders`（可动态填充 description 里的 `{变量}`）。上手阶段前三者够用。

流程走一遍：

1. **schema 先做类型校验**：`vol.Required(CONF_HOST): str` 表示 host 必填且必须是字符串。类型不对，voluptuous 在进入 `async_step_user` 之前就会拦下，并在对应字段下显示错误。
2. **`validate_input` 做真实校验**：类型对不代表能连上，这里真的去连一次设备。这是整个流程里唯一可能耗时的环节，所以是 `async` 的。你集成的 API 客户端 `YourHubClass` 按 HA 架构铁律应封装在独立 PyPI 库（第 6 章细讲），这里先用占位。
3. **异常映射**：连不上抛 `CannotConnect` → 记到 `errors["base"]`；主机非法抛 `InvalidHost` → 记到 `errors["host"]`。记到哪个键，决定了错误显示在哪里。
4. **兜底**：任何没预料到的异常，`except Exception` 记录完整堆栈日志，然后统一显示「未知错误」，绝不裸奔给用户看。
5. **成功**：`async_create_entry(title=..., data=user_input)` 生成 config entry，流程结束，HA 跳回「设备与服务」并显示新条目。

> [!tip] 大白话
> 把表单校验想成「门卫核验申请材料」。第一步 schema 是「查证件类型对不对」——要求填手机号，结果填了邮箱，当场打回；第二步 `validate_input` 是「查这证件能不能真的进门」——号码格式对，但系统里查无此人，也打回。字段级错误是「申请表上具体哪一行划红线」，整体错误是「整张表盖章退回，不针对某一栏」。

## 4.3 errors 回显：字段级 vs 整体 vs 兜底

`errors` 是一个字典，它有三种「落点」：

| 落点 | 写法 | 显示位置 | 典型场景 |
|------|------|----------|----------|
| 字段级 | `errors["host"]` | 表单中 host 输入框下方 | 这个字段本身有问题（如主机地址非法） |
| 整体 | `errors["base"]` | 表单顶部通用错误区 | 无法连接、认证失败这类整体性问题 |
| 兜底 | `errors["base"] = "unknown"` | 表单顶部 | 没预料到的异常，不暴露细节 |

「字段级 vs 整体」的选择标准：**错误能否归因到某一个输入框？** 能就绑字段，不能就绑 `base`。比如「密码错误」绑到 `errors["password"]`（让用户知道去改哪里），而「连不上服务器」跟哪个字段都无关，绑 `base` 最合理。

兜底 `"unknown"` 的意义是**不向用户泄露内部细节**：未知异常多半是代码 bug 或意外输入，直接展示堆栈既难看又暴露实现；正确做法是 `_LOGGER.exception` 把完整堆栈写进日志（开发时一眼定位），界面上只给一句中性的「未知错误」，用户可以去日志里排查。

错误的具体文案不写在代码里，而是写在外层 `strings.json`（下节）。代码里只放一个**错误键**（如 `"cannot_connect"`），文案由 HA 按键名去翻译文件里查。**键必须两边对齐**——代码抛了 `"invalid_host"`，`strings.json` 里没有这个键，界面上就会显示成原始键名，用户看到一串英文标识符，体验很差。

## 4.4 strings.json：把文案搬出去

`strings.json` 放在 `custom_components/<domain>/strings.json`，结构对应 config flow 的三个区块：

```json
{
  "config": {
    "step": {
      "user": {
        "title": "连接 Hello World 设备",
        "description": "请输入设备的连接信息",
        "data": {
          "host": "主机地址",
          "username": "用户名",
          "password": "密码"
        }
      }
    },
    "error": {
      "cannot_connect": "无法连接到设备",
      "invalid_host": "主机地址无效",
      "unknown": "未知错误"
    },
    "abort": {
      "already_configured": "该设备已配置"
    }
  }
}
```

- `config.step.user.data`：表单里每个字段的**显示标签**（键是字段名）。完整的文案与翻译规则见官方 [Config Flow 文档](https://developers.home-assistant.io/docs/core/integration/config_flow/)。
- `config.error`：错误键 → 用户可见文案。代码里 `errors["base"] = "cannot_connect"`，这里的 `"cannot_connect"` 就是查表的键。
- `config.abort`：流程被**中止**时的文案（如「该设备已配置」，配合唯一性使用，见下节）。

> [!note] 进阶提示
> 想要多语言，翻译由 `script.translations develop` 生成到 `translations/*.json`；公共文案可用 `[%key:common::config_flow::...%]` 引用。上手阶段先维护 `strings.json` 一份即可。

## 4.5 唯一性：async_set_unique_id + _abort_if_unique_id_configured

同一个设备被用户配置两遍，会出现重复条目、重复实体。Config Flow 提供标准防重机制：**唯一 ID + 查重中止**。在 `async_create_entry` 之前补两行：

```python
            else:
                await self.async_set_unique_id(info["unique_id"])  # 用 MAC，不是 IP
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)
```

- **`async_set_unique_id`**：给这条配置绑定一个全局唯一标识。HA 用它在 entity registry / device registry 之间关联同一台设备。
- **`_abort_if_unique_id_configured()`**：如果这个 unique_id 已经配置过，立即中止本次流程，并显示 `strings.json` 里 `config.abort.already_configured` 的文案。它还可以带 `updates=` 参数，在检测到重复时顺手把已有条目更新为新提交的数据——适合「设备信息变了、但仍是同一台」的场景。

**unique_id 选什么，是本章最容易踩的坑：**

- 禁止用 IP、设备名。IP 会变（DHCP 换地址），设备名可以重复，都不能作为稳定身份。
- 用 MAC 地址、序列号、芯片 ID 这类**出厂唯一且不变**的标识。

> [!tip] 大白话
> 把 unique_id 想成「门禁卡上的唯一编号」。编号是出厂烙上去、一辈子不变的；而 IP 就像「今天坐哪个工位」——换工位（换 IP）不影响你是谁。系统靠编号认设备：编号一样就说明「这张卡已经办过了」，直接告诉你「已配置」，不让重复办。

## 4.6 Options Flow：data 不可变，options 可变

配置条目创建后，`data` 里存的是「安装时的固定信息」（主机地址、账号等）。但用户可能之后想改一些**偏好**（如轮询频率、显示单位）。这就是 Options Flow 的舞台。

**`data` vs `options` 的分工：**

| 维度 | `data` | `options` |
|------|--------|-----------|
| 可变性 | 安装后不可变 | 用户随时可改 |
| 存放内容 | 连接凭证、设备地址 | 偏好、开关、频率等 |
| 修改方式 | 需 reconfigure/删除重配 | 设置界面里的「选项」 |
| 典型例子 | host、username、password | 更新间隔、显示单位 |

Options Flow 的骨架：在 config flow 类里声明一个静态方法返回 `OptionsFlow` 子类；OptionsFlow 的**第一个 step 恒为 `async_step_init`**。

```python
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.schema_config_entry_flow import add_suggested_values_to_schema

from .const import CONF_SCAN_INTERVAL, DOMAIN


class HelloWorldOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            # options 保存后，用户即可通过 add_update_listener 感知变更
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(CONF_SCAN_INTERVAL): cv.positive_int,
            }
        )
        return self.async_show_form(
            step_id="init",
            data_schema=add_suggested_values_to_schema(schema, self.config_entry.options),
        )


class HelloWorldConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        """让 HA 知道选项流程从哪个类实例化。"""
        return HelloWorldOptionsFlow(config_entry)
```

- `async_get_options_flow` 是 config flow 类里的**静态方法**，返回一个 OptionsFlow 实例。想让 options 变更后集成自动重新加载，可以让 OptionsFlow 继承 `OptionsFlowWithReload` 基类，省去手写 `add_update_listener` 的样板（`OptionsFlow`/`ConfigEntry` 的完整语义见官方 ConfigEntry 文档 [官方 Config Flow 文档](https://developers.home-assistant.io/docs/core/integration/config_flow/)）。
- `add_suggested_values_to_schema(schema, self.config_entry.options)`：把**当前已保存的 options** 预填进表单，用户看到的是「当前值」而不是空白。
- 保存后 `options` 变了，HA 会在条目上触发 `add_update_listener`；集成里用 `entry.async_on_unload(entry.add_update_listener(处理函数))` 监听并处理（如重新加载）。

> [!tip] 大白话
> 把 options 想成「拿到门禁卡之后，在前台登记的可调偏好」。`data` 是发卡时写死的信息（工号、所属部门），员工自己改不了；`options` 是卡上可以现场调整的偏好（比如门禁生效时段），随时找前台改，改完立刻生效。

## 4.7 异常语义：ConfigEntryNotReady vs ConfigEntryAuthFailed

config entry 创建后，HA 会调用你集成的 `async_setup_entry`（第 5、6 章会写）。这一步如果失败，抛什么异常决定了后续行为。**这两个异常是本章必须分清的一对：**

| 异常 | 语义 | 触发行为 | 类比 |
|------|------|----------|------|
| `ConfigEntryNotReady` | 设备/服务暂时不可用（刚开机、网络抖动） | 条目进入 `SETUP_RETRY`，按指数退避自动重试：等待 `min(2^次数 × 5, 上限)` 秒后再试，不是硬失败 | 门禁系统还在重启，过几秒再刷一次卡 |
| `ConfigEntryAuthFailed` | 凭证失效（token 过期、密码被改） | 触发 reauth 重新认证流程，把用户引导回「重新登录」 | 卡被吊销了，需要重新办授权 |

为什么这个区分很重要？因为**用错会让用户体验崩掉**：

- 把 `ConfigEntryAuthFailed` 误抛成 `ConfigEntryNotReady` → HA 会无限指数退避重试，但重试再多次也救不回失效的 token，白白消耗资源。
- 把临时故障误抛成 `ConfigEntryAuthFailed` → 用户被频繁拉去重新登录，其实过几秒网络就恢复了。

> [!tip] 大白话
> 把这两个异常想成两种「刷不开门」的情况。`ConfigEntryNotReady` 是「门禁系统刚开机还在自检」——系统知道过会儿就好，过几秒自动再试一次，不用你操心；`ConfigEntryAuthFailed` 是「你卡里的权限被撤了」——系统再试也没用，只能把你带到前台重新办授权。一个等自动修复，一个必须人工介入。

## 4.8 reauth / reconfigure：点到为止

两个更进阶的流程，本笔记只让你知道「存在」：

- **reauth**：凭证失效后，重新走一遍「登录/授权」来刷新凭证。
- **reconfigure**：让用户重新配置某个条目的 `data`（比如设备搬了新地址）。

官方 2024 年后的写法是用 helper 获取当前条目：`self._get_reauth_entry()` / `self._get_reconfigure_entry()`，不要再手动去 `self.context["entry_id"]` 里翻；配置 `unique_id` 后加 `_abort_if_unique_id_mismatch()` 防止改错设备。**OAuth2 的完整授权流程不在本笔记范围内**，等真正遇到再查官方文档即可。

## 4.9 本章小结

- Config Flow 由 `config_flow.py` 里继承 `config_entries.ConfigFlow` 的类承载，`manifest.json` 须设 `"config_flow": true`，二者缺一不可。
- 表单流程是「两段式」：`async_step_user(user_input=None)` 先展示表单，提交后校验，成功 `async_create_entry`，失败带 `errors` 重显表单。
- 错误映射分三种落点：字段级 `errors["字段"]`、整体 `errors["base"]`、兜底 `except Exception` + `"unknown"`；文案统一放 `strings.json`。
- 唯一性用 `async_set_unique_id` + `_abort_if_unique_id_configured()`，unique_id 选 MAC/序列号这类稳定标识，**禁用 IP/设备名**。
- `data` 安装后不可变、`options` 可变；Options Flow 首步恒为 `async_step_init`，用 `add_suggested_values_to_schema` 预填当前值。
- `ConfigEntryNotReady` 自动指数退避重试，`ConfigEntryAuthFailed` 触发 reauth——临时故障与凭证失效要分清。

下一章我们进入实体世界：把 config entry「接上电」，用 `async_forward_entry_setups` 装载 sensor 平台，写第一个真正会显示状态的 sensor 实体。到那时你会发现，这一章做好的 config entry，正是下一章实体注册的入口凭证。
