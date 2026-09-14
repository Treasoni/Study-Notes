> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/zhi-neng-ge-dan-de-jin-jie-wan-fa.md).

# 智能歌单的进阶玩法

智能歌单功能 在音乐收藏-播放列表中

实现随机播放1

1. 标题包含空（必定满足）
2. 选择标准随机
3. 动态更新

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F5JXe2OLzd1SDKcpqBRDi%2Fimage.png?alt=media&amp;token=b5ff3ebb-45b2-47d4-b95d-c59323620d92" alt=""><figcaption><p>随机播放</p></figcaption></figure>

动态文件目录歌单

文件路径为周杰伦的都会动态添加到歌单中

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FwdiMYdgKOYrZFfjl1Z3T%2Fimage.png?alt=media&amp;token=4db10910-471b-4e01-b98c-414a7f1bab01" alt=""><figcaption></figcaption></figure>

更多场景组合，等待你的发掘

场景1：创建“最近添加”的播放列表&#x20;

需求：总是想听最近添加到音乐库的新歌曲。&#x20;

规则设置：

添加日期是“在过去一个月内” 结果：这个播放列表将自动包含所有在过去30天内添加到你的音乐库中的歌曲。当你添加新的曲目时，它们会自动出现在这个播放列表中。 场景2：锻炼时的动力播放列表 需求：想要一个充满活力的音乐来激励自己锻炼。 规则设置：

流派是“电子”或“摇滚” BPM（每分钟节拍数）大于120 结果：这个播放列表将只包含那些节奏较快、能够激发能量的电子或摇滚乐曲，非常适合用来跑步或健身。 场景3：通勤放松播放列表 需求：希望有一个播放列表，在每天上下班途中可以听到轻松的音乐。 规则设置：

流派是“爵士”或“民谣” 评分等于或高于4星 播放时间小于5分钟 结果：这个播放列表将会包括你个人评价较高且适合短途聆听的爵士或民谣风格的歌曲，帮助你在通勤过程中放松心情。 场景4：发现新音乐 需求：想要探索未曾听过的新歌曲。 规则设置：

播放计数等于0 添加日期是“在过去六个月内” 结果：此播放列表将展示所有在过去半年内加入但尚未收听过的歌曲，鼓励你去尝试和发现新音乐。 场景5：经典老歌怀旧夜 需求：组织一个以经典老歌为主题的聚会。 规则设置：

年份介于1960年至1989年之间 专辑艺术家不是“Various Artists” 结果：这个播放列表将汇集来自1960年代至1980年代的经典流行或摇滚歌曲，非常适合用来营造怀旧氛围的晚会。
