---
url: "https://newzone.top/services/dockers-on-nas/xiaoya.html"
title: "小雅 Alist：阿里云盘影视资源合集 | LearnData 开源笔记"
scraped_at: 2026-10-05T16:22:23+00:00
---

[跳到主要内容](https://newzone.top/services/dockers-on-nas/xiaoya.html#main-content)
#  小雅 Alist：阿里云盘影视资源合集
约 990 字大约 3 分钟
[小雅 Alist](https://hub.docker.com/r/xiaoyaliu/alist) 是基于阿里云盘的影视聚合方案，维护着一份持续更新的影音资源目录，省去了自己找片、管片的麻烦。官方配置指南见 [xiaoya docker 配置指南](https://xiaoyaliu.notion.site/xiaoya-docker-69404af849504fa5bcf9f2dd5ecaa75f)。
小雅 Alist Web 界面
## [Docker Compose 部署](https://newzone.top/services/dockers-on-nas/xiaoya.html#docker-compose-%E9%83%A8%E7%BD%B2)
推荐通过 Docker Compose 部署，详情参见 [Docker Compose 部署教程](https://newzone.top/services/dockers-on-nas/#%E9%83%A8%E7%BD%B2%E6%95%99%E7%A8%8B)。配置示例：

```
services:
  xiaoya:
    image: xiaoyaliu/alist:latest
    container_name: xiaoya
    volumes:
/volume1/docker/xiaoya:/data
    ports:
6789:80
    environment:
PUID=1026
PGID=100
TZ=Asia/Shanghai
    restart: always
```

部署完成后浏览器访问 `http://<你的服务器 IP 或域名>:6789` 即可使用。
## [更新 mytoken](https://newzone.top/services/dockers-on-nas/xiaoya.html#%E6%9B%B4%E6%96%B0-mytoken)
小雅访问阿里云盘依赖 Refresh Token，阿里后台会随时令 token 过期。出现"无法加载列表 / 播放失败"时先更新 token。
常用获取方式（任选其一）：
  * <https://aliyuntoken.vercel.app/>：用阿里云盘 App 扫码即得 32 位 refresh token（第三方 Vercel 部署，稳定性偶有波动）。
  * <https://alist.nn.ci/zh/guide/drivers/aliyundrive.html>：官方文档提供的扫码工具。
  * <https://opentoken.xiaoya.pro/>：小雅自家的 Open Token 刷新服务。


获得新 token 后，在小雅 Alist 的「存储」设置里替换对应字段并保存。
## [结合 Emby 使用](https://newzone.top/services/dockers-on-nas/xiaoya.html#%E7%BB%93%E5%90%88-emby-%E4%BD%BF%E7%94%A8)
若已经在用 Emby，可通过 strm 文件把小雅资源接入自己的媒体库，参考 [《如何使用 EMBY 展示小雅内容》教程](https://xiaoyaliu.notion.site/d353c9ceb15444d7b8e21ce6097ed739?v=145044ac8252470a9feef094ff1db520)。
同步脚本可一键拉取完整元数据：

```
# 一键下载元数据到指定媒体库与小雅配置目录
bash -c "$(curl -fsSL https://docker.xiaoya.pro/update_metainfo.sh)" -s /volume1/docker/emby /volume1/docker/xiaoya
```

> ⚠ **执行前请注意**
>   * 元数据体积可达 **160 GB** 左右，确认磁盘空间充足。
>   * 会覆盖指定 Emby 目录下的同名元数据；**先备份原`/volume1/docker/emby` 目录**。
>   * `curl | bash` 属于高权限操作，运行前建议先 `curl -fsSL https://docker.xiaoya.pro/update_metainfo.sh` 保存脚本、核对内容后再执行。
> 

## [TVBox 定制源](https://newzone.top/services/dockers-on-nas/xiaoya.html#tvbox-%E5%AE%9A%E5%88%B6%E6%BA%90)
小雅 Alist 自带 TVBox 源并随主项目一起维护，比第三方源稳定。配置步骤：
  1. 在小雅配置目录新建 `docker_address.txt`，写入小雅局域网地址，例如 `http://192.168.2.3:6789`。
  2. 重启容器。
  3. TVBox 的媒体源填 `http://192.168.2.3:6789/tvbox/my.json`。


## [保存到自己的阿里云盘为何失败](https://newzone.top/services/dockers-on-nas/xiaoya.html#%E4%BF%9D%E5%AD%98%E5%88%B0%E8%87%AA%E5%B7%B1%E7%9A%84%E9%98%BF%E9%87%8C%E4%BA%91%E7%9B%98%E4%B8%BA%E4%BD%95%E5%A4%B1%E8%B4%A5)
阿里云盘对跨账号的"转存 / 复制 / 移动"加了限制，即使通过 `show_my_ali.txt` 在小雅里挂载了个人云盘，复制仍会稳定返回 `Request failed with status code 403`。
可行的变通方案：
  * **单文件下载** ：小雅 Alist 内逐个下载到本地或 NAS。
  * **temp 目录批量下载** ：阿里云盘 App →「文件 > 资源库 > temp」，这里会列出你最近点击过的视频文件，可多选后一次性下载。


