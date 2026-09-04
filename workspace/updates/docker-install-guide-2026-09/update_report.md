# Update Report — Linux Docker 安装指南（国内网络版）

- 目标文件：`docker/Linux-Docker与DockerCompose安装指南-国内网络版.md`
- 更新方式：就地 patch（用户确认：全部 4 类 / patch-in-place）
- 更新日期：2026-09-04
- 关联计划：`update_plan.md`

## 变更摘要

### A. 版本号（29.7.1 → 29.8.0；Compose v5.4.0 → v5.5.1）
- 第二章 apt 示例：`5:29.8.0-1~ubuntu.24.04~noble`、madison 历史示例 `5:29.7.2-1`、pin/锁版本命令同步。
- 第三章 rpm 示例：`3:29.8.0-1.el9`、`3:29.7.2-1.el9`。
- 第四章/第六章：Compose v5.5.1、`29.8.0` 输出示例。

### B. apt 密钥方法（gnupg + dearmor → 官方 `.asc` 直存）
- 第二章 §1 前置依赖去掉 `gnupg`（`ca-certificates curl`），相关正文/标题/本章小结同步。
- 密钥命令改为：`curl -fsSL .../gpg -o /etc/apt/keyrings/docker.asc` + `chmod a+r`。
- deb822 `Signed-By`、`.list` 兼容写法、第八章速查卡全部改 `docker.asc`。
- 保留说明：旧 `docker.gpg` + dearmor 仍兼容但已非官方主推。

### C. RHEL/CentOS el10 路径规则
- 第三章 §六表格与规则已改为：CentOS 家族 → `linux/centos/`，RHEL/Rocky/Alma → `linux/rhel/`，两目录均发布 el8/el9/el10。
- 第八章 dnf 速查注释与「路径分水岭」要点同步。

### D. 镜像加速源（2026-09 校准）
- daemon.json 推荐组合改为 `DaoCloud / 1Panel / 毫秒`（原 `毫秒/轩辕/DaoCloud/1Panel` 去掉轩辕免费档）。
- 轩辕免费档近期 429 限流/离线波动 → 降为备选；新增候选 简行 `docker.jiaxin.site`、DockerProxy `dockerproxy.net|.link`（需实测）。
- `docker info` 预期输出、第五章与第八章清单/小结同步。
- 失效源清单维持不变。

### E. 链接与参考
- 第五章 §3 增加 2026-09 参考：status.anye.xyz 存活监控、SMZDM 2026-08-15 实测。
- 第八章官方文档拆出独立 CentOS 安装页。

### F. 其他
- 第四章 compose-plugin 安装补 dnf 变体。
- 文末追加 `## 更新记录`（2026-09-04）。

## 来源（核验基准）

- 官方：Docker Engine install docs（Ubuntu/Debian/RHEL/CentOS）、docker/compose GitHub latest、moby/moby docker-v29.8.0 tag。
- 仓库元数据：阿里云 docker-ce 源 `Packages.gz` / RPM Packages（noble stable / el9 stable）确认版本串与 epoch。
- 镜像源实测：
  - [容器镜像监控 status.anye.xyz](https://status.anye.xyz/)
  - [SMZDM：实测 26 个加速地址（2026-08-15）](https://post.smzdm.com/p/anvq683p/#1)
  - [SMZDM：实测 15 个国内 Docker 镜像源（2026-08-20）](https://post.smzdm.com/p/am9xe69k/#1)
  - vault 内实况：`docker/docker镜像拉取DNS解析超时排错`（2026-08-28，1ms.run DNS 实例）、`DockerDesktop镜像加速器配置` 等姊妹笔记。

## 双链 / MOC 检查

- 笔记内双链目标全部存在（镜像加速器vs代理-概念对比、DockerDesktop镜像加速器配置、Windows-DockerDesktop安装指南-国内网络版）。
- `docker/Docker MOC` 中本笔记索引项描述仍准确，无需改动。

## 未处理风险 / 后续建议

1. 姊妹笔记仍含部分旧信息，本次未改（如需请走批量更新流程）：
   - `docker/镜像加速器vs代理-概念对比`（轩辕免费档仍按头号源展示、dearmor 相关说明段落）。
   - `docker/DockerDesktop镜像加速器配置`（08-08 版本，可用源顺序可再校准）。
   - `docker/docker镜像拉取DNS解析超时排错`（保留其原始事故配置作为教学现场，属合理）。
2. 镜像加速源属高时效信息，公共免费源随时可能限流/停服；建议按月参考 status.anye.xyz 复核。
3. Docker Engine 每两周左右发版，示例版本号会再次过期；后续更新可只改版本串。
