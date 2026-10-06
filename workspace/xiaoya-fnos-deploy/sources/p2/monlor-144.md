---
url: "https://www.monlor.com/archives/144/"
title: "小雅影视库一键部署项目，私人影视库的最佳选择 - Monlor's Blog"
scraped_at: 2026-10-05T16:22:19+00:00
---



  1. 正文 


###  小雅全家桶部署
📚 项目地址：**<https://github.com/monlor/docker-xiaoya>**
💡使用 Docker Compose 以更优雅的方式来部署小雅服务，支持一键部署 Alist + Emby + Jellyfin，全平台支持，Linux/Windows/Mac/群晖，X86/Arm架构
###  功能特性
🚀 使用 Docker Compose 一键部署服务，兼容群晖，Linux，Windows，Mac，包含所有X86和Arm架构
✨ 部署alist+下载元数据+部署emby/jellyfin服务全流程自动，无需人工干预
🔹 **Docker集成** ：所有脚本集成到Docker镜像中，避免了系统环境污染。
🔹 **镜像合并** ：合并了jellyfin和emby的x86和arm镜像，部署时无需区分镜像名。
🔹 **自动化脚本** ：集成云盘清理脚本到alist服务，无需单独部署。
🔹 **环境配置简化** ：通过环境变量配置阿里云盘token，无需映射文件。
🔹 **依赖检查自动化** ：jellyfin和emby启动时自动进行依赖检查，等待元数据下载完成后自动添加hosts。
🔹 **设备兼容性** ：完全兼容所有能运行docker的x86和arm设备。
🔹 **自动清理与同步** ：支持自动清理阿里云盘，自动同步小雅元数据。
🔹 **自动更新地址** ：自动更新内部的alist，emby，jellyfin访问地址，无需手动配置。
🔹 **元数据服务更新** ：通过metadata服务自动更新emby配置和元数据。
###  一键部署
####  部署或更新脚本
> 脚本支持重复执行

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/monlor/docker-xiaoya/main/install.sh)"

```

使用加速源（我的加速源也可能帮你减速🤣）

```
export GH_PROXY=https://gh.monlor.com/ IMAGE_PROXY=ghcr.monlor.com && bash -c "$(curl -fsSL ${GH_PROXY}https://raw.githubusercontent.com/monlor/docker-xiaoya/main/install.sh)"

```

####  卸载脚本

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/monlor/docker-xiaoya/main/uninstall.sh)"

```

使用加速源（我的加速源也可能帮你减速🤣）

```
export GH_PROXY=https://gh.monlor.com/ IMAGE_PROXY=ghcr.monlor.com && bash -c "$(curl -fsSL ${GH_PROXY}https://raw.githubusercontent.com/monlor/docker-xiaoya/main/uninstall.sh)"

```

####  自定义配置
【**非必须，小白跳过这一步** 】脚本没有计划支持硬解，在我看来这个功能没有必要。如果你需要修改硬解，端口，数据目录，环境变量，请自行修改docker-compose.yml和env文件，修改完成后执行下面的命令，使配置生效。**修改后注意** ：执行更新脚本会覆盖docker-compose.yml，不会覆盖env文件。

```
cd 你的安装目录
docker-compose up --remove-orphans -d

```

####  发烧友测试版
以下是测试版一键部署脚本，使用此脚本可以体验最新的功能，具体可以查看更新了哪些测试版专属功能，**此脚本仅限发烧友使用，需要有一定的解决问题能力**

```
export VERSION=main && bash -c "$(curl -fsSL ${GH_PROXY}https://raw.githubusercontent.com/monlor/docker-xiaoya/${VERSION:-main}/install.sh)"

```

###  部署配置推荐  
| 部署方案  | CPU  | 内存  | 硬盘  |  
| --- | --- | --- | --- |  
| **Alist + Emby**  | 2核  | 4G  | 150G  |  
| **仅部署 Alist**  | 1核  | 512M  | 512M  |  
| **Alist + Emby + Jellyfin**  | 2核  | 4G  | 200G  |  
| **Alist + Jellyfin**  | 2核  | 4G  | 150G  |  
###  配置示例
  * [部署小雅alist+emby](https://www.monlor.com/docker-compose.yml)
  * [部署小雅alist+jellyfin](https://www.monlor.com/docker-compose-jellyfin.yml)
  * [部署小雅alist+emby+jellyfin](https://www.monlor.com/docker-compose-all.yml)


###  服务组件介绍
  * [Alist](https://www.monlor.com/alist): 提供资源在线播放，WebDav服务
  * [Metadata](https://www.monlor.com/metadata): Emby和Jellyfin的元数据管理
  * [Emby](https://www.monlor.com/emby): 用家庭影视库的方式，可视化展示Alist中的资源
  * [Jellyfin](https://www.monlor.com/jellyfin): Emby的开源版本，功能是一样的


###  手动部署
仅展示小雅alist+emby的部署方式
####  使用Docker Compose
  1. 创建compose文件夹


```
mkdir /opt/xiaoya
cd /opt/xiaoya

```

  1. 下载配置


```
curl -#LO https://raw.githubusercontent.com/monlor/docker-xiaoya/main/docker-compose.yml
curl -#LO https://raw.githubusercontent.com/monlor/docker-xiaoya/main/env

```

  1. 修改配置env里面的阿里云盘相关变量，启动服务


```
docker compose up -d

```

  1. 查看日志


```
docker compose logs

```

####  使用docker部署【不推荐】
  1. 创建volume


```
docker volume create xiaoya
docker volume create media
docker volume create config
docker volume create meta
docker volume create cache

```

  1. 创建网络


```
docker network create xiaoya

```

  1. 启动小雅alist，修改下面的阿里云盘配置，再执行命令


```
docker run -d --name alist \
    -v xiaoya:/data \
    -p 5678:5678 -p 2345:2345 -p 2346:2346 \
    -e TZ=Asia/Shanghai \
    -e ALIYUN_TOKEN=阿里云盘TOKEN \
    -e ALIYUN_OPEN_TOKEN=阿里云盘Open Token \
    -e ALIYUN_FOLDER_ID=阿里云盘文件夹ID \
    -e AUTO_UPDATE_ENABLED=true \
    -e AUTO_CLEAR_ENABLED=true \
    -e EMBY_ADDR=http://emby:6908 \
    --network=xiaoya \
    ghcr.io/monlor/xiaoya-alist 

```

  1. 启动metadata用于元数据同步


```
docker run -d --name metadata \
    -e LANG=C.UTF-8 \
    -e EMBY_ENABLED=true \
    -e JELLYFIN_ENABLED=false \
    -e AUTO_UPDATE_EMBY_CONFIG_ENABLED=true \
    -e ALIST_ADDR=http://alist:5678 \
    -e EMBY_ADDR=http://emby:6908 \
    -v xiaoya:/etc/xiaoya \
    -v media:/media/xiaoya \
    -v config:/media/config \
    -v cache:/media/config/cache \
    -v meta:/media/temp \
    --network=xiaoya \
    ghcr.io/monlor/xiaoya-metadata

```

  1. 启动emby服务


```
docker run -d --name emby
    -e TZ=Asia/Shanghai \
    -e GIDLIST=0 \
    -e ALIST_ADDR=http://alist:5678 \
    --privileged \
    --device /dev/dri:/dev/dri \
    -v media:/media \
    -v config:/config \
    -v cache:/cache \
    -p 6908:6908 \
    --network=xiaoya \
    ghcr.io/monlor/xiaoya-embyserver

```

  1. 查看日志


```
docker logs alist
docker logs metadata
docker logs emby

```

###  安全建议
🔹 **开启alist的登陆** ，alist服务设置`FORCE_LOGIN=true`，设置webdav的密码`WEBDAV_PASSWORD`
🔹 **在emby控制台修改ApiKey** ，这个key需要配置到metadata和alist服务，变量名：`EMBY_APIKEY`
最后修改：2024 年 06 月 04 日
© 允许规范转载
#### 赞赏作者


如果觉得我的文章对你有用，请我喝杯咖啡吧☕️~
#### 83 条评论
  1. [March 2nd, 2025 at 06:44 pm](https://www.monlor.com/archives/144/#comment-446)
独特的构思和新颖的观点，让这篇文章在众多作品中脱颖而出。
  2. [March 1st, 2025 at 07:54 pm](https://www.monlor.com/archives/144/#comment-434)
结论部分可提出实际应用建议，提升价值。
  3. [February 13th, 2025 at 07:24 pm](https://www.monlor.com/archives/144/#comment-424)
大佬您好，目前我遇到了一个问题，在env中填写115pan—cookie之后，重构时可以看到提示有效的cookie和会员识别，但是获取直链不成功。cookie从ios客户端抓包取得，在alist标准版测试没有问题，可以正常播放，但是在小雅中提示{"state":false,"error":"请重新登录","errno":99,"request":"/app/share/downurl?t=1739445771","data":[]}: user not login。请问我应该怎么解决呢。(☆ω☆)
  4. [November 29th, 2024 at 11:08 pm](https://www.monlor.com/archives/144/#comment-408)
你的文章充满了欢乐，让人忍不住一笑。 <https://www.4006400989.com/qyvideo/40579.html>
  5. [November 28th, 2024 at 06:23 pm](https://www.monlor.com/archives/144/#comment-405)
你的文章充满了欢乐，让人忍不住一笑。 <https://www.yonboz.com/video/27716.html>
  6. [November 20th, 2024 at 09:26 am](https://www.monlor.com/archives/144/#comment-398)
博主你好 我有个疑问阿里云盘自动清理间隔是0-60分钟如果想改成 180分钟怎么改 忘指教因为有些电影是超过60分钟的时长的，还没看完 直链就没有了
  7. [November 18th, 2024 at 03:53 am](https://www.monlor.com/archives/144/#comment-396)
你的文章充满了欢乐，让人忍不住一笑。 <http://www.55baobei.com/ybg9nHvVjb.html>
  8. [November 2nd, 2024 at 07:31 pm](https://www.monlor.com/archives/144/#comment-384)
你的文章让我学到了很多技能，非常实用。
  9. [September 24th, 2024 at 10:34 am](https://www.monlor.com/archives/144/#comment-375)
博主，一直提示我元数据“获取目录失败，这个要怎么搞
metadata-1 | Link is 元数据/config_jf.mp4metadata-1 | metadata-1 | 09/24 10:30:50 [NOTICE] Downloading 1 item(s)alist-1 | 获取目录失败： object not foundmetadata-1 | metadata-1 | 09/24 10:30:50 [NOTICE] Download complete: /media/temp/config_jf.mp4metadata-1 | metadata-1 | Download Results:metadata-1 | gid |stat|avg speed |path/URImetadata-1 | ======+====+===========+=======================================================metadata-1 | df7675|OK | 1.5KiB/s|/media/temp/config_jf.mp4metadata-1 | metadata-1 | Status Legend:metadata-1 | (OK):download completed.metadata-1 | Download config_jf.mp4 failed, file size less than 10M, retry after 10 seconds.metadata-1 | Downloading config_jf.mp4, try 5...metadata-1 | Link is 元数据/config_jf.mp4metadata-1 | metadata-1 | 09/24 10:31:00 [NOTICE] Downloading 1 item(s)alist-1 | 获取目录失败： object not foundmetadata-1 | metadata-1 | 09/24 10:31:00 [NOTICE] Download complete: /media/temp/config_jf.mp4metadata-1 | metadata-1 | Download Results:metadata-1 | gid |stat|avg speed |path/URImetadata-1 | ======+====+===========+=======================================================metadata-1 | cc35b9|OK | 2.8KiB/s|/media/temp/config_jf.mp4metadata-1 | metadata-1 | Status Legend:metadata-1 | (OK):download completed.metadata-1 | Download config_jf.mp4 failed, file size less than 10M, retry after 10 seconds.metadata-1 | Download config_jf.mp4 failed.
  10. **Silence**
[September 12th, 2024 at 06:18 pm](https://www.monlor.com/archives/144/#comment-373)
大佬，这边的项目目前是停止更新了吗
  11. [August 28th, 2024 at 09:07 pm](https://www.monlor.com/archives/144/#comment-368)
xiaoya-alist-1 | 获取目录失败： object not foundxiaoya-alist-1 | 获取目录失败： object not foundxiaoya-alist-1 | 获取目录失败： object not foundxiaoya-alist-1 | 获取目录失败： object not foundxiaoya-alist-1 | 获取目录失败： object not foundxiaoya-alist-1 | 获取目录失败： object not foundxiaoya-alist-1 | 获取目录失败： object not found已经安装了小雅+emby，现在继续安装小雅+emby+jellyfin 一直提示这个。有点晕。
    1. **johanna**
[September 3rd, 2024 at 10:30 am](https://www.monlor.com/archives/144/#comment-369)
解决了吗？我也遇到同样的问题了。我设置了文件夹的权限也是不行，是不是网络问题哦
  12. **kacason**
[August 20th, 2024 at 05:13 pm](https://www.monlor.com/archives/144/#comment-366)
大佬，请问env里的ali token和opentoken字段，值需要加双引号吗？ 我发现每次./manage.sh reload 或者单独重启alist 的容器后， Ali的token和opentoken都不是我写进env的，每次我都得手动进/opt/xiaoya/data/xiaoya去修改这两个token。
  13. [August 20th, 2024 at 04:48 pm](https://www.monlor.com/archives/144/#comment-365)
请问ALIST后面的用户名和密码在哪里看？网上找的.alist admin 在用SSL连接的时候报错，小白请教！！
  14. **marcoer**
[August 10th, 2024 at 07:49 pm](https://www.monlor.com/archives/144/#comment-362)
求问博主，现在阿里转存115在alist网页端播放正常，但启动emby客户端却一直转圈无法播放，查看docker后台也没有任何调用阿里的进程，emby_server里的地址是 求问该怎么解决这个emby不能正常播放的问题？谢谢！
    1. **kacason**
[August 18th, 2024 at 10:17 pm](https://www.monlor.com/archives/144/#comment-364)
ip改成你docker宿主机实际ip试试
  15. **winhkey**
[August 6th, 2024 at 04:37 pm](https://www.monlor.com/archives/144/#comment-360)
请问转存到115以后，是可以自动调用115链接播放，还是得从挂载的115网盘进去重新播放
  16. [August 2nd, 2024 at 05:34 pm](https://www.monlor.com/archives/144/#comment-356)
目前阿里云盘推出了第三方应用权益包的月套餐，不付费就限速，问题是，付费了也只有1T，如果是刷剧，一下子就没了。楼主可以出个方便修改到夸克或者115的方法不？
  17. **marcoer**
[August 2nd, 2024 at 03:57 pm](https://www.monlor.com/archives/144/#comment-355)
该评论仅登录用户及评论双方可见
  18. **marcoer**
[August 1st, 2024 at 04:48 pm](https://www.monlor.com/archives/144/#comment-348)
博主大大好！按您这个部署方法安装完成后，怎么添加ali2115.txt（阿里云转存115）并生效啊？我之前用过其他alist+emby确定是可以用emby播放阿里转存到115网盘的视频的，但您这个我找不到地方添加啊？配置文件不知道怎么改，将ali2115.txt放到默认目录 /opt/xiaoya/，重启docker服务也没生效。我是安装在ubuntu24.04上的（一台笔记本划了240G空间），安装的您的alist+Emby一键部署。阿里云我充了一个月的svip试验，测试是还是限速的，在alist网页端能播放，但卡（380kb/s），所以就非常需要转存到115网盘。您这个方案很好，但就是差了这个转存115网盘的设置，请教该如何设置添加转存115网盘？急！万分感谢！ali2115.txt的内容如下：purge_ali_temp=true
cookie="USERSESSIONID=xxx"
purge_pan115_temp=true
dir_id=0
    1. [August 1st, 2024 at 06:07 pm](https://www.monlor.com/archives/144/#comment-349)
进alist容器的/etc/xiaoya目录，自己添加该文件重启就好了
      1. **fushiji**
[August 5th, 2024 at 08:17 pm](https://www.monlor.com/archives/144/#comment-358)
那容器重启后，ali2115.txt 是不是就丢失了呢？怎么参映射到Nas本地的目录呢？OωO
      2. **marcoer**
[August 2nd, 2024 at 03:02 pm](https://www.monlor.com/archives/144/#comment-354)
搞定了，原来是进容器操作，还以为是像之前那些操作直接复制到本地文件夹。谢谢博主！ヾ(≧∇≦*)ゝ
      3. **marcoer**
[August 2nd, 2024 at 01:49 pm](https://www.monlor.com/archives/144/#comment-353)
照博主说的放在/etc/xiaoya下了，但还是限速500K？另外我是笔记本电脑装的ubuntu系统，就放这个目录没问题吧？没放在var/lib/docker目录下
      4. **marcoer**
[August 1st, 2024 at 06:30 pm](https://www.monlor.com/archives/144/#comment-351)
谢谢，这就试试！
  19. [July 31st, 2024 at 07:39 pm](https://www.monlor.com/archives/144/#comment-347)
有个关于emby路径的小问题，部署emby docker参数 -v config:/config -v cache:/cache，请问emby这里的两个路径代表什么意思，配置在哪里啊？
    1. [August 1st, 2024 at 06:07 pm](https://www.monlor.com/archives/144/#comment-350)
这是用的docker 卷，用docker volume命令创建的，你也可以映射在本地文件夹
      1. [August 2nd, 2024 at 11:09 am](https://www.monlor.com/archives/144/#comment-352)
这个cache映射感觉是多余的？这样映射后实际emby容器并没有用到/cache，其实还是使用的 /config/cache
  20. [July 29th, 2024 at 02:50 pm](https://www.monlor.com/archives/144/#comment-338)
請問版主大大,這個組合會用到那些PORT呢,因為一開群暉防火牆,就不能用,要把群暉防火牆關掉才能更新...
    1. [July 29th, 2024 at 02:54 pm](https://www.monlor.com/archives/144/#comment-339)
5678 2345 2346 6908 8096
      1. [July 30th, 2024 at 12:44 am](https://www.monlor.com/archives/144/#comment-340)
大大晚上好,感謝大大回答,可以再請問大大,如果一開始用Alist + Emby ,後來想增加 Jellyfin,是可以直接重執行一鍵程序選4嗎...還是要選3...或是只能推倒重頭來過了??
        1. [July 30th, 2024 at 09:20 am](https://www.monlor.com/archives/144/#comment-341)
不会重新来，可以随时重新执行安装脚本来修改安装类型


#### 发表评论 
使用cookie技术保留您的个人信息以便您下次快速评论，继续评论表示您已同意该条款 
# 小雅影视库一键部署项目，私人影视库的最佳选择
[monlor](https://www.monlor.com/archives/144/) • 2024 年 06 月 04 日
<p><img src="https://cdn.monlor.com/2024/6/4/SCR-20240604-sexe.jpeg" alt="" style=""></p><h3><a id="%E5%B0%8F%E9%9B%85%E5%85%A8%E5%AE%B6%E6%A1%B6%E9%83%A8%E7%BD%B2" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>小雅全家桶部署</h3><p>📚 项目地址：<strong><span class="external-link"><a class="no-external-link" href="https://github.com/monlor/docker-xiaoya" target="_blank"><i data-feather="external-link"></i>https://github.com/monlor/docker-xiaoya</a></span></strong></p><p>💡使用 Docker Compose 以更优雅的方式来部署小雅服务，支持一键部署 Alist + Emby + Jellyfin，全平台支持，Linux/Windows/Mac/群晖，X86/Arm架构</p><h3><a id="%E5%8A%9F%E8%83%BD%E7%89%B9%E6%80%A7" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>功能特性</h3><p><img src="https://cdn.monlor.com/2024/6/4/SCR-20240603-kpvb.jpeg" alt="" style=""></p><p>🚀 使用 Docker Compose 一键部署服务，兼容群晖，Linux，Windows，Mac，包含所有X86和Arm架构</p><p>✨ 部署alist+下载元数据+部署emby/jellyfin服务全流程自动，无需人工干预</p><p>🔹 <strong>Docker集成</strong>：所有脚本集成到Docker镜像中，避免了系统环境污染。</p><p>🔹 <strong>镜像合并</strong>：合并了jellyfin和emby的x86和arm镜像，部署时无需区分镜像名。</p><p>🔹 <strong>自动化脚本</strong>：集成云盘清理脚本到alist服务，无需单独部署。</p><p>🔹 <strong>环境配置简化</strong>：通过环境变量配置阿里云盘token，无需映射文件。</p><p>🔹 <strong>依赖检查自动化</strong>：jellyfin和emby启动时自动进行依赖检查，等待元数据下载完成后自动添加hosts。</p><p>🔹 <strong>设备兼容性</strong>：完全兼容所有能运行docker的x86和arm设备。</p><p>🔹 <strong>自动清理与同步</strong>：支持自动清理阿里云盘，自动同步小雅元数据。</p><p>🔹 <strong>自动更新地址</strong>：自动更新内部的alist，emby，jellyfin访问地址，无需手动配置。</p><p>🔹 <strong>元数据服务更新</strong>：通过metadata服务自动更新emby配置和元数据。</p><h3><a id="%E4%B8%80%E9%94%AE%E9%83%A8%E7%BD%B2" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>一键部署</h3><h4><a id="%E9%83%A8%E7%BD%B2%E6%88%96%E6%9B%B4%E6%96%B0%E8%84%9A%E6%9C%AC" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>部署或更新脚本</h4><blockquote> <p>脚本支持重复执行</p> </blockquote><pre><code class="language-bash">bash -c &quot;$(curl -fsSL https://raw.githubusercontent.com/monlor/docker-xiaoya/main/install.sh)&quot; </code></pre><p>使用加速源（我的加速源也可能帮你减速🤣）</p><pre><code class="language-bash">export GH_PROXY=https://gh.monlor.com/ IMAGE_PROXY=ghcr.monlor.com &amp;&amp; bash -c &quot;$(curl -fsSL ${GH_PROXY}https://raw.githubusercontent.com/monlor/docker-xiaoya/main/install.sh)&quot; </code></pre><h4><a id="%E5%8D%B8%E8%BD%BD%E8%84%9A%E6%9C%AC" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>卸载脚本</h4><pre><code class="language-bash">bash -c &quot;$(curl -fsSL https://raw.githubusercontent.com/monlor/docker-xiaoya/main/uninstall.sh)&quot; </code></pre><p>使用加速源（我的加速源也可能帮你减速🤣）</p><pre><code class="language-bash">export GH_PROXY=https://gh.monlor.com/ IMAGE_PROXY=ghcr.monlor.com &amp;&amp; bash -c &quot;$(curl -fsSL ${GH_PROXY}https://raw.githubusercontent.com/monlor/docker-xiaoya/main/uninstall.sh)&quot; </code></pre><h4><a id="%E8%87%AA%E5%AE%9A%E4%B9%89%E9%85%8D%E7%BD%AE" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>自定义配置</h4><p>【<strong>非必须，小白跳过这一步</strong>】脚本没有计划支持硬解，在我看来这个功能没有必要。如果你需要修改硬解，端口，数据目录，环境变量，请自行修改docker-compose.yml和env文件，修改完成后执行下面的命令，使配置生效。<strong>修改后注意</strong>：执行更新脚本会覆盖docker-compose.yml，不会覆盖env文件。</p><pre><code class="language-bash">cd 你的安装目录 docker-compose up --remove-orphans -d </code></pre><h4><a id="%E5%8F%91%E7%83%A7%E5%8F%8B%E6%B5%8B%E8%AF%95%E7%89%88" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>发烧友测试版</h4><p>以下是测试版一键部署脚本，使用此脚本可以体验最新的功能，具体可以查看<span class="external-link"><a class="no-external-link" href="https://github.com/monlor/docker-xiaoya/commits/main/" target="_blank"><i data-feather="external-link"></i>commit</a></span>更新了哪些测试版专属功能，<strong>此脚本仅限发烧友使用，需要有一定的解决问题能力</strong></p><pre><code class="language-bash">export VERSION=main &amp;&amp; bash -c &quot;$(curl -fsSL ${GH_PROXY}https://raw.githubusercontent.com/monlor/docker-xiaoya/${VERSION:-main}/install.sh)&quot; </code></pre><h3><a id="%E9%83%A8%E7%BD%B2%E9%85%8D%E7%BD%AE%E6%8E%A8%E8%8D%90" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>部署配置推荐</h3><table> <thead> <tr> <th>部署方案</th> <th>CPU</th> <th>内存</th> <th>硬盘</th> </tr> </thead> <tbody> <tr> <td><strong>Alist + Emby</strong></td> <td>2核</td> <td>4G</td> <td>150G</td> </tr> <tr> <td><strong>仅部署 Alist</strong></td> <td>1核</td> <td>512M</td> <td>512M</td> </tr> <tr> <td><strong>Alist + Emby + Jellyfin</strong></td> <td>2核</td> <td>4G</td> <td>200G</td> </tr> <tr> <td><strong>Alist + Jellyfin</strong></td> <td>2核</td> <td>4G</td> <td>150G</td> </tr> </tbody> </table><h3><a id="%E9%85%8D%E7%BD%AE%E7%A4%BA%E4%BE%8B" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>配置示例</h3><ul> <li><a href="/docker-compose-alist.yml">只部署小雅alist</a></li> <li><a href="/docker-compose.yml">部署小雅alist+emby</a></li> <li><a href="/docker-compose-jellyfin.yml">部署小雅alist+jellyfin</a></li> <li><a href="/docker-compose-all.yml">部署小雅alist+emby+jellyfin</a></li> </ul><h3><a id="%E6%9C%8D%E5%8A%A1%E7%BB%84%E4%BB%B6%E4%BB%8B%E7%BB%8D" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>服务组件介绍</h3><ul> <li><a href="/alist">Alist</a>: 提供资源在线播放，WebDav服务</li> <li><a href="/metadata">Metadata</a>: Emby和Jellyfin的元数据管理</li> <li><a href="/emby">Emby</a>: 用家庭影视库的方式，可视化展示Alist中的资源</li> <li><a href="/jellyfin">Jellyfin</a>: Emby的开源版本，功能是一样的</li> </ul><h3><a id="%E6%89%8B%E5%8A%A8%E9%83%A8%E7%BD%B2" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>手动部署</h3><p>仅展示小雅alist+emby的部署方式</p><h4><a id="%E4%BD%BF%E7%94%A8docker-compose" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>使用Docker Compose</h4><ol> <li>创建compose文件夹</li> </ol><pre><code class="language-bash">mkdir /opt/xiaoya cd /opt/xiaoya </code></pre><ol start="2"> <li>下载配置</li> </ol><pre><code class="language-bash">curl -#LO https://raw.githubusercontent.com/monlor/docker-xiaoya/main/docker-compose.yml curl -#LO https://raw.githubusercontent.com/monlor/docker-xiaoya/main/env </code></pre><ol start="3"> <li>修改配置env里面的阿里云盘相关变量，启动服务</li> </ol><pre><code class="language-bash">docker compose up -d </code></pre><ol start="4"> <li>查看日志</li> </ol><pre><code class="language-bash">docker compose logs </code></pre><h4><a id="%E4%BD%BF%E7%94%A8docker%E9%83%A8%E7%BD%B2%E3%80%90%E4%B8%8D%E6%8E%A8%E8%8D%90%E3%80%91" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>使用docker部署【不推荐】</h4><ol> <li>创建volume</li> </ol><pre><code class="language-bash">docker volume create xiaoya docker volume create media docker volume create config docker volume create meta docker volume create cache </code></pre><ol start="2"> <li>创建网络</li> </ol><pre><code class="language-bash">docker network create xiaoya </code></pre><ol start="3"> <li>启动小雅alist，修改下面的阿里云盘配置，再执行命令</li> </ol><pre><code class="language-bash">docker run -d --name alist \ -v xiaoya:/data \ -p 5678:5678 -p 2345:2345 -p 2346:2346 \ -e TZ=Asia/Shanghai \ -e ALIYUN_TOKEN=阿里云盘TOKEN \ -e ALIYUN_OPEN_TOKEN=阿里云盘Open Token \ -e ALIYUN_FOLDER_ID=阿里云盘文件夹ID \ -e AUTO_UPDATE_ENABLED=true \ -e AUTO_CLEAR_ENABLED=true \ -e EMBY_ADDR=http://emby:6908 \ --network=xiaoya \ ghcr.io/monlor/xiaoya-alist </code></pre><ol start="4"> <li>启动metadata用于元数据同步</li> </ol><pre><code class="language-bash">docker run -d --name metadata \ -e LANG=C.UTF-8 \ -e EMBY_ENABLED=true \ -e JELLYFIN_ENABLED=false \ -e AUTO_UPDATE_EMBY_CONFIG_ENABLED=true \ -e ALIST_ADDR=http://alist:5678 \ -e EMBY_ADDR=http://emby:6908 \ -v xiaoya:/etc/xiaoya \ -v media:/media/xiaoya \ -v config:/media/config \ -v cache:/media/config/cache \ -v meta:/media/temp \ --network=xiaoya \ ghcr.io/monlor/xiaoya-metadata </code></pre><ol start="5"> <li>启动emby服务</li> </ol><pre><code class="language-bash">docker run -d --name emby -e TZ=Asia/Shanghai \ -e GIDLIST=0 \ -e ALIST_ADDR=http://alist:5678 \ --privileged \ --device /dev/dri:/dev/dri \ -v media:/media \ -v config:/config \ -v cache:/cache \ -p 6908:6908 \ --network=xiaoya \ ghcr.io/monlor/xiaoya-embyserver </code></pre><ol start="6"> <li>查看日志</li> </ol><pre><code class="language-plain_text">docker logs alist docker logs metadata docker logs emby </code></pre><h3><a id="%E5%AE%89%E5%85%A8%E5%BB%BA%E8%AE%AE" class="anchor" aria-hidden="true"><span class="octicon octicon-link"></span></a>安全建议</h3><p>🔹 <strong>开启alist的登陆</strong>，alist服务设置<code>FORCE_LOGIN=true</code>，设置webdav的密码<code>WEBDAV_PASSWORD</code></p><p>🔹 <strong>在emby控制台修改ApiKey</strong>，这个key需要配置到metadata和alist服务，变量名：<code>EMBY_APIKEY</code></p>
