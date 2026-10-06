> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web/qie-ge-yin-gui.md).

# 切割音轨

使用CUE专辑标记文件无损切割整轨CD音轨

1. 在[ffmpeg](https://johnvansickle.com/ffmpeg/) 官网中下载，版本基于你电脑系统架构的版本选择即可。\
   可执行文件放置在挂载的 /app/data/bin/ 目录\
   /app/data/ 为 部署时挂载的配置文件路径\
   ![](https://3761008155-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fg0Qb0o78UzRYrKFIbuBp%2Fuploads%2FBomUcx5E8SgMvw1vGlNm%2Fimage.png?alt=media\&token=73e837d7-03d2-415e-8a83-f90fd8b4fe37)
2. 解压缩后将 ffmpeg 执行文件（下图中ffmpeg单个文件，大小 20Mb 左右），移动到/app/data/bin 目录下。\
   /app/data/ 目录为部署时挂载的配置文件路径。\
   ![](https://3761008155-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fg0Qb0o78UzRYrKFIbuBp%2Fuploads%2FWfteBF3MhpSpaweIB2EU%2Fimage.png?alt=media\&token=0e1dae4e-8eeb-41c3-9dc2-5a3fa8e86dad)
3. 最终路径是 /app/data/bin/ffmpeg

***

注意点： 1. ffmpeg 不支持 ape 音乐的操作，如需要切分 ape 音乐，可先将 ape 转换为其他格式。

2. 需要有 ffmpeg 的执行权限 chmod +x /app/data/bin/ffmpeg
