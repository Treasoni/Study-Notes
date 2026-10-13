# ch03 陈旧的映射（stale map）

对应 G 清单见 `../../02_batch_update_plan.md` §2.1。

| # | 位置（改前） | 陈旧内容 | 处置 | 新内容 | 依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | 3.1 目录树 | 「`/data` 是配置目录 + 容器内 metadata 放 `/etc/xiaoya`」的旧口径，且未列凭据文件名 | 重画 | `/etc/xiaoya/` 树（`mytoken.txt`、`myopentoken.txt`、`temp_transfer_folder_id.txt`、三个 cookie、`docker_address.txt`、`guestlogin/guestpass`、`data/`） | all_in_one.sh:156,1230,1367-1369 |
| 2 | 3.1 挂载表 | 挂载关系不明（`/data` 与 metadata） | 换为两行表 | `/etc/xiaoya`→`/data`；`/etc/xiaoya/data`→`/www/data` | all_in_one.sh:1392 |
| 3 | 3.2 端口 | 宿主 `5677` → 容器 `5678` 口径，且未分「容器内 / 宿主」 | 重排为两表 | 容器内 `80`/`2345`/`2346`/`2347`；宿主 `5678`/`2345`/`2346`/`2347` | all_in_one.sh:1377,1398 |
| 4 | 3.2 | （缺）容器内是 `80` 不是 `5678` 的提醒 | 新增 | `[!warning]`：旧路线容器内 `5678`、宿主 `5677`；本路线反过来 | all_in_one.sh:1377 |
| 5 | 3.3 凭据表 | `ALIYUN_TOKEN` / `ALIYUN_OPEN_TOKEN` / `ALIYUN_FOLDER_ID` 环境变量 | 换为落盘文件 | `mytoken.txt`（`:569`）/ `myopentoken.txt`（`:628`）/ `temp_transfer_folder_id.txt`（`:948`） | all_in_one.sh:569,628,948 |
| 6 | 3.3 注入方式 | 「环境变量注入」 | 改写 | 「安装时问答 + 落盘文件」 | all_in_one.sh:1230,1237-1245 |
| 7 | 3.3.1 夸克 | 只用环境变量 `QUARK_COOKIE`，且手抓为唯一办法 | 改写 | 文件 `quark_cookie.txt`（`:740`）；**支持扫码自动获取**（`:742`），手抓降为后手 | all_in_one.sh:740,742 |
| 8 | 3.3.1 115/UC | （缺）扫码口径 | 补充 | 115 `115_cookie.txt`（`:292`，扫码 `:680`）；UC `uc_cookie.txt`（`:259`） | all_in_one.sh:259,292,680 |
| 9 | 3.3.2 WebDAV | 单一账号口径（`dav` 或 `guest` 反复） | 改写为双分支 | 路径恒 `/dav`；开强制登入（默认）→ `dav` + 自设密码（`:1304`、`:1401`）；未开 → `guest`/`guest_Api789`（hub `:18`） | all_in_one.sh:1304,1401;01_hub_docker_com.md:18 |
| 10 | 3.3.2 | （缺）强制登入两条风险理由 | 新增 | `:1293`「暴露到公网可能被坏人扫描到并无限制使用」、`:1294`「多人异地访问可能触发网盘风控甚至封禁账号」 | all_in_one.sh:1293-1294 |
| 11 | 3.4 fnOS | 「官方仓库」措辞 | 更正 | 改为「整合脚本项目 README」；点明兼容表第一列 `all_in_one.sh` 即主脚本 | 01_raw_githubusercontent_com.md:236,277 |
| 12 | 3.5 配置片段 | monlor 单路线 compose | 换为「主 + 备」 | 主：一键脚本命令（README:39）；备：官方镜像 `xiaoyaliu/alist` 等价 compose（all_in_one.sh:1373-1392） | README:39；all_in_one.sh:1373-1392 |
| 13 | 3.5 | （缺）术语校正 | 新增 | `[!note]`「整合脚本 vs 官方镜像」 | 01_hub_docker_com.md:8,18；README:33-34 |
| 14 | 全章镜像名 | `ghcr.io/monlor/xiaoya-alist` | 替换 | `xiaoyaliu/alist` | all_in_one.sh:1376 |
| 15 | 引文对照 | 30 条（含 monlor 语境多条） | 重编 | 36 条，出处补全为一列（表头「原文 / 中译 / 出处」） | 见章内表 |

## 保留未动的部分

- 「本章要解决的问题」的三张清单立意与「下一章预告」。
- 3.3 三件套「怎么拿」的三步（扫码法主推、F12 法降备选）、位数差异 note、token 过期与「二次确认」提醒、第三方工具风险提醒。
- 3.3.1 手抓夸克 cookie 的四步与两个坑（要用 Chrome、`__puus` 约 3 小时过期）。
- 引文对照表前的引导句（含 `—` 的含义说明）。
- 「更新记录」既有五行（历史留档，允许出现 monlor 字样）。
