# Home Assistant 中 ha 命令的使用 - 探测结果

收集时间: 2026-08-06 23:10
搜索关键词: ha CLI 官方文档 / ha core supervisor addons 实战 / ha 系统运维命令与常见坑

## 探测结论摘要

1. **`ha` 是 Supervisor 系统级 CLI**：`ha <group> <command>`，本质是对 Supervisor REST API 的 1:1 封装。顶层命令组约 19 个：`addons/audio/authentication/backups/banner/cli/core/dns/docker/hardware/host/info/jobs/multicast/network/observer/os/resolution/supervisor`。核心实战组：core、supervisor、addons、host、os、network、hardware、info、logs、update、backups、resolution。
2. **可用环境**：`ha` 命令只存在于 **HAOS** 与 **HA Supervised**。Docker Container / Core 直装没有 Supervisor，没有 `ha` 命令。Supervised 宿主 shell 也可能 command not found，需 `docker exec -it hassio_cli bash` 进入 CLI 容器。`shell_command` 集成运行在 Core 容器内，同样调不到 `ha`。
3. **进入终端方式**：SSH & Web Terminal addon（OpenSSH + 内嵌 Web Terminal，root 登录，Bash 带 `ha` 补全）、Studio Code Server（VS Code，仅 AMD64/aarch64）、HAOS 系统控制台（键盘+屏幕，可执行 `ha os datadisk wipe`、`ha auth list` 等本地终端专用命令）。
4. **命名澄清**：现在的 `ha` = 原 hassio-cli（2020 年品牌改名统一）。与已弃用的 `hass-cli`（面向 Core REST API 的独立 Python 客户端）是**不同工具**，勿混。
5. **核心命令要点**：
   - `ha core`：11 个子命令（check/info/logs/options/rebuild/restart/start/stats/stop/update）。版本升级 `ha core update --version x.y.z`；安全模式 `ha core restart --safe-mode`。
   - `ha supervisor`：info/logs/reload/update。升级顺序：先 `ha supervisor update` 再 core/host。
   - `ha addons`：list/install/uninstall/update/start/stop/restart/logs/info <slug>。addon slug 形如 `core_ssh`、`core_mosquitto`、`a0d7b954_adguard`（社区带作者前缀）。
   - 系统级：`ha host reboot`、`ha os update`、`ha network info`、`ha hardware info`、`ha resolution info`。
   - 全局 flag：`--raw-json`、`--api-token`、`--no-progress`、`--log-level`。`ha <command> --help` 查看子命令。
6. **常见坑**：
   - `ha: command not found` → 非 HAOS/Supervised，或需 `docker exec -it hassio_cli bash`。
   - `Another job is running for job group home_assistant_core` → Supervisor 串行化任务，等上一任务结束即可，可用 `ha jobs` 查询。
   - `ha addons update` 无更新时返回退出码 1，脚本判失败需忽略。
   - 磁盘日志：HA 2026.01 起 `ha core options --duplicate-log-file=true` + `ha core rebuild` + `ha core restart`。
   - OS 更新不自动备份，需手动备份；备份 AES-128 加密，emergency kit 密钥丢失无法恢复。
   - HA 2025-12 起弃用 Core（venv）/Supervised 安装模式，`ha` 体系只随 HAOS/Container+Supervisor 完整存在。

## 信源清单

| # | 标题 | URL | 相关性 | 来源类型 |
|---|------|-----|--------|---------|
| 1 | HA 官方 common-tasks: Command Line（ha CLI 用法） | github.com/home-assistant/home-assistant.io/blob/.../common-tasks/commandline.md | 5/5 | 官方文档 |
| 2 | HA 官方 CLI 仓库 home-assistant/cli（ha help 命令组总览） | github.com/home-assistant/cli | 5/5 | 官方文档 |
| 3 | Advanced SSH & Web Terminal addon 文档 | github.com/hassio-addons/app-ssh/.../ssh/DOCS.md | 5/5 | 官方文档 |
| 4 | 社区：ha: command not found（环境可用性） | community.home-assistant.io/t/ha-command-not-found/177356/14 | 5/5 | 社区讨论 |
| 5 | 社区：Another job is running for job group home_assistant_core | community.home-assistant.io/t/.../619612/12 | 4/5 | 社区讨论 |
| 6 | 社区：如何定位 addon slug | community.home-assistant.io/t/.../928112/4 | 4/5 | 社区讨论 |
| 7 | GitHub 讨论：恢复 home-assistant.log 磁盘日志 | github.com/orgs/home-assistant/discussions/1527 | 4/5 | 社区讨论 |
| 8 | HA CLI（原 hassio-cli）源码 4.0.1 | git.sudo.is/home-assistant/cli/src/tag/4.0.1 | 4/5 | 官方文档 |
| 9 | 博客：HAOS 18.0 升级完整指南（备份/顺序） | www.goyou.it/en/wiki/2026/06/23/complete-guide-to-updating-to-home-assistant-os-180.html | 4/5 | 技术博客 |
| 10 | LWN：HA 弃用 core/supervised 安装模式 | lwn.net/Articles/1022252/ | 4/5 | 新闻 |

## 建议方向菜单

- **A. 完整命令速查手册**（推荐）：覆盖全部核心命令组的实战用法 + 完整速查表 + 常见坑。贴合"上手速查"定位，一次成册。
- **B. 核心运维实战**：聚焦 core/supervisor/addons 三大组 + 升级/备份/排障流程。
- **C. 概念与环境向**：讲清 ha CLI 架构、可用环境、进入方式，命令做概览。
- **D. 排障场景向**：以踩坑场景为线索组织（command not found / job running / addon slug / 日志恢复 / 备份恢复）。
