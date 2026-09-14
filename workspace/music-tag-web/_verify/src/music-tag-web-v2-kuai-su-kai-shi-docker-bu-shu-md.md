> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-bu-shu.md).

# Docker部署

使用docker快速部署，与V1 版本的区别，容器内的端口是 8002，和不需要 command /start 命令

官网地址：<http://www.musictagweb.com/>

1. **拉取镜像**：
   * 在终端中使用以下命令从 Docker Hub 拉取最新版本的 `music_tag_web` 镜像：

     ```
     docker pull xhongc/music_tag_web:latest
     ```
2. **启动容器**：
   * 使用以下命令启动容器，记得替换 `/path/to/your/music` 和 `/path/to/your/config` 为实际路径：

     ```
     docker run -d -p 8002:8002 -v /path/to/your/music:/app/media -v /path/to/your/config:/app/data --name=music-tag-web --restart=unless-stopped xhongc/music_tag_web:latest 
     ```
   * 将 `/path/to/your/music` 替换为你的 NAS 上音乐文件夹的绝对路径。
   * 将 `/path/to/your/config` 替换为你新建的一个目录路径，用于存放应用程序的配置文件。
3. **访问应用**：
   * 安装完成后，在网页浏览器中输入 `http://127.0.0.1:8002` 或者绿联设备的实际 IP 地址加上端口 8002。
4. **修改默认密码**（可选）：
   * 登录后，默认账号密码为 `admin/admin`。
   * 在登录界面输入账号密码后，进入管理界面，可以修改默认密码。
   * 如果你反向代理页面进去报错 csrf 错误，请用局域网地址进入。
5. **修改 Subsonic 密码**（可选）：
   * 如果需要修改 Subsonic 的默认账号密码，也请在登录后进行操作。
   * 修改后可能需要重新登录，并且如果页面没有正确加载，请尝试刷新页面。
6. **激活 V2 版本**：
   * 登录后，点击 V1 标签，按照提示输入 V2 激活码以完成激活。
7. **遇到问题时**：
   * 如果在输入激活码时遇到错误提示，请检查和校正服务器时间，保证时间为正常的北京时间。
   * 如果问题仍然存在，请尝试联系作者寻求帮助。

<br>
