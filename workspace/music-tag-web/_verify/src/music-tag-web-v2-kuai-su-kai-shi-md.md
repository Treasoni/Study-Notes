> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi.md).

# 快速开始

与V1 版本的区别，容器内的端口是 8002，和不需要 command /start 命令

#### 官网地址：<http://www.musictagweb.com/>

#### 怎么安装？怎么部署？怎么使用？

#### V1 版本部署：

* 容器内的端口是 8001。
* 需要使用 `command /start` 命令来启动服务。

#### V2 版本部署：

* **容器端口**: V2 版本中的容器监听端口为 8002。
* **无需启动命令**: 不再需要使用 `command /start` 命令来启动服务。
* **多架构支持**: V2 版本支持 arm64、amd64 和 armv7 架构的 Docker 部署。
* **内容兼容性**: V2 项目包含了 V1 版本的所有功能，并可能添加了新的特性或改进。

## docker 镜像说明

镜像名称 `xhongc/music_tag_web:latest`

latest 为最新版本号，你也可以指定版本，例如：2.1.7, ...  可以在 [dockerhub](https://hub.docker.com/repository/docker/xhongc/music_tag_web/tags) 页面查看。

如果因为**网络问题，无法拉取镜像**，可以使用阿里云的 music tag web 镜像

阿里云镜像名称：`registry.cn-hangzhou.aliyuncs.com/xhongc/music_tag_web:latest`

下文中的 `xhongc/music_tag_web:latest` 替换成&#x20;

`registry.cn-hangzhou.aliyuncs.com/xhongc/music_tag_web:latest` &#x20;

即刻完成部署<br>
