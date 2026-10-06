---
url: "https://github.com/power721/alist-tvbox/issues/721"
title: "【小雅资源索引数据】未完全载入，部分小雅索引路径不存在，是否可以增加索引管理界面？ · Issue #721 · power721/alist-tvbox"
type: "github-issue"
repo: "power721/alist-tvbox"
scraped_at: 2026-10-06
---

# 小雅资源索引数据未完全载入（AList-TvBox Issue #721）

> 来源：GitHub Issue power721/alist-tvbox#721。主题：AList-TvBox 默认只加载小雅资源的部分索引，导致包括夸克分享在内的大量挂载资源搜不到。
> 说明：以下为与该主题相关的正文**逐字节选**（仅规范化了少量空白/行内标记，文字未改）。

## 正文节选

1. 在使用小雅资源的时候，只使用了部分索引数据，导致很多挂载的资源无法被搜索到，例如小雅的夸克分享索引，115分享索引以及部分电影等。

目前项目中主要加载了以下 index 数据：
- index.share.txt （只含有 `/🈴我的阿里分享/Tacit0924/` 和 `/🈴我的阿里分享/近期更新`）
- index.video.txt (含有部分 `/每日更新` 数据)
- index.comics.txt
- index.docu.txt
- index.book.txt
- index.music.txt
- index.non.video.txt

小雅中其他的常用索引数据需要加载，包括她的分享链接索引：

- index.115.txt #115分享 （通过手动在资源中添加小雅资源配置 data 目录中的 115share_internal.txt ，挂载目录为 /🏷️我的115分享）
- index.daily.txt # 完整的每日更新
- index.movie.txt #电影
- index.pikpak.txt #pikpak分享（通过手动在资源中添加小雅资源配置 data 目录中的 pikpakshare_list.txt ，挂载目录为 /🕸️我的PikPak分享）
- index.quark.txt #夸克分享（通过手动在资源中添加小雅资源配置 data 目录中的 quarkshare_list.txt ，挂载目录为 /🌀我的夸克分享）
- index.reality.txt #综艺
- index.tv.txt #电视剧

另外我发现，小雅的内置的 `/🈴我的阿里分享` 中，只有 `/🈴我的阿里分享/Tacit0924` 存在索引数据，而 `/🈴我的阿里分享/每日更新`（和小雅根目录下的 `/每日更新` 不同）和 `/🈴我的阿里分享/YYDSVIP综艺` 并不存在索引数据，仍然需要手动扫描构建。

2. 如上所述，小雅资源自己的索引数据有大量目录路径实际不存在，并且大部分在三级或四级目录前就已经失效。

## 与本笔记的关系

- 佐证「小雅**确有**一块夸克分享区」：挂载目录 `/🌀我的夸克分享`，列表文件 `quarkshare_list.txt`。
- 同时说明：该索引**默认不一定会被加载**（要手动放列表），且**大量目录路径实际不存在**——即覆盖率 / 有效性**不稳定**，需实机确认。
