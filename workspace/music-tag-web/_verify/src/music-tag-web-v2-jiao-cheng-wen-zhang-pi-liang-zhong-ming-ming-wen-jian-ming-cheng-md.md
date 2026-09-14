> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/pi-liang-zhong-ming-ming-wen-jian-ming-cheng.md).

# 批量重命名文件名称

本实验演示批量对文件名重命名。

重命名文件的情况有：\
\- 场景 1：文件名含有音轨号我不喜欢，我想批量去除掉。\
\- 场景 2：文件名我想以 艺术家-音乐名 格式进行重命名。

### 场景1 ：去除文件名中的音轨号

如果您不喜欢文件名中包含的音轨号，并希望批量去除它们，可以使用正则表达式来实现这一目标。例如，对于文件名 `01.夜曲.flac`，您可以使用如下正则表达式来解析并提取音轨号和歌曲标题：

```
(?P<tracknumber>\d+)\.(?P<title>\w+)
```

此正则表达式将匹配数字（即音轨号）后面跟着一个点和随后的单词字符（即歌曲标题）。虽然上述表达式能够正确地解析这些信息，但不会直接更改文件名。

我们只需要改变正则表达式，就能实现去掉音轨号，只保留《夜曲》 作为文件名。

```
(?P<tracknumber>\d+)\.(?P<filename>\w+)
```

实验结果如下图：

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F1RLsHiECkR1hx9URei72%2Fimage.png?alt=media&amp;token=7ce056d6-4d28-4cbe-9b82-a074a2061a2a" alt=""><figcaption></figcaption></figure>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F9MkoqqgIjDsoG0pI1STU%2Fimage.png?alt=media&amp;token=d0f8ee70-c586-4eac-a244-e1c8a167ed62" alt=""><figcaption></figcaption></figure>

### 场景2：采用艺术家-音乐名格式重命名文件

**步骤说明:**

1. **确保元数据完整**: 首先确认您的文件元数据中已经包含了正确的艺术家信息。
2. **使用手动刮削功能**:
   * 打开支持手动刮削功能。
   * 勾选需要重命名的文件。
   * 在“文件名”字段中，使用变量来构建新的文件名格式。

**变量使用示例:**

* 假设您想将文件重命名为${artist}-${title}这样的格式，其中${artist}代表艺术家名，${title}代表音乐名，文件扩展名会继续填充源文件的扩展名，所以你无需额外输入文件扩展名。

实验结果如下图：

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FYjU517CJcJpKEtmENHka%2Fimage.png?alt=media&amp;token=19e9d785-4cb5-45fa-8ade-4189dba955c2" alt=""><figcaption></figcaption></figure>

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FtrfYJKb8s5ccuXCac4aJ%2Fimage.png?alt=media&amp;token=a2a9109b-9827-40c5-8b0c-c9fb208ba3a1" alt=""><figcaption></figcaption></figure>
