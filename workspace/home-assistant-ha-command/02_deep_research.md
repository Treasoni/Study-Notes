# Home Assistant 中 ha 命令的使用 - 深度素材

收集时间: 2026-08-06 23:15
方向: A. 完整命令速查手册
信源: 官方文档（home-assistant.io / home-assistant/cli 源码）+ 官方社区 + 技术博客，多源交叉验证

---

## 一、核心概念

### 1.1 ha CLI 本质
- 语法：`ha <group> <command> [args] [flags]`，本质是对 **Supervisor REST API** 的 1:1 封装。
- 顶层命令组（约 19 组）：`addons`（开发版重命名为 `apps`）、`audio`、`authentication`（别名 auth）、`backups`、`banner`、`cli`、`core`、`dns`、`docker`、`hardware`、`host`、`info`、`jobs`、`multicast`、`network`、`observer`、`os`、`resolution`、`supervisor`。
- 开发版新增（尚未入官方 19 组文档）：`mounts`、`security`、`store`。
- 前身是 `hassio-cli`，2020 品牌改名统一为 `ha`。
- 所有 flag 可用 `SUPERVISOR_` 前缀环境变量替代（`SUPERVISOR_ENDPOINT`、`SUPERVISOR_API_TOKEN` 等），可远程调用。

### 1.2 可用环境（关键）
- `ha` **只存在于 HAOS 与 HA Supervised**（带 Supervisor）。
- **Docker Container / Core 直装没有 `ha` 命令**（最常见坑）。
- Supervised 宿主 shell 报 command not found → `docker exec -it hassio_cli bash` 进入 CLI 容器。
- HAOS 控制台默认 `HA>` 提示符，输入 `login` 进入 root shell。
- `shell_command` 集成运行在 Core 容器内，**调不到 `ha`**；改用 `hassio.*` 服务或 Supervisor REST API。
- HA 2025-12 起弃用 Core（venv）/Supervised 安装模式与 32-bit，只支持 HAOS 与 Container；架构仅剩 aarch64/amd64。

### 1.3 命名澄清
- `ha`（当前 CLI，管 Supervisor）≠ `hass-cli`（已弃用的独立 Python 客户端，走 Core REST API 管实体/服务）。
- `ha core` 管 Core Python 应用；`ha supervisor` 管管理/编排层。

### 1.4 进入终端方式
| 方式 | 说明 |
|------|------|
| SSH & Web Terminal addon | OpenSSH + 内嵌 Web Terminal，root 登录，Bash 带 `ha` 补全；可访问宿主机 D-Bus/音频/UART/GPIO/Docker |
| Studio Code Server（VS Code） | 仅 AMD64/aarch64 |
| HAOS 系统控制台 | 键盘+屏幕；本地终端专用命令（datadisk wipe、auth list）仅此处可执行 |

### 1.5 全局 flags
| Flag | 说明 |
|------|------|
| `--api-token string` | Supervisor API token（远程必填） |
| `--endpoint string` | Supervisor 端点（默认 `supervisor`，远程 `http://IP:PORT`） |
| `--config string` | 配置文件（默认 `$HOME/.homeassistant.yaml`） |
| `--log-level string` | 日志级别（默认 WARN） |
| `--no-progress` | 禁用进度动画 |
| `--raw-json` | 输出原始 JSON |
| `-h/--help` | 帮助（`ha <group> --help` 看子命令） |
| 环境变量 | `SUPERVISOR_ENDPOINT` / `SUPERVISOR_API_TOKEN` / `SUPERVISOR_LOG_LEVEL` |

---

## 二、命令参考全集（按组）

### 2.1 ha addons（开发版为 ha apps）
| 子命令 | 用途 | 关键参数 |
|--------|------|---------|
| `addons` | 列出已安装 addon | — |
| `info [slug]` | addon 详情 | 无 slug 默认 self；`--raw-json` |
| `install <slug>` | 安装（只装最新版） | slug 必填 |
| `uninstall <slug>` | 卸载 | slug 必填 |
| `update <slug>` | 升级 | `--version`、`--backup`；别名 upgrade/up；无更新时退出码 1 |
| `start/stop/restart <slug>` | 生命周期控制 | slug 必填 |
| `logs <slug>` | 日志 | `--follow`、`--lines` |
| `stats <slug>` | CPU/内存/网络/磁盘统计 | slug 必填 |
| `rebuild <slug>` | 重建容器镜像 | slug 必填 |
| `changelog <slug>` | 更新日志 | slug 必填 |

**addon slug 来源**：官方 `core_ssh`、`core_mosquitto`；社区 `a0d7b954_adguard`（作者 GitHub ID 前缀）。获取：addon 详情页 URL `/hassio/addon/<slug>/info`，或 `docker ps` 容器名 `addon_<slug>`。

### 2.2 ha core
| 子命令 | 用途 | 关键参数 |
|--------|------|---------|
| `check` | 校验配置语法 | — |
| `info` | 版本/状态 | `--raw-json`（version/version_latest/update_available） |
| `logs` | Core 日志 | `--follow` |
| `options` | 运行选项 | `--boot`、`--image`、`--port`(8123)、`--ssl`、`--watchdog`、`--duplicate-log-file` 等 |
| `rebuild` | 重建 Core 容器 | — |
| `restart` | 重启 | `-s/--safe-mode` 安全模式、`-f/--force`；别名 reboot |
| `start` / `stop` | 启动/停止 | — |
| `stats` | 资源统计 | — |
| `update` | 升级 | `--version x.y.z`、`--backup`；别名 upgrade/downgrade |

### 2.3 ha supervisor
| 子命令 | 用途 | 关键参数 |
|--------|------|---------|
| `info` | 总览（含各组件版本/channel） | — |
| `logs` | Supervisor 日志 | `--follow` |
| `reload` | 轻量重载配置 | — |
| `update` | 升级（升级顺序第一步） | `--version` |
| `options` | 选项 | `-c/--channel` stable\|beta\|dev、`-t/--timezone`、`--auto-update` 等 |
| `restart` | 重启 | — |
| `stats` | 资源统计 | — |
| `repair` | 修复 | — |
| `available_updates` | 列出可用更新 | — |

### 2.4 ha host / ha os（系统级）
| 命令 | 用途 | 注意 |
|------|------|------|
| `ha host reboot` | 重启宿主机 | 立即执行，先备份 |
| `ha host shutdown` | 关机 | 需手动开机 |
| `ha host info` / `ha host options --hostname` | 宿主机信息/改名 | 新版 `ha host --help` 为准 |
| `ha host logs` / `ha host disks` | 启动日志 / 磁盘 | `logs boots`、`disks usage` |
| `ha os update [--version]` | 升级 OS | 先备份保供电；切 boot slot |
| `ha os info` | A/B 双槽版本 | 失败自动回退上一槽 |
| `ha os datadisk wipe` | 抹除数据盘（**本地终端专用**，输入 YES 确认） | 不可逆，全删 |
| `ha os datadisk list/move` | 数据盘列表/迁移 | — |
| `ha os import` | 从 USB 导入配置 | — |
| `ha os config swap options` | swap 设置 | `--swap-size`、`--swappiness`(0-200) |
| `ha os boot_slot` / `ha os boards` | 启动槽/板卡配置 | — |

> 注：`ha host update` 在旧文档出现，新版源码无此子命令，OS 升级走 `ha os update`，以 `ha host --help` 为准。

### 2.5 ha network
| 子命令 | 用途 | 关键参数 |
|--------|------|---------|
| `info` | 网卡 IP/网关/DNS/方法 | `nameservers: []` = DNS 未配置 |
| `update <interface>` | 改接口配置 | `--ipv4-method static\|auto\|disabled`、`--ipv4-address`、`--ipv4-gateway`、`--ipv4-nameserver`、`--wifi-ssid/--wifi-psk`、`--mdns`、`--llmnr` |
| `scan` | 扫描 WiFi | — |
| `reload` | 重载网络配置 | NetworkManager 驱动 |
| `vlan` | VLAN 管理 | — |

示例：`ha network update eth0 --ipv4-method static --ipv4-address 192.168.1.100/24 --ipv4-gateway 192.168.1.1 --ipv4-nameserver 8.8.8.8,8.8.4.4`

### 2.6 ha hardware
- `ha hardware info`：系统硬件信息（`--raw-json`），配合 `ha resolution info` 排兼容性
- `ha hardware audio`：音频设备信息

### 2.7 ha info / ha jobs / ha resolution（诊断）
| 命令 | 用途 | 输出要点 |
|------|------|---------|
| `ha info` | 系统总览 | arch、channel、docker、hassos、homeassistant、hostname、machine、supervisor、timezone、supported_arch |
| `ha jobs info` | 运行中/排队任务 | `done:null` 堆积是已知 bug，可 `ha jobs reset` 或重启 Supervisor |
| `ha jobs options` / `ha jobs reset` | 任务条件管理/重置 | — |
| `ha resolution info` | Supervisor 问题/建议 | checks/issues/suggestions；`unsupported: job_conditions` 等 |
| `ha resolution check run` | 手动健康检查 | — |
| `ha resolution healthcheck` | 检查项状态 | — |
| `ha resolution issue dismiss [slug]` | 忽略问题 | — |
| `ha resolution suggestion apply/dismiss [slug]` | 应用/忽略建议 | — |

### 2.8 ha backups（备份恢复）
| 子命令 | 用途 | 关键参数 |
|--------|------|---------|
| `new` | 创建备份 | `--name`、`--password`、`-a/--app`（部分备份）、`-f/--folders`、`-l/--location`、`--homeassistant-exclude-database`、`--uncompressed` |
| `list`（裸 `ha backups` 默认） | 列出备份 | — |
| `info <slug>` | 备份详情 | 区分 full/partial |
| `restore <slug>` | 恢复 | `--password`（**备份加密密钥**，非登录密码）、`--folders`、`-a/--app`；partial 必须显式指定 |
| `remove <slug>` | 删除 | — |
| `options` | 过期策略 | `--days-until-stale`（默认 30 天） |
| `freeze` / `thaw` | 暂停/解冻备份引擎 | — |
| `reload` | 重载备份列表 | — |

**备份要点**：
- 全量可恢复备份建议用自动化调 `hassio.backup_full`（compressed:true）；GUI/`ha backups new` 常产出 partial。
- 备份 AES-128 加密，密钥只在 emergency kit，Nabu Casa 不存；换密钥后旧备份需旧密钥解密。
- CLI 无 download 子命令，下载备份走 Web UI（Settings > System > Backups）。
- 灾难恢复链路：`ha backups list` → `ha backups info <slug>` → `ha backups restore <slug> --folders/--app/--password`。

### 2.9 其余组（一般不手动动）
| 命令 | 用途 |
|------|------|
| `ha audio info / default / volume / profile` | 音频引擎（hassio_audio 容器） |
| `ha dns info / options / reset / restart / update` | 内部 DNS（hassio_dns） |
| `ha docker info / registries add\|delete / migrate_storage_driver` | Docker 后端与私有镜像仓库 |
| `ha multicast info / update / restart` | Multicast |
| `ha observer info / update` | Observer |
| `ha cli info / update` | ha 工具本体升级 |
| `ha banner` | 打印欢迎横幅 |
| `ha auth list / reset / cache` | 用户认证；`list` 仅本地终端 |

---

## 三、实战流程

### 3.1 升级顺序（最佳实践）
1. 先做完整备份存设备外；查两版本间 Breaking Changes。
2. 顺序：`ha supervisor update` → `ha core update --backup` → `ha os update`。
3. Core 先于 OS 升级（OS 更新不自动备份，出错可回滚）。
4. 落后 >6 个版本时 `ha core update --version` 每 6 个版本一升，确认正常再继续。
5. 每到可用版本立即再备份作回滚检查点。
6. 升级后检查 Persistent Notifications 与日志。

### 3.2 日常速查
- 查状态：`ha info`、`ha core info`、`ha supervisor info`
- 看日志：`ha core logs -f`、`ha supervisor logs -f`、`ha addons logs <slug> -f`
- 排障：`ha core restart --safe-mode`（安全模式禁问题集成）、`ha core check`（先验配置）
- 改配置生效：`ha core options --duplicate-log-file=true` → `ha core rebuild` → `ha core restart`
- 静态 IP：`ha network update eth0 --ipv4-method static ...` → `ha network info` 验证
- 升级 addon：`ha addons update <slug>`
- 版本指定：`ha core update --version 2024.8.0`、`ha os update --version 15.2`

### 3.3 远程调用
```bash
export SUPERVISOR_ENDPOINT=http://<ip>:8123
export SUPERVISOR_API_TOKEN=<token>
ha core info
```

---

## 四、常见坑清单

| 坑 | 解决办法 |
|----|---------|
| `ha: command not found` | 确认 HAOS/Supervised；Supervised 用 `docker exec -it hassio_cli bash`；Container/Core 无 ha |
| `Another job is running for job group home_assistant_core` | `ha jobs info` 查 stuck job；`ha core stop` → `ha core restart --safe-mode`；排查 Entso-e 等集成；必要时重启主机 |
| `ha core options --duplicate-log-file=true` 后日志没出现 | 必须接着 `ha core rebuild` + `ha core restart` |
| `ha addons update` 无更新返回退出码 1 | 脚本判失败需忽略退出码 1 |
| restore 报 "only a partial backup" | 加 `--folders/--app` 指定内容；全量用 hassio.backup_full |
| restore 输登录密码被拒 | `--password` 是备份加密密钥（UI 里那个），非用户密码 |
| `ha jobs info` 输出巨大/内存高 | 已知 bug（备份子任务未清理）；`ha jobs reset` 或重启 Supervisor |
| 改静态 IP 不生效 | `ha network reload` 或重启；网关只设一个主接口 |
| 按旧文档敲 `ha host update` 报错 | 以 `ha <组> --help` 为准；OS 升级用 `ha os update` |
| `ha os datadisk wipe` 后数据仍在 | 多为坏盘，换存储介质；部分硬件需实体按钮（Yellow+CM4 红钮、Green 黑钮） |
| shell_command 自动化调不到 ha | 用 `hassio.*` 服务或 Supervisor REST API |

---

## 五、工具链与生态

- 终端 addons：**SSH & Web Terminal**（推荐，root + ha 补全）、**Advanced SSH & Web Terminal**、**Studio Code Server**
- 远程：Supervisor REST API / `SUPERVISOR_*` 环境变量 / `hassio.*` 服务
- 关联工具：`hass-cli`（已弃用，勿混）、Docker CLI（`docker exec -it hassio_cli bash`）
- 控制台：HAOS 系统控制台（`HA>` → `login`）

## 六、进阶路径/学习资源

- 官方文档：home-assistant.io/common-tasks/command-line/（命令清单）
- 官方 CLI 源码：github.com/home-assistant/cli（`ha help` 命令组；开发版新增 apps/mounts/security/store）
- 官方博客/社区：Home Assistant Community 升级、备份、job system 讨论
- 源码参考：github.com/home-assistant/supervisor（Job System、API）

---

## 七、信源清单

| # | 来源 | URL | 类型 |
|---|------|-----|------|
| 1 | HA 官方 common-tasks: Command Line | github.com/home-assistant/home-assistant.io/.../commandline.md | 官方 |
| 2 | home-assistant/cli 仓库 | github.com/home-assistant/cli | 官方 |
| 3 | Advanced SSH & Web Terminal addon | github.com/hassio-addons/app-ssh/.../ssh/DOCS.md | 官方 |
| 4 | HA 官方 update 文档 | raw.githubusercontent.com/.../common-tasks/update.md | 官方 |
| 5 | HA OS 官方文档 | github.com/home-assistant/home-assistant.io/.../common-tasks/os.markdown | 官方 |
| 6 | 官方网络配置文档 | developers.home-assistant.io/docs/operating-system/network/ | 官方 |
| 7 | ha: command not found 讨论 | community.home-assistant.io/t/ha-command-not-found/177356/14 | 社区 |
| 8 | Another job is running 讨论 | community.home-assistant.io/t/.../619612/12 及 /986693/3 | 社区 |
| 9 | CLI 恢复备份讨论 | community.home-assistant.io/t/home-assistant-restore-from-command-line-interface-cli-documentation/991935/2 | 社区 |
| 10 | find addon slug 讨论 | community.home-assistant.io/t/find-addon-slug/244750/6 | 社区 |
| 11 | Supervisor 2025.1 Backup 讨论 | community.home-assistant.io/t/2025-1-backing-up-into-2025/821339/612 | 社区 |
| 12 | Supervisor Job System（DeepWiki） | deepwiki.com/home-assistant/supervisor/8.1-job-system | 社区/文档 |
| 13 | HAOS 18.0 升级指南 | www.goyou.it/en/wiki/2026/06/23/complete-guide-to-updating-to-home-assistant-os-180.html | 博客 |
| 14 | 弃用 Core/Supervised/32-bit | community.home-assistant.io/t/deprecating-core-and-supervised-installation-methods-and-32-bit-systems/893617/3 | 官方公告 |

## 八、素材质量评估

- **官方文档数**：6（命令清单、update、OS、网络、CLI 源码、SSH addon）
- **社区/博客数**：8（command not found、job running、restore、slug、备份、DeepWiki、升级指南、弃用公告）
- **覆盖度**：19 个顶层命令组全部覆盖；核心组（core/supervisor/addons/host/os/network/backups）有实战示例与输出要点；常见坑 11 条。
- **时效性**：标注了 2025-2026 变更（Core/Supervised 弃用、duplicate-log-file、CLI 开发版 apps 改名）。
- **分歧点**：`ha host update`（旧文档有、新源码无）；`ha backups new` 产出 partial vs hassio.backup_full 全量 —— 均已标注，以官方源码/最新为准。
