> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/wang-ji-deng-lu-mi-ma-zen-me-ban.md).

# 忘记登录密码怎么办？

在Music Tag Web 中忘记登录密码

**第一步：重置管理员密码**

如果您忘记了如何操作，请按照以下步骤进行。

1. 首先，您需要进入项目的Docker容器内。
2. 在容器中打开终端，并执行下面的命令来启动密码更改过程：

   ```
   python manage.py changepassword admin
   ```

   请注意，这里的`admin`指的是您希望更改密码的用户账号名。如果您要为不同的用户更改密码，请将`admin`替换为目标用户的用户名。
3. 执行上述命令后，系统会提示您输入并确认新密码。请根据屏幕上的指示设置一个安全的新密码。

完成以上步骤后，指定用户的密码就更新成功了。
