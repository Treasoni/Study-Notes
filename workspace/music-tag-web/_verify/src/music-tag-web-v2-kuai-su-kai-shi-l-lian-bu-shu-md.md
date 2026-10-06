> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/l-lian-bu-shu.md).

# 绿联部署

官网地址：<http://www.musictagweb.com/>

1. 打开终端。
2. 连接到绿联设备的SSH地址。
3. 使用 `sudo -i` 命令获取管理员权限。
4. 输入以下Docker运行命令以启动Music Tag Web服务：

   ```
   docker run -d -p 8002:8002 -v /path/to/your/music:/app/media -v /path/to/your/config:/app/data --name=music-tag-web --restart=unless-stopped xhongc/music_tag_web:latest 
   ```

   请确保将 `/path/to/your/music` 替换为你NAS上的音乐文件夹的绝对路径，并且 `/path/to/your/config` 替换为一个你新创建的目录路径，该目录将用于存放应用程序的配置文件。
5. 安装完成后，在网页浏览器中输入绿联设备的IP地址后跟端口号8002（例如 <http://greenlink\\_ip:8002），即可访问Music> Tag Web的登录界面。

请注意将 "greenlink\_ip" 替换为你的绿联设备的实际IP地址。
