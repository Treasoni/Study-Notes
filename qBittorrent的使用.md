# 下**砸**qBittorrent

目前qB分为官方版和增强版。

## qBittorrent 官方版

**特点**

1.  **来源：**qBittorrent 官方网站 / GitHub 发布的稳定版本。

2.  **核心功能：**

    a)  支持 BT、磁力链接下载

    b)  支持 RSS 自动下载

    c)  WebUI（网页远程控制）

    d)  下载队列管理、限速控制、种子管理

**优势：**

1.  稳定、可靠

2.  跨平台（Windows、Linux、macOS）

3.  社区活跃，有定期更新

**缺点：**

1.  默认界面比较简单

2.  没有一些高级功能或优化（例如更强的缓存优化或去广告）

## qBittorrent 增强版 / 优化版

**注意：**不同社区可能有不同称呼，比如 "qBittorrent Enhanced Edition" 或
"qBittorrent Advanced Build"。一般是第三方改版，不是官方维护的。

**特点**

1.  **增强功能：**

    a)  改进 WebUI 界面，更美观

    b)  增加下载优化选项（内存缓存优化、多线程优化）

    c)  自带 RSS 高级过滤器、定时任务

    d)  可能去掉官方版一些广告或不必要组件

2.  **第三方插件：**

    a)  有些增强版内置了 Tracker 服务器监控、IP 过滤增强

3.  **优势：**

    a)  对高级用户更友好

    b)  下载更快、更稳定（在一些系统/场景下）

4.  **缺点：**

    a)  不是官方发布，安全性略低

    b)  更新不如官方稳定，可能出现兼容性问题

    c)  部分增强版可能捆绑非官方插件，需要注意来源

# 基本设置

## 配置下载

这里主要是配置下载的保存路径和你种子的保存路径

1.  在**默认保存路径**中：换成你电脑或者是nas相应的文件夹路径

2.  在**复制下载完的.torrent文件到**：这个选项的作用就是对种子文件进行备份。以防后面数据丢失。

!![](assets/qBittorrent的使用/file-20260202224412228.png)

## 配置BitTorrent

这里我们要自动添加我们的tracker服务器到这里的**自动添加以下tracker到新的torrent**,这个选择中。

我们可以在下面找到相应的tracker：

公共 Tracker 列表合集：https://trackerslist.com/#/zh

Tracker
列表（GitHub）：https://github.com/XIU2/TrackersListCollection/blob/master/README-ZH.md

![](media/image2.png){width="4.027407042869641in"
height="3.7054483814523183in"}

## 速度和Web UI

保持默认即可

## 高级

在高级配置中如果有**自动更新**选项最好关闭，并且打开**总是向同级的所有
Tracker 汇报**

!