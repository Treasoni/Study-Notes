---
url: "https://club.fnnas.com/forum.php?mod=viewthread&tid=13887"
title: "飞牛上使用 Docker Compose 部署 Tailscale - 应用分享 飞牛私有云论坛 fnOS"
scraped_at: 2026-08-27T19:22:06+00:00
---

  * 用户名
  * Email


  * [论坛BBS](https://club.fnnas.com/forum.php "BBS")


请 后使用快捷导航没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register)
#  飞牛上使用 Docker Compose 部署 Tailscale
**11823** 查看   
|  

飞牛币
    154  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 5, 距离下一级还需 45 积分


|  _2025-2-5 09:02:06_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=36609) |[倒序浏览](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&extra=&ordertype=1) [阅读模式](javascript:;)  
 |  [i=s] 本帖最后由 417042482 于 2025-2-7 10:47 编辑 [/i]<br /> <br /> 尽管 Tailscale 官网提供了Linux环境的一键部署命令，但是考虑让飞牛长期稳定运行，还是尽量少做改动。 基于此，这里推荐使用 Docker Compose部署，通用性好，以后要迁移也方便： ``` services: tailscale: image: tailscale/tailscale:stable # 使用stable标签，每次部署或重新启动容器时，都将使用最新的稳定版（官方建议的） container_name: tailscale network_mode: host # 使用host模式 privileged: true # 特权模式 environment: TS_AUTHKEY: tskey-auth-XXXXXXXXXXX #获取方法：TS管理页面 → Settings → Keys → Generate auth key，创建好了复制过来 TS_STATE_DIR: /var/lib/tailscale # 状态目录, 作用是容器重新启动后配置不变 TS_ROUTES: 192.168.1.0/24 # 子网路由，推荐使用，设置成自己的网段 TS_HOSTNAME: fnos # 节点名字, 可自定义 volumes: - /vol1/1000/docker/tailscale/state:/var/lib/tailscale # 映射状态目录, 冒号左边路径可自定义 devices: - /dev/net/tun:/dev/net/tun cap_add: - net_admin restart: unless-stopped ``` 关于 Tailscale Key 的获取方法，这里给一张图： ![image.png](data/attachment/forum/202502/05/090104dmffnan0nuanqnal.png "image.png")   |  
| --- |  
收藏 
[本主题由 管理团队 于 2026-3-19 14:35 移动](https://club.fnnas.com/forum.php?mod=misc&action=viewthreadmod&tid=13887 "帖子模式")
### **本帖子中包含更多资源**
您需要 [登录](https://club.fnnas.com/member.php?mod=logging&action=login) 才可以下载或查看，没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register "注册账号")
x
 |  
|  

飞牛币
    554  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 70, 距离下一级还需 130 积分


|  _2025-2-27 18:25:02_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=853)  
 |  请教：TS_ROUTES: 192.168.1.0/24 这个网段 是本地路由器网段 还是tailscale 的虚拟网段？ |  
| --- |  
### 点评
本地路由器网段 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=80763&ptid=13887) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=13887&repquote=80763&extra=&page=1)
2025-3-2 15:12 
 |  
|  

飞牛币
    7166  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 15, 距离下一级还需 35 积分


|  _2025-3-2 15:12:45_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=14361)  
 |  本地路由器网段 |  
| --- |  
 |  
|  

飞牛币
    316  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 28, 距离下一级还需 22 积分


|  _2025-3-17 14:49:22_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=39507)  
 |  设置成自己的网段是为了在家里能在不开TS的情况下无缝衔接家里局域网吗 |  
| --- |  
### 点评
Tailscale子网路由实现的功能是，一个局域网内，只要有一个设备安装了Tailscale，外网设备就可以通过该设备访问家里局域网的其他设备。 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=96695&ptid=13887) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=13887&repquote=96695&extra=&page=1)
2025-3-31 10:30 
 |  
|  

飞牛币
    154  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 5, 距离下一级还需 45 积分


|  _2025-3-31 10:30:46_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=36609)  
 | 
> [z14211 发表于 2025-3-17 14:49](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=88970&ptid=13887) 设置成自己的网段是为了在家里能在不开TS的情况下无缝衔接家里局域网吗
Tailscale子网路由实现的功能是，一个局域网内，只要有一个设备安装了Tailscale，外网设备就可以通过该设备访问家里局域网的其他设备。 |  
| --- |  
### 点评
怎么弄？ 路由器有这个，NAS没有，怎么访问NAS [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=134203&ptid=13887) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=13887&repquote=134203&extra=&page=1)
2025-6-16 13:39 
 |  
|  

飞牛币
    27  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 2, 距离下一级还需 48 积分


|  _2025-6-16 13:38:51_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=68534)  
 |  怎么访问路由器旁边的NAS  |  
| --- |  
 |  
|  

飞牛币
    27  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 2, 距离下一级还需 48 积分


|  _2025-6-16 13:39:31_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=68534)  
 | 
> [417042482 发表于 2025-3-31 10:30](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=96695&ptid=13887) Tailscale子网路由实现的功能是，一个局域网内，只要有一个设备安装了Tailscale，外网设备就可以通过该设 ...
怎么弄？ 路由器有这个，NAS没有，怎么访问NAS  |  
| --- |  
 |  
|  

飞牛币
    633  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 11, 距离下一级还需 39 积分


|  _2025-7-29 10:25:15_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=30693)  
 |  部署后 ts 容器不停重启不能用 看不懂日志  |  
| --- |  
### 点评
检查一下你的api key 是不是用了single use模式， 生成key的时候，要把reusable按钮打开 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=157755&ptid=13887) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=13887&repquote=157755&extra=&page=1)
2025-8-11 11:22 
 |  
|  

飞牛币
    4674  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 109, 距离下一级还需 91 积分


|  _2025-8-11 11:22:39_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=6812)  
 | 
> [anywn 发表于 2025-7-29 10:25](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=152422&ptid=13887) 部署后 ts 容器不停重启不能用 看不懂日志
检查一下你的api key 是不是用了single use模式， 生成key的时候，要把reusable按钮打开 |  
| --- |  
 |  
|  

飞牛币
    253  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 48, 距离下一级还需 2 积分


|  _2025-12-14 17:42:25_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=13887&page=1&authorid=90019)  
 |  但是这个docker的话想开启exit node比较麻烦  |  
| --- |  
 |  
#### fnOS1.0上线纪念勋章
飞牛fnOS 1.0 上线，晒体验活动纪念勋章
[粤ICP备2023020469号](https://beian.miit.gov.cn/)
