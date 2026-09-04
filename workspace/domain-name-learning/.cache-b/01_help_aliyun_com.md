---
url: "https://help.aliyun.com/zh/dws/user-guide/domain-name-security1"
title: "域名安全最佳实践-域名(Domain)-阿里云帮助中心"
scraped_at: 2026-09-04T04:46:55+00:00
---

输入文档关键字查找
一旦发生域名被劫持、非法转移或DNS篡改，可能导致服务中断、用户信息泄露、品牌声誉受损，甚至造成重大经济损失。阿里云提供覆盖账户、注册商、注册局到DNS解析层的防御体系，支持从基础防护到企业级高安全场景的灵活配置。
本文将为您系统介绍各项安全能力，并帮助您根据自身角色与业务场景，快速判断应启用哪些防护措施。具体配置步骤与技术细节，可参考各子页面文档。
## 阿里云提供的核心安全能力  
|   |   | **核心防护目标**  |  
| --- | --- | --- |  
| **防护层级**  | **安全功能**  | **核心防护目标**  |  
| --- | --- | --- |  
| 账户层  | 多因素认证（MFA）  | 防止账号被盗，在用户名和密码之外再额外增加一层安全保护。  |  
| 注册商层  | 禁止转移锁  | 阻止域名被恶意转出至其他注册商。  |  
| 禁止更新锁  | 防止联系人信息、NS服务器等关键设置被篡改。  |  
| 注册局层  | 注册局安全锁  | 提供最高级别锁定，任何变更均需人工核验，抵御高级持续性攻击。  |  
| 解析层  | DNSSEC  | 防范DNS劫持与缓存污染，确保用户访问的是真实服务器。  |  
## 使用场景推荐
根据业务实际情况参考配置：  
|   |   | **推荐防护组合**  |  
| --- | --- | --- |  
| **用户类型**  | **典型场景**  | **推荐防护组合**  |  
| --- | --- | --- |  
| 个人开发者 / 博主（拥有个人域名，用于博客、作品集或测试项目）  | - 域名主要用于展示或学习- 不常登录管理后台- 担心忘记续费或账号被盗导致域名丢失- 可能使用弱密码或共用邮箱登录  | MFA + 禁止转移锁  |  
| 中小企业运营者（负责公司官网、小程序、电商平台等线上入口）  | - 网站已上线并对外服务- DNS配置稳定，不频繁变更- 曾听说过同行网站被篡改跳转到广告页- 多人协助管理，担心误操作或权限失控  | MFA + 禁止转移锁 + 禁止更新锁  |  
| 企业IT/运维负责人（管理品牌主域、核心系统入口或高流量平台）  | - 主域名承载登录系统、支付页面或会员服务- 一旦宕机将影响大量用户和收入- 属于曾被攻击的目标，或行业监管要求高等级防护- 追求“即使账号泄露也不能被操作”的极致安全  | MFA + 禁止转移锁 + 禁止更新锁 + 注册局安全锁 + DNSSEC  |  
## 各防护能力简介
### **多因素认证（MFA）**
MFA（Multi-Factor Authentication，多因素认证）是一种提升账号安全性的最佳实践，它能够在用户名和密码之外再额外增加一层安全保护。
启用MFA后，登录阿里云时需完成以下两步验证：
  1. 第一重验证：输入您的账号名和密码。
  2. 第二重验证：其他验证方式，例如虚拟MFA每30秒自动生成的6位动态验证码。


通过双重认证，即使密码泄露，未持有您手机的人也无法登录您的账号，有效防止账号被盗，极大提升安全性。具体操作可参考[配置账号的MFA](https://help.aliyun.com/zh/account/configure-account-mfa)。
### **禁止转移锁**
开启后域名将被置为注册商禁止转移状态（clientTransferProhibited），避免您的域名被恶意转出阿里云。
如需获取域名转移密码，需先关闭禁止转移锁。
开启禁止转移锁的具体操作可参考[设置禁止转移锁](https://help.aliyun.com/zh/dws/user-guide/enable-the-transfer-prohibition-lock)。
### **禁止更新锁**
开启后可防止您的域名注册信息（域名联系人、电话、地址、传真、电子邮箱）、域名DNS服务器被恶意篡改。目前“.com/.net/.org/.info/.biz/.mobi/.asia/.me/.so/.cc/.tv/.name/.cn/.中国 /.公司/.网络”等后缀域名支持开启禁止更新锁。
开启禁止更新锁的具体操作可参考[开启禁止更新锁](https://help.aliyun.com/zh/dws/user-guide/enable-the-update-prohibition-lock)。
### **注册局安全锁**
注册局安全锁是目前最高等级的域名安全保护措施，由注册局在根服务器层面操作，禁止域名被恶意转移、篡改及删除。目前“.com/.cn/.net/.cc/.tv/.name/.中国/.gov.cn”等后缀域名支持开启注册局安全锁。开启注册局安全锁后，域名将被置为以下三种锁定状态：
  * 注册局设置禁止删除（serverDeleteProhibited）
  * 注册局设置禁止转移（serverTransferProhibited）
  * 注册局设置禁止更新（serverUpdateProhibited）


如果需要对域名做任何状态的变更及信息更改，需先解除对应的锁定状态。具体操作可参考[使用注册局安全锁](https://help.aliyun.com/zh/dws/user-guide/use-the-security-lock-of-domain-name-registries)。
### **DNSSEC**
域名系统安全扩展（DNS Security Extensions，简称DNSSEC）是用于确定源域名可靠性的数字签名 ，通过在域名中添加DNSSEC记录，可以增强对DNS域名服务器的身份认证，有效防止DNS缓存污染等攻击。具体操作可参考[配置DNSSEC](https://help.aliyun.com/zh/dws/user-guide/configure-dnssec-domain-name-system-security-extensions)。
该文章对您有帮助吗？
  * 本页导读 （1）
  * 阿里云提供的核心安全能力
  * 使用场景推荐
  * 各防护能力简介
  * 多因素认证（MFA）
  * 禁止转移锁
  * 禁止更新锁
  * 注册局安全锁
  * DNSSEC


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
4008013260[售前咨询](https://smartservice.console.aliyun.com/pre-sale/chat?entrance=201&referrer=https%3A%2F%2Fhelp.aliyun.com%2Fzh%2Fdws%2Fuser-guide%2Fdomain-name-security1)[售后在线](https://smartservice.console.aliyun.com/service/robot-chat?entrance=201&referrer=https%3A%2F%2Fhelp.aliyun.com%2Fzh%2Fdws%2Fuser-guide%2Fdomain-name-security1)
### 其他服务
[我要建议](https://www.aliyun.com/connect/home)[我要投诉](https://www.aliyun.com/complaint)
登录以查看您的控制台资源
管理云资源
状态一览
快捷访问
