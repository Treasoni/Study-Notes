这里我是打算用WinPE的方式进行安装。[WinPE](PVE的学习/WinPE.md)

前提准备：
- 一个刷了ventoy的U盘[1.3Ventoy（最灵活）](PVE的学习/写盘工具.md#1.3Ventoy（最灵活）)
- window的iso镜像
```http
https://www.microsoft.com/zh-cn/software-download/windows10ISO
```
- FirPE的iso镜像。
```HTTP
https://www.firpe.cn
```

# 1. 具体过程
## 1.1 删除分区
把U盘插入到电脑中，我们进入到FirPE中，把这台电脑的之前的分区进行格式化
> [!warning]

> ⚠️ 用重要内容注意备份。

## 1.2 转换分区格式
我们的分区表类型一般为：
- MBR
- GPT（新电脑一般用这个）
![](assets/如何安装window系统/截屏2026-02-03%2019.03.05.png)
## 1.3 快速分区
![](assets/如何安装window系统/截屏2026-02-03%2019.05.26.png)
- 这里的分区表类型就是你之前转换的类型
- 分区数量看你自己需求，一般是两个
- ==**高级设置**==中我们对分区的大小进行划分，这里的系统分区就是我们之后电脑的c盘，看自己需求划分。
## 1.4 重启
完成上面操作后就是重启，在ventoy界面中选择自己已经下好的window镜像。

# 2. 安装window系统
这里我就不详细说了，重要的是我们是把**window系统**安装在我们之前选中的**系统分区**。
![](assets/如何安装window系统/截屏2026-02-03%2019.08.44.png)