> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/gua-xiao-yi-shu-jia-bing-bei-navidrome-shi-bie.md).

# 刮削艺术家并被 navidrome 识别

本实验演示在music tag web 中批量刮削艺术家封面，并成功被 navidrome 识别到

**前提条件：** 确保您的音乐已导入到音乐收藏中。如果尚未导入，请[音乐收藏与播放](/music-tag-web-v2/gong-neng-miao-shu/yin-yue-shou-cang-yu-bo-fang.md)参考相关指南完成此步骤。

**对于收藏中缺少艺术家封面的情况：**\
![](https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FZI1AdUKtXtKu1IkEMVOL%2Fimage.png?alt=media\&token=f775330b-5fcf-4961-9818-256dbd96b4ef)

1. **设置艺术家封面抓取：**

   * 进入“系统设置”。
   * 选择“其他设置”。
   * 定位至“刮削艺术家”，并点击相应的按钮。\
     ![](https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FWqmjbrRkRlMXqgZeRCVa%2Fimage.png?alt=media\&token=32052c7a-43f2-4c63-aa27-89ba950d7572)

   操作完成后，您可以在“操作记录”中查看刮削过程的详情，确认艺术家信息是否已成功更新。
2. **艺术家页面展示封面：**
   * 成功刮削后，艺术家页面将显示封面图片。
   * 如果您的音乐文件目录结构如下所示：

     ```
     /app/media/music/王以太/演.说.家/人间天堂.flac
     ```
   * 则系统将在 `/王以太/` 目录下自动生成 `artist.jpg` 文件。
3. **封面文件识别：**
   * `artist.jpg` 文件将被 NaviDrome 自动识别并用于艺术家页面的展示。

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FnC45ZnrOkiGOcYsflWNE%2Fimage.png?alt=media&amp;token=867cbd36-0c06-4969-96f7-42a8ee8402e3" alt=""><figcaption></figcaption></figure>

\
![](https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FH4QIH55itP88gZpf3pN3%2Fimage.png?alt=media\&token=b6377d14-5ef0-4227-a898-9d440aa6ed81)\
![](https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FNkFNDHwTNGVWsmcH2x4r%2Fimage.png?alt=media\&token=4eb10b54-c33b-4f3a-a7a2-a4971dd9e93a)

**总结：** 为了确保艺术家封面能被正确显示，请务必按照以下目录结构组织您的音乐文件：

```
/艺术家/
    /专辑/
        音乐文件
```

这样可以保证 NaviDrome 能够准确地识别和展示艺术家及其作品的信息。

<br>
