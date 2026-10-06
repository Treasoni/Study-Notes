> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/ji-ben-she-zhi.md).

# 基本设置

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FaELxVAOf0PKhIHcA37Ee%2Fimage.png?alt=media&amp;token=01c79130-7999-4be4-9858-ffcfd1619fe7" alt=""><figcaption><p>基本设置</p></figcaption></figure>

1. **本地音乐写入位置 ，** 写入元数据会影响做种，写入数据库必须有 mtw 提供的 subsonic 服务端播放才能显示。
2. **webdav 音乐写入位置**，网盘挂载在本地的目录，写入元数据会下载音乐后修改再上传回网盘，有较为频繁的操作，写入数据库，只会读取音乐文件的一部分内容就能读到元数据，然后存入 mtw 的数据库，使用提供的 subsonic 服务端播放才能显示。
