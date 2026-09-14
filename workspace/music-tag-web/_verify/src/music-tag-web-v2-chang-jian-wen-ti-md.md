> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/chang-jian-wen-ti.md).

# 常见问题

FAQ ：官网地址：http\://www\.musictagweb.com/

1. Q：专辑封面图片、艺术家展示是裂开的图片和音乐也播放不了？\
   A：修改文件夹权限，设置为Everyone。\
   ![](https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FXoEKKPKicfj1vbvCufuS%2Fphoto_2024-03-25_21-45-52.jpg?alt=media\&token=d8582630-1c17-4f1b-8da5-5a32da278df4)<img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FqRVlSiZW9cq9AQssotEZ%2Fphoto_2024-03-25_21-46-08.jpg?alt=media&amp;token=34ce71db-eae7-4f3a-bd87-cd84edb18a1f" alt="" data-size="original">\
   ps. 确定配置访问的是 8002 端口

2. Q：怎么进来还是V1啊？\
   A：点击 V1 按钮输入激活码激活。<br>

3. Q：怎么获得激活码呢？\
   A：爱发电中<https://ifdian.net/a/music-tag-web> 发电后，会私信发你激活码。当爱发电进不去时，可添加作者微信（charlesnowed）购买激活码。<br>

4. Q：输入激活码没有反应？\
   A：确保容器里能访问到外部的网络，能访问到激活服务器，可以修改网络模式为 host试试。<br>

5. Q：为什么我首页歌曲是 0？\
   A：在操作台中勾选想要导入的歌曲目录-导入收藏，等待后台导入即可。<br>

6. Q：为什么音乐收藏一直在 loading 中？\
   A：更改过或未设置subsonic 的密码需要设置一次，需要重新再登录一次，后再刷新音乐收藏页面。<br>

7. Q: 后台刮削一直没有生效不执行啊？删除不存在的音乐收藏没有生效不执行啊？\
   A：其他设置-停止所有后台任务，等待重新执行。<br>

8. Q：搜索刮削不了任何信息，提示暂无歌曲信息\
   A：确认容器内可以访问网络，可以修改网络模式为 host试试。<br>

9. Q：/admin 进不去后台，报 403 无法访问\
   A：受限制框架安全机制，反代的地址无法进入，局域网地址可以。<br>

10. Q：购买激活码后，我重新部署容器或在另一台机器部署是否可以呢？\
    A：/app/data 配置没删除，重新部署自动生效 ，/app/data 删除 ， 可以用激活码重新激活\
    重新激活有 6 次上限，为了限制频繁激活。（可联系作者清空激活信息）\
    另一台机器激活后，上一台机器就会失效下线了<br>

11. Q：后台刮削中转移文件/整理文件可不可不选择，都是必选的吗？\
    A：是的，必须要选择，不然每次监控就不是增量数据，数据会越积累越多，这个目录的目的是为了新增音乐的自动刮削，如果因此不满足你的需求，我们从长计议。<br>

12. Q：V1 升级到 V2 需要重新部署吗？\
    A：需要确保你部署时后容器内端口是 8002，和去掉了 command /start 命令<br>

13. Q：激活失败？验证超时\
    A：容器内的时间校正为北京时间，不要相差超过一分钟！

14. Q：出现Database is locked ，数据库繁忙这么办？\
    A：Sqlite 数据库并发读写**独占锁**机制，会锁定整个数据库，可以切换到 mysql 数据库有更好体验。<br>
