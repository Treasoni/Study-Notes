> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/qun-hui-bu-shu.md).

# 群晖部署

官网地址：http\://www\.musictagweb.com/

&#x20;1\. 在注册表中搜索 music\_tag\_web, 第一个就是本项目的镜像，xhongc/music\_tag\_web<br>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2Fe3SDAR9zTEeLrK7VZ66H%2Fimage.png?alt=media&amp;token=35c52ff8-878f-47fa-a69a-9adc94e50311" alt=""><figcaption><p>注册表</p></figcaption></figure>

2. 填写配置，端口配置容器内是 8002（第二个值），容器外可以随意填写你喜欢的（第一个值）\
   存储空间设置里，将你的音乐文件映射到/app/media    此路径不可更改。\
   另，新建一个目录存放该项目的配置文件 映射到 /app/data    此路径不可更改。<br>

   <figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FbE6weiIn8Vf2PYrdAmaP%2Fimage.png?alt=media&amp;token=23c52507-156d-4b2f-bc56-3f3c0ef966cf" alt=""><figcaption></figcaption></figure>
