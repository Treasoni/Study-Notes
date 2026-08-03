# Debian 最小化安装后 sudo 权限配置 - 意图文件

## 基本信息

- **主题**: Debian 最小化安装后 sudo 权限配置
- **项目标识**: debian-practice
- **创建时间**: 2026-08-03
- **当前阶段**: 阶段 0（意图澄清）
- **输出目标**: obsidian
- **Vault 路径**: C:\note\Study-Notes
- **笔记目录**: 项目实战/debian实战
- **MOC 路径**: 待定（可后续补）

## 学习目标

### 笔记类型
实战笔记

### 学习深度
上手

### 用户基础
有了解

## 研究计划

### 探索方向
1. sudo 权限配置的标准流程与命令原理（`su -` vs `su`、`apt install sudo`、`usermod -aG sudo`、sudo 组机制）
2. visudo 高级配置与 sudoers 语法（`NOPASSWD`、`%sudo` 组规则、安全最佳实践）
3. 常见问题排查（用户不在 sudo 组、`/etc/sudoers` 缺失用户规则、%sudo 行被注释、sudoers 语法错误导致 sudo 失效）

### 重点收集
- **核心概念**: sudo 与 su 的区别、`/etc/sudoers` 配置、sudo 用户组、visudo 编辑机制、sudoers 语法（`user host=(runas) command`）
- **实战代码**: `su -`、`apt update && apt install sudo -y`、`usermod -aG sudo your_username`、`sudo whoami` 验证、visudo 免密配置、排错场景直接写入用户规则
- **常见坑**: sudoers 语法错误会导致全部 sudo 失效；`%sudo` 行被注释；用户组变更需重新登录生效；Debian 最小化安装默认无 sudo；`su` 不带 `-` 不加载完整环境变量；必须用 `visudo` 而非 vim/nano 直接编辑
- **工具链**: Debian / apt、visudo、nano / vim、`/etc/sudoers`

### 信源偏好
- 官方文档: 是（Debian wiki、`man sudoers`、`man visudo`）
- 技术博客: 是
- 社区讨论: 是（Ask Ubuntu / Stack Overflow / Unix SE）
- 学术论文: 否

## 备注

- 素材基础来自用户提供的完整实战流程（含 `zhq 未出现在 sudoers 文件中` 排错案例），需在阶段 1-2 用官方文档和社区资料验证、补充原理与边界情况。
- 最终笔记发布到 vault 内 `项目实战/debian实战/`，MOC 待用户后续确认。
