# 如何让 Docker 容器内部的服务控制/处理容器外或宿主机的文件 - 意图文件

## 基本信息

- **主题**: 如何让 Docker 容器内部的服务控制/处理容器外或宿主机的文件
- **项目标识**: docker-container-host-file-access
- **创建时间**: 2026-08-29
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: 待指定（发布前确认，如 `Notes/Docker`）
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
实战笔记

### 学习深度
上手（掌握核心方案，能解决实际问题）

### 用户基础
有了解（用过 docker run / docker compose，知道基本概念）

## 研究计划

### 探索方向
1. 绑定挂载（bind mount）与命名卷（named volume）：如何把宿主机目录挂载进容器，让容器内服务读写
2. 权限映射：UID/GID、`--user`、user namespace remap、rootless 下的文件属主问题
3. 安全边界：只读挂载（ro）、SELinux/AppArmor（`:z`/`:Z`）、挂载 Docker socket 的风险
4. 替代方案：通过 Docker API/socket 控制宿主、网络服务转发、外部共享目录同步

### 重点收集
- **核心概念**: bind mount、named volume、volume、tmpfs、UID/GID 映射、user namespace、read-only 挂载、docker socket
- **实战代码**: `docker run -v` / `--mount`、docker compose `volumes:`、`--user`、`chown`/`chmod`、userns-remap 配置
- **常见坑**: permission denied、root 与宿主文件属主错乱、Docker Desktop（macOS/Windows）挂载性能与路径差异、SELinux 标签、符号链接路径解析
- **工具链**: Docker Engine、Docker Compose、Podman、Portainer

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户最初问题是「容器内服务如何控制/处理容器外或宿主机文件」，笔记以实战场景（读、写、权限、安全）为主线。
- 输出到当前 vault `D:\Study-Notes`；最终 note_folder、moc_path 在阶段 6/7 前确认。
