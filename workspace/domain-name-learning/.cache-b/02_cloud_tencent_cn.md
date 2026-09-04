---
url: "https://cloud.tencent.cn/document/product/302/105665"
title: "云解析 DNS 添加子域名解析_腾讯云"
scraped_at: 2026-09-04T04:45:07+00:00
---

[_腾讯云_](https://cloud.tencent.cn)


### 近期搜索热词


[更多问题，派给帮你解答立即下载](https://www.workbuddy.cn/)
[登录](javascript:void%200;)[免费注册](javascript:void%200;)
  * 联系客服：[95716](tel:95716)或[4009 100 100](tel:4009100100)转1


### 近期搜索热词
  * WorkBuddy
  * CodeBuddy
  * TokenHub


  * 腾讯智能体
    * [WorkBuddy EnterpriseNEW](https://cloud.tencent.com/product/workbuddy-enterprise)
    * [WorkBuddyHOT](https://cloud.tencent.com/product/workbuddy)
    * [CodeBuddyNEW](https://cloud.tencent.com/product/acc)
    * [WorkBuddy Managed AgentsNEW](https://cloud.tencent.com/product/workbuddy-managed-agents)
  * 大模型
    * 语言模型
    * 视觉模型
    * 语音模型
  * 模型与应用开发
    * [大模型服务平台 TokenHubHOT](https://cloud.tencent.com/product/tokenhub)
    * [智能体开发平台 ADPHOT](https://cloud.tencent.com/product/adp)
  * AI 应用
  * AI 应用解决方案
    * [云端秒级部署 OpenClaw 全能助手](https://cloud.tencent.com/act/solution-ai-application1-17566)
    * [WorkBuddy Claw 一号员工已上岗](https://cloud.tencent.com/act/solution-ai-application1-17582)


#### [操作指南](javascript:void%200; "操作指南")
  * [域名设置](javascript:void%200; "域名设置")




[帮你快速理解、总结文档立即下载](https://www.workbuddy.cn/)
[文档中心](https://cloud.tencent.cn/document/product "文档中心")[云解析 DNS](https://cloud.tencent.cn/document/product/302 "云解析 DNS")[操作指南](https://cloud.tencent.cn/document/product/302/3443 "操作指南")[域名设置](https://cloud.tencent.cn/document/product/302/104803 "域名设置")添加子域名解析
# 添加子域名解析
最近更新时间：2025-12-30 10:38:52
  * 微信扫一扫
  * 复制链接
链接复制成功


_我的收藏_
## 本页目录：
  * [操作指南](https://cloud.tencent.cn/document/product/302/105665#2ec9194e-b3fb-41b8-bf85-479909c6be5a "操作指南")


若您需要将子域名在云解析 DNS 管理并添加解析记录，您可参考本文进行操作。
### 步骤一： 云解析 DNS 添加子域名
1. [云解析 DNS 控制台](https://console.cloud.tencent.com/cns)，在左侧导航栏中选择
2. 页面中，单击。如下图所示：
3. 在输入框中输入您需要解析的子域名，并单击。如下图所示，请将`a.test.com`替换为您需要解析的子域名。
如果主账号开启了子账号强制打标签，那么子账号添加域名需打标签。
如果要添加的标签数较多，可以使用**键值粘贴板** 功能快速添加多个标签。
更多关于腾讯云标签的介绍请参见 [腾讯云标签概述](https://cloud.tencent.com/document/product/651/13334)
4. 页面弹出提示，需前往主域名所在的 DNS 服务商处为域名添加 TXT 解析记录。
记录信息如下图所示：
如您的主域名在当前账号下，可忽略以下步骤。
5. 登录主域名所在的 DNS 服务商，在主域名下添加 TXT 解析记录。以下操作以腾讯云 DNSPod 为例。
5.1 [云解析 DNS 控制台](https://console.cloud.tencent.com/cns)，在左侧导航栏中选择**权威解析，**
5.2 页面中，单击目标域名名称，如下图所示：
5.3 页面中，单击，并设置以下 TXT 解析记录。如下图所示：
记录值请参见  截图内容。
6. TXT 校验。
6.1 TXT 记录添加完成后，回到 ，如下图所示，单击 **TXT 校验**
6.2 **验证成功，添加完成** ，如下图所示：
### 步骤二： 子域名设置 NS 记录
添加子域名后，如果子域名状态提示“未使用云解析 DNS 地址”，则您需要前往您的解析商处，为子域名添加 NS 解析记录指向 DNSPod DNS 服务器地址。如下图所示：
#### 在腾讯云设置 NS 记录
若您的主域名注册商是腾讯云，可参考此步骤。
1. [云解析 DNS 控制台](https://console.cloud.tencent.com/cns)，在左侧导航栏中选择
2. 页面中，选择目标，如下图所示：
3. 页面中，单击，添加以下两项 NS 解析记录。如下图所示：
记录值请参考您的控制台指引，如下图所示：
#### 在阿里云设置 NS 记录
若您的主域名注册商是阿里云，可参考此步骤。
本文档仅供参考，具体以第三方页面为准；如有版权或其他问题，请及时联系 [腾讯云在线客服](https://cloud.tencent.com/act/event/Online_service)
1. 
2. 选择目标域名，并单击右侧。如下图所示：
3. 在解析设置页面中，单击，并添加以下两项 NS 解析记录。如下图所示：
记录值请参考您的控制台指引。如下图所示：
### 步骤三： 添加子域名解析记录
1. [云解析 DNS 控制台](https://console.cloud.tencent.com/cns)，在左侧导航栏中选择**权威解析，**
2. 页面中，单击目标**子域名名称** ，如下图所示：
3. 在记录管理页面中，单击**添加记录，** 即可设置子域名对应解析记录。如下图所示：
4. 完成以上步骤后， 请等待解析生效。解析生效后您即可访问设置的对应解析。如需查看解析是否生效，请参见 [如何检查解析是否生效？](https://cloud.tencent.cn/document/product/302/53974)
5. 如主域名下已存在该子域名解析记录，需要在子域名解析设置页面进行解析设置，然后在主域名下删除子域名解析记录。如果主域名下没有该子域名，请忽略此步骤。
子域名和主域名下都添加该子域名解析记录，子域名优先解析。
子域名不支持设置 URL 转发。
文档内容是否对您有帮助？
如果遇到产品相关问题，您可咨询 在线客服寻求帮助。


  * 

腾讯智能体
    [WorkBuddy Managed Agents](https://cloud.tencent.com/document/product/1831/134407 "WorkBuddy Managed Agents") 

腾讯大模型


AI 基础产品


AI 应用产品


AI 平台产品


云上网络


混合云网络


安全运营


业务风控


云安全


数据安全


安全服务


零信任


API 与工具


云生态

  * 

计算


操作系统与工具


高性能计算


分布式云


容器


Serverless


消息队列


微服务工具与平台


关系型数据库


关系型数据库 TDSQL


NoSQL 数据库
    [腾讯云分布式缓存数据库（兼容 Redis）](https://cloud.tencent.cn/document/product/239 "腾讯云分布式缓存数据库（兼容 Redis）") 

数据库软硬一体


数据库 SaaS 服务


数据库分布式云


数据分析
    [Elasticsearch Service](https://cloud.tencent.cn/document/product/845 "Elasticsearch Service") 

数据开发与治理


数据应用与可视化
    [数字孪生可视化网页版 RayData Web](https://cloud.tencent.cn/document/product/1609 "数字孪生可视化网页版 RayData Web")     [数字孪生可视化专业版 RayData Plus](https://cloud.tencent.cn/document/product/1652 "数字孪生可视化专业版 RayData Plus") 

云原生应用平台


设计协同管理工具


监控与运维

  * 

视频服务


视频终端


媒体处理


实时互动


云通信


域名管理


区块链


网站与备案


CDN 与边缘平台


边缘计算


金融服务


教育服务


传媒服务


零售服务


移动服务


建筑服务


医疗服务


文旅服务


科创服务


云迁移工具


开发者工具

  * 

基础存储服务


存储数据服务


数据迁移


混合云存储


智能存储


企点商通


企点营销云


办公协同


连接器


CRM


物联网


通用解决方案


行业解决方案


微信解决方案


私有云


用户服务


云资源管理
    [云资源自动化 for Crossplane](https://cloud.tencent.cn/document/product/1763 "云资源自动化 for Crossplane") 

更多



搜索结果
当前产品
全部
问 AI 助手
正在为您收集信息
中国站


[ 文档“捉虫”活动 检视指定产品文档，发现和反馈有效问题，奖！](https://cloud.tencent.com/developer/article/1610407)
[ API专项"捉虫" 反馈API文档问题，代金券、周边好礼奖不停！](https://cloud.tencent.com/developer/article/1630768)
[ 文档建议，你提了吗 快来使用腾讯云产品文档，提出有效建议，奖！](https://cloud.tencent.com/developer/article/1523112)     [步骤一： 云解析 DNS 添加子域名](https://cloud.tencent.cn/document/product/302/105665#8e4a6f25-820b-4857-b0a7-4204dc8c6150)
