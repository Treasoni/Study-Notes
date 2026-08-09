# 从零开发 Home Assistant 自定义集成 - 探测结果

收集时间: 2026-08-08
搜索关键词: 自定义集成开发入门 / 集成配置使用 / 集成开发测试发布
信源: 官方文档 + 技术博客 + 社区讨论

## 方向菜单

用户已选择方向：**A. 从零开发自定义集成**

| 方向 | 内容 | 难度（零基础/有了解/熟悉） |
|------|------|---------------------------|
| **A. 从零开发自定义集成** ⭐已选 | 用 Python 写 custom integration：开发环境（Dev Container）、manifest.json、Config Flow、Entity 平台、DataUpdateCoordinator，最后 HACS 分发 | 高 / 中 / 低 |
| B. 配置使用现有集成 | 通过「设置→设备与服务」接入米家/涂鸦/ESPHome/MQTT 等现有集成，管理设备与实体，装 HACS | 中高 / 低 / 低 |
| C. 开发进阶：测试/调试/发布 | pytest 测试、Hassfest/HACS Action 校验、debugpy 调试、HACS 发布与官方 core 贡献 | 高 / 中偏高 / 低 |

## 方向 A 探测详情

### 1. 核心知识模块（探测结果）
1. **开发环境搭建** — 官方推荐 VS Code Dev Container（预装 Home Assistant Core、Ruff、mypy、pytest、Mosquitto MQTT broker），也支持本地 venv。硬性要求 Python 3.12+ 与 async/await 熟悉度。
2. **集成基本结构** — `custom_components/<domain>/` 目录布局：`manifest.json`（必需 metadata + 自定义集成**必须**带 `version`）、`__init__.py`（`async_setup` / `async_setup_entry`）、`const.py`、`config_flow.py`、`strings.json`、实体平台文件（如 `sensor.py`、`light.py`）。
3. **manifest.json 元数据** — `domain`（小写下划线、须与目录名一致）、`name`、`codeowners`、`config_flow`、`requirements`（固定版本）、`iot_class`、`integration_type`、`dependencies` / `after_dependencies`、自动发现字段（`zeroconf` / `dhcp` / `bluetooth`）。
4. **Config Flow（配置流程）** — `config_entries.ConfigFlow` 子类 + `VERSION`，`async_step_user` → 表单校验 → `async_create_entry`；`async_set_unique_id` + `_abort_if_unique_id_configured` 防重复；`async_step_reauth` / reconfiguration；UI 文案统一放 `strings.json`。
5. **Entity 平台与 DataUpdateCoordinator** — `async_setup_entry` + `async_add_entities` 注册实体；`SensorEntityDescription` / `CoordinatorEntity` 简化代码；轮询型集成用 `DataUpdateCoordinator`（`_async_update_data`，抛 `ConfigEntryAuthFailed` / `UpdateFailed`）。架构原则：集成不直接调设备 API，封装为 PyPI 第三方库再调用。
6. **Services、States 与测试分发** — 状态机制（`domain.object_id`、状态值必须字符串）；自定义服务；单测/CI 最佳实践；通过 HACS 分发。

### 2. 典型学习路径
1. **搭环境**：装 Docker + VS Code，Fork 示例仓库用 Dev Container 打开，跑通 `Run Home Assistant Core`（`http://localhost:8123`）。
2. **写最小集成**：建 `custom_components/hello_world/`，写 `DOMAIN` + `async_setup` 的 `__init__.py` 和最小 `manifest.json`，在 `configuration.yaml` 加一行加载，验证 HA 启动成功 setup。
3. **跑官方脚手架**：`python3 -m script.scaffold integration` 生成带 config flow、测试和 i18n 的骨架。
4. **加 config flow**：实现 `async_step_user` 表单，接入 `voluptuous` 校验、错误处理与唯一 ID 防重复。
5. **加实体平台**：选 sensor 平台（最易上手），用 `DataUpdateCoordinator` 轮询外部 API，暴露 1-2 个实体。
6. **补全工程细节**：翻译、测试、代码风格、`hass.data[DOMAIN]` 数据共享、dispatcher 通知实体更新。
7. **分发**：打 tag、配置 HACS 所需文件，发布到 GitHub 供他人通过 HACS 安装。

### 3. 关键参考资料
- [Creating your first integration | Home Assistant Developer Docs](https://developers.home-assistant.io/docs/creating_component_index/) — 官方入门
- [Set up development environment | Home Assistant Developer Docs](https://developers.home-assistant.io/docs/development_environment/) — Dev Container 开发环境
- [Integration file structure | Home Assistant Developer Docs](https://developers.home-assistant.io/docs/creating_integration_file_structure/) — 目录结构与 manifest 字段权威说明
- [Config flow | Home Assistant Developer Docs](https://developers.home-assistant.io/docs/core/integration/config_flow/) — config flow 完整约定
- [boralyl/github-custom-component-tutorial](https://github.com/boralyl/github-custom-component-tutorial) — 社区常用实战教程
- [hacs.integration_blueprint](https://github.com/jpawlowski/hacs.integration_blueprint) — 自带 devcontainer 的现代蓝图
- [hasscn.top 开发者文档](https://hasscn.top/developers/docs/add-ons/tutorial/) — 中文对照阅读

### 4. 难度评估
- **零基础**（不懂 Python/HA）：高。门槛集中在 asyncio 异步模型 + HA 事件循环 + 生态概念叠加。
- **有了解**（会 Python、用过 HA、懂基础 async）：中等。官方脚手架 + 示例仓库 + 教程可快速上手，1-3 天能写出带 config flow 的简单 sensor 集成。
- **熟悉者**：低。主要学习质量规范、自动发现字段与多平台扩展。

## 综合分析

- 用户已确认方向 A（从零开发自定义集成），深度「上手」、基础「有了解」，与本方向的中等难度匹配。
- 官方开发者文档（developers.home-assistant.io）是权威信源，探测结果充分，无缺口。
- 学习路径清晰：环境 → 最小集成 → 脚手架 → config flow → sensor 平台 → 工程细节，适合「上手」深度按此推进。
- 下一步进入阶段 2（深度收集），针对方向 A 的核心模块精读官方文档并沉淀 `02_deep_research.md`。
