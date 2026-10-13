# ch03 更新报告

| 项 | 值 |
| --- | --- |
| note_id | `ch03` |
| 源文件 | `chapters/03_动手前准备.md` |
| 动作 | update |
| 输出模式 | patch-in-place（`updated_note` 即 `chapters/03_动手前准备.md`） |
| 发布副本 | `output/03 动手前准备.md`、`流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md` |
| 标题变更 | 无（保持「第 3 章 动手前准备——目录、端口与凭据（新手可跳过）」） |
| 复核查验 | 待 P5 统一执行（`check-md-structure.py` + 引文回源） |

## 完成项

- 3.1 目录树重画为 `/etc/xiaoya` 本路线实况，挂载表改为「`/etc/xiaoya`→`/data`、`/etc/xiaoya/data`→`/www/data`」两行；新增「这棵树就是凭据放哪」note。
- 3.2 端口拆成「容器内 / 宿主」两表（容器内 `80`/`2345`/`2346`/`2347`；宿主 `5678`/…），新增「容器内是 `80` 不是 `5678`」warning 与新「大白话」比喻。
- 3.3 三件套由环境变量改为落盘文件口径；「怎么拿」三步与位数 note 保留，只换落点。
- 3.3.1 夸克/115/UC 改文件口径，**补扫码自动获取**（夸克 `:742`、115 `:680`），手抓降为后手。
- 3.3.2 WebDAV 改**强制登入双分支**（`dav`+自设密码 / `guest`+`guest_Api789`），并解释 `dav` 与路径 `/dav` 的历史混淆。
- 3.4 修「官方仓库」为「整合脚本项目 README」，点明兼容表第一列即主脚本。
- 3.5 片段由 monlor compose 改为「一键脚本（主）+ 官方镜像等价 compose（备）」，新增「整合脚本 ≠ 官方」note。
- 引文对照重编为 36 条，表头补全「出处」列；monlor 语境行移出正文。
- 全篇镜像名 `ghcr.io/monlor/xiaoya-alist` → `xiaoyaliu/alist`。

## 遗留 / 风险

| # | 项 | 说明 |
| --- | --- | --- |
| 1 | vault 侧表格列宽由 Obsidian 自动补空格 | `publish_copies.py --check` 在用户打开笔记后可能报 `vault=≠`，属渲染层格式，非内容漂移 |
| 2 | 3.5 的 compose 为**等价示意**，非脚本逐字输出 | 已在段首注明「参数出处：all_in_one.sh:1373-1392」，避免读者误当可直接复制成品 |
| 3 | 引文对照第 25 条为**旧法**（解码站）原文 | 属有意保留的「降为备选」对照，正文已标注其已失效 |

## 校验

- `publish_copies.py --check --only 03`：`OK`（output==、vault==）。
- 引文锚点回源：本次改后对 `sources/xiaoyaDev/all_in_one.sh` 逐条 grep 复核，修正 13 处行号偏移（详见 `../../03_batch_update_log.md` 批间复核记录）。
- 正文残留扫描：`rg -n "monlor|ghcr.io/monlor|ALIYUN_TOKEN|QUARK_COOKIE|EMBY_ENABLED|5677" chapters/03_动手前准备.md` 命中 6 行，逐行核定后**全部为有意保留**：
  1. `:67` 3.2 的 `[!warning]`——本路线与旧路线（monlor，容器内 `5678`/宿主 `5677`）的**对照说明**，删掉读者反而会照旧教程配错端口；
  2. `:236` 引文对照第 28 条——论坛用户原话 `PS:ALIYUN_TOKEN 第二天就失效了，需要重新获取`（`sources/01_club_fnnas_com.md:157`），系**逐字引文**，按引文纪律不得改写，其中 `ALIYUN_TOKEN` 是发言者当时使用的 monlor 变量名；
  3. `:250`–`:255` 「更新记录」历史行。

  正文的部署指令、目录、端口、镜像、凭据五部分已无 monlor 残留。
