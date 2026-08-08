## 学习笔记大纲：《从零开发 Home Assistant 自定义集成（custom integration）》

> 笔记类型：实战笔记（practice）
> 学习深度：上手（照着教程写完并跑通一个最小自定义集成）
> 用户基础：有了解（会 Python + async/await，用过 HA）
> 预计总篇幅：约 20000-23000 字
> 章节数：9
> 主线：搭环境 → 骨架与 manifest → Config Flow → Sensor 实体 → Coordinator 数据 → 测试调试 → HACS 分发 → 排错

### 章节总览

| 章节 | 标题 | 篇幅 | 代码示例 |
|------|------|------|----------|
| 第 1 章 | 认识 Home Assistant 自定义集成 | 短 | 无 |
| 第 2 章 | 开发环境搭建 | 中 | 有 |
| 第 3 章 | 集成骨架与 manifest.json | 中 | 有 |
| 第 4 章 | Config Flow 配置流程 | 长 | 有 |
| 第 5 章 | Entity 平台与 Sensor 实体 | 中 | 有 |
| 第 6 章 | DataUpdateCoordinator 数据轮询 | 长 | 有 |
| 第 7 章 | 测试与调试 | 中 | 有 |
| 第 8 章 | HACS 分发 | 短 | 有 |
| 第 9 章 | 常见坑与最佳实践 | 中 | 无 |

---

### 第 1 章：认识 Home Assistant 自定义集成

- **篇幅**：短（约 1000-1500 字）
- **覆盖要点**：什么是自定义集成（custom integration）、与内置集成的区别、`custom_components/<domain>` 的生态位置、本笔记的学习路径总览、最终成品预览（一个带 config flow + sensor + coordinator + HACS 分发的最小集成）。明确范围边界：不重复 HA 部署/使用层内容（避免与已有笔记重叠）。
- **素材引用**：一.2、一.3、五、七
- **代码示例**：无（仅目录结构示意）
- **大白话设计**：把 HA 比作一家公司，集成是「外聘员工」；`custom_components/` 是外聘员工工位区，`homeassistant/components/` 是正式员工工位区。点出本章之后每个核心概念都会配一个 `[!tip] 大白话` 类比。

### 第 2 章：开发环境搭建

- **篇幅**：中（约 2000-2500 字）
- **覆盖要点**：官方推荐 VS Code Dev Container 全流程（fork core → clone → Reopen in Container）、Windows 前置 WSL2 + `/etc/wsl.conf` 设 `systemd=true`、容器内「Run Home Assistant Core」跑起 `localhost:8123`、F5 直接带断点调试、devcontainer 真实配置要点（appPort 8123、`~/.local/ha-venv`、预装 Ruff/pylint/Pylance、`PYTHONASYNCIODEBUG=1`）、本地 venv 替代方案及两者对比、官方脚手架 `python3 -m script.scaffold integration` 生成骨架。
- **素材引用**：一.1、四、五
- **代码示例**：有（devcontainer 配置片段、scaffold 命令、`hass -c config` 启动命令）
- **大白话设计**：Dev Container 是「装好所有工具的全新工位」，打开容器即可开工；脚手架是「装修公司给的毛坯房图纸」，一张图纸生成骨架。提醒坑：Mosquitto 不是现行 core 镜像预装项，别照抄旧教程。

### 第 3 章：集成骨架与 manifest.json

- **篇幅**：中（约 2000-2500 字）
- **覆盖要点**：`custom_components/<domain>` 目录结构（目录名即 domain）、最小文件集（`manifest.json` + `__init__.py`）、按平台拆分的文件组织（sensor.py / coordinator.py / const.py / services.yaml）、manifest 必填与核心字段逐一讲解（`domain` / `name` / `version` / `codeowners` / `requirements` / `iot_class` / `integration_type`）、`dependencies` vs `after_dependencies`、自动发现字段（zeroconf/dhcp/mqtt 等）、`configuration.yaml` 加载方式与 CONFIG_SCHEMA、真实 manifest 参考（mobile_app / esphome）。
- **素材引用**：一.2、一.3、二
- **代码示例**：有（完整 `manifest.json` JSON、`__init__.py` 的 `async_setup` 骨架）
- **大白话设计**：manifest.json 是「入职登记表/员工身份证」，`domain` 是唯一工号（小写下划线、不可改）；`version` 是自定义集成必填的版本号，格式必须 AwesomeVersion 兼容。

### 第 4 章：Config Flow 配置流程

- **篇幅**：长（约 3000-3500 字）
- **覆盖要点**：`config_flow.py` 类结构（继承 `ConfigFlow`、`domain = DOMAIN`）、manifest 设 `config_flow: true`、`async_step_user` 表单 + voluptuous schema、`validate_input` 与异常映射（自定义 `CannotConnect`/`InvalidHost`）、errors 回显（字段级 vs `errors["base"]` + 兜底 `unknown`）、`async_create_entry`、strings.json 文案结构、唯一性（`async_set_unique_id` + `_abort_if_unique_id_configured`）、Options Flow（`async_get_options_flow` + `async_step_init` + `add_suggested_values_to_schema`）、`data` 不可变 vs `options` 可变、`ConfigEntryNotReady` vs `ConfigEntryAuthFailed` 异常语义（自动重试 vs 触发 reauth）。reauth/reconfigure 只点到不深入，不展开 OAuth2 进阶。
- **素材引用**：一.4、一.7（ConfigEntry 语义相关）、二
- **代码示例**：有（官方 detailed_hello_world_push 的 `config_flow.py` 表单示例、`strings.json` 结构、OptionsFlow 骨架）
- **大白话设计**：Config Flow 是「门禁卡申请流程」——用户填申请表（表单），校验通过后发一张门禁卡（config entry）；`options` 是拿到卡后可在前台调整的偏好（如保险箱里的可调设置）；`unique_id` 是门禁卡上的唯一编号，禁止用 IP/设备名。

### 第 5 章：Entity 平台与 Sensor 实体

- **篇幅**：中（约 2500-3000 字）
- **覆盖要点**：平台装载机制（`async_forward_entry_setups` 把 sensor 平台接进来）、每个平台实现 `async_setup_entry(hass, entry, async_add_entities)` + `async_add_entities` 注册、Entity 状态机基础（`available`、`should_poll`、`_attr_` 类属性、**属性 getter 禁止 I/O**）、`has_entity_name=True` 强制项、`unique_id`（平台内唯一、关联 entity registry）、`device_info` 自动注册 device registry、声明式实体写法（`SensorEntityDescription` 子类 + `value_fn`，参考 mops_pm25）、`CoordinatorEntity` 基类作为与第 6 章的衔接点。
- **素材引用**：一.5（Entity 部分）、一.6、二、三
- **代码示例**：有（`sensor.py` 实体类、`SensorEntityDescription` 声明式子类、`async_setup_entry` + `async_add_entities` 骨架）
- **大白话设计**：Entity 是「柜台展示员」，sensor 实体把数据摆上货架；`_attr_` 类属性是「商品的固定标签」，读内存不发网络请求。

### 第 6 章：DataUpdateCoordinator 数据轮询

- **篇幅**：长（约 3000-3500 字）
- **覆盖要点**：Coordinator 职责、`_async_update_data` 用 `asyncio.timeout(10)` 包裹网络请求、异常语义（认证失败抛 `ConfigEntryAuthFailed`、一般错误抛 `UpdateFailed`、限流抛 `UpdateFailed(retry_after=60)`、`asyncio.TimeoutError`/`aiohttp.ClientError` 内部已处理）、多实体共享一次轮询（`context=idx` 区分订阅者）、`async_config_entry_first_refresh()` 失败抛 `ConfigEntryNotReady` 自动重试、`_async_setup` 一次性初始化（HA 2024.8+）、`entry.runtime_data` 存放 coordinator（优于 `hass.data[DOMAIN]`）、**架构铁律：集成内不放协议代码，API 交互封装成独立 PyPI 库**、推送模型简述（`async_set_updated_data` / dispatcher 成对订阅退订）。
- **素材引用**：一.5（Coordinator 部分）、一.6、二、三
- **代码示例**：有（`coordinator.py` 骨架、API client 独立封装示例、`async_setup_entry` 中 coordinator 接线与 `async_add_entities`）
- **大白话设计**：Coordinator 是「仓库统一收货员」，多个柜台（实体）共享一份到货数据，不用每家各跑一趟；`update_interval` 只在有人来看货时才去收货。

### 第 7 章：测试与调试

- **篇幅**：中（约 2500-3000 字）
- **覆盖要点**：pytest-homeassistant-custom-component 插件（`conftest.py` 声明 `pytest_plugins`、直接用 `hass` fixture、从 `common` 导入 `MockConfigEntry`、`enable_custom_integrations` 必需且 `recorder_mock` 要先初始化）、测试断言走核心接口（`hass.states` / `hass.services` / registries，不碰内部细节）、pytest 命令与 `asyncio_mode = auto`、debugpy 断点调试（`configuration.yaml` 加 `debugpy:`、`-Xfrozen_modules=off` 启动、`justMyCode: false`、pathMappings 对应 `custom_components`）、logger 配置（`custom_components.<domain>: debug`、manifest 加 `loggers` 键修复 UI 调试按钮失效）、`hass --script check_config` 排障。
- **素材引用**：一.7、一.8、三、四
- **代码示例**：有（`conftest.py`、一条 sensor 平台测试用例、`configuration.yaml` 调试配置片段）
- **大白话设计**：测试是「入职考试」——不考内部小动作，只看对外表现（状态、服务、注册表）；debugpy 是「随身体检仪」，断点命中时整个 HA 会暂停。

### 第 8 章：HACS 分发

- **篇幅**：短（约 1500-2000 字）
- **覆盖要点**：hacs.json 字段（必填 `name`，可选 `content_in_root`/`zip_release` 等）、manifest 至少含 6 个必填字段（domain/documentation/issue_tracker/codeowners/name/version）、hassfest Action 与 hacs/action 双保险、版本取 Release tag（**仅 push tag 不建 Release 无效**）、HACS 更新机制（GitHub API 拉取 release、版本存 `manifest.json` 的 `version`、下载后需重启生效）。
- **素材引用**：一.9、三、四
- **代码示例**：有（`hacs.json`、`.github/workflows/hassfest.yaml` 与 hacs/action workflow 片段）
- **大白话设计**：HACS 是「集成界的应用商店」——上架（hassfest + hacs/action 校验）后，其他用户就能搜到并一键安装你的集成。

### 第 9 章：常见坑与最佳实践

- **篇幅**：中（约 2000-2500 字）
- **覆盖要点**：常见坑清单（manifest 缺 `version`、`domain` 与目录名不一致、requirements 不固定版本、asyncio 阻塞/属性 getter 做 I/O、`ConfigEntryNotReady` vs `ConfigEntryAuthFailed` 用错、调试日志不生效、debugpy 断点不命中、EntitySelector 留空 `vol.Invalid`、Mosquitto 非预装、HACS 版本不更新）+ 最佳实践（集成代码薄、协议逻辑放独立 PyPI 库、`entry.runtime_data`、多实体共享 coordinator、`_attr_` + `SensorEntityDescription`、reauth/reconfigure 用官方 helper、测试断言走核心接口、分发双 action）。
- **素材引用**：三、一.6、四
- **代码示例**：无（以表格清单为主）
- **大白话设计**：以「排错清单 + 体检报告」形式收尾，逐条给「症状 → 原因 → 修法」。

---

## 学习路径说明

### 前置要求

- 会用 Home Assistant（在「设置 → 设备与服务」配过集成、理解设备/实体基本概念）
- 会基础 Python 与 async/await 语法（协程、`await`、`asyncio` 概念）
- 能看懂 YAML 与 JSON（HA 配置与 manifest.json 都是这类格式）
- 会基本 Git 操作（fork / clone / commit / push 即可，分发章节要用）

### 学完能做什么

- 用 Dev Container 一键搭好 HA 自定义集成开发环境，F5 可断点调试
- 读懂并能手写一个合法的 `manifest.json`，理解每个核心字段的含义
- 用官方脚手架生成骨架，实现一个带表单配置流程（config flow）的集成
- 用 DataUpdateCoordinator 轮询一个外部 API，暴露 1-2 个 sensor 实体
- 用 pytest 给自定义集成写基础测试，用 debugpy + logger 定位问题
- 走通 HACS 分发（hassfest + hacs/action + Release tag），让集成可被安装

### 建议学习顺序

| 顺序 | 章节 | 内容 | 预计耗时 |
|------|------|------|----------|
| 1 | 第 1-2 章 | 理解概念 + 搭好开发环境 | 约 1-2 小时 |
| 2 | 第 3 章 | 写出能加载的最小集成骨架 | 约 1 小时 |
| 3 | 第 4 章 | 实现 config flow 配置流程 | 约 2 小时 |
| 4 | 第 5-6 章 | 接入数据并暴露 sensor 实体（核心） | 约 2-3 小时 |
| 5 | 第 7 章 | 测试与调试 | 约 1-2 小时 |
| 6 | 第 8-9 章 | 分发 + 排错复习 | 约 1-2 小时 |

> 建议按「第 5 章 → 第 6 章」顺序阅读，先学会实体怎么写，再接入数据轮询；第 4、6 章是本笔记两处重点，值得放慢速度。

---

## 素材引用对照表（02_deep_research.md 章节编号）

| 编号 | 素材内容 |
|------|----------|
| 一.1 | 开发环境搭建（Dev Container / venv / 脚手架） |
| 一.2 | 集成目录结构 |
| 一.3 | manifest.json 字段 |
| 一.4 | Config Flow 配置流程 |
| 一.5 | Entity 平台 + DataUpdateCoordinator |
| 一.6 | Services / 异步纪律 |
| 一.7 | 测试 |
| 一.8 | 调试 |
| 一.9 | HACS 分发 |
| 二 | 实战代码/项目案例（官方示例、blueprint、mops_pm25、Plex） |
| 三 | 常见坑 / 最佳实践 |
| 四 | 工具链 / 生态 |
| 五 | 进阶路径 / 学习资源 |
| 七 | 综合分析 |
