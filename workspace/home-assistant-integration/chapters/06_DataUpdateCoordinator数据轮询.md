# 第 6 章 DataUpdateCoordinator 数据轮询

第 5 章我们把 sensor 实体比作「柜台展示员」，让它们把数据摆上货架。但一个关键问题悬而未决：**货架上的货从哪来？** 实体属性 getter 是禁止做网络请求的，如果让每个实体各拉各的数据，既重复又混乱。这一章解决数据来源问题：用一个 `DataUpdateCoordinator` 统一轮询外部 API，把结果缓存在内存里，所有实体共享同一份。这是 HA 集成架构中最关键的一环，也是本笔记的两大重点之一——它决定你的集成是「每家柜台各跑一趟进货」还是「一个仓库统一收货」。

## 6.1 问题：实体不能自己发请求

回顾第 5 章，实体读取数据的正确姿势是 `_attr_` 类属性或属性 getter 返回内存里的值，例如 `self.coordinator.data`。官方异步纪律明确规定：**属性 getter 只能读内存，不能做 I/O**。原因很现实——HA 的事件循环是单线程的，getter 里一旦出现网络请求，就会阻塞整个 HA 的响应，其他所有集成都会被拖住（[官方 asyncio_working_with_async 文档](https://developers.home-assistant.io/docs/dev_101_async/)）。

那数据该由谁来拉？最笨的办法是每个实体在 `update()` 里各发一次请求。假设你有 5 个实体，`update_interval` 设为 30 秒，那么每 30 秒就会对同一个 API 发出 5 次完全相同的请求——浪费带宽，也容易被对方限流。更糟的是，错误处理会散落在每个实体里，你无法统一应对「认证失效」「限流」这类全局性故障。

`DataUpdateCoordinator` 正是为解决这个问题而生的：它是 HA 内置的「数据轮询协调器」，负责按固定间隔拉取一次数据、缓存到 `coordinator.data`，再通知所有订阅的实体来读缓存（[官方 fetching_data 文档](https://developers.home-assistant.io/docs/integration_fetching_data/)）。第 5 章提到的 `CoordinatorEntity` 基类，就是实体端接入 coordinator 的标准方式。

> [!tip] 大白话
> 把 Coordinator 想成**仓库统一收货员**：外部 API 是供应商，实体是各个柜台。没有收货员时，每个柜台都得自己跑到门口接货，来一车货就重复接 N 遍；有了收货员，一车货到后他搬进仓库、分给所有柜台，每个柜台只需去仓库看一眼自己那份。所以，多个实体共享一份数据，网络请求只发一次，错误也由收货员统一处理。

理解 coordinator 的关键，是看懂一个完整轮询周期里发生的事：

1. 到达 `update_interval`（比如 30 秒），coordinator 调用 `_async_update_data`。
2. **成功**：返回值写入 `self.data`，`last_update_success` 置为 `True`，然后通知所有订阅的实体「数据更新了，来读缓存」。`CoordinatorEntity` 收到通知后自动刷新状态。
3. **失败**：`last_update_success` 置为 `False`，`CoordinatorEntity` 会把实体的 `available` 翻成 `False`——这正是第 5 章提到的「`CoordinatorEntity` 自带 Mark unavailable 逻辑」，实体端不需要写任何代码，故障时界面自动变不可用。

`last_update_success` 这个标志，就是实体「是否可用」的数据来源。所以只要 `_async_update_data` 写好，实体侧几乎不用关心轮询的成败细节。

## 6.2 coordinator.py 骨架

按第 3 章的文件组织约定，coordinator 单独放一个 `coordinator.py`。核心是继承 `DataUpdateCoordinator`，重写 `_async_update_data`——它会在每个轮询周期被调用，返回值会存进 `coordinator.data`，供所有实体读取。

```python
# coordinator.py
"""数据轮询协调器：统一拉取外部 API 数据，缓存后分发给各实体。"""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from my_cloud_api import MyApiClient          # 独立 PyPI 库（见 6.6）
from my_cloud_api.errors import (             # 库自带的自定义异常
    ApiAuthError,
    ApiRateLimitError,
)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MyCoordinator(DataUpdateCoordinator[dict]):
    """统一轮询外部 API，把数据缓存到 coordinator.data。"""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, api: MyApiClient
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),  # 每 30 秒轮询一次
        )
        self.api = api

    async def _async_setup(self) -> None:
        """一次性初始化，首次刷新期间自动调用（HA 2024.8+）。"""
        # 只做一次的事放这里：拿设备信息、建立连接、探测能力等
        await self.api.async_fetch_device_info()

    async def _async_update_data(self) -> dict:
        """每次轮询调用：拉数据并返回，存进 coordinator.data。"""
        try:
            # 网络请求必须包在超时里，防止 API 卡死整个轮询
            async with asyncio.timeout(10):
                raw = await self.api.async_fetch_sensor_data()
        except ApiAuthError as err:
            # 认证失效：触发 reauth，而不是普通重试
            raise ConfigEntryAuthFailed("API 认证失败，需要重新授权") from err
        except ApiRateLimitError as err:
            # 限流：告诉 HA 60 秒后再试
            raise UpdateFailed("请求过于频繁") from err
        # 注意：asyncio.TimeoutError 和 aiohttp.ClientError
        # 已被 coordinator 内部处理，这里无需捕获
        return raw
```

要点逐一说明：

- **`asyncio.timeout(10)`**：把网络请求包裹在 10 秒超时里，是官方文档的标准做法。API 卡住时，轮询不会无限期阻塞。
- **返回值即数据**：`_async_update_data` 的返回值会成为 `self.data`，实体只读它，绝不自己发请求。
- **不要在 `_async_update_data` 里直接做业务**：它只负责「把原始数据拿回来」，加工、建模交给独立库。

运行后你会在 `home-assistant.log` 里看到 coordinator 自己的轮询记录（Debug 级别）：

```text
Updating my_cloud data                  # 开始轮询
Finished fetching my_cloud data in 0.340 seconds   # 成功，耗时 0.34 秒
```

如果 API 一直失败，日志会显示 `Unable to fetch my_cloud data: ...`，同时实体在界面上变为不可用。这套日志是 coordinator 自动打的，不用你自己写——这也是为什么构造时要把 `_LOGGER` 传进去。

## 6.3 异常语义：把错误翻译成 HA 听得懂的语言

coordinator 的价值不只在于「少发请求」，更在于**统一错误语义**。HA 对不同的异常有不同的反应，你必须把 API 库抛出的错误翻译成 HA 认识的那几种（异常映射参考官方维护者蓝本 [ludeeus/integration_blueprint](https://github.com/ludeeus/integration_blueprint)）：

| 情况 | 抛出的异常 | HA 会怎样 |
|------|-----------|-----------|
| 认证失败（token 失效等） | `ConfigEntryAuthFailed` | 触发 reauth 重授权流程，不自动重试 |
| 一般业务错误 | `UpdateFailed` | 实体标记为不可用，下个周期再试 |
| 限流（429 等） | `UpdateFailed(retry_after=60)` | 等待 60 秒后再重试 |
| 超时 / 网络层错误 | 不捕获 | `asyncio.TimeoutError` / `aiohttp.ClientError` 由 coordinator 内部处理 |

两个易错点要特别记牢：

- **`ConfigEntryAuthFailed` 和 `ConfigEntryNotReady` 别用反**。第 4 章讲过：`NotReady` 是「暂时起不来，指数退避自动重试」，`AuthFailed` 是「登录已失效，需要用户重新授权」。认证失败时如果抛了 `NotReady`，HA 会一直空转重试，用户却得不到重新登录的提示——这是新手最常见的坑之一（素材 三.常见坑 #5）。
- **超时和网络错误不用你管**。`asyncio.TimeoutError`、`aiohttp.ClientError` 由 coordinator 内部处理并转为实体不可用，你不需要（也不应该）在 `_async_update_data` 里捕获它们。你只需要处理**业务语义**层面的错误。

为什么「限流」值得单独设一个 `retry_after=60`？因为限流通常是**可预期的**：API 明确告诉你「60 秒内别再来了」。如果你不加 `retry_after`，coordinator 会按原 `update_interval`（比如 30 秒）继续撞上去，每次都吃一个 429，白白浪费。带上 `retry_after`，coordinator 会尊重这个冷却期，到点再试。

一个完整的认证失败场景是这样流转的：集成运行中，云端把 token 吊销了 → 下一次轮询 `async_fetch_sensor_data` 抛 `ApiAuthError` → 你把它翻译成 `ConfigEntryAuthFailed` → HA 触发 reauth，用户在 UI 上重新授权 → 授权成功后配置条目重载、coordinator 重建、一切恢复正常。如果没有这一步翻译，用户只会在日志里看到「数据获取失败」，不知道是该重新登录——这就是统一异常语义的价值。

## 6.4 接线：一个 coordinator + 多个实体

coordinator 写好后，要在 `__init__.py` 的 `async_setup_entry` 里把它建起来，并接入各实体平台（官方 [fetching_data](https://developers.home-assistant.io/docs/integration_fetching_data/) 的接线方式）：

```python
# __init__.py（async_setup_entry 片段）
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client

from my_cloud_api import MyApiClient
from .const import DOMAIN
from .coordinator import MyCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # 1. 用 entry 配置建好 API client（独立库）
    api = MyApiClient(
        host=entry.data["host"],
        token=entry.data["token"],
        session=aiohttp_client.async_get_clientsession(hass),  # 复用 HA 的会话
    )

    # 2. 只建一个 coordinator，所有实体共享
    coordinator = MyCoordinator(hass, entry, api)

    # 3. 首次刷新：失败会抛 ConfigEntryNotReady，HA 自动重试
    await coordinator.async_config_entry_first_refresh()

    # 4. 存到 entry.runtime_data（见 6.5）
    entry.runtime_data = coordinator

    # 5. 把 sensor 平台接进来
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
```

这里的顺序是刻意安排的：**先 `first_refresh`，再 `async_forward_entry_setups`**。如果首次拉取失败（比如 API 还没就绪），`async_config_entry_first_refresh()` 会抛 `ConfigEntryNotReady`，`async_setup_entry` 中止，HA 按指数退避自动重试——不会先加载一堆读不到数据的实体。

实体端用 `CoordinatorEntity` 订阅，并用 `context=idx` 区分自己是哪一路数据：

```python
# sensor.py（片段）
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MyCoordinator


class MySensor(CoordinatorEntity[MyCoordinator]):
    """订阅 coordinator 的实体：只读 coordinator.data，不自己发请求。"""

    def __init__(self, coordinator: MyCoordinator, idx: str) -> None:
        super().__init__(coordinator, context=idx)  # context 标识这一路数据
        self.idx = idx

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data
        if data is None or self.idx not in data:
            return None
        return data[self.idx]["value"]


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator: MyCoordinator = entry.runtime_data
    # 按数据里的每个条目生成一个实体
    async_add_entities(
        MySensor(coordinator, idx) for idx in coordinator.data
    )
```

两个行为细节值得留意（素材 一.5）：

- **`update_interval` 只在有订阅者时才轮询**。HA 会跟踪 coordinator 的订阅者数量，实体全部被移除、无人订阅后，轮询自动停止，不再产生无谓的网络请求。
- **`_async_setup` 做一次性初始化**（HA 2024.8+ 新增）。像「获取设备信息」这类只需做一次的事放在 `_async_setup` 里，它会在 `async_config_entry_first_refresh()` 期间被自动调用，并和 `_async_update_data` 共享同一套错误处理——初始化时认证失败同样触发 reauth，初始化失败同样走 `ConfigEntryNotReady` 重试。

`context=idx` 是这套共享机制的关键细节。多个实体订阅同一个 coordinator，HA 需要知道「这次数据更新该通知谁」。给每个实体传一个不同的 `context`（比如数据里的传感器 id），coordinator 就能按上下文区分订阅者；而不传 `context` 的实体则订阅「全部数据」。你可以在 `coordinator.async_contexts()` 里看到当前所有活跃订阅者——这也正是「只在有订阅者时才轮询」的实现基础。轮询到的数据回到 `coordinator.data` 后，每个实体读自己 `idx` 对应那一份，互不干扰。

> [!tip] 大白话
> 把 `update_interval` 想成收货员的工作节奏：收货员只在**有人来看货时才去收货**。实体订阅 coordinator，相当于登记「我每天会来取货」；如果所有实体都被移走、没有订阅者了，收货员就不再空跑，省下每次往返的运费。`_async_setup` 则像开业前的仓库盘点——只做一次，之后正常收货。

## 6.5 entry.runtime_data：coordinator 该放哪

旧式写法是把 coordinator 塞进全局字典 `hass.data[DOMAIN]`：

```python
# 旧写法：字符串键 + 全局字典，类型全靠自觉
hass.data[DOMAIN] = coordinator
# 另一处取用
coordinator = hass.data[DOMAIN]
```

新版官方蓝本推荐改用 **`entry.runtime_data`**（素材 二.ludeeus/integration_blueprint）：

```python
# 新写法：跟着 config entry 走，类型可标注
entry.runtime_data = coordinator
# 平台里取用
coordinator: MyCoordinator = entry.runtime_data
```

后者更好的原因：一是**类型安全**，可以标注 `MyCoordinator`，IDE 和静态检查都能帮你兜底；二是**不污染全局字典**，不用担心字符串键拼错、多设备实例互相覆盖；三是语义清晰，coordinator 本来就是「这个配置条目私有的运行数据」，放在 entry 上名正言顺。

多实例场景下这个优势更明显。假如一个集成支持配置两个网关，旧写法 `hass.data[DOMAIN]` 只能存一份，你得再套一层 `{entry_id: coordinator}` 字典才能区分；而 `entry.runtime_data` 天然跟着 entry 走，每个配置条目一份，平台代码里直接 `entry.runtime_data` 取到的就是「当前这个条目」的 coordinator，不会拿错。第 5 章提到的动态设备发现，也是靠 `set(coordinator.data)` 差集配合 `async_add_entities` 增量加实体，这些都建立在「coordinator 随 entry 存」的基础上。

## 6.6 架构铁律：集成要薄，协议放独立 PyPI 库

官方对自定义集成有一条**硬性架构规则**：集成代码内**禁止包含任何协议特定代码**，设备/云 API 的交互必须封装成独立 PyPI 库，集成通过 `manifest.json` 的 `requirements` 依赖它（官方 api_lib_index 文档，见[开发文档索引](https://developers.home-assistant.io/docs/creating_component_index/)）。这条规则直接决定了 6.2 里 `MyApiClient` 为什么从 `my_cloud_api` 导入，而不是写在集成里。

独立库建议拆成**两层**：

```python
# 独立 PyPI 库 my_cloud_api/api.py —— 第 1 层：认证 + HTTP 请求
"""只管「怎么把请求发出去、拿回原始数据」，不关心业务含义。"""

import aiohttp


class MyApiClient:
    def __init__(self, host: str, token: str, session: aiohttp.ClientSession) -> None:
        self._host = host
        self._token = token
        self._session = session

    async def async_fetch_sensor_data(self) -> dict:
        """拉原始 JSON 并返回，不做业务加工。"""
        url = f"{self._host}/api/sensors"
        headers = {"Authorization": f"Bearer {self._token}"}
        async with self._session.get(url, headers=headers) as resp:
            resp.raise_for_status()  # 网络/HTTP 错误从这里冒出
            return await resp.json()
```

```python
# 独立 PyPI 库 my_cloud_api/models.py —— 第 2 层：数据模型
"""把原始 JSON 变成带类型的对象，供集成直接消费。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SensorData:
    sensor_id: str
    value: float
    unit: str

    @classmethod
    def from_dict(cls, raw: dict) -> "SensorData":
        return cls(
            sensor_id=raw["id"],
            value=float(raw["value"]),
            unit=raw["unit"],
        )
```

两层各司其职：**请求层**管认证、重试、超时、翻页，**模型层**管字段校验和类型转换。集成只拿到干净的 `SensorData` 对象，完全不碰 HTTP 细节。本地联调时，在开发环境装依赖并让 HA 跳过本地包即可（素材 一.5）：`pip3 install -e ../my_cloud_api` + 启动时加 `hass --skip-pip-packages my_cloud_api`。

为什么这条规则被官方定为「铁律」，而不是「建议」？至少有三个现实理由：一是**可复用**，同一个协议库可以被多个集成、甚至非 HA 项目共用，不用每次重写一遍认证握手；二是**可版本化**，库独立发版，API 变更时只需升级 `requirements` 里的版本号，集成代码一行不改；三是**安全与审核**，HACS 和官方审查时，协议代码越少、越集中在独立库里，越容易做安全审计——把认证逻辑藏在集成里，既难审也难修。

> [!tip] 大白话
> 把集成想成餐厅前台、协议库想成后厨：前台（实体）只负责把菜端给客人，做菜（协议细节、认证、翻页）全在后厨。厨房升级换菜谱（库版本更新），前台不用改；前台也绝不自己起灶开火——否则 HACS 审核官看到你的集成里藏着一个厨房，直接打回。

## 6.7 推送模型：不轮询，等数据上门

轮询适合「API 只支持主动拉取」的场景。但有些 API 是推送式的（webhook、websocket、MQTT），这时仍用固定间隔轮询就浪费了。有两种轻量做法（素材 一.5、二.plex，点到为止）：

**做法一：保留 coordinator，手动喂数据。** 用 `coordinator.async_set_updated_data(data)` 代替轮询——实体仍然从 `coordinator.data` 读缓存，但数据不再是定时拉来的，而是外部事件到达时推给你的。

**做法二：dispatcher 纯事件驱动（Plex 模式）。** 更轻量，直接用 `async_dispatcher_send` / `async_dispatcher_connect`：

```python
# 实体订阅（async_added_to_hass 里）
self.async_on_remove(
    async_dispatcher_connect(self.hass, self._dispatcher, self._handle_update)
)
# 数据到达时通知（数据源那边）
async_dispatcher_send(hass, dispatcher)
```

推送模型有一个铁律：**订阅和退订必须成对**。在 `async_added_to_hass` 里订阅，把 unsubscribe 句柄交给 `async_on_remove`（或保存在 `async_will_remove_from_hass` 里退订），否则实体被移除后回调还挂在事件总线上，会造成内存泄漏。纯事件驱动的实体还要设 `should_poll=False`。

怎么选？一句话：**API 只能拉就轮询，API 会推就用推送**。云平台大多只提供 REST 拉取接口，轮询是默认解；MQTT、websocket、本地 UDP 这类主动上报的协议，才值得上推送模型。对「上手」阶段，先扎实掌握轮询，推送留个印象即可——大多数自定义集成用 coordinator 轮询就够用了。

## 本章小结

- Coordinator 是「仓库统一收货员」：一个实例统一轮询外部 API，`coordinator.data` 缓存一份数据，所有 `CoordinatorEntity` 共享读取，网络请求只发一次。
- `_async_update_data` 里用 `asyncio.timeout(10)` 包裹网络请求；认证失败抛 `ConfigEntryAuthFailed`（触发 reauth），一般错误和限流抛 `UpdateFailed`（限流可带 `retry_after=60`），超时和 `aiohttp.ClientError` 交给 coordinator 内部处理。
- 多实体共享一次轮询：`async_setup_entry` 只建一个 coordinator，实体用 `context=idx` 订阅；`update_interval` 只在存在订阅者时才轮询。
- `async_config_entry_first_refresh()` 失败抛 `ConfigEntryNotReady` 自动重试；一次性初始化放 `_async_setup`（HA 2024.8+）；coordinator 存进 `entry.runtime_data`，优于 `hass.data[DOMAIN]`。
- 架构铁律：集成内不放协议代码，API 交互封装成独立 PyPI 库（认证/HTTP 层 + 数据模型层）；推送场景用 `async_set_updated_data` 或 dispatcher，订阅退订必须成对。

## 下一章预告

coordinator 跑起来了，数据能稳定流进实体了。但集成越写越复杂，你怎么确认它真的没写错？第 7 章进入「测试与调试」——用 pytest 给集成写「入职考试」，用 debugpy 给 HA 装上「随身体检仪」，把隐藏在事件循环深处的 bug 揪出来。
