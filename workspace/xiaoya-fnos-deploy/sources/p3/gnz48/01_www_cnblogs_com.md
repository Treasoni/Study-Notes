---
url: "https://www.cnblogs.com/gnz48/p/18651934"
title: "群晖docker部署小雅全家桶及全部资源挂载到emby教程 - 很多无尾熊 - 博客园"
scraped_at: 2026-10-05T16:38:13+00:00
---



随笔 - 877  文章 - 6  评论 - 18  阅读 -  76万
#  [ 群晖docker部署小雅全家桶及全部资源挂载到emby教程 ](https://www.cnblogs.com/gnz48/p/18651934 "发布于 2025-01-04 15:23")
# 群晖docker部署小雅全家桶及全部资源挂载到emby教程
  * 2023-12-13 10:12


**群晖docker部署小雅全家桶及全部资源挂载到emby教程**
_群晖安装小雅全家桶大致三步，_
_1、部署小雅alist容器_
_2、拉取小雅网盘元数据（此步骤耗时很长2-4小时不等，合计拉取数据大小为60G+，取决你的网速）_
_3、部署docker版的emby，如已经安装了emby，这里有一下2种情况。_
_1.1：如已经安装了dokcer版的emby，请修改端口号，不要占用8096。_
_1.2：如已经安装了套件版的emby，ssh工具在最后会给你自动安装的emby容器，随后把新部署的docker emby删除，并重建一个新容器，并在重建的时候修改端口号，以防8096端口冲突造成容器无限重启。_
**下面正式进入教程：**
一、docker部署小雅alist容器。
**1、在群晖docker文件夹下新建文件夹xiaoya。**
**2、获取你的阿里云mytoken.txt、myopentoken.txt、temp_transfer_folder_id.txt**
①Mytoken获取链接：<https://media.cooluc.com/decode_token/> 点击顶部“进入移动端网页登录入口
在打开的网页按“F12 ”打开浏览器开发者工具。
在右边的开发者工具栏里，有一个“login.do?appName=aliyun”链接的选项，鼠标右键选择“复制--复制响应”
然后回到网页端，粘贴上步骤的“复制响应”数据到输入框，点击“解码Refresh Token”，在页面的上方就会弹出我们需要的手机端阿里云盘 Token（32位长）.
②myopentoken 获取链接：<https://alist.nn.ci/tool/aliyundrive/request.html> ，点击“Go to login”，然后直接用自己的阿里云盘手机端APP扫码登录。然后在下一个网页方框就能得到需要需要的网页端阿里云盘Open Token（280位长）。
③temp_transfer_folder_id获取需要登陆阿里云盘，[https://www.aliyundrive.com/drive，在资源盘下新建文件夹（xiaoya）,点击进入后复制阿里云盘转存目录folder](https://www.aliyundrive.com/drive%EF%BC%8C%E5%9C%A8%E8%B5%84%E6%BA%90%E7%9B%98%E4%B8%8B%E6%96%B0%E5%BB%BA%E6%96%87%E4%BB%B6%E5%A4%B9%EF%BC%88xiaoya%EF%BC%89,%E7%82%B9%E5%87%BB%E8%BF%9B%E5%85%A5%E5%90%8E%E5%A4%8D%E5%88%B6%E9%98%BF%E9%87%8C%E4%BA%91%E7%9B%98%E8%BD%AC%E5%AD%98%E7%9B%AE%E5%BD%95folder) id，用于转存xiaoya网盘资源至自己网盘.
**2、在桌面新建TXT文本，将以上获取的key分别填入新建文本mytoken.txt、myopentoken.txt、temp_transfer_folder_id.txt，上传至群晖docker/xiaoya文件夹中。**
**3、使用** ssh软件**登陆群晖，再用sudo -i，登陆root账号使用以下命令。**
> javascript  
```
  
> 

| docker run -d --restart=always --name="xiaoya" -p 5678:80 -p 2345:2345 -p 2346:2346 -v /volume1/docker/xiaoya:/data xiaoyaliu/alist:latest

 |  
> | --- |  
> 
```

**4、在群晖docker下启动xiaoya容器, 浏览器打开：** 【http:// 群晖的局域网IP:5678】,需等5分钟刷新浏览器验证是否挂载成功。刚开始页面会显示“获取设置失败”，这是正常情况“，这是因为小雅Alist加载需要一些时间。首次访问时，由于小雅需要进行索引，启动时间会比较慢，根据网络情况，需要1-5分钟不等。
5、自动清除阿里云盘缓存
使用小雅时，会先将视频缓存在自己的阿里云盘中。时间一长可能会占满整个云盘空间，导致无法使用。我们可以定期手动清空缓存文件夹，这里小雅为我们提供了一个自动删除缓存的方法，只需要一行代码。同样使用SSH工具连接端口后，输入以下命令：
javascript  
```
  


| bash -c "$(curl -s https://xiaoyahelper.zengge99.eu.org/aliyun_clear.sh| tail -n +2)" -s 3
 |  
| --- |  

```

二、挂载小雅emby全家桶。
1、在/volume1/docker/xiaoya文件夹下新建两个文本文档。
1.1：docker_address.txt，填写http://群晖ip地址:5678 .
1.2：emby_server.txt，填写 http://群晖ip地址:8096 .
_【此处注意：】_
_如果已装有docker版emby的，请将原emby端口8096改成其他。_
_如果已装有套件版的emby，请填写其他端口号，不能用8096。_
_如果没有装过emby套件或者docker版的，请忽略。_
2、在/volume1/docker/xiaoya下新建文件夹media文件夹。
3、登陆本地小雅网盘，http://群晖ip地址:5678，任意打开一个mp4视频，验证是否正常播放。
使用ssh登陆群晖sudo -i登陆root账号使用以下命令。【二选一】
部署命令：
1.使用emby官方容器命令（无法调用核显硬解）
> javascript  
```
  
> 

| bash -c "$(curl http://docker.xiaoya.pro/emby_plus.sh)" -s /volume1/docker/xiaoya/media /volume1/docker/xiaoya
 |  
> | --- |  
> 
```

2.使用第三方emby容器命令，（可以调用核显硬解）
> javascript  
```
  
> 

| bash -c "$(curl http://docker.xiaoya.pro/emby_plus.sh | sed 's#emby/embyserver#amilys/embyserver#')" -s /volume1/docker/xiaoya/media /volume1/docker/xiaoya
 |  
> | --- |  
> 
```

此时已经开始下载元数据，大概数据有60G+，所以请给docker准备150G+的空间，这里忘记截图了。
下载缓存时间较长，需要1~2小时甚至更长（本人从拉取元数据到安装完成大概耗时5小时+），根据网络和NAS性能，完成后会有提示请耐心等待，完成后重启xiaoya容器。
这里下载完成后，会自动开始解压下载的元数据，解压时间为半小时左右，此时会显示：
这里的端口号可能不对，这里请往上看第二步第一点，
你的端口号是你自己设置的端口号。如果你没装过emby，你的端口号可以用8096或者2345登录。
随后会自动开始安装emby容器。
这里安装完成后，进群晖查看你的容器。
如果你的容器自动重启，请删掉容器并重建。emby映像已下载好，直接双击重新部署即可，部署过程中请勾选自动重新启动。
这里修改端口号，把本地端口修改成为emby_server.txt里面填入的端口号，以防和已装好的emby8096端口冲突。
储存空间和装载路径同上，可以照抄上面的。
部署完成后，网页打开【http:// 群晖的局域网IP:你设置的端口号】，登录账号：xiaoya ，密码：1234 。
比如我这里就是【http:// 群晖的局域网IP:8921】，随后就尽情看片吧，速度杠杠的。
因我戴尔服务器没有核显，无法硬解，所以网页播放是不行的，会显示没有兼容的流。
所以建议大家直接用infuse、emby客户端，或者支持emby传输协议的软件：如Fileball、Vidhub等软件播放。
**小雅官网地址 ：**[http://alist.xiaoya.pro ](http://alist.xiaoya.pro/)更多详细可进小雅官网查阅。
本文作者：很多无尾熊
本文链接：https://www.cnblogs.com/gnz48/p/18651934
版权声明：本作品采用知识共享署名-非商业性使用-禁止演绎 2.5 中国大陆[许可协议](https://www.cnblogs.com/gnz48/p/18651934)进行许可。
免责声明：本内容来自平台创作者，博客园系信息发布平台，仅提供信息存储空间服务。 
[很多无尾熊](https://home.cnblogs.com/u/gnz48/) [粉丝 - 27](https://home.cnblogs.com/u/gnz48/followers/) [关注 - 0](https://home.cnblogs.com/u/gnz48/followees/)
[« ](https://www.cnblogs.com/gnz48/p/18651929) 上一篇： [Linux如何解压gz、tar.gz、zip、tar、tar.bz2等压缩文件](https://www.cnblogs.com/gnz48/p/18651929 "发布于 2025-01-04 15:20") [» ](https://www.cnblogs.com/gnz48/p/18651942) 下一篇： [无人值守24小时直播！Docker、群晖NAS配置](https://www.cnblogs.com/gnz48/p/18651942 "发布于 2025-01-04 15:28")
posted @ 2025-01-04 15:23 [很多无尾熊](https://www.cnblogs.com/gnz48) 阅读(7153) 评论(0) [收藏](javascript:void\(0\)) [举报](https://report.cnblogs.com?targetLink=https%3A%2F%2Fwww.cnblogs.com%2Fgnz48%2Fp%2F18651934&targetId=18651934&targetType=0)
登录后才能查看或发表评论，立即 [登录](javascript:void\(0\);) 或者 [逛逛](https://www.cnblogs.com/) 博客园首页 
[【推荐】实时动态可视化（HMI,SCADA,DCS,仿真,CAD) C++源码库！](http://www.uccpsoft.com/index.htm)[【推荐】博客园团队诚聘 .NET+Angular 全栈开发工程师，杭州20-30K](https://www.cnblogs.com/cmt/p/22888277)[【推荐】科研领域的连接者艾思科蓝，一站式科研学术服务数字化平台](https://ais.cn/u/QjqYJr)
  * 2023-01-04 [安卓tv YouTube客户端https://smartyoutubetv.github.io/](https://www.cnblogs.com/gnz48/p/17024957.html)
  * 2023-01-04 [chrom插件代理下载](https://www.cnblogs.com/gnz48/p/17024235.html)


### 公告
昵称： [ 很多无尾熊 ](https://home.cnblogs.com/u/gnz48/) 园龄： [ 4年8个月 ](https://home.cnblogs.com/u/gnz48/ "入园时间：2022-01-18") 粉丝： 关注： 
打赏二维码  
|   
 | 2026年10月  |  
| --- |  
 |  
| 日  | 一  | 二  | 三  | 四  | 五  | 六  |  
| 27  | 28  | 29  | 30  |  
 |  
 |  
 |  
 |  
 |  
###  常用链接 


###  随笔档案 


###  文章档案 


  * [ 1. 解决Android/安卓原生ROM出现网络连接受限（Limited connection），网络无法链接的问题(30905) ](https://www.cnblogs.com/gnz48/p/16433726.html)
  * [ 2. Linux如何解压gz、tar.gz、zip、tar、tar.bz2等压缩文件(22326) ](https://www.cnblogs.com/gnz48/p/18651929)
  * [ 3. OpenWrt固件_官方下载_官方自己编译定制软件包(14941) ](https://www.cnblogs.com/gnz48/p/17007914.html)
  * [ 5. 在新版 Edge 浏览器启用 B 站 HEVC、HDR、8K(14129) ](https://www.cnblogs.com/gnz48/p/16266339.html)


  * [ 2. 小米 EU ROM 无需 root 还原钱包服务(2) ](https://www.cnblogs.com/gnz48/p/17139893.html)
  * [ 3. 无需越狱，第三方微信多开聊天记录恢复教程(2) ](https://www.cnblogs.com/gnz48/p/16820946.html)
  * [ 4. 10代cpu及以上可以装的win7系统(2) ](https://www.cnblogs.com/gnz48/p/16222960.html)


  * [ 2. 2024年最新国内可用的Docker镜像加速器地址汇总(1) ](https://www.cnblogs.com/gnz48/p/18634154)
  * [ 3. 关于手机24小时插电鼓包问题，安卓电池充电保护-智能充电/温控切断（Root方案）(1) ](https://www.cnblogs.com/gnz48/p/16968740.html)


  * [Office Tool Plus[otp]](https://otp.landian.vip/zh-cn/)
  * [mirror GitHub Proxy](https://mirror.ghproxy.com/)
  * [library Mirror List](https://www.library.ac.cn/)


Copyright © 2026  Powered by you 🌊 Theme in [acnb](https://www.cnblogs.com/gnz48/p/18651934)
本站已运行[1669 天 0 时 38 分 13 秒 ] 
欢迎光临本站，您是第1位访问者！ 
赤壁矶头千古浪，铜鞮陌上三更月。
点击右上角即可分享
  1. 1 所念皆星河 房东的猫
  2. 2 所念皆星河 CMJ
  3. 3 热河 南京市民
  4. 4 起风了2018夏 卖辣椒也用券
  5. 5 纸短情长2018夏 烟把儿乐队
  6. 6 关于郑州的记忆 南京市民
  7. 7 定西 南京市民
  8. 8 化作樱花树 SNH48
  9. 9 化青春的约定 SNH48
  10. 10 BINGO! SNH48
  11. 11 恋爱捉迷藏 (2016 Bravery·挑战B50特殊联合公演现场) GNZ48
  12. 12 365天的纸飞机 AKB48 Team SH
  13. 13 《瞬间的永恒》夜色钢琴曲 赵海洋
  14. 14 卡农 我的野蛮女友
  15. 15 爱有天意ost 未知
  16. 16 野蛮女友ost 未知
  17. 17 野蛮女友ost 未知
  18. 18 野蛮女友ost 未知
  19. 19 野蛮女友ost 未知
  20. 20 野蛮女友ost 未知
  21. 21 我想念你...自*管的悲伤 未知
  22. 22 在人间 未知
  23. 23 野蛮女友ost 未知
  24. 24 野蛮女友ost 未知
  25. 25 風になる つじあやの
  26. 26 潮鳴り 折戸伸治
  27. 27 青石巷 魏琮霏
  28. 28 坐在巷口的那对男女 自然卷
  29. 29 优美的小调(钢琴曲) 张宇桦
  30. 30 天之痕(钢琴版) 群星
  31. 31 花がとぶ飛ぶ 邱有句,李德奎
  32. 32 挺你 IDOL SCHOOL
  33. 33 Eternity 李墨染
  34. 34 北京东路的日子 汪源,刘千楚,徐逸昊,鲁天舒,姜玮珉,胡梦原,张鎏依,梁竞元,游彧涵,金书援,许一璇,张夙西
  35. 35 初恋サイダー Buono!
  36. 36 花朝可期——A-SOUL原创应援曲 林小暗
  37. 37 花之祭 SNH48
  38. 38 ハートサングラス 26時のマスカレイド
  39. 39 47の素敵な街へ(チーム8) AKB48
  40. 40 优美的小调(钢琴曲) 张宇桦
  41. 41 风のように S.E.N.S.
  42. 42 秋～華恋～ α·Pav
  43. 43 同窗 同窗
  44. 44 远方 同窗
  45. 45 流着泪微笑 (合唱版) 鞠婧祎,徐晨辰
  46. 46 初恋蝴蝶 中泰
  47. 47 初恋蝴蝶 jxl


所念皆星河 - 房东的猫
00:00 / 00:00
作词 : 镜千
作曲 : CMJ
编曲 : 关天天
制作人 : 关天天
你眨了下眼睛
像夜空 闪烁的恒星
为我所有不安
找到了 指引
我呢喃了一句
晚风里 出走的心绪
为你每次试探
捎去了 回应
所念皆星河 辗转里反侧
你占领每个 永恒的片刻
无垠的宇宙 浩瀚的选择
你是最亮那颗
所爱如月色 触手而不得
将温柔的梦 都投射
你眼里有我 对这世间的
吝啬
你返航的轨迹
是所有 等待的意义
绕过多少周期
从未曾 离心
多遥远的距离
都不抵 内心的亲密
周旋每段关系
认出你 身影
所念皆星河 辗转里反侧
你占领每个 永恒的片刻
无垠的宇宙 浩瀚的选择
你是最亮那颗
所爱如月色 触手而不得
将温柔的梦 都投射
你眼里有我 对这世间的
吝啬
所念皆星河 辗转里反侧
你占领每个 永恒的片刻
无垠的宇宙 浩瀚的选择
你是最亮那颗
所爱如月色 触手而不得
将温柔的梦 都投射
你眼里有我 对这世间的
吝啬
茫茫的星河 终点是你的
身侧
总策划 : 唐晶晶、凌联兴
监制 : 姚政、纤橙
统筹 : 陈莹、小粉
企划 : 潘俊、黄鲲、袁晓童
文案 : 黄果璇、镜千
封面 : 高霄帆
吉他 : 关天天
混音 : 刘城函
和声 : 少年佩
伴唱 : 沙栩帆
弦乐 : 国际首席爱乐乐团
制作统筹 : OneCandy
