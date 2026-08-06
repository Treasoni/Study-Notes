## 第七章 场景模板与自动化：packages 与 Blueprint

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §5、§6（时效性修正 #5）
> 前置关联：第 5 章（MVP 预置清单）、第 6 章（entity_map.yaml）

> [!summary] 本章回答三个问题
> 1. 预置的 custom_components 怎么组织、怎么锁版本、哪些东西绝不能进仓库？
> 2. 回家 / 离家 / 睡眠这类场景，怎么用 packages 模板化成一个可复制的 YAML 结构？
> 3. HA 的 YAML 没有变量，多客户复制怎么办？改了配置到底重载还是重启？

第 6 章的 AI 智能体解决了「一句话控制设备」，但真实家庭里最高频的动作不是对话，而是例行场景：进门开灯、离家全关、睡前切夜灯。这些场景不该每次都让用户开口说一遍，而应该在触发条件满足时自动执行。本章进入核心平台层的自动化引擎，解决「场景怎么模板化、怎么复制到多个客户」的 YAML 工程问题——这是把单机系统变成可交付产品的最后一层能力。

### 7.1 custom_components 预置布局与版本锁定

先看「打进镜像的组件」长什么样。第 5 章给出的 MVP 预置清单（xiaomi_home / localtuya / midea_ac_lan / gree / hon）在镜像里就是一个标准目录布局[深度收集 §5](../02_deep_research.md)：

```text
config/
└── custom_components/
    ├── xiaomi_home/        # MVP #1：米家官方集成（锁 tag v0.4.7）
    │   ├── __init__.py     # 组件入口，setup 逻辑
    │   ├── manifest.json   # 元信息：domain / name / version
    │   ├── config_flow.py  # 界面配置向导
    │   └── ...
    ├── localtuya/          # MVP #2：涂鸦本地
    ├── midea_ac_lan/       # MVP #3：美的全本地
    └── hon/                # MVP #5：海尔（高级/易碎）
```

每个组件的核心是 `manifest.json`。它以 `domain` 唯一标识组件，`version` 是版本锚点（以下为示意，真实 manifest 字段更多）：

```json
{
  "domain": "xiaomi_home",
  "name": "Xiaomi Home",
  "version": "0.4.7",
  "config_flow": true,
  "codeowners": ["@XiaoMi"]
}
```

为什么版本锁定这么重要？**没有 HACS = 没有自动更新**。组件更新的唯一时机是 install.sh 或你自己替换目录。第 5 章提到 xiaomi_home 的 `battery_level` 弃用告警截至 v0.4.7 未修复（HA 2026.8 移除），如果镜像里混进一个更新的版本，告警可能变成错误。工程上守住两条纪律：

1. **manifest `version` 对齐发布 tag**：镜像构建时按 tag 检出（如 `v0.4.7`），manifest 里的 version 必须与 tag 一致；
2. **CI 校验防漂移**：写一个检查脚本，比较检出 tag 与 manifest version，不一致直接让构建失败。

> [!warning] 绝不提交客户凭据
> custom_components 目录、packages、脚本里只放代码和模板。设备 token、网关 key、`local_key`、客户凭据一律不能进仓库——`.env` 与真实的 `entity_map.yaml` 必须进 `.gitignore`。镜像打包时也要确认没有把客户 A 的 token 打进准备给客户 B 的镜像。

### 7.2 packages 场景模式

#### 加载方式：!include_dir_named

场景配置按「一个场景一个文件」组织。在 `configuration.yaml` 里声明 packages 目录：

```yaml
homeassistant:
  packages: !include_dir_named packages
```

`!include_dir_named` 会把 `config/packages/` 下的每个文件按**文件名（去扩展名）**作为 key 加载。这个 key 必须是合法 domain（小写字母 / 数字 / 下划线，不能有连字符、空格或中文）——否则该 package 会被静默跳过，只在日志里留一条 warning，非常容易踩。

> [!note] 文件 key = package 名
> `packages/home.yaml` → key 为 `home`。`home`、`away`、`sleep` 都是合法 domain。别命名成 `home-scene.yaml`（连字符非法）或 `回家.yaml`（中文非法）。

#### 场景三件套：input_boolean + script + automation

每个场景由三件套组成，各司其职：

| 组件 | 角色 | 为什么需要 |
|------|------|-----------|
| `input_boolean` | 模式开关 | 持久记录当前模式，供其他自动化做条件判断，也能在 UI / 语音 / Agent 里手动切换 |
| `script` | 动作序列 | 可复用的动作清单，automation、UI、Agent 都能调，避免动作散落各处 |
| `automation` | 触发 | 监听触发条件（开门 / 人离开 / 按钮），满足时调用对应 script |

一个完整的回家场景 `packages/home.yaml`：

```yaml
# packages/home.yaml —— 文件 key = "home"
input_boolean:
  home_mode:
    name: 在家模式
    icon: mdi:home-heart

script:
  scene_home:
    alias: 回家场景
    mode: single
    sequence:
      - service: light.turn_on
        target:
          entity_id: light.living_room_ceiling
        data:
          brightness: 255
          color_temp: 400
      - service: climate.set_temperature
        target:
          entity_id: climate.living_room_ac
        data:
          temperature: 26
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.home_mode   # 最后置位，标记已进入「在家」模式

automation:
  - alias: 回家触发（开门）
    mode: single
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door
        to: "on"
        for:
          seconds: 2                            # 防抖：避免门一碰就触发
    condition:
      - condition: state
        entity_id: input_boolean.home_mode
        state: "off"                            # 已「在家」就不再重复执行
    action:
      - service: script.scene_home
```

关键设计点：

- **`input_boolean` 放在 sequence 最后置位**：先执行完动作、再翻转模式标记。配合 condition 判断「当前不在目标模式」，保证场景只执行一次；
- **`mode: single`**：防止脚本 / 自动化在运行中被重复触发叠加；
- **condition 用模式开关而非直接判断**：即使触发条件多次满足，模式已置位就不会重复执行，这是场景幂等性的核心。

离家与睡眠是同一套模式，只换触发与动作。离家 `packages/away.yaml` 以「人离开 home 区域」为触发、关灯 / 关空调 / 关插座为动作，最后置位 `input_boolean.away_mode`：

```yaml
# packages/away.yaml
input_boolean:
  away_mode:
    name: 离家模式
    icon: mdi:shield-home

script:
  scene_away:
    alias: 离家场景
    mode: single
    sequence:
      - service: light.turn_off
        target:
          entity_id: light.living_room_ceiling
        data:
          transition: 2                        # 2 秒渐暗，不突兀
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.living_room_ac
        data:
          hvac_mode: "off"
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.away_mode

automation:
  - alias: 离家触发（人离开）
    mode: single
    trigger:
      - platform: state
        entity_id: person.owner
        to: "not_home"                         # 离开 home 区域后 person 状态为 not_home
    action:
      - service: script.scene_away
```

睡眠 `packages/sleep.yaml` 同理，差异在动作语义——关客厅灯、夜灯调到微亮、卧室空调 25℃、以床头按钮触发。三个模式开关合在一起还能做交叉条件，比如「睡眠模式下，夜间自动化只开夜灯不开客厅灯」。

#### 改动后：重载还是重启

改 YAML 和改组件代码，生效方式完全不同：

| 改了什么 | 生效方式 | 命令 / 入口 |
|----------|----------|-------------|
| 单个 automation / script | 重载 | `automation.reload` / `script.reload`（UI：开发者工具 → YAML） |
| packages / configuration.yaml | 重载核心配置 | `homeassistant.reload_core_config` |
| custom_components 的 Python 代码或 manifest | 必须完整重启 | `homeassistant.restart` 或 `docker compose restart homeassistant` |

> [!warning] 组件改动重载不生效
> custom_components 在 HA 启动时加载进进程，改了 `__init__.py` 只重载 YAML 不会生效，必须完整重启。Container 部署没有 `ha` CLI，重启走 `docker compose restart homeassistant` 或 REST `POST /api/services/homeassistant/restart`。

### 7.3 Blueprint 使用与限制

Blueprint 是「自动化模板」：把一段可复用的自动化抽成模板，声明输入项（input），使用时只需填输入。文件放在 `config/blueprints/automation/<author>/<file>.yaml`[深度收集 §5](../02_deep_research.md)。

一个最小「开门亮灯」Blueprint：

```yaml
# config/blueprints/automation/myco/door_light.yaml
blueprint:
  name: 开门亮灯
  domain: automation
  input:
    trigger_entity:
      name: 触发传感器
      selector:
        entity:
          domain: binary_sensor
    target_light:
      name: 目标灯
      selector:
        entity:
          domain: light
    brightness:
      name: 亮度（0-255）
      default: 255
      selector:
        number:
          min: 1
          max: 255

trigger:
  - platform: state
    entity_id: !input trigger_entity
    to: "on"

action:
  - service: light.turn_on
    target:
      entity_id: !input target_light
    data:
      brightness: !input brightness

mode: single
```

实例化：在 automation（或 packages 里的 automation 段）用 `use_blueprint` 引用，`path` 相对 `config/blueprints/automation/`：

```yaml
automation:
  - alias: 门口亮灯（客厅）
    use_blueprint:
      path: myco/door_light.yaml
      input:
        trigger_entity: binary_sensor.front_door
        target_light: light.living_room_ceiling
        brightness: 200
```

Blueprint 的边界要清楚：

- **无内置版本 / 自动更新**：Blueprint 没有版本概念，改了模板文件不会自动同步到已实例化的自动化，需要自己管理分发；
- **adaptive_lighting 是 custom component**：不是 Blueprint。它提供「随时间缓慢调节色温 / 亮度」的能力，需要预置到 custom_components；可以再配一个 scheduler blueprint 按时间切换它的模式；
- **auto_climate 不存在**：这是报告里的过时结论（时效性修正 #5）[深度收集 §6](../02_deep_research.md)。需要「按设定温控」时，用通用 climate blueprint 或自建，不要去找一个不存在的组件。

> [!tip] 什么时候用 Blueprint 而不是 package
> 场景（回家 / 离家 / 睡眠）需要 input_boolean 状态和跨 domain 动作，用 package 更直接；单个「一个触发 → 一组动作」的通用逻辑（开门亮灯、温度到点切换）适合抽成 Blueprint 给不同实体复用。

### 7.4 YAML 无变量问题的构建期替换

HA 的 YAML 配置里没有变量（运行时 Jinja2 模板只作用在自动化内部，配置文件的实体引用是静态的）。同一套场景模板，客户 A 的客厅灯是 `light.living_room_ceiling`，客户 B 可能是 `light.kt_ceiling`——实体 ID 因客户而异。多客户复制必须在**构建期**替换实体引用。

最轻量的方式是 `envsubst`：模板里写环境变量占位，构建时按客户注入：

```yaml
# config.template/packages/home.yaml.tpl
script:
  scene_home:
    alias: 回家场景
    sequence:
      - service: light.turn_on
        target:
          entity_id: $LIVING_ROOM_LIGHT        # 占位，构建期替换
        data:
          brightness: 255
```

```bash
# 构建期：每个客户一组环境变量
export LIVING_ROOM_LIGHT="light.living_room_ceiling"   # 客户 A
export LIVING_ROOM_AC="climate.living_room_ac"
envsubst < packages/home.yaml.tpl > config/packages/home.yaml
# 渲染完先校验再重启
hass --script check_config
```

实体一多，`envsubst` 的变量会失控。更可维护的是 `jinja2`——模板支持变量、循环、条件，变量来源可以直接复用第 6 章的 `entity_map.yaml`：

```jinja
{# packages/home.yaml.j2 #}
script:
  scene_home:
    alias: 回家场景
    sequence:
      - service: light.turn_on
        target:
          entity_id: {{ living_room_light }}
        data:
          brightness: 255
```

```bash
jinja2 packages/home.yaml.j2 \
  -D living_room_light="light.living_room_ceiling" \
  -D living_room_ac="climate.living_room_ac" \
  > config/packages/home.yaml
```

> [!note] 本章的替换是第 8 章三层分离的底层机制
> 这里只解决「一个文件怎么渲染成客户配置」。第 8 章的 `config.template/ → customers/<id>/ → 运行时 /config` 三层结构里，实体引用由 codegen 按 entity_map 重写，用的就是这套构建期替换，并统一跑 `hass --script check_config` 校验。

### 本章小结

- custom_components 标准布局 = `config/custom_components/<domain>/`（`__init__.py` + `manifest.json` + `config_flow.py`）；无 HACS 无自动更新，manifest version 必须对齐 tag 并由 CI 校验防漂移；token / 网关 key / 客户凭据绝不进仓库。
- packages 用 `!include_dir_named packages` 按文件名加载，文件 key 必须是合法 domain，否则被静默跳过。
- 场景三件套 = `input_boolean`（模式开关）+ `script`（动作序列）+ `automation`（触发）；回家 / 离家 / 睡眠各一个 package，用 `mode: single` 和「先动作后置位」保证幂等。
- 改 YAML 用重载（`automation.reload` / `homeassistant.reload_core_config`），改 custom_components 代码必须完整重启。
- Blueprint 放在 `config/blueprints/automation/<author>/<file>.yaml`，用 `use_blueprint` 实例化；无内置版本更新；adaptive_lighting 是 custom component，auto_climate 不存在需自建。
- HA YAML 无变量，多客户用 envsubst / jinja2 在构建期替换实体引用，渲染后跑 `hass --script check_config` 校验。

---

下一章把单机的场景能力升级成产品：你会看到 `config.template/` 模板层怎么与每个客户的 `entity_map.yaml` 分离，三种分发渠道（git clone + install.sh / Blueprint 导入 / 预打包镜像）怎么选，以及报告里那 6 处过时结论如何统一回顾。

## 第八章 产品化复制与时效性风险

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §5、§6、§7、§8
> 前置关联：[[Home Assistant 三种部署方式对比与选型.md]]、[[04_无头onboarding自动化|第四章 无头 onboarding]]、[[07_场景模板与自动化|第七章 场景模板与自动化]]

> [!summary] 本章回答三个问题
> 1. 一个人把系统做出来后，怎么复制给多个客户而不互相污染？
> 2. git clone / Blueprint / Docker 镜像三种分发渠道各适合谁？
> 3. 报告里哪些结论已经过期、哪些决策还悬而未决？

前七章你已经把「一键部署 → 跨品牌接入 → AI 对话 → 场景自动化」整条链路在自己机器上跑通了。但「自己跑通」和「复制给多个客户」之间隔着两道坎：一是怎么在不泄露每个客户密钥、不被上一个客户的设备 ID 污染的前提下重复交付；二是你基于桌面报告得出的一堆结论，哪些会随官方弃用和上游版本迭代而失效。本章就是把这套系统「产品化」的最后一公里：先给出三层分离的复制策略，再对比三种分发渠道，最后把报告 6 处时效性修正和 7 项待实测决策一次性盘点清楚，并给出一份可执行的维护节奏。

### 8.1 三层分离复制策略

先想清楚一个问题的本质：**多个客户之间的差异到底在哪？** 其实只有两处——密钥（DeepSeek API Key、品牌设备的 token 与网关 key）和实体映射（同一个「客厅灯」，在客户 A 是 `light.living_room_1`，在客户 B 是 `light.living_room_2`）。如果直接复制整个 `config` 目录，会连上一个客户的设备 token、网关 key、实体 ID 一起带过去，既泄露密钥，又把场景模板污染成「只对上一个客户有效」。

所以复制策略的核心是**把差异隔离到最小范围**，用三层结构把「可公开的模板」和「每个客户独有的配置」分开[深度收集 §5](../02_deep_research.md)：

```text
ai-smart-home-system/
├── config.template/            # 模板层：无密钥，可入库
│   ├── configuration.yaml
│   ├── custom_components/      # 预置组件，manifest version 锁 tag
│   ├── packages/               # 回家/离家/睡眠场景（!include_dir_named）
│   └── blueprints/             # 通用 automation blueprint
├── customers/
│   ├── _template/              # 客户配置空模板
│   │   ├── .env.example
│   │   └── entity_map.example.yaml
│   └── customer-B/             # 真实客户层：不入库（gitignore）
│       ├── .env                # TZ / DEEPSEEK_API_KEY / HA_IMAGE / AGENT_IMAGE
│       └── entity_map.yaml     # 口语别名 → 该客户实体 ID
├── scripts/
│   ├── install.sh              # 一键部署入口
│   └── render_config.sh        # 模板 + 客户配置 → 运行时 /config
└── docker-compose.yml          # 全部用 ${VAR} 参数化
```

三层各自的定位：

| 层 | 内容 | 是否入库 | 改动频率 |
|------|--------|----------|----------|
| `config.template/` | 无密钥配置、预置组件、场景模板 | 是 | 产品升级时 |
| `customers/<id>/` | `.env` + `entity_map.yaml` | 否（gitignore） | 每个客户部署时 |
| 运行时 `/config` | 渲染生成的实际配置 | 否 | 每次部署生成 |

三层的意义在于**让「可以分享」和「必须保密」永远不混在一起**：

- **模板层**没有任何密钥，可以公开、可以入库、所有客户共享一份。第 7 章预置的 `custom_components`、packages 场景、blueprint 都放这一层。
- **客户层**只放每个客户独有的两个文件，且由 `.gitignore` 强制排除——绝不提交设备 token、网关 key、客户凭据[深度收集 §5](../02_deep_research.md)。
- **运行时层**永远由脚本渲染生成，而不是手工拷贝，保证「渲染出来的就是校验过的」。

渲染与校验的流程（示意）如下。因为 HA 的 YAML 没有变量机制，多客户的实体引用要在**构建期**用 `envsubst` / jinja2 / codegen 替换[深度收集 §5](../02_deep_research.md)：

```bash
# render_config.sh 关键步骤（示意）
render_config() {
  local customer="$1"
  local out="${2:-./config}"            # 运行时 /config
  rm -rf "$out" && cp -r config.template/. "$out"   # 1. 复制模板层

  # 2. 注入客户 .env 变量（HA YAML 无变量 → 构建期替换）
  set -a; source "customers/$customer/.env"; set +a
  envsubst < "$out/configuration.yaml" > "$out/configuration.yaml.tmp"
  mv "$out/configuration.yaml.tmp" "$out/configuration.yaml"

  # 3. codegen 按 entity_map 重写 packages 里的实体引用
  python3 scripts/codegen_entities.py \
    --map "customers/$customer/entity_map.yaml" \
    --dir "$out/packages"

  # 4. 校验（容器内执行）
  docker exec homeassistant hass --script check_config -c /config
}
```

最后一步的 `hass --script check_config` 是上线前必做的闸门：它会把 configuration、packages、blueprint 全部解析一遍，任何写错的 domain、引用了不存在的实体、YAML 语法错误都会在这里暴露，而不是等客户运行时才发现。

### 8.2 三种分发渠道对比

三层分离解决的是「配置怎么组织」，分发渠道解决的是「成品怎么送到客户手里」。三种渠道的适用对象完全不同[深度收集 §2、§5](../02_deep_research.md)：

| 维度 | git clone + install.sh | HA Blueprint 导入 | Docker 预打包镜像 |
|------|------------------------|--------------------|--------------------|
| 交付对象 | 整个系统（config + Agent + compose） | 仅自动化/场景层 | 整个系统（打成镜像） |
| 客户前提 | 有 Docker 主机，能跑命令行（或部署人员代跑） | 已有一个 HA 实例 | 有 Docker 主机，一条命令 |
| 安装动作 | `git clone` + `./install.sh` | 下载 yaml → UI 导入 | `docker pull` + `run` / compose |
| 可审计性 | 高（全量源码可见） | 中（只有场景） | 低（黑盒镜像） |
| 更新方式 | `git pull` + 重新渲染 | 手动替换 yaml | 重新拉新 tag 镜像 |
| 典型适用 | 技术型客户 / 部署团队代跑 | 已有 HA 的进阶用户 | 完全非技术用户的「产品化」交付 |

**渠道一：git clone + install.sh（主渠道）**。项目本身是一个 git 仓库，`config.template` + `scripts` + `docker-compose.yml` + Agent 源码全在里面，放在 Gitee 上（国内拉取更快）。复制给第二个客户 = 克隆仓库 + 建 `customers/<id>` + 跑一条命令。它的可审计性最高——交付给客户的就是仓库本身，部署人员能看到每一步在做什么，排错时可以翻到第 3 章的 `install.sh` 逐段核对。复制流程如下：

```bash
# 场景：为第 2 个客户 customer-B 复制一套部署
# 1. 克隆项目仓库
git clone https://gitee.com/your/ai-smart-home-system.git ~/ha-deploy
cd ~/ha-deploy

# 2. 创建客户配置层（.env 与 entity_map.yaml 不入库）
mkdir -p customers/customer-B
cp customers/_template/.env.example customers/customer-B/.env
cp customers/_template/entity_map.example.yaml customers/customer-B/entity_map.yaml

# 3. 编辑该客户的密钥与实体映射
vim customers/customer-B/.env            # DEEPSEEK_API_KEY / TZ / 镜像变量
vim customers/customer-B/entity_map.yaml # "客厅灯" → 该客户的 light.xxx

# 4. 一条命令渲染 + 拉起
./install.sh --customer customer-B

# 5. 校验运行时配置（容器内）
docker exec homeassistant hass --script check_config -c /config
```

注意 `install.sh` 与第 3 章的差别：多了 `--customer` 参数后不再交互式询问 `.env`，而是直接读取 `customers/<id>/.env`，再按 8.1 的三层流程渲染。「第二个客户」的部署就收敛成**新建目录 + 填两个文件 + 跑一条命令**，全程不接触第一个客户的任何密钥。

**渠道二：HA Blueprint 导入**。最轻，只把自动化场景做成 blueprint yaml 交给已有 HA 的用户，路径 `config/blueprints/automation/<author>/<file>.yaml`，UI 里 `use_blueprint:` 实例化。它的局限很明显：不包含 Agent、不包含 onboarding、不包含镜像链——只交付「场景」这一小块。适合已有 HA 的老用户想直接借用你的回家/离家/睡眠模板，不适合交付整套系统。

**渠道三：Docker 预打包镜像**。最接近「产品」的形态：把 HA + 预置 custom_components + 场景 + Agent 打成一个镜像，客户只 `docker pull` + 一条 `compose up` 就完事。但有两个硬约束必须提前想清楚：一是**客户差异（密钥、实体映射）绝不能进镜像**，只能通过环境变量或挂载卷注入，否则镜像一泄露就等于把所有客户的密钥泄露——这正好又绕回 8.1 的三层分离；二是分发通道本身受限制，阿里云 ACR 个人版新实例不支持匿名拉取、必须 `docker login`[深度收集 §2](../02_deep_research.md)，这直接影响「客户怎么拿到镜像」，详见 8.4 事项 7。

### 8.3 时效性修正清单回顾

第 1 章提过，桌面报告里有 6 处过时信息需要修正。把这份清单完整回顾一遍，因为它代表一类**结构性风险**：上游（HA 官方 / DeepSeek / 各品牌仓库）随时可能再次弃用或改接口，修正不是一次性动作[深度收集 §6](../02_deep_research.md)：

| # | 报告说法 | 2026-08 现状修正 | 对本项目的意义 |
|---|---------|------------------|----------------|
| 1 | Supervised 作为部署底座 | Container 为主 + HAOS 为辅（Supervised 2025.12 弃用） | 部署形态整体改写，`install.sh` 变成「编排容器」而非「引导安装向导」 |
| 2 | 用 `deepseek-chat` | 改用 `deepseek-v4-flash`（旧名 2026-07-24 停用） | Agent 的模型名、thinking、tool_choice 都要按 V4 写 |
| 3 | ACR 个人版镜像站可匿名拉取 | 不能匿名，须 `docker login`；ghcr 走代理链 | 镜像分发渠道必须重新决策（见 8.4 事项 7） |
| 4 | 预置 `xiaomi_gateway3` | 改用米家官方 `xiaomi_home` | 米家接入换成官方 OAuth 路线，预置清单改写 |
| 5 | 存在 `auto_climate` blueprint | 不存在，需自建或换通用 climate blueprint | 场景模板不能照抄报告，第 7 章已改为自建 |
| 6 | 华为可接入 | 无可靠路径，只给指引（Matter / 反向控制） | 华为从「可接入」降级为「文档指引」 |

注意第 1 和第 2 项是「已经发生且不可逆」的硬变更，第 3-6 项是「事实与报告不符」的修正。这张表的价值在于：它既是本项目与桌面报告所有分歧点的索引，也是以后每次升级前要逐条复核的检查清单。

### 8.4 待实测与产品决策事项（7 项）

如果说 8.3 是「过去的信息需要修正」，这里就是「现在的信息还不够」。7 项事项决定了首版产品敢承诺什么、不敢承诺什么，每一项都对应一个明确的追踪来源[深度收集 §7](../02_deep_research.md)：

| # | 事项 | 要实测/决策什么 | 影响范围 | 追踪来源 |
|---|------|----------------|----------|----------|
| 1 | 镜像链大陆实测 | `ghcr.nju.edu.cn` / `ota.hasscn.top` 在中国大陆家庭宽带的真实可用性 | 第 2 章回退链顺序、`install.sh` 默认值 | 社区镜像源汇总 / 瀚思彼岸论坛 |
| 2 | `xiaomi_home` 弃用告警 | 是否已有 v0.4.8+ 修复 `battery_level`（HA 2026.8 将移除该属性） | HA Core 版本锁定策略、米家接入稳定性 | XiaoMi/ha_xiaomi_home Releases & Issues |
| 3 | 美的 V3 token | NetHome Plus Token 接口对中国区新设备是否仍可用 | 美的接入承诺（能否写进 MVP 向导） | wuwentao/midea_ac_lan（Issue #530） |
| 4 | onboarding API 有效性 | 在 2026 stable（2026.7.x）上是否仍有效 | 「5 分钟承诺」边界、是否回退 `.storage`/浏览器向导 | home-assistant.io onboarding / HA Community |
| 5 | 第三方工具依赖取舍 | 是否接受 `Xiaomi-cloud-tokens-extractor`、`msmart-ng` 取 token | 合规风险、首次人工步骤清单 | 各工具仓库 |
| 6 | 首版主推品牌组合 | 阶段 C 品牌向导先做哪几个品牌 | 向导工作量、5 分钟承诺范围 | 设备保有量调研 |
| 7 | Agent 镜像分发通道 | ACR 私有 vs Docker Hub 公开 vs 自建 registry | 部署体验、客户密钥安全 | ACR 文档 / Docker Hub |

前 4 项是**纯技术待实测**，实测结论直接改写第 2、5 章的默认参数；后 3 项是**产品决策**，决定首版的承诺边界和合规姿态。特别是第 5 项，使用第三方工具提取品牌 token 属于「借道」官方未提供的接口，要在 MVP 阶段就明确接受程度，而不是等上线后再补。

**阅读与维护建议**：上游变更节奏并不一致——HA 官方每月一个大版本，breaking changes 集中在 release notes；DeepSeek 的模型与定价在 api-docs.deepseek.com 更新；各品牌仓库以 tag 和 Issue 为主[深度收集 §8](../02_deep_research.md)。建议按这个节奏维护：

1. **季度复查**：每季度把 8.3 的 6 项清单和 8.4 的 7 项事项各过一遍，看是否有新的弃用公告或修复。
2. **升级前强制检查**：每次 HA 大版本升级前，必须重跑一遍 8.3 清单——升级本身就可能是新的「时效性修正」。
3. **订阅关键来源**：home-assistant.io release notes、api-docs.deepseek.com、`XiaoMi/ha_xiaomi_home`、`wuwentao/midea_ac_lan`（Issue #530）、`xZetsubou/hass-localtuya`、`mmalolepszy/hon-revived`。
4. **用版本锁定防漂移**：第 7 章的做法继续沿用——`manifest.json` 的 version 对齐发布 tag，CI 校验防漂移；无 HACS 就无自动更新，漂移只能靠构建期校验兜住。
5. **实测一项销项一项**：7 项待实测里每解决一项，就回到 `02_deep_research.md` §7 更新状态，避免「以为测过、其实没测」。

### 本章小结

- 三层分离复制策略 = `config.template/`（可入库）→ `customers/<id>/`（`.env` + `entity_map.yaml`，不入库）→ 运行时 `/config`（脚本渲染 + `check_config` 校验），把客户差异隔离到最小范围，密钥永不混入模板。
- 三种分发渠道适用对象不同：git clone + install.sh 是主渠道（可审计、可复现）；Blueprint 只交付场景；Docker 预打包镜像最接近产品，但客户差异必须走环境变量/挂载，且受 ACR 匿名拉取限制。
- 报告 6 处时效性修正已全部采纳，它们代表一类「上游弃用/改接口」的结构性风险，需要持续跟踪而非一次性修复。
- 7 项待实测/决策事项决定首版承诺边界，每项都有明确追踪来源；第 5 项第三方工具依赖属于合规决策，要尽早定调。
- 维护建议 = 季度复查 8.3/8.4 清单 + 每次 HA 大版本升级前强制检查 + 订阅关键上游来源 + 版本锁定防漂移。

---

至此，整条链路闭环了：第 1-2 章选型与地基，第 3-4 章一键部署与无头 onboarding，第 5 章跨品牌接入，第 6 章 AI 智能体，第 7 章场景模板，第 8 章把它变成可以复制、可以持续维护的产品。你现在具备的不只是一套能跑的脚本，而是「如何让它持续能跑」的判断力——这份判断力，正是 8.4 那份待实测清单和时效性清单想教给你的东西。

## 结语

从选型、镜像链、一键部署、无头 onboarding，到跨品牌接入、AI 智能体、场景模板，最后到产品化复制——八章走完，你已拥有从零搭建并持续维护一套跨品牌 AI 智能家居系统的完整能力。这套系统的护城河不在某一段脚本或配置文件，而在「判断什么会变、什么能复用」的工程判断力：第 8 章的时效性修正清单与待实测事项，就是这份判断力的落地载体。按季度复查、升级前强制检查、版本锁定防漂移，这套系统就能随上游一起进化。

---

*本文档由 8 个章节按端到端主线组装而成，生成于 2026-08-05。各章素材来源与前置关联见章节开头；全篇时效性结论以第 8 章 8.3 / 8.4 清单为准。*
