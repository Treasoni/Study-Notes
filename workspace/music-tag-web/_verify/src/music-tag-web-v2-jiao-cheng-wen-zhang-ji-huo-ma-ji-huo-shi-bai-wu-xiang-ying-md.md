> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/ji-huo-ma-ji-huo-shi-bai-wu-xiang-ying.md).

# 激活码激活失败、无响应

**情况 1：激活后无任何提示，无响应。**

原因：\
激活时需向激活服务器发送认证验证，容器内网络不通导致无响应\
解决方案：\
docker 部署时网络模式改为 host 模式（需要占用 8001、8002、9001 端口，启动失败查看端口占用情况），或者让 bridge 能访问外部网络。

**情况 2：出现提示：请矫正服务时间，验证超时！**\
解决方案：\
服务器（NAS）上的时间和北京时间误差不要超过 1 分钟，请进行矫正调整。

**情况 3：出现提示：激活码已被激活**\
原因：\
重复多次激活，超限 6 次\
解决方案：\
描述清楚当前问题后，找开发者进行重置次数。
