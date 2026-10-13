# 共享来源库（run: update-xiaoya-fnos-alist）

适用范围：**整套 8 篇**。所有新写内容只引用下表来源；旧 monlor 语境来源降级为「历史对照」，只允许出现在「更新记录」里。

---

## S1 · 主线一手来源：`xiaoyaDev/xiaoya-alist` README

| 项 | 值 |
| --- | --- |
| 本地文件 | `sources/01_raw_githubusercontent_com.md` |
| 原始 URL | `https://raw.githubusercontent.com/xiaoyaDev/xiaoya-alist/master/README.md` |
| 抓取时间 | 2026-10-05 |
| 用途 | 菜单全表、安装/备用命令、兼容性表、周边工具、官方口径 |

关键锚点：

| 行 | 内容 |
| ---: | --- |
| `:33-34` | 「整合安装脚本，内置所有相关软件的安装」 |
| `:39` | 主命令 `bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"` |
| `:45,49,53` | 备用地址（ddsrem 直链 / jsdelivr / raw.githubusercontent） |
| `:57,61` | `main.sh` 引导脚本地址（jsdelivr / raw） |
| `:66-69` | 菜单规则「数字代表先选 x，再选 x」，如 `2 2 8` = 先 2 再 2 最后 8 |
| `:75` | `安装 小雅Alist -> 1 1` |
| `:76` | `安装 Emby全家桶（一键） -> 2 1` |
| `:120` | `更新 小雅Alist -> 1 2` |
| `:132` | `卸载 小雅Alist -> 1 3` |
| `:138-143` | `安装/更新/卸载 小雅Alist-TVBox` 等 |
| `:169` | 「弃用菜单（此菜单下的功能不再维护，不建议使用）」 |
| `:173,196` | `安装/卸载 Jellyfin全家桶` 在**弃用菜单**下（`6 8 3 1` / `6 8 3 4`） |
| `:180-182` | 「目前官方 Jellyfin 安装方案已经长久未维护！」需用 AI老G 脚本，风险自担 |
| `:205-209` | 相关镜像：`ddsderek/xiaoya-emd`、`xiaoya-proxy`、`xiaoya-cron`、`xiaoya-glue`、`xiaoya-115cleaner` |
| `:218-234` | 组件架构兼容表（小雅Alist x86-64/arm64/armhf 全 ✅） |
| `:236-277` | 系统兼容表（`all_in_one.sh` 列）；`:277` **fnOS（飞牛私有云）✅** |
| `:294` | 周边工具：小雅官方 strm 文件一键生成脚本（notion 链接） |
| `:295` | 周边工具：`monlor/docker-xiaoya`（compose 全家桶）——**monlor 在本项目里只是「周边」，不是主线** |
| `:297-298` | 周边工具：`StrmAssistant`（Emby 用）、`xiaoya-alist-search`（**不装 Emby 时在 iOS Fileball 上全局搜索/直接观看**） |
| `:302` | 致谢 `xiaoyaLiu`（`alist.xiaoya.pro`）＝小雅官方 |

---

## S2 · 主线一手来源：整合安装脚本 `all_in_one.sh`

| 项 | 值 |
| --- | --- |
| 本地文件 | `sources/xiaoyaDev/all_in_one.sh`（6567 行） |
| 原始 URL | `https://raw.githubusercontent.com/xiaoyaDev/xiaoya-alist/master/all_in_one.sh` |
| 用途 | 安装流程、镜像、端口、目录、凭据、就绪判定、脚本自报的访问地址 |

关键锚点：

| 行 | 内容 |
| ---: | --- |
| `:156-158` | 配置目录默认值 `xiaoya_alist_config_dir` → `/etc/xiaoya`（若探测到大容量盘则用 `${path_lib}/xiaoya`） |
| `:161-163` | 媒体目录默认 `/opt/media` |
| `:202` | `TARGET_LOG_LINE_SUCCESS="success load storage: [/©️"` |
| `:204` | `wait_xiaoya_start()` 取 `docker logs ... \| tail -n 10` 判就绪 |
| `:220-231` | `check_quark_cookie()` → `quark_cookie.txt`，含 `__puus` 校验 |
| `:259-279` | `check_uc_cookie()` → `uc_cookie.txt` |
| `:292-298` | `check_115_cookie()` → `115_cookie.txt` |
| `:569-606` | `mytoken.txt` 写入/校验（阿里云盘 refresh token，长度 >31） |
| `:628-669` | `myopentoken.txt` 写入/校验（open token，长度 >279） |
| `:676-699` | `enter_115_cookie()`（支持扫码） |
| `:740-761` | 夸克 Cookie 录入（支持扫码） |
| `:948-978` | `settings_aliyunpan_folder_id()` → `temp_transfer_folder_id.txt` |
| `:1204` | `install_xiaoya_alist()` 定义 |
| `:1230` | `files=("mytoken.txt" "myopentoken.txt" "temp_transfer_folder_id.txt")` |
| `:1289-1330` | 强制登入流程；`:1304` **「强制登入用户名：dav（无法修改）」**，`:1293-1294` 两条风险提示，`:1329` 写 `guestpass.txt`，`:1330` 写 `guestlogin.txt`；`:1289` 已存在则跳过 |
| `:1367-1369` | 写 `docker_address.txt` = `http://$localip:5678` |
| `:1371` | `docker_command=("docker run" "-itd" "--privileged")` |
| `:1373` | host 网络镜像 `xiaoyaliu/alist:hostmode` + `--network=host` |
| `:1376-1377` | bridge 镜像 `xiaoyaliu/alist:latest` + `-p 5678:80 -p 2345:2345 -p 2346:2346 -p 2347:2347` |
| `:1385-1390` | 有 `local_dir.txt` 时额外挂 `${strm_dir}:/strm` |
| `:1392` | `-v ${CONFIG_DIR}:/data -v ${CONFIG_DIR}/data:/www/data --restart=always --name=<容器名>` |
| `:1395-1405` | 安装完成 INFO：`alist: http://ip:5678`（`:1398`）；`webdav: http://ip:5678/dav, 用户密码: dav/<自设密码>`（`:1401`）；未开强制登入则 `默认用户密码: dav/guest_Api789`（`:1403`）；`tvbox: http://ip:5678/tvbox/my_ext_jar.json` |
| `:5848` | 容器名默认写 `xiaoya` 到 `container_name/xiaoya_alist_name.txt` |

---

## S3 · `main.sh`（引导脚本）

| 项 | 值 |
| --- | --- |
| 本地文件 | `sources/xiaoyaDev/main.sh`（71 行） |
| 用途 | 说明 README 里 `main.sh` 入口做的事：下载 `all_in_one.sh`（ddsrem → jsdelivr → raw.githubusercontent 三路回退）到 `/tmp/xiaoya_install.sh` 后执行 |

---

## S4 · 官方镜像来源（术语校正用）

| 项 | 值 |
| --- | --- |
| 本地文件 | `sources/01_hub_docker_com.md` |
| 原始 URL | `https://hub.docker.com/r/xiaoyaliu/alist` |
| 抓取时间 | 2026-10-05 |
| 用途 | **「官方」到底指什么**：作者 `xiaoyaliu`，内容源 `alist.xiaoya.pro`，TG 频道 `t.me/xiaoyaliu` |
| `:18` | 「webdav 账号密码 用户: guest 密码: guest_Api789」 |
| `:15` | 「端口：5678 访问：http://xxxxx:5678/」 |
| `:16` | 官方一键脚本 `bsh -c "$(curl -s http://docker.xiaoya.pro/update_new.sh)"` |
| `:19` | 「重启就会自动更新数据库及搜索索引文件」 |

> 术语结论：**官方 = 镜像 `xiaoyaliu/alist`（作者 xiaoyaLiu）**；`xiaoyaDev/xiaoya-alist` 是**社区整合脚本**，只是它内部用的就是官方镜像。含 `:16` 的官方 `update_new.sh` 已被本轮弃用（不在新主线）。

---

## S5 · 现象类来源（可继续沿用，与部署路线无关）

| 本地文件 | 用途 |
| --- | --- |
| `sources/p3/gnz48/01_www_cnblogs_com.md` | 首次访问「获取设置失败」属正常、初始化 1~5 分钟、网页能播即算通 |
| `sources/p2/newzone-xiaoya.md` | token 会过期（「无法加载列表 / 播放失败」先更新 token）；`docker_address.txt` 用途 |
| `sources/forum/tid-9690.md` | fnOS 用户实操现象（如 `/data/docker_address.txt: Operation not permitted` 权限报错）；`:280` 记 WebDAV「guest / guest_Api789 / 路径 /dav」 |

---

## S6 · 历史对照来源（**仅限「更新记录」引用**）

| 本地文件 | 说明 |
| --- | --- |
| `sources/p2/monlor-144.md` | monlor 项目 README（环境变量方案、资源推荐表） |
| `sources/p3/monlor-env/01_raw_githubusercontent_com.md` | monlor 的 `.env` 模板（`EMBY_ENABLED`、`WEBDAV_PASSWORD` 等注释） |
| `sources/p2/monlor-144.md:317`、`sources/p3/github-api/listing.json.md` | monlor 仓库元信息（最后提交时间） |

---

## S7 · 待核实项（本轮已解决）

| 原疑问 | 结论 | 依据 |
| --- | --- | --- |
| WebDAV 用户名到底是 `dav` 还是 `guest` | **两分支**：开「强制登入」（脚本默认）→ 用户名 `dav` + 自设密码；未开 → 官方默认 `guest` / `guest_Api789`。历史上把 **路径 `/dav`** 与 **强制登入用户名 `dav`** 混为一谈 | `all_in_one.sh:1304,1401,1403` + `01_hub_docker_com.md:18` |
