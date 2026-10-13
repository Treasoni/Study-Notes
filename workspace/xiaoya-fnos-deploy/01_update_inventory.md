# 阶段 1：更新清单（run: update-xiaoya-fnos-alist）

## 扫描范围

| 项 | 值 |
| --- | --- |
| 正文唯一来源 | `workspace/xiaoya-fnos-deploy/chapters/`（`0*.md`，7 章） |
| 入口页 | `workspace/xiaoya-fnos-deploy/output/小雅 fnOS 单容器部署（总览）.md`（不在 `chapters/`） |
| 派发副本 | `workspace/xiaoya-fnos-deploy/output/*.md` + `final_note.md`（由脚本机械重建） |
| 发布副本 | `流媒体与影音/小雅 fnOS 单容器部署/*.md`（同上） |

副本不单独编辑：`publish_copies.py` 从 `chapters/` 重建 `output/` 与 vault，`assemble_final.py` 重建 `final_note.md`。

## 清单一览

| id | 文件 | 标题 | 体积(B) | monlor/dds 命中 | 状态 | 理由 |
| --- | --- | --- | ---: | ---: | --- | --- |
| ch01 | `chapters/01_开篇定位.md` | 第 1 章 开篇定位 | 13233 | 5 | ready | AList/Emby 组件描述引自 monlor；「官方脚本」措辞需校正 |
| ch02 | `chapters/02_选型对比.md` | 第 2 章 选型对比 | 19987 | 15 | ready | 路线 E 组成、资源推荐表、硬解引文均据 monlor |
| ch03 | `chapters/03_动手前准备.md` | 第 3 章 动手前准备 | 28096 | 14 | ready | 目录/端口/凭据三张清单全为 monlor 环境变量口径 |
| ch04 | `chapters/04_部署实战.md` | 第 4 章 部署实战 | 12745 | 37 | ready | 整章围绕 monlor 镜像与 compose，需整体改写 |
| ch05 | `chapters/05_前端接入.md` | 第 5 章 前端接入 | 45151 | 10 | ready | 少量 monlor 引文（阿里限速/转存 115）与 `ALIYUN_TO_115` 口径 |
| ch06 | `chapters/06_避坑清单.md` | 第 6 章 避坑清单 | 11749 | 0 | candidate | 仅 1 处 monlor 环境变量 `AUTO_CLEAR_ENABLED` 提法 |
| ch07 | `chapters/07_运维与收尾.md` | 第 7 章 运维与收尾 | 13677 | 17 | ready | 更新口径、资源推荐表、镜像纪律均按 monlor 写 |
| overview | `output/小雅 fnOS 单容器部署（总览）.md` | 总览 | 3821 | 2 | ready | 读前须知点名 monlor 镜像与 monlor 项目 |

> `monlor/dds 命中` 为关键词粗筛（`monlor|ghcr|ddsrem|DDSRem|ddsderek|EMBY_ENABLED|JELLYFIN_ENABLED|docker compose`），仅用于排序人工复核，不等于精确改动行数。

## 关键词命中分布（按文件）

| 文件 | monlor 系 | ddsrem 系 | 备注 |
| --- | ---: | ---: | --- |
| 01 | 5 | 0 | 组件描述 + 镜像提及 |
| 02 | 15 | 0 | 路线 E 组成 3 条 + 资源表 1 条 + 硬解 1 条 |
| 03 | 14 | 0 | 目录/端口/凭据全篇 |
| 04 | 27 | 0 | 全章 |
| 05 | 8 | 0 | 限速/转存 115 引文 |
| 06 | 0 | 0 | 仅 `AUTO_CLEAR_ENABLED` 1 处（不含关键词列） |
| 07 | 14 | 0 | 更新口径 + 资源表 + 未决项 |

## 判定说明

- **skip**：无。8 个文件全部进入处理（ch06 与 overview 属轻量校订）。
- **needs-review**：无。
- **前置引用**：`sources/01_raw_githubusercontent_com.md` 顶部 URL 即 `https://raw.githubusercontent.com/xiaoyaDev/xiaoya-alist/master/README.md`，**已是目标项目的 README**，无需换源，第 1–3 章现有引用可继续沿用。
- **新增一手来源**：`sources/xiaoyaDev/all_in_one.sh`（6567 行，取自 `raw.githubusercontent.com/xiaoyaDev/xiaoya-alist/master/all_in_one.sh`）与 `sources/xiaoyaDev/main.sh`（bootstrap）。
