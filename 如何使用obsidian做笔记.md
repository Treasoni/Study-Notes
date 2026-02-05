# 1.如何进行云备份
我们这里采用的使用使用github的方式进行云备份的。[Git创建仓库](Git/git教程.md#Git创建仓库)
首先我们需要使用git进行操作
>1. 我们先创建一个文件夹,并且用git进行初始化一个本地库。
>2. 我们在github上创建一个库，然后用命令把这个库和我们本地库进行关联。

## 1.1如何进行实时备份
我们如果仅是靠上面这个方法的话，我们每次都需要用命令把文件上传到github中，但是我们可以在obsidian的插件仓库中安装一个叫==**git**==的插件。
我们然后把这个下面几个设置打开
1. 这个是实现定时同步库的。
> [!warning]

> 这是普通提示内容==***这里就是每1分钟同步一次***==

![](assets/如何使用obsidian做笔记/截屏2026-01-30%2017.29.55.png)
2. 这个是实现开机同步内容
![](assets/如何使用obsidian做笔记/截屏2026-01-30%2017.38.34.png)
# 2.图像存储功能的使用
我们下载第三方插件==Custom Attachment Location== 然后进行下面设置：

![](assets/如何使用obsidian做笔记/截屏2026-01-30%2017.41.45.png)
然后在这里的==Markdown URL==中输入内容
```text
assets/${noteFileName}/${generatedAttachmentFileName}
```

![](assets/如何使用obsidian做笔记/截屏2026-01-30%2017.42.17.png)
之后在==文件与链接==中关闭==使用Wiki链接== 并把==内部链接类型==改成==基于当前笔记的相对路径==。
![](assets/如何使用obsidian做笔记/截屏2026-01-30%2017.45.06.png)
# 3.修改导出格式
下载第三方插件==Enhancing Export== 
> [!warning]

> 我们提前需要下载好pandoc,我们可以在
```http
https://github.com/jgm/pandoc
```
>下载相应的可执行程序，然后把可执行程序的文件位置添写在这里
>![](assets/如何使用obsidian做笔记/截屏2026-01-30%2017.52.33.png)

# 4. 如何使用Claude code
## 4.1 下载相应的插件
用下面的链接：
```http
https://github.com/YishenTu/claudian
```
按照教程把这个插件放在
```
.obsidian/plugins/
```
## 4.2 进行环境配置
我们主要是配置着插件的环境：
这里的环境[2.2 进行Claude code配置](AI学习/如何使用Claude%20code.md#2.2%20进行Claude%20code配置)里的火山引擎的那个。
![](assets/如何使用obsidian做笔记/截屏2026-02-05%2017.36.08.png)