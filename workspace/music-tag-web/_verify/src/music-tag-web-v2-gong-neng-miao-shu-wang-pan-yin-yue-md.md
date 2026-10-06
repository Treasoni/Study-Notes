> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/wang-pan-yin-yue.md).

# 网盘音乐

播放和管理网盘音乐

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F7TwNJzNRPwsoL936Ux5t%2Fimage.png?alt=media&amp;token=06506a68-76fd-428b-ba09-b05c9a438fd8" alt=""><figcaption><p>网盘音乐播放</p></figcaption></figure>

## 直连模式

> 直接连接 alist api，对网盘音乐进行刮削和入库。\
> 注意：刮削操作不会修改网盘音乐文件的元数据。

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2Fp6NueuaMDMuiEFdO0VvM%2Fimage.png?alt=media&amp;token=0240f247-8a6a-49a2-bbf1-b32e4cbc8a9d" alt=""><figcaption><p>直连设置</p></figcaption></figure>

* Alist Url： alist 的访问地址，可以是局域网地址或域名地址。\
  使用 alist 来管理连接网盘，如果你还未安装可以在 alist 官网找到[安装教程](https://alist.nn.ci/zh/guide/install/docker.html)
* 根目录地址：可能你的网盘上存在目录 /电影/，/音乐/， /照片/，选择你需要展示的根目录，将映射在本项目的/app/webdav/ 目录下。
* 用户名：alist 登录用户名
* 账号密码：alist 登录密码
* 显示条数：每个目录下显示多少条子目录或文件
* 清除缓存：本项目会缓存音乐文件的元数据，防止频繁访问网盘 API。

配置完成后查看-操作台- /app/webdav 目录 是否出现网盘文件。如果你当前目录是/app/media ，后退一层目录就能看到 /app/webdav目录，点击进入就是 网盘中配置的根目录下的文件和目录。

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FznyUC8mKw7y5oboDhwpv%2Fimage.png?alt=media&amp;token=4c5ba66e-cf02-4058-a1fc-4759da4ad892" alt="" width="188"><figcaption></figcaption></figure>

## 本地挂载

> 通过挂载工具将网盘挂载本地/app/weddav 目录，可当做本地文件使用

1. **部署时增加映射**\
   额外映射挂载卷&#x20;

   * /path/to/your/webdavmusic:/app/webdav:rw

   挂载的地址需要和 alist 中的地址一致，alist 才能正确解析出网盘音乐地址\
   例如：\
   在 alist 中音乐的地址是：<http://127.0.0.1:5244/aliyun/音乐/陈楚生/2024-> 风吹过的思念/陈楚生 - 风吹过的思念.flac\
   ![](https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FZ6hcPMCmVsAoj1tweKaA%2Fimage.png?alt=media\&token=3bf85c9c-1b59-4288-a6ed-be85b43842d0)\
   那么在操作台中地址是：/app/webdav/aliyun/音乐/陈楚生/2024- 风吹过的思念/陈楚生 - 风吹过的思念.flac\
   这样才能正确的
2. **系统设置**-基本设置-webdav写入位置-勾选数据库
3. **导入收藏**
4. **系统设置**-网盘音乐-配置 alist 地址，该项目利用 alist 解析网盘音乐 302 地址。<br>
