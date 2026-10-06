> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/bian-liang-de-shi-yong-shuo-ming.md).

# 变量的使用说明

当前项目基于 Mako 实现，**仅解析 `${...}` 表达式**，不支持完整 Mako 块语法。

### **零、什么是变量**

变量本质是**占位符**，在输入框编写 `${变量名}`，系统保存标签/重命名文件时，会自动替换为歌曲对应的真实信息。

### 一、基础格式

统一写法：

```
${变量名}
```

示例数据（示例歌曲信息）：

```
title = 冰雨
artist = 刘德华
album = 忘情水
tracknumber = 1
discnumber = 1
```

模板：

```
${title} - ${artist}
```

最终效果：

```
冰雨 - 刘德华
```

### 二、常用变量列表

| 变量名                      | 说明          |
| ------------------------ | ----------- |
| ${title}                 | 歌曲标题        |
| ${artist}                | 歌手          |
| ${first\_artist}         | 第一个歌手       |
| ${first\_artist\_letter} | 第一个歌手首字母    |
| ${album}                 | 专辑名称        |
| ${albumartist}           | 专辑艺术家       |
| ${discnumber}            | CD 号        |
| ${tracknumber}           | 音轨号         |
| ${filename}              | 完整文件名       |
| ${file\_song\_name}      | 不含扩展名的歌曲文件名 |
| ${parent\_path}          | 父目录路径       |
| ${parent\_parent\_path}  | 上一级父目录路径    |
| ${lyrics}                | 歌词          |
| ${comment}               | 注释          |
| ${year}                  | 发行年份        |
| ${genre}                 | 音乐流派        |
| ${composer}              | 作曲          |
| ${lyricist}              | 作词          |
| ${counter}               | 计数器         |
| ${null}                  | 空值          |

### 三、在标签中使用

可将其他字段内容赋值到指定标签，也可组合拼接。

1. 标题标签填入 `${filename}`：将**文件名**写入歌曲标题
2. 艺术家标签填入 `${albumartist}`：将**专辑艺术家**设为歌曲歌手
3. 专辑标签填入 `${year} - ${album}` 效果示例：

   ```
   1997 - 忘情水
   ```

### 四、在文件名中使用

#### 1. 基础模板

模板：

```
${tracknumber}. ${title} - ${artist}
```

输出：

```
1. 冰雨 - 刘德华.flac
```

#### 2. 音轨号补零

模板：

```
${tracknumber.zfill(2) + ". " if tracknumber else ""}${title} - ${artist}
```

输出：

```
01. 冰雨 - 刘德华.flac
```

#### 3. 兼容 CD 号 + 音轨号

模板：

```
${discnumber.zfill(2) + "_" if discnumber and tracknumber else ""}${tracknumber.zfill(2) + ". " if tracknumber else ""}${title} - ${artist}
```

不同场景效果：

* 同时有CD号、音轨号：`01_01. 冰雨 - 刘德华.flac`
* 仅有音轨号：`01. 冰雨 - 刘德华.flac`
* 两者均为空：`冰雨 - 刘德华.flac`

### 五、变量与普通文字混用

模板内可直接搭配常规文本，变量与文字自由组合。 示例1：

```
${title} - ${artist}
```

示例2：

```
CD${discnumber} - ${album}
```

效果：

```
CD1 - 忘情水
```

### 六、条件判断（空值兜底）

用于变量为空时，设置默认展示内容。

1. 标准写法

```
${title if title else "未知标题"}
```

释义：存在标题则显示标题，无标题则显示「未知标题」。

2. 简写写法

```
${title or "未知标题"}
```

## 举例子介绍

### 一、基础语法

#### 变量替换

```
${title}
${artist}
${album}
```

**示例** 模板：

```
${title} - ${artist}
```

变量数据：

```json
{
  "title": "冰雨",
  "artist": "刘德华"
}
```

输出结果：

```
冰雨 - 刘德华
```

### 二、默认值

变量为空时设置兜底内容，两种写法等价：

```
${title if title else "未知标题"}
# 简写形式
${title or "未知标题"}
```

**示例** 模板：

```
${title or "未知标题"} - ${artist or "未知歌手"}
```

输出结果：

```
未知标题 - 刘德华
```

### 三、条件拼接

适用于**有值才展示前缀/后缀**的场景。

模板：

```
${tracknumber + ". " if tracknumber else ""}${title}
```

变量数据：

```json
{
  "tracknumber": "01",
  "title": "冰雨"
}
```

输出结果：

```
01. 冰雨
```

若 `tracknumber` 为空，输出：

```
冰雨
```

### 四、数字补零

推荐使用 `zfill()` 方法实现数字补零：

```
${tracknumber.zfill(2) if tracknumber else ""}
```

**示例** 模板：

```
${tracknumber.zfill(2) + ". " if tracknumber else ""}${title}
```

变量数据：

```json
{
  "tracknumber": "1",
  "title": "冰雨"
}
```

输出结果：

```
01. 冰雨
```

### 五、文件名场景模板

#### 需求效果

* 01\_01. 冰雨 - 刘德华
* 1. 冰雨 - 刘德华
* 冰雨 - 刘德华

#### 通用模板

```
${discnumber.zfill(2) + "_" if discnumber and tracknumber else ""}${tracknumber.zfill(2) + ". " if tracknumber else ""}${title} - ${artist}
```

#### 规则说明

1. `discnumber`、`tracknumber` 均有值：展示 `01_01.`
2. 仅 `tracknumber` 有值：展示 `01.`
3. 两者都为空：直接展示 `标题 - 艺术家`

#### 效果演示

* `discnumber=1, tracknumber=1` → `01_01. 冰雨 - 刘德华`
* `discnumber=空, tracknumber=1` → `01. 冰雨 - 刘德华`
* `discnumber=空, tracknumber=空` → `冰雨 - 刘德华`

### 六、多字段兜底

优先级取值，依次向后兜底，支持叠加默认值。

基础写法：

```
${artist if artist else albumartist}
# 简写
${artist or albumartist}
```

叠加默认值：

```
${artist or albumartist or "未知歌手"}
```

### 七、字符串处理

#### 去除首尾空格

```
${title.strip() if title else ""}
```

#### 字符替换

```
${title.replace("/", "-") if title else ""}
```

#### 截取首个歌手（按 `/` 分割）

```
${artist.split("/")[0] if artist else ""}
```

#### 组合示例

```
${tracknumber.zfill(2) + ". " if tracknumber else ""}${title.strip()} - ${artist.split("/")[0]}
```

### 八、当前不支持的写法

1. **Mako 块语法（不支持）**

```
% if tracknumber:
${tracknumber}. ${title}
% else:
${title}
% endif
```

2. **foobar2000 风格语法（不支持）**

```
$if(${discnumber},$num(${discnumber},2),)
```

✅ 正确写法（Python 表达式风格）：

```
${discnumber.zfill(2) + "_" if discnumber else ""}
```

### 九、注意事项

不建议在 `${}` 内使用复杂格式化写法，正则解析会兼容异常。

❌ 不推荐：

```
${"{:02d}".format(int(tracknumber))}
```

✅ 常规推荐：

```
${str(int(tracknumber)).zfill(2) if tracknumber else ""}
```

✅ 高兼容写法（适配 `1/12` 这类特殊格式，避免 `int` 报错）：

```
${tracknumber.zfill(2) if tracknumber else ""}
```

### 十、通用推荐模板

适配 CD 号、音轨号、字段缺失等各类场景，推荐日常文件重命名使用：

```
${discnumber.zfill(2) + "_" if discnumber and tracknumber else ""}${tracknumber.zfill(2) + ". " if tracknumber else ""}${title or "未知标题"} - ${artist or albumartist or "未知歌手"}
```
