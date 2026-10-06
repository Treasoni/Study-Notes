---
url: "https://raw.githubusercontent.com/AkimioJR/MediaWarp/main/README.md"
title: "MediaWarp README（raw Markdown 重抓）· TODO LIST 与功能段"
scraped_at: 2026-10-06T13:07:28+00:00
note: "补正 01_github_com.md：该件由 GitHub HTML 页面转文本，TODO LIST 的 checkbox 状态在转换中丢失（全部渲染成裸 `*` 项），使「适配 飞牛影视」被误读为待办。本件按 raw Markdown 逐字重抓，保留 `- [x]` / `- [ ]`，仅收录支持状态判定所需的段落。"
---

# TODO LIST（逐字，raw Markdown，main 分支）

- [x] HTTPStrm 实现 302 重定向
- [x] 屏蔽特定客户端访问
- [x] 提供多种 Web 前端美化功能
- [x] AlistStrm 实现 302 重定向
- [x] 嵌入一些实用的 JavaScript 方便使用
- [x] 缓存图片、字幕提高性能
- [x] ~~多格式配置文件（优先级：JSON > TOML > YAML > YML > Java properties > Java props，格式参考[config.yaml.example](./config/config.yaml.example)）~~
- [x] 支持通过 `--config` 参数指定配置文件地址
- [x] ART 字幕转 ASS 字幕（仅 Emby）
- [ ] ASS 字幕字体子集化并嵌入字体
- [x] 适配 Emby
- [x] 适配 Jellyfin
- [ ] 适配 Plex
- [x] 适配 飞牛影视
- [x] 支持播放网盘转码内容（仅飞牛影视 AlistStrm 模式）

- [ ] ~~利用 Redis 做数据缓存~~
  > 需求不大，放弃，有需要可以直接使用 Nginx 或者其他反向代理工具的缓存

- [ ] ~~多服务器转码推流~~
  > 需求不大，放弃

- [ ] ~~利用 Mysql / PostgreSQL / Redis 优化 Infuse 媒体库模式下扫库体验~~
  > 有需要可以参考 [MisakaFxxk/MisakaF_Emby/Infuse](https://github.com/MisakaFxxk/MisakaF_Emby/tree/main/Infuse) 自行实现

- [ ] ~~多服务器负载均衡~~
  > 在服务器前面加一个负载均衡可能更好

# 功能（节选，逐字）

- Strm 文件可以实现 302 直链播放，流量不经过 Emby Server / Jellyfin Server / 飞牛影视服务器
  - **推荐配合 [AutoFilm](https://github.com/AkimioJR/AutoFilm) 使用**
  - 已通过测试客户端（Web、iOS Emby、Infuse、Conflux、Fileball、Vidhub）
  - 支持 Strm：
    - HTTPStrm：Strm 文件内容是 HTTP 链接，浏览器访问链接可以直接下载到视频文件（**客户端需要可以访问到该链接，MediaWarp 不需要访问到该地址**）
    - AlistStrm：Strm 文件内容是 AList 上视频文件的路径（**路径需要采用 utf-8 编码格式**；仅支持 **AList v3 API的服务I**，目前 **OpenList 兼容 AList v3 API**；**客户端无需访问到 AList 服务器，仅需要 MediaWarp 可以访问到 AList 服务器，但是需要可以访问到 AList 服务器上文件的 raw_url 属性，如果使用网盘存储则无需在意这一点，但目前兼容性较差且不支持转码，通过挂载真实目录可以缓解这一问题**）

- 飞牛影视

  ![HTTPStrm](./img/FNTV-HTTPStrm.png)
  ![AlistStrm](./img/FNTV-AlistStrm.png)

# 相关文档（逐字）

- [教程文档](https://blog.akimio.top/posts/1041/)
- [更新日志](./docs/UpdateLog.md)
- [开发文档](./docs/DEV.md)
- [User-Agent参考](./docs/UA.md)
