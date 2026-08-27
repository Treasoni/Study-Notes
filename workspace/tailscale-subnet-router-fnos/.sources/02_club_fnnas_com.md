---
url: "https://club.fnnas.com/forum.php?mod=viewthread&tid=28001"
title: "Tailscale 内网穿透部署教程，远程访问无压力 - 应用分享 飞牛私有云论坛 fnOS"
scraped_at: 2026-08-27T19:22:06+00:00
---

  * 用户名
  * Email


  * [论坛BBS](https://club.fnnas.com/forum.php "BBS")


请 后使用快捷导航没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register)
#  Tailscale 内网穿透部署教程，远程访问无压力
**16344** 查看   
|  

飞牛币
    10009  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-6-6 21:01:43_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=2158) |[倒序浏览](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&extra=&ordertype=1) [阅读模式](javascript:;)  
 | 
> 之前发过使用docker部署Tailscale的教程，不过是一年前的事情了，今天再重新发表一遍，这次使用compose部署更加方便，教程也会更加详细一点，希望对有需要的朋友有所帮助！
对于大部分用户来说，白嫖 Tailscale 已经足够了，免费计划只允许 3 账户，允许接入 100 台设备，运气好的时候你家宽带还能跑满，但是已有的时候就非常慢，不过这种时候很少，一般也都不差，有钱的也可以选择付费。 借助Tailscale，我们可以快速将家中或办公室内的服务器、小主机、NAS 等设备纳入同一个私有网络中，实现内网穿透、远程 SSH、子网访问甚至文件共享。
### 注册账号
先去官网注册账号，英文的，可以借助浏览器翻译 
```
https://tailscale.com/

​
```
推荐使用微软账号注册最方便 登录你的微软账号就行 首页
### 生成密钥
需要先生成密钥在部署docker，登录后 依次点击： ①：Settings ②：Personal Settings（ Keys） ③：Generate auth key…，生成客户端认证密钥 将生成的密钥暂时存起来，有效期90天。
### 部署Tailscale
**飞牛 Compose方式部署代码** 1️⃣我们需要先创建一个路径，这个路径储存我们的docker-Compose.yml的文件和配置文件 2️⃣打开Docker，Compose新增项目->输入项目名称->设置路径->上传或者创建docker- compose.yml把下面代码复制进去，点击完成直至构建完成 🐳Docker compose 注意看里面的注释， KEY 和 网段 这两个地方要换成你自己的 
```
version: '3.8'

services:
  tailscale:
    image: tailscale/tailscale
    container_name: tailscale
    hostname: tailscale-docker # 设备名称可以换
    network_mode: "host"
    cap_add:
      - NET_ADMIN
      - NET_RAW
    environment:
      - TS_AUTHKEY=xxx  # 替换成你的前面生成的key
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_ROUTES=192.168.31.0/24  # 替换成你实际内网段
    volumes:
      - ./tailscale-var-lib:/var/lib/tailscale
      - /dev/net/tun:/dev/net/tun
    restart: unless-stopped

volumes:
  tailscale-var-lib:

​
```
3️⃣ 等部署完成，我们在返回tailscale进行下一步配置 在回到tailscale可以看到我们 的飞牛设备已经在 里面了，并且分配了公网IP  **需要再设置一下：** 1. 找到刚刚添加进来的设备，点击名称 2 .找到前面代码中填入的网段Awaiting Approval（等待批准），点击 Edit 网段前面复选框打钩，然后保持 保存之后就变成已批准（ Approved ）了 这时候我们只要在需要访问的设备上安装tailscale客户端，登陆账号就可以通过分发的公网ip进行访问了 
```
https://tailscale.com/download

​
```
我在手机上下载了，将设备加入进去 正常访问飞牛NAS 我ping了一下下发的ip，响应速度还可以 所以说，没有公网的朋友可以使用tailscale也是一个非常不错的选择。  |  
| --- |  
收藏 
[本主题由 管理团队 于 2026-3-21 21:44 分类](https://club.fnnas.com/forum.php?mod=misc&action=viewthreadmod&tid=28001 "帖子模式")
 |  
|  公众号:知新坊  |  
|  

飞牛币
    2610  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 30, 距离下一级还需 20 积分


|  _2025-6-7 18:11:07_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=22589)  
 |  国内尤其是移动用这个差强人意~ |  
| --- |  
 |  
|  

飞牛币
    10009  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-6-8 14:19:09_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=2158)  
 | 
> [dlyangb1 发表于 2025-6-7 18:11](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=130920&ptid=28001) 国内尤其是移动用这个差强人意~
看地区的，不是所有的移动都这样 |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    340  

积分


主题
  
 |  
|  |  


|  _2025-6-9 23:08:02_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=30058)  
 |  大佬，我想请教一下，我按你的步骤一步一步往下了，他构建好了以后启动了没 3 秒又停止了，不知道是不是我内网的问题，能麻烦帮忙一下吗  |  
| --- |  
 |  
|  

飞牛币
    10009  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-6-10 09:48:19_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=2158)  
 | 
> [Gevak 发表于 2025-6-9 23:08](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=131723&ptid=28001) 大佬，我想请教一下，我按你的步骤一步一步往下了，他构建好了以后启动了没 3 秒又停止了，不知道是不是我 ...
你看看日志截图是什么，是什么报错 |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    826  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 60, 距离下一级还需 140 积分


|  _2025-6-10 11:18:10_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=13684)  
 |  晚上用不了  |  
| --- |  
 |  
|  

飞牛币
    10009  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-6-13 16:35:04_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=2158)  
 | 
> [sunrisesky 发表于 2025-6-10 11:18](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=131812&ptid=28001) 晚上用不了
基本没问题。能用 |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    130  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 31, 距离下一级还需 19 积分


|  _2025-8-24 23:06:25_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=63051)  
 |  你好，现在好像更新了，我在DOCKER 上面说问你给的代码，他报了警告
  * **警告訊息** **:**
    * **level=warning msg="/vol1/1000/docker/tailscale/docker-compose.yml: the attribute version is obsolete, it will be ignored, please remove it to avoid potential confusion"**
    * **這條訊息提醒您，在** **docker-compose.yml** **檔案中使用的** **version** **屬性已經過時。雖然 Docker Compose 會忽略這個屬性並繼續正常運作，但建議您將其移除，以避免未來產生混淆。這只是一個警告，並不會影響本次操作的成功。** 然后我想问一下，注释里面有一段需要更改成自己的内网 IP 网段但是后面有个斜杠24，这个是给他的端口嘛，必须加上，还是你内网的一部分? 因为我最终执行起来，他点开就直接闪退了光速弹出这3个 """ Container tailscale Starting Container tailscale Started Exited:0 """

 |  
| --- |  
 |  
|  

飞牛币
    65  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 12, 距离下一级还需 38 积分


|  _2025-10-7 12:06:30_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=87346)  
 |  安卓下载不了，window下载安装不了，这怎么办😣😣😣😣  |  
| --- |  
 |  
|  

飞牛币
    66  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2025-10-11 14:55:25_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=14029)  
 |  这个方案访问速度有多快，可以播放1080P视频吗？（NAS ipv6，访问端无ipv6）  |  
| --- |  
 |  
|  

飞牛币
    208  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 40, 距离下一级还需 10 积分


|  _2025-10-11 16:11:53_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=86840)  
 |  这种方法有很大的弊端就是docker一旦重启，就会变更IP地址，建议使用官方linux安装方法，使用ssh连接后命令行安装  |  
| --- |  
### 点评
禁用钥匙更新就是禁用ip更新，贴主这个方法安装时已经设置子路由了，就内网ip也能用 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=200311&ptid=28001) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=28001&repquote=200311&extra=&page=1)
2025-11-16 17:31 
请教：用这种办法以后更新如何更新 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=198964&ptid=28001) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=28001&repquote=198964&extra=&page=1)
2025-11-13 10:14 
 |  
|  

飞牛币
    109  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 13, 距离下一级还需 37 积分


|  _2025-10-27 17:50:17_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=89682)  
 |  有公网ip会有安全隐患么 |  
| --- |  
### 点评
这TM不是公网 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=207135&ptid=28001) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=28001&repquote=207135&extra=&page=1)
2025-11-26 11:49 
 |  
|  

飞牛币
    109  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 13, 距离下一级还需 37 积分


|  _2025-11-2 07:51:05_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=89682)  
 |  按楼主操作部署成功了，速度贼快，大大的赞！！  |  
| --- |  
 |  
|  

飞牛币
    554  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 70, 距离下一级还需 130 积分


|  _2025-11-13 10:14:42_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=853)  
 | 
> [underway 发表于 2025-10-11 16:11](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=184101&ptid=28001) 这种方法有很大的弊端就是docker一旦重启，就会变更IP地址，建议使用官方linux安装方法，使用ssh连接后命令 ...
请教：用这种办法以后更新如何更新 |  
| --- |  
 |  
|  

飞牛币
    320  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 11, 距离下一级还需 39 积分


|  _2025-11-15 09:42:07_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=94314)  
 |  学会了就是网速太慢了  |  
| --- |  
 |  
|  

飞牛币
    412  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 46, 距离下一级还需 4 积分


|  _2025-11-16 17:31:42_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=87436)  
 | 
> [underway 发表于 2025-10-11 16:11](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=184101&ptid=28001) 这种方法有很大的弊端就是docker一旦重启，就会变更IP地址，建议使用官方linux安装方法，使用ssh连接后命令 ...
禁用钥匙更新就是禁用ip更新，贴主这个方法安装时已经设置子路由了，就内网ip也能用 |  
| --- |  
 |  
|  

飞牛币
    3157  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 3, 距离下一级还需 47 积分


|  _2025-11-21 14:24:38_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=99449)  
 |  其实ssh连接后一行代码搞定了，不用这么麻烦  |  
| --- |  
 |  
|  

飞牛币
    1524  

积分


主题
  
 |  
|  |  


|  _2025-11-26 11:49:27_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=84881)  
 | 
> [StephXue 发表于 2025-10-27 17:50](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=191556&ptid=28001) 有公网ip会有安全隐患么
这TM不是公网 |  
| --- |  
 |  
|  

飞牛币
    463  

积分


主题
  
 |  
|  |  


|  _2025-12-3 23:49:01_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=98809)  
 |  建议不要设置 `- TS_ROUTES=192.168.31.0/24  # 替换成你实际内网段` 这个tailscale的子网路由，如果你设置成你家的内网段，会导致内网互相访问，也走飞牛的tailscale的子网，导致延迟变高，虽然外网访问的时候也可以用内网ip访问，但是内网互相访问就被这个影响了，而且这个时候，如果你飞牛是关机状态，而你用的设备的tailscale没关的话，会导致内网里的设备，你都ping不通了，因为他没法通过飞牛的子网转发了，如果有解决办法，请告诉我  |  
| --- |  
### 点评
不会吧，你说的是exit node，出口节点吧，如果终端不设置出口节点，那么内网设备不会强制走tailscale的 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=215334&ptid=28001) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=28001&repquote=215334&extra=&page=1)
2025-12-14 17:38 
 |  
|  

飞牛币
    253  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 48, 距离下一级还需 2 积分


|  _2025-12-14 17:38:17_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=90019)  
 | 
> [落安x 发表于 2025-12-3 23:49](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=210764&ptid=28001) 建议不要设置 - TS_ROUTES=192.168.31.0/24 # 替换成你实际内网段 这个tailscale的子网路由，如果你设置成 ...
不会吧，你说的是exit node，出口节点吧，如果终端不设置出口节点，那么内网设备不会强制走tailscale的 |  
| --- |  
 |  
|  

飞牛币
    208  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 14, 距离下一级还需 36 积分


|  _2025-12-17 14:48:36_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=103410)  
 |  测试了一下，没有星空快，影视缓冲不下了  |  
| --- |  
 |  
|  

飞牛币
    1081  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2026-2-8 21:36:07_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=116128)  
 |  一直重启中，用不了……  |  
| --- |  
 |  
|  

飞牛币
    2333  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 6, 距离下一级还需 44 积分


|  _2026-2-10 10:29:05_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=9550)  
 |  搞定了，可以用，很赞！  |  
| --- |  
 |  
|  

飞牛币
    474  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 3, 距离下一级还需 47 积分


|  _2026-3-29 12:15:40_ 来自手机 [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=104228)  |  
|  

飞牛币
    312  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 10, 距离下一级还需 40 积分


|  _2026-5-26 10:16:38_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=57071)  
 |  一次就搞定了，感谢  |  
| --- |  
 |  
|  

飞牛币
    6  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2026-6-28 20:05:29_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=164896)  
 |  安装好显示已连接 但输入ip就是连不上 入户网段和nas所在网段不一致导致的么 |  
| --- |  
 |  
|  

飞牛币
    171  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2026-7-7 22:08:03_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=28001&page=1&authorid=100685)  
 |  安卓版的哪位有？发一个。  |  
| --- |  
 |  
#### 音乐内测玩家
首批飞牛音乐内测玩家临时勋章
#### 社区上线纪念勋章
飞牛私有云社区上线，晒NAS活动纪念勋章
#### 社区共建团荣誉勋章
飞牛社区组织荣誉认证，为飞牛私有云社区发展无私奉献，发光发热
#### 飞牛百度网盘玩家
参与“极速下载，畅享特权”百度网盘活动纪念
#### fnOS1.0上线纪念勋章
飞牛fnOS 1.0 上线，晒体验活动纪念勋章
#### EVO2产品纪念
纪念飞牛首款自有硬件EVO2
#### 灌水之星
别人逛社区，TA住在社区。 发帖如呼吸，互动如本能， 水得理直气壮，水得令人佩服
#### AMD适配纪念勋章
纪念2026年4月16日，飞牛fnOS率先适配AMD在系统编解码、杜比、AI环境，并正式开启OTA
#### 音乐上线纪念勋章
纪念公测两周年飞牛音乐正式上线
[粤ICP备2023020469号](https://beian.miit.gov.cn/)
