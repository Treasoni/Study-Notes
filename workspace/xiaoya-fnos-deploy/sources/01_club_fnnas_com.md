---
url: "https://club.fnnas.com/forum.php?mod=viewthread&tid=9690"
title: "小雅Alist部署教程【解决应用中心版本无数据】 - 应用分享 飞牛私有云论坛 fnOS"
scraped_at: 2026-10-05T16:18:40+00:00
---

  * 用户名
  * Email


  * [论坛BBS](https://club.fnnas.com/forum.php "BBS")


请 后使用快捷导航没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register)
#  小雅Alist部署教程【解决应用中心版本无数据】
**31772** 查看   
|  

飞牛币
    5341  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2024-12-27 11:15:33_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=16259) |[倒序浏览](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&extra=&ordertype=1) [阅读模式](javascript:;)  
 |  飞牛NAS应用中心自带的小雅Alist实测无法正常获取到视频数据，如果已经安装了应用中心的小雅Alist需要先卸载掉，然后按照本文的教程重新部署。 1.在飞牛NAS的文件管理里面，创建一个用于存放小雅Alist的文件夹，如上图所示。同时在电脑上创建一个空白的docker-compose.yml文件上传。不会创建空白文件的在电脑任何地方右键新建txt文档，然后重命名即可。在data文件夹右键点击后选择复制原始路径，原始路径在下面的配置参数里需要使用。 `      - /vol2/1000/docker2/xiaoya/data:/data # 将容器中的 /data 目录映射到名为 xiaoya 的数据卷，用于持久化存储 ` 这一行参数，需要把冒号左侧的路径换成你刚才创建的路径。 2.双击打开docker-compose.yml，把下面的代码复制进去后保存。每行代码都有注释，可以修改对应的值。其中三个端口可以自定义，自己容易记住并且和飞牛的其他服务使用的端口不冲突即可。冒号左侧为宿主机端口，可以修改为你需要使用的端口，右侧不需要修改。 `ALIYUN_TOKEN` `ALIYUN_OPEN_TOKEN` `ALIYUN_FOLDER_ID` 这三个是必填项，具体的获取方法请自己搜索解决，网上这样的教程很多。搜索关键词是—小雅Alist 阿里云盘配置。按照各种教程里的方法获取后复制到配置文件对应的参数位置即可，也就是参数右侧两个引号之间的位置。 如有挂载夸克、115网盘的需求，也可以在配置文件里填写参数。配置文件里面的其他参数根据自己的徐倩倩填写，每个参数我都写了详细的注释。 
```
services:
  alist:
    image: ghcr.io/monlor/xiaoya-alist:latest # 使用的镜像，来源于 GitHub 容器注册表
    volumes:
      - /vol2/1000/docker2/xiaoya/data:/data # 将容器中的 /data 目录映射到名为 xiaoya 的数据卷，用于持久化存储
    ports:
      - "5677:5678" # 宿主机端口 5677 映射到容器的 5678 端口，alist Web 服务
      - "5345:2345" # 宿主机端口 5345 映射到容器的 2345 端口，备用端口或其他服务使用
      - "5346:2346" # 宿主机端口 5346 映射到容器的 2346 端口，备用端口或其他服务使用
    environment: # 定义环境变量，用于容器运行时的配置
      TZ: Asia/Shanghai # 设置容器的时区为上海时区
      ALIYUN_TOKEN: "" # 阿里云盘的访问令牌，需要用户填写
      ALIYUN_OPEN_TOKEN: "" # 阿里云盘的开放访问令牌，需要用户填写
      ALIYUN_FOLDER_ID: "" # 阿里云盘的文件夹 ID，用于指定操作目录
      QUARK_COOKIE: "" # 夸克网盘的 Cookie，需要用户填写，非必填。
      PAN115_COOKIE: "" # 115 网盘的 Cookie，需要用户填写，非必填。
      AUTO_UPDATE_ENABLED: "true" # 是否启用自动更新小雅 alist 的功能，"true" 启用，"false" 禁用
      AUTO_CLEAR_ENABLED: "true" # 是否启用阿里云盘自动清理功能，"true" 启用，"false" 禁用
      AUTO_CLEAR_INTERVAL: "" # 自动清理间隔时间，单位为分钟，范围为 0-60，默认为空（使用默认设置）
      PIKPAK_USER: "" # PikPak 用户名和密码，格式为 `email:password`，非必填
      TVBOX_SECURITY: "false" # 是否启用 TVBox 随机订阅地址功能，"true" 启用，"false" 禁用
      WEBDAV_PASSWORD: "" # WebDAV 的用户密码，默认用户为 dav
      ALIST_ADDR: "http://alist:5678" # 容器内部的 alist 地址，通常不需要修改
      EMBY_ENABLED: "false" # 是否启用 Emby 功能，"true" 启用，"false" 禁用
      JELLYFIN_ENABLED: "false" # 是否启用 Jellyfin 功能，"true" 启用，"false" 禁用
      AUTO_UPDATE_EMBY_CONFIG_ENABLED: "false" # 是否启用 Emby 配置的自动更新功能
      AUTO_UPDATE_EMBY_INTERVAL: "" # Emby 配置自动更新的间隔时间，单位为天
      AUTO_UPDATE_EMBY_METADATA_ENABLED: "false" # 是否启用 Emby 元数据的自动更新功能
      CLEAR_TEMP: "true" # 下载解压后是否清理临时文件，"true" 启用，"false" 禁用
    restart: unless-stopped # 设置容器的重启策略，容器意外停止时自动重启
    networks:
      - default # 指定容器使用的网络，这里使用默认网络

networks:
  default: # 定义默认网络，容器间可以通过服务名互相访问

​
```
3.打开飞牛的Docker管理，按上图的指示创建项目，项目名称自定义，路径就是刚才创建的文件夹。弹窗点击确定，然后勾选创建项目后立即启动，然后点击完成即可。 4.项目创建成功后，在容器里就能看到创建号的小雅Alist容器。初始化的时候需要几分钟时间，耐心等待即可。 5.使用飞牛的局域网IP+配置文件里面设置的第一个端口号,比如我的是http://192.168.2.146:5677 , webdav的配置的用户名和密码是guest/guest_Api789。  |  
| --- |  
收藏 
送赞
### **本帖子中包含更多资源**
您需要 [登录](https://club.fnnas.com/member.php?mod=logging&action=login) 才可以下载或查看，没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register "注册账号")
x
 |  
|  

飞牛币
    14  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 6, 距离下一级还需 44 积分


|  _2025-1-25 10:47:13_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=35955)  
 |  开始生成配置文件... /start.sh: line 13: /data/docker_address.txt: Operation not permitted 一直失败，有哪位大佬帮我看看，我是那一步错了 |  
| --- |  
### 点评
2025-9-3 10:25 
请问解决了吗？ 在线蹲一个回复 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=71146&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=71146&extra=&page=1)
2025-2-12 17:33 
 |  
|  

飞牛币
    154  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 9, 距离下一级还需 41 积分


|  _2024-12-27 15:18:12_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=15556)  
 |  大佬厉害，跟着做就成功了，👍 |  
| --- |  
 |  
|  

飞牛币
    3060  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 38, 距离下一级还需 12 积分


|  _2024-12-30 10:54:22_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=26836)  
 |  成功了，大佬 |  
| --- |  
 |  
|  

飞牛币
    3060  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 38, 距离下一级还需 12 积分


|  _2024-12-30 10:56:09_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=26836)  
 |  _本帖最后由 mengs 于 2024-12-31 09:33 编辑_ 自动清理间隔时间，范围为 0-60，60分钟一部电影没看完就被清理了 ，然后放不了，可以设置更长或者自动设置云空间满了再清理？PS:ALIYUN_TOKEN 第二天就失效了，需要重新获取  |  
| --- |  
### 点评
我的没失效，好着呢 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=44413&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=44413&extra=&page=1)
2025-1-7 17:41 
 |  
|  

飞牛币
    36  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2025-1-6 11:19:56_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=25538)  
 |  一直提示。。。获取设置失败： 请稍后，正在加载储存 |  
| --- |  
### 点评
等一会儿就好了！ [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=44412&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=44412&extra=&page=1)
2025-1-7 17:40 
 |  
|  

飞牛币
    5341  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-1-7 17:40:43_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=16259)  
 |  等一会儿就好了！ |  
| --- |  
 |  
|  

飞牛币
    5341  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-1-7 17:41:02_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=16259)  
 |  我的没失效，好着呢 |  
| --- |  
### 点评
我的操作问题，现在好了 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=45228&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=45228&extra=&page=1)
2025-1-9 12:20 
 |  
|  

飞牛币
    426  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 64, 距离下一级还需 136 积分


|  _2025-1-8 09:52:28_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=29411)  
 |  我看日志是建立成功了 但是无法打开小雅 在浏览器输入192.168.10.10:5678（NAS的局域网IP），打不开，显示“拒绝了我们的连接请求” 按照教程重新尝试了好多次，docker的网络IP也换过，都是这样。 丘指点 |  
| --- |  
 |  
|  

飞牛币
    426  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 64, 距离下一级还需 136 积分


|  _2025-1-8 11:13:07_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=29411)  
 |  补充一下，yml里这样填了webdav WEBDAV_PASSWORD: "guest/guest_Api789" # WebDAV 的用户密码，默认用户为 dav 反正就是怎么折腾都不行，好难受啊 |  
| --- |  
### 点评
用户名： guest 密码：guest_Api789 路径：/dav [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=44691&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=44691&extra=&page=1)
2025-1-8 11:19 
 |  
|  

飞牛币
    5341  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-1-8 11:19:06_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=16259)  
 |  用户名： guest 密码：guest_Api789 路径：/dav |  
| --- |  
### 点评
是这样填吗？ WEBDAV_PASSWORD: "用户名：guest 密码：guest_Api789 路径：/dav" # WebDAV 的用户密码，默认用户为 dav [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=44696&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=44696&extra=&page=1)
2025-1-8 11:22 
 |  
|  

飞牛币
    426  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 64, 距离下一级还需 136 积分


|  _2025-1-8 11:22:24_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=29411)  
 |  是这样填吗？ WEBDAV_PASSWORD: "用户名：guest 密码：guest_Api789 路径：/dav" # WebDAV 的用户密码，默认用户为 dav |  
| --- |  
### 点评
[md]![Picsew_20250108113946.jpeg](data/attachment/forum/202501/08/114136pphgvh0n9rrlhcnr.jpeg "Picsew_20250108113946.jpeg") 不用写，没人就是这样的 [/md] [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=44718&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=44718&extra=&page=1)
2025-1-8 11:42 
 |  
|  

飞牛币
    5341  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-1-8 11:42:01_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=16259)  
 |  ![Picsew_20250108113946.jpeg](data/attachment/forum/202501/08/114136pphgvh0n9rrlhcnr.jpeg "Picsew_20250108113946.jpeg") 不用写，默认就是这样的  不用写，默认就是这样的  |  
| --- |  
### **本帖子中包含更多资源**
您需要 [登录](https://club.fnnas.com/member.php?mod=logging&action=login) 才可以下载或查看，没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register "注册账号")
x
### 点评
[md]永远是这样……被拒绝…docker里的小雅明明成功运行，看日志也正常 ![IMG_9456.png](data/attachment/forum/202501/08/115826nisdsvj2225ng82v.png "IMG_9456.png") [/md] [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=44728&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=44728&extra=&page=1)
2025-1-8 11:59 
 |  
|  

飞牛币
    426  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 64, 距离下一级还需 136 积分


|  _2025-1-8 11:59:37_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=29411)  
 |  永远是这样……被拒绝…docker里的小雅明明成功运行，看日志也正常 ![IMG_9456.png](data/attachment/forum/202501/08/115826nisdsvj2225ng82v.png "IMG_9456.png")  永远是这样……被拒绝…docker里的小雅明明成功运行，看日志也正常   |  
| --- |  
### **本帖子中包含更多资源**
您需要 [登录](https://club.fnnas.com/member.php?mod=logging&action=login) 才可以下载或查看，没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register "注册账号")
x
 |  
|  

飞牛币
    426  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 64, 距离下一级还需 136 积分


|  _2025-1-8 12:09:43_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=29411)  
 |  端口改成5677，成功挂载了！！搞了3天终于前进了一步✌️ |  
| --- |  
 |  
|  

飞牛币
    3060  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 38, 距离下一级还需 12 积分


|  _2025-1-9 12:20:13_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=26836)  
 | 
> [MRBANK 发表于 2025-1-7 17:41](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=44413&ptid=9690) 我的没失效，好着呢
我的操作问题，现在好了 |  
| --- |  
 |  
|  

飞牛币
    23  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 3, 距离下一级还需 47 积分


|  _2025-1-10 21:12:15_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=27297)  
 |  alist Pulling alist Error Get "https://ghcr.io/v2/": read tcp 192.168.50.56:55682->20.205.243.164:443: read: connection reset by peer Error response from daemon: Get "https://ghcr.io/v2/": read tcp 192.168.50.56:55682->20.205.243.164:443: read: connection reset by peer 一直报这个错是什么原因,可以帮忙解答下吗 谢谢 |  
| --- |  
### 点评
兄弟我找到原因了，是GitHub的原因，换成国内镜像就可以了，具体参考这个https://blog.csdn.net/asdfaa/article/details/137845694 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=69479&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=69479&extra=&page=1)
2025-2-9 21:56 
我也是这个问题，一直搞不定，换了源也不行，哪位大佬指导下！ [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=69115&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=69115&extra=&page=1)
2025-2-8 22:47 
 |  
|  

飞牛币
    115  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 4, 距离下一级还需 46 积分


|  _2025-1-11 17:19:13_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=21058)  
 |  好教程，支持！ |  
| --- |  
 |  
|  

飞牛币
    35  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 8, 距离下一级还需 42 积分


|  _2025-1-21 11:08:28_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=32796)  
 |  我看不见大佬这边附件，是等级不够吗 |  
| --- |  
### 点评
我没有上传附件啊，就是图片，这边可以显示啊 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=60043&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=60043&extra=&page=1)
2025-1-21 16:40 
 |  
|  

飞牛币
    5341  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-1-21 16:40:14_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=16259)  
 |  我没有上传附件啊，就是图片，这边可以显示啊 |  
| --- |  
 |  
|  

飞牛币
    28  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 3, 距离下一级还需 47 积分


|  _2025-2-6 09:06:10_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=37856)  
 |  好教程，谢谢  |  
| --- |  
 |  
|  

飞牛币
    28  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 3, 距离下一级还需 47 积分


|  _2025-2-7 16:07:18_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=37856)  
 |  请教一下：为什么nas过一段时间，就登不上，显示： failed get storage: please add a storage first. |  
| --- |  
 |  
|  

飞牛币
    132  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 24, 距离下一级还需 26 积分


|  _2025-2-8 08:29:22_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=38094)  
 |  大佬，远程怎么访问呢 |  
| --- |  
### 点评
配置ddns就可以访问了 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=68503&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=68503&extra=&page=1)
2025-2-8 09:49 
 |  
|  

飞牛币
    5341  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-2-8 09:49:38_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=16259)  
 |  配置ddns就可以访问了 |  
| --- |  
### 点评
大佬，怎么配置DDNS呢，我是刚入坑新手 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=69736&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=69736&extra=&page=1)
2025-2-10 11:48 
大佬，这两天有报错了，BadRequest:driveId, fileId cannot be empty，怎么搞啊，谢谢 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=69076&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=69076&extra=&page=1)
2025-2-8 21:37 
 |  
|  

飞牛币
    68  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 3, 距离下一级还需 47 积分


|  _2025-2-8 21:37:11_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=32494)  
 |  大佬，这两天有报错了，BadRequest:driveId, fileId cannot be empty，怎么搞啊，谢谢  |  
| --- |  
 |  
|  

飞牛币
    74  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 6, 距离下一级还需 44 积分


|  _2025-2-8 22:47:26_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=38507)  
 |  我也是这个问题，一直搞不定，换了源也不行，哪位大佬指导下！ |  
| --- |  
 |  
|  

飞牛币
    74  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 6, 距离下一级还需 44 积分


|  _2025-2-9 21:56:07_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=38507)  
 |  兄弟我找到原因了，是GitHub的原因，换成国内镜像就可以了，具体参考这个<https://blog.csdn.net/asdfaa/article/details/137845694>  |  
| --- |  
 |  
|  

飞牛币
    132  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 24, 距离下一级还需 26 积分


|  _2025-2-10 11:48:41_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=38094)  
 | 
> [MRBANK 发表于 2025-2-8 09:49](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=68503&ptid=9690) 配置ddns就可以访问了
大佬，怎么配置DDNS呢，我是刚入坑新手 |  
| --- |  
 |  
|  

飞牛币
    60  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 13, 距离下一级还需 37 积分


|  _2025-2-12 17:32:49_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=39591)  
 |  也是一样的问题，有没有老哥碰到解决的？ 开始生成配置文件... /start.sh: line 13: /data/docker_address.txt: Operation not permitted 一直失败，有哪位大佬帮我看看，我是那一步错了 |  
| --- |  
 |  
|  

飞牛币
    60  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 13, 距离下一级还需 37 积分


|  _2025-2-12 17:33:22_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=39591)  
 |  请问解决了吗？ 在线蹲一个回复 |  
| --- |  
 |  
|  

飞牛币
    68  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 3, 距离下一级还需 47 积分


|  _2025-2-15 09:44:21_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=32494)  
 |  前两天好用了两天，这两天有报错这个了failed get storage: please add a storage first.大佬怎么搞啊 |  
| --- |  
### 点评
docker的设置里需要设置一个文件夹到/tmp。我也遇到了，看到报错信息说是，找不到下载好的更新文件。 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=76847&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=76847&extra=&page=1)
2025-2-23 19:02 
 |  
|  

飞牛币
    38  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 4, 距离下一级还需 46 积分


|  _2025-2-17 00:16:50_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=38270)  
 |  可以把小雅数据存本地，然后飞牛tv里面添加这些数据吗？ |  
| --- |  
 |  
|  

飞牛币
    241  

积分


主题
  
 |  
|  |  


|  _2025-2-20 18:18:40_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=41314)  
 |  如果用夸克上面是不是只填写夸克的Cookie就可以了？就不需要填写阿里云盘的那三个参数了吧？ |  
| --- |  
 |  
|  

飞牛币
    96  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 6, 距离下一级还需 44 积分


|  _2025-2-23 19:02:11_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=12393)  
 |  docker的设置里需要设置一个文件夹到/tmp。我也遇到了，看到报错信息说是，找不到下载好的更新文件。 |  
| --- |  
 |  
|  

飞牛币
    115  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 18, 距离下一级还需 32 积分


|  _2025-3-11 11:42:54_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=46160)  
 |  谢谢大佬 一次成功了👍 |  
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


|  _2025-3-12 01:15:33_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=46353)  
 |  一遍成功，特意登录点个赞谢谢 |  
| --- |  
 |  
|  

飞牛币
    21  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2025-3-13 13:08:31_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=46678)  
 |  _本帖最后由 厚薄x 于 2025-3-13 13:13 编辑_ 感谢楼主 |  
| --- |  
 |  
|  

飞牛币
    60  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 2, 距离下一级还需 48 积分


|  _2025-3-15 21:43:42_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=46488)  |  
|  

飞牛币
    512  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 20, 距离下一级还需 30 积分


|  _2025-3-19 13:41:38_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=45419)  
 |  大佬第一个没找到在哪里设置 - /vol2/1000/docker2/xiaoya/data:/data # 将容器中的 /data 目录映射到名为 xiaoya 的数据卷，用于持久化存储 |  
| --- |  
 |  
|  

飞牛币
    512  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 20, 距离下一级还需 30 积分


|  _2025-3-19 14:43:49_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=45419)  
 |  配置成功了，多谢大佬。 |  
| --- |  
 |  
|  

飞牛币
    225  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 7, 距离下一级还需 43 积分


|  _2025-3-19 16:18:49_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=35578)  
 |  ALIYUN_TOKEN 、ALIYUN_OPEN_TOKEN ，alist文档——阿里云盘 Open拿到的是refresh_token，要怎么填呢？ |  
| --- |  
### 点评
https://alist.nn.ci/zh/tool/aliyundrive/request.html [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=91203&ptid=9690) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=12&tid=9690&repquote=91203&extra=&page=1)
2025-3-21 10:45 
 |  
|  

飞牛币
    5341  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-3-21 10:45:39_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=16259)  
 | 
> [CheukWing 发表于 2025-3-19 16:18](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=90152&ptid=9690) ALIYUN_TOKEN 、ALIYUN_OPEN_TOKEN ，alist文档——阿里云盘 Open拿到的是refresh_token，要怎么填呢？ ...
<https://alist.nn.ci/zh/tool/aliyundrive/request.html>  |  
| --- |  
 |  
|  

飞牛币
    37  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 4, 距离下一级还需 46 积分


|  _2025-3-23 12:54:43_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=49194)  
 |  这个WEBDAV也没用吧？我的这个挂上之后，能看见不能不放，也不能下载。。。 |  
| --- |  
 |  
|  

飞牛币
    37  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 2, 距离下一级还需 48 积分


|  _2025-3-30 11:29:41_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=50334)  
 |  有坑啊，lz使用了github的镜像源，在国内难以访问。需要把配置文件内第三行 image: ghcr.io/monlor/xiaoya-alist:latest # 使用的镜像，来源于 GitHub 容器注册表中的ghcr.io更改成其他镜像源，比如南京大学的镜像源image: ghcr.nju.edu.cn，更正后应该是这样的： image: ghcr.nju.edu.cn/monlor/xiaoya-alist:latest # 使用的镜像，来源于 GitHub 容器注册表 |  
| --- |  
 |  
|  

飞牛币
    37  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 2, 距离下一级还需 48 积分


|  _2025-3-30 11:30:57_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=50334)  
 |  有坑，需要把配置文件第三行 image: ghcr.io/monlor/xiaoya-alist:latest # 使用的镜像，来源于 GitHub 容器注册表中的ghcr.io改成ighcr.nju.edu.cn，不然无法拉取镜像 |  
| --- |  
 |  
|  

飞牛币
    12  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 2, 距离下一级还需 48 积分


|  _2025-3-30 23:07:22_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=51455)  
 |  现在这样了不知道哪里错了 开始生成配置文件... /start.sh: line 13: /data/docker_address.txt: Operation not permitted 有知道的大神帮帮忙  现在这样了不知道哪里错了 开始生成配置文件... /start.sh: line 13: /data/docker_address.txt: Operation not permitted 有知道的大神帮帮忙  |  
| --- |  
 |  
|  

飞牛币
    117  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 18, 距离下一级还需 32 积分


|  _2025-4-21 00:01:57_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=56665)  
 |  已成功,感谢  |  
| --- |  
 |  
|  

飞牛币
    6371  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 102, 距离下一级还需 98 积分


|  _2025-4-25 09:45:53_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=27790)  |  
|  

飞牛币
    6371  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 102, 距离下一级还需 98 积分


|  _2025-4-25 09:46:30_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=27790)  
 |  MARK 后续继续学习  |  
| --- |  
 |  
|  

飞牛币
    6371  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 102, 距离下一级还需 98 积分


|  _2025-4-25 09:47:02_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=9690&page=1&authorid=27790)  
 |  alist速度现在问题很大 感觉速度太慢了  |  
| --- |  
 |  
#### 社区上线纪念勋章
飞牛私有云社区上线，晒NAS活动纪念勋章
#### 社区共建团荣誉勋章
飞牛社区组织荣誉认证，为飞牛私有云社区发展无私奉献，发光发热
#### 飞牛百度网盘玩家
参与“极速下载，畅享特权”百度网盘活动纪念
#### fnOS1.0上线纪念勋章
飞牛fnOS 1.0 上线，晒体验活动纪念勋章
#### 灌水之星
别人逛社区，TA住在社区。 发帖如呼吸，互动如本能， 水得理直气壮，水得令人佩服
#### AMD适配纪念勋章
纪念2026年4月16日，飞牛fnOS率先适配AMD在系统编解码、杜比、AI环境，并正式开启OTA
#### 音乐上线纪念勋章
纪念公测两周年飞牛音乐正式上线
#### 音乐内测玩家
首批飞牛音乐内测玩家临时勋章
#### DIY极客玩家
[粤ICP备2023020469号](https://beian.miit.gov.cn/)
