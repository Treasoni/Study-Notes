---
url: "http://blog.liukewen.cn/2024/36TSGY2.html"
title: "17. FNOS飞牛OS使用docker-compost安装qbittorrent | KewenBlogs"
scraped_at: 2026-10-07T14:41:04+00:00
---

[文章 271](http://blog.liukewen.cn/archives/)[标签 12](http://blog.liukewen.cn/tags/)[分类 309](http://blog.liukewen.cn/categories/)
源码分析


#  安装主体文件
这里是使用compose安装的，这个方便compose配置文件如下：
yaml  
| 
```
123456789101112131415161718192021222324
```
 | 
```
# https://club.fnnas.com/forum.php?mod=viewthread&tid=2741&extra=page%3D1version: "3"services:  qbittorrent:    image: linuxserver/qbittorrent:4.6.6    container_name: qbittorrent    environment:      - PUID=0      - PGID=0      - TZ=Asia/Shanghai       - UMASK_SET=022      - WEBUI_PORT=6700  # Web UI端口      - TORRENTING_PORT=6701 # 监听端口，默认6881，修改为20000-65535区间值，下同    volumes:      - /vol1/1000/docker/qbittorrent/config:/config  # docker 路径映射      - /vol1/1000/docker/qbittorrent/theme:/theme  # 主题文件夹      - /vol1/1000/media/qbittorrent/downloads:/downloads # 下载文件夹      - /vol1/1000/media/qbittorrent/downloads:/watch # 监控文件夹    ports:      - 6700:6700  # 同上面Web UI端口一致      - 6701:6701      - 6701:6701/udp    restart: unless-stopped
```
 |  
| --- | --- |  
或者使用host模式
yaml  
| 
```
1234567891011121314151617181920
```
 | 
```
# https://club.fnnas.com/forum.php?mod=viewthread&tid=2741&extra=page%3D1version: "3"services:  qbittorrent:    image: linuxserver/qbittorrent:4.6.6    container_name: qbittorrent    environment:      - PUID=0      - PGID=0      - TZ=Asia/Shanghai       - UMASK_SET=022      - WEBUI_PORT=6700  # Web UI端口      - TORRENTING_PORT=6701 # 监听端口，默认6881，修改为20000-65535区间值，下同    volumes:      - /vol1/1000/docker/qbittorrent/config:/config  # docker 路径映射      - /vol1/1000/docker/qbittorrent/theme:/theme  # 主题文件夹      - /vol1/1000/media/qbittorrent/downloads:/downloads # 下载文件夹      - /vol1/1000/media/qbittorrent/downloads:/watch # 监控文件夹    restart: unless-stopped    network_mode: host
```
 |  
| --- | --- |  
然后启动，默认账号为admin，密码需要到运行日志里面找打开容器，找到运行日志，有类似于下面的则说明创建成功了
plaintext  
| 
```
1234567891011121314151617
```
 | 
```
******** Information ********To control qBittorrent, access the WebUI at: http://localhost:6700The WebUI administrator username is: adminThe WebUI administrator password was not set. A temporary password is provided for this session: 4X72ucMPJYou should set your own password in program preferences.Connection to localhost (::1) 6700 port [tcp/*] succeeded![ls.io-init] done.
```
 |  
| --- | --- |  
#  UI 主题
vuetorrent皮肤地址<https://github.com/VueTorrent/VueTorrent/releases/tag/v2.14.1>
下载到本地，然后传到qbittorrent配置的theme文件夹路径下
在页面配置中选择WEB_UI，然后填写路径`/theme/vuetorrent`
文章作者: 
文章链接: <http://blog.liukewen.cn/2024/36TSGY2.html>
版权声明: 本博客所有文章除特别声明外，均采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可协议。转载请注明来源 [KewenBlogs](http://blog.liukewen.cn)！
#### [微信扫一扫：分享 微信里点“发现”，扫一下 二维码便可将本文分享至朋友圈。 ](javascript:)
相关推荐
[ 2024-02-04 5. docker compose使用 简介引用 菜鸟教程引用 csdn Compose 是用于定义和运行多容器 Docker 应用程序的工具。通过 Compose，可以使用 YML 文件来配置应用程序需要的所有服务。然后，使用一个命令，就可以从 YML 文件配置中创建并启动所有服务。 Compose 使用的三个步骤： 使用 Dockerfile 定义应用程序的环境。 使用 docker-compose.yml 定义构成应用程序的服务，这样它们可以在隔离环境中一起运行。 执行 docker-compose up 命令来启动并运行整个应用程序。 安装docker-compose与docker关系 引用docker官网 Compose file format Docker Engine release Compose... ](http://blog.liukewen.cn/2024/151TW48.html "5. docker compose使用")[ 2024-01-18 5. 群晖docker安装qbittorrent 下载镜像ContainerManager 注册表中搜索下载linuxserver/qbittorrent 创建容器选中映像里面的linuxserver/qbittorrent，点击运行 配置 第一页： 容器名称随便 资源限制随便 自动重启随便 通过WebStation设置门户网页不选 第二页： 本地端口映射: 如 8999 映射 8999（这里必须相同的映射，否则下载没有网络） 存储空间映射：/docker/qbittorrent/config > config/docker/qbittorrent/downloads > downloads 环境在环境下面增加WEBUI_port 值为 上面本地映射端口如8999 网络修改成host(这一步也很重要，没有的话pt下载保种有问题) 第三页默认 启动启动，完成后点击详情，进入日志页，找到临时密码（旧版本默认admin/password）  ](http://blog.liukewen.cn/2024/2HEF59Z.html "5. 群晖docker安装qbittorrent")[ 2024-02-19 14. 群晖docker实现115网盘123网盘挂载共享文件夹 1. 说明115网盘上传只能是官方的客户端才可以，但是官方客户端不能直接挂载到群晖中，而下载的可以使用webdav的方式；因此需要分上传的解决方案和下载的解决方案，上传使用官方上传，手动，而读取网盘文件则挂载成文件夹123网盘建议通过官方客户端上传 115强烈建议使用 funcman/115pc + clouddriver2 来配合使用123强烈建议使用官方客户端+alist+clouddriver2挂载 2. 上传2.1. 115上传2.1.1. 官方客户端上传选择官方客户端上传则自行到115官方下载并上传即可 2.1.2. 第三方客户端上传2.1.2.1. 下载镜像下载镜像funcman/115pc 参考 2.1.2.2. 安装docker原版安装命令 1234567docker create --name=115pc \ -p 11580:5800 \ -p... ](http://blog.liukewen.cn/2024/GF5H5X.html "14. 群晖docker实现115网盘123网盘挂载共享文件夹")
kewen
保持对技术的热爱，追寻自己的人生
[文章 271](http://blog.liukewen.cn/archives/)[标签 12](http://blog.liukewen.cn/tags/)[分类 309](http://blog.liukewen.cn/categories/)
[我的Gitee主页](https://gitee.com/LiuKewenSc)
本博客使用[Hexo搭建](https://hexo.io/zh-cn/)，采用了[butterfly主题](https://butterfly.js.org/)
  1. [1. 安装主体文件](http://blog.liukewen.cn/2024/36TSGY2.html#%E5%AE%89%E8%A3%85%E4%B8%BB%E4%BD%93%E6%96%87%E4%BB%B6)
  2. [2. UI 主题](http://blog.liukewen.cn/2024/36TSGY2.html#UI-%E4%B8%BB%E9%A2%98)


最新文章
[1. websocket工程搭建](http://blog.liukewen.cn/2024/DCXN4N.html "1. websocket工程搭建")2026-09-21
[1. Netty基础工程搭建](http://blog.liukewen.cn/2024/2EE2F6F.html "1. Netty基础工程搭建")2026-09-21
[8. 解决Chrome强制把http成功定向为https的问题](http://blog.liukewen.cn/2024/11K1RYV.html "8. 解决Chrome强制把http成功定向为https的问题")2026-09-21
[5. 数据7层](http://blog.liukewen.cn/2023/2Z7DQQC.html "5. 数据7层")2026-09-21
[6. 路由器静态IP配置](http://blog.liukewen.cn/2024/3PXWC40.html "6. 路由器静态IP配置")2026-09-21
[7. https建立流程](http://blog.liukewen.cn/2024/3EX6CC5.html "7. https建立流程")2026-09-21
[3. URL-DNS](http://blog.liukewen.cn/2023/24SEDF0.html "3. URL-DNS")2026-09-21
[4. WebService](http://blog.liukewen.cn/2023/27K9TJT.html "4. WebService")2026-09-21
[1. 网络问题解决](http://blog.liukewen.cn/2023/3SHHMAN.html "1. 网络问题解决")2026-09-21
[2. 状态码](http://blog.liukewen.cn/2023/22GPJSD.html "2. 状态码")2026-09-21
