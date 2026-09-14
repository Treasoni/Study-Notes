> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/hou-tai-gua-xiao-zen-me-wan.md).

# 后台刮削怎么玩

#### 后台刮削目录

* **路径选择**：您有两个选项 `/app/download` 和 `/app/media/download/`。
* 采用`/app/media/download/` 的话你无需再次映射挂载目录文件，在部署时候你已经映射目录/app/media了，你只需要在对应的此目录下创建一个 download文件即可，你之后的下载音乐都可以丢在这个目录下
* `采用/app/download` 意味着你可以自定义另外的任意文件夹来充当这个下载目录，你需要在部署的时候 额外添加一个挂载映射\
  ![](https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2Fo8x37xGnUe67cwKP7sSb%2Fimage.png?alt=media\&token=feacb9d8-44d3-4582-a5cc-d6376725a0ee)

#### 音乐预处理

1. **声纹识别**：对于缺少艺术家或专辑元数据的音乐文件，系统会使用声纹识别技术尝试找到匹配的信息。
2. **乱码修复**：系统会自动检测并修复文件名、艺术家、专辑名中的乱码问题。
3. **繁体转简体**：所有繁体中文会被转换成简体中文，保持一致性。

#### 音乐自动刮削

* **自动刮削**：从音乐流媒体平台获取元数据来更新音乐文件的标签信息。
* **手动刮削**：允许用户自定义修改音乐元数据，包括重命名文件、导出歌词和封面图片等。

#### 音乐文件整理（必选）

* **整理文件**：确保所有文件按照规定的格式存放。
* **转移文件**：根据处理结果（成功或失败），将文件转移到相应的 `completed` 或 `failed` 目录中。

####
