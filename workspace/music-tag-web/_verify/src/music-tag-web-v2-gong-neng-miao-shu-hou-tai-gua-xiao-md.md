> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/hou-tai-gua-xiao.md).

# 后台刮削

自动对新添加进文件夹的音乐自动刮削后整理归档到目录中。

**开启后台刮削**，后台会每3分钟检查 目标目录 进行自动刮削。

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FPE089C49zWBsdWNQV5iU%2Fimage.png?alt=media&amp;token=2312e9ca-2104-4d1a-8c02-d022c3ca7201" alt=""><figcaption></figcaption></figure>

**后台刮削目录：**

监听两个目标目录

`/app/download`&#x20;

该目录需要自在部署docker应用时额外再映射一个目录到/app/download，这个目录做为新增文件的下载目录可以是自定义的任意目录

`/app/media/download`

该目录不需要再次映射，因为/app/media 不出意外你在部署时已经映射过了，只需要在/app/media创建一个download 目录即可

**音乐预处理**

支持声纹识别、乱码修复、繁体转简体

**音乐自动刮削**
