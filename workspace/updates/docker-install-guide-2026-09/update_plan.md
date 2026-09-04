# Update Plan — Linux Docker 安装指南（国内网络版）

- 目标文件：`docker/Linux-Docker与DockerCompose安装指南-国内网络版.md`
- 落盘方式：就地 patch 原笔记（用户已确认）
- 更新日期：2026-09-04
- 核验：官方源（docker docs raw / GitHub releases / Aliyun Packages.gz）+ 社区实测（SMZDM 2026-08-15 / status.anye.xyz / dongyubin/DockerHub），双 agent 核验

## Stale Map

### A. 版本号（过时）
| 位置 | 旧值 | 新值 | 依据 |
| --- | --- | --- | --- |
| Engine 示例/预期输出多处 | 29.7.1 | 29.8.0（2026-09-03 发布） | moby/moby docker-v29.8.0 |
| apt noble 版本串 | `5:29.7.1-1~ubuntu.24.04~noble` | `5:29.8.0-1~ubuntu.24.04~noble` | Aliyun noble stable Packages.gz |
| rpm el9 版本串 | `3:29.7.1-1.el9` | `3:29.8.0-1.el9` | Aliyun el9 Packages |
| Compose | v5.4.0 | v5.5.1（2026-09-03） | docker/compose latest |

### B. apt 密钥方法（旧方法 → 官方新流程）
- `gpg --dearmor` 存 `/etc/apt/keyrings/docker.gpg`、预装 `gnupg` → 官方改为直接存 ASCII `/etc/apt/keyrings/docker.asc`（`sudo curl -fsSL .../gpg -o .../docker.asc`），不再需要 gnupg。
- 涉及：ch2 §1 前置依赖、ch2 §2 密钥、deb822 `Signed-By`、`docker.list` 兼容写法、ch8 apt 速查。

### C. RHEL/CentOS el10 路径（说法过严）
- 「el10 必须走 `linux/rhel/`」→ 官方现按发行版：RHEL 8/9/10 → `linux/rhel`；CentOS 家族 → `linux/centos`。两目录 el8/el9/el10 均有同版本包（阿里云已同步）。Rocky/Alma 为 RHEL 再编译版，官方不再单列。
- 涉及：ch3 §6 表格与规则、ch3 小结、ch8 dnf 速查。

### D. 镜像加速源（2026-09 校准）
- `docker.1ms.run`：存活，但大陆直连偏慢、个别环境 DNS 不稳（排错笔记 08-28）→ 保留但注明。
- `docker.xuanyuan.me`：免费档 429 限流 / 离线波动 → 降为备选。
- `docker.m.daocloud.io`：存活且最稳 → 主推。
- `docker.1panel.live`：存活，地域相关 → 保留。
- 新增候选（需实测）：`docker.jiaxin.site`、`dockerproxy.net|.link`。
- 失效源清单维持不变。
- 涉及：ch5 §2/§3/§5、ch5 小结、ch8 §4/§5/§6/小结。

### E. 链接
- ch8 §7 官方文档：拆出独立 CentOS 安装页链接（`docs.docker.com/engine/install/centos/`）。
- ch5 §3 增加 2026-09 参考：SMZDM 实测、status.anye.xyz 监控。

### F. 其他方法修正
- ch4 §2 插件安装命令补 `dnf` 变体（原文用 yum 代指 dnf 系，易误导）。

### G. 元数据
- frontmatter `updated` → 2026-09-04；文末追加 `## 更新记录`。

## 保留不动
- deb822 `.sources`、5 件套包清单、standalone URL、GPG epoch 格式（apt `5:` / rpm `3:`）、sed 换源、daemon.json 语法、vault/故障排查章节结构与风格。
