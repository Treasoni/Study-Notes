# 第 5 章：进阶——NOPASSWD 免密配置（可选）

第 4 章在 `%deploy` 规则里出现过 `NOPASSWD:` 标签，它能让特定命令免输密码。但它是 sudoers 里最容易被滥用的特性——攻破你的账号的人只要拿到一条免密命令，往往就等于拿到 root。所以本章把它单列为「可选/谨慎」小节：先讲语法与示例，再讲清安全边界，**默认不推荐**。

## 5.1 免密语法

`NOPASSWD:` 是一个**标签（tag）**，加在命令列表前，让它**后面的连续命令**都免密：

```text
user host=(runas) NOPASSWD: 命令1, 命令2
```

两种典型形态：

| 形态 | 示例 | 含义 |
|------|------|------|
| 单命令免密 | `zhq ALL=(ALL) NOPASSWD: /usr/bin/systemctl` | 仅 `systemctl` 免密，其余命令仍需密码 |
| 全免密 | `zhq ALL=(ALL) NOPASSWD: ALL` | 所有命令免密，**强烈不推荐** |

命令仍必须是**绝对路径**（沿用第 4 章规则），否则 sudo 匹配不上 [Baeldung — Guide to Linux visudo Command](https://www.baeldung.com/linux/visudo-command-tutorial)。

**孪生标签 `PASSWD:`**：标签持续生效，直到被同行的 `PASSWD:` 重新打开。混用可以做到「多数命令免密、个别高危命令仍要密码」：

```text
GROUPTWO ALL = NOPASSWD: /usr/bin/updatedb, PASSWD: /bin/kill
```

解读：`/usr/bin/updatedb` 免密；到 `/bin/kill` 时 `PASSWD:` 重新生效，执行它仍需输入密码 [DigitalOcean — How To Edit the Sudoers File](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)。改完照第 4 章的验证链走一遍：`sudo visudo -c` 应输出 `parsed OK`，再用 `sudo -l` 确认规则。

## 5.2 安全边界与建议

免密的本质是：**有人拿到你的账号后，不需要再拿到你的密码就能提权**。sudo 的密码提示本身就是「最后一次确认」的门槛，`NOPASSWD` 等于把这道门拆掉了 [Debian Wiki — sudo](https://wiki.debian.org/sudo)。

因此只该对**小范围、低风险、绝对路径**的命令开免密，例如只读的状态查询；任何「写操作」或能派生出 shell 的命令（编辑器、`python`、包管理器）都不该免密 [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)。

| 做法 | 结论 |
|------|------|
| `NOPASSWD: ALL` 全免密 | 实际等于 root，通常应避免 [Debian Wiki](https://wiki.debian.org/sudo) |
| 宽泛 `ALL=(ALL) ALL` | 用户「实际就是 root」，同理慎用 [Debian Wiki](https://wiki.debian.org/sudo) |
| 单命令免密（低风险） | 可接受，仅限自动化 / 脚本 / CI 场景 |

一句话边界：本章是**选项，不是默认推荐**。日常手动操作沿用第 3 章「入组 + 输密码」就足够；免密只在无人值守的自动化场景里才真正有价值。

## 本章小结

- `NOPASSWD:` 是标签，对其后连续命令生效；`PASSWD:` 是孪生标签，可重新打开密码门槛。
- `user ALL=(ALL) NOPASSWD: /usr/bin/systemctl` 只对单命令免密；`NOPASSWD: ALL` 全免密，强烈不推荐。
- 命令仍需绝对路径；改完用 `sudo visudo -c` 校验。
- 免密等于拆掉最后一道确认门槛，只对低风险命令开；`NOPASSWD: ALL` 与宽泛 `ALL=(ALL) ALL` 实际就是 root，通常应避免。
- 适用场景：自动化 / 脚本 / CI；手动日常操作不做默认推荐。

下一章回到最常见的故障：用户报 `user is not in the sudoers file`，第 2-4 章学的组机制与 sudoers 语法会在排错里派上用场。
