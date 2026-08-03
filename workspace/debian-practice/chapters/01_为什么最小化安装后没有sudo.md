# 第 1 章：为什么最小化安装后没有 sudo

**结论先行**：Debian 最小化安装默认没有 sudo，这不是故障，而是安装器依据「root 密码是否留空」做出的设计选择。先弄清分叉规则，才能判断自己的系统属于哪条路、下一步该怎么走。

## 1.1 Debian 最小化安装的两种行为分叉

Debian Wiki 明确区分两种安装行为 [Debian Wiki — sudo](https://wiki.debian.org/sudo)：

- **root 密码留空**：sudo 自动安装，且安装时创建的普通用户已加入 `sudo` 组，装完即开箱即用，无需额外配置。
- **root 密码已设置**：sudo 不会被安装，可选创建的普通用户也不在 `sudo` 组，需手动三步配置（第 3 章展开）。

两者的本质区别：留空 root 密码，系统默认信任「首个用户」为管理员，把提权工具与授权一次配好；显式设置 root 密码，管理权默认交给 root，普通用户不自动获得任何提权能力。

**`sudo: command not found` 的根因**

最小化安装（Docker 镜像、VPS 初始系统）多属第二种情况，且往往连普通用户都没创建。此时输入 `sudo` 会直接报：

```plaintext
sudo: command not found
```

根因是 `/usr/bin/sudo` 这个二进制根本没有安装，而不是 PATH 缺目录 [linuxconfig — sudo command not found](https://linuxconfig.org/sudo-command-not-found-solution)。遇到 `command not found`，第一反应应是「命令是否存在」，而非「路径里有没有」。

## 1.2 笔记目标与整体路径

本笔记的目标：**让普通用户在最小化 Debian 上获得安全可用的 sudo 权限**。学完能独立跑通「安装 sudo → 加组授权 → 验证」全链路，会用 `visudo` 做安全精细授权，并排查三类最常见的 sudo 故障。

整体路径分五段：

1. **原理**（第 2 章）：`su` vs `su -`、sudo 的定位、Debian `sudo` 组机制
2. **标准配置**（第 3 章）：手动三步安装与授权
3. **进阶语法**（第 4-5 章）：visudo、sudoers 条目、免密（可选）
4. **排错**（第 6-7 章）：三类常见故障与恢复
5. **安全总结**（第 8 章）：最佳实践与速查清单

下一章先补原理——`su` 与 `su -` 的差别、为什么「加组后还要重新登录」。不弄清这两点，第 3 章的标准配置每一步都会踩坑。
