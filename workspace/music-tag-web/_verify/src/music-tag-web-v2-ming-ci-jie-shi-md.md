> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/ming-ci-jie-shi.md).

# 名词解释

本项目中用到的名称进行说明描述，去除歧义。

### 刮削

**刮削一词源于影视刮削，应用到音乐中也具有同样的意思**\
音乐刮削：刮削是音频播放软件及音乐管理软件的一项功能，它可以自动识别音乐文件，并在线获取相应的专辑封面、歌曲名称、艺术家、专辑信息、流派和发行日期等数据，使得管理和播放本地音乐文件变得更加便捷。

### 元数据

元数据通常是指我们在音乐流媒体平台看到的与歌曲息息相关的信息，包括歌曲名称、演唱者、作词、作曲、唱片公司、发行公司等等，一般内嵌于音乐文件中，与音乐共同存在。

### 手动刮削

本项目中的功能，选择需要修改文件或文件目录，可自定义修改音乐**元数据中的内容。**

### 自动刮削

本项目中的功能，选择需要修改文件或文件目录，可自动从音乐流媒体平台搜索**元数据**实行**刮削**操作

### 后台刮削

本项目中的功能，固定的文件目录下，可自动从音乐流媒体平台搜索**元数据、整理文件夹、重命名**等一系列操作

### 变量

本项目中**元数据**的变量名称，可用变量名称去定义和组合，并赋值给其它**元数据**

* `${title}: 标题变量`
* `${artist}` : 艺术家变量
* `${first_artist}`: 多艺术家情况下的第一个艺术家 变量
* `${first_artist_letter}`：艺术家的第一个字母
* `${album}`: 专辑
* `${albumartist}` : 专辑艺术家
* `${discnumber}` : CD号，唱片碟号
* `${tracknumber}`: 音轨号
* `${filename}` :文件名称
* `${file_song_name}`：文件名称不含后缀名
* `${file_suffix}`:文件后缀 / 文件扩展名
* `${parent_path}`: 文件父目录名称
* `${parent_parent_path}`: 文件父目录的父目录名称
* `${lyrics}`: 歌词
* `${comment}`: 描述
* `${year}`: 年份
* `${genre}`: 风格/流派
* `${composer}`: 作曲家
* `${lyricist}`: 作词家
* `${language}`: 语言
* `${guess_language}`: 自动识别语言
* `${null}`: 空字符，将元数据置为空。
* `${counter}`: 递增计数器

[变量的使用说明](/music-tag-web-v2/gong-neng-miao-shu/bian-liang-de-shi-yong-shuo-ming.md)

**Docker目录挂载**

绑定挂载（Bind Mounts）是 Docker 容器与宿主机之间共享文件或目录的一种方式。它允许你将宿主机上的任意路径直接映射到容器内的指定路径。

当你使用绑定挂载时，你需要指定两个路径：

* **宿主机地址（Host Path）**：这是你的本地计算机（即运行 Docker 的机器）上的一个文件或目录的路径。这个路径是你想要与容器共享的数据所在的位置。
* **容器内地址（Container Path）**：这是在容器内部的路径，数据将会在这里变得可用。这个路径是相对于容器根目录的，所以通常以斜杠 `/` 开始。容器内的地址一般是开发者定义的路径位置，不可修改了。

例如，如果你有一个位于宿主机 `/home/user/data` 目录下的文件，并且你想让这些文件在容器内的 `/app/data` 目录中可用，那么你会使用如下命令：

`docker run -v /home/user/data:/app/data myimage`

**开放API**

由本项目开放出去的api，供其他第三方应用集成调用的接口，例如 info接口可供homepage应用展示信息，lyrics接口可供音流app展示歌词，health接口可供docker健康检查心跳检测
