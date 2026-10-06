---
url: "https://www.cnblogs.com/z-addone/p/18823480"
title: "安装小雅Alist - Z_AddOne - 博客园"
scraped_at: 2026-10-05T16:38:09+00:00
---

#  [z-addone](https://www.cnblogs.com/z-addone)


随笔 - 20  文章 - 0  评论 - 3  阅读 -  10679
#  [ 安装小雅Alist ](https://www.cnblogs.com/z-addone/p/18823480 "发布于 2025-04-13 17:48")
注意：安装小雅Alist之前需要先安装Alist。
Alist可以在宝塔面板的docker界面一键安装
**已有新的安装方式，请参考** ：[一键安装小雅Alist - Z_AddOne - 博客园](https://www.cnblogs.com/z-addone/p/19084746)
# 安装小雅
在宝塔面板-->Docker-->线上镜像，搜索 _xiaoyaliu_ ，拉取
安装完之后，即可看到
# 配置小雅
## 任务目标
我们需要获得有关阿里云盘的三条数据，并将其放入小雅对应的文件夹里  
| 内容  | 对应文件名  | 获取方式  |  
| --- | --- | --- |  
| tocken  | mytoken.txt  | [阿里云盘 / 分享 | AList文档](https://alist.nn.ci/zh/guide/drivers/aliyundrive.html)  |  
| refresh_token  | myopentoken.txt  | [阿里云盘 Open | AList文档](https://alist.nn.ci/zh/guide/drivers/aliyundrive_open.html)  |  
| 转存目录的 folder id  | temp_transfer_folder_id.txt  | 先转存这个[阿里云盘分享](https://www.aliyundrive.com/s/rP9gP3h9asE)到自己网盘。然后参考[阿里云盘 / 分享 | AList文档](https://alist.nn.ci/zh/guide/drivers/aliyundrive.html#%E5%88%B7%E6%96%B0%E4%BB%A4%E7%89%8C)获得自己的folder id  |  
[bilibili 小雅alist三大token获取方式](https://www.bilibili.com/opus/1083749639002259525)
## 文件配置
将得到的数据存储到对应的txt文件内，之后打开小雅容器对应目录，创建 _data_ 文件夹，将三个txt文件放入
创建 _data_ 文件夹
将三个文件传入，其余文件在容器运行后会自动生成
至此，小雅基本已经完成配置，启动容器，查看日志是否成功启动
## 定时清理小雅缓存文件
由于小雅本质是将别人阿里云盘的文件先转存到自己的阿里云盘内再进行播放，如此当时间久了就会是云盘空间不足，我们可以手动清理，当然也可以使用插件，进行自动清理
搜索 _xiaoyakeeper_ 拉取镜像，等待安装完成即可
# 本地访问小雅
## 准备配置信息

```
  
小雅的ip地址：192.168.28.38:5678  （例子）

协议：WebDAV协议

账户：guest

密码：guest_Api789

```

## 电脑Potpalyer访问
打开PotPlayer播放器，点击“新建专辑”
最后，点击确定。
## 手机ES文件浏览器访问
参考资料：
  * [如何低成本搭建一个docker 轻服务器 随时随地访问小雅影音库 OrangePi Zero3 ｜免费内网穿透 bilibili](https://www.bilibili.com/video/BV1ND421T7nB/?spm_id_from=333.1387.favlist.content.click&vd_source=e88731727a722c629c5950e91da85296)
  * [用Docker单独安装xiaoya-alist_docker 小雅-CSDN博客](https://blog.csdn.net/wbsu2004/article/details/138304477)
  * [如何设置xiaoya的docker](https://xiaoyaliu.notion.site/xiaoya-docker-69404af849504fa5bcf9f2dd5ecaa75f)（小雅官方文档，可能需要加速访问）
  * [Home | AList文档](https://alist.nn.ci/zh/)（Alist官方文档）


__EOF__
* **本文作者：** [z-addone](https://www.cnblogs.com/z-addone)
* **本文链接：** <https://www.cnblogs.com/z-addone/p/18823480>
* **关于博主：** 评论和私信会在第一时间回复。或者[直接私信](https://msg.cnblogs.com/msg/send/z-addone)我。 
* **版权声明：** 除特殊说明外，转载请注明出处～[知识共享署名-相同方式共享 4.0 国际许可协议] 
* **声援博主：** 如果您觉得文章对您有帮助，可以点击文章右下角****一下。
免责声明：本内容来自平台创作者，博客园系信息发布平台，仅提供信息存储空间服务。 
[Z_AddOne](https://home.cnblogs.com/u/z-addone/) [粉丝 - 2](https://home.cnblogs.com/u/z-addone/followers/) [关注 - 0](https://home.cnblogs.com/u/z-addone/followees/)
[« ](https://www.cnblogs.com/z-addone/p/18823479) 上一篇： [搭建个人博客网站](https://www.cnblogs.com/z-addone/p/18823479 "发布于 2025-04-13 17:45") [» ](https://www.cnblogs.com/z-addone/p/18857773) 下一篇： [ClawCloud服务器+WordPress个人博客+Argon主题美化](https://www.cnblogs.com/z-addone/p/18857773 "发布于 2025-05-02 20:32")
posted @ 2025-04-13 17:48 [Z_AddOne](https://www.cnblogs.com/z-addone) 阅读(3146) 评论(0) [收藏](javascript:void\(0\)) [举报](https://report.cnblogs.com?targetLink=https%3A%2F%2Fwww.cnblogs.com%2Fz-addone%2Fp%2F18823480&targetId=18823480&targetType=0)
登录后才能查看或发表评论，立即 [登录](javascript:void\(0\);) 或者 [逛逛](https://www.cnblogs.com/) 博客园首页 
[【推荐】实时动态可视化（HMI,SCADA,DCS,仿真,CAD) C++源码库！](http://www.uccpsoft.com/index.htm)[【推荐】博客园团队诚聘 .NET+Angular 全栈开发工程师，杭州20-30K](https://www.cnblogs.com/cmt/p/22888277)[【推荐】科研领域的连接者艾思科蓝，一站式科研学术服务数字化平台](https://ais.cn/u/QjqYJr)
  * [你把时间放在哪里，哪里就会生长 | 一个互联网人的时间配置法](https://www.cnblogs.com/yuyisi/p/23139319)
  * [一切都会回潮-写在一个职业周期的低处](https://www.cnblogs.com/yuyisi/p/23058239)
  * [开源：基于.Net开发的数据库自治诊断平台——DBPilot ](https://www.cnblogs.com/skychen1218/p/22961976)
  * [Memory 记忆设计讨论：Agent Memory 到底应该是什么？](https://www.cnblogs.com/duwenlong/p/22879534)
  * [AI 越来越强，打工人怎么反而越来越累了？](https://www.cnblogs.com/HaiJun-Aion/p/22870343)


[ Scroll Down ](javascript:void\(0\);)




Created with Snap
MENU
### 公告
文章目录 
访问主页 
Alipay
WeChat
qrCode
点击开启 
返回顶部 
昵称： [ Z_AddOne ](https://home.cnblogs.com/u/z-addone/) 园龄： [ 6年2个月 ](https://home.cnblogs.com/u/z-addone/ "入园时间：2020-07-27") 粉丝： 关注： 
  * [树莓派(6)](https://www.cnblogs.com/z-addone/tag/%E6%A0%91%E8%8E%93%E6%B4%BE/)
  * [宝塔(5)](https://www.cnblogs.com/z-addone/tag/%E5%AE%9D%E5%A1%94/)
  * [docker(3)](https://www.cnblogs.com/z-addone/tag/docker/)
  * [服务器(2)](https://www.cnblogs.com/z-addone/tag/%E6%9C%8D%E5%8A%A1%E5%99%A8/)
  * [vue(1)](https://www.cnblogs.com/z-addone/tag/vue/)
  * [springboot(1)](https://www.cnblogs.com/z-addone/tag/springboot/)
  * [Linux(1)](https://www.cnblogs.com/z-addone/tag/Linux/)
  * [校园网(1)](https://www.cnblogs.com/z-addone/tag/%E6%A0%A1%E5%9B%AD%E7%BD%91/)
  * [博客(1)](https://www.cnblogs.com/z-addone/tag/%E5%8D%9A%E5%AE%A2/)




[ ##textLeft## ##textRight## ] 
ღゝ◡╹)ノ♡
##linksHtml##
##cnzzHtml## 
博客园 © 2004-2026 浙公网安备 33010602011771号 浙ICP备2021040463号-3 
点击右上角即可分享
