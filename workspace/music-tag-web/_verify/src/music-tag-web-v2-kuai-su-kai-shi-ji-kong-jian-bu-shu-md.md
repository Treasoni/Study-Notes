> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/ji-kong-jian-bu-shu.md).

# 极空间部署

由于我没有极空间nas 教程来自网站：https\://izspace.cn/music/musictag.html

官网地址：<http://www.musictagweb.com/>

1. 拉取music tag web镜像

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FVKvnsstkAz7fbKChinbG%2Fimage.png?alt=media&amp;token=bdccc2bf-d883-4e26-8f65-d6b3d25bac99" alt=""><figcaption></figcaption></figure>

第二步，双击下载后的镜像文件

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F1faKLqrdYLTSMTNXCmi8%2Fimage.png?alt=media&amp;token=2b2e1548-06e4-4dda-90bb-f5fe1f7bc417" alt=""><figcaption></figcaption></figure>

第三步，创建 Docker 文件夹目录

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FWYCQL0ko67sLht1quCGX%2Fimage.png?alt=media&amp;token=160ff6f1-ef65-4dce-812f-66969e595217" alt=""><figcaption></figcaption></figure>

第四步，添加目录地址 本地存放音乐的目录 / 我的文件 /Music【替换成自己的目录】/app/media 刚新建的 Docker 配置目录 / 高速存储 /Docker/MuasiTag/config【替换成自己的目录】/app/data

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F4JYD2XQZ1mZ9S5hBgtVV%2Fimage.png?alt=media&amp;token=ab638fbc-ee2e-4b03-922c-d9169dd41c9c" alt=""><figcaption></figcaption></figure>

第五步，添加端口也可以是【host】默认应该是 8002，我选择的是自定义端口【bridge】

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FzjKtOnREwwM4Ju9fbaqr%2Fimage.png?alt=media&amp;token=35167ba9-4f38-432a-a5b2-b79f9da246b7" alt=""><figcaption></figcaption></figure>

部署完成
