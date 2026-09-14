> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web/kuai-su-kai-shi.md).

# 快速开始

快速开始部署您的应用

1. &#x20;从Docker Registry拉取镜像\
   `docker pull xhongc/music_tag_web:latest`
2. #### dokcer run

   `docker run -d -p 8001:8001 -v /path/to/your/music:/app/media -v /path/to/your/config:/app/data --restart=always xhongc/music_tag_web:latest`
3. 或者 使用portainer stacks部署（与2选一个方式即可）\
   `version: '3'`

   `services: music-tag: image: xhongc/music_tag_web:latest container_name: music-tag-web ports: - "8001:8001" volumes: - /path/to/your/music:/app/media:rw - /path/to/your/config:/app/data command: /start restart: always`

ps. `/path/to/your/music` 改成你的音乐文件夹路径！

`/path/to/your/config` 改为配置文件路径！

4. 修改默认密码（可选）\
   访问在`127.0.0.1:8001/admin` 默认账号密码 *admin/admin* 修改默认密码\
   ![](https://github.com/xhongc/music-tag-web/blob/dev_1.0/img_7.png)

此时你已经部署好了，你想知道具体怎么使用，请往下看吧。<br>

<br>
