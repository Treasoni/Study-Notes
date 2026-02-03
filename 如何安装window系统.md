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
## 1.1 删除分区，快速分区
把U盘插入到电脑中，我们进入到FirPE中，把这台电脑的之前的分区进行格式化
> [!warning]

> ⚠️ 用重要内容注意备份。

然后进行快速分区