# 第 5 章：Entity 平台与 Sensor 实体

第 4 章我们走通了 config flow：用户填完表单、校验通过，HA 签发了一张「门禁卡」——一个 config entry。但这时候打开 HA 界面，依然看不到任何数据。本章要解决的就是「从配置到展示」这一段：定义一个 sensor 平台，把 config entry 转成 HA 认识的实体，让数据真正摆上货架。读完你会明白实体是怎么被装载、注册、驱动起来的，也会看到一个「薄实体」应该长什么样。

## 5.1 平台装载机制：async_forward_entry_setups

HA 集成按「平台」拆分文件：传感器放 `sensor.py`，二进制传感器放 `binary_sensor.py`，开关放 `switch.py`……这正是第 3 章目录结构里「按平台拆分」的落地——一个文件就是一个平台，HA 通过平台文件组织不同的实体类型[官方平台索引文档](https://developers.home-assistant.io/docs/creating_component_index/)。config flow 只是「办好了门禁卡」，真正让实体出场的是 `async_forward_entry_setups`。

在 `__init__.py` 里，`async_setup_entry` 的最后一步把平台装载进来：

```python
# __init__.py —— 承接第 4 章的 async_setup_entry
async def async_setup_entry(hass, entry):
    """config flow 校验通过后，HA 调用这里正式建立条目。"""
    # 告诉 HA：请把这个 config entry 交给 sensor 平台处理。
    # HA 会去 custom_components/<domain>/sensor.py 找同名入口函数。
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
```

`async_forward_entry_setups` 做的事：为列表里的每个平台，调用对应文件里的 `async_setup_entry(hass, entry, async_add_entities)`。一次可以传多个平台，比如 `["sensor", "binary_sensor", "switch"]`。所以每个平台文件的职责非常单一——只实现这一个入口函数，把实体「注册」给 HA：

```python
# sensor.py —— sensor 平台的唯一入口
async def async_setup_entry(hass, entry, async_add_entities):
    """拿到 config entry，决定要注册哪些实体。"""
    coordinator = entry.runtime_data.coordinator  # 数据源，第 6 章接入
    async_add_entities(
        ExampleSensor(coordinator, description) for description in SENSOR_TYPES
    )
```

`async_add_entities` 是 HA 塞给你的「注册回调」：你往里丢一批实体实例，HA 就把它们纳入实体状态机，开始驱动。一个平台入口可以多次调用它，也可以一次传一个列表（比如第 6 章动态发现设备时，用差集增量添加）。

> [!tip] 大白话
> 把 config flow 想成「办了门禁卡」，`async_forward_entry_setups` 就是把这张卡送到对应柜台的过程：HA 是前台，`sensor.py` 是传感器柜台。前台拿着卡喊一声「传感器柜台有人来了」，柜台里的 `async_setup_entry` 就出来接人。所以你这头只负责写「柜台怎么接待」，装载的吆喝交给 HA。

## 5.2 Entity 状态机基础：实体怎么「活」起来

实体不是静态数据，它由一套状态机驱动[官方 Entity 文档](https://developers.home-assistant.io/docs/core/entity/)。上手阶段先记三个开关：

- **`available`**：实体当前是否可用。为 False 时 UI 置灰、自动化自动跳过。默认 True。
- **`should_poll`**：是否由 HA 周期性调用 `update()`/`async_update()` 拉取新值。默认 True（轮询模型）；设为 False 走推送模型，用 `async_write_ha_state()` / `async_schedule_update_ha_state()` 主动通知状态变化。轮询适合「不知道数据何时变」的外部 API；推送适合能主动回调的本地设备。
- **`_attr_` 前缀类属性**：给实体提供「默认实现」的声明式写法。

实体还有两个生命周期钩子值得知道：`async_added_to_hass()` 在实体加入 HA 时调用，常用于订阅外部事件；`async_will_remove_from_hass()` 在实体被移除时调用，用于退订。订阅与退订必须成对，否则会泄漏监听器——Plex 集成的 dispatcher 模式就是典型例子，第 6 章推送模型还会再碰到。

`_attr_` 是 HA 实体里最常用的套路：凡是名字以 `_attr_` 开头的类属性，HA 会自动把它当作同名属性的默认值。例如 `_attr_native_unit_of_measurement = "µg/m³"` 就等于实现了 `native_unit_of_measurement` 属性返回该值：

```python
class ExampleSensor(SensorEntity):
    _attr_has_entity_name = True            # 声明式：固定标签直接写在类上
    _attr_native_unit_of_measurement = "µg/m³"
    _attr_device_class = "pm25"
```

**关键纪律：属性 getter 禁止 I/O。** 无论用 `_attr_` 还是 `@property`，实体属性的读取都只能发生在事件循环的「内存读取」里，绝不能在这里发 HTTP 请求、查数据库、做阻塞计算。正确做法是：数据在 `update()`/`async_update()` 方法里统一拉取并缓存到 `self`，getter 只负责把缓存摆上货架。

```python
class PlainSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self):
        self._cached_value = None

    async def async_update(self):
        """should_poll=True 时，HA 周期性调用这里：唯一允许 I/O 的地方。"""
        self._cached_value = await self._fetch()  # 发请求、拿数据、缓存

    @property
    def native_value(self):
        return self._cached_value                 # getter 只读缓存
```

update 负责「取」，getter 负责「摆」，各司其职。HA 的状态驱动循环是：`async_update()` 拉新数据 → 写状态 → 界面读取属性。任何属性 getter 一旦越过这条线去做 I/O，就可能阻塞整个事件循环。

> [!warning] 易错点
> 属性 getter 里做 I/O（发请求、读文件、阻塞计算）是自定义集成最常见的问题之一：HA 的事件循环是单线程的，getter 一次阻塞，整个 HA 都会卡顿。这也是素材里反复强调的异步纪律。

> [!tip] 大白话
> `_attr_` 类属性就像「商品的固定标签」——「产地：杭州」「规格：500ml」印在包装上，顾客拿起就看，不用每次跑去仓库问。getter 只读内存就是「看标签」，代价近乎为零；如果在 getter 里发网络请求，等于每次有人看标签都要跑一趟仓库，既慢又容易把事件循环堵死。

## 5.3 身份三件套：has_entity_name / unique_id / device_info

一个新实体要「合法上岗」，有三样身份信息几乎必配：

| 配置 | 作用 | 注意 |
|------|------|------|
| `has_entity_name = True` | 实体名自动组合为「设备名 + 实体名」 | HA 官方强制新集成开启 |
| `unique_id` | 实体的唯一身份证号，关联 entity registry | 平台内唯一，禁止用 IP / 设备名 |
| `device_info` | 把实体挂到某台「设备」下，自动注册 device registry | 提供 `identifiers` 即可 |

- **`has_entity_name=True`**：官方强制项。开启后 friendly_name 由设备名与实体名拼接，避免「PM2.5 / PM2.5 / PM2.5」这种到处重名的混乱。
- **`unique_id`**：实体在 entity registry 里的主键。有了它，HA 才能在重启后记住用户对它的改名、隐藏、归属区域；没有它，每次重启实体都像「新来的」。它要求平台内唯一、一旦确定不可用户配置。
- **`device_info`**：把多个实体归到同一台「设备」下（比如一台净化器有 PM2.5 和温度两个传感器）。只要提供 `identifiers`，HA 会自动在 device registry 里建好设备记录，UI 里这些实体就出现在同一张设备卡下：

```python
self._attr_device_info = DeviceInfo(
    identifiers={(DOMAIN, coordinator.address)},
    manufacturer="Example",
    name="示例设备",
)
```

注意两个注册表的分工：**entity registry 管实体**（改名、隐藏、归属区域），**device registry 管设备**（一台设备聚合多个实体）。`unique_id` 决定实体进 entity registry，`device_info` 决定设备进 device registry。也正因为 unique_id 承担了「记住用户设置」的重任，它必须稳定且唯一：官方要求禁止用 IP、设备名这类可能变化的值，而要用 MAC、序列号或我们这里的「设备地址 + key」这类长期不变的组合。

多个平台（`sensor`、`binary_sensor`）的实体只要提供同一组 `identifiers`，就会归入同一台设备，UI 上共享一张设备卡——这是 device registry 最常见的价值。

> [!tip] 大白话
> Entity 就是「柜台展示员」，sensor 实体负责把数据摆上货架给用户看。`unique_id` 是展示员的工号，凭工号 HA 才能认出「还是上次那个人」，不然每次重启都是新面孔；`device_info` 是「所属部门」，把同属一台设备的展示员编进同一组；`has_entity_name` 决定工牌上怎么写名字。展示员自己不做数据搬运——数据由后仓（coordinator）送来，他只负责上架。

## 5.4 声明式实体写法：SensorEntityDescription + value_fn

一个集成往往有多个 sensor。与其为每个传感器复制一份类，不如把「差异」提取成描述。HA 提供 `SensorEntityDescription` 作为基类，社区常用 `@dataclass(frozen=True)` 子类化它、再追加一个 `value_fn` 字段（参考 [mops_pm25](https://github.com/haruue/mops_pm25) 的实现）：

```python
# sensor.py
from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity


@dataclass(frozen=True)
class ExampleSensorDescription(SensorEntityDescription):
    """在官方描述类上「加料」：多一个 value_fn 告诉实体怎么取值。"""

    value_fn: object | None = None


SENSOR_TYPES = (
    ExampleSensorDescription(
        key="pm2_5",
        name="PM2.5",
        native_unit_of_measurement="µg/m³",
        device_class="pm25",
        value_fn=lambda c: c.data.get("pm2_5"),
    ),
    ExampleSensorDescription(
        key="temperature",
        name="温度",
        native_unit_of_measurement="°C",
        device_class="temperature",
        value_fn=lambda c: c.data.get("temperature"),
    ),
)


class ExampleSensor(CoordinatorEntity, SensorEntity):
    """实体很薄：数据从 coordinator 拿，只负责上架。"""

    _attr_has_entity_name = True

    def __init__(self, coordinator, description):
        super().__init__(coordinator)
        self.entity_description = description
        # 唯一 ID：设备地址 + 描述 key，保证平台内唯一
        self._attr_unique_id = f"{coordinator.address}-{description.key}"

    @property
    def native_value(self):
        return self.entity_description.value_fn(self.coordinator)
```

这段代码每一行的意图：

- `@dataclass(frozen=True)`：描述类不可变，安全、可哈希，符合声明式风格。
- `value_fn`：描述里声明「这个 key 怎么从 coordinator 的数据里取值」，实体类不再写 if/else 分支。它不一定是 lambda：当取值逻辑变复杂（单位换算、字段缺失时的兜底值），可以抽成命名函数，在描述里引用函数名即可。
- `entity_description` 一旦赋值，HA 会自动用描述里的 `name` / `native_unit_of_measurement` / `device_class` 填充实体属性，实体类本身不用再声明 `_attr_` 去覆盖。
- `native_value` 委托 `value_fn(self.coordinator)`：getter 只做内存读取，满足 5.2 的纪律。
- `_attr_unique_id = f"{coordinator.address}-{description.key}"`：用「设备地址 + 传感器 key」拼出稳定唯一 ID，天然满足「平台内唯一、可追溯到设备」的要求。

`SENSOR_TYPES` 是模块级常量，放在 `sensor.py` 顶部即可；描述多了也可以挪到 `const.py`。注册时用生成器表达式把每个描述实例化为实体——这正是官方维护者蓝本里的常见写法：先声明描述列表，再用一行生成器交给 `async_add_entities`，见 5.1 的入口骨架。描述列表与实体类的解耦，让「新增一个传感器」彻底变成纯配置操作。

以后想加一个传感器，只需在 `SENSOR_TYPES` 里加一行描述，实体类一行都不用改。这就是声明式写法的收益：**差异数据化，逻辑收敛在描述里。**

## 5.5 衔接：CoordinatorEntity 基类

上面的实体类继承的不是 `SensorEntity` 而是 `CoordinatorEntity`——这是一个值得提前认识的基类，它是第 6 章 DataUpdateCoordinator 的「插座」[官方数据获取文档](https://developers.home-assistant.io/docs/integration_fetching_data/)：

- 它自动接管 `should_poll`：把实体的刷新请求转成 `coordinator.async_request_refresh()`。
- 它自动实现 `async_update()`：实体该更新时，去问 coordinator 要最新数据。
- 它自动挂钩 `available`：coordinator 上次更新成功（`last_update_success`）时实体才可用，失败自动置灰。

换句话说，`CoordinatorEntity` 把 5.2 节讲的三个开关全部接管了：`should_poll`、`async_update`、`available` 都不再需要你手写，实体类只要关心「从 coordinator 的数据里取出并格式化这一个值」。一旦实体继承它，轮询、更新、可用性三件事都交给 coordinator 统一管理，实体只剩「摆数据」这一件事。这正是下一章的内容：coordinator 如何定时去 API 拉数据、多实体如何共享同一次轮询、异常如何归类成重试或 reauth。

## 本章小结

- 平台装载：`async_forward_entry_setups(entry, ["sensor"])` 把 sensor 平台接进来；平台文件只需实现 `async_setup_entry(hass, entry, async_add_entities)`，用 `async_add_entities` 注册实体。
- 实体状态机三开关：`available`、`should_poll`（默认 True）、`_attr_` 类属性；**属性 getter 只读内存，I/O 必须放 update 方法**。
- 身份三件套：`has_entity_name=True`（强制）、`unique_id`（平台内唯一、关联 entity registry）、`device_info`（自动注册 device registry）。
- 声明式写法：`@dataclass(frozen=True)` 子类化 `SensorEntityDescription` + `value_fn`，实体差异全部收敛进描述。
- 实体继承 `CoordinatorEntity` 后，轮询 / 更新 / 可用性都交给 coordinator，为第 6 章铺路。

下一章，我们要解决最后一个问题：这些实体展示的数据从哪来？DataUpdateCoordinator 将作为「仓库统一收货员」，定时去外部 API 拉数据，让所有实体共享同一份到货数据。
