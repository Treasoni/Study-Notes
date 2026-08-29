## 第 3 章：Compose 挂载：volumes 长短语法与顶层声明

第 2 章的命令行挂载适合临时验证；项目一旦固定下来，配置几乎都会写进 `docker-compose.yml`。本章讲 compose 里 `volumes:` 的短语法、长语法、顶层命名卷声明，以及三个高频坑。

### 3.1 短语法：一行搞定

短语法沿用 `docker run -v` 的三段式，格式 `VOLUME:CONTAINER_PATH[:ACCESS_MODE]`：

```yaml
# docker-compose.yml
services:
  web:
    image: nginx
    volumes:
      - ./html:/usr/share/nginx/html:ro   # 相对宿主路径，必须 ./ 开头
      - app-data:/var/lib/data            # 不带路径 = 命名卷
```

`ACCESS_MODE` 是逗号分隔的选项列表：`rw`（默认）、`ro`（只读）、`z`、`Z`（SELinux）[S4]。适合一眼看懂的简单场景。

> [!tip] 大白话
> 把 `./html:/usr/share/nginx/html:ro` 想成一张「访客证」：左边是你宿主机上的工位，右边是访客能进的门，`ro` 就是「只能参观、不许动手」。宿主改文件，容器立刻看到；容器想写回去？门禁卡没这个权限。

### 3.2 长语法：把每个挂载展开成 map

要精确控制，用长语法。核心字段 `type/source/target/read_only`，再加类型专属子项 [S4]：

```yaml
services:
  web:
    image: nginx
    volumes:
      - type: bind
        source: ./html
        target: /usr/share/nginx/html
        read_only: true
        bind:
          create_host_path: false   # 宿主目录不存在时报错，不自动建
      - type: volume
        source: app-data
        target: /var/lib/data
        volume:
          nocopy: true              # 关闭空卷预填充
      - type: tmpfs
        target: /tmp/cache
        tmpfs:
          size: 10485760            # 10 MB 内存盘
```

- bind 子项：`propagation`、`create_host_path`、`selinux`（`z`/`Z` 标签）
- volume 子项：`nocopy`、`subpath`（只挂卷内子目录）
- tmpfs 子项：`size`、`mode` [S4]

### 3.3 顶层 `volumes:` 与 `external: true`

命名卷只给一个服务用时写在服务内即可；跨服务复用或复用已有卷，要在顶层声明 [S4]：

```yaml
services:
  db:
    image: postgres
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
    external: true   # 引用已存在的卷，不新建
```

### 3.4 关联字段：`user` / `read_only` / `volumes_from`

- `user: "1000:1000"`：覆盖容器进程运行用户（默认取镜像 `USER`，未设则 root）[S4]
- `read_only: true`：整个容器根文件系统只读，卷可单独开写
- `volumes_from`：继承其他服务的挂载 [S4]

这三个字段第 4 章会结合权限细讲，这里先认识它们与 `volumes` 配套。

### 3.5 三个坑

1. **相对宿主路径必须以 `./` 或 `../` 开头**，否则 compose 把 `foo` 当命名卷而非目录 [S4]
2. **短语法会自动创建不存在的宿主目录**；想严格把关用长语法 `create_host_path: false` [S4]
3. **`:z/:Z` 在 compose 中会被忽略**，要打 SELinux 标签就用长语法 `selinux:` 字段 [S1][S4]

> [!tip] 大白话
> 第 3 个坑很像「装修被叫停」：短语法里的 `:z` 像口头承诺，compose 直接当没听见；长语法 `selinux:` 字段才是白纸黑字的施工许可。

### 本章小结

- 短语法三段式适合简单场景，`ACCESS_MODE` 支持 `rw/ro/z/Z`
- 长语法用 `type/source/target/read_only` 显式声明，bind/volume/tmpfs 各有子项
- 跨服务复用或引用已有卷时用顶层 `volumes:` + `external: true`
- `user`、`read_only`、`volumes_from` 与挂载配套使用
- 相对路径不加 `./` 会被当命名卷；`create_host_path: false` 阻止自动建目录

下一章进入权限篇：为什么容器一写宿主目录就 `permission denied`，UID/GID 到底怎么对得上。
