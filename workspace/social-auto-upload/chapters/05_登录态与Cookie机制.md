## 第 5 章 登录态与 Cookie 机制

第 3 章你跑通了 `login → check → upload-video` 的最小闭环，但多半只知其然：`login` 到底把登录态存到了哪里？`check` 凭什么判断「已失效」？一旦平台风控拦下自动化登录，还有什么逃生通道？本章把这三件事讲透——它们是理解第 6 章所有排错案例的前提。

### 5.1 登录态存储与账号模型

第 3 章反复强调过一个模型：**一个 `account_name` = 一个账号文件**。落到磁盘上，这个「账号文件」是一份 JSON，固定放在 `cookies/[平台]/[平台]_[account].json`（具体目录/文件名的拼写以最新代码为准）。比如抖音建了 `demo` 和 `work` 两个账号，结构大致是这样：

```text
cookies/
├── douyin/
│   ├── douyin_demo.json     # --account demo 的抖音登录态
│   └── douyin_work.json     # --account work 的抖音登录态
├── xiaohongshu/
│   └── xiaohongshu_demo.json
└── kuaishou/
    └── kuaishou_demo.json
```

有两点值得记住：

1. **目录和文件都按「平台 + 账号名」分区**，所以同一平台可以并存多个账号，多账号并发时 `--account` 就是挑选对应文件的钥匙。
2. **这份 JSON 不是一串普通 cookie，而是 patchright/playwright 的 `storage_state` 序列化结果**——里面除了各站点的 cookie，还包含 localStorage 等浏览器本地状态。抖音的登录态有一部分就放在 localStorage 里，所以抖音专用导出脚本会连 localStorage 一起带走。

这也回头印证了 conf.py 的极简设计：官方配置里**没有**「cookie 路径」这类键，因为路径规则是写死在代码里的约定。你只需保证 `--account` 的名字和登录时一致，脚本自己会去对应位置找文件，不要臆造或手工改名。

> [!tip] 大白话：cookie 文件里不只有 cookie
> cookie 是平台发你的「临时工牌」，证明你登录过；localStorage 则是浏览器本地「储物柜里的便签」，是站点自己记的小账本。抖音既发工牌、又往便签上写字，所以它的登录态文件要把「工牌 + 便签」一起存，缺一样都可能被当成陌生人。

### 5.2 `check` 怎么判失效

`check` 并不会打开 cookie 文件逐项核对有效期，而是**开着浏览器导航到该平台的发布/上传页，看页面是否出现登录 UI**：出现了，就判定 cookie 已失效；没出现，就认为还能用。以抖音为例，`sau douyin check --account demo` 会进入创作服务平台的发布页，如果页面冒出「扫码登录」字样，check 即报未登录。

各平台靠什么元素判失效，是跟着页面改版走的易变信息。下表是调研时（2026-09）代码里的失效信号，使用前**以最新代码为准**：

| 平台（CLI 前缀） | 典型失效信号 | 说明 |
|---|---|---|
| 抖音 `douyin` | 页面出现「扫码登录」 | 登录框弹出即判失效 |
| 快手 `kuaishou` | 「机构服务」选择器 | 出现该元素视为未进入创作者后台 |
| 视频号 `tencent` | 「微信小店」 | 出现视为停在登录页/非目标页 |
| 小红书 `xiaohongshu` | 「手机号 / 扫码登录」 | 出现登录面板即判失效 |

> [!warning] `check` 看的是间接证据，存在竞态误判
> 用「页面上有没有登录 UI」反推「cookie 有没有失效」，本质是看间接证据，而不是核对 cookie 本身。页面加载稍慢、平台改版让选择器对不上（[Issue #230](https://github.com/dreammis/social-auto-upload/issues/230)），check 都可能在 cookie 仍然有效时误报 `invalid`（[#224](https://github.com/dreammis/social-auto-upload/issues/224) 讨论区也多次出现，属真实案例，勿当必然）。真遇到「明明刚登录过、check 却说失效」，先 `git pull` 升到最新代码，再去 Issues 搜同款症状。社区讨论给出的改进方向是改判 `sessionid` 这类登录 cookie 是否存在，而不是看 UI 文案——但这仍是 issue 中的建议，是否合入以最新代码为准。

> [!tip] 大白话：check 像个「看动作」的保安
> check 不查你工牌的签发日期，而是看「有没有人朝闸机走」：画面里一出现「扫码登录」四个字，它就当你还没进门。所以闸机还没完全打开、或保安一时眼花（页面加载慢、改版），它也会误拦明明有卡的人。

### 5.3 高风控逃生通道：CDP 9222 导出真实浏览器登录态（抖音）

自动化登录最怕平台风控。headless 环境下抖音、快手常出现「扫码后二维码异常 / 登录超时」（[#224](https://github.com/dreammis/social-auto-upload/issues/224)，真实案例），无头浏览器的指纹太明显，平台不给你完成登录。此时不要硬刚，改用**真实浏览器登录态复用**：让真人在 VNC/桌面里用真实 Chrome 登录一次，再把这份登录态「导出」给自动化用。完整流程三步：

```bash
# ① 在 VNC / 桌面环境启动真实 Chrome，开启 Remote Debugging Port 9222
#   （Linux 服务器示例；Windows 换成 chrome.exe 的全路径）
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/douyin-profile"
```

② 在弹出的 Chrome 里手动登录 `creator.douyin.com`（扫码或短信均可），确认进到创作服务平台后再继续；③ 登录态就绪后，在项目根目录执行导出与校验：

```bash
# ③ 连接 9222，抽取 cookie + localStorage，写成 uploader 可读的 storage_state JSON
bash export_douyin_cookie.sh --account demo

# ④ 校验这份登录态是否被认可
sau douyin check --account demo
```

原理：9222 是 Chrome 的 **Remote Debugging Port（远程调试端口）**。Chrome 开启该端口后，外部程序就能通过 CDP（Chrome DevTools Protocol）向它询问「当前浏览器里有哪些 cookie、哪些 localStorage」。[`export_douyin_cookie.sh`](https://github.com/dreammis/social-auto-upload) 做的事就是：连上 `http://127.0.0.1:9222`，用 CDP 的 `Network.getAllCookies` 拿到全部 cookie，再在页面里执行 JS 抽出 localStorage，最后打包成和 `sau douyin login` 写出的同款 JSON，落到 `cookies/douyin/douyin_<account>.json`。之后 `check` 与 `upload-video` 走无头浏览器加载这份 JSON，等于自动化替身「借」到了真实登录凭证。

> [!tip] 大白话：别让替身再闯一次门禁
> 把 headless 自动化想成「替身演员」，把 VNC 里那台真实 Chrome 想成「本尊」。替身自己去走扫码登录，保安（风控）一眼识破；CDP 9222 的做法是让替身直接**复刻本尊的门禁卡**——本尊只登录一次，导出脚本把整套凭证拷给替身，之后替身刷卡进场。脚本目前针对抖音（`export_douyin_cookie.sh`），其它平台思路相同、脚本各异。

### 5.4 短信验证码与扫码

自动化登录还常遇到两类需要「真人」介入的关卡：短信验证码和扫码。工具的处理方式是把它们变成显式的「喂给 / 扫给」动作，而不是偷偷破解。

**短信验证码：`verify_code.txt` 喂码。** 平台会向手机发验证码，脚本不替你收短信，而是停在「等待输入验证码」状态，去项目根目录找 `verify_code.txt`。你把收到的验证码写进这个文件，脚本读到后自动填入并提交；**验证完成后文件会被自动删除**，避免残留敏感信息，下次需要就再写一张。

**扫码：直接把二维码展示给你。** 需要扫码时，脚本会把二维码图片显示出来（桌面 / agent 场景），你掏出手机 App 扫一下即可；工具不会去做 OCR 之类的事。

这两类机制背后是同一条心法：**登录被风控时，优先「复用真实浏览器登录态」，而不是硬刚自动化**。扫码 / 短信只是第一道坎；headless 指纹、异地 IP、海外登录（小红书 [Issue #226](https://github.com/dreammis/social-auto-upload/issues/226)）都可能让自动化登录在半路被拦。与其反复调参重试，不如退一步——用 5.3 的 CDP 9222 导出，或把 `LOCAL_CHROME_HEADLESS` 临时设 `False` 走有头浏览器，让「人登录一次，机器接管以后」。

> [!tip] 大白话：验证码靠「传纸条」
> 脚本没有读短信的本事，它只认项目根目录里那张叫 `verify_code.txt` 的小纸条。你收到验证码就写上去，脚本读完纸条就撕掉（自动删除），下次要用再写一张。

### 本章小结

- 登录态落盘为 `cookies/[平台]/[平台]_[account].json`，本质是 patchright/playwright 的 `storage_state` JSON，抖音导出还带 localStorage；目录/文件命名规则以最新代码为准。
- `check` 不核对 cookie 有效期，而是导航到发布/上传页看是否出现登录 UI；各平台失效信号（抖音「扫码登录」/ 快手「机构服务」/ 视频号「微信小店」/ 小红书「手机号 / 扫码登录」）属易变信息，以最新代码为准。
- `check` 判失效存在竞态缺陷（[#224](https://github.com/dreammis/social-auto-upload/issues/224) / [#230](https://github.com/dreammis/social-auto-upload/issues/230)）：有效 cookie 也可能被误判 `invalid`，先升最新代码再排查。
- 高风控场景别硬刚自动化：VNC 开真实 Chrome 登录 `creator.douyin.com` → `bash export_douyin_cookie.sh --account <name>` → `sau douyin check`，本质是通过 CDP 9222 用 `Network.getAllCookies` + JS 把真实登录态导出成兼容 JSON。
- 短信验证码走根目录 `verify_code.txt` 喂码、验证后自动删除；扫码直接把二维码展示给用户扫。

下一章把这些机制落到真实运维上：headless 登录被识别、创作者中心改版导致选择器失效、视频号二维码 iframe、海外登录被 ban……每一条坑都能对应到本章的某个机制——先懂机制再看案例，排错才不会像无头苍蝇。
