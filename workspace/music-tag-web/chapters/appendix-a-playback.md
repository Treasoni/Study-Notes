# 附录 A 播放侧与生态（可跳读）

> [!note] 这一节可跳读，不影响主线
> 正文主线到「整理与批处理」就收束了。本附录只装播放侧的零散能力：Subsonic 服务端与客户端清单、音乐收藏、Navidrome 联动、小爱音箱、网盘音乐、智能歌单与去重。你暂时没有 Navidrome / Jellyfin，所以「边车」定位不展开；每小节可单独跳读。

## A.1 服务端：V2 自己就是一台音乐服务器

V2 的播放服务端是自带的，不必再装一个 Navidrome 之类的服务端。「音乐收藏与播放」页开头写：「Open Subsonic 协议的播放服务器。登录的 host 是站点 ip:8002, 账号密码在后台管理里subsonic 用户中查看并修改。」[^cA-p1]「Subsonic客户端」页说得更直接：「Music Tag Web 提供音乐服务器，就不需要其他的服务端了，可以直接用下列中的客户端连接听歌了」。[^cA-p6]

同页第 4、5 条补了两点：

1. 第 4 条写「支持所有 subsonic 的客户端。 基于 Open Subsonic 协议音乐播放接口。」[^cA-p1]，所以客户端不限于官方列出的那几款。
2. 密码不在「修改密码」页改。第 5 条写：「admin/后台中 subsonic 用户中，修改 api token 即是密码。」改完「需要重新登录后刷新页面」。[^cA-p1]

> [!warning] 默认凭据是文档空白，别照猜
> Subsonic 用户的**默认用户名与默认密码具体值**，官方页面没给，本笔记同样没取到，也不会替你编一个。登录不上时，直接去后台看 subsonic 用户的当前配置。

> [!tip] 大白话
> 把 V2 想成一台自带点歌台的音箱柜：柜子（服务端）随柜附带，不用另买功放。8002 是门牌号，各种 Subsonic 客户端只是不同样式的遥控器。关键不是「再装一个服务端」，而是「把门牌号告诉遥控器」。

## A.2 客户端清单：官方两页写得不一样，两版并列

同一套官方手册里，「跨平台」一行列的客户端不一致：

| 平台 | 「音乐收藏与播放」页 | 「Subsonic客户端」页 |
| --- | --- | --- |
| 跨平台 | 音流 | 箭头音乐、音流 |
| Android | Symfonium、DSub、Tempo、substreamer、Subtracks、Ultrasonic | 与左列相同 |
| iOS | play:Sub、substreamer、Amperfy、iSub | 与左列相同 |
| Web | Thunderdrome、Airsonic Refix、Subplayer、Aurial、Subfire、Jamstash | 与左列相同 |
| 桌面 | Supersonic、Sublime Music、Submariner、Sonixd | 与左列相同 |

差异只在「跨平台」一行：前者写「音流」[^cA-p1]，后者写「箭头音乐、音流」[^cA-p6]，其余四类两页一致。

> [!note] 怎么理解这一处不一致
> 这是同一文档内两页各自维护列表造成的不同步，不是两套互斥结论。稳妥读法是取并集：跨平台有「音流」和「箭头音乐」，其余四类同上表。

## A.3 音乐收藏：先导入，才有得播

播放侧的一切都建立在「音乐收藏」这个中间层上，它和「操作台里能看到文件」不是一回事。第 1 条写：「在操作台中，勾选想要导入的目录，导入收藏，等待导入后可在音乐收藏中展示。」[^cA-p1] 顺序是勾选目录 → 导入收藏 → 等跑完。

第 6 条讲反过来的清理：「已经导入收藏的音乐，后续在文件管理中删除了，收藏中还存在可在其他设置-删除不存在收藏中同步删除，或着直接通过 操作台中的删除文件夹功能删除文件。该功能会同时删除音乐收藏中的音乐。」[^cA-p1]

> [!warning] 删文件会连带删收藏
> 「该功能会同时删除音乐收藏中的音乐」，指用操作台「删除文件夹」删文件时，收藏记录会被一起清掉。想只清记录不动文件，走「其他设置-删除不存在收藏」。

> [!tip] 大白话
> 把音乐收藏想成图书馆的**索书卡**，操作台里的文件是**书架**。往书架塞新书，索书卡不会自动出现——必须手动「导入收藏」建卡；书被抽走，卡片还留在盒子里（所以有「删除不存在收藏」补卡）。而操作台的「删除文件夹」是连书带卡一起扔。

## A.4 Navidrome 联动：`artist.jpg` 和 `cover.jpg` 是两类文件

**官方教程讲艺术家图。**前提条件写得很明确：「确保您的音乐已导入到音乐收藏中。」[^cA-p7] 即 A.3 没做完就不必往下看。流程三步：

1. 「系统设置」→「其他设置」→「刮削艺术家」，点击按钮；完成后到「操作记录」看刮削详情。
2. 若目录结构形如 `/app/media/music/王以太/演.说.家/人间天堂.flac`，那么「则系统将在 `/王以太/` 目录下自动生成 `artist.jpg` 文件。」
3. 「`artist.jpg` 文件将被 NaviDrome 自动识别并用于艺术家页面的展示。」[^cA-p7]

「总结」把目录结构写成硬约束：`/艺术家/` → `/专辑/` → `音乐文件`，原话是「为了确保艺术家封面能被正确显示，请务必按照以下目录结构组织您的音乐文件」[^cA-p7]；页首也自称「本实验演示在music tag web 中批量刮削艺术家封面，并成功被 navidrome 识别到」[^cA-p7]。

**社区经验讲专辑图。** 飞牛论坛帖里，有用户给出打开「导出图片」开关的做法：「我发现navidrome显示的专辑封面是取得歌曲文件夹里面的cover.jpg，用music-tag刮削后，要把“导出图片”这个设置为开，保存音乐信息就会自动生成一张cover.jpg。」[^cA-p8] 这是**社区经验，非官方口径**；同帖后续有人回「成功了，感谢」。

| 维度 | `artist.jpg` | `cover.jpg` |
| --- | --- | --- |
| 来源层级 | 官方教程（P7） | 社区经验（P8） |
| 对应界面 | 「刮削艺术家」 | 「导出图片」开关设为开 |
| 生成位置 | `/艺术家名/` 目录下 | 歌曲所在文件夹内 |
| 服务对象 | Navidrome 艺术家页展示 | Navidrome 专辑封面展示 |

**关于「部分识别不出」。** 楼主说的是：「music-tag 刮削过后 navidrome 部分有些还是识别不出来 手动和自动刮削都试过了」[^cA-p8]。这**不构成对官方成功结论的反驳**——官方实验针对 `artist.jpg`，该帖讨论的主要是专辑封面一侧。

同帖另有用户给出体积与分辨率经验值：「有情提示 图片别大于80K 不信你可以试一下」「补充下 分辨 800-550 左右合适 高了有时候不识别」[^cA-p8]。这是**社区经验值**：官方没给封面体积或分辨率限制，请当作排错方向，别当硬阈值。

> [!tip] 大白话
> 把音乐文件想成一份份**塑封专辑**：`cover.jpg` 是**专辑盒面**上的图，`artist.jpg` 是**歌手货架**上的头像。Navidrome 逛货架先看头像，翻专辑先看盒面。所以「头像贴好了但盒面空着」，看起来就是「部分识别不出」——不是方法失效，是你贴错了位置。

## A.5 社区 compose 样例：两容器共用一个音乐目录

> [!warning] 这是社区做法，不是官方推荐配置
> 下面整段来自博客园一篇个人文章[^cA-p9]，属**社区实践层级**。其中端口等数值**不能当官方事实**：官方 P1–P7 从未提及 Navidrome 默认端口。

该文作者把 Navidrome 与 MTW 放进同一份 compose，两容器挂**同一个音乐目录**：Navidrome 挂 `/music`，MTW 挂 `/app/media`，改完标签两边读的是同一批文件。

```yaml
version: "3"
services:
  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    ports:
      - "4533:4533"
    environment:
      - ND_LOGLEVEL=info
      - ND_MUSICFOLDER=/music
      - ND_DATAFOLDER=/data
      - ND_ENABLEDOWNLOADS=true
    volumes:
      - /vol1/1001/06_Music:/music  # 你的音乐目录，和NAS路径对应
      - ./navidrome:/data  # Navidrome 数据持久化
    restart: always
    networks:
      - music-network

  musictagweb:
    image: xhongc/music_tag_web:latest
    container_name: musictagweb
    ports:
      - "8002:8002"  # 前端访问端口，可自行修改
    volumes:
      - /vol1/1001/06_Music:/app/media  # 挂载和Navidrome相同的音乐目录，直接编辑标签
      - ./musictagweb/data:/app/data  # 挂载数据存储目录
    restart: unless-stopped
    networks:
      - music-network

networks:
  music-network:
    driver: bridge
```

两处可留意：MTW 只挂 `/app/media` 与 `/app/data`，没有 `/app/download`（该作者不需要后台刮削）；MTW 用 `restart: unless-stopped`，作者解释是「在MusicTagWeb上面，启动模式是 unless-stopped ，也就是可以随时手动停止」，需要加歌时再打开容器，属低性能 NAS 的省资源取舍[^cA-p9]。`8002:8002` 与官方 V2 端口一致。

## A.6 小爱音箱：用语音点局域网里的歌

功能定位是「使用小爱音箱播放局域网内的音乐，支持歌曲和播放列表点歌。」[^cA-p2] 配置项按官方顺序填：

1. **设备型号、名称、小米账号。** 型号看音箱底部标签（例如 LX06）；账号「为小米 ID ，非手机号码」；名称填账号下这台音箱的名字，改过名填改后的。
2. **关键字**：识别「要播放局域网音乐」的需求。
3. **内网地址和端口**：「内网地址是本项目的内网地址，端口是部署命令的端口。」[^cA-p2]
4. **测试连接**：成功会发出语音；没声音先核对配置与账号密码，都正确还没声音，可能是「该型号的音箱不支持这个功能」。
5. **轮询时间**：查询间隔，单位秒。
6. **是否启用**：唤醒说「小爱同学 关键词 歌曲名」，操作日志可看是否检索到（官方连写三遍「不需要说歌手！」）。

官方列的兼容性口径是：「测试通过的型号 LX06，L16A，LX5A ，L17A，S12。」另有「只能播放mp3 格式的型号：L05B」。[^cA-p2]

> [!warning] 型号清单不是白名单
> 官方只给了「测试通过」和「只能播 mp3」各一条，并提示其他型号「可能是该型号的音箱不支持这个功能」。**清单之外的机型行为如何，官方没有完整兼容列表**——本笔记也没有，别反推「不在列表里就一定不行」。

## A.7 网盘音乐：直连与本地挂载，先分清再选

这页给出两条路径，差别不在配置细节，而在**刮削会不会动到网盘上的原始文件**。

**直连模式**官方定义是「直接连接 alist api，对网盘音乐进行刮削和入库。」[^cA-p3] 要填 Alist Url、根目录地址、alist 用户名与账号密码，另有「显示条数」「清除缓存」；根目录地址映射到容器内 `/app/webdav/`，配好后去「操作台」看该目录是否出现网盘文件。关键是那句提示：「注意：刮削操作不会修改网盘音乐文件的元数据。」[^cA-p3]

**本地挂载**的官方说明是「通过挂载工具将网盘挂载本地/app/weddav 目录，可当做本地文件使用」[^cA-p3]。四步：

1. 部署时额外增加映射卷，官方示例写 `/path/to/your/webdavmusic:/app/webdav:rw`；挂载地址要与 alist 里的一致，alist 才能正确解析。
2. 「系统设置」→「基本设置」→「webdav写入位置」→ 勾选「数据库」。
3. 导入收藏。
4. 「系统设置」→「网盘音乐」→ 配置 alist 地址。

> [!note] 原文拼写不一致，按 `webdav` 理解
> 本地挂载那段正文把路径写成 `/app/weddav`（多一个 d），同页映射示例写的是 `/app/webdav`。这是页面内的笔误，**原文如此，保留原样不做「顺手修正」**；实操按映射示例的 `/app/webdav` 来。

| 维度 | 直连模式 | 本地挂载 |
| --- | --- | --- |
| 前置 | alist 可访问 + 账号密码 | alist 可访问 + 额外映射一卷 |
| 刮削是否改网盘原文件 | 官方明示：不会修改 | 当作本地文件使用 |
| 额外步骤 | 无 | 勾选 webdav 写入位置为「数据库」→ 导入收藏 |
| 适合谁 | 只想在 MTW 里管理、不愿动云上文件 | 想把网盘当本地曲库处理 |

> [!tip] 大白话
> 把网盘想成**别人家的仓库**。直连是「隔着窗户看货、在自家账本上登记」，货不动；本地挂载是「把货搬进自己院子」。后者自由度高，但记得勾「webdav 写入位置-数据库」，否则你会对着一个不更新的收藏列表发呆。

**网盘类型是文档空白**：该页只说明经 alist 接入，**未列举支持哪些具体网盘**，本笔记同样没取到。

## A.8 智能歌单与音乐去重

两个都是轻量工具，不需要账号或插件，门槛只是「音乐库里有东西」。

**智能歌单**入口是「音乐收藏-智能歌单」，作用一句话：「根据满足条件快速从音乐库中创建歌单列表」[^cA-p4]。但该页只有标题、一张截图和这一句，**没有列出「条件」支持哪些字段或操作符**——这是未取到的内容，本笔记不补写条件清单。

**音乐去重**入口是「操作台-勾选目录-重复文件检查」。页首那句最要紧：「查找出重复的文件 不会自动删除您的文件，可以到操作记录中查看重复文件进一步删除操作。」[^cA-p5] 执行成功后到「操作记录」看结果，详情罗列检查到的重复文件，由你挑要删哪些。

> [!tip] 大白话
> 音乐去重像**超市盘点时拉一张「疑似同款」清单**：它只把重复的挑出来摆在你面前，一支笔都不替你划。真正的删除永远在「操作记录」里由你手动完成。看到检查跑完别以为文件已经清掉了——那只是一张待办清单。

## 附录 A 小结

- **服务端自带**：连站点 IP 加 8002；密码在后台 subsonic 用户里，改「api token」即是改密码，改完重新登录刷新；**默认凭据官方未给出**。
- **客户端清单取两页并集**：跨平台「音流 / 箭头音乐」，其余四类两页一致。
- **音乐收藏是中间层**：必须手动「导入收藏」；清记录走「删除不存在收藏」，而「删除文件夹」会连收藏一起删。
- **`artist.jpg` 与 `cover.jpg` 是两类文件**：前者由官方「刮削艺术家」生成在 `/艺术家名/` 下，后者靠社区提到的「导出图片」开关生成；「部分识别不出」多半是两类图混为一谈。
- **网盘音乐两条路**：直连不动云上原文件；本地挂载要额外映射并勾选「webdav 写入位置-数据库」；原文 `/app/weddav` 是笔误，按 `/app/webdav` 操作。
- **智能歌单与去重「只看不动」**：去重不会自动删文件，条件字段官方未列出。

附录 A 主打「能播、能连、能找」。故障排错看附录 C，改配置看附录 B。

[^cA-p1]: Music Tag Web V2 官方手册，「音乐收藏与播放」页（官方层级），2026-09-14 抓取。https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/yin-yue-shou-cang-yu-bo-fang
[^cA-p2]: Music Tag Web V2 官方手册，「小爱音箱」页（官方层级），2026-09-14 抓取。https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/xiao-ai-yin-xiang
[^cA-p3]: Music Tag Web V2 官方手册，「网盘音乐」页（官方层级），2026-09-14 抓取。https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/wang-pan-yin-yue
[^cA-p4]: Music Tag Web V2 官方手册，「智能歌单」页（官方层级），2026-09-14 抓取。https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/zhi-neng-ge-dan
[^cA-p5]: Music Tag Web V2 官方手册，「音乐去重」页（官方层级），2026-09-14 抓取。https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/yin-yue-qu-zhong
[^cA-p6]: Music Tag Web V2 官方手册，「Subsonic客户端」页（官方层级），2026-09-14 抓取。https://xiers-organization.gitbook.io/music-tag-web-v2/subsonic-ke-hu-duan
[^cA-p7]: Music Tag Web V2 官方手册，「刮削艺术家并被 navidrome 识别」页（官方层级），2026-09-14 抓取。https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/gua-xiao-yi-shu-jia-bing-bei-navidrome-shi-bie
[^cA-p8]: 飞牛私有云论坛帖 4152「music-tag 刮削过后 navidrome有些还是识别不出来」（社区实践层级，非官方），2026-09-14 抓取。https://club.fnnas.com/forum.php?mod=viewthread&tid=4152
[^cA-p9]: 博客园「Docker部署Navidrome+MusicTagWeb搭建私人音乐库」（社区实践层级，非官方），2026-09-14 抓取。https://www.cnblogs.com/ivoink/articles/22696323
