---
title: 厚浪镜像（HLmirror）使用指南 —— 从机制到实操
created: 2026-09-14
updated: 2026-09-14
tags: [docker, 镜像加速, HLmirror, 厚浪镜像, 前缀重写, registry-mirrors, containerd, k8s, 排错]
status: 已完成
source_project: houlang-mirror-usage
sources:
  - "https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror"
  - "https://docs.docker.com/docker-hub/image-library/mirror/"
  - "https://docs.docker.com/reference/cli/dockerd/"
  - "https://docs.docker.com/engine/daemon/proxy/"
  - "https://containerd.io/docs/1.7/hosts/"
  - "https://kubernetes.io/docs/concepts/containers/images/"
  - "https://docs.daocloud.io/community/mirror/"
  - "https://github.com/moby/moby/issues/42022"
---

# 厚浪镜像（HLmirror）使用指南 —— 从机制到实操

## 目录

- 第 1 章 它到底是什么 —— 前缀重写式加速器
  - 1.1 一句话定位：它是什么，现在是什么状态
  - 1.2 三类镜像加速的机制分野（核心概念节）
  - 1.3 为什么它填不进 daemon.json 的 registry-mirrors（本笔记核心论点）
  - 1.4 拉取时到底发生了什么：缓存、回源与 digest 校验
  - 1.5 凭据流向：为什么前缀重写在账号安全上更干净
  - 1.6 服务条款现状，以及本章的素材边界
  - 1.7 同类方案对照：前缀重写的两种写法
- 第 2 章 怎么用 —— 从注册到 docker pull
  - 2.1 全链路总览
  - 2.2 第一步：注册与登录控制台
  - 2.3 第二步：创建访问令牌
  - 2.4 第三步：在目标机器上 docker login
  - 2.5 第四步：改写镜像地址（速查核心节）
  - 2.6 第五步：拉取并验证
  - 2.7 场景差异：Linux 服务器 / Docker Desktop / k8s 节点
  - 2.8 速查卡
- 第 3 章 进阶场景与常见坑
  - 3.1 改写代价之一：compose 文件
  - 3.2 改写代价之二：k8s —— manifest 改写 vs containerd hosts.toml
  - 3.3 常见坑 1–5
  - 3.4 私有镜像与鉴权：GHCR 私有仓库
  - 3.5 令牌生命周期：docker logout 与令牌吊销
  - 3.6 配额与限速：只有字段名，没有数字
  - 3.7 排错入口清单

## 第 1 章：它到底是什么 —— 前缀重写式加速器

> 本章受众：已经会用 `docker pull` / `docker login`，但还没搞清楚厚浪镜像到底属于哪一类加速服务的人。

如果你的 Docker 知识是从「改 `daemon.json` 里的 `registry-mirrors`」这件事学起的，那么看到厚浪镜像的第一反应很可能是：**它能不能填进那个配置里？** 答案是不能，而且不是「暂时不能」，是机制上根本不成立。

问题出在「镜像加速器」这个词已经被用烂了。它现在至少指三种机制完全不同的东西，而中文笔记里普遍把它们混为一谈。本章的任务不是教你怎么配（那是第 2 章），而是先把这三个物种分开，然后逐个回答：厚浪是哪一类、它为什么填不进 `daemon.json`、它拉取时在背后做了什么、它在账号安全上有什么不同、以及它当前的边界在哪里。

> [!note] 本章不涉及的内容
> 注册、建令牌、`docker login`、`docker pull` 的完整实操在第 2 章；compose / k8s 的改写代价与常见坑在第 3 章。本章只建立机制认知。

---

### 1.1 一句话定位：它是什么，现在是什么状态

官方的自我定位非常短，只有一句话，且说得比营销文案实在：

> 新版 HLmirror 将原有 Cloudflare 节点全部替换为了厚浪云自有节点，增加了国内缓存加速。
> <!-- C15 -->（[《如何使用新版 HLmirror》](https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror)，2026-03-31）

这句话交代了两件事，都是事实层面的：**节点从 Cloudflare 换成了自有节点**（线路归属变了），**增加了国内缓存**（有本地回源缓存这一层）。它没说「能加速哪些上游」——那部分要靠后面 1.2 与第 2 章的后缀表补。

产品页另外给了一个时间锚点：

> 🎉 上线于2024年6月9日，HLmirrors为国内用户提供优质的镜像加速服务
> <!-- S5 -->（[厚浪云 HLmirrors 产品页](https://houlang.cloud/zh-CN/article/products/hlmirror)）

也就是说，这是一项 2024 年年中上线、2026 年初做过一次节点改造的**仍在运营中**的服务，不是那种「教程还在、服务已死」的过期加速地址。

#### 一个必须提前澄清的混淆点

同一张产品页上还挂着另一个服务，长得极像，但**和 Docker 镜像毫无关系**：

> ## 🌐 通用镜像
> - 🔗 镜像地址：[all.hlmirror.com](https://all.hlmirror.com)
> <!-- C23 -->（同上产品页）

`all.hlmirror.com` 是**网页镜像**（把国外网页内容代理回国内），不是容器镜像仓库。它的名字里带 `mirror`、域名里带 `hlmirror`，所以搜「厚浪 镜像」时很容易和 `mirror.houlang.cloud` 撞在一起。记法很简单：**带 `cloud` 的是给 Docker 用的，带 `.com` 的是给浏览器用的。**

顺带一提，系统状态页里 `all.hlmirror.com` 恰好和 Docker 镜像被放在同一个「HLmirror」分组下：

> ## HLmirror
> <!-- C24 -->（[厚浪云系统状态页](https://status.houlang.cloud/status/system)）

这个分组是本章少有的**可自行观测的入口**——服务是否在线，可以自己去看，不必依赖第三方说法。

#### 使用方式：官方只给了三步

官方教程「首次使用 / 添加令牌 / 登录机器」三节 <!-- C16 --> 描述的是：**注册登录站点 → 在「访问令牌」选项卡新建令牌 → 把生成的登录命令复制到目标机器上执行**。这三步之后才是手动改写镜像地址去 `docker pull`。

注意这三步里**没有一步是「修改配置文件」**。这一点很关键，它是 1.2 与 1.3 的伏笔。

> [!tip] 大白话
> 厚浪不是给你的 Docker 装一根新管道，而是**给你换了一个取件地址**。管道（网络线路）它确实优化了，但你和 Docker 之间没有任何配置被改写——你只是把「我要去 `ghcr.io` 拿货」改口说成「我要去 `mirror.houlang.cloud/ghcr/` 拿货」。理解这一点，后面所有「为什么不能填进配置里」的问题都会自动有答案。

---

### 1.2 三类镜像加速的机制分野（核心概念节）

「镜像加速器」在 2026 年至少指下面三类东西。它们的配置位置、覆盖范围、以及**你为此要付出的代价**完全不同：

| 类型                        | 典型形态                            | 配置位置                                                                                                                       | 覆盖哪些上游                                                                   | 你的凭据流向                                 | 对文件改动的要求                                     |
| ------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------- | -------------------------------------------- |
| **原地镜像**（registry mirror） | `registry-mirrors`              | `daemon.json` 的 `registry-mirrors` 键，或启动 dockerd 时的 `--registry-mirror` 参数 <!-- C4 --> / Docker Desktop 的 Docker Engine 设置 | **仅 Docker Hub** <!-- C1 -->                                             | Hub 凭据会被发给镜像站 <!-- C6 -->              | 配置一次，**所有 `docker pull` 自动生效**，不用改任何镜像地址     |
| **HTTP/HTTPS 代理**         | `HTTP_PROXY` / `HTTPS_PROXY`    | 守护进程启动环境变量；systemd 场景用 drop-in 文件 <!-- C26 -->                                                                             | **Docker Hub 及其他 registry** <!-- C25 -->                                 | 取决于代理是否做 TLS 中间人（通用机制推断）               | 配置一次，全局生效                                    |
| **前缀重写**（本笔记主角）           | `mirror.houlang.cloud/{后缀}/...` | **不配置任何东西**                                                                                                                | Docker Hub、GCR、GHCR、nvcr、k8s、mcr、elastic、gitlab、quay（共 9 个） <!-- C19 --> | 你主动 `docker login` 到镜像站本身 <!-- C20 --> | **每一处镜像地址都要手改**，compose / k8s manifest 里一个个改 |

> [!note] 关于「代理」一行
> 覆盖范围一列依据 Docker 官方原文 **C25**（"access images stored on Docker Hub **and other registries**"），配置位置依据 **C26**。但「你的凭据流向」一列写的「取决于代理是否做 TLS 中间人」是**通用机制推断**——官方该页并未讨论代理下的凭据可见性，这一格不构成结论。

三类的配置点差异，用写法对照更直观：

```text
# ── 类型 1：原地镜像（registry-mirrors）────────────────────
# 执行位置：目标机器的 /etc/docker/daemon.json
{
  "registry-mirrors": ["https://<某个镜像站>"]
}
# 你照旧写 docker pull nginx，dockerd 在后端把请求改道去镜像站。
# ⚠ 只对 Docker Hub 生效，且改道时会把你的 Hub 凭据一并带过去。

# ── 类型 2：代理（HTTP_PROXY / HTTPS_PROXY）────────────────
# 执行位置：dockerd 进程的环境变量或 systemd 单元
HTTPS_PROXY=http://127.0.0.1:7890
# 请求整体走代理通道出去，镜像地址本身一个字都不用改。

# ── 类型 3：前缀重写（厚浪这一类）──────────────────────────
# 执行位置：不配置，直接改你要拉的那个地址
原：ghcr.io/immich-app/immich-server:v2.6.1
改：mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
```

三者的取舍可以浓缩成一句：**类型 1 和 2 是「配一次、管全局」，代价是覆盖面窄（类型 1）或有额外信任成本（类型 2）；类型 3 是「覆盖面最广，代价是每一处地址都得手改」。** 这个代价在第 3 章会展开——它会直接决定你在 compose 和 k8s 场景下有多痛。

> [!tip] 大白话
> - **registry-mirrors = 把仓库搬到家门口**：仓库还是那一个（只认 Docker Hub），只是换了个近的存放点，你拿货时不用改收货地址。
> - **代理 = 全程绕路中转**：你的车还是开去原来的仓库，只是路上换了一条道走。
> - **前缀重写 = 换前台代收，包裹原样不动**：仓库和货都没变，变的是你填在收件单上的地址。

> [!tip] 相关笔记（本 vault 内）
> - [[镜像加速器vs代理-概念对比]] —— 概念层的两类对照。**注意**：该文把「镜像加速器」等同于 `registry-mirrors`，只覆盖本节三类里的**第一类**；已在其顶部加了订正提示。
> - [[DockerDesktop镜像加速器配置]] —— 第一类（原地镜像）在 Mac / Windows 上的配置实操。
> - [[docker进行代理]] —— 第二类（代理）的两层用法：其 §4.2 讲守护进程代理（对应本节「只影响 `docker pull`」那一层），其余章节讲容器内代理，两者不要混。

---

### 1.3 为什么它填不进 daemon.json 的 registry-mirrors（本笔记核心论点）

这一节只有一个论据，但它是官方的逐字原文，且直接判了死刑。Docker 官方在《Mirror the Docker Hub library》的 Alternatives 一段里写道：

> It's currently not possible to mirror another private registry. Only the central Hub can be mirrored.
> <!-- C1 -->（[Docker Docs · Mirror the Docker Hub library](https://docs.docker.com/docker-hub/image-library/mirror/)）

译：**目前无法镜像另一个私有仓库，只有中心化的 Docker Hub 能被镜像。**

这句话就是「厚浪填不进 `daemon.json`」的根因。把厚浪地址写进 `registry-mirrors`，最多只能让 **Docker Hub 的拉取**换道，而 `ghcr.io`、`quay.io`、`nvcr.io`、`registry.k8s.io`、`mcr.microsoft.com` 这些上游**一个都覆盖不到**——因为它们压根不在 registry mirror 这个机制的作用域里。

两个容易被忽略的细节：

**第一，dockerd 参考页并不会告诉你这件事。** 官方对 `registry-mirrors` 的全部描述只有一句话：

> `registry-mirrors` | Specifies a list of registry mirrors.
> <!-- C5 -->（[Docker Docs · dockerd CLI reference](https://docs.docker.com/reference/cli/dockerd/)）

它**没有**任何「仅限 Docker Hub」的明文。所以如果你只查 dockerd 参考页，会得到一个「这是个通用镜像列表」的错误印象。**论据必须落在 C1（镜像专页），不能落在 C5（CLI 参考页）。**

**第二，就算真的配了镜像站，也不豁免于 Docker 的政策。** 同一页还有一句：

> Mirrors of Docker Hub are still subject to Docker's fair use policy.
> <!-- C2 -->（同上 Docker Docs 页面）

译：Docker Hub 的镜像仍然受 Docker 公平使用政策约束。也就是说，**镜像站不是「绕过限制」的通道**，它自己也是被约束的一方。

那厚浪这类服务的正确用法是什么？官方教程的措辞非常明确：

> 将你原有的镜像地址替换为 HLmirror 即可高速拉取！
> <!-- C18 -->（[《如何使用新版 HLmirror》](https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror)）

注意是**替换地址**，不是**配置镜像源**。这两个动作在字面上只差几个字，在机制上是两种东西。

把错误预期和实际用法并排放一次：

```text
# ❌ 错误预期：以为这样就能让 GHCR 走厚浪
# 执行位置：目标机器 /etc/docker/daemon.json
{
  "registry-mirrors": ["https://mirror.houlang.cloud"]
}
# 实际结果：按 C1，registry-mirrors 只处理 Docker Hub。
#          docker pull ghcr.io/immich-app/immich-server:v2.6.1 的地址
#          不会被改写到厚浪，也不会因此变快。

# ✅ 实际用法：不动 daemon.json，改镜像地址本身
原：ghcr.io/immich-app/immich-server:v2.6.1
改：mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
```

> [!warning] 填了会怎样
> 最坏的情况不是「报错」，而是**它看起来能用**——Docker Hub 的镜像确实会走厚浪，于是你以为配对了；等到你去拉一个 GHCR 或 quay 的镜像时，它默默走了公网，你以为「厚浪对 ghcr 支持不好」。这不是支持不好，这是**这条路径压根没被触发过**。

> [!tip] 大白话
> `registry-mirrors` 是**只认 Docker Hub 的专用车道**。你把厚浪的名字写进车道标牌上，车道该只通哪儿还是只通哪儿——标牌写得再对，这辆车也开不进 GHCR 的园区。想让 GHCR 的车进厚浪的园区，唯一办法是**在你的运单上直接写厚浪的门牌号**。

---

### 1.4 拉取时到底发生了什么：缓存、回源与 digest 校验

前缀重写不是「换了个域名转发」这么简单，厚浪这一侧实际扮演的是一个 **pull-through cache（穿透式缓存）**。Docker 官方对这类缓存的机制描述是：

> The first time you request an image from your local registry mirror, it pulls the image from the public Docker registry and stores it locally before handing it back to you. On subsequent requests, the local registry mirror is able to serve the image from its own storage.
> <!-- C3 -->（[Docker Docs · Mirror the Docker Hub library](https://docs.docker.com/docker-hub/image-library/mirror/)）

译：**第一次请求时，它先去公共 Docker registry 拉取并落盘，再交给你；后续请求则由缓存自身直接提供。**

而当你用 **tag**（比如 `:latest`、`:v2.6.1`）去拉的时候，还有一道校验：

> When a pull is attempted with a tag, the Registry checks the remote to ensure if it has the latest version of the requested content. Otherwise, it fetches and caches the latest content.
> <!-- C3 -->（同上）

译：**带 tag 拉取时，Registry 会向远端确认是否已是最新版本，若否就重新拉取并缓存。**

这两句合在一起，解释了一个很多人会误判的现象。缓存命中确实是常态，但**带 tag 的拉取不是「拿本地那份就走」**——它会回源校验 digest。所以：

- 如果你怀疑「加速器里存的是旧版本」，**通常不是原因**，因为带 tag 拉取会去远端确认。
- 反过来，如果你的上游恰好不可用，回源这一步就会成为故障点。

关于「上游不可用时会怎样」，本轮素材里只有一条，且来源层级偏低：后台配置项中出现过「可以在一定时长内回退旧缓存」这类提示文案 <!-- C22 -->（来源：mirror.houlang.cloud 前端 bundle，属**实现细节**，且**会随版本变化**）。

> [!warning] 开放问题：回退旧缓存的时长窗口
> **无公开数值，未实测。** 本轮研究只见到后台配置项的提示文案（C22），官方没有给出任何面向用户的时长承诺，我也没有做实测。**这里不给出任何具体时长数字**，请以控制台实际表现为准。

> [!tip] 大白话
> 把它想成**小区便利店的备货**：第一次你要某个牌子的饮料，店里没货，得先跑一趟总仓补货，然后摆上架（首次回源）。
> 之后你再来，直接从店里拿（缓存命中）。
> 但如果你点名要「**最新款**」（带 tag 拉取），店员不会直接给你货架上的，而是**先打个电话回总部确认有没有更新的批次**——电话打不通，这次就悬了。

---

### 1.5 凭据流向：为什么前缀重写在账号安全上更干净

这是一个很容易被忽略、但影响账号安全的差异。

Docker 上游仓库里有一个至今（2021-02-13 提交，**截至抓取时仍处于开启状态** <!-- C9 -->，见 [moby/moby Issue #42022](https://github.com/moby/moby/issues/42022)）未关闭的 issue，标题就叫「Docker Hub Credentials Leaking to Registry Mirrors」。原文：

> If dockerd has registry mirrors configured, when you log into Docker Hub the mirrors start receiving the credentials on image pulls. This is a security risk, as mirrors shouldn't have access to your Docker Hub tokens.
> <!-- C6 -->（[moby/moby #42022](https://github.com/moby/moby/issues/42022)）

译：**如果 dockerd 配置了 registry mirrors，当你登录 Docker Hub 后，镜像站会在拉取时开始收到你的凭据。这是安全风险——镜像站不该有权限拿到你的 Docker Hub token。**

而且它不只是「有风险」这么抽象，还有一个实打实的副作用：

> It also has the side effect of preventing some registry mirrors from working properly. GCR for example tries to authenticate with the Docker Hub credentials sent and fails, making all requests return an unauthorized error response.
> <!-- C7 -->（同上）

译：**它还会让某些镜像站无法正常工作。比如 GCR 会尝试用发来的 Docker Hub 凭据认证，认证失败后所有请求都返回 unauthorized。**

也就是说，走 `registry-mirrors` 这条路，你的 Hub 凭据是会被「顺带转发」给第三方的——这是机制决定的，不是某家镜像站的问题。

issue 里给出的复现思路 <!-- C8 -->（P3 决议：**只收录命令，不展开安全研究细节**）：

```text
# 执行位置：本机 dockerd 调试环境（来自 moby/moby #42022，仅列命令）
dockerd --debug --registry-mirror=https://mirror.gcr.io
docker pull docker

# 随后抓取发往镜像站的 HTTP 请求，观察其 authorization header。
# 结论：该 header 中携带了 Docker Hub 凭据。此处不复现细节。
```

> [!warning] 以下是 [推论]，不是 issue 原文
> **前缀重写式不把镜像站注册成 Hub 镜像，因此不存在上面这条凭据转发路径。**
>
> 这是**我的推理，issue 本身并没有说这句话**。依据是机制差异：`registry-mirrors` 下你的 Hub 凭据是被 dockerd 主动转发出去的；而前缀重写下你根本没有配置任何镜像，凭据是你**主动**用 `docker login` 交给厚浪自己的（C20）。两条路径在机制上不重叠，所以推论成立——但它仍是推论，**没有一手来源直接证实「厚浪不会碰你的 Hub 凭据」**。

> [!tip] 大白话
> `registry-mirrors` 像**你把 Hub 的门禁卡复印了一份，交给小区门口所有代收点**——你只是想让人帮你取快递，结果每个代收点都拿到了你家的门禁卡。
> 前缀重写则是**你另外办了一张厚浪自己的取件卡**（`docker login mirror.houlang.cloud`），Hub 那张卡始终揣在自己兜里，没给过任何人。

---

### 1.6 服务条款现状，以及本章的素材边界

产品页「⚠️ 重要提示」一节的原文是：

> 使用本服务前，请务必阅读并同意我们的[📜 使用协议](https://home.houlangs.com/?p=d0291245-fa62-413a-8d4f-3debf0f81a07)

该链接指向的域名是 `home.houlangs.com`。本轮通过 DNS 复核（阿里 DoH）查询该域名，返回 **`Status: 3`，即 NXDOMAIN（域名不存在）** <!-- D3 -->（来源：S5 产品页链接 + 本机 DNS 复核）。同一张产品页上的「厚浪云知识库」链接也指向同一域名下的路径，同样不可达。

这一条事实有两个后果，本质上是同一件事的两面：

> [!warning] 后果一：那个链接不要点，也不要推荐
> **该条款链接当前已失效。** 这不是「可能打不开」，是域名已不存在。请注意：
> - 不要照抄旧笔记或旧教程里的 `home.houlangs.com` 链接；
> - 不要向他人推荐这个地址；
> - 如果你要在笔记或文档里引用厚浪的条款，**不要用这个链接**。
>
> 仍在正常工作的是知识库域名 `home.houlang.cloud`（官方教程就在那里）。

> [!warning] 后果二（开放问题 Q6）：条款与隐私政策原文不可获取
> 由于托管域名已 NXDOMAIN，本轮无法取得服务条款与隐私政策的任何文本。因此：
> - 本笔记**不陈述**厚浪的条款内容、数据留存策略、凭据处理承诺；
> - 任何「官方说不会记录你的令牌」这类表述，**没有来源支撑，一律不得写入**。

#### 1.6.1 本章的素材边界

> [!note] 没有独立第三方基准
> 本章也无法给出该服务的**独立第三方端到端基准测试**——本轮研究未发现任何有数据、有复现方法的第三方测评（这是 P1 探测阶段就登记在案的覆盖缺口）。所以本章对性能的描述只复述官方口径（C15），不替它背书。

---

### 1.7 同类方案对照：前缀重写的两种写法

同为「前缀重写式」，不同厂商的写法并不一样。以 DaoCloud 的公开镜像加速文档为例（**二手来源：同类厂商自述**），它明确给了两种：

| 写法 | 示例 | 特点 |
| --- | --- | --- |
| **增加前缀**（原文标注"推荐"） | `k8s.gcr.io/coredns/coredns` → `m.daocloud.io/k8s.gcr.io/coredns/coredns` | **保留**原始上游主机名，镜像站域名插在最前面 |
| **修改镜像仓库的前缀** | `k8s.gcr.io/coredns/coredns` → `k8s-gcr.m.daocloud.io/coredns/coredns` | 上游主机名被换成专属子域，路径部分不变 |

<!-- S11 -->（[DaoCloud 文档中心 · 公开镜像加速](https://docs.daocloud.io/community/mirror/)）

同页还有一句关键信息：

> DaoCloud 目前收录了 600+ 国外镜像，方便国内用户拉取。您可以随时[在 GitHub 上提 PR](https://github.com/DaoCloud/public-image-mirror/pulls)，增加更多的镜像地址。

「需要提 PR 才能增加镜像地址」——这意味着它走的是**白名单制**：只有在已收录清单内的镜像才能拉。

厚浪的写法是第三种：**用短后缀替换上游主机名**。

| 厂商       | 写法             | 示例                                         | 是否需要白名单             |
| -------- | -------------- | ------------------------------------------ | ------------------- |
| DaoCloud | 增加前缀（保留上游主机名）  | `m.daocloud.io/k8s.gcr.io/coredns/coredns` | 是（600+ 收录，需提 PR 扩充） |
| DaoCloud | 修改仓库前缀（换成专属子域） | `k8s-gcr.m.daocloud.io/coredns/coredns`    | 同上                  |
| 厚浪       | 短后缀替换上游主机名     | `mirror.houlang.cloud/k8s/...`             | **[推论] 无白名单，可透传**   |

> [!warning] 最后一行是 [推论]
> 「**厚浪没有白名单、任意该上游下的镜像都能透传**」这一条，**官方没有明说**，是从官网文案与其「直接用后缀替换即可，无需事先登记」的使用方式反推出来的（见 02 深度素材对 G-D 缺口的登记）。它**未经实测验证**，请当作待验证的推论，不要当作承诺。

厚浪这种「短后缀」设计的好处是好记：`ghcr`、`quay`、`nvcr` 基本就是上游域名的首段，不用背 `m.daocloud.io/` 这种额外层级。代价是**可读性变差**——`mirror.houlang.cloud/k8s/...` 看不出原始上游是谁，需要对照速查表（第 2 章 2.5）才能还原。

> [!tip] 大白话
> 后缀代号就是**快递分区号**。DaoCloud 的写法像把「寄往 A 市的包裹，先寄到中转仓，包裹上仍写着 A 市」；厚浪的写法像「A 市的包裹统一写一个分区号 3」，仓分得清，但人得记住 3 号分区就是 A 市。白名单的差别则是：中转仓只收**登记过的**货（DaoCloud），还是**来者不拒**（厚浪，[推论]）。

---

### 本章小结

- 「镜像加速器」不是一种东西，而是三类：**原地镜像（`registry-mirrors`）/ 代理 / 前缀重写**。厚浪属于第三类，它**不改任何配置**，只改你填的镜像地址。
- 厚浪填不进 `daemon.json` 的根因是官方原文 **C1：只有中心化的 Docker Hub 能被镜像**。填了也覆盖不到 gcr / ghcr / quay / nvcr / k8s / mcr / elastic / gitlab 中任何一个。
- 拉取时厚浪扮演 **pull-through cache**：首次回源、后续命中缓存；**带 tag 拉取会回源校验 digest**（C3），所以「缓存里是旧版」通常不是故障原因。
- 回退旧缓存的时长窗口 **无公开数值、未实测**（Q4），本章不给数字；服务条款与隐私政策原文 **不可获取**（Q6），条款链接已失效，**不要引导用户去点**。
- 凭据上，`registry-mirrors` 会把 Hub 凭据转发给镜像站（C6/C7，issue 至今未关闭 C9）；**「前缀重写不存在这条路径」是 `[推论]`**，issue 本身没说这句话。
- 与 DaoCloud 对照：它是**白名单制**（600+ 收录），厚浪用短后缀且 **[推论] 无白名单**。

### 下一章预告

机制讲完了，接下来是动手。第 2 章会给出从「注册 → 建令牌 → 目标机器 `docker login` → 改写地址 → `docker pull`」的完整链路，包含 **9 个上游后缀的速查替换表**（并处理官方教程的 9 个后缀与前端内置 8 个常量的不一致），以及一张可以直接收藏的速查卡。

---

## 第 2 章：怎么用 —— 从注册到 docker pull

> 本章受众：已经读过第 1 章（或已经知道厚浪属于「前缀重写」这一类），现在要真正动手把它用起来的人。

第 1 章讲的是「为什么」，这一章讲的是「怎么做」。好消息是：**整条链路里没有一步是改配置文件**。你要做的全部事情，就是在网页上点几下、在目标机器上敲一条 `docker login`，然后把镜像地址里的上游主机名换成厚浪的后缀——没了。

但「简单」和「不容易做错」是两回事。这条链路里有三个地方最容易翻车：把令牌当账号密码用、在 `daemon.json` 里瞎找配置项、以及**不知道后缀到底有几个、以谁为准**。本章会把这三点逐一钉死，并在最后给出一张可以直接收藏的速查卡（2.8）。

> [!note] 本章与第 1、3 章的分工
> 机制原理（三类加速的差别、为什么填不进 `daemon.json`、缓存与回源）见第 1 章，本章不重复。compose / k8s 的改写代价、私有镜像、配额与限速、完整排错清单见第 3 章。本章只负责「从注册到 `docker pull` 这条主线怎么走通」。

---

### 2.1 全链路总览

官方教程把使用过程拆成三步，标题依次是「首次使用 / 添加令牌 / 登录机器」<!-- C16 -->。这三步之后，官方在「拉取镜像」一节补上了第四件事：**替换镜像地址**。所以完整链路其实有五步：

| 步骤 | 做什么 | 在哪里做 | 素材依据 |
| --- | --- | --- | --- |
| **1** | 访问 `mirror.houlang.cloud` 注册并登录 | 浏览器 | C16 <!-- C16 --> |
| **2** | 在控制台「访问令牌」分区新建令牌 | 浏览器控制台 | C16 <!-- C16 --> |
| **3** | 复制生成的登录命令，到目标机器上执行 `docker login` | **目标机器**（终端） | C16 <!-- C16 --> |
| **4** | 把原镜像地址替换为厚浪地址（改后缀） | 你写命令 / 写文件的地方 | C18 <!-- C18 --> |
| **5** | `docker pull` 新地址，并确认拿到的镜像正确 | **目标机器**（终端） | C17 <!-- C17 --> |

前三步是官方的原话口径，第 4、5 步是官方在「拉取镜像」一节明示的用法：

> 将你原有的镜像地址替换为 HLmirror 即可高速拉取！
> <!-- C18 -->（[《如何使用新版 HLmirror》](https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror)）

把这条链路画成一条线，五个节点的位置关系是这样的：

```text
# 执行位置：全链路示意（浏览器 1–2 步，目标机器 3–5 步）

[浏览器] ① 注册登录 mirror.houlang.cloud
              │
              ▼
[控制台] ② 访问令牌 → 新建令牌 → 拿到「令牌 + 登录命令」
              │
              ▼ 复制这条登录命令
[目标机器] ③ docker login -u <邮箱> -p <hlm_令牌> mirror.houlang.cloud
              │  ← 成功标志：Login Succeeded
              ▼
[你写命令/文件] ④ 把地址里的上游主机名换成后缀
              ghcr.io/…            → mirror.houlang.cloud/ghcr/…
              library/nginx:latest → mirror.houlang.cloud/dh/library/nginx:latest
              ▼
[目标机器] ⑤ docker pull mirror.houlang.cloud/…
```

一句话记住这条链路的分工：**1、2 步是「办一张厚浪的卡」，第 3 步是「把卡交给目标机器」，第 4 步是「改收货地址」，第 5 步才是「收货」。** 前四步里任何一步没做，第 5 步都不会按你预期走。

> [!tip] 大白话
> 把厚浪想成一家**代收点**：第 1、2 步是你去代收点**登记并办一张取件卡**；第 3 步是把这张卡**授权给你家那台机器**（`docker login`）；第 4 步是以后寄件时**在运单上写代收点的门牌号**（改地址）；第 5 步才是去代收点**真取货**（`docker pull`）。四步缺一不可，但最容易被漏掉的是第 3 步——很多人改完地址就直接 pull，然后卡在鉴权上。

---

### 2.2 第一步：注册与登录控制台

官方的第一步只有一行字：

> 访问 [mirror.houlang.cloud](https://mirror.houlang.cloud/) 进行登录注册
> <!-- C16 -->（[《如何使用新版 HLmirror》](https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror)）

看到这个域名时，请先确认自己没走错门。同一家厂商还有一个长得很像的 `all.hlmirror.com`，那是**网页镜像**（给浏览器用的），和 Docker 镜像毫无关系——这在第 1 章 1.1 已经澄清过。给 Docker 用的永远是 **`mirror.houlang.cloud`**。

你注册的是「新版 HLmirror」，官方对这次改造的定位是：

> 新版 HLmirror 将原有 Cloudflare 节点全部替换为了厚浪云自有节点，增加了国内缓存加速。
> <!-- C15 -->（[《如何使用新版 HLmirror》](https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror)，2026-03-31）

「国内缓存加速」这一层，正是后面第 4 步改完地址能变快的原因所在（机制见第 1 章 1.4）。

登录后进入控制台（`mirror.houlang.cloud/dashboard`）。控制台首页由**四个并列分区**组成：

| 分区 | 这一区是干嘛的 | 本章会用到哪一区 |
| --- | --- | --- |
| **账号信息** | 账号与用户组 | 不用 |
| **访问令牌** | 创建 / 查看 / 删除令牌 | **2.3 要在这里建令牌** |
| **用量** | 当前配额窗口的使用量 | 第 3 章会提，本章不展开 |
| **镜像源** | 当前账号可访问的镜像渠道列表 | **2.5 的 D1 裁决入口** |

> [!note] 这四个分区名是「界面文案」，不是官方命名
> 上表的四个分区名，来自对 `mirror.houlang.cloud` 前端 bundle 的字符串提取（`sources/09_console_ui_strings.md`，来源层级为**实现细节**）。它们**不是官方文档里的正式命名**，只是控制台界面上实际出现的字样。之所以要列出，是因为其中**「镜像源」这一区对本章很关键**——2.5 处理「后缀到底有几个」这个矛盾时，最终就落在这个分区上。

「镜像源」分区为什么关键？因为它是**你账号实际能用哪些后缀**的唯一权威入口。前端代码里内置的常量、教程文章里列的表格，都可能和你的账号实际看到的列表不一致——此刻以你在**这一区**看到的为准。这句结论会在 2.5 展开。

> [!tip] 大白话
> 控制台的四个分区，就像**办完卡之后 App 里的四个标签页**：一个放你的资料（账号信息），一个放你办的卡（访问令牌），一个放你这个月的消费记录（用量），还有一个放「这张卡能在哪些店刷」（镜像源）。本章 2.3 要用的是「卡」那个标签页；2.5 出问题时，你要回头看的是「哪些店能刷」那个标签页。

---

### 2.3 第二步：创建访问令牌

官方的第二步：

> 在「访问令牌」选项卡中新建令牌
> <!-- C16 -->（同上）

以及紧接着的一句，是本节的要点：

> 创建令牌后会得到令牌和登录命令
> <!-- C16 -->（同上）

也就是说，**令牌和登录命令是一起给你的**，你不需要自己去拼这条命令。在控制台界面上，令牌页的主按钮文案是「创建新的访问令牌」/「创建令牌」，创建完成后会提供「复制登录命令」与「仅复制令牌」两个复制入口 <!-- S4b -->（来源：`sources/09_console_ui_strings.md`，实现细节）。**直接点「复制登录命令」**，省得自己拼错。

关于令牌本身，有一条来自实现细节的信息需要标注来源层级：

> `docker login -u ${email} -p ${token} ${host}`
> <!-- C20 -->（来源：`mirror.houlang.cloud` 前端 bundle，属**实现细节**、非官方文档口径）

也就是登录命令的形态是「用户名用邮箱、密码位放令牌、目标是厚浪的域名」。此外，**令牌带 `hlm_` 前缀** <!-- C20 -->（同为 S4 实现细节）。这条前缀不是官方教程说的，是从前端实现里看到的，所以它**可能随版本变化**——写进笔记是为了让你认出「拿到手的字符串是令牌，不是密码」。

一条需要先说清楚的边界：**本轮没有收集到任何关于令牌数量、有效期、配额数值的公开口径**。控制台界面上出现过「删除访问令牌」这样的操作文案 <!-- S4b -->，所以令牌是可以在控制台删除的；但「删除/吊销之后会发生什么」属于开放问题，**未取证**，第 3 章会专门标注，本章不做任何行为推测。

> [!tip] 大白话
> 令牌就是**一张专门给机器用的门禁卡**，不是你的账号密码本身。它的几个性质都能用门禁卡来类比：它是**发给机器而不是发给人**的（所以你会把命令复制到服务器上跑，而不是背下来）；它能被**单独作废重新办**（控制台里能删），不用动你的账号；它长得也和账号密码不一样（带 `hlm_` 前缀，一眼能区分）。**最关键的一条：这张卡只交给「需要拉镜像的那台机器」，不给别的任何地方。**

> [!warning] 令牌的泄露面 = 账号
> 令牌是 `docker login` 用的凭据 <!-- C20 -->。拿到它的人，可以用它在任何机器上以你的身份登录厚浪、消耗你的额度。所以：
> - **不要**把令牌贴到聊天群、issue、公开仓库、截图里；
> - **不要**把它当成「账号密码」填到任何其他地方（它只用于 `docker login`，见 2.4 的误用提醒）；
> - 怀疑泄露时，去控制台把这条令牌删掉再建一条。
>
> 社区 QQ 群（230832864）在本项目中**只作为线索来源，不作为可引用依据**；把令牌贴进群里更是万万不可。

---

### 2.4 第三步：在目标机器上 docker login

官方的第三步是这三步里唯一「不发生在浏览器里」的一步：

> 复制登录命令到需要拉取镜像的机器进行登录，本文以 Ubuntu 服务器为例
> <!-- C16 -->（同上）

「需要拉取镜像的机器」是关键词——**在哪台机器拉镜像，就在哪台机器登录**。登录状态是跟着那台机器上的 Docker 走的，不会因为你本机登录了、服务器上就自动能用。命令形态（S4 实现细节）：

```bash
# 执行位置：目标机器（本例为 Ubuntu 服务器）
# 官方命令模板：docker login -u ${email} -p ${token} ${host}
# 代入后（直接从控制台「复制登录命令」拿到的就是这一条）：
docker login -u your-email@example.com -p hlm_xxxxxxxxxxxxxxxx mirror.houlang.cloud

# 成功时的输出末尾会出现：
# Login Succeeded
```

> [!warning] 用单引号或交互输入更稳妥
> `-p` 后面直接跟明文令牌，命令会留在 shell 历史里。如果介意，可以**省略 `-p`**，让 `docker login` 用交互方式提示你输入（令牌粘进去时终端不回显），或者改用 `--password-stdin` 从标准输入读。这两种做法是 Docker 客户端的通用能力，**不是厚浪教程里的内容**，此处仅作提醒。

#### 成功标志：`Login Succeeded`

官方给的判据非常明确，只有一个字符串：

> 看到“ _Login Succeeded_ ”即代表登录成功，后续可通过 HLmirror 高速拉取镜像
> <!-- C17 -->（同上）

所以第 3 步的验收标准就是：**命令输出里出现 `Login Succeeded`**。看到它，才进入第 4 步；没看到，说明登录没成，先别急着改地址去 pull。

> [!warning] 常见误用：把令牌当密码填到别处
> 令牌是 `docker login` 的凭据，它的「用户名」是你的**邮箱**、它的「密码」才是令牌。最常见的三种错法：
> 1. **把令牌填成用户名**——`-u` 应该填邮箱，不是 `hlm_…` 串；
> 2. **把令牌当 Docker Hub 密码用**——去登录 `docker.io` 或别的仓库，令牌在那边无效；
> 3. **把令牌写进 `daemon.json`**——那里根本没有能放令牌的字段，令牌不是给守护进程配置用的。
>
> 记住一条：**令牌只在 `docker login … mirror.houlang.cloud` 这一条命令里出现**，出现别的地方基本都是错的。

> [!warning] 开放问题 Q1：拉公开镜像是否**必须**先 `docker login`？
> **未实测，官方教程未说明匿名能否拉取。**
>
> 官方教程把 `docker login` 写成了一条必经步骤（C16 的三步里就含它），但它**从头到尾没有说明**「不登录、直接匿名 `docker pull` 一个公开镜像行不行」。本轮研究也**没有做实测**。
>
> 因此这里**不能给你结论**——既不能写「必须先登录」，也不能写「不用登录也行」。稳妥的做法是：**按官方教程走，先登录再拉**。如果你确实想知道匿名行为，请自行在目标机器上试一次 `docker pull mirror.houlang.cloud/dh/library/nginx:latest`（不登录）并观察结果，以实测为准。

---

### 2.5 第四步：改写镜像地址（速查核心节）

这是本章篇幅最长的一节，也是你以后最常回来查的一节。核心动作只有一句话：**把镜像地址里的「上游主机名」换成「厚浪域名 + 后缀」。**

官方对这件事的表述是：

> HLmirror 支持 Docker Hub、GHCR 等多个镜像源，通过后缀区分。
> <!-- C19 -->（同上）

「通过后缀区分」——这就是「短后缀替换」这个写法的由来（第 1 章 1.7 已对照过它与 DaoCloud 写法的差别）。

#### 9 个后缀速查表

官方教程给出的后缀表如下（**逐字**，含原文的 `NVDIA` 拼写）：

| 上游                           | 后缀代号      | 替换地址                            |
| ---------------------------- | --------- | ------------------------------- |
| Docker Hub                   | `dh`      | `mirror.houlang.cloud/dh/`      |
| Google Container Registry    | `gcr`     | `mirror.houlang.cloud/gcr/`     |
| Github Container Registry    | `ghcr`    | `mirror.houlang.cloud/ghcr/`    |
| NVDIA NGC                    | `nvcr`    | `mirror.houlang.cloud/nvcr/`    |
| Kubernetes Registry          | `k8s`     | `mirror.houlang.cloud/k8s/`     |
| Microsoft Container Registry | `mcr`     | `mirror.houlang.cloud/mcr/`     |
| Elastic Docker Registry      | `elastic` | `mirror.houlang.cloud/elastic/` |
| registry.gitlab.com          | `gitlab`  | `mirror.houlang.cloud/gitlab/`  |
| Quay                         | `quay`    | `mirror.houlang.cloud/quay/`    |

<!-- C19 -->（[《如何使用新版 HLmirror》](https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror)）

> [!warning] D1：这张表有 9 行，但你的账号未必是 9 行 —— **后缀以控制台镜像源列表为准**
> 这张 9 行表抄自官方教程，**其中包含 `gitlab`**。但本轮研究同时发现一处不一致：
>
> - **官方教程**列出 **9** 个后缀：`dh / gcr / ghcr / nvcr / k8s / mcr / elastic / gitlab / quay`（上表）；
> - **前端 bundle 内置的常量只有 8 个**，且**不含 `gitlab`** <!-- C19/D1 -->（来源：`mirror.houlang.cloud` 前端 bundle，属**实现细节**）。
>
> 两者不一致时，**以控制台「镜像源」分区里实际列出的为准**（该分区见 2.2）。理由很简单：你真正能拉哪些上游，取决于**你的账号被开通了哪些渠道**，而这件事只有控制台知道。
>
> 两条操作原则：
> 1. **不要**把前端 bundle 的内置常量当成权威——它只是实现细节，且会随版本变化，不代表你的账号实际可用的清单；
> 2. **不要**假设官方教程的 9 行对每个账号都成立——教程是文章，控制台是实况。
>
> 本节照官方教程写 9 个后缀（因为那是官方口径），但你落地时请**先看一眼控制台的「镜像源」列表**再决定用哪几个。

#### 官方两个示例（逐字）

**以 ghcr 为例** <!-- C19 -->（同上）：

```text
# 执行位置：对照示意（非可执行文件）
原镜像地址：ghcr.io/immich-app/immich-server:v2.6.1
替换为 HLmirror：mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
拉取命令示例：docker pull mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
```

**以 Docker Hub 为例** <!-- C19 -->（同上）：

```text
# 执行位置：对照示意（非可执行文件）
原镜像地址：library/nginx:latest
替换为 HLmirror：mirror.houlang.cloud/dh/library/nginx:latest
拉取命令示例：docker pull mirror.houlang.cloud/dh/library/nginx:latest
```

这两个例子恰好覆盖了改写时的两种形态，值得单独说清楚：

| 情形                                                                     | 原地址长什么样                                 | 改写动作                                             | 例                                                                                                       |
| ---------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **地址里带上游主机名**（ghcr / quay / nvcr / gcr / k8s / mcr / elastic / gitlab） | `ghcr.io/<命名空间>/<镜像>:<标签>`              | **把主机名整段换成** `mirror.houlang.cloud/后缀/`，后面路径原样保留 | `ghcr.io/immich-app/immich-server:v2.6.1` → `mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1` |
| **地址里不带主机名**（Docker Hub 的简写）                                           | `library/nginx:latest` 或 `nginx:latest` | 补上 `mirror.houlang.cloud/dh/` 前缀                 | `library/nginx:latest` → `mirror.houlang.cloud/dh/library/nginx:latest`                                 |

第二种情形是最容易犯迷糊的：平时你敲 `docker pull nginx` 时，Docker 悄悄替你补上了 `docker.io/library/`；现在要换地址，你得**显式把这段补上去**，并且用 `dh` 这个后缀代表 Docker Hub。

把「原地址 → 厚浪地址」的换法做成一张对照示意（含官方没举例但同构的上游）：

```text
# 执行位置：对照示意（改写规则演示，不需要执行）

# 规则：mirror.houlang.cloud/{后缀}/{原地址去掉上游主机名后的部分}
#   ├ 带主机名的：删掉主机名，换成 域名/后缀
#   └ Docker Hub：补上 dh 前缀

ghcr.io/immich-app/immich-server:v2.6.1  →  mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
quay.io/prometheus/node-exporter:v1.8.2  →  mirror.houlang.cloud/quay/prometheus/node-exporter:v1.8.2
nvcr.io/nvidia/cuda:12.4.1-base-ubuntu22.04 → mirror.houlang.cloud/nvcr/nvidia/cuda:12.4.1-base-ubuntu22.04
registry.k8s.io/kube-apiserver:v1.30.0   →  mirror.houlang.cloud/k8s/kube-apiserver:v1.30.0
mcr.microsoft.com/dotnet/runtime:8.0     →  mirror.houlang.cloud/mcr/dotnet/runtime:8.0
library/nginx:latest                     →  mirror.houlang.cloud/dh/library/nginx:latest
```

> [!warning] 关于上表后四行的来源
> 上面的 ghcr 与 Docker Hub 两行是**官方示例逐字对应**的写法。其余几行是**我用同一规则套出来的 `[推论]`**——官方没给这些上游的示例，但改写规则（删主机名、套后缀）是一致的。上表中的**上游 URL 一律不写**：官方教程只给了上游**名称**和后缀代号，没有给 URL，请勿自行补 URL 后当作官方口径。

> [!tip] 大白话
> 后缀代号就是**快递分区号**。原来的地址 `ghcr.io/…` 像「寄往 GHCR 市的包裹」，厚浪的写法是「所有 GHCR 市的包裹统一改成 3 号分区、由厚浪这个中转仓代收」——`mirror.houlang.cloud/ghcr/` 就是那个「3 号分区」。
>
> 用起来就一步：**原来地址开头写的是「哪个市」，现在改写「厚浪中转仓 + 那个市的分区号」**，后面的「街道门牌」（命名空间 / 镜像名 / 标签）一个字都不用动。Docker Hub 特殊一点，它平时**不写市名**（直接 `nginx`），所以要你手动补一个 `dh` 分区号上去。

---

### 2.6 第五步：拉取并验证

第 4 步改完地址，第 5 步就是把它拉下来。用官方示例里的那条命令：

```bash
# 执行位置：目标机器（已按 2.4 完成 docker login）
docker pull mirror.houlang.cloud/dh/library/nginx:latest

# 也可以用官方 ghcr 示例：
docker pull mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
```

拉取成功后，镜像就以**你填的那个完整地址**作为名字存进了本地。这一点在后续 `docker run` / compose 引用时要注意：**你用什么地址拉的，就得用什么地址引用**（第 3 章讲 compose 时会强调这一点）。

#### 验证拿到的是不是想要的镜像

> [!warning] 以下验证命令是 Docker 通用做法，**不是本服务的官方说明** `[推论]`
> 官方教程只讲到「`docker pull` 厚浪地址」为止，**没有**给验证步骤。下面这几条是**通用 Docker 命令**，我列出来是为了让你有办法自查，但它们**不来自本轮的素材**，请当作 `[推论]`/常识使用：

```bash
# 执行位置：目标机器
# 1. 看镜像是否已在本地、名字是否就是厚浪地址
docker images

# 2. 看某个镜像的详细元数据（digest、架构、标签等）
docker inspect mirror.houlang.cloud/dh/library/nginx:latest

# 3. 如果想比对「厚浪拉的」与原地址是否是同一份内容
#    可对比两侧的 RepoDigests（注意：这需要两个地址都能拉到）
docker inspect --format='{{index .RepoDigests 0}}' mirror.houlang.cloud/dh/library/nginx:latest
```

关于「拿到的到底是不是最新版」，第 1 章 1.4 已经讲过机制：**带 tag 拉取时会回源校验 digest**（C3），所以「加速器里是旧版」通常不是问题所在——但回源这一步依赖上游可达，上游抖动时它会是故障点（第 3 章 3.3 的坑 ④）。

> [!note] 上游不可用时的兜底
> 本轮素材里另有一条**实现细节**层面的信息：上游不可用时，可在**一定时长内回退旧缓存** <!-- C22 -->（来源：`mirror.houlang.cloud` 前端 bundle 的后台配置项文案，**会随版本变化**）。该「一定时长」的**具体数值无公开口径、未实测**（第 1 章 1.4 的 Q4 已标注），这里**不给任何数字**。

> [!tip] 大白话
> 第 5 步就是**去代收点真取货**。取回来之后，包裹上贴的地址会变成「代收点 + 分区号」那一串（`mirror.houlang.cloud/…`），而不是原来的 `ghcr.io/…`——这不是取错了，这是正常现象，因为你就是按这个新地址下的单。以后要用这个包裹（`docker run`），**报的也得是新地址**。

---

### 2.7 场景差异：Linux 服务器 / Docker Desktop / k8s 节点

> [!warning] 本节全部内容为 `[推论]`，官方教程未涉及
> 官方教程在这一块只有一句限定语：**「本文以 Ubuntu 服务器为例」**（原文见 2.4 的 C16 引用）。它**只演示了 Ubuntu 服务器这一种场景**，对 **Docker Desktop** 和 **k8s 节点侧**没有任何官方口径（这是素材缺口 **G-A**）。
>
> 因此，**本节以下所有内容都是我基于机制推出来的 `[推论]`，不是官方说法**。请按「待验证的推断」对待，不要当作权威结论，更不要以官方口吻转述给他人。k8s 节点侧的完整讨论放在第 3 章，本节只做提示。

**Linux 服务器**（官方唯一演示的场景）：就是本章 2.4–2.6 的走法——在服务器上 `docker login mirror.houlang.cloud`，改地址，`docker pull`。**只有这一条是官方口径。**

`[推论]` **Docker Desktop（Windows / macOS）**：机制上，Docker Desktop 里跑的还是 Docker 客户端与守护进程，`docker login` 这条命令同样可用，所以**应当同样走「登录 + 改地址」这条路**。需要特别注意的是：

- **不要**去 Docker Desktop 的 Settings → Docker Engine 里找 `registry-mirrors` 来填厚浪——那是第 1 章 1.2 讲的**另一种机制**（原地镜像），按 1.3 的 C1 原文，它**只对 Docker Hub 生效**，填了也覆盖不到 ghcr / quay / nvcr 等任何一个；
- 也就是说，即使你在 Docker Desktop 里看到那个配置框，**它也不是为厚浪准备的入口**。厚浪的入口永远只有「`docker login` + 改地址」这一条。

`[推论]` **k8s 节点侧**：前缀重写在 k8s 里意味着**改写 manifest 里每一处 `image:` 字段**（因为集群不会自动把地址替换掉）；如果不想改 manifest，另一条路是动 containerd 的 `hosts.toml`。这两条路都不在本章范围，**详见第 3 章**。此处只需记住一点：**k8s 不会因为你在某台机器上 `docker login` 过就自动生效**——它的镜像拉取由节点侧的容器运行时负责，是另一套路径。

> [!tip] 大白话
> 官方教程是一份**只写了「Ubuntu 服务器」这一道菜的做法**。Linux 服务器你照着做就行；Docker Desktop 和 k8s 是它没写的那两道菜，**下面这些是我按食材自己推的做法**，能说通，但厨师没教过。特别是 k8s：它更像「一个团队自己有一套餐厨流程」，你在自己笔记本上办的卡（`docker login`），**不会自动被那个团队的厨房认**。

---

### 2.8 速查卡

> [!summary] 厚浪镜像 · 一页速查
> 下面只汇总**本章已经给出**的信息，方便回查。**这里不引入任何新论断**。

**① 令牌创建入口**

- 打开 `mirror.houlang.cloud` → 登录 → 控制台「**访问令牌**」分区 → 「创建新的访问令牌」→ 复制「**登录命令**」<!-- C16 / S4b -->

**② 登录命令模板**（执行位置：**目标机器**）

```bash
# 执行位置：目标机器
docker login -u <你的邮箱> -p <hlm_令牌> mirror.houlang.cloud
# 成功标志：输出里出现 Login Succeeded     <!-- C17 -->
```

**③ 9 个后缀替换表**（以官方教程为准；**后缀以控制台「镜像源」列表为准**）

| 上游 | 后缀 | 替换地址 |
| --- | --- | --- |
| Docker Hub | `dh` | `mirror.houlang.cloud/dh/` |
| Google Container Registry | `gcr` | `mirror.houlang.cloud/gcr/` |
| Github Container Registry | `ghcr` | `mirror.houlang.cloud/ghcr/` |
| NVDIA NGC | `nvcr` | `mirror.houlang.cloud/nvcr/` |
| Kubernetes Registry | `k8s` | `mirror.houlang.cloud/k8s/` |
| Microsoft Container Registry | `mcr` | `mirror.houlang.cloud/mcr/` |
| Elastic Docker Registry | `elastic` | `mirror.houlang.cloud/elastic/` |
| registry.gitlab.com | `gitlab` | `mirror.houlang.cloud/gitlab/` |
| Quay | `quay` | `mirror.houlang.cloud/quay/` |

**④ 拉取命令模板**（执行位置：**目标机器**）

```bash
# 执行位置：目标机器
# 规则：mirror.houlang.cloud/{后缀}/{原地址去掉上游主机名后的部分}
docker pull mirror.houlang.cloud/dh/library/nginx:latest
docker pull mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
```

**⑤ 成功标志**

- 登录成功：输出出现 `Login Succeeded` <!-- C17 -->
- 拉取成功：`docker pull` 正常结束，镜像以**厚浪地址**的名字出现在本地

**⑥ 失败先查什么（按这个顺序）**

1. **登录那步过了吗？** 没看到 `Login Succeeded` 就先解决登录，别去查地址。
2. **地址改写对不对？** 上游主机名是否已换成「域名 + 后缀」；Docker Hub 的简写是否补了 `dh`。
3. **后缀在不在你的列表里？** 回控制台「**镜像源**」分区核对，**以后缀以控制台为准**。
4. **是不是想填进 `daemon.json`？** 那条路不通，机制原因见第 1 章 1.3。
5. **令牌有没有放对位置？** 它只在 `docker login` 里出现（2.4 的误用提醒）。
6. **上游是不是在抖？** 带 tag 拉取会回源，服务状态可看状态页（第 1 章 1.1 / 第 3 章）。

> [!note] 本速查卡不包含的内容
> 配额、限速、令牌有效期、拉取速率等**任何数字**，本章均未给出，速查卡也不给——本轮素材没有这些数值的公开口径 <!-- C21 -->（第 3 章会说明「以控制台 / 账号实际为准」）。compose / k8s 的改写写法也不在这里，见第 3 章。

---

### 本章小结

- 全链路是**五步**：注册登录 → 新建令牌 → 目标机器 `docker login` → 改写镜像地址 → `docker pull`。官方教程的三步（C16）是前三步，后两步是官方在「拉取镜像」一节补的（C18）。
- **没有一步是改配置文件**。厚浪的入口只有「`docker login` + 改地址」，`daemon.json` 的 `registry-mirrors` 不是它的入口（机制原因见第 1 章 1.3）。
- 令牌就是**给机器用的门禁卡**：创建时连登录命令一起给你，带 `hlm_` 前缀（来源为实现细节），**泄露面等于账号**，只交给需要拉镜像的那台机器。
- 登录成功的唯一判据是输出里的 **`Login Succeeded`**（C17 逐字）。
- **后缀表官方给了 9 个（含 `gitlab`），但前端 bundle 内置常量只有 8 个**（D1）；不一致时**以控制台「镜像源」列表为准**，不把 bundle 当权威。
- **拉公开镜像是否必须先登录（Q1）未实测**，官方教程未说明匿名能否拉取，本章**不给结论**，建议照官方走即先登录。
- **2.7 的场景差异全部是 `[推论]`**：官方只演示了 Ubuntu 服务器；Docker Desktop 与 k8s 节点侧都没有官方口径（G-A）。

### 下一章预告

主线走通了，接下来是「什么时候会踩坑」。第 3 章会讲清：**为什么前缀重写对 compose 和 k8s 意味着「每一处 `image:` 都得手改」**、不想改 manifest 时的 containerd `hosts.toml` 路线、私有镜像（GHCR）为什么是零验证记录、令牌的生命周期问题，以及配额与限速「只有字段名、没有任何数字」这件事该怎么理解。

---

## 第 3 章：进阶场景与常见坑

> 本章受众：已经跑通第 2 章那条「注册 → 建令牌 → `docker login` → 改地址 → `docker pull`」链路的人。

手动 `docker pull` 的时候，前缀重写几乎是零成本的：改一个字符串，快就完事。真正会让人踩坑的，是把它放进**别人写的文件**里——compose 的 `image:`、k8s 的 manifest、节点上的容器运行时配置。这些地方的共同点是：**你要改的位置不止一处，而且漏掉一处不会有任何报错**。

本章就干三件事：把「改文件」这份代价讲清楚（3.1 / 3.2）、把五个最高频的坑固定编号列出来（3.3），再把三块**本轮研究确实答不了**的空白如实标注出来（3.4 / 3.5 / 3.6），最后给一张排错入口清单（3.7）。

> [!note] 本章不涉及的内容
> 三类机制（原地镜像 / 代理 / 前缀重写）的分野与「为什么填不进 `daemon.json`」见第 1 章；注册、建令牌、`docker login`、**9 后缀速查表**与完整拉取流程见第 2 章 2.5。本章只处理"用起来会遇到什么代价与坑"。

---

### 3.1 改写代价之一：compose 文件

官方对用法的定义只有一句话，前面两章都引过，但这里要看的是它的**字面动作**：

> 将你原有的镜像地址替换为 HLmirror 即可高速拉取！
> <!-- C18 -->（[《如何使用新版 HLmirror》](https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror)）

关键词是「**替换**」。它不是一个"配置一次、自动改道"的开关，而是把你**已经写在文件里**的那个字符串换掉。既然是替换字符串，那么结论就很直接：**你写了几处镜像地址，就要改几处。**

compose 文件里，镜像地址出现在 `image:` 字段：

```yaml
# 执行位置：项目内 compose 文件（docker-compose.yml）
services:
  web:
    image: mirror.houlang.cloud/dh/library/nginx:latest        # 原：nginx:latest
  api:
    image: mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
    # 原：ghcr.io/immich-app/immich-server:v2.6.1
```

两处 `image:` 都得改。上面这两行的改写依据就是第 2 章 2.5 的速查表：`nginx:latest` 走 `dh` 后缀（并补上 `library/` 这一层），`ghcr.io/...` 走 `ghcr` 后缀。漏掉 `api:` 那一行，`web` 走厚浪、`api` 走公网，跑起来一切正常，只是慢——**没有任何报错会提醒你漏了**。

> [!warning] 别以为配一次就全自动
> 前缀重写**没有"全局生效"这一说**。第 1 章 1.2 里的 `registry-mirrors` 和代理，都是"配置一次、之后所有 `docker pull` 自动改道"；前缀重写不走这条路，它是**每一处地址都要在写法上体现**。`docker pull` 时省下来的那份事，代价原封不动地转移到了"改文件"上。

> [!note] 一个待确认的相邻位置：[推论]
> Dockerfile 的 `FROM` 行、Helm values、CI 流水线里的镜像地址，从「地址替换」这个动作看属于同一类；但**官方教程只谈了镜像地址本身**，没有逐一点名这些位置。把它们一并改写属于 `[推论]`，方向没错，但请自行验证。

> [!tip] 大白话
> `registry-mirrors` 像**给小区门口换一个统一的代收点**，之后所有快递自动改道到新地方；前缀重写像**你每一张快递单都得亲手写一遍新地址**。单子只有一张的时候，后者更省事；单子有二十张的时候，漏写一张就够你排查半天。
>
> 改完 compose 文件后要用的命令（`docker compose up -d`、`down`、`pull` 等）见 [[Docker与DockerCompose命令速查]]。

---

### 3.2 改写代价之二：k8s —— manifest 改写 vs containerd hosts.toml

#### 3.2.1 先钉死一件事：k8s 没有原生的「前缀重写」API

> [!warning] C14：这是一条"查不到"的结论，不是"官方说没有"
> 本轮检索中，**未找到 Kubernetes 提供「镜像前缀重写」这类原生 API 的任何一手出处**（02 素材把这条登记为缺口 G8）。
> 因此本笔记的写法是：**它不是 k8s 的能力**，请**不要**把前缀重写描述成 k8s 原生特性，也不要在别人的方案里默认它存在。
> k8s 场景下能走的路只有两条，且都在 k8s **之外**：
> ① 在 manifest 里把 `image:` 写成厚浪的全限定地址——这条在你写的 YAML 里；
> ② 改**节点**上的容器运行时（containerd）配置——这条在节点上，属于集群管理员的领域。
> <!-- C14 -->

#### 3.2.2 路线一：改 manifest 的 `image` 字段

这一条与 3.1 同源，只是文件从 compose 换成了 k8s 清单：

```yaml
# 执行位置：集群 manifest（Pod / Deployment 的 spec.containers）
containers:
  - name: web
    image: mirror.houlang.cloud/dh/library/nginx:latest          # 原：nginx:latest
  - name: server
    image: mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
    # 原：ghcr.io/immich-app/immich-server:v2.6.1
```

这里有一个 k8s 特有的前提，必须写清楚，否则你会以为 `image: nginx` 也会自动走厚浪：

> If you don't specify a registry hostname, Kubernetes assumes that you mean the [Docker public registry](https://hub.docker.com/). You can change this behavior by setting a default image registry in the [container runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) configuration.
> <!-- C13 -->（[Kubernetes Docs · Images](https://kubernetes.io/docs/concepts/containers/images/)）

译：**如果你不写 registry 主机名，Kubernetes 就认为你指的是 Docker 公共仓库；这个行为可以通过在容器运行时配置里设置"默认镜像仓库"来改变。**

也就是说，`image: nginx:latest` 和 `image: mirror.houlang.cloud/dh/library/nginx:latest` 在 k8s 眼里是**两个不同的仓库地址**，不存在"后者是前者加速版"的关系——`.io/library` 那层默认逻辑只对 Docker 公共仓库生效。**你必须写全限定地址，k8s 才会去厚浪。** <!-- S10 -->

> [!tip] 大白话
> k8s 读 `image:` 的方式像**一个不认路的快递员**：你只写「3 号楼」，他就默认送去**公司总部大楼**的 3 号楼（Docker 公共仓库）；你要他去厚浪那个仓，就得**把门牌号写全**。他不会帮你找近路，也**没有**"把收到的地址统一改一改"这种设定——这正是 3.2.1 的 C14 在说的事。

#### 3.2.3 路线二：在节点上配 containerd `hosts.toml`

另一条路是把加速做在**节点**这一层，让 manifest 一个字都不用改。containerd 的 registry 配置有过两代写法，旧的已经被官方判废：

> The old CRI config pattern for specifying registry.mirrors and registry.configs has been **DEPRECATED**. You should now point your registry `config_path` to the path where your `hosts.toml` files are located
> <!-- C10 -->（[containerd Docs · Hosts](https://containerd.io/docs/1.7/hosts/)）

译：**旧的、用 `registry.mirrors` / `registry.configs` 指定 registry 的 CRI 配置写法已废弃；现在应把 registry 的 `config_path` 指向存放 `hosts.toml` 文件的目录。**

这一条的现实意义是：**很多存量教程里那种 `registry.mirrors = [...]` 的写法，正属于"已废弃"的那一代**。照抄老博客时，先确认它用的是哪一代。

配置分两步。第一步，让 containerd 知道去哪个目录找（官方示例，逐字）：

```toml
# 执行位置：k8s 节点 /etc/containerd/config.toml（官方示例，逐字）
version = 2
[plugins."io.containerd.grpc.v1.cri".registry]
   config_path = "/etc/containerd/certs.d"
```
<!-- C10 --> <!-- S9 -->

第二步，按 **registry 主机名** 建子目录，每个子目录里放一个 `hosts.toml`。官方给的目录结构示例（逐字）：

```text
# 执行位置：k8s 节点 shell（官方示例，逐字）
$ tree /etc/containerd/certs.d
/etc/containerd/certs.d
└── docker.io
    └── hosts.toml
```
<!-- C10 -->（[containerd Docs · Hosts](https://containerd.io/docs/1.7/hosts/)）

同一页还补了一句很实用的话：**这个目录下的改动不需要重启 containerd 守护进程**（"Updates under this directory do not require restarting the containerd daemon."）。

`hosts.toml` 里可以声明镜像源，并用 `capabilities` 区分能力。官方「Setup a Local Mirror for Docker」示例（逐字）：

```toml
# 执行位置：k8s 节点 /etc/containerd/certs.d/<registry 主机名>/hosts.toml（官方示例，逐字）
server = "https://registry-1.docker.io"    # Exclude this to not use upstream

[host."https://public-mirror.example.com"]
  capabilities = ["pull"]                  # Requires less trust, won't resolve tag to digest from this host
[host."https://docker-mirror.internal"]
  capabilities = ["pull", "resolve"]
  ca = "docker-mirror.crt"
```
<!-- C11 --> <!-- C12 --> <!-- S9 -->

那两行注释就是本节最重要的两个知识点：

**第一，`capabilities = ["pull"]  # Requires less trust, won't resolve tag to digest from this host`。** <!-- C11 --> 能力清单里只写 `pull`、不写 `resolve`，含义是这个 host **不被信任去把 tag 解析成 digest**——也就是第 1 章 1.4 讲的"带 tag 拉取要回源校验 digest"那一步，不会交给公共镜像源来做。官方给了一张能力对照表说明原因（顶格）：

| Registry Type | Pull | Resolve | Push |
| --- | --- | --- | --- |
| Public Registry | yes | yes | yes |
| Private Registry | yes | yes | yes |
| Public Mirror | yes | no | no |
| Private Mirror | yes | yes | no |

官方对这张表的解释只有一句（逐字）：**"A public mirror should never be trusted to do a resolve action."**（公共镜像源绝不该被信任去执行 resolve 操作。）<!-- C11 -->

**第二，`server = "https://registry-1.docker.io"    # Exclude this to not use upstream`。** <!-- C12 --> `server` 是这个 registry 命名空间的默认上游；**把它省略，就等于禁用上游**，所有请求只走你列出的 `[host]` 条目。改上游还是完全替换上游，差别就在这一行有没有删。

> [!note] 厚浪能不能直接填进这里？本轮无验证记录
> `[host."…"]` 条目确实是用来列镜像源的，形态上就像"给这个 registry 指一个镜像"。但厚浪的路径结构是 `mirror.houlang.cloud/{后缀}/…`（地址里额外带一层后缀），它与上例中 `https://public-mirror.example.com` 这种**纯主机名**形态能不能直接互换，**本轮没有任何验证记录**。
> 因此本节**不给出"可直接照抄的厚浪 `hosts.toml`"**——给一个看起来能用、实际未必成立的配置，比不给更糟。k8s 场景下，本笔记有据可依的用法是 **3.2.2 的 manifest 改写**。

> [!tip] 大白话
> 两条路的分工，用寄件打比方最清楚：
> **manifest 改写 = 每次寄件都手写新地址**——包裹（镜像）完全不变，但每一张单子（每一处 `image:`）都要你自己写对，谁写漏了谁就寄去老地方。
> **hosts.toml = 在小区门口设一个统一转发点**——单子上地址照旧，箱子到门口自动被转走。代价是这个转发点要装在**每一台节点**上（它是节点级配置，不是集群级的），而且要动的是管理员的地盘。

---

### 3.3 常见坑 1–5

编号固定（1–5），顺序与 02 素材 §4.3 一致，便于以后回查与互相引用。每个坑统一「现象 → 原因 → 怎么做」。

#### 坑 ①：把它填进 `daemon.json` 的 `registry-mirrors`

> [!warning] 现象 → 原因 → 怎么做
> **现象**：把厚浪地址写进 `daemon.json` 的 `registry-mirrors` 之后，拉 Docker Hub 的镜像确实快了，于是以为配好了；结果拉 `ghcr.io/...`、`quay.io/...` 时一点没变，还以为是"厚浪对这些上游支持不好"。
> **原因**：`registry-mirrors` 只能镜像 Docker Hub——官方原文是 **"It's currently not possible to mirror another private registry. Only the central Hub can be mirrored."**（C1）；而厚浪的用法是**地址替换**，不是配置镜像源（C18）。这两件事在机制上不重叠，详见第 1 章 1.3。
> **怎么做**：不要动 `daemon.json` 的 `registry-mirrors`；在拉取时直接把地址改成厚浪地址（第 2 章 2.5 速查表）。

#### 坑 ②：把令牌当账号密码到处贴

> [!warning] 现象 → 原因 → 怎么做
> **现象**：拿到 `hlm_` 开头的令牌后，把它填进别的登录表单、写进公开仓库、或在群里贴出来求助。
> **原因**：令牌是给 `docker login` 用的**凭据**（C20），不是控制台的账号密码；它的泄露面约等于账号本身。
> **怎么做**：只把它用在 `docker login`；**按机器分别创建令牌**，一台一个，便于日后单独处置；怀疑泄露就到控制台删除它。
> 说明：控制台的**账号信息 / 访问令牌 / 用量 / 镜像源**四个分区名来自界面文案，属**界面描述、非官方命名**。删除令牌之后的实际生效行为，见 3.5（未取证）。令牌的创建与用法见第 2 章 2.3 / 2.4。

#### 坑 ③：以为 compose / k8s 会自动生效

> [!warning] 现象 → 原因 → 怎么做
> **现象**：手动 `docker pull` 很快，但 `docker compose up` 或 Pod 启动时还是慢，甚至拉取失败。
> **原因**：前缀重写是**地址替换**，不是全局开关（C18）。compose 的 `image:`、manifest 的 `image:` 都是需要你亲手改的位置。
> **怎么做**：改文件——compose 见 3.1，k8s 见 3.2.2；改完**逐个确认没有漏网的 `image:`**，包括 init 容器、sidecar 这些容易忘的地方。

#### 坑 ④：`latest` 与缓存的误判

> [!warning] 现象 → 原因 → 怎么做
> **现象**：担心"加速器里存的是旧版本"；或者拉完 `:latest` 觉得行为没变，怀疑自己拿到了旧镜像。
> **原因**：带 tag 拉取时会**回源校验 digest**（C3，第 1 章 1.4 已逐字引用），所以"缓存里是旧版"通常不是原因。反过来，**上游不可用时**才可能回退旧缓存，而该时长窗口**无公开数值**（C22；对应开放问题 Q4，第 1 章 1.4 已标注，本章同样不给数字）。
> **怎么做**：要确定性就**用 digest 而不是 tag** 来固定版本；怀疑是服务侧问题时，先看状态页的 HLmirror 分组（第 1 章 1.1），再回头怀疑自己的本地配置。

#### 坑 ⑤：拿免费服务的限速当故障

> [!warning] 现象 → 原因 → 怎么做
> **现象**：某段时间拉取明显变慢，第一反应是"配置写错了"或"服务坏了"，开始反复重装、乱改 `daemon.json`。
> **原因**：控制台侧存在"月度配额"与"下载限速"这一类字段（C21），但**公开页面没有任何面向用户的数值承诺**——所以"变慢"未必是故障，也未必不是，单看现象判不出来。
> **怎么做**：先看状态页确认服务侧是否正常，再看控制台的「用量」分区（3.6）；**不要拿一个想象中的"平时速度"当基准**去判定故障。

---

### 3.4 私有镜像与鉴权：GHCR 私有仓库

第 2 章 2.5 速查表里的 `ghcr` 一行，解决的是 **公开**镜像的地址改写（官方示例用的 `immich` 就是公开镜像）。**私有**仓库是另一件事，而它在本轮研究里是一块明确的空白。

> [!warning] Q3：公开渠道零验证记录
> **GHCR 私有镜像能否经前缀加速、以及如何鉴权，本轮在公开渠道零验证记录。**
> 具体地说，本轮检查过的三处都没有相关说明：
> - 官方教程——只给了公开镜像的示例；
> - 控制台可见的界面文案——只有分区名与字段标签，没有私有仓库相关说明；
> - 服务前端实现细节——没有可支撑结论的内容。
>
> 因此本节的处理是：
> - **不写"可以"，也不写"不可以"**——两个方向都没有任何证据；
> - **不推测鉴权流程**（例如"应该在 `docker login` 时加某个参数"这类写法，本轮无据，**禁止编造**）；
> - **不把"厚浪支持 `ghcr` 后缀"推广成"厚浪支持 GHCR 私有镜像"**——这是两件事。

需要私有仓库鉴权的场景，本轮能给的只是一条**文字线索**（不是结论）：你 vault 内已有一篇 [[GHCR 推送镜像权限配置]]，讲的是 GHCR 侧的权限配置，可自行对照阅读。它与本节的 Q3 不是同一个问题，但相关。

> [!tip] 大白话
> `ghcr` 后缀解决的是「**门牌号改成厚浪的**」；私有镜像的问题是「**进这个门要不要出示证件、厚浪能不能替你出示**」。前者是**地址**问题，后者是**授权**问题。地址改得通，不代表授权也能顺过去——正因为这两件事必须分开看，本节才不敢替对方回答。

---

### 3.5 令牌生命周期：`docker logout` 与令牌吊销

> [!warning] Q5：未取证，本节不写任何行为推测
> 以下问题**本轮全部未取证**，因此**不给出结论**：
> - `docker logout mirror.houlang.cloud` 之后，本机凭据是否立即失效；
> - 在控制台删除 / 吊销令牌之后，已登录的机器会不会失效、多久失效；
> - 已经缓存在本地的镜像还能不能继续拉 / 继续用；
> - 正在进行的拉取会不会中断。
>
> 本节明确**禁止"按常识补全"这些答案**。哪怕某个说法听上去天经地义，它在本轮**没有一手依据**——写进笔记就是把猜测伪装成事实。想知道实际行为，只能自己实测：在控制台删掉一个不影响生产的令牌，观察目标机器上的表现。

能在界面层面确认的只有一件小事（来源：前端 bundle，属**实现细节**）：控制台的「访问令牌」分区里存在「**删除访问令牌**」这条操作文案 <!-- S4b -->。**按钮存在，不等于我们知道点下去之后会发生什么**——这中间的空白，就是 Q5。

> [!tip] 大白话
> 这一节像一份**没做过的实验记录**。你知道实验室里有一台叫「删除访问令牌」的机器，也知道它就在那儿；但按下去会亮哪个灯、机器多久后停——**没人记录过**。与其编一个"应该会……"，不如把"没记录"老老实实写出来。

---

### 3.6 配额与限速：只有字段名，没有数字

这一节的全部内容，就是「**有哪些字段名**」和「**没有什么**」。

控制台「用量」分区相关的界面文案 <!-- S4b -->（属**界面描述、非官方命名**）出现过这几个词：

| 出现位置 | 文案 |
| --- | --- |
| 用量页字段 | 「月度配额」 |
| 用量页字段 | 「配额窗口 …重置」 |
| 速率字段 | 「不限速」 |

服务前端实现细节里，与之对应的字段名是 `monthly_quota_bytes` 与 `download_rate_limit_bps`。<!-- S4 --> <!-- C21 -->

把「知道」和「不知道」并排放一次：

| 我们知道的 | 我们不知道的 |
| --- | --- |
| 存在"月度配额"这个概念（字段 `monthly_quota_bytes`） | 免费账号的配额具体是多少 |
| 存在"下载限速"这个概念（字段 `download_rate_limit_bps`），且有「不限速」这一状态 | 限速的具体速率是多少 |
| 配额有"窗口"，并会重置（界面文案「配额窗口 …重置」） | 窗口的具体长度与重置时点 |
| 控制台有「用量」分区可以查看 | 数值的呈现形式（进度条 / 百分比 / 剩余字节） |

> [!warning] Q2：无公开口径，以控制台实际为准
> 本轮在**公开页面**（含官方教程、产品页、控制台可见文案）中，**没有找到任何面向用户的配额或限速数值承诺**。因此：
> - 本笔记**不出现任何配额、限速、时长的具体数字**；
> - 需要知道实际额度，**只能以控制台「用量」分区的显示、以及你账号的实际情况为准**；
> - 任何"免费版每月多少""限速多少 MB/s"之类的说法，**没有来源支撑，一律不得写入**。

> [!tip] 大白话
> 限速像**高峰期地铁**：确实会挤，但**站里没公布时刻表**。你能做的是抬头看一眼站台的显示屏（控制台的「用量」分区），而不是拿一个想象中的"平时速度"去反推"今天是不是坏了"。

---

### 3.7 排错入口清单

遇到问题时的**排查顺序**。本节只写"先查什么"，**不写因果结论**——凡是涉及"到底为什么"的判断，上文都已按"未取证 / 无公开口径"如实标注过，不在这里补全。

| 现象 | 先查什么 | 再查什么 |
| --- | --- | --- |
| **登录失败**（没看到 `Login Succeeded`） | 令牌是否复制完整、有没有多余空格；命令形态是否为 `docker login -u <邮箱> -p <hlm_令牌> mirror.houlang.cloud`（第 2 章 2.4） | 成功标志固定是 `Login Succeeded`（C17）。拿不到它，就说明这一步没过，**不要继续往下排** |
| **拉取失败** | 镜像地址是否已按第 2 章 2.5 的速查表改对（后缀对不对、路径层级有没有少） | 看状态页 `status.houlang.cloud` 的 HLmirror 分组（第 1 章 1.1）确认服务侧是否在线；若是网络层面的超时，对照 vault 内既有的 [[docker镜像拉取DNS解析超时排错]] |
| **变慢** | 控制台「用量」分区（见 3.6） | 看状态页；在动任何配置之前，先排除 3.3 坑 ⑤ 说的限速误判 |

> [!summary] 三条原则
> 1. **登录没过，别排拉取**——这两步是串联的，前一步没过，后面所有现象都没有诊断价值。
> 2. **先确认真实原因，再改配置**。三类现象里，"变慢"最容易在原因不明时被误改成 `daemon.json`——那是第 1 章 1.3 讲的另一个机制，改了不解决问题。
> 3. **按证据层级判断说法**。本笔记多处标注了"未取证 / 无公开口径 / 零验证记录"，你排错时也该用同一把尺子去看网上那些"官方承诺……"的说法。

---

### 本章小结

- 前缀重写的代价落在**文件**上：compose 的每一处 `image:`（3.1）、k8s manifest 的每一处 `image:`（3.2.2）都要手改，**它不是全局生效**（C18）。
- **k8s 没有原生的「镜像前缀重写」API**（C14：本轮未找到任何一手出处）。k8s 下的两条路是「改 manifest 里的 `image:`」或「改节点容器运行时配置」；后者旧的 `registry.mirrors` 写法**已废弃**（C10），新写法是 `config_path` 指向 `hosts.toml` 目录，`capabilities`（C11）与省略 `server`（C12）各有用意。
- 五个坑编号固定：① 填进 `registry-mirrors`（C1 / C18）② 令牌当密码到处贴（C20）③ 以为 compose / k8s 自动生效（C18）④ `latest` 与缓存的误判（C3 / C22）⑤ 拿限速当故障（C21）。
- 三块空白，都**不升格为结论**：GHCR **私有**镜像（Q3，公开渠道零验证记录）、令牌生命周期（Q5，未取证）、配额与限速数值（Q2，无公开口径）。**本章没有出现任何配额 / 限速 / 时长的具体数字。**

### 本章结束之后

三章到此结束。日常回查请直接走**第 2 章 2.8 的速查卡**，不必重读全文；只有当"机制上想不通"时，再回第 1 章补齐认知。如果之后要处理私有镜像鉴权或令牌轮换，记得先看 3.4 与 3.5——那两节标的是"空白"，不是"结论"。
