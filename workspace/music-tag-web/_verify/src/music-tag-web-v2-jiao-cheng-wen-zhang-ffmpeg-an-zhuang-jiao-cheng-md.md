> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/ffmpeg-an-zhuang-jiao-cheng.md).

# ffmpeg安装教程

ffmpeg安装后可用于本项目中音乐转码和整轨音乐分割

查看ffmpeg是否安装

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2Fak8jMncJhRGiWJRCfUyP%2Fimage.png?alt=media&amp;token=40d5c622-cbdd-442d-aa17-9862a0e228c6" alt=""><figcaption></figcaption></figure>

1. 下载ffmpeg

进入<https://johnvansickle.com/ffmpeg/> 页面，右侧选择一个属于自己计算机的架构的版本，一般是amd64或arm64

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FbIcjbNj11JUN169YdG2u%2Fimage.png?alt=media&amp;token=2440166e-ea17-44a8-b06e-0167d9c7ef4f" alt=""><figcaption></figcaption></figure>

怎么查看自己计算机是什么架构的？\
*要查看您的电脑是基于AMD64（也称为x86\_64）架构还是ARM64（也称为aarch64）架构，您可以通过以下几种方法之一进行检查：*

*Windows 操作系统 使用“系统”设置：*&#x20;

*打开“开始”菜单。 点击“设置”图标（齿轮形状）。 选择“系统” > “关于”。 在“设备规格”下查找“系统类型”。这里会列出您的处理器架构（如32位操作系统或64位操作系统，以及是否为x86或ARM）。*&#x20;

*使用命令提示符或PowerShell： 打开命令提示符或PowerShell。*&#x20;

*输入 wmic os get osarchitecture 并按下回车键。这将显示操作系统的架构。 或者输入 systeminfo 命令，然后在输出中查找 "System Type" 一行。*&#x20;

*macOS 操作系统 打开“关于本机”（点击屏幕左上角的苹果图标，然后选择“关于本机”）。 在弹出的窗口中，您可以看到有关处理器的信息。如果它说“Apple芯片”，那么这是ARM架构；如果是Intel，则是x86架构。*

&#x20;*Linux 操作系统 使用终端命令： 打开一个终端窗口。 输入 uname -m 并按下回车键。对于AMD64架构，这将返回 x86\_64；对于ARM64架构，这将返回 aarch64*

2. 解压缩包

解压后找到ffmpeg的文件，只需要这个一个文件

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FSAHAnw0PXlu73eg6PJ4w%2Fimage.png?alt=media&amp;token=7883ed12-62c8-49b0-ae16-fbe6eaac9dfc" alt=""><figcaption></figcaption></figure>

3. 复制或移动到该项目文件夹下

你在部署项目时候挂在出来的/aap/data 对应本地计算机的目录

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FZZABddnD4vQPMfgNhlnN%2Fimage.png?alt=media&amp;token=c62f4b26-3ff9-4b19-9622-6f9c971861ee" alt=""><figcaption></figcaption></figure>

例如你的地址是 /volume/music\_tag\_web/data 在此目录下新建 bin目录（如果不存在的话）\
最终地址是：/volume/music\_tag\_web/data/bin

将上面解压后的ffmepg 移动到 /volume/music\_tag\_web/data/bin 下面\
最终ffmpeg地址是：/volume/music\_tag\_web/data/bin/ffmpeg

4. 给ffmpeg一个执行权限

同样在 /volume/music\_tag\_web/data/bin/ 目录下，执行下面命令

chmod +x ffmpeg

完成后系统信息里就显示ffmpeg的版本了，就完成安装了

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FMB6Z5HE1H3LStsLUOIuO%2Fimage.png?alt=media&amp;token=7b319de1-d68b-49a7-b4ed-533fc413da01" alt=""><figcaption></figcaption></figure>
