## 学习笔记大纲：《Home Assistant 中 ha 命令的使用》

> 笔记类型：实战速查手册（concept + cheat_sheet 混合：先讲清 ha 命令是什么、怎么进终端，再给常用命令实战 + 完整速查表）
> 预计总篇幅：中（约 20-25 页）
> 章节数：8
> 命令覆盖：19 个顶层命令组全部覆盖（正文详述常用组，低频组收进第 8 章速查表）

### 第一章：认识 ha 命令
- **篇幅**：中
- **覆盖要点**：`ha <group> <command>` 语法结构、ha CLI 本质（Supervisor REST API 封装）、19 个顶层命令组总览、可用环境（HAOS / HA Supervised 才有；Docker Container / Core 直装没有）、三种进入终端方式（SSH & Web Terminal / VS Code addon / HAOS 系统控制台）、命名澄清（ha vs hass-cli、ha core vs ha supervisor）、全局 flags 与 `SUPERVISOR_*` 环境变量
- **素材引用**：一（1.1-1.5）、五、七
- **代码示例数量**：1（进入终端与 command not found 应急：`login`、`docker exec -it hassio_cli bash`）

### 第二章：核心命令组实战 —— core / supervisor / addons
- **篇幅**：长
- **覆盖要点**：`ha core`（check/info/logs/options/restart/start/stop/stats/update/rebuild）、`ha supervisor`（info/logs/reload/update/options/restart/stats/repair）、`ha addons`（list/info/install/uninstall/update/start/stop/restart/logs/stats/rebuild/changelog）、addon slug 的获取与含义（官方 `core_*` vs 社区 `a0d7b954_*`）、各命令常用参数与别名（`--follow`、`--version`、`--backup`、`-s/--safe-mode`、`upgrade/downgrade/up` 等）
- **素材引用**：2.1、2.2、2.3、3.2
- **代码示例数量**：6（core info / core check / core logs -f / core restart --safe-mode / addons install+update+logs / supervisor update）

### 第三章：系统级命令组 —— host / os / network / hardware
- **篇幅**：长
- **覆盖要点**：`ha host`（reboot/shutdown/info/options/logs/disks）、`ha os`（update/info/datadisk wipe|list|move/import/config swap/boot_slot/boards）、`ha network`（info/update/scan/reload/vlan，静态 IP 配置）、`ha hardware`（info/audio）、`ha host update` 新旧文档差异提示
- **素材引用**：2.4、2.5、2.6、四
- **代码示例数量**：4（host reboot / os update --version / network update 静态 IP + network info 验证 / hardware info --raw-json）

### 第四章：诊断命令组 —— info / jobs / resolution
- **篇幅**：中
- **覆盖要点**：`ha info` 系统总览输出解读（arch/channel/supervisor/homeassistant/hassos 等字段）、`ha jobs`（info/options/reset，`done:null` 堆积已知 bug）、`ha resolution`（info/check run/healthcheck/issue dismiss/suggestion apply|dismiss）用于排查 unsupported/issue
- **素材引用**：2.7、四
- **代码示例数量**：3（ha info / ha jobs info + jobs reset / ha resolution info + check run）

### 第五章：备份与恢复 —— backups
- **篇幅**：中
- **覆盖要点**：`ha backups`（new/list/info/restore/remove/options/freeze/thaw/reload）、full vs partial 备份、备份加密与密钥（`--password` 是加密密钥非登录密码）、CLI 无 download 子命令、灾难恢复链路、自动化全量备份 `hassio.backup_full` 建议
- **素材引用**：2.8、四
- **代码示例数量**：4（backups new / backups list / backups restore --folders --password / backups options --days-until-stale）

### 第六章：升级与运维流程
- **篇幅**：中
- **覆盖要点**：标准升级顺序（`supervisor update` → `core update --backup` → `os update`）、版本指定（`--version`）、落后多版本时每 6 版一升、安全模式（`ha core restart --safe-mode`）、配置修改生效链路（`core options` → `core rebuild` → `core restart`）、日常速查清单、远程调用（`SUPERVISOR_ENDPOINT` / `SUPERVISOR_API_TOKEN`）
- **素材引用**：3.1、3.2、3.3、2.2、2.4
- **代码示例数量**：4（升级顺序命令序列 / core update --version / os update --version / 远程调用环境变量 + ha core info）

### 第七章：常见坑与排障
- **篇幅**：中
- **覆盖要点**：11 条常见坑逐条拆解（`ha: command not found`、Another job is running、duplicate-log-file 不生效、addons update 退出码 1、restore partial 与密码被拒、jobs info 内存高、静态 IP 不生效、旧文档 ha host update、datadisk wipe 数据仍在、shell_command 调不到 ha）、排障判断路径（先 `ha core check` 再重启）
- **素材引用**：四、1.2、2.8、2.7
- **代码示例数量**：2（Supervised 宿主 docker exec 进 CLI / 排障组合命令）

### 第八章：完整速查表（cheat-sheet）
- **篇幅**：长
- **覆盖要点**：19 个顶层命令组全量速查汇总（正文已详述的 core/supervisor/addons/host/os/network/hardware/info/jobs/resolution/backups 压缩为一行式语法 + 低频组 audio/dns/docker/multicast/observer/cli/banner/auth 给全子命令）、全局 flags 速查、开发版新增组提示（mounts/security/store）、常用命令推荐段落
- **素材引用**：二（2.1-2.9 全量）、1.5、五
- **代码示例数量**：0（纯表格速查，不再展开示例）

## 学习路径说明

### 前置要求
- 已有 HAOS 或 HA Supervised 部署环境（Docker Container / Core 直装无 `ha` 命令，不适用本笔记）
- 能进入一个终端：SSH & Web Terminal addon、VS Code addon 或 HAOS 系统控制台
- 了解 Home Assistant 基本概念：Core、Supervisor、Addon 三者关系
- 可互链既有笔记：[[homeassistant/haos-deploy/部署 HAOS 详细教程]]、[[homeassistant/Home Assistant 部署方式对比]]

### 学完能做什么
- 用 `ha` 命令查系统状态、看日志、定位卡住的 job 和 Supervisor 问题
- 独立完成 core / supervisor / addon / OS 的安装、升级与版本指定
- 用命令行完成备份、恢复与数据盘管理
- 配置静态 IP、重启/关机宿主机、查看硬件信息
- 遇到 `ha` 命令相关报错能按坑位清单自行排障
- 日常不翻文档，直接查第 8 章速查表

### 建议学习顺序
- 第 1 章 → 第 2 章 → 第 3 章（前 3 章按依赖顺序，先懂环境再上手核心与系统命令，约 2-3 小时）
- 第 4 章 + 第 5 章（诊断与备份，约 1 小时）
- 第 6 章（升级运维流程，把前几章命令串成完整流程，约 1 小时）
- 第 7 章（坑位排障，用时排查时按需查阅）
- 第 8 章（速查表，日常工具，建议打印或收藏）
