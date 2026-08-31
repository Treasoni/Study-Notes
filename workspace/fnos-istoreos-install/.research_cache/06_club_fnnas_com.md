---
url: "https://club.fnnas.com/forum.php?mod=viewthread&tid=26481"
title: "飞牛虚拟机部署 iStoreOS 做个旁路由教程 - 虚拟机 飞牛私有云论坛 fnOS"
scraped_at: 2026-08-31T16:19:10+00:00
---

  * 用户名
  * Email


  * [论坛BBS](https://club.fnnas.com/forum.php "BBS")


请 后使用快捷导航没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register)
#  飞牛虚拟机部署 iStoreOS 做个旁路由教程
**23037** 查看   
|  

飞牛币
    10056  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-5-23 08:59:00_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=2158) |[倒序浏览](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&extra=&ordertype=1) [阅读模式](javascript:;)  
 | 
> 飞牛虚拟机版本重磅更新，本次升级带来了更强的镜像兼容能力与更完善的硬件支持。支持直接使用 img 镜像安装系统，新增 OVA镜像的导入导出功能，虚拟磁盘也支持导入 qcow2 等格式。远程桌面支持声音输出，同时显卡新增 virtio-gpu，Windows 11下可自由调整分辨率。除此之外，网络适配器新增 E1000E 类型，硬盘启动顺序也支持自定义，全面提升系统兼容性与使用便捷性。
这次飞牛虚拟机的更新带来了诸多实用功能，整体体验有了明显提升。借此机会，我也整理了一篇使用飞牛虚拟机部署 iStoreOS的图文教程，并附上了设置旁路由的基础配置步骤，适合新手快速上手。希望这篇内容能为有类似需求的朋友提供一些参考和帮助，让大家利用现有设备可以玩玩软路由功能。 **下载镜像** 1️⃣ 首先我们先去iStoreOS官网下载最新的镜像包img.gz格式，下载x86_64镜像 
```
https://fw.koolcenter.com/iStoreOS/
​
```
2️⃣ 将下载的 img.gz压缩包 上传到飞牛任意目录下，进行解压得到一个img后缀的镜像 **配置虚拟机** 1️⃣ 创建虚拟机 2️⃣选择刚刚解压的镜像，其他内容根据需求自行配置，也可以参考下图 3️⃣点击下一步，进行格式转换，耐心等待一会 4️⃣ 添加储存空间 选择好储存空间，第一个虚拟磁盘后面的2433 MB目前改不了，也删不了，我们先完成创建后面再回来改。 你还可以添加新的虚拟磁盘，最多8个 5️⃣ 添加网卡 多个网卡小主机可以添加多个，然后下一步 6️⃣ 硬件直通 根据自己的需求进行硬件直通，我用不到就直接下一步 完成创建 7️⃣修改空间大小 不要启动，编辑刚刚创建的iStoreOS虚拟机 点击磁盘，之前不能改的2433 MB就可以改了，根据自己的需求改，iStoreOS一般20G足够使用 **安装iStoreOS** 开机，通过NVC访问页面 然后等待自动安装镜像，等到如下图的地方敲回车 输入完整的 quickstart 回车，或者输入 qu 按tab键后自动补全（ quickstart ） 回车， 按键盘下键，选择Change LAN IP 敲回车，设置静态IP 配置静态IP：输入局域网没有被占用的IP回车，再输入子网掩码回车，就可以正常访问了。 浏览器输入刚刚设置的静态IP进行访问 默认账号root密码password **简单配置** 1️⃣ 设置旁路由 点击网络向导 点击 配置为旁路由 输入和前面一样的静态IP、子网掩码、网关地址，DNS服务器默认是阿里的，可以自己改一下，关闭DHCpv4服务，开启自动获取IPv6后面可以DDNS远程访问配置。保存配置 回到首页右上角就能看到设置的静态ip和获取到的ipv6公网地址了 2️⃣ 格式化剩余空间 默认 iStoreOS 系统根目录 只占用2G的空间，其他空间需要手动格式化后使用 点击如下图位置 三个点点 未分区，进行格式化 格式化之后分区是sda4（挂载点/mnt/vio2-4） 3️⃣ Docker目录迁移 点击快速配置 目录迁移到刚刚格式化的目录里面 到这里，基本设置就完成了 **结尾** 作为旁路由当然要配置一下上外网的环境、广告过滤等等功能，但是我写完之后发现其实高大全更合适里面有现成的插件，下次再发一篇关于高大全的吧，过程大致一样的，有兴趣的朋友研究玩玩，软路由我玩的也不多，教程有问题的地方还请指正！  |  
| --- |  
收藏 
送赞
[本主题由 管理团队 于 2026-1-22 20:00 加入精华](https://club.fnnas.com/forum.php?mod=misc&action=viewthreadmod&tid=26481 "帖子模式")
 |  
|  公众号:知新坊  |  
|  

飞牛币
    146  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 22, 距离下一级还需 28 积分


|  _2025-5-23 15:57:29_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=50808)  |  
|  

飞牛币
    592  

积分


主题
  
 |  
|  |  


|  _2025-5-23 16:00:26_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=52719)  
 |  非常好～ 飞牛虚拟机解决了用户的痛点啊。 另外顺便提个**ug， 我发现immortalwrt.img.gz 直接导入飞牛就没问题，能正确引导，但是iStoreOS.img.gz 直接导入飞牛，引导不了。就报错。所以貌似iStoreOS的gz压缩格式有点特殊。  |  
| --- |  
### 点评
immortalwrt.img.gz在哪下载 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=231572&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=231572&extra=&page=1)
2026-1-11 06:45 
我没有解压，直接用，没有问题 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=124786&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=124786&extra=&page=1)
2025-5-26 09:39 
 |  
|  悟空导航站 https://tvhelper.cpolar.cn  |  
|  

飞牛币
    299  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 9, 距离下一级还需 41 积分


|  _2025-5-23 21:47:46_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=8292)  
 |  这个固件有没有科学梯子的功能？  |  
| --- |  
### 点评
找Are-u-ok [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=207351&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=207351&extra=&page=1)
2025-11-26 17:34 
 |  
|  

飞牛币
    566  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 62, 距离下一级还需 138 积分


|  _2025-5-24 00:24:25_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=44991)  
 |  、、 大佬，我安装完成以后是这个样子的，有啥方法解决吗？  |  
| --- |  
### **本帖子中包含更多资源**
您需要 [登录](https://club.fnnas.com/member.php?mod=logging&action=login) 才可以下载或查看，没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register "注册账号")
x
 |  
|  

飞牛币
    10056  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-5-24 10:44:53_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=2158)  
 | 
> [gomovies 发表于 2025-5-23 21:47](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=124066&ptid=26481) 这个固件有没有科学梯子的功能？
is官方默认固件是没有的，需要自己下载的 |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    10056  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-5-24 10:47:07_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=2158)  
 | 
> [wukongdaily 发表于 2025-5-23 16:00](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=123925&ptid=26481) 非常好～ 飞牛虚拟机解决了用户的痛点啊。 另外顺便提个**ug， 我发现immortalwrt.img.gz 直接导入飞牛就没 ...
immortalwrt你是直接生成的固件嘛 |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    10056  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-5-24 10:50:27_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=2158)  
 | 
> [wang372110401 发表于 2025-5-24 00:24](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=124123&ptid=26481) 、、 大佬，我安装完成以后是这个样子的，有啥方法解决吗？
此界面输入 passwd 按照提示输入 ​新密码​ |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    5140  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-5-24 11:02:10_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=36234)  
 |  怎么让局域网设备上网走旁路由呢  |  
| --- |  
### 点评
需要上网的设备，改成手动IP，网关和dns都改成旁路由的ip地址就可以了 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=195359&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=195359&extra=&page=1)
2025-11-4 14:25 
 |  
|  

飞牛币
    685  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 7, 距离下一级还需 43 积分


|  _2025-5-24 22:34:06_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=36106)  
 |  现在可以直接使用img了，真好  |  
| --- |  
 |  
|  

飞牛币
    71  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2025-5-24 23:37:33_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=64163)  
 |  大佬你好，配置IP这步输入局域网没有被占用的IP，如何找到局域网没有被占用的ip，我试了设置你图片这个，连不上  |  
| --- |  
 |  
|  

飞牛币
    308  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 12, 距离下一级还需 38 积分


|  _2025-5-26 02:47:04_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=59265)  
 |  看小陈的博客 |  
| --- |  
### 点评
你的装好了 但是界面完全不一样 看懵了 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=126548&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=126548&extra=&page=1)
2025-5-29 14:51 
你的分享下载速度真的快 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=125288&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=125288&extra=&page=1)
2025-5-27 08:41 
 |  
|  

飞牛币
    10056  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-5-26 09:18:09_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=2158)  
 | 
> [源稚生 发表于 2025-5-24 23:37](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=124438&ptid=26481) 大佬你好，配置IP这步输入局域网没有被占用的IP，如何找到局域网没有被占用的ip，我试了设置你图片这个，连 ...
就简单的就是路由器后台看看，已经连接的设备用的IP，避开就行 |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    10056  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-5-26 09:18:49_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=2158)  
 | 
> [Jimboo7339 发表于 2025-5-24 11:02](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=124200&ptid=26481) 怎么让局域网设备上网走旁路由呢
连上wifi或者网线之后，手动设置代理，手机和电脑都是有的地方设置的，可以百度一下 |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    3172  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-5-26 09:39:25_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=7256)  
 | 
> [wukongdaily 发表于 2025-5-23 16:00](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=123925&ptid=26481) 非常好～ 飞牛虚拟机解决了用户的痛点啊。 另外顺便提个**ug， 我发现immortalwrt.img.gz 直接导入飞牛就没 ...
我没有解压，直接用，没有问题 |  
| --- |  
 |  
|  平台账号：科技智趣坊  |  
|  

飞牛币
    65  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 9, 距离下一级还需 41 积分


|  _2025-5-27 08:41:37_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=62195)  
 | 
> [Derive 发表于 2025-5-26 02:47](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=124741&ptid=26481) 这个有插件大家随意https://f.557667.xyz:2233/s/57735ebfbc4b40fcad，详细的安装教程看小陈 ...
你的分享下载速度真的快 |  
| --- |  
### 点评
2025-5-28 14:31 
 |  
|  

飞牛币
    308  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 12, 距离下一级还需 38 积分


|  _2025-5-28 14:31:34_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=59265)  
 | 
> [大地x 发表于 2025-5-27 08:41](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=125288&ptid=26481) 你的分享下载速度真的快
哈哈，一般般 |  
| --- |  
 |  
|  

飞牛币
    65  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 9, 距离下一级还需 41 积分


|  _2025-5-29 14:51:58_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=62195)  
 | 
> [Derive 发表于 2025-5-26 02:47](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=124741&ptid=26481) 这个有插件大家随意https://f.557667.xyz:2233/s/57735ebfbc4b40fcad，详细的安装教程看小陈 ...
你的装好了 但是界面完全不一样 看懵了 |  
| --- |  
### 点评
很简单啊，设置完ip后直接访问不就行啦，你看下小陈的视频 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=126945&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=126945&extra=&page=1)
2025-5-30 01:27 
 |  
|  

飞牛币
    308  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 12, 距离下一级还需 38 积分


|  _2025-5-30 01:27:22_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=59265)  
 | 
> [大地x 发表于 2025-5-29 14:51](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=126548&ptid=26481) 你的装好了 但是界面完全不一样 看懵了
很简单啊，设置完ip后直接访问不就行啦，你看下小陈的视频 |  
| --- |  
 |  
|  

飞牛币
    133  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 18, 距离下一级还需 32 积分


|  _2025-5-30 11:04:05_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=65262)  
 |  各位大佬，所有设置都正常，虚拟机里的系统也启动了，但点击 NVC 里面全是黑的无任何显示。 只能通过IP进入，有知道是怎么回事的吗。  |  
| --- |  
 |  
|  

飞牛币
    3885  

积分


主题
  
 |  回帖  |  
| --- |  


|  _2025-5-30 14:09:13_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=4042)  
 |  用虚拟机测试的，结果虚拟机开启ovs后重启就失联了哈哈...... |  
| --- |  
 |  
|  

飞牛币
    272  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2025-6-3 18:59:38_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=63915)  |  
|  

飞牛币
    41  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2025-6-11 16:07:01_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=52165)  
 |  真的非常感谢！  |  
| --- |  
 |  
|  

飞牛币
    95  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 54, 距离下一级还需 146 积分


|  _2025-6-30 21:24:51_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=8208)  
 |  第一次用飞牛虚拟机安装旁路由，非常感谢大神的指导。教程很详细很到位！  |  
| --- |  
 |  
|  

飞牛币
    74  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 5, 距离下一级还需 45 积分


|  _2025-7-9 10:10:03_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=37969)  
 |  为什么我按照教程设置完成之后，首页显示未联网呢？求大神指导一下。   |  
| --- |  
### **本帖子中包含更多资源**
您需要 [登录](https://club.fnnas.com/member.php?mod=logging&action=login) 才可以下载或查看，没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register "注册账号")
x
### 点评
没有wan口，不知道是没有直通网卡，还是只直通了一个网卡， [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=167450&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=167450&extra=&page=1)
2025-9-1 09:39 
 |  
|  

飞牛币
    4027  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 5, 距离下一级还需 45 积分


|  _2025-7-12 10:07:25_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=25114)  
 |  输入IP后卡在登入界面了 请问怎么解决  |  
| --- |  
 |  
|  

飞牛币
    182  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 11, 距离下一级还需 39 积分


|  _2025-7-13 02:06:29_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=22450)  
 |  输入ip之后无法访问怎么解决？我输入的是自己局域网的ip。而且每次重启都会自己恢复到192.168.100.1，完全不可用啊  |  
| --- |  
 |  
|  

飞牛币
    57  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 2, 距离下一级还需 48 积分


|  _2025-7-29 18:29:58_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=72782)  |  
|  

飞牛币
    182  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 11, 距离下一级还需 39 积分


|  _2025-7-31 07:07:26_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=22450)  
 |  istore每次重启就重置  |  
| --- |  
 |  
|  

飞牛币
    10056  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-8-3 13:07:56_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=2158)  
 | 
> [十三只兔子 发表于 2025-7-31 07:07](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=153221&ptid=26481) istore每次重启就重置
这个没有遇到过，不太清楚什么情况 |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    10056  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-8-3 13:08:16_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=2158)  
 | 
> [佳Lollop 发表于 2025-7-29 18:29](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=152642&ptid=26481) 安装失败
什么原因失败的，报错提示是什么 |  
| --- |  
 |  
|  公众号:知新坊  |  
|  

飞牛币
    151  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 21, 距离下一级还需 29 积分


|  _2025-9-1 09:39:02_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=56783)  
 | 
> [孙梓铭_AiV11 发表于 2025-7-9 10:10](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=144781&ptid=26481) 为什么我按照教程设置完成之后，首页显示未联网呢？求大神指导一下。
没有wan口，不知道是没有直通网卡，还是只直通了一个网卡， |  
| --- |  
 |  
|  

飞牛币
    49  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 2, 距离下一级还需 48 积分


|  _2025-9-1 15:50:41_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=81831)  
 |  这两个一个是istore的IP，一个是我的电脑IP，设置后进入不到网页，请问大佬应该怎么设置IP地址  |  
| --- |  
### **本帖子中包含更多资源**
您需要 [登录](https://club.fnnas.com/member.php?mod=logging&action=login) 才可以下载或查看，没有账号？[立即注册](https://club.fnnas.com/member.php?mod=register "注册账号")
x
 |  
|  

飞牛币
    306  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 83, 距离下一级还需 117 积分


|  _2025-9-2 16:34:12_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=33064)  
 |  请教一下安装这个旁路由的作用有哪些？ |  
| --- |  
 |  
|  

飞牛币
    10056  

积分


主题
  
 |  主题  |  回帖  |  牛值  |  
| --- | --- | --- |  


|  _2025-9-2 19:46:46_ _楼主_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=2158)  
 | 
> [Momo_w6g6a 发表于 2025-9-2 16:34](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=168185&ptid=26481) 请教一下安装这个旁路由的作用有哪些？
挂个梯子玩玩 |  
| --- |  
### 点评
你的公众号有关注 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=172721&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=172721&extra=&page=1)
2025-9-12 10:28 
 |  
|  公众号:知新坊  |  
|  

飞牛币
    26  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2025-9-6 22:38:47_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=82785)  
 |  就等你更新完整教程 |  
| --- |  
 |  
|  

飞牛币
    3263  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 10, 距离下一级还需 40 积分


|  _2025-9-7 11:26:44_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=81506)  
 |  有没有老师能科普下软路由比较牛的作用 谢谢  |  
| --- |  
 |  
|  

飞牛币
    306  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 83, 距离下一级还需 117 积分


|  _2025-9-12 10:28:03_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=33064)  
 | 
> 挂个梯子玩玩
你的公众号有关注 |  
| --- |  
 |  
|  

飞牛币
    5607  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 16, 距离下一级还需 34 积分


|  _2025-9-13 13:38:13_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=63207)  
 |  挂个梯子玩玩  |  
| --- |  
 |  
|  

飞牛币
    238  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 77, 距离下一级还需 123 积分


|  _2025-10-29 14:09:51_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=76233)  
 |  遇到2个问题：
  1. 输入原始192.168.100.1 没办法访问ISTORE界面

2.改LAN IP 192.168.31.250 它自己又会改回192.168.100.1 不知道怎么回事 麻烦您回复下 谢谢  |  
| --- |  
 |  
|  

飞牛币
    233  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 11, 距离下一级还需 39 积分


|  _2025-11-4 14:25:54_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=84539)  
 | 
> [Jimboo7339 发表于 2025-5-24 11:02](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=124200&ptid=26481) 怎么让局域网设备上网走旁路由呢
需要上网的设备，改成手动IP，网关和dns都改成旁路由的ip地址就可以了 |  
| --- |  
### 点评
有办法自动吗，连上的设备自动变成这样 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=280493&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=280493&extra=&page=1)
2026-4-15 22:22 
 |  
|  

飞牛币
    6  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2025-11-26 17:34:15_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=101136)  
 | 
> [gomovies 发表于 2025-5-23 21:47](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=124066&ptid=26481) 这个固件有没有科学梯子的功能？
找Are-u-ok |  
| --- |  
 |  
|  

飞牛币
    80  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 19, 距离下一级还需 31 积分


|  _2025-11-27 17:58:08_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=95973)  
 |  好，谢谢分享 |  
| --- |  
 |  
|  

飞牛币
    283  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 3, 距离下一级还需 47 积分


|  _2026-1-11 06:45:07_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=30401)  
 | 
> [wukongdaily 发表于 2025-5-23 16:00](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=123925&ptid=26481) 非常好～ 飞牛虚拟机解决了用户的痛点啊。 另外顺便提个**ug， 我发现immortalwrt.img.gz 直接导入飞牛就没 ...
immortalwrt.img.gz在哪下载 |  
| --- |  
 |  
|  

飞牛币
    283  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 3, 距离下一级还需 47 积分


|  _2026-1-11 22:56:19_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=30401)  
 |  dhcp不起作用，是虚拟机的问题吗  |  
| --- |  
 |  
|  

飞牛币
    392  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 71, 距离下一级还需 129 积分


|  _2026-1-19 20:58:35_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=88160)  
 |  大佬，我按照教程用虚拟机安装了istoreos，并设置了旁路由模式，但是本级地址也手动设置了IP、网关、DNS，设置后，可以连上飞牛，也能连上istoreos，但是就是不能上网，请问是为什么？ |  
| --- |  
 |  
|  

飞牛币
    1191  

积分


主题
  
 |  
|  |  
初出茅庐, 积分 71, 距离下一级还需 129 积分


|  _2026-4-15 22:22:55_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=47408)  
 | 
> [zhy770416 发表于 2025-11-4 14:25](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=195359&ptid=26481) 需要上网的设备，改成手动IP，网关和dns都改成旁路由的ip地址就可以了
有办法自动吗，连上的设备自动变成旁路由 |  
| --- |  
 |  
|  

飞牛币
    1846  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 7, 距离下一级还需 43 积分


|  _2026-6-26 15:02:24_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=104479)  
 |  若遇到系统显示英文，没有中文选项，怎么修复？在终端执行下列命令 uci set luci.languages.zh_cn='中文 (Chinese)'; uci set luci.main.lang='zh_cn'; uci commit luci |  
| --- |  
 |  
|  

飞牛币
    11  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 1, 距离下一级还需 49 积分


|  _2026-6-29 10:53:34_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=164973)  
 |  需要多网口机器才行吗  |  
| --- |  
### 点评
多网口，一网口应该都可以。只要其它设备的网关和dns指向 这个旁路由的ip就可以了。 [详情](https://club.fnnas.com/forum.php?mod=redirect&goto=findpost&pid=312195&ptid=26481) [回复](https://club.fnnas.com/forum.php?mod=post&action=reply&fid=28&tid=26481&repquote=312195&extra=&page=1)
2026-7-16 10:44 
 |  
|  

飞牛币
    147  

积分


主题
  
 |  
|  |  
江湖小虾, 积分 20, 距离下一级还需 30 积分


|  _2026-7-16 10:44:51_ [只看该作者](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481&page=1&authorid=31787)  
 | 
> 需要多网口机器才行吗
多网口，一网口应该都可以。只要其它设备的网关和dns指向 这个旁路由的ip就可以了。 |  
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
