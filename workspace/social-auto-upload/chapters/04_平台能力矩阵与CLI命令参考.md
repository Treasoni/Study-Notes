## 第 4 章 平台能力矩阵与 CLI 命令参考

第 3 章用抖音走通了「配置-登录-发布」的最小闭环，但抖音只是 11 个平台里的一个。一旦想把同一条内容铺到 B 站、小红书、视频号，问题立刻变成：每个平台的命令怎么拼？哪些平台能发图文、能定时？本章把 11 个平台的能力差异和 `sau` 命令收成一套「速查层」：先给平台能力总表，再拆 CLI 通用结构，接着给发布参数速查，最后点出一个文档缺口——成功/失败到底怎么判定。

### 4.1 平台能力总表（11 平台）

先给结论性地图。下表覆盖 11 个平台，列头含义：

- **CLI 前缀** = `sau` 后第一段，即平台子命令名（如抖音是 `sau douyin …`）；
- **视频 / 图文 / 定时发布** = 平台侧能力（README 能力矩阵口径）；
- **CLI 接入** = 当前 `sau` 主线是否已接入（未接入则只能用历史 example）。

| 平台 | CLI 前缀 | 视频 | 图文 | 定时发布 | CLI 接入 | 说明 |
|------|---------|:--:|:--:|:--:|:--:|------|
| 抖音 | `douyin` | ✅ | ✅ | ✅ | ✅ | 主线能力最完整；图文另支持 BGM / notef |
| Bilibili | `bilibili` | ✅ | ❌ | ✅ | ✅ | 自动下载 biliup；`--tid` 分区必填（示例 249） |
| 小红书 | `xiaohongshu` | ✅ | ✅ | ✅ | ✅ | 浏览器版；旧流程才需 XHS_SERVER |
| 快手 | `kuaishou` | ✅ | ✅ | ✅ | ✅ | — |
| 视频号 | `tencent` | ✅ | ❌ | ✅ | ✅ | CLI 前缀是 `tencent`；可传 `--collection` / `--draft` |
| 百家号 | `baijiahao` | ✅ | ❌ | ❌ | ✅ | 可传 `--collection` |
| 支付宝生活号 | `alipay` | ✅ | ❌ | ❌ | ✅ | 需先开通生活号创作 |
| 微博 | `weibo` | ✅ | ❌ | ❌ | ✅ | 标题 ≤ 30 字 |
| 虎扑 | `hupu` | ✅ | ❌ | ❌ | ✅ | 标题 4–40 字 |
| YouTube | `youtube` | ✅ | ❌ | ❌ | ✅ | 浏览器自动化操作 Studio；可传 `--playlist` / `--visibility`；被墙需 `YT_PROXY` |
| TikTok | （无） | ✅ | ❌ | ✅（矩阵列） | ❌ | 走历史 Chrome example，未接入 CLI |

读这张表最有价值的一条信息：**图文能力很稀缺，只有抖音 / 小红书 / 快手三行是 ✅**。想做图文分发，先圈定这三个平台即可；其余平台表格里直接标了 ❌，不用浪费时间找图文参数。

> [!warning] 版本口径：两处能力冲突以最新代码为准
> ① **YouTube 实际有 CLI**：README 快速开始段列「已接入 CLI」时漏写了 YouTube，但同一段给了 `sau youtube` 示例、CLI.md 也含 youtube——判定为有 CLI（推断）。② **TikTok 定时发布未接入 CLI**：README 能力矩阵把 TikTok 定时发布标成 ✅，但 CLI.md 的 `--schedule` 支持表里没有 TikTok——现状是「平台侧支持、工具侧还没接」。以上均为易变 / 推断信息，以仓库最新代码为准（[README](https://github.com/dreammis/social-auto-upload) / [docs/CLI.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/CLI.md)）。

> [!tip] 大白话：怎么读这张能力表
> 把每一行想成该平台的「报名规则清单」：哪些玩法它收（✅）、哪些不收（❌）。所以它不回答「哪个平台最好」，只回答「你手上这条内容在这个平台能不能发」——视频几乎哪都能发，图文却只有三家里能发。

### 4.2 CLI 通用结构

`sau` 把所有平台收成了同一套命令骨架：

```bash
sau <platform> <action> --account <account_name> [参数]
```

- `<platform>`：平台子命令名，即 4.1 表的「CLI 前缀」列；
- `<action>`：要做的动作；
- `--account <account_name>`：**通用必选**，指定用哪个账号身份。一个 `account_name` 对应一份独立的账号文件（Cookie），互不干扰——这是第 3 章「一个账号名 = 一个账号文件」模型在命令层的体现。

每个平台发布前的基本动作是固定「三件套」：

```bash
# 以抖音为例：login（准备登录态）→ check（校验登录态）→ upload-video（发布）
sau douyin login --account demo
sau douyin check --account demo
sau douyin upload-video --account demo --file demo.mp4 --title "示例标题" --desc "示例描述"
```

| 子命令 | 作用 | 备注 |
|--------|------|------|
| `login` | 准备登录态 | 首次要扫码 / 短信验证（短信验证码写项目根目录 `verify_code.txt`） |
| `check` | 校验登录态是否有效 | 平台出现登录 UI 即判失效；判定细节见第 5 章 |
| `upload-video` | 发布视频 | 不传 `--schedule` 就立即发布 |
| `upload-note` | 发布图文 | 仅抖音 / 快手 / 小红书支持 |

通用运行参数有三个，控制浏览器「怎么跑」：

| 参数 | 含义 | 默认 | 典型用途 |
|------|------|------|----------|
| `--headless` | 无头运行，不弹出浏览器窗口 | 默认 | 日常发布、服务器部署 |
| `--headed` | 有头运行，弹出真实浏览器窗口 | 关 | 登录被风控时临时打开看现场 |
| `--debug` | 打印调试信息 | 关 | 排错定位 |

**多账号并发**：每个 `--account` 是独立账号文件、不共享登录态，所以可以同时跑多条命令处理不同账号。比如想给两个抖音号发同一条视频，就开两个终端各指定一个 `--account`，或写进脚本并行执行——账号之间互不干扰。

> [!tip] 大白话：命令骨架想成「去柜台办事」
> `sau <platform> <action> --account <name>` 就像「到 XX 平台柜台办 XX 业务，报上你的会员号」：`<platform>` 是去哪个柜台，`<action>` 是办什么事，`--account` 是报哪张卡。同一个平台有几个号，就分几次报不同会员号，各办各的。

### 4.3 发布参数速查

发布参数分三层：视频通用参数 → 图文专用参数（仅三平台）→ 各平台扩展参数。先记通用层，再按平台查扩展层。

**视频通用参数**（`upload-video`）：

```bash
sau <platform> upload-video --account demo \
  --file video.mp4 \      # 必填：本地视频路径
  --title "标题" \         # 必填：标题
  --desc "描述" \          # 必填：描述
  --tags "科技,AI"         # 可选：标签，逗号分隔
```

**图文专用参数**（`upload-note`，仅抖音 / 快手 / 小红书）：

```bash
# 图文参数名从 --desc 换成 --note；图片用 --images 一次传多张
sau douyin upload-note --account demo \
  --images a.png b.png \   # 必填：图片路径，空格分隔多张
  --title "图文标题" \
  --note "图文正文"

# 抖音图文额外选项：--notef 传图文文件、--bgm 指定背景音乐
sau douyin upload-note --account demo \
  --images a.png b.png --title "标题" --note "正文" \
  --notef content.md --bgm "卡农"
```

一个容易记的元数据约定：**视频的正文 = title + desc + tags，图文的正文 = title + note + tags**。所以图文命令里没有 `--desc`，取而代之的是 `--note`。

**各平台扩展参数**：在通用参数之上，个别平台多了自己的选项，多为平台功能入口（分区、合集、可见性等）。

| 平台 | 扩展参数 | 说明 |
|------|---------|------|
| Bilibili | `--tid <分区id>` | 投稿分区，必填；示例 `249`。文档标「必填」，实际是否仍强制需实测 |
| YouTube | `--playlist <id>` / `--visibility <值>` | 投到指定播放列表 / 设置可见性；被墙网络需在 conf.py 配 `YT_PROXY` |
| 视频号 | `--collection` / `--draft` | 可选；精确语义以最新代码 / 实测为准 |
| 百家号 | `--collection` | 可选 |
| 支付宝生活号 | `--collection` | 可选；平台侧需先开通生活号创作 |
| 抖音 | `--product-link` / `--product-title` | 商品链接 / 商品标题（带货挂链场景） |

**定时发布**：在支持定时的平台上，传 `--schedule` 就切换为定时策略，不传则立即发布。参数是**绝对时间**：

```bash
# 格式固定为 "YYYY-MM-DD HH:MM"，传未来绝对时间，到点自动发布
sau douyin upload-video --account demo \
  --file demo.mp4 --title "标题" --desc "描述" \
  --schedule "2026-09-06 20:00"
```

CLI 的定时支持矩阵（比 4.1 能力矩阵更窄，以 CLI.md 为准）：

| 平台 | `--schedule` 定时 | 覆盖内容 |
|------|:--:|------|
| 抖音 `douyin` | ✅ | 视频 + 图文 |
| 快手 `kuaishou` | ✅ | 视频 + 图文 |
| 小红书 `xiaohongshu` | ✅ | 视频 + 图文 |
| Bilibili `bilibili` | ✅ | 仅视频 |
| 视频号 `tencent` | ✅ | 仅视频 |
| 百家号 `baijiahao` | ❌ | — |
| 支付宝生活号 `alipay` | ❌ | — |
| 微博 `weibo` | ❌ | — |
| 虎扑 `hupu` | ❌ | — |
| YouTube `youtube` | ❌ | CLI.md 支持表未列（能力矩阵亦为 ❌） |
| TikTok | 不可用 | 能力矩阵标 ✅，但未接入 CLI |

> [!tip] 大白话：把 `--schedule` 想成「预约上架」
> 传了 `--schedule "YYYY-MM-DD HH:MM"`，命令就从「现在立刻发」变成「到点自动发」；不传才是立即发布。作者提到定时时间计算默认按「第二天」策略处理边界——也就是约的是未来某天的绝对时刻，跨天 / 边界情况按此推算。具体边界以实测为准。

### 4.4 成功/失败判定缺口

看到这里，你可能会想找一张「成功输出长什么样、失败退出码是多少」的表——但翻遍 README、docs/install.md、docs/CLI.md，**都没有说明命令的输出格式、退出码或成功标志**。这是当前文档的一个真实缺口（[docs/CLI.md](https://github.com/dreammis/social-auto-upload/blob/main/docs/CLI.md)）。

所以本笔记不臆造任何返回约定，实践上按下面三步确认：

1. **以 CLI 输出 / 实测为准**：跑一次上传，观察当前版本实际打印了什么；
2. **回平台侧确认**：发布后到对应平台的创作者后台 / 作品页看作品是否真的出现，这是最硬的判据；
3. **需要代码级判定时再看实现**：想写脚本判断成功与否，去读对应平台 uploader 实现或 `sau_cli.py`，而不是猜 JSON 字段。

> [!warning] 别采信「返回 0 即成功」这类说法
> 因为文档没定输出 / 退出码约定，任何第三方教程写的成功判定格式都可能对不上你的版本。遇到这类说法，先在自己环境实测一次再采信；平台改版或项目升版后，判定方式也可能变（机制详见第 5、6 章）。

### 本章小结

- 11 个平台里 10 个已接入 `sau` CLI（YouTube 按 CLI.md 判定已接入，README 行文漏写）；TikTok 未接入，走历史 example。
- 图文能力仅抖音 / 小红书 / 快手三平台支持；其余平台只能发视频。
- CLI 统一结构 `sau <platform> <action> --account <name>`，`--account` 通用必选；动作固定为 login → check → upload-video / upload-note 三件套。
- 视频参数通用 `--file / --title / --desc`，图文用 `--images / --title / --note`；平台扩展参数（B 站 `--tid`、视频号 `--collection / --draft`、YouTube `--playlist / --visibility` 等）按扩展表查。
- 定时发布用 `--schedule "YYYY-MM-DD HH:MM"`；CLI 支持抖音 / 快手 / 小红书 / B站 / 视频号，百家号 / 支付宝 / 微博 / 虎扑不支持。
- 成功 / 失败判定文档缺口未补：以 CLI 输出 / 实测为准，发布后回平台侧确认。

下一章从「命令怎么拼」转向「为什么时灵时不灵」：登录态到底存在哪、`check` 凭什么判断失效、Cookie 过期和平台风控怎么绕——把第 3、4 章里 `login` 那一步背后的机制讲透。
