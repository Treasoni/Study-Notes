> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/duo-mu-lu-du-li-gua-zai-de-fang-shi.md).

# 多目录独立挂载的方式

本文档介绍如何通过多目录独立挂载的方式，将多个音乐库目录添加到容器中，实现灵活管理且避免路径冲突。这种方式适合拥有多个分散音乐文件夹的用户。

### 配置步骤

#### 1. 准备工作

* 确认你的音乐文件分散在哪些目录（例如：/path/to/pop\_music、/path/to/rock\_music 等）
* 确保这些目录对 Docker 有可读权限

#### 2. 修改 docker-compose.yml

打开你的 docker-compose.yml 文件，找到 volumes 配置部分，按以下格式添加挂载配置：\
yaml

```yaml
volumes:
  # 流行音乐库
  - /path/to/your/pop_music:/app/media/Pop
  # 摇滚音乐库
  - /path/to/your/rock_music:/app/media/Rock
  # 古典音乐库
  - /path/to/your/classical_music:/app/media/Classical
  # 可以根据需要继续添加更多音乐库
  # - /path/to/another_music:/music/AnotherCategory
```

#### 3. 配置说明

* 左侧路径（`/path/to/your/...`）：是你本地计算机上的实际音乐文件夹路径
* 右侧路径（`/app/media/...`）：是容器内的路径，按音乐类别进行分类

#### 4. 使用方法

1. 根据你的实际音乐文件夹路径修改左侧路径
2. 根据音乐类型自定义右侧的分类名称（如 Jazz、Blues 等）
3. 如需添加新的音乐库，只需按照相同格式添加新的挂载行
4. 修改完成后，使用以下命令重启容器使配置生效：bash

   ```bash
   docker-compose down
   docker-compose up -d
   ```

   <br>

### 容器内访问

在容器内部，你可以通过以下路径访问对应音乐库：<br>

* `/music/Pop`：对应本地流行音乐库
* `/music/Rock`：对应本地摇滚音乐库
* `/music/Classical`：对应本地古典音乐库

### 注意事项

1. 确保挂载路径的正确性，错误的路径会导致容器无法访问音乐文件
2. 新增或移除音乐库后，需要重启容器才能生效
3. 避免使用特殊字符作为目录名称，可能导致挂载失败
4. 如果需要修改现有音乐库的路径，直接在配置中更新对应行的左侧路径即可

<br>
