---
url: "https://blog.akimio.top/posts/1041/"
title: "MediaWarp 教程文档（作者博客）"
scraped_at: 2026-10-06T13:07:28+00:00
note: "官方 README「相关文档」指向的教程文档。正文为页面正文清洗稿；代码块按 YAML 常规缩进整理，行内容逐字（原页面代码块以 <span> 分行，缩进不可逐字还原）。"
---

## 文章摘要（页面自带，AI 生成并声明经人工审核）

MediaWarp 是针对媒体服务器的增强工具，旨在优化基于 STRM 文件的流媒体播放体验，解决传统 STRM 方案中存在的带宽瓶颈和兼容性问题。

- 绕过带宽限制：当客户端播放 STRM 文件时，MediaWarp 将客户端请求直接重定向至远程资源（如在线流媒体、远程服务器文件），避免流量经过家庭局域网的 Emby/Jellyfin 服务器，彻底消除宽带上行速率限制。
- 传统模式：客户端 → Emby服务器 → 远程资源（受上行带宽制约）
- MediaWarp模式：客户端 → 远程资源（直连加速）
- 智能回退机制：若客户端因跨域请求被拦截、需要身份验证、格式兼容性问题（如客户端不支持 H.265 编码）、转码需求而无法直接播放远程资源，MediaWarp 将自动回退至 Emby 服务器推流。
- 强制禁止转码：通过配置可拦截转码请求，强制客户端仅使用原始流。

## 什么是 Strm，MediaWarp 又有什么用

EmbyServer 官方 Wiki 对 Strm 文件的表述：STRM 文件使用指南

STRM 文件是一种能让 Emby 媒体服务器将在线音视频流模拟为本地媒体文件的文本文件。只要流媒体格式及传输协议受 Emby 支持，即可通过 STRM 文件实现流畅播放。这类文件本质上是普通的文本文件，仅通过将扩展名改为 .strm 来伪装成特定格式，其内容包含指向流媒体的 URL 或本地文件路径。

目前 Emy、Jellyfin 均支持 strm 文件，Plex 暂不原生支持。一言以蔽之，.strm是一种类似于 Windows .link 的“快捷方式”，文件内容指向了真实文件的存放地址

### 为什么要用 MediaWarp

当 Emby、Jellyfin 中存在 strm 文件并且指向正确时，客户端即可正确播放，如果资源是在远程服务器，此时 Emby 服务器会先从远程服务器下载资源然后再通过 ffmpeg 推流推送给客户端。如果在互联网中访问家庭局域网中的 Emby，其速度会受到家庭局域网出口的限制，即受到宽带上行速率的限制

使用 MediaWarp 后，当客户端需要访问某个影片时，MediaWarp 会尝试将客户端的请求重定向至远程服务的资源中，此时客户端会直接从远程服务中获取影片资源，流量不再经过 Emby 服务端，即不再受到宽带上行速率的限制

当客户端由于无法正确访问到远程服务器资源，例如浏览器拦截跨域请求、远程服务对请求头进行身份认证、客户端不支持影片资源格式（例如在浏览器中无法播放 H265 编码的视频）抑或是客户端需要转码播放时，客户端会请求推流播放，此时 MediaWarp 会将请求转发至 Emby 服务器，流量会再次经过 Emby 服务器（注：可在 MediaWarp 中配置，强制禁止进行转码，以拦截请求）

总而言之，MediaWarp 定位于服务端于客户端的一个中间件（也就是名字中为什么会带有 Warp），客户端请求原画播放时流量不再经过客户端，需要转码时服务端也能正确推流

### HttpStrm

这是 MediaWarp 对 strm 文件中内容形如http://host/path/stream的称谓，也是网络各大论坛中对 strm 文件狭义的称呼方式

### AlistStrm

其本质是本地文件，内容形如/Movies/Topgun (1986)/Topgun.mp4（可以使用 AutoFilm的AlistPath模式生成）,与传统本地 strm 文件不同的是，其路径真实存在于 Alist 服务的路径中并且 Emby 服务端可以无法访问 strm 文件内容目录（可以，但不推荐），请求原画播放时，MediaWarp 会尝试将客户端的请求重定向到 Alist 服务器的下载地址，抑或是 Alist 服务器上游的真实地址（网盘），区别在于浏览器是否收到 Alist 的控制，当 Alist 的访问策略是本机代理时，流量会受到 Alist 宽带的限制

## 安装

### 二进制可执行文件

在最新发布页面下载适合设备系统、架构的版本并解压，参考其中的config.yaml.example文件配置适合的配置文件，放在相对于可执行文件的./config/目录下，然后直接运行可执行文件

### 使用 Docker 安装

安装 Docker Engine 或 Docker Desktop

在发布页面下对应版本的压缩包，参考其中的config.yaml.example文件配置适合的配置文件，随后需要映射进容器的/config目录下

启动容器

使用 Docker Run 的方式安装：

```bash
docker run -d --name MediaWarp  -v ./config:/config -v ./logs:/logs -v ./static:/static akimio/mediawarp:0.2.0
```

使用 Docker Compose 的方式安装：

```yaml
services:
  mediawarp:
    image: akimio/mediawarp:0.2.0
    container_name: MediaWarp
    restart: unless-stopped
    ports:
      - 9000:9000
    volumes:
      - ./mediawarp/config:/config
      - ./mediawarp/logs:/logs
      - ./mediawarp/static:/static
```

```bash
docker compose up -d
```

## 配置文件

目前 MediaWarp 处于初期更新迭代状态，配置文件不稳定，可能不同版本间差异较大，且有不兼容的情况，具体配置以发布对应版本中的config.yaml.example为准

以下配置文件以 0.2.0版本为例，重点解述重要的配置项

### 配置文件格式

MediaWarp 仅支持 YAML 格式的配置文件（config.yaml）。

旧版本支持的 JSON、TOML 等格式已弃用，请确保使用正确格式。

### 媒体服务器类型

MediaServer.Type: 支持Emby、Jellyfin 和 FNTV（飞牛影视）。

配置示例：

```yaml
server:
  type: Jellyfin  # 对于 Jellyfin
```

或者

```yaml
server:
  type: FNTV      # 对于飞牛影视
```

### 日志与缓存 (Log & Cache)

log: 控制访问日志 (access) 和服务日志 (service) 是否输出到控制台 (console) 或文件 (file)。

cache: enable 是否启用缓存；*_ttl 设置不同资源的缓存有效期（如 http_strm_ttl, image_ttl）。支持的时间单位包括 “ns”, “us”, “ms”, “s”, “m”, “h”。

### 客户端过滤器 (Client)

可以屏蔽特定的客户端访问。enable 是否启用；mode 模式，BlackList (黑名单) 或 WhiteList (白名单)；list 客户端名称列表（User-Agent 中包含的关键字），例如 Infuse, Fileball。

### HTTPStrm

- transcode：false 强制关闭转码，告诉客户端服务器不支持转码，强制客户端尝试直接播放；true 保持原有转码设置。
- final_url：true 时 MediaWarp 会尝试请求目标 URL，如果目标返回重定向（302/301），它会跟随跳转直到获取最终的直链地址，然后将这个最终地址返回给客户端。
- prefix_list：指定 EmbyServer 中 Strm 文件路径的前缀。

### AlistStrm

- raw_url：false 响应 Alist 服务器的直链（302 跳转到 Alist 地址），要求客户端可以访问到 Alist 服务器；true 直接响应 Alist 上游的真实链接（Alist API 中的 raw_url 属性，如阿里云盘的下载链接），客户端不需要能访问 Alist，只需能访问网盘即可。
  - 推荐: 如果客户端在公网，且 Alist 在内网，建议设置为 true。
- TransCode：False 表示对应影片不支持转码播放并移除转码播放链接；True 不做任何修改。
- list：支持配置多个 Alist 服务器。每个 Alist 服务器需配置地址 (addr)、认证信息 (username/password 或 token) 以及对应的路径前缀 (prefix_list)。

### 字幕设置 (Subtitle)

仅 Emby 支持。enable 启用字幕优化功能；art2ass 是否开启 SRT 字幕转 ASS 字幕功能；ass_style 自定义转换后的 ASS 字幕样式。

### Web 页面修改 (Web)

支持 Emby 和 Jellyfin，FNTV（飞牛影视）不支持。
