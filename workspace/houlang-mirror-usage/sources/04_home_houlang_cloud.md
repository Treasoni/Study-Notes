---
url: "https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror"
title: "如何使用新版 HLmirror - 厚浪云｜知识库"
scraped_at: 2026-09-13T16:04:45+00:00
---

[Administrator](https://home.houlang.cloud/authors/jacopo "Administrator")
发布于 2026-03-31 / 3,581 阅读
# 如何使用新版 HLmirror
# 加入厚浪云用户群反馈问题：[230832864](https://qm.qq.com/q/pU0B3xXJba)
> 新版 HLmirror 将原有 Cloudflare 节点全部替换为了厚浪云自有节点，增加了国内缓存加速。
> 以下为使用教程
## 首次使用
访问 [mirror.houlang.cloud](https://mirror.houlang.cloud/) 进行登录注册
mirror.houlang.cloud 网页截图
## 添加令牌
在“访问令牌”选项卡中新建令牌
在 HLmirror 新建访问令牌
创建令牌后会得到令牌和登录命令
HLmirror 新建令牌成功页
## 登录机器
复制登录命令到需要拉取镜像的机器进行登录，本文以 Ubuntu 服务器为例
在 Ubuntu 服务器登录 HLmirror
看到“ _Login Succeeded_ ”即代表登录成功，后续可通过 HLmirror 高速拉取镜像
## 拉取镜像
HLmirror 支持 Docker Hub、GHCR 等多个镜像源，通过后缀区分。  
| 上游  | 后缀代号  | 替换地址  |  
| --- | --- | --- |  
|  Docker Hub  | dh  |  mirror.houlang.cloud/dh/  |  
| Google Container Registry  | gcr  | mirror.houlang.cloud/gcr/  |  
| Github Container Registry  | ghcr  | mirror.houlang.cloud/ghcr/  |  
| NVDIA NGC  | nvcr  | mirror.houlang.cloud/nvcr/  |  
| Kubernetes Registry  | k8s  | mirror.houlang.cloud/k8s/  |  
| Microsoft Container Registry  | mcr  | mirror.houlang.cloud/mcr/  |  
| Elastic Docker Registry  | elastic  | mirror.houlang.cloud/elastic/  |  
| registry.gitlab.com  | gitlab  | mirror.houlang.cloud/gitlab/  |  
| Quay  | quay  | mirror.houlang.cloud/quay/  |  
将你原有的镜像地址替换为 HLmirror 即可高速拉取！
### 示例
#### 以 ghcr 为例👇
原镜像地址：ghcr.io/immich-app/immich-server:v2.6.1
替换为 HLmirror：mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
拉取命令示例：docker pull mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
#### 以 Docker Hub 为例👇
原镜像地址：library/nginx:latest
替换为 HLmirror：mirror.houlang.cloud/dh/library/nginx:latest
拉取命令示例：docker pull mirror.houlang.cloud/dh/library/nginx:latest
# 分享
https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror
复制
