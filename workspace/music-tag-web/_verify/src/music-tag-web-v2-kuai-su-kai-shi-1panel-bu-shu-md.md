> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/1panel-bu-shu.md).

# 1panel部署

1panel 面板部署方式

官网地址：<http://www.musictagweb.com/>

## 方式一、应用商店安装（推荐）

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FXv4pEJYaFGrAXnQlhDOR%2Fc61071c66d0affa1ccc5c61c3307d8f6.png?alt=media&amp;token=e9d88a3a-3ba4-41ad-83aa-cb0a8052518d" alt=""><figcaption></figcaption></figure>

1. 打开 1Pannel 应用商店 - 搜索 Music Tag Web\ <br>

   <figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FUoQDElJYjfyY5gJ4CJKg%2Fbaf0505cd73004b9d9c6475beffbc7a5.png?alt=media&amp;token=9f45444c-9248-4cc3-8591-6dc0f515f5a6" alt=""><figcaption></figcaption></figure>
2. 点击安装即可。\
   默认挂载路径为&#x20;
   * ./data:/app/media:rw&#x20;
   * ./config:/app/data
3. 如需自定义媒体库地址，则编辑 compose 文件修改挂载的地址，例如：

```
<你的媒体库地址>:/app/media:rw 
```

## 方式二、镜像安装

1. 镜像中拉取镜像，仓库名 Docker Hub 镜像名：xhongc/music\_tag\_web:latest

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FhJSE2quZQgfyoQhLNLzo%2Fimage.png?alt=media&amp;token=f4886b27-254b-42e1-98be-3e14dab83eb9" alt=""><figcaption><p>镜像页面</p></figcaption></figure>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FUYv66uparuCpQ7Zn3KQb%2Fimage.png?alt=media&amp;token=b350d81c-c1ac-4ccb-aaa1-d0604d36d969" alt=""><figcaption><p>拉取镜像</p></figcaption></figure>

2. 创建容器，服务器端口可以自己定义你喜欢的端口（第一个值），容器端口必须是 8002（第二个值）不能改变，协议选 TCP 协议\
   \
   挂载设置里，将你的音乐文件映射到/app/media    此路径不可更改。\
   另，新建一个目录存放该项目的配置文件 映射到 /app/data    此路径不可更改。<br>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F93vC1q02gZ1GKewvOGfk%2Fimage.png?alt=media&amp;token=5f8ca00a-1541-4486-b0b7-2cb1aef44bc0" alt=""><figcaption><p>创建容器</p></figcaption></figure>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FsQ2axwZCC4ndw6qgEdLZ%2Fimage.png?alt=media&amp;token=83ac805a-9cdb-4c7a-953e-c02ef2bb5b2a" alt=""><figcaption><p>容器配置</p></figcaption></figure>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FJPOIwSW3iWtxpp6O6VnE%2Fimage.png?alt=media&amp;token=ef8d12f7-3e54-4f6c-8575-0d13aa8e186f" alt=""><figcaption><p>部署完成</p></figcaption></figure>

在登录后 点击V1 标签，输入 V2 激活 即可完成激活。
