---
title: Strm 流文件与 302 播放详解
aliases:
  - Strm 教程
  - 302 重定向入门
  - Strm 与 302
tags:
  - 流媒体
  - Strm
  - HTTP
  - 302重定向
  - IPTV
  - 入门教程
created: 2026-02-10
updated: 2026-10-04
status: active
source_project: study-system
---

# Strm 流文件与 302 播放详解

> [!summary] 一句话先看懂
> **Strm 文件**就是一个「只写了一行网址的记事本」，它里面没有视频；**302 播放**是服务器「指路」的过程——你问它要视频，它说「你去另一个地址拿」。这两样东西经常搭伙用，让你用一个几百字节的小文件、一个会过期的安全地址，播放网上的视频。

> [!tip] 这篇笔记该怎么读
> - **完全零基础**：按 0 → 1 → 2 → 3 → 4 → 5 的顺序读，**第 6 节（动手实践）先跳过**。
> - **只想搞懂概念**：读第 0 节和第 1 节就够了。
> - **想自己动手做**：先读第 2、3 节理解原理，再跳到第 6 节照着做。

## 目录

1. [三分钟速览（零基础先读）](#1-三分钟速览零基础先读)
2. [名词扫盲表（看不懂就回来查）](#2-名词扫盲表看不懂就回来查)
3. [Strm 流文件到底是什么](#3-strm-流文件到底是什么)
4. [302 播放到底是什么](#4-302-播放到底是什么)
5. [Strm 和 302 是怎么配合的](#5-strm-和-302-是怎么配合的)
6. [我什么时候会用到它（使用场景）](#6-我什么时候会用到它使用场景)
7. [动手实践（进阶，新手可跳过）](#7-动手实践进阶新手可跳过)
8. [常见问题 FAQ](#8-常见问题-faq)
9. [速查表与总结](#9-速查表与总结)

---

## 1. 三分钟速览（零基础先读）

### 1.1 先打个比方

想象你要把一部电影分享给朋友的播放器：

| 现实生活 | 电脑里对应的事 |
|---|---|
| 你不能把整部电影抄一份给朋友（太大） | 视频文件太大，不想复制、不想下载 |
| 你写一张小纸条，上面只写「电影在 xx 网站」 | 你创建一个 **Strm 文件**，里面只写一个网址 |
| 朋友按地址去找，网站老板说「我这儿没有，你去隔壁仓库拿」 | 服务器回一个 **302 重定向**，告诉播放器去新地址 |
| 朋友最终在隔壁仓库看到了电影 | 播放器自动跟过去，播放到视频 |

所以：

- **Strm 文件 = 一张写着网址的小纸条**（不是电影本身）
- **302 = 老板给你指路**（不是直接给电影，而是告诉你换个地方拿）

### 1.2 一张图看懂

```text
你的播放器
    │  ① 打开 电影.strm（里面写着 https://api.xxx.com/play?id=123）
    ▼
API 服务器  （"总台"，负责验证你有没有权限）
    │  ② 回一句：302，去 https://cdn.xxx.com/movie.m3u8?token=abc 拿
    ▼
CDN 服务器  （"离你最近的仓库"，真正存视频的地方）
    │  ③ 检查 token 没过期 → 把视频发给你
    ▼
你的播放器开始播放 🎬
```

### 1.3 这事跟我有关系吗？

如果你遇到下面这些情况，这篇笔记就有用：

- 你在用 **电视盒子、NAS、Emby / Jellyfin / Plex、Kodi** 搭建自己的家庭影院；
- 你想看 **IPTV 网络电视直播**，手里有一堆 `.m3u` / `.strm` 播放源；
- 你好奇「为什么我直接复制一个视频链接，过一会儿就打不开了」；
- 你想自己动手做个能播放直播源的小工具。

如果只是想看个概念，读完第 2、3 节就够了。

---

## 2. 名词扫盲表（看不懂就回来查）

> [!note] 新手遇到看不懂的词，回这张表查。第一次出现的术语，后面都会再解释一遍。

| 名词 | 大白话解释 | 你会遇到的场景 |
|---|---|---|
| **文件扩展名** | 文件名最后那一段（如 `.strm`、`.mp4`），告诉电脑「这是什么类型的文件」 | 看到 `CCTV1.strm`，知道它是 Strm 文件 |
| **URL / 网址** | 一个资源的「门牌地址」，如 `https://example.com/a.mp4` | Strm 文件里写的就是它 |
| **HTTP** | 浏览器/播放器和服务器「说话」的一套规则 | 所有网页、视频请求都靠它 |
| **状态码** | 服务器回话时的「结果编号」，200 = 成功，302 = 换个地址，404 = 找不到 | 302 播放的核心就是它 |
| **302 重定向** | 「你要的东西不在这，去这个新地址拿」，属于**临时**转发 | 视频网站防盗链、分流 |
| **m3u8** | 一种「播放清单」文件，里面列着一小段一小段的视频地址 | 直播、在线视频常见 |
| **HLS** | 把视频切成很多小片段、边下边播的技术，清单文件就是 m3u8 | 苹果设备、直播流常用 |
| **MP4** | 最常见的视频文件格式，可以整段下载 | 本地视频、点播 |
| **CDN** | 「内容分发网络」：把视频复制到离你最近的服务器，让你看得更快 | 大网站的加速手段 |
| **token** | 一段临时的「通行证密码」，用来证明你有权限看 | 302 跳转后的地址常带它 |
| **防盗链** | 防止别人直接盗用你的视频地址（白嫖你的流量） | 真实地址为什么要藏起来 |
| **负载均衡** | 「分流」：把大量用户分散到不同服务器，避免挤爆 | 大网站用 302 把用户分到不同机器 |
| **IPTV** | 网络电视：通过互联网看电视直播，而不是有线电视 | `.m3u` / `.strm` 直播源 |
| **Kodi / Emby / Jellyfin / Plex** | 媒体中心软件，相当于「自己家的电视台 + 影院 App」 | 用来管理、播放这些源 |
| **电视盒子 / NAS** | 前者是插在电视上的小电脑，后者是家用的网络存储服务器 | 它们存储空间有限，所以爱用 Strm |
| **ffmpeg / yt-dlp** | 命令行音视频处理/下载工具，能自动跟随 302 | 进阶玩家用 |
| **referer / user-agent** | 请求时附带的两条信息：referer =「我从哪个页面来」，user-agent =「我是什么客户端」 | 有些源会检查它们来防盗链 |

---

## 3. Strm 流文件到底是什么

### 3.1 一句话解释

**Strm 流文件**是一种特殊的文本文件（扩展名 `.strm`），里面存的是**媒体资源的播放地址**，而不是媒体内容本身。

> [!note] 通俗理解
> 把它想成播放器的「快捷方式」或「书签」：文件本身没有视频/音频，只有一个指向真实内容的「指针」（网址）。播放器打开它时，会读出里面的网址，然后直接从网络加载播放。

**它长什么样（真的就这么简单）：**

```text
# 文件名：电影.strm，内容只有一行
https://example.com/video.m3u8
```

**为什么叫 Strm？**

- Strm = **St**rea**m**（流）的缩写；
- 表示这是一个「流媒体引用文件」。

### 3.2 Strm 文件的特点

| 特性 | 说明 |
|------|------|
| **文件大小** | 极小（通常几字节到几百字节，就是一行网址那么长） |
| **内容格式** | 纯文本，第一行是 URL |
| **扩展名** | `.strm` |
| **不包含媒体数据** | 只存地址，不存内容 |
| **实时播放** | 直接从源播放，不下载到本地 |

### 3.3 它和「快捷方式（.lnk）」有什么区别

很多人会问：这不就是个快捷方式吗？其实不太一样：

| | Strm 文件 | Windows 快捷方式 |
|---|---|---|
| **指向什么** | 网络地址（网址） | 本地文件 / 程序 |
| **跨平台吗** | 是（Windows / Linux / Mac / 盒子都能认） | 基本只在 Windows |
| **内容形式** | 纯文本，你能一眼看懂、能改 | 二进制，乱码看不了 |
| **谁来打开** | 需要支持网络流的播放器 | 系统直接打开 |

### 3.4 最常见的用法：把「一堆源」整理成「一堆小文件」

```text
直播源文件/
├── CCTV1.strm          # 里面写着 https://...
├── CCTV2.strm          # 里面写着 https://...
├── 体育频道.strm        # 里面写着 https://...
└── 新闻频道.strm        # 里面写着 https://...
```

每个文件几百字节，整个目录加起来可能还不到 1 MB，却可以管理成百上千个频道。

### 3.5 为什么大家爱用 Strm（4 个好处）

1. **省空间**：不用把视频下载下来，适合存储有限的电视盒子。
2. **实时更新**：源变了，只要改文件里的那一行网址即可。
3. **统一管理**：所有源都是同一类小文件，方便批量操作。
4. **加载快**：读一个文本文件几乎不耗时。

### 3.6 手动创建一个 Strm 文件（不需要会编程！）

这是最适合新手的方法，用系统自带的记事本 / 文本编辑器就能做：

1. 新建一个文本文件；
2. 第一行写上播放地址（比如一个 `.m3u8` 或 `.mp4` 网址）；
3. 保存；
4. 把文件名后缀从 `.txt` 改成 `.strm`（Windows 要留意「显示文件扩展名」开关，否则可能变成 `电影.strm.txt`）。

**示例：**

```text
# 文件名：电影.strm
https://cdn.example.com/movie.m3u8
```

改完就能拖进 Emby / Jellyfin / Kodi 之类的播放器里试播了。

---

## 4. 302 播放到底是什么

### 4.1 一句话解释

**302 播放**指的是利用 HTTP 的 **302 重定向**状态码，先问到一个「临时的真实地址」，再去那里播放媒体资源的技术。

> [!note] 通俗理解
> 这像一场「寻宝问路」：你问甲宝藏在哪，甲说「去问乙」；你问乙，乙说「去问丙」；最后丙才给你真正的地址。302 就是这个「指路」的过程——每一次指路，就是一次 302 跳转。

**先把 HTTP 状态码看简单点：**

| 状态码 | 含义 | 大白话 |
|---|---|---|
| 200 | OK | 「东西在这儿，拿去」（直接给内容） |
| 302 | Found | 「东西不在这儿，去这个新地址拿」（临时转发） |
| 404 | Not Found | 「你要的东西不存在」 |

**302 响应长这样：**

```text
HTTP/1.1 302 Found
Location: https://cdn.example.com/v123/master.m3u8?token=abc123
                                                  ↑ 新地址写在 Location 这一行
```

### 4.2 完整的「一次 302」是几步

```text
1. 播放器请求播放地址
   GET https://api.example.com/play?id=123

2. 服务器返回 302 重定向
   HTTP/1.1 302 Found
   Location: https://cdn.example.com/v123/master.m3u8?token=abc123

3. 播放器自动跳到新地址
   GET https://cdn.example.com/v123/master.m3u8?token=abc123

4. 拿到媒体内容（这里是 m3u8 播放清单）并开始播放
```

**有时候会连跳好几次：**

```text
原始请求
    ↓
302 跳转 1 → API 服务器（验证权限）
    ↓
302 跳转 2 → 负载均衡服务器（决定给你哪台机器）
    ↓
302 跳转 3 → CDN 节点（离你最近的仓库）
    ↓
最终拿到真实地址，开始播放
```

> [!warning] 跳转不是无限的
> 大多数播放器会限制 5～20 次跳转，跳太多会直接报错。所以正常情况下「几跳之内」必须落到真实地址。

### 4.3 为什么要这么「绕」（直接给真实地址不行吗）

一开始你可能会想：直接把真实地址给播放器不就完了，干嘛要 302 绕一圈？因为「绕」能解决 4 个现实问题：

**① 防盗链 / 隐藏真实地址**

```text
用户请求视频
    ↓
服务器返回 302 → 指向带 token 的真实地址
    ↓
播放器按 302 指向去请求真实地址
    ↓
真实地址里可能带着：临时 token、IP 限制、过期时间戳
```

好处：真实地址不暴露；地址可以动态生成、会过期，防止别人直接分享白嫖。

**② 负载均衡（分流）**

```text
请求进入
    ↓
302 重定向到不同服务器
    ├── → 服务器 A（亚洲用户）
    ├── → 服务器 B（美洲用户）
    └── → 服务器 C（欧洲用户）
```

**③ 内容分发优化**

- 根据你的位置，重定向到最近的 CDN 节点；
- 根据网络状况，选择最优线路；
- 根据设备类型，返回不同编码。

**④ 统计与权限控制**

- 在 302 服务器上统计播放次数；
- 校验来源页面（referer）、客户端（user-agent）、IP、时间，不合法就拒绝。

### 4.4 302 地址里常见的参数

| 参数 | 作用（大白话） |
|------|------|
| `token` | 通行证密码，证明你有权限 |
| `expire` | 过期时间戳，过了这个点地址就作废 |
| `ip` | 只允许这个 IP 访问 |
| `referer` | 只允许从这个来源页面访问 |
| `user-agent` | 只允许特定的客户端（播放器）访问 |

---

## 5. Strm 和 302 是怎么配合的

### 5.1 组合使用的场景

```text
场景：播放一个「需要 302 重定向」的视频

1. 创建 Strm 文件
   内容：https://api.example.com/play?id=123

2. 播放器打开这个 Strm 文件

3. 播放器请求里面的 URL，服务器返回 302 重定向

4. 播放器自动跟随 302，拿到真实地址

5. 播放真实地址的视频
```

> [!tip] 记忆口诀
> **Strm 负责「记住去问谁」，302 负责「临时告诉你真实在哪」。**
> Strm 里存的是稳定的 API 地址，真实地址则交给 302 动态生成、随时更换。

### 5.2 为什么这样设计有好处

```text
┌─────────────────────────────────────────┐
│  好处 1：简化 Strm 文件管理              │
│  Strm 只需存 API 地址，不用频繁更新      │
├─────────────────────────────────────────┤
│  好处 2：保护真实源地址                  │
│  真实地址通过 302 动态生成，不易被扒取   │
├─────────────────────────────────────────┤
│  好处 3：灵活切换源                      │
│  后端改一下 302 指向，客户端无需更新     │
└─────────────────────────────────────────┘
```

### 5.3 实际案例：IPTV 直播源

```text
IPTV 直播源配置（m3u 文件）

#EXTINF:-1,CCTV-1
https://api.iptv.com/channel?cctv1   ← 这个 URL 会 302 重定向

#EXTINF:-1,CCTV-2
https://api.iptv.com/channel?cctv2   ← 这个 URL 会 302 重定向

#EXTINF:-1,湖南卫视
https://api.iptv.com/channel?hunan   ← 这个 URL 会 302 重定向
```

**流程：**

1. 播放器读取频道地址；
2. 请求返回 302，重定向到真实直播流；
3. 播放器自动跟随并播放。

---

## 6. 我什么时候会用到它（使用场景）

| 场景 | 它是怎么用的 |
|------|-------------|
| **IPTV 直播** | Strm 存 API 地址，点开时 API 302 到真实直播流 |
| **视频网站** | 点播放 → 后端验证权限 → 302 到带 token 的 CDN 地址 |
| **家庭媒体中心** | Emby / Jellyfin / Kodi 用 Strm 管理外部源，不占本地空间 |
| **CDN 分发** | 302 把用户引到最近的节点，看视频更快 |
| **直播源管理** | 每个频道一个 `.strm` 文件，源变了改文件即可 |

---

## 7. 动手实践（进阶，新手可跳过）

> [!warning] 这一节假设你会用「命令行」或「Python」
> 完全零基础可以先跳过，等以后需要了再回来。核心原理在第 3、4、5 节已经讲完了。

### 7.1 批量创建 Strm 文件

**方法一：命令行（Linux / Mac）**

```bash
# 单个创建
echo "https://example.com/video.m3u8" > 视频.strm

# 批量创建（从一个 URL 列表文件 urls.txt 逐行读取）
while read -r url name; do
    echo "$url" > "$name.strm"
done < urls.txt
```

**方法二：Python 批量创建**

```python
# 创建 Strm 文件
def create_strm(url, filename):
    with open(f"{filename}.strm", "w", encoding="utf-8") as f:
        f.write(url)

# 示例：创建直播源
sources = {
    "CCTV1": "https://live.example.com/cctv1.m3u8",
    "CCTV2": "https://live.example.com/cctv2.m3u8",
    "湖南卫视": "https://live.example.com/hunan.m3u8",
}

for name, url in sources.items():
    create_strm(url, name)
```

### 7.2 Strm 文件的高级用法

**在 URL 后附加元数据（部分播放器支持）：**

```text
# 基础 URL
https://example.com/video.m3u8

# 带标题（用 # 号）
https://example.com/video.m3u8#标题

# 带 Kodi 专用参数（让 Kodi 用特定解码器处理 HLS）
https://example.com/video.m3u8
#KODIPROP:inputstream=inputstream.adaptive
#KODIPROP:inputstream.adaptive.manifest_type=hls
```

**把源分门别类组织：**

```text
媒体库/
├── 直播/
│   ├── 央视频道/
│   │   ├── CCTV1.strm
│   │   ├── CCTV2.strm
│   │   └── CCTV13.strm
│   └── 卫视频道/
│       ├── 湖南卫视.strm
│       └── 浙江卫视.strm
└── 电影/
    ├── 动作片/
    └── 喜剧片/
```

### 7.3 获取 302 后的真实地址

**方法一：播放器自动跟随（最省事）**

大多数现代播放器会自动处理 302，你什么都不用做：

- 浏览器、VLC、MPV、Kodi、Emby、ffmpeg、yt-dlp 都会自动跟随。

**方法二：curl 只看重定向地址**

```bash
# -I 只取响应头，-s 静默模式，grep 过滤出 Location 那一行
curl -I -s https://api.example.com/play?id=123 | grep -i location

# -L 表示自动跟随重定向（直接拿到最终内容）
curl -L https://example.com/play?id=123
```

**方法三：Python 手动解析**

```python
import requests

def get_real_url(api_url):
    """跟随 302 重定向，获取真实播放地址"""
    # allow_redirects=False：不要自动跳，我要自己看 302 指向哪
    response = requests.head(api_url, allow_redirects=False)

    if response.status_code == 302:
        return response.headers.get("Location")
    elif response.status_code == 200:
        return api_url  # 已经直接返回内容
    else:
        raise Exception(f"请求失败: {response.status_code}")

api_url = "https://api.example.com/play?id=123"
print(f"真实播放地址: {get_real_url(api_url)}")
```

**方法四：JavaScript（浏览器 / Node.js）**

```javascript
async function getRedirectUrl(url) {
    const response = await fetch(url, {
        method: "HEAD",
        redirect: "manual", // 不自动跟随，手动看 302
    });

    if (response.status === 302) {
        return response.headers.get("Location");
    }
    return url;
}

getRedirectUrl("https://api.example.com/play?id=123")
    .then(realUrl => console.log(realUrl));
```

### 7.4 综合案例：处理 302 直播源并生成 Strm

```python
import requests

class LiveChannel:
    """处理 302 重定向的直播频道"""

    def __init__(self, api_url):
        self.api_url = api_url
        self.real_url = None
        self.token = None

    def get_real_url(self):
        """获取 302 重定向后的真实地址"""
        try:
            response = requests.head(self.api_url, timeout=5, allow_redirects=False)

            if response.status_code == 302:
                self.real_url = response.headers.get("Location")
                if "token=" in self.real_url:  # 顺便把 token 抠出来演示
                    self.token = self.real_url.split("token=")[1].split("&")[0]
                return True
            elif response.status_code == 200:
                self.real_url = self.api_url
                return True
            else:
                print(f"获取失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"请求错误: {e}")
            return False

    def create_strm(self, filename):
        """创建 Strm 文件"""
        if self.get_real_url():
            with open(f"{filename}.strm", "w", encoding="utf-8") as f:
                f.write(self.real_url)
            print(f"创建成功: {filename}.strm → {self.real_url}")
        else:
            print("创建失败: 无法获取播放地址")

channel = LiveChannel("https://api.example.com/play?channel=cctv1")
channel.create_strm("CCTV1")
```

### 7.5 案例：解析 m3u 播放列表，批量生成 Strm

```python
import os
import re
import requests

def parse_m3u_and_generate_strm(m3u_url, output_dir):
    """解析 m3u 播放列表，生成一堆 Strm 文件"""
    response = requests.get(m3u_url)
    m3u_content = response.text

    os.makedirs(output_dir, exist_ok=True)

    current_name = None
    for line in m3u_content.split("\n"):
        line = line.strip()

        if line.startswith("#EXTINF:"):
            # #EXTINF:-1,CCTV-1  → 取逗号后面的频道名
            match = re.search(r",(.+)$", line)
            if match:
                current_name = match.group(1).strip()

        elif line.startswith("http") and current_name:
            filename = f"{output_dir}/{current_name}.strm"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(line)
            print(f"创建: {filename}")
            current_name = None

parse_m3u_and_generate_strm(
    m3u_url="https://example.com/iptv.m3u",
    output_dir="直播源",
)
```

### 7.6 案例：自己搭一个最简单的 302 重定向服务器

用 Flask（一个 Python 的网页框架）几行代码就能模拟一个「会指路的服务器」：

```python
from flask import Flask, redirect, request

app = Flask(__name__)

# 模拟的直播源数据库
live_sources = {
    "cctv1": "https://cdn1.example.com/cctv1.m3u8",
    "cctv2": "https://cdn2.example.com/cctv2.m3u8",
    "hunan": "https://cdn3.example.com/hunan.m3u8",
}

@app.route("/play")
def play():
    """返回 302 重定向到真实播放地址"""
    channel = request.args.get("channel")
    if channel in live_sources:
        return redirect(live_sources[channel], code=302)
    return "频道不存在", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

访问 `http://localhost:8080/play?channel=cctv1`，就会 302 跳到 `https://cdn1.example.com/cctv1.m3u8`。

---

## 8. 常见问题 FAQ

### Q1：Strm 文件和快捷方式（.lnk）有什么区别？

| | Strm 文件 | 快捷方式 |
|---|---|---|
| **用途** | 指向网络地址 | 指向本地文件 / 程序 |
| **平台** | 跨平台 | 平台特定 |
| **内容** | 文本格式，可读可改 | 二进制格式 |
| **播放器** | 需要支持网络流 | 系统打开 |

### Q2：为什么要用 302，而不是直接返回真实地址？

**用 302 的好处：**

1. **安全性**：真实地址带动态 token，不暴露给用户；
2. **灵活性**：后端可以随时切换 CDN 或源站；
3. **负载均衡**：根据请求重定向到不同服务器；
4. **统计**：可以在 302 服务器上统计播放次数；
5. **防盗链**：可以验证来源、时间、IP 等。

### Q3：播放器怎么处理 302？

大多数现代播放器会自动处理：浏览器、VLC / MPV、Kodi / Emby、ffmpeg / yt-dlp 都会自动跟随。如果需要手动处理，才用第 7.3 节的方式获取 302 后的地址。

### Q4：怎么测试一个链接是不是 302？

```bash
# 方法一：curl（-v 会打印详细过程，能看到 302 那一步）
curl -I -v https://example.com/play?id=123
```

```python
# 方法二：Python
import requests
r = requests.head("https://example.com/play?id=123", allow_redirects=False)
print(r.status_code)                 # 302
print(r.headers.get("Location"))     # 跳转后的地址
```

方法三：用在线工具，比如 `https://httpstatus.io/`。

### Q5：302 重定向有限制吗？

有，一般有：

- **跳转次数限制**：大多数播放器限制 5～20 次；
- **时间限制**：token 有过期时间；
- **IP 限制**：有些源只允许从请求的那个 IP 访问。

### Q6：Strm 文件能播放本地文件吗？

可以！格式照样写路径就行：

```text
# Windows
E:\Videos\movie.mp4

# Linux / Mac
/home/user/Videos/movie.mp4

# 网络路径（共享盘）
\\server\share\video.mp4
smb://server/share/video.mp4
```

### Q7：Strm 播放失败怎么排查？

1. **看内容**：用文本编辑器打开 `.strm`，确认 URL 是否正确；
2. **测链接**：拿浏览器或 curl 试试这个 URL 通不通；
3. **查 302**：是不是返回了有效的重定向地址（有的地址会过期）；
4. **看格式**：URL 结尾格式对不对（`.m3u8`、`.mp4` 等）；
5. **看日志**：Kodi、VLC 等都有日志功能，报错信息往往直接指出问题。

---

## 9. 速查表与总结

### 9.1 概念速查

| 概念 | 本质 | 一句话用途 |
|------|------|-----------|
| **Strm 文件** | 存放 URL 的纯文本文件 | 播放器的「快捷方式」，告诉它去哪找 |
| **302 播放** | HTTP 重定向机制 | 动态告诉你「真实地址」在哪 |

### 9.2 使用场景速览

```text
┌─────────────────────────────────────┐
│  IPTV 直播  → Strm 文件 + 302 重定向 │
├─────────────────────────────────────┤
│  视频网站   → API 接口返回 302 重定向 │
├─────────────────────────────────────┤
│  媒体中心   → Strm 管理外部源        │
├─────────────────────────────────────┤
│  CDN 分发   → 302 指向最近节点       │
└─────────────────────────────────────┘
```

### 9.3 最该记住的 4 句话

- **Strm 不存储内容**，只存储地址（一个写着网址的小文件）；
- **302 用于隐藏 / 保护真实地址**（服务器帮你指路）；
- **现代播放器会自动处理 302**，你不用手动跳；
- **两者常结合使用**：Strm 存稳定的 API 地址，API 返回 302 指向真实视频。

---

## 相关笔记

- [[硬件解码vs软件解码]] —— 视频播放时，到底是 CPU 还是显卡在干活。

---

## 更新记录

| 日期 | 版本 | 变更摘要 |
|------|------|----------|
| 2026-02-10 | v1.0 | 初版创建 |
| 2026-10-04 | v1.1 | 面向新手重写：补充 YAML frontmatter；新增「三分钟速览」「名词扫盲表」「相关笔记」；为 m3u8 / HLS / CDN / token / 防盗链 / 负载均衡等术语补大白话解释与生活比喻；把零散代码集中到「动手实践（进阶，新手可跳过）」；修正 7.6 案例中缺失的 `request` 导入；重排 FAQ 与总结。技术内容与代码示例无删减。 |
