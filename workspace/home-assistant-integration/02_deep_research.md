# 从零开发 Home Assistant 自定义集成 - 深度收集

收集时间: 2026-08-08
搜索关键词: HA custom integration dev environment / manifest.json / config flow / DataUpdateCoordinator / pytest / hassfest / HACS publish
信源: 官方文档（developers.home-assistant.io + home-assistant.io）+ GitHub 真实代码（core 仓库 + 官方示例/蓝本）+ PyPI + HACS 官方文档 + 社区讨论

> 本文件服务对象：从零写一个**可运行、可 HACS 分发**的 HA 自定义集成（sensor 平台），深度「上手」，用户基础「有了解」（会 Python + async/await + 用过 HA）。

---

## 一、核心概念/理论素材

### 1. 开发环境搭建

**官方推荐：VS Code + Dev Container（devcontainer）**
- 流程：fork `home-assistant/core` → `git clone` + `code .` → VS Code 检测到容器配置弹「Reopen in Container」→ 首次构建数分钟。
- 容器内任务面板选 **Run Home Assistant Core**，浏览器访问 `http://localhost:8123` 即可看到 HA 界面；**F5 直接进带断点调试**。
- Windows 前置要求：**WSL2 + `/etc/wsl.conf` 设 `systemd=true`**；macOS 需 Docker Desktop。

**devcontainer 真实配置（core 仓库现行版）**
- `postCreateCommand` 跑 `script/setup`；`postStartCommand` 跑 `script/bootstrap`。
- `appPort` 映射 **8123**(HA) 与 5683/udp(Shelly)；预装 VS Code 扩展：Ruff、pylint、Pylance、yaml、prettier、GitHub PR、Copilot。
- 默认解释器 `~/.local/ha-venv`；`PYTHONASYNCIODEBUG=1`。
- `Dockerfile.dev`：基于 `vscode/devcontainers/base:debian`，apt 装 ffmpeg、bluez、libudev-dev、libpcap-dev、libturbojpeg0 等，装 `uv` 建 venv 并安装 `requirements.txt` + `requirements_test.txt`(pytest) + `requirements_test_pre_commit.txt`(Ruff/mypy)。

> [!warning] 注意：**现行 core dev 镜像未预装 Mosquitto**。社区文档常把「本地 Mosquitto MQTT broker」列成 devcontainer 预装项，但现行 `devcontainer.json`/`Dockerfile.dev` 里没有，需自行 `apt install mosquitto` 或另起容器。写教程时不要把它当预装项。

**替代方案：本地 venv**
- 官方同样支持手动方案：`git clone home-assistant/core` → `script/setup` → `source .venv/bin/activate && hass -c config`（Python 3.14.2+）。
- 对比：venv 重启更快、硬件（USB/Zigbee/蓝牙）直通，适合迭代调试；devcontainer 环境一致、零手动配置、F5 即调，但 Windows/macOS 容器难直通硬件。官方推荐新手走 devcontainer。

**官方脚手架**
- 命令：`python3 -m script.scaffold integration`（在 core 检出目录内运行）。
- 生成内容（`script/scaffold` 源码确认）：`__init__.py`（含 `async_setup` 骨架 + CONFIG_SCHEMA）、`const.py`（DOMAIN 常量）、`manifest.json`（含 `quality_scale`）、`quality_scale.yaml` + `tests/` 目录；选 config flow 会追加 `config_flow.py` + `strings.json` 并改 manifest。
- 社区实操衔接：`hass -c config` 验证环境 → scaffold → `mkdir /config/custom_components` → 整目录拷入 → 补 `manifest.json` 的 `"version": "0.0.1"` → 重启后在「设置→设备与服务」看到。

### 2. 集成目录结构

- 自定义集成位于 **`custom_components/<domain>/`**；内置集成位于 `homeassistant/components/<domain>`。**目录名即 domain。**
- 最小文件集：`manifest.json` + `__init__.py`。
- 按平台拆分：每类实体一个文件（`sensor.py`、`binary_sensor.py`、`light.py`…）；注册服务需 `services.yaml`；`DataUpdateCoordinator` 建议放 `coordinator.py`；`const.py` 放常量。
- 官方示例仓库 `example-custom-config` 三种规模：
  - `example_sensor`：仅 `manifest.json` + `__init__.py` + `sensor.py` 三文件。
  - `detailed_hello_world_push`：`__init__.py`、`config_flow.py`、`const.py`、`hub.py`、`sensor.py`、`cover.py`、`manifest.json`、`strings.json`、`translations/en.json`。
  - `expose_service_*`：展示 `services.yaml` 用法。
- HACS 蓝本 `hacs.integration_blueprint`：平台按子包组织（`binary_sensor/`、`button/`、`fan/`…），含 `data.py`、`diagnostics.py`、`repairs.py`、`coordinator/`、`entity/`。

### 3. manifest.json 字段

**必填/核心字段**
- `domain`：**唯一、不可改、须与目录名一致**（小写下划线）。
- `name`：集成显示名。
- `version`：**自定义集成（含覆盖内置集成）必须写**，符合 AwesomeVersion（CalVer 或 SemVer）；内置 core 集成省略。
- `codeowners`：GitHub 维护者（格式 `@user` 列表）。
- `requirements`：pip 兼容字符串，官方示例均 **`==` 固定版本**；安装失败会导致集成加载失败。
- `iot_class`：六值 —— `assumed_state` / `cloud_polling` / `cloud_push` / `local_polling` / `local_push` / `calculated`。
- `integration_type`：八值 —— `device` / `entity` / `hardware` / `helper` / `hub` / `service` / `system` / `virtual`，**未设默认 `hub`**。
- `dependencies`：硬依赖（本集成加载前必须先加载）；`after_dependencies`：软依赖（优先加载但非必需）。
- 自动发现字段：`zeroconf` / `dhcp` / `bluetooth` / `mqtt` / `ssdp` / `homekit` / `usb`。
- 调试相关：`loggers`（列出 requirements 依赖库的 logger 名，修复 UI「Enable debug logging」按钮失效）。

**真实 manifest 参考**
- `mobile_app`：`config_flow: true`、`integration_type: device`、`iot_class: local_push`、dependencies（http/webhook/websocket_api）、requirements `"PyNaCl==1.6.2"`、无 version（内置集成）。
- `esphome`：zeroconf `_esphomelib._tcp.local.`、mqtt `esphome/discover/#`、dhcp `registered_devices: true`、`quality_scale: platinum`、requirements 三个包全部 `==` 固定。

**integration_type 语义**（官方博客 2022-10-24）
- `hub`：中枢网关管理多设备（如 Hue）；`service`：每个配置条目连单一外部服务（如 AdGuard）；`device`：每个配置条目对应单一物理设备（如 ESPHome）；`virtual`：仅含 manifest 无代码的虚拟集成（2022.11 引入，替代 supported brands，通过 `supported_by`/`iot_standards` 指向真实实现）。

**configuration.yaml 加载**
- 把 domain 作为顶层键（如 `hello_state:`）即可加载；定义 `CONFIG_SCHEMA`（voluptuous）则配置先经其校验转换再交给集成。
- **ADR-0007/ADR-0010**：禁止新集成使用「平台键」YAML；设备/服务集成应走 config flow，YAML 仅既有集成例外。

### 4. Config Flow 配置流程

**核心结构**
- `config_flow.py`：类继承 `config_entries.ConfigFlow`，`domain = DOMAIN`；`manifest.json` 设 `config_flow: true`。
- `VERSION` / `MINOR_VERSION` 默认 1；主版本升级触发 `async_migrate_entry`。
- 表单：voluptuous schema + `async_show_form` / `async_create_entry`；错误与文案定义在 `strings.json` 的 `config` 键下。

**官方示例（detailed_hello_world_push/config_flow.py）**
```python
DATA_SCHEMA = vol.Schema({("host"): str})

async def validate_input(hass, data):
    # 抛自定义 CannotConnect/InvalidHost（继承 HomeAssistantError）

async def async_step_user(self, user_input=None):
    errors = {}
    if user_input is not None:
        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)
    return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
```
- 错误可绑**字段级** `errors["host"]` 或**整体** `errors["base"]`；兜底 `except Exception` 记录日志并置 `"unknown"`。

**唯一性**
- `async_set_unique_id` + `_abort_if_unique_id_configured(updates=...)`（可顺便更新已有条目）。
- **unique_id 禁止用 IP、设备名**，可用 MAC/序列号。

**reauth / reconfigure（官方 2024-10-21 博客）**
- 用 `self._get_reauth_entry()` / `self._get_reconfigure_entry()` 替代手动查 `self.context["entry_id"]`；每次 step 局部取，不缓存为类属性。
- `async_set_unique_id` 后调 `_abort_if_unique_id_mismatch()` 防改错账号。
- `async_update_reload_and_abort` 用 `data_updates=` 合并更新更安全（降低 schema 演进数据丢失风险）。
- reconfigure 成功需在 `strings.json` 加 `reconfigure_successful`。
- reauth 成功后默认总是 reload；`reload_even_if_entry_is_unchanged=False` 仅用于「数据未真正变化」场景。

**Options Flow**
- config flow 内定义静态 `async_get_options_flow` 返回 `OptionsFlow` 子类；首个 step 恒为 `async_step_init`；用 `add_suggested_values_to_schema` 预填当前值；`async_create_entry(data=user_input)` 保存。
- 继承 `OptionsFlowWithReload` 可在 options 变更时自动重载。
- **`data` 安装后不可变、`options` 可变**；监听变化用 `entry.async_on_unload(entry.add_update_listener(...))`。

**ConfigEntry 对象（core 源码确认）**
- 字段：`entry_id`、`domain`、`title`、`data`（MappingProxyType 只读）、`options`（只读）、`unique_id`、`state`、`version`/`minor_version`、`source`、`disabled_by`、`runtime_data`。

**异常语义（core 源码确认）**
- `ConfigEntryNotReady`：`async_setup_entry` 中抛出 → 条目置 `SETUP_RETRY`，按**指数退避**（`min(2**tries*5, 最大等待)`）自动重试，不是硬失败。
- `ConfigEntryAuthFailed`：触发 reauth 流程。

**strings.json 结构（官方示例）**
```json
{
  "config": {
    "step": { "user": { "data": { "host": "主机地址" } } },
    "error": { "cannot_connect": "无法连接", "invalid_auth": "认证失败", "unknown": "未知错误" },
    "abort": { "already_configured": "已配置" }
  }
}
```
- 支持 `[%key:common::config_flow::...%]` 引用公共文案；翻译由 `script.translations develop` 生成。

### 5. Entity 平台 + DataUpdateCoordinator

**DataUpdateCoordinator（官方 fetching_data 文档）**
- `_async_update_data` 内用 **`asyncio.timeout(10)`** 包裹网络请求。
- 认证失败抛 `ConfigEntryAuthFailed`（触发 reauth）；一般错误抛 `UpdateFailed`；限流抛 `UpdateFailed(retry_after=60)`。
- `asyncio.TimeoutError` / `aiohttp.ClientError` **已被 coordinator 内部处理**，无需自己捕获。
- 多实体共享一次轮询：`async_setup_entry` 建一个 coordinator 实例，实体以 `context=idx` 订阅。
- `update_interval` **仅在有订阅者时才轮询**；`async_config_entry_first_refresh()` 失败抛 `ConfigEntryNotReady` 自动重试。
- 推送型 API 可调 `coordinator.async_set_updated_data(data)` 代替轮询。
- HA 2024.8 新增 `_async_setup`：一次性初始化（如获取设备信息），在 `async_config_entry_first_refresh()` 期间自动调用，与 `_async_update_data` 同享错误处理。

**Entity 状态机（官方 core/entity 文档）**
- `available`：false 时实体不可用；`should_poll` 默认 true（用 `update()`/`async_update()` 拉取）；`unique_id` 平台内唯一、关联 entity registry、不可用户配置；`device_info` 自动注册到 device registry。
- `_attr_` 前缀类属性提供默认实现。**属性 getter 只能读内存，不能做 I/O**；数据应在 update 方法里拉取缓存。
- `has_entity_name=True` 为强制项，friendly_name 由设备名+实体名组成。
- `async_added_to_hass` / `async_will_remove_from_hass` 生命周期用于订阅/退订。
- 推送模型：设 `should_poll=False` 后用 `async_write_ha_state()` / `async_schedule_update_ha_state()` 通知。

**架构原则（官方 api_lib_index 文档，硬性规则）**
- **集成内禁止包含任何协议特定代码**；设备/云 API 交互必须抽成独立 PyPI 库，集成依赖该库。
- 库建议拆两层：认证/HTTP 请求层 + 数据模型层；本地测试用 `pip3 install -e ../my_lib` + `hass --skip-pip-packages my_lib_module_name`。

**平台装载（官方 creating_platform_index）**
- 自定义集成按平台拆分（`sensor.py` 等），通过 `async_forward_entry_setups` 装载；每个平台实现 `async_setup_entry(hass, entry, async_add_entities)`，实体经 `async_add_entities([...])` 注册。

**官方质量规则**
- 动态设备：`entry.runtime_data` 存放 coordinator；每次更新用 `set(coordinator.data)` 差集发现新设备，经 `coordinator.async_add_listener` 注册 `async_add_entities` 增量加实体。
- Mark unavailable：`CoordinatorEntity` 自带该逻辑（与 `coordinator.last_update_success` 挂钩）；需额外条件时 `return super().available and self.identifier in self.coordinator.data`。

### 6. Services / 异步纪律

- 自定义服务：`services.yaml` 声明参数，`__init__.py` 里 `hass.services.async_register` 注册。
- **异步纪律**（官方 asyncio_working_with_async）：属性 getter 禁止 I/O；回调用 `async_` 前缀方法；协程与回调加 `@callback` 装饰；`hass.async_block_till_done()` 等待派发完成。

### 7. 测试

- **pytest-homeassistant-custom-component**：从 home-assistant/core 自动抽取测试插件与 fixtures 的 pytest 插件，让自定义组件用与 HA 核心相同方式测试。
  - `conftest.py` 声明 `pytest_plugins = ["pytest_homeassistant_custom_component"]` 后即可直接用 `hass` fixture。
  - helper 从 `pytest_homeassistant_custom_component.common` 导入（如 `MockConfigEntry`）。
  - **`enable_custom_integrations`**（HA ≥2021.6.0b0 必需）；`recorder_mock` 须先于 `enable_custom_integrations` 初始化。
  - 每日按 HA 最新版（含 beta）更新。
- 官方测试指南：集成测试不触碰内部细节，通过核心接口断言 —— `hass.states`、`hass.services`、设备/实体 registry；配置项用 `MockConfigEntry` 模拟。
- 命令：`pytest tests`；单集成 `pytest ./tests/components/<组件>/ --cov=homeassistant.components.<组件> --cov-report term-missing -vv`；快照测试用 `--snapshot-update`（Syrupy，`.ambr` 文件）。
- 其他：`-p no:homeassistant` 关闭 socket 拦截；常需 `asyncio_mode = auto`。

### 8. 调试

- **debugpy 集成**：`configuration.yaml` 加 `debugpy:`；默认监听 0.0.0.0:5678；`start: true` 启动时注入、`wait: true` 等待调试器连接（调试 `async_setup` 启动序列）。VS Code 用 attach + `pathMappings`。**安全警告**：可达调试端口者可执行任意代码，生产勿常开。
- **断点不命中（core issue #110623）**：HA 须以 `python3 -Xfrozen_modules=off -m homeassistant` 启动；VS Code 确认 `justMyCode: false`；`pathMappings` 正确（本地 `custom_components/<domain>` ↔ 容器 `/config/custom_components/<domain>`）。asyncio 架构下断点命中时整个 HA 会暂停。
- **logger 配置**：`logger: logs: custom_components.<domain>: debug`；requirements 依赖库需单独加 logger 条目（如 `aiogithubapi: debug`）。UI「Enable debug logging」按钮对自定义组件默认无效（core #84489），在 manifest.json 加 `loggers` 键修复。
- **排障**：官方推荐 `hass --script check_config`（Docker 下 `docker exec home-assistant python -m homeassistant --script check_config --config /config`）；日志在配置目录 `home-assistant.log`，每次启动重置；UI 在 Settings → System → Logs 查看。未配 logger 时默认级别 warning。

### 9. HACS 分发

- **hassfest Action**：`.github/workflows/hassfest.yaml`，`uses: home-assistant/actions/hassfest@master`，push/PR/每日 cron 运行，跟踪 beta 通道提前提示不兼容。
- **hacs.json**（仓库根目录）：必填 `name`；可选 `content_in_root` / `zip_release`（需 `filename`）/ `homeassistant` / `hacs` / `persistent_directory`。版本取最新 **release tag**（无 tag 用 commit 前 7 位）；**仅 push tag 不生成 Release 无效**。
- **HACS 集成细则**：每仓库只能一个集成；代码须在 `custom_components/<domain>/`（`content_in_root: true` 例外）；manifest 至少含 `domain` / `documentation` / `issue_tracker` / `codeowners` / `name` / `version`；必须先加入 home-assistant/brands；有 Release 时展示最近 5 个版本。
- **hacs/action**：`uses: hacs/action@main`，`category` 必填（integration/plugin/template/theme/appdaemon/python_script），`ignore` 可忽略 archived/brands/description/hacsjson 等检查项；建议搭配 hassfest action。
- **更新机制**：HACS 通过 GitHub API 拉取 release 数据（未认证会限流致版本陈旧），约每天检查；已装版本存 `manifest.json` 的 `version`（记录于 `.storage/hacs.repositories`），与最新 release 比对；**下载后须重启 HA 才生效**。

---

## 二、实战代码/项目案例（权威参考实现）

| 项目 | 定位 | 值得抄的模式 |
|------|------|-------------|
| `home-assistant/example-custom-config` | 官方示例仓库 | 最简三文件（example_sensor）；完整 config flow 示例（detailed_hello_world_push：validate_input 抛自定义异常 → errors 回显 → async_create_entry） |
| `ludeeus/integration_blueprint` | HA 核心维护者 Ludeeus 的官方脚手架 | `entry.runtime_data` 存 client/coordinator（取代 `hass.data[DOMAIN]`）；API 库异常统一映射（Auth→ConfigEntryAuthFailed、RateLimit→UpdateFailed(retry_after)）；`CoordinatorEntity[Coordinator]` 基类 + `_attr_unique_id=entry_id` + `DeviceInfo`；sensor 用 `SensorEntityDescription` + 生成器 `async_add_entities` |
| `jpawlowski/hacs.integration_blueprint` | HACS 分发标准蓝本 | 目录组织（platform 子包、config_flow 拆分、diagnostics/repairs）、AI 辅助开发指导 |
| `haruue/mops_pm25` | 声明式实体模式 | `@dataclass(frozen=True)` 子类化 `SensorEntityDescription` + `value_fn`；`native_value` 委托 `value_fn(self.coordinator)`；`_attr_has_entity_name=True`；`unique_id = f"{coordinator.address}-{description.key}"` |
| `jjlawren/home-assistant` (plex/sensor.py) | dispatcher 推送模式 | `async_dispatcher_send`/`async_dispatcher_connect`；`async_added_to_hass` 订阅 + 保存 unsubscribe 句柄；`@callback`；必须成对订阅/退订防泄漏；`should_poll=False` 纯事件驱动 |

---

## 三、常见坑 / 最佳实践

### 常见坑
1. **manifest 缺 `version`**（自定义集成必填，格式要 AwesomeVersion 兼容）。
2. **`domain` 与目录名不一致**（大小写/下划线不符）→ 集成加载失败。
3. **requirements 不固定版本** → 环境漂移；依赖库安装失败 → 集成加载失败。
4. **asyncio 阻塞**：属性 getter 做 I/O、同步库阻塞事件循环。
5. **`ConfigEntryNotReady` vs `ConfigEntryAuthFailed` 用错**：NotReady→自动重试；AuthFailed→触发 reauth。
6. **调试日志不生效**：UI「Enable debug logging」对自定义组件默认无效，需 manifest `loggers` 键。
7. **debugpy 断点不命中**：需 `-Xfrozen_modules=off` + `justMyCode: false` + 正确 `pathMappings`。
8. **可选 EntitySelector 留空报 `vol.Invalid`**（社区案例）：可选 selector 不设 `default`，或按条件动态组 schema。
9. **Mosquitto 不是 devcontainer 预装项**（现行 core 镜像），别照抄旧教程。
10. **HACS 版本不更新**：仅 push tag 不建 Release 无效；未认证 GitHub API 会限流导致版本陈旧。

### 最佳实践
1. **集成代码尽量薄，业务逻辑放独立 PyPI 库**（官方硬性架构规则）。
2. `entry.runtime_data`（较新）优于 `hass.data[DOMAIN]` 存 client/coordinator。
3. 多实体共享一个 coordinator，`context=idx` 区分；`_async_setup` 做一次性初始化（HA 2024.8+）。
4. 实体用 `_attr_` 类属性 + `SensorEntityDescription`（可加 `value_fn`）减少重复代码；`has_entity_name=True` 强制。
5. reauth/reconfigure 用官方 helper（`_get_reauth_entry` / `data_updates=`）。
6. 测试断言走核心接口（`hass.states`/`hass.services`/registries），不碰内部细节。
7. 分发：hassfest action + hacs/action 双保险；manifest 6 必填字段齐备。

---

## 四、工具链 / 生态

| 工具 | 用途 | 备注 |
|------|------|------|
| VS Code Dev Container | 一键预配置开发环境 | F5 断点调试；Windows 需 WSL2 + systemd |
| `script.scaffold integration` | 生成集成骨架 | 含 config flow/测试/i18n 可选 |
| `hass -c config` / `hass --debug` | 启动 HA（开发配置目录/调试模式） | `--debug` 出自源码确认 |
| `pytest-homeassistant-custom-component` | 自定义组件测试插件 | `hass` fixture + `MockConfigEntry` |
| `hassfest`（action） | 集成合规校验 | `home-assistant/actions/hassfest@master` |
| `hacs/action` | HACS 校验 | `category: integration` |
| `debugpy` | 远程断点调试 | 端口 5678；生产勿开 |
| `hacs.json` + GitHub Release | 分发 | tag 必须建 Release |

---

## 五、进阶路径 / 学习资源

**学习路径（契合「上手」深度）**
1. 搭环境：Fork core → Dev Container 打开 → 跑通 `Run Home Assistant Core`。
2. 最小集成：`custom_components/hello_world/` + `manifest.json`（domain+name+version）+ `__init__.py`（DOMAIN + async_setup）→ configuration.yaml 加一行验证加载。
3. 官方脚手架：`python3 -m script.scaffold integration` 生成 config flow 骨架。
4. Config flow：async_step_user 表单 + voluptuous 校验 + unique_id 防重复。
5. Sensor 平台 + DataUpdateCoordinator：轮询外部 API，暴露 1-2 个实体。
6. 工程细节：翻译（strings.json）、测试（pytest + hass fixture）、dispatcher 通知。
7. 分发：GitHub 仓库 + hassfest/hacs action + Release tag。

**核心资源**
- 官方开发文档索引：https://developers.home-assistant.io/docs/creating_component_index/
- 开发环境：https://developers.home-assistant.io/docs/development_environment/
- 文件结构：https://developers.home-assistant.io/docs/creating_integration_file_structure/
- manifest：https://developers.home-assistant.io/docs/creating_integration_manifest/
- Config flow：https://developers.home-assistant.io/docs/core/integration/config_flow/
- 数据获取/Coordinator：https://developers.home-assistant.io/docs/integration_fetching_data/
- 官方示例仓库：https://github.com/home-assistant/example-custom-config
- 官方维护者蓝本：https://github.com/ludeeus/integration_blueprint
- HACS 发布文档：https://hacs.xyz/docs/publish/start/（+ /integration/ + /action/）
- 中文对照：https://hasscn.top/developers/docs/

---

## 六、素材质量确认

- **官方文档数**：14+ 篇（developers.home-assistant.io 核心页 + 官方博客 + home-assistant.io 集成文档），全部精读。
- **官方/权威代码数**：6 个 GitHub 仓库（core 源码 + 官方示例 + 官方维护者蓝本 + 真实内置集成 manifest + 社区高质量实现），经 GitHub API 获取。
- **深度文章数**：HACS 官方发布文档 3 篇 + PyPI + 社区排查案例若干。
- **权威度**：核心结论均有官方文档原句或源码佐证；社区内容仅作补充/踩坑参考。
- **时效性**：官方文档持续维护（2026 现行）；版本相关标注了引入版本（如 `_async_setup` 2024.8、virtual 2022.11）。

---

## 七、综合分析

1. **官方权威主链**：Dev Container → `script.scaffold` → config flow → sensor 平台 + DataUpdateCoordinator → pytest → hassfest + HACS。这条路径与「上手」深度完全匹配，按序推进即可写通最小集成。
2. **推荐实现范式**：以官方 `fetching_data` 文档 + `ludeeus/integration_blueprint` 为主线（`entry.runtime_data` + 异常映射 + `CoordinatorEntity` 基类），实体层参考 `mops_pm25` 的 `SensorEntityDescription + value_fn` 声明式写法，推送场景参考 Plex dispatcher 模式。
3. **架构铁律**：集成内不放协议代码，API 交互封装独立 PyPI 库（官方硬性要求），这决定笔记里应把「API client 封装」作为一个独立模块来讲。
4. **易错点集中**：manifest 版本/domain/requirements、asyncio 阻塞、ConfigEntryNotReady vs AuthFailed、调试日志与断点配置。这些应作为独立「常见坑」章节。
5. **素材覆盖完整，无缺口**，可直接进入 P3 大纲生成。
