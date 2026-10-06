> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/xiao-ai-yin-xiang.md).

# 小爱音箱

使用小爱音箱播放局域网内的音乐，支持歌曲和播放列表点歌。

测试通过的型号 LX06，L16A，LX5A ，L17A，S12。

只能播放mp3 格式的型号：L05B

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FNwDjjysPuyrWcclmjxWQ%2Fimage.png?alt=media&amp;token=8c055180-d0e6-4d0f-84fd-167cb64f1bfa" alt=""><figcaption><p>小爱音箱配置</p></figcaption></figure>

1. **配置相应的信息，** 根据描述填写设备型号，名称，小米账号。\
   设备型号：在音箱底部标签获取，例如LX06\
   小米账号：为小米 ID ，非手机号码\
   设备名称：账号下小米音箱的名称，如果修改过音箱的名称则填写修改后的设备名称
2. **关键字**：用于识别是播放局域网音乐的需求。
3. **内网地址和端口**，内网地址是本项目的内网地址，端口是部署命令的端口。
4. **测试连接，** 测试成功小爱音箱会发出语音。\
   未发出语音播报，需检查上面的配置是否正确，小米账号密码是否正确，都检查正确还未发出语音可能是该型号的音箱不支持这个功能。
5. **轮询时间**，设置一个查询的间隔时间，单位为 秒
6. **是否启用**，启动后就可通过，唤醒小爱同学播放，例如：小爱同学 关键词 歌曲名，可以在操作日志查看是否检索到歌曲，（不需要说歌手！，不需要说歌手！，不需要说歌手！）
