# ch07 陈旧的映射（stale map）

对应 G 清单见 `../../02_batch_update_plan.md` §2.1。

| # | 位置（改前） | 陈旧内容 | 处置 | 新内容 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | 7.2 工具归属 | 只写工具自身仓库，未与整合脚本挂钩 | 补充 | 点明 xiaoyahelper 与整合脚本同属 `xiaoyaDev` 组织；补「菜单 `3 1`」安装路线 | README:79,292 |
| 2 | 7.2 手动命令 | `-s 3 -tg` 缺命令出处行号 | 校正 | 出处 `01_github_com.md:38,51,58`；引文出处校正到 `:32/:33/:47/:48/:55/:61/:82` | 01_github_com.md |
| 3 | 7.3 更新口径表 | 「重跑 monlor 一键安装脚本（仓库说明「脚本支持重复执行」）」 | **整节重写** | 菜单表：更新 `1 2`、卸载 `1 3`、装/更新 xiaoyahelper `3 1`、卸载 `3 3` | README:79,120,132,136 |
| 4 | 7.3 更新命令 | `curl ... raw.githubusercontent.com/monlor/docker-xiaoya/main/install.sh` | 替换 | 同第 4 章主命令 `ddsrem.com/xiaoya_install.sh`，进菜单选 `1 2` | README:39,120 |
| 5 | 7.3 镜像名纪律 warning | `ghcr.io/monlor/xiaoya-alist`（monlor 社区镜像） | 删除，改为两条新 warning | 「`1 1` 是安装、`1 2` 才是更新」；「卸载前备份 `/etc/xiaoya`」 | README:120,132 |
| 6 | 7.3 大白话 | 「覆盖 compose、`env` 里凭据不动」 | 改写 | 「凭据还在原来的抽屉里，一个字都不用重填」 | — |
| 7 | 7.4 资源推荐表 | monlor 项目四行表（1 核 / 512M / 512M …）+「维护者推荐」warning | **整节重写** | 三条可回源事实表：镜像 22 MB、脚本挑 >200 G 盘位、兼容表小雅Alist 三列全 ✅；删表；新增「本笔记不给最小配置数字」warning | hub:30；all_in_one.sh:145-163；README:218-234 |
| 8 | 7.5 自检第 ② 行 | 「用 monlor 社区镜像 `ghcr.io/monlor/xiaoya-alist`」 | 替换 | 「社区整合脚本 `xiaoyaDev/xiaoya-alist` 菜单 `1 1`（内部即官方镜像 `xiaoyaliu/alist`）」 | README:75；all_in_one.sh:1376 |
| 9 | 7.6 未决项一 | 「`ghcr.io` 上有没有小雅官方的镜像」（monlor 社区镜像） | 移除 | 术语已在第 4 章澄清（官方＝`xiaoyaliu/alist`），不再列为未决 | hub:8；README:295 |
| 10 | 7.6 未决项二 | 「`/data` 与 `/etc/xiaoya` 各自装什么」 | 移除并换行 | 第 3 章已给出文件级口径；换成「单容器最小硬件配置」 | ch03 |
| 11 | 7.6 新增 | （缺）卸载是否删配置 | 新增 | 未决行：README 未说明 `1 3` 的保留策略 | README:132 |
| 12 | 本章小结 | 「monlor 社区镜像」「维护者推荐 1 核/512M」 | 改写 | 五条：装完要养 / xiaoyahelper（`3 1`）/ 更新 `1 2`、卸载 `1 3` / 三条硬件事实 / 七项未决 | 同上 |
| 13 | 引文对照 | 9 条（含 monlor 语境 2 条） | 重编 | 15 条，来源改挂 `01_github_com.md` + `01_raw_githubusercontent_com.md` + `01_hub_docker_com.md` + `all_in_one.sh`；第 2 条补回原文末尾的 `！`、第 14/15 条注明空格已归一 | 见章内表 |

## 保留未动的部分

- 7.1「为什么装完还得养」整节（转存机制、图书馆比喻）。
- 7.2 的模式 0–5 表与「模式 2 已废弃」warning、四条实用补充（`myruntime.txt` / `mycmd.txt` / `mycheckintoken.txt` / 别改本体）。
- 7.5 自检表的 ① / ①-a / ①-b / ①-c 四行（前端链路内容与部署路线无关）。
- 7.6 中与部署路线无关的五项（`xiaoya.host`、STRM 起始版本、MediaWarp/fntv-proxy 共存、未获取的两篇文章、「半分钟几个 T」）。
- 章末「最后一句」分层心智段。
- 「更新记录」既有两行（历史留档，允许出现 monlor 字样）。
