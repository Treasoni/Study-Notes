# ch04 陈旧的映射（stale map）

对应 G 清单见 `../../02_batch_update_plan.md` §2.1。

| # | 位置（改前） | 陈旧内容 | 处置 | 新内容 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | 标题 / frontmatter title | 「单容器小雅（monlor 镜像）」 | 替换 | 「单容器小雅（一键脚本）」 | 用户确认（P2） |
| 2 | 4.1 五行表 | 维护方=monlor；凭据=环境变量；编排=compose | 整节重写 | 六行表：维护方=`xiaoyaDev/xiaoya-alist`；一键命令=ddsrem 脚本；镜像=`xiaoyaliu/alist`；凭据=交互式落盘；形态=终端菜单；单容器=`1 1` | README:33-34,39,75-76；all_in_one.sh:1376 |
| 3 | — | （缺）「整合脚本 ≠ 官方」概念 | 新增 | note：官方=镜像 `xiaoyaliu/alist`（作者 xiaoyaLiu）；本笔记=社区整合脚本；monlor 只在「周边工具」 | hub:8,18；README:33-34,295；all_in_one.sh:1376 |
| 4 | 4.2 一键脚本 | `monlor/docker-xiaoya/main/install.sh` | 替换 | `bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"` + 菜单 `1 1` | README:39,45-53,66-67,75 |
| 5 | 4.2 Compose 段 | 手写 `docker-compose.yml`，`ALIYUN_TOKEN` 等环境变量 | 删除，改为问答表 | 「脚本会依次问你什么」八行表（配置目录/三 token/Cookie×3/强制登入 → 落盘文件） | all_in_one.sh:156,569,628,948,740,259,292,1289-1330 |
| 6 | 4.2 端口 | 宿主 `5677` → 容器 `5678`；`5345`/`5346` | 替换 | 宿主 `5678` → 容器 `80`；`2345`/`2346`/`2347` | all_in_one.sh:1377 |
| 7 | 4.2 配置目录 | `/vol2/1000/docker2/xiaoya/data` | 替换 | 默认 `/etc/xiaoya`（挂 `/data`，其下 `data/` 挂 `/www/data`） | all_in_one.sh:156,1392 |
| 8 | 4.2 镜像 | `ghcr.io/monlor/xiaoya-alist` | 替换 | `xiaoyaliu/alist:latest`（host 网络：`:hostmode`） | all_in_one.sh:1373,1376 |
| 9 | 4.2 截图 | 两张 monlor compose/env 界面 PNG | **删除** | 删文件 + 正文改纯文字/代码；Obsidian 回收站 | 用户确认（P2） |
| 10 | 4.2 新增 | （缺）镜像源 / root | 新增 | warning：`6 6` Docker 镜像源；脚本要 root（macOS 反而不能 root） | README:163；all_in_one.sh:6232-6236,6484,6488 |
| 11 | 4.3 自检第 2 条 | 网页「获取设置失败」等 1~5 分钟 | 前置就绪判定 | 脚本内置等待到日志 `success load storage: [/©️`；网页层现象保留 | all_in_one.sh:202,204；gnz48:46；tid-9690:200 |
| 12 | 4.3 自检 WebDAV | 单一账号 `dav`/`guest` 反复 | 改写为双分支 | 路径 `/dav`；开强制登入→`dav`+自设密码；未开→`guest`/`guest_Api789` | all_in_one.sh:1304,1401,1403；hub:18 |
| 13 | 4.3 第二个高频报错 | ghcr 拉取被重置 | 替换 | 改为镜像源选择；保留 `/data/docker_address.txt: Operation not permitted` 权限坑 | tid-9690:96；all_in_one.sh:1367-1369 |
| 14 | 本章小结 | monlor 四条 + ghcr 换源 | 重写 | 八条：整合脚本≠官方 / 两步部署 / 单容器含义 / 问答落盘 / 端口 / WebDAV 双分支 / 脚本判就绪 / 镜像源 | 同上 |
| 15 | 引文对照 | 11 条（含 monlor 语境 5 条） | 重编 | 18 条，全部改挂新来源 + 现象类来源 | 见章内表 |

## 保留未动的部分

- 「本章要解决的问题」的立意与「下一章预告」。
- 现象类引文（「获取设置失败」、`docker_address.txt` 权限报错、token 过期）。
- 引文对照表前的引导句（含 `—` 的含义说明）。
- 「更新记录」既有两行（历史留档，允许出现 monlor 字样）。
