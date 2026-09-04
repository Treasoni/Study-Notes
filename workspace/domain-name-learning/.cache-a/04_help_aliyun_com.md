---
url: "https://help.aliyun.com/zh/dns/basic-concepts-dns2-0"
title: "DNS的基本概念-云解析DNS(DNS)-阿里云帮助中心"
scraped_at: 2026-09-04T04:45:06+00:00
---

输入文档关键字查找
本文为您介绍云解析 DNS 的基础概念，帮助您了解相关知识，以便更好地理解和使用产品功能。
## **DNS**
DNS（Domain Name System，域名系统）即“域名系统”。DNS是整个互联网服务的基础系统之一，同时也是企业内网服务的重要基础服务系统之一，负责将人们访问的互联网域名和企业内网域名转换为IP地址，这一转换的过程叫做“域名解析”， 所以DNS又称“域名解析系统”，相当于网络访问的指路牌。DNS作为域名和IP地址相互映射的一个分布式数据库，能够使用户更方便的访问网络资源和网络服务，而不用去记住能够被机器直接读取的IP数串。DNS协议运行在UDP协议之上，使用端口号53。DNS从服务的网络环境来区分，分为公网DNS和内网DNS。DNS从解析链路扮演的功能角色来区分，分为权威DNS和递归 DNS。
## **域名的分层结构**
域名采用层次树状结构命名，每个连接在互联网上的主机或路由器，都有唯一的层次结构名字。域名由标号（label）序列组成，各标号之间用点（小数点）隔开。关于域名层次结构如下图：
**举例说明**
  * `.com`是**顶级域名；**
  * `aliyun.com`是**主域名** ，也叫二级域名；
  * `example.aliyun.com`、`www.aliyun.com`是**子域名** ，也叫三级域名；
  * `test.example.aliyun.com`是**子域名的子域** ，也叫四级域名。


## **DNS服务器层级**
DNS解析过程涉及4个层级的DNS服务器，分别如下：  
| **服务器类型**  |  
| --- |  
| **服务器类型**  |  
| --- |  
| 根域名服务器  | 英文全称：Root Name Server，简称Root Server。本地域名服务器在本地查询不到解析结果时，则第一步会向它进行查询，并获取顶级域名服务器的IP地址。  |  
| 顶级域名服务器  | 英文全称：Top-Level Domain Name Server，简称：TLD Server。负责管理在该顶级域名服务器下注册的主域名，例如“example.com”，.com则是顶级域名服务器，在向它查询时，可以返回主域名“example.com”所在的权威域名服务器地址。  |  
| 权威域名服务器  | 英文全称：Authoritative Name Server，简称NS。在特定区域内具有唯一性，负责维护该区域内的域名与IP地址之间的对应关系。例如云解析DNS的[公网权威解析](https://help.aliyun.com/zh/dns/jx-public-network-authority-analysis/)，您可在此[添加解析记录](https://help.aliyun.com/zh/dns/pubz-add-parsing-record)，最终它会将配置的ip记录返回给用户。  |  
| 本地域名服务器  | 英文全称：Local DNS Server，简称Local DNS。本地域名服务器是响应来自客户端的递归请求，并最终跟踪直到获取到解析结果的DNS服务器。例如用户本机自动分配的DNS、运营商ISP分配的DNS、谷歌/223.5.5.5公共DNS等。  |  
每个层级的域名都有其专属的域名服务器，最顶层是根域名服务器。每一层的域名服务器都存储着下级域名服务器的IP地址，从而能够逐级进行查询。
## **DNS解析过程**
通过域名`example.com`访问网站的域名解析过程如下。
  1. 用户在Web浏览器中输入`example.com`， 向本地域名服务器发起查询请求。若本地域名服务器存在缓存的解析数据，则直接将域名`example.com`对应的IP地址返回给Web浏览器，跳至步骤9。若本地域名服务器没有查到缓存的解析数据，则继续步骤2。
  2. 本地域名服务器向根域名服务器进行查询。 
  3. 根域名服务器将`.com`顶级域名服务器的地址，返回给本地域名服务器。
  4. 本地域名服务器向`.com`顶级域名服务器发起`example.com`的查询请求。
  5. .com顶级域名服务器将为`example.com`提供权威解析的权威域名服务器地址，返回给本地域名服务器。 
  6. 本地域名服务器向权威域名服务器发起查询请求。
  7. 权威域名服务器将域名`example.com`对应的IP地址，返回给本地域名服务器。
  8. 本地域名服务器最后把查询的IP地址响应给Web浏览器。
  9. Web浏览器通过IP地址访问网站服务器。
  10. 网站服务器返回网页信息。


## **递归解析（Recursive Query）**
DNS服务器帮你把整个查询流程走到底，中间任何一步都由这台服务器去处理，最后直接把最终结果返回给你。如：
  * 客户端将“请帮我查出www.example.com的IP”递交给本地DNS（递归服务器）。
  * 递归服务器自己如果不知道答案，会去根DNS、TLD、权威DNS不断发问，并跟进每一步；直到获得最终答案。
  * 用户只需要等递归服务器给出最后的解析结果即可。


**特点**
  * 用户只需问一次、等一次。
  * 递归服务器压力较大，需要走完整查询流程。
  * 这是客户端和本地DNS之间最常见的方式。


**常见应用**
  * 普通用户/PC/浏览器 ：只有递归查询，不处理迭代查询。
  * 本地DNS服务器（如你的宽带运营商、公网8.8.8.8、公司内网DNS）：通常承担递归解析的角色，对外（向根、TLD、权威DNS）发起迭代查询。
  * 公共DNS服务器：对用户递归，对更上级DNS迭代。


## **迭代解析（Iterative Query）**
DNS服务器只帮你查“它知道的下一步线索”，如果自己没有答案就告诉你下一步去哪问，用户必须自己去完成整个查询流程。如：
  * 客户端问本地DNS：“www.example.com的IP是多少？”
  * 本地DNS不知道，查问根DNS。根DNS不直接回答IP，而是答：“你去问TLD服务器”，这里的根DNS则在进行迭代解析。
  * 本地DNS问TLD服务器，TLD告诉你“去找这个权威DNS”，这里的TLD服务器则在做迭代解析。
  * 直到找到权威服务器，获取最终结果。


**特点**
  * 每一步都需要客户端自己去问。
  * 服务器压力较小，但客户端负担大（通常不这样用）。


**常见应用**
  * 根DNS服务器、TLD服务器、权威DNS服务器。
  * 企业、学校等自建的DNS服务器。
  * 公共DNS服务器：对用户递归，对更上级DNS迭代。


## **DNS缓存**
DNS缓存是将解析数据存储在靠近发起请求的客户端的位置，也可以说DNS数据是可以缓存在任意位置，最终目的是以此减少递归查询过程，可以更快的让用户获得请求结果。
## **TTL**
英文全称Time To Live ，这个值是告诉本地域名服务器，域名解析结果可缓存的最长时间，缓存时间到期后本地域名服务器则会删除该解析记录的数据，删除之后，如有用户请求域名，则会重新进行递归查询/迭代查询的过程。关于如何修改解析记录的 TTL 值，请参见[如何修改 TTL 时间](https://help.aliyun.com/zh/dns/pubz-how-to-modify-ttl-time)。
## **解析记录**
解析记录用于定义域名如何被解析。在云解析 DNS 中添加域名后，需要配置解析记录来指定该域名指向的目标地址，例如 IPv4 地址、IPv6 地址、另一个域名或邮件服务器地址等。访问域名时，DNS 系统根据对应的解析记录返回目标地址，完成域名到目标地址的映射。
每条解析记录由以下核心字段组成，共同决定域名的解析行为。  
|   |  
| --- |  
| **字段名称**  |  
| --- |  
| **主机记录**  | 域名前缀部分。例如，对于域名 `www.example.com`，主机记录为 `www`；若设置为 `@`，表示主域名本身；若设置为 `*`，表示泛解析，匹配所有未显式配置的子域名。  |  
| **记录类型**  | 定义解析记录的功能，决定记录值的格式和用途。常见类型包括 A、AAAA、CNAME、MX、TXT 等，不同类型的记录值格式各不相同。  |  
| **解析请求来源** （线路）  | 定义哪些访问来源使用本条解析记录。支持系统预设线路（如默认、联通、电信、移动等）和自定义线路。当记录类型为 URL 转发（显性 URL 或隐性 URL）时，线路锁定为「默认」，不可修改。  |  
| 解析记录在本地 DNS 服务器中的缓存时间，单位为秒。TTL 值越小，记录修改后生效越快，但 DNS 查询频率也越高。权威版支持自定义输入 TTL 秒数，推荐值为 60 秒（企业高级版/旗舰版）或 600 秒（其他版本）；内网版需从固定选项中选择。  |  
| **记录值负载策略**  | 当同一主机记录和记录类型配置了多条记录值时，决定如何分配访问流量。支持「轮询」和「权重」两种模式。权重模式仅在快速区且记录类型为 A、AAAA、CNAME 或 ALIAS 时可用。当记录类型为 CNAME 或 ALIAS 时，强制开启权重模式。  |  
| 权重模式下的流量分配比例，取值范围 0～100。数值越大，分得的访问流量越多。  |  
| MX 和 SRV 记录显示，取值范围 1～50。数值越小优先级越高。SRV 记录的优先级范围为 0～65535。  |  
| **启用状态**  | 控制该解析记录是否生效，支持「启用」和「暂停」两种状态。暂停后，该记录不再参与域名解析。  |  
| 用于标识和区分不同解析记录的备注信息，方便管理。  |  
云解析 DNS 支持以下解析记录类型。  
|   |   |  
| --- | --- |  
| **记录类型**  | **用途说明**  |  
| --- | --- |  
| 将域名指向一个 IPv4 地址。例如，将 `www.example.com` 指向 `192.0.2.1`。  |  
| AAAA  | 将域名指向一个 IPv6 地址。  |  
| CNAME  | 将域名指向另外一个域名。当目标域名 IP 地址变化时，只需修改目标域名的解析记录，无需修改当前域名的配置。  |  
| ALIAS  | 将域名指向另外一个域名，是根域名 CNAME 的替代方案。与 CNAME 不同，ALIAS 记录可以与同域名的其他记录类型共存。该类型受版本控制，企业高级版和旗舰版可用。  |  
| 将子域名指定给其他 DNS 服务器解析，常用于域名托管或子域名委派。  |  
| 将域名指向邮件服务器地址，用于电子邮件系统的邮件交换。  |  
| TXT  | 文本记录，最大长度 512 字符。通常用于 SPF 记录（反垃圾邮件校验）、域名所有权验证等场景。  |  
| SRV  | 标识提供特定服务（如 VoIP、即时通讯）的服务器，包含优先级、权重、端口和目标地址四个子字段。  |  
| CAA  | CA 证书颁发机构授权记录，用于指定允许为该域名颁发证书的证书颁发机构（CA），包含 flag、tag 和 value 三个子字段。  |  
| SVCB  | 服务绑定记录，用于声明访问服务时使用的端点和参数。支持别名模式和服务模式。  |  
| HTTPS  | 约定 HTTPS 服务的安全建连信息，与 SVCB 记录类似，专用于 HTTPS 服务。  |  
| TLSA  | 基于 DANE 协议，将 TLS 证书或公钥指纹与域名绑定并写入 DNS。客户端在建立 TLS 连接时，可通过 DNS 验证证书的真实性。  |  
| 显性 URL（REDIRECT_URL）  | 将域名重定向到另外一个地址，浏览器地址栏会显示重定向后的目标地址。记录值格式为 `301|目标URL`（永久重定向）或 `302|目标URL`（临时重定向）。该类型仅支持「默认」线路。  |  
| 隐性 URL（FORWARD_URL）  | 与显性 URL 类似，但浏览器地址栏仍显示原域名，隐藏真实目标地址。  |  
| PTR  | 将 IP 地址指向一个域名，即反向解析。仅在反向解析区域（`in-addr.arpa` 结尾的域名）中可用。  |  
PTR 记录仅在反向解析区域（以 `in-addr.arpa` 结尾的域名）中显示。ALIAS 记录类型受版本控制，旗舰版和企业高级版可用，免费版中该选项被禁用。内网域名解析支持的记录类型包括：A、AAAA、CNAME、MX、TXT、SRV、PTR。
## **IPV4、IPV6双栈技术**
双栈英文Dual IP Stack，就是在一个系统中可同时使用IPv6/ IPv4这两个可以并行工作的协议栈。
## **DNS Query Flood Attack**
指域名查询攻击，攻击方法是通过操纵大量傀儡机器，发送海量的域名查询请求，当每秒域名查询请求次数超过DNS服务器可承载的能力时，则会造成解析域名超时从而直接影响业务的可用性。
## **URL转发**
英文 Url Forwarding，也可称地址转向，它是通过服务器的特殊设置，将一个域名指向到另外一个已存在的站点。
## **edns-client-subnet**
google提交了一份DNS扩展协议，允许DNS resolver传递用户的IP地址给authoritative DNS server。
## **DNSSEC**
域名系统安全扩展（DNS Security Extensions），简称DNSSEC。它是通过数字签名来保证DNS应答报文的真实性和完整性，可有效防止DNS欺骗和缓存污染等攻击，能够保护用户不被重定向到非预期地址，从而提高用户对互联网的信任。
## **移动解析HTTPDNS相关概念**
### **应用终端**
指专门用于网络接入的终端设备和应用服务，包括并不限于移动终端、物联网终端、APP应用等。
### **DoH（DNS-over-Https）**
用来加密的DNS请求流量，阿里云公共DNS通过RFC 8484指定的经过TLS加密的HTTP连接提供DNS解析。
### **DoT（DNS-over-TLS）**
用来加密的DNS请求流量，阿里云公共DNS通过RFC 7858指定的经过TLS加密的TCP连接提供DNS解析。
该文章对您有帮助吗？
  * 本页导读 （1）
  * 域名的分层结构
  * DNS服务器层级
  * DNS解析过程
  * 递归解析（Recursive Query）
  * 迭代解析（Iterative Query）
  * DNS缓存
  * IPV4、IPV6双栈技术
  * DNS Query Flood Attack
  * URL转发
  * edns-client-subnet
  * DNSSEC
  * 移动解析HTTPDNS相关概念
  * 应用终端
  * DoH（DNS-over-Https）
  * DoT（DNS-over-TLS）


一站式为企业和开发者提供大模型能力体系，大模型原生应用以及最佳解决方案，助力云上开发者轻松完成 AI 落地。
#### [千问AI平台 千问官方 MaaS 平台，为开发者和 Agent 而生，新用户赠送 1 亿 + tokens 额度](https://www.qianwenai.com/)
#### [AI 体验馆 免费体验前沿云上 AI 应用，开启智能创新](https://www.aliyun.com/exp/)
#### 大模型
#####  文本生成
###### [ Qwen3.8-Max _HOT_ 0902 快照版本重磅更新，智能体时代全能旗舰模型](https://platform.qianwenai.com/try-ai?models=qwen3.8-max-0902)###### [ Qwen3.8-Flash _NEW_ 百万级上下文窗口，一次性处理超长文档和代码仓库](https://platform.qianwenai.com/try-ai?models=qwen3.8-flash)###### [ Qwen3-VL-Plus 视觉 Coding、空间感知、多模态思考等全面升级](https://platform.qianwenai.com/try-ai?models=qwen3-vl-plus)
###### [ Kimi-K3 Kimi 最新旗舰模型，长程编程与推理利器](https://www.qianwenai.com/models/kimi%2Fkimi-k3)###### [ Deepseek-v4-pro 旗舰 MoE 大模型，百万上下文与顶尖推理能力](https://platform.qianwenai.com/try-ai?models=deepseek-v4-pro)###### [ GLM-5.2 1M上下文，专为长程任务能力而生](https://platform.qianwenai.com/try-ai?models=glm-5.2)
#####  图片和视频生成
###### [ Wan3.0-Video 四模态全能参考，多种创作一站支持](https://platform.qianwenai.com/try-ai?scene=video&models=wan3.0-video)###### [ Qwen-Image-3.0-Pro _NEW_ 细节真实，知识厚实，让图像生成真正成为可落地的生产力工具](https://platform.qianwenai.com/try-ai/chat?models=qwen-image-3.0-pro)###### [ HappyHorse-1.1-T2V 让文字生成流畅细腻的高质量视频](https://platform.qianwenai.com/try-ai?models=happyhorse-1.1-t2v)
#####  语音识别与合成
###### [ Qwen3-TTS-Flash  离线语音合成大模型，多语言方言自适应，低延迟高稳定](https://platform.qianwenai.com/try-ai?scene=tts&models=qwen3-tts-flash)###### [ Cosyvoice-V3-Flash 高表现力语音合成大模型，语音克隆听感自然](https://platform.qianwenai.com/try-ai?scene=tts&models=cosyvoice-v3-flash)###### [ Fun-ASR 支持中英文自由切换，具备更强的噪声鲁棒性](https://platform.qianwenai.com/try-ai?models=fun-asr)
##### [ 千问AI平台-Token Plan _NEW_ 个人版上线、团队版降价；千问3.8-Max首发发尝鲜](https://www.qianwenai.com/benefits/tokenplan)##### [千问AI平台-模型体验 在线体验全尺寸、多种模态的模型效果](https://platform.qianwenai.com/try-ai)##### [Happy 系列大模型 新一代 AI 视频生成模型，深度适配广告营销等场景](https://www.aliyun.com/product/happymodel)
##### [大模型服务平台百炼-应用模版 丰富多元化的应用模版和解决方案](https://bailian.console.aliyun.com/?tab=app#/app-market/newTemplate)##### [大模型服务平台百炼-智能体 灵活可视化地构建企业级 Agent](https://bailian.console.aliyun.com/?tab=app#/app-center)##### [人工智能平台 PAI AI Native 的算法工程平台，一站式完成建模、训练、推理服务部署](https://www.aliyun.com/product/bigdata/learn)
#### 大模型原生应用
##### [ Qoder _HOT_ 面向真实软件的智能体编程平台](https://www.qianwenai.com/agents/qoder)##### [万镜一刻 AIGC视频创作平台，创意直达成片](https://www.qianwenai.com/agents/wonderclip)[ 智能客服平台，对话机器人、对话分析、智能外呼](https://www.qianwenai.com/agents/voicepica)
##### [ 千问办公 _NEW_ 一站式AI生产力平台](https://www.qianwenai.com/agents/qwenwork)##### [万有无界 企业级人与Agent协作平台，接入和调度多个数字员工](https://www.qianwenai.com/agents/wanyou)[ 云端极速 AI 应用创作平台](https://www.qianwenai.com/agents/meoo)
#### 大模型解决方案
##### [快速部署 Dify，高效搭建 AI 应用 依托云原生高可用架构,实现Dify私有化部署](https://www.aliyun.com/solution/tech-solution/rapidly-deploy-dify-to-accelerate-ai-application-development)##### [10 分钟在聊天系统中增加一个 AI 助手 在企业官网、通讯软件中为客户提供 AI 客服](https://www.aliyun.com/solution/tech-solution/build-a-chatbot-for-your-website-or-chat-system)
##### [10分钟微调：让0.6B模型媲美235B模型 用1%尺寸在特定领域达到大模型90%以上效果](https://www.aliyun.com/solution/tech-solution/qwen3-distill)##### [即刻拥有 DeepSeek-R1 满血版 多种方案随心选，轻松解锁专属 DeepSeek](https://www.aliyun.com/solution/tech-solution/deepseek-r1-for-platforms)
##### [多模态数据信息提取 从文本、图片、视频中提取结构化的属性信息](https://www.aliyun.com/solution/tech-solution/information-extraction)##### [超强辅助，Bolt.diy 一步搞定创意建站 通过自然语言交互简化开发流程,全栈开发支持](https://www.aliyun.com/solution/tech-solution/bolt-diy)
##### [与 AI 智能体进行实时音视频通话 构建支持视频理解的 AI 音视频实时通话应用](https://www.aliyun.com/solution/tech-solution/real-time-interaction)##### [构建大模型应用的安全防护体系 通过阿里云安全产品对 AI 应用进行安全防护](https://www.aliyun.com/solution/tech-solution/build-large-model-application-security-system)
精选产品[人工智能与机器学习](https://ai.aliyun.com/)[计算](https://www.aliyun.com/product/list/ecs)[容器](https://www.aliyun.com/product/aliware/containerservice)[存储](https://www.aliyun.com/storage/storage?spm=5176.19720258.J_2686872250.30.3f0e4ff6AwBQKs)[网络与CDN](https://www.aliyun.com/product/network/network)[安全](https://www.aliyun.com/product/list/security%20)[中间件](https://www.aliyun.com/product/list/aliware)[数据库](https://www.aliyun.com/product/outline/index?spm=5176.19720258.J_2686872250.45.3f0e4ff6AwBQKs)[大数据计算](https://www.aliyun.com/product/bigdata/apsarabigdata)媒体服务[企业服务与云通信](https://www.aliyun.com/product/list/ent-cmc)域名与网站终端用户计算Serverless[开发工具](https://www.aliyun.com/product/list/developertools)[迁移与运维管理](https://www.aliyun.com/product/list/operation-mainenance)[专有云](https://apsara-stack.aliyun.com)
#### 精选产品
##### [ 大模型服务平台百炼 _大模型_ 大模型服务与应用平台](https://www.aliyun.com/product/bailian)##### [ 千问大模型 _大模型_ 多元化、高性能、安全可靠的大模型服务](https://www.aliyun.com/product/tongyi)##### [无影云电脑 随时随地安全接入的云上超级电脑](https://www.aliyun.com/product/ecs/gws)##### [云解析DNS 覆盖公网/内网、递归/权威、移动APP等全场景解析服务](https://www.aliyun.com/product/dns)##### [大数据开发治理平台 DataWorks Data Agent 驱动的一站式 Data+AI 开发治理平台](https://www.aliyun.com/product/dide)
##### [域名与网站 提供智能易用的域名与建站服务](https://wanwang.aliyun.com/)##### [对象存储 OSS 稳定、安全、高性价比、高性能的云存储服务](https://www.aliyun.com/product/oss)##### [ 人工智能平台 PAI _大模型_ 一站式AI开发、训练和推理服务](https://www.aliyun.com/product/bigdata/learn)##### [Qoder CN 基于千问大模型等，支持代码智能生成、研发智能问答](https://www.aliyun.com/product/lingma)##### [容器服务 Kubernetes 版 ACK 提供一站式管理容器应用的 K8s 服务](https://www.aliyun.com/product/kubernetes)
##### [云服务器 ECS 安全可靠、弹性可伸缩的云计算服务](https://www.aliyun.com/product/ecs)##### [云数据库 RDS 全托管，含MySQL、PostgreSQL、SQL Server、MariaDB多引擎](https://www.aliyun.com/product/rds)##### [短信服务 国内短信简单易用，安全可靠，秒级触达，全球覆盖200+国家和地区。](https://www.aliyun.com/product/sms)##### [云原生大数据计算服务 MaxCompute 面向分析的企业级SaaS模式云数据仓库](https://www.aliyun.com/product/maxcompute)##### [GPU 云服务器 基于神龙架构的弹性GPU算力服务](https://www.aliyun.com/product/egs)
##### [轻量应用服务器 快速构建应用程序和网站，即刻迈出上云第一步](https://www.aliyun.com/product/swas)##### [数字证书管理服务（原SSL证书） 实现全站HTTPS，呈现可信的WEB访问](https://www.aliyun.com/product/cas)##### [Qoder 面向真实软件的智能体编程平台](https://www.aliyun.com/product/qoder)##### [云原生数据库 PolarDB 100%兼容MySQL、PostgreSQL，兼容Oracle，支持集中和分布式](https://www.aliyun.com/product/polardb)
精选解决方案[AI](https://www.aliyun.com/solution/tech-solution/ai)互联网应用开发大数据现代化应用安全网络可观测上云与迁云[企业出海](https://www.aliyun.com/goglobal)政企业务
#### 精选解决方案
##### [ DeepSeek Harness：构建插件化智能体 _NEW_ 快速部署 DeepSeek Harness 开源智能体](https://www.aliyun.com/solution/tech-solution/deepseek-harness)##### [Qwen Audio：打造专属 AI 语音助手 Qwen-Audio-3.0-Realtime 端到端实时语音角色扮演](https://www.aliyun.com/solution/tech-solution/qwen-audio)##### [ 一键部署幻兽帕鲁游戏服务器 _HOT_ 一键购买专属联机服务器，轻松开启游戏](https://www.aliyun.com/solution/tech-solution/palworld)##### [漫剧工坊：一站式动画创作平台 快速生产连贯的高质量长漫剧](https://www.aliyun.com/solution/tech-solution/use-bailian-to-intelligently-create-comics)
##### [ MiniMax-H3：一键部署，即刻创作 _NEW_ 通过计算巢快速部署 MiniMax H3 全模态视频创作环境。](https://www.aliyun.com/solution/tech-solution/minimax-h3-deploy-in-one-click-create-instantly)##### [一句话生成原生可编辑精美 PPT 文稿 输入一句话想法, 轻松生成专业的 PPT](https://www.aliyun.com/solution/tech-solution/vibe-ppt)##### [HappyHorse 打造一站式影视创作平台 可视化编排打通从文字构思到成片全链路闭环](https://www.aliyun.com/solution/tech-solution/infinite-canvas)##### [快速拥有专属 OpenClaw 让AI从“聊天伙伴”进化为能干活的“数字员工”](https://www.aliyun.com/solution/tech-solution/clawdbot)
##### [千问办公，解锁你的工作新方式 企业级Agent产品，直接交付可用成果](https://www.aliyun.com/solution/tech-solution/qwenwork)##### [GLM-5.2：长任务时代开源旗舰模型 真正可用的 1M 上下文,一次完成代码全链路开发](https://www.aliyun.com/solution/tech-solution/glm-for-platforms)##### [Hermes Agent，打造自进化智能体 自主进化，持久记忆，越用越聪明](https://www.aliyun.com/solution/tech-solution/hermes-agent)##### [低代码高效构建企业门户网站 以可视化方式快速构建移动和 PC 门户网站](https://www.aliyun.com/solution/tech-solution/build-a-website)
##### [睿译宝，AI翻译排版一步到位 上传文档即自动完成翻译和格式还原](https://www.aliyun.com/solution/tech-solution/rui-yi-bao)##### [即刻拥有 DeepSeek-V4-Pro 轻松解锁专属 DeepSeek-V4-Pro ](https://www.aliyun.com/solution/tech-solution/deepseek-v4-for-platforms)##### [ 5 分钟轻松部署专属 QwenPaw _HOT_ 从聊天伙伴进化为能主动干活的本地数字员工](https://www.aliyun.com/solution/tech-solution/copaw)##### [10 分钟搭建微信、支付宝小程序 高效部署网站，快速应用到小程序](https://www.aliyun.com/solution/tech-solution/develop-your-wechat-mini-program-in-10-minutes)
上云优选，普惠好价，为开发者和企业提供多款超值优选上云必备产品；超 140 款免费试用产品；初创企业最高可得 100 万抵扣金。
#### 普惠上云
##### [普惠上云 官方力荐 云服务器38元/年起，超值低价云产品抢先购](https://www.aliyun.com/benefit/select/cloud-discount)##### [官方推荐返现计划 推荐新用户得奖励，单订单最高返9万](https://dashi.aliyun.com/)##### [云工开物 高校专属算力普惠，学生认证享300元代金券](https://university.aliyun.com/)
#### 免费试用
##### [解决方案免费试用 新老同享 最高领取价值200元试用点，立即开启云上创新](https://www.aliyun.com/solution/free)##### [AI 产品 免费试用 1亿+ 大模型 tokens 和 30+ 款产品免费体验](https://free.aliyun.com/product/ai)##### [140+云产品 免费试用 产品新客免费试用，最长12个月](https://free.aliyun.com/)##### [大模型ACA认证体验 助力企业全员 AI 认知与能力提升](https://edu.aliyun.com/learning/topic/llm-free-trial)
#### AI 特惠
##### [智启 AI 普惠权益 至高享 1亿+免费 tokens，加速 Al 应用落地](https://www.aliyun.com/benefit/scene/ai-discount)##### [阿里云 OPC 创新助力计划 至高百万元 Token 补贴，加速一人公司成长](https://opc.aliyun.com/)##### [ Token Plan 模型订阅计划 _NEW_ Qwen3.8-Max 首发尝鲜，限时加量 10 倍，夜间低至2折](https://www.qianwenai.com/benefits/tokenplan)##### [万小智 AI 建站低至 15元/月 送.CN域名，送备案服务码 ](https://opc.aliyun.com/activity#J_1)##### [ Night Plan 支持 Qwen 3.8-Max _NEW_ 夜间 5 折，Qwen/Meoo/TokenPlan 客户专享](https://www.aliyun.com/benefit/client/nightplan)##### [万镜一刻，视频创作低至39元/月 AI 短剧与营销素材高效产出](https://www.aliyun.com/benefit/scene/yikeai)
#### AI 场景体验
##### [AI 电商营销 从图文生成到视频创作，一键激活电商全链路生产力](https://www.aliyun.com/benefit/aiuse/e-commerce)##### [AI Coding 描述需求，智能体自主编程，端到端独立完成](https://www.aliyun.com/benefit/scene/qoder)##### [AI 广告创作 图文、视频一站生成，高效打造优质广告素材](https://www.aliyun.com/benefit/aiuse/ad)##### [AI 建站 0 代码专业建站，无忧落地极速上线](https://www.aliyun.com/benefit/client/website?tid=service-overview)##### [AI 办公 AI智能应用，一键激活高效办公新体验 ](https://www.aliyun.com/product/qwenwork)##### [AI 短剧/漫剧 AI助力短剧漫剧创作，剧本、分镜、视频高效生成](https://www.aliyun.com/benefit/scene/playlet)##### [智能客服 自动承接线索、识别商机，让客服更高效、服务更出色。 ](https://www.aliyun.com/benefit/scene/callcenter)##### [企业知识库 一键入库随问随引，RAG新客享30天免费额度](https://www.aliyun.com/benefit/client/office)
#### AI 活动
##### [AI 生产力先锋 先锋实践拓展 AI 生产力的边界](https://www.aliyun.com/activity/ai-seminar/home)##### [飞天发布时刻 所见，即是所愿](https://summit.aliyun.com/apsaramoment)##### [AI 实训营 从基础到进阶，Agent 创客手把手教你](https://www.aliyun.com/benefit/aihands-on/mainpage)
#### 创新加速
##### [上云场景组合购 覆盖90%+业务场景，专享组合折扣价](https://www.aliyun.com/benefit/client/package)##### [云聚AI 严选权益  精选AI产品，从模型到应用全链提效](https://www.aliyun.com/benefit/client/index)##### [AI 用量加速计划 新老同享，达量后返](https://www.aliyun.com/benefit/client/maas)
提供灵活的计费方式和清晰的计费规则，满足不同的业务场景需求；支持自助估算价格、高效采购；专业的成本管理工具，持续优化云上成本。
#### [产品定价 了解云产品的定价详情](https://www.aliyun.com/price/detail)#### [云上成本管理 管理和优化成本](https://www.aliyun.com/price/cost-management)
#### [价格计算器 自助选配和估算价格](https://www.aliyun.com/price/product)#### [价格优势 推动算力普惠，释放技术红利](https://www.aliyun.com/price/advantage)
#### [配置报价器 一站式生成采购清单，支持单品或批量购买](https://www.aliyun.com/price/cpq/list)
##### [阿里云 OPC 创新助力计划 至高可申请百万元 Token 补贴，五大权益加速 OPC 成功](https://opc.aliyun.com/)
提供与阿里云能力融合和互补的优质伙伴产品和服务，满足企业上云和各类业务应用开发需求。
[网站建设](https://market.aliyun.com/xinxuan/webdesign)[多端小程序](https://market.aliyun.com/xinxuan/application/miniapps)[Salesforce 国际版订阅](https://market.aliyun.com/products/56790007/cmfw00037956.html?innerSource=search_salesforce#sku=yuncode3195600001)[友盟天域](https://market.aliyun.com/products/56842011/cmfw00040027.html)[观测云](https://market.aliyun.com/products/56838014/cmgj00053362.html)[Tuya 物联网平台阿里云版](https://www.aliyun.com/research/tuya)[蓝凌 OA](https://market.aliyun.com/xinxuan/lanling-oa)[电子合同](https://market.aliyun.com/xinxuan/wyy-2023)[畅捷通](https://market.aliyun.com/products/56764034/cmgj00042861.html)[Tableau 订阅](https://market.aliyun.com/products/56024006/cmfw00062543.html)[AI空中课堂在线直播课堂（旗舰版）](https://market.aliyun.com/products/201204006/cmgj00070018.html)
[行业生态解决方案](https://market.aliyun.com/industry)[开发者生态解决方案](https://market.aliyun.com/developer/shouye)[AI 开发和 AI 应用解决方案](https://market.aliyun.com/developer/AIGC)
[数据集](https://market.aliyun.com/dataexchange)[手机三要素](https://market.aliyun.com/products?k=%E6%89%8B%E6%9C%BA%E4%B8%89%E8%A6%81%E7%B4%A0&scene=market)[身份实名认证](https://market.aliyun.com/products?k=%E8%BA%AB%E4%BB%BD%E5%AE%9E%E5%90%8D%E8%AE%A4%E8%AF%81&scene=market)[短信](https://market.aliyun.com/products?k=%E7%9F%AD%E4%BF%A1&scene=market)[OCR 文字识别](https://market.aliyun.com/products?k=OCR%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB&scene=market)[发票查验](https://market.aliyun.com/products?k=%E5%8F%91%E7%A5%A8%E6%9F%A5%E9%AA%8C&scene=market)[天气预报查询](https://market.aliyun.com/products?k=%E5%A4%A9%E6%B0%94%E9%A2%84%E6%8A%A5%E6%9F%A5%E8%AF%A2&scene=market)[快递物流查询](https://market.aliyun.com/products?k=%E5%BF%AB%E9%80%92%E7%89%A9%E6%B5%81%E6%9F%A5%E8%AF%A2&scene=market)
[ERP](https://market.aliyun.com/products?k=ERP&scene=market)[CRM](https://market.aliyun.com/products?k=CRM&scene=market)[OA 办公系统](https://market.aliyun.com/products?k=OA%E5%8A%9E%E5%85%AC%E7%B3%BB%E7%BB%9F&scene=market)[财税管理](https://market.aliyun.com/products/56764034?page=1&scene=market)[400电话](https://market.aliyun.com/products?k=400%E7%94%B5%E8%AF%9D&scene=market)[广告营销](https://market.aliyun.com/products/56842011?page=1&scene=market)
[Windows](https://market.aliyun.com/products?k=Windows&scene=market)[宝塔 Linux](https://market.aliyun.com/products?k=%E5%AE%9D%E5%A1%94+Linux&scene=market)[CentOS](https://market.aliyun.com/products?k=CentOS&scene=market)[Docker](https://market.aliyun.com/products?k=Docker&scene=market)[JAVA](https://market.aliyun.com/products?k=JAVA&scene=market)[全能环境](https://market.aliyun.com/products?k=%E5%85%A8%E8%83%BD%E7%8E%AF%E5%A2%83&scene=market)[操作系统](https://market.aliyun.com/products?k=%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F&scene=market)[WordPress](https://market.aliyun.com/products?k=WordPress&scene=market)[Ubuntu](https://market.aliyun.com/products?k=Ubuntu&scene=market)[Red Hat](https://market.aliyun.com/products?k=Red+Hat&scene=market)[SUSE](https://market.aliyun.com/products?k=SUSE&scene=market)
[模板建站](https://market.aliyun.com/products/56598032?page=1&scene=market)[定制建站](https://market.aliyun.com/products/52738005?page=1&scene=market)[模板小程序](https://market.aliyun.com/products/205798005?page=1&scene=market)[定制小程序](https://market.aliyun.com/products/52752001?page=1&scene=market)[APP 开发](https://market.aliyun.com/products/55514022?page=1&scene=market)[建站系统](https://market.aliyun.com/products/57342011?page=1&scene=market)
[域名](https://market.aliyun.com/products?k=%E5%9F%9F%E5%90%8D&scene=market)[商标](https://market.aliyun.com/products?k=%E5%95%86%E6%A0%87&scene=market)[备案](https://market.aliyun.com/products?k=%E5%A4%87%E6%A1%88&scene=market)[公司注册](https://market.aliyun.com/products?k=%E5%85%AC%E5%8F%B8%E6%B3%A8%E5%86%8C&scene=market)[上云迁移](https://market.aliyun.com/products/52738004?page=1&scene=market)[代维服务](https://market.aliyun.com/products/52732002?page=1&scene=market)
[VPN](https://market.aliyun.com/products?k=VPN&scene=market)[SSL 证书](https://market.aliyun.com/products?k=SSL%E8%AF%81%E4%B9%A6&scene=market)[堡垒机](https://market.aliyun.com/products?k=%E5%A0%A1%E5%9E%92%E6%9C%BA&scene=market)[防火墙](https://market.aliyun.com/products?k=%E9%98%B2%E7%81%AB%E5%A2%99&scene=market)[主机安全](https://market.aliyun.com/products?k=%E4%B8%BB%E6%9C%BA%E5%AE%89%E5%85%A8&scene=market)
#### [AI 应用及服务市场](https://market.aliyun.com/common/ai)
[AI 应用](https://market.aliyun.com/products?k=AI%E5%BA%94%E7%94%A8&scene=market)[大模型](https://market.aliyun.com/products?k=%E5%A4%A7%E6%A8%A1%E5%9E%8B&scene=market)[自然语言处理](https://market.aliyun.com/products?k=%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86&scene=market)[数据标注](https://market.aliyun.com/products/201198004?page=1&scene=market)[机器学习](https://market.aliyun.com/products?k=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&scene=market)
坚持伙伴优先，为伙伴提供产品、销售和服务的商业合作模式；与伙伴紧密合作，共同为客户提供更完备的产品、更完善的服务。
#### 成为销售伙伴
[分销伙伴](https://partner.aliyun.com/programs/reseller_P)[咨询伙伴](https://partner.aliyun.com/program/consult_partner)
#### 销售伙伴合作计划
[无影生态合作计划](https://partner.aliyun.com/management/epp_wuying)[Salesforce On Alibaba Cloud Consulting Partner 合作计划](https://partner.aliyun.com/program/Salesforce_program)[AI 大模型销售与服务生态合作计划](https://partner.aliyun.com/program/aimsp)
#### 成为产品伙伴
[产品生态集成认证中心](https://partner.aliyun.com/program/PEIC)[产品生态伙伴](https://chanpinshengtai.aliyun.com/partner/partner)[产品生态伙伴工作台](https://aps.aliyun.com/#/)
#### 产品伙伴合作计划
[阿里云MaaS产品伙伴计划（繁花）](https://chanpinshengtai.aliyun.com/partner/ai)[弹性计算合作计划](https://partner.aliyun.com/program/txjs_program)[云存储合作计划](https://partner.aliyun.com/program/cunchu)[数据库合作计划](https://partner.aliyun.com/program/sjk_program)[云网络合作计划](https://chanpinshengtai.aliyun.com/chanpinpartner/network)[Salesforce On Alibaba Cloud ISV 合作计划](https://partner.aliyun.com/program/Salesforce-ISV)
[服务生态伙伴](https://gts.aliyun.com/)
#### 服务伙伴合作计划
[Al MaaS 服务伙伴赋能合作](https://gts.aliyun.com/ai-maas/partner/certification)[伙伴信用分合作计划](https://www.aliyun.com/gts/msp/Creditscoresystem)
#### 更多支持
[合作伙伴培训与认证](https://edu.aliyun.com/certification/partner)[查询合作伙伴](https://partner.aliyun.com/management/query#/)[登录合作伙伴管理后台](https://account.aliyun.com/login/qr_login.htm?oauth_callback=https://partner.aliyun.com/management/v2)
提供多样化的支持计划和专家服务，满足上云咨询、迁移上云、云上运维等场景的全链路服务需求。
#### 售前咨询
[在线服务](https://smartservice.console.aliyun.com/pre-sale/chat?entrance=201&referrer=https%3A%2F%2Fwww.aliyun.com%2F%3Fspm%3Da1z2e.12184483.navigationzhcn.dnavigationzhcn6.469d3247dm8YgK)
#### 售后服务
[自助服务](https://smartservice.console.aliyun.com/tourist-self/self-service-center?from=webnav)[在线服务](https://smartservice.console.aliyun.com/service/robot-chat)[工单服务](https://smartservice.console.aliyun.com/service/create-ticket)[短信专区](https://smartservice.console.aliyun.com/tourist-self/self-service-center/topic?topicCode=dysms&from=webnav)
#### 企业增值服务
[企业支持计划](https://www.aliyun.com/service/supportplans)[专家技术服务](https://www.aliyun.com/service/list)[企业增值服务台](https://custservice.console.aliyun.com/value-added/home)
#### 企业成长
[服务实践](https://www.aliyun.com/service/customer-case)[创新中心](https://chuangke.aliyun.com/)
[大模型认证](https://edu.aliyun.com/certification/llm)[全部认证](https://edu.aliyun.com/certification/)[训练营](https://edu.aliyun.com/trainingcamp)
#### 信息公告
[官网公告](https://www.aliyun.com/notice/)[健康状态](https://status.aliyun.com/)
[博文](https://developer.aliyun.com/indexFeed/)[问答](https://developer.aliyun.com/ask/)[电子书](https://developer.aliyun.com/ebook/)[镜像站](https://developer.aliyun.com/mirror/)
#### 我要反馈
[我要建议](https://www.aliyun.com/connect/home)[我要投诉](https://www.aliyun.com/complaint)
作为全球领先的全栈人工智能服务商，阿里云坚持让计算成为公共服务，助力全球客户加速价值创新。
[什么是云计算](https://www.aliyun.com/about/what-is-cloud-computing)[技术领先](https://www.aliyun.com/why-us/leading-technology)[稳定可靠](https://www.aliyun.com/why-us/reliability)[安全合规](https://www.aliyun.com/why-us/security-compliance)[分析师报告](https://www.aliyun.com/analyst-reports)[研究报告与白皮书](https://www.aliyun.com/reports)
[AI 算法大赛](https://tianchi.aliyun.com/competition/algorithmList/)[云开发大赛](https://tianchi.aliyun.com/competition/programList)[入门学习赛](https://tianchi.aliyun.com/competition/coupleList)
#### 最佳实践
[云上春晚](https://www.aliyun.com/about/gala)[云上奥运之旅](https://www.aliyun.com/about/games)[云栖战略参考](https://www.aliyun.com/about/magazines)[云上的中国](https://www.aliyun.com/about/ysdzg)[看见新力量](https://startup.aliyun.com/special/seenewpower)[金融模力时刻](https://summit.aliyun.com/market/financial-agent)[客户案例](https://www.aliyun.com/customer-stories/customer-case-index)
#### 市场活动
[2026 阿里云峰会](https://summit.aliyun.com/2026)[阿里云中企出海大会](https://summit.aliyun.com/go-global)[云栖大会](https://yunqi.aliyun.com/)[活动全景](https://www.aliyun.com/about/events)
#### 魔搭 ModelScope
[魔搭 ModelScope](https://modelscope.cn/home)
#### 高校合作
[云工开物](https://university.aliyun.com/)[科研合作](https://university.aliyun.com/activity/air)
[Careers](https://careers.aliyun.com/en/home)[社会招聘](https://careers.aliyun.com/off-campus/home)[校园招聘](https://careers.aliyun.com/campus/home)
### 阿里云中国站
www.aliyun.com
简体中文English### [阿里云国际站 www.alibabacloud.com](https://www.alibabacloud.com/)
### 联系我们
4008013260[售前咨询](https://smartservice.console.aliyun.com/pre-sale/chat?entrance=201&referrer=https%3A%2F%2Fhelp.aliyun.com%2Fzh%2Fdns%2Fbasic-concepts-dns2-0)[售后在线](https://smartservice.console.aliyun.com/service/robot-chat?entrance=201&referrer=https%3A%2F%2Fhelp.aliyun.com%2Fzh%2Fdns%2Fbasic-concepts-dns2-0)
### 其他服务
[我要建议](https://www.aliyun.com/connect/home)[我要投诉](https://www.aliyun.com/complaint)
登录以查看您的控制台资源
管理云资源
状态一览
快捷访问
