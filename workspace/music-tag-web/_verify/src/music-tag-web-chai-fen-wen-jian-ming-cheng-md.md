> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web/chai-fen-wen-jian-ming-cheng.md).

# 拆分文件名称

你收集的音乐文件中，只有文件名称存在歌曲基本信息，元数据中没有的情况，可以快速的将文件名称中的基本信息嵌入到音乐元数据中。

<figure><img src="https://3761008155-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fg0Qb0o78UzRYrKFIbuBp%2Fuploads%2FufM7VfEUM576N7qjw9dT%2Fimage.png?alt=media&amp;token=e4527714-d94a-44de-907a-78c34433138d" alt=""><figcaption><p>拆分文件名称</p></figcaption></figure>

1. 支持定义两个标题规则，成功命中规则的文件会被修改。

例如： ${tracknumber}.${title}\
我的文件名称为：01. 我想.mp3\
${tracknumber}= 01, ${title} = 我想\
命中规则，会将tracknumber， title 嵌入音乐元数据。
