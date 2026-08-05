# 第 7 章：排错——sudo command not found 与 sudoers 损坏恢复

第 6 章解决的是「授权没配上」的故障；本章处理剩下两类更「硬」的问题：`sudo: command not found`（命令本身不存在）和 sudoers 文件损坏（配置坏了导致 sudo 直接罢工）。前者多半是包没装，后者是配置被改坏，两者都需要先从 sudo 之外拿到 root 才能修复。

## 7.1 sudo not found 的根因区分

`sudo: command not found` 看起来简单，但根因有两种，别急着改 PATH。先做一个关键判定：看 `/usr/bin/sudo` 到底存不存在 [linuxconfig — sudo command not found](https://linuxconfig.org/sudo-command-not-found-solution)。

| 根因 | 现象 | 判定方式 |
| --- | --- | --- |
| sudo 包未安装 | `/usr/bin/sudo` 不存在 | 最小化安装（Docker 镜像、VPS 初始系统）最常见 |
| 包已装但 PATH 缺 `/usr/bin` | `/usr/bin/sudo` 存在 | `which sudo` 找不到但文件在 |

```bash
ls -l /usr/bin/sudo
# 报 No such file or directory → 没装包，走下面的修复
# 有输出 → 包在，才去查 echo $PATH 是否含 /usr/bin
```

确认是没装包后，按第 3 章的路径修复（前提是掌握 root 密码）：

```bash
su -                          # 切 root，必须带 -（加载完整环境）
apt update && apt install sudo -y    # apt update 必须先于 install
usermod -aG sudo <你的用户名>   # Debian 系加入 sudo 组
su - <你的用户名>               # 切回普通用户
sudo whoami                   # 输出 root 即成功
```

注意 `<你的用户名>` 要替换成实际用户名；`apt update` 必须先跑，否则可能装到过期索引而失败 [linuxconfig](https://linuxconfig.org/sudo-command-not-found-solution)。

## 7.2 sudoers 损坏的症状与恢复分级

「not found」是包没装，而 sudoers 损坏是「装好了但配置坏了」——通常由**绕过 visudo 直接编辑 `/etc/sudoers`**（用 vim/nano）或**误改权限**引起。损坏后 sudo 一启动就报三段式错误 [Unix & Linux SE — sudoers 损坏恢复](https://unix.stackexchange.com/questions/650920/)：

```text
sudo: /etc/sudoers is world writable
sudo: no valid sudoers sources found. quitting
sudo: unable to initialize policy plugin
```

`is world writable` 指权限过宽。sudoers 的标准权限是 **0440、属主 root:root**；`/etc/sudoers.d/` 目录本身是 775，目录里的 `README` 是 440。

这段错误出现时，**sudo 已经完全不可用**——连 `sudo visudo` 都起不来。要修复，必须先通过 sudo 之外的方式拿 root，按可用手段分级：

| 级别 | 前提 | 做法 |
| --- | --- | --- |
| ① | root 密码已知 | `su -` 切 root → `chmod 440 /etc/sudoers` |
| ② | 系统有 polkit | `pkexec bash`（或 `pkexec chmod 0440 /etc/sudoers`） |
| ③ | 以上都没有 | Live CD / 安装盘启动，挂载根分区到 `/mnt`，`chmod 440 /mnt/etc/sudoers`；云主机可拆盘挂到别的机器修 |

两个细节要注意：

- 走 ② 时，SSH 场景通常需要**双终端**：先在一个终端跑 `pkttyagent` 注册 polkit 会话，再在另一个终端跑 `pkexec`，否则会报 polkit session cookie 错误。
- 走 ③ 时，`/mnt` 换成你实际挂载根分区的目录，文件路径对应写成 `/mnt/etc/sudoers`。

修好权限回到正常系统后，必须校验一次才能确认真的恢复了：

```bash
sudo visudo -c
# /etc/sudoers: parsed OK
```

只有输出 `parsed OK` 才算修好，否则 sudo 可能再次罢工。这两类故障的共同源头是「绕过 visudo 直接碰 sudoers」——visudo 提供排他锁、保存时语法校验和错误回滚，是唯一安全的编辑方式 [Unix & Linux SE](https://unix.stackexchange.com/questions/650920/)。

## 本章小结

- `sudo: command not found` 先判 `ls /usr/bin/sudo`：文件不存在→没装包；文件在→才查 PATH。
- 修复路径：`su -` → `apt update && apt install sudo` → `usermod -aG sudo <用户>` → `sudo whoami`。
- sudoers 损坏的三段式错误（world writable / no valid sources / policy plugin）出现时，sudo 已完全不可用。
- 标准权限 0440、root:root；恢复分级：`su -` → `pkexec` → Live CD/挂盘。
- 修复后必跑 `sudo visudo -c`；永远用 visudo 编辑 sudoers，别用 vim/nano 直接改。

下一章（最后一章）把第 3 到第 7 章的命令串成一张从最小化安装到安全使用 sudo 的总结清单，并沉淀安全最佳实践。
