---
tags: [shell, bash, linux, 脚本, 自动化]
created: 2026-03-07
updated: 2026-03-07
---

# Shell 脚本入门教程

> [!info] 概述
> **一句话定义**：Shell 脚本是一种为 Shell 编写的脚本程序，用于自动化执行命令和任务。
>
> **通俗比喻**：Shell 脚本就像是给电脑写的"菜谱"——你把要做的事情一步步写下来，电脑就会按照你的"菜谱"自动执行，不用你每次都手动操作。

## 核心概念

### 是什么

**Shell** 是一个用 C 语言编写的程序，它是用户使用 Linux 的桥梁：
- **命令语言**：用户通过命令与系统交互
- **程序设计语言**：支持变量、条件判断、循环等编程语法

**Shell 脚本（Shell Script）** 是一种为 Shell 编写的脚本程序，把多条命令写在一个文件里，一次性执行。

### 为什么需要

| 场景 | 手动操作 | Shell 脚本 |
|------|----------|------------|
| 日常备份 | 每天手动输入命令 | 自动定时执行 |
| 批量处理 | 逐个文件操作 | 一键批量处理 |
| 系统监控 | 手动检查状态 | 自动检测并报警 |
| 环境部署 | 反复输入配置命令 | 一键部署完成 |

### 通俗理解

**🎯 比喻**：Shell 脚本就像"批处理任务清单"

```
想象你是餐厅经理：
┌─────────────────────────────────────────┐
│  每天开店前要做的事情（手动）：            │
│  1. 开灯                                 │
│  2. 开空调                               │
│  3. 检查库存                             │
│  4. 启动收银系统                         │
│  5. 打开背景音乐                         │
│                                         │
│  → 写成脚本后：运行 open_shop.sh 一键搞定 │
└─────────────────────────────────────────┘
```

**📦 示例**：第一个 Shell 脚本

```bash
#!/bin/bash
# 这是一个简单的 Shell 脚本示例

echo "Hello World!"  # 输出文字
echo "当前时间：$(date)"
echo "当前目录：$(pwd)"
```

## 技术细节

### 1. Shell 的种类

> [!info] 📚 来源
> - [Bash 简介 - 网道](https://wangdoc.com/bash/intro) - Shell 历史和种类
> - [GNU Bash 官方手册](https://www.gnu.org/s/bash/manual/bash.html) - 官方文档

常见的 Shell 类型：

| Shell | 程序名 | 说明 |
|-------|--------|------|
| **Bourne Shell** | `sh` | Unix 最初的 Shell |
| **Bourne Again Shell** | `bash` | Linux 默认 Shell，最常用 |
| **C Shell** | `csh` | 语法类似 C 语言 |
| **Korn Shell** | `ksh` | 结合了 csh 和 sh 的优点 |
| **Z Shell** | `zsh` | 功能强大，macOS Catalina 后默认 |
| **Fish** | `fish` | 用户友好，自动补全强大 |

```bash
# 查看当前使用的 Shell
echo $SHELL

# 查看系统安装的所有 Shell
cat /etc/shells

# 查看 Bash 版本
bash --version
```

### 2. 第一个脚本

**创建脚本文件**：
```bash
# 创建脚本文件
vim hello.sh
```

**脚本内容**：
```bash
#!/bin/bash
# ^^^ 这是 shebang，指定解释器

echo "Hello World!"
echo "欢迎使用 Shell 脚本"
```

**运行脚本**：

```bash
# 方法一：作为可执行程序（需要执行权限）
chmod +x hello.sh    # 添加执行权限
./hello.sh           # 执行脚本

# 方法二：作为解释器参数（不需要执行权限）
bash hello.sh
# 或
sh hello.sh

# 方法三：在当前 Shell 中执行（会影响当前环境）
source hello.sh
# 或
. hello.sh
```

> [!warning] 执行方式区别
> - `./script.sh` 或 `bash script.sh`：在**子 Shell** 中执行，不影响当前环境
> - `source script.sh`：在**当前 Shell** 中执行，会影响当前环境（如变量定义）

### 3. 变量

> [!info] 📚 来源
> - [Shell 变量 - 菜鸟教程](https://www.runoob.com/linux/linux-shell-variable.html)

```bash
#!/bin/bash

# 定义变量（等号两边不能有空格）
name="张三"
age=25

# 使用变量（加 $ 符号）
echo "姓名：$name"
echo "年龄：$age"

# 推荐使用 ${} 包裹变量
echo "姓名是：${name}，年龄是：${age}岁"

# 只读变量
readonly PI=3.14
# PI=3.14159  # 报错：只读变量不能修改

# 删除变量
unset name
echo "$name"  # 输出空行
```

**特殊变量**：

| 变量 | 含义 |
|------|------|
| `$0` | 脚本文件名 |
| `$1`~`$9` | 第 1~9 个参数 |
| `${10}` | 第 10 个及以上参数 |
| `$#` | 参数个数 |
| `$*` | 所有参数（作为整体） |
| `$@` | 所有参数（作为数组） |
| `$?` | 上个命令的退出状态（0=成功） |
| `$$` | 当前进程 ID |
| `$!` | 后台运行的最后一个进程 ID |

```bash
#!/bin/bash
# 保存为 params.sh

echo "脚本名：$0"
echo "第一个参数：$1"
echo "第二个参数：$2"
echo "参数个数：$#"
echo "所有参数：$@"

# 运行：./params.sh hello world 123
```

### 4. 字符串

```bash
#!/bin/bash

name="Shell"
# 单引号：原样输出，不能解析变量
echo 'Hello $name'  # 输出：Hello $name

# 双引号：可以解析变量和转义字符
echo "Hello $name"  # 输出：Hello Shell

# 字符串拼接
greeting="你好, "$name"!"
echo $greeting

# 获取字符串长度
str="Hello World"
echo ${#str}  # 输出：11

# 截取字符串
echo ${str:0:5}  # 输出：Hello（从索引0开始，取5个字符）

# 查找子串
echo $(expr index "$str" Wo)  # 输出子串位置
```

### 5. 数组

```bash
#!/bin/bash

# 定义数组
arr=(1 2 3 4 5)
# 或
arr=(
    "apple"
    "banana"
    "orange"
)

# 读取数组元素
echo ${arr[0]}    # 第一个元素：apple
echo ${arr[@]}    # 所有元素
echo ${arr[*]}    # 所有元素（另一种写法）

# 数组长度
echo ${#arr[@]}   # 元素个数
echo ${#arr[*]}   # 元素个数（另一种写法）

# 遍历数组
for fruit in ${arr[@]}; do
    echo "水果：$fruit"
done
```

### 6. 运算符

> [!info] 📚 来源
> - [Shell 运算符 - 菜鸟教程](https://www.runoob.com/linux/linux-shell-basic-operators.html)

**算术运算符**：
```bash
#!/bin/bash

a=10
b=20

# 使用 $(( )) 进行算术运算
echo "加法：$((a + b))"     # 30
echo "减法：$((a - b))"     # -10
echo "乘法：$((a * b))"     # 200
echo "除法：$((b / a))"     # 2
echo "取余：$((b % a))"     # 0

# 使用 expr（注意空格）
val=`expr $a + $b`
echo "a + b = $val"

# 自增
((a++))
echo "a++ = $a"  # 11
```

**比较运算符**：
```bash
#!/bin/bash

a=10
b=20

# 数字比较
if [ $a -eq $b ]; then echo "相等"; fi    # equal
if [ $a -ne $b ]; then echo "不相等"; fi   # not equal
if [ $a -gt $b ]; then echo "大于"; fi     # greater than
if [ $a -lt $b ]; then echo "小于"; fi     # less than
if [ $a -ge $b ]; then echo "大于等于"; fi # greater or equal
if [ $a -le $b ]; then echo "小于等于"; fi # less or equal

# 字符串比较
str1="hello"
str2="world"
if [ $str1 = $str2 ]; then echo "字符串相等"; fi
if [ $str1 != $str2 ]; then echo "字符串不等"; fi
if [ -z $str1 ]; then echo "字符串为空"; fi   # zero
if [ -n $str1 ]; then echo "字符串非空"; fi   # non-zero
```

**文件测试运算符**：
```bash
#!/bin/bash

file="test.sh"

if [ -e $file ]; then echo "文件存在"; fi     # exist
if [ -f $file ]; then echo "是普通文件"; fi   # file
if [ -d $file ]; then echo "是目录"; fi       # directory
if [ -r $file ]; then echo "可读"; fi         # readable
if [ -w $file ]; then echo "可写"; fi         # writable
if [ -x $file ]; then echo "可执行"; fi       # executable
if [ -s $file ]; then echo "文件不为空"; fi   # size > 0
```

### 7. 流程控制

> [!info] 📚 来源
> - [Shell 流程控制 - 菜鸟教程](https://www.runoob.com/linux/linux-shell-process-control.html)

**if 条件判断**：
```bash
#!/bin/bash

a=10
b=20

# 基本 if
if [ $a -lt $b ]; then
    echo "a 小于 b"
fi

# if-else
if [ $a -gt $b ]; then
    echo "a 大于 b"
else
    echo "a 不大于 b"
fi

# if-elif-else
score=85
if [ $score -ge 90 ]; then
    echo "优秀"
elif [ $score -ge 80 ]; then
    echo "良好"
elif [ $score -ge 60 ]; then
    echo "及格"
else
    echo "不及格"
fi

# 多条件（AND / OR）
if [ $a -gt 5 ] && [ $a -lt 15 ]; then
    echo "a 在 5 到 15 之间"
fi

if [ $a -lt 5 ] || [ $a -gt 15 ]; then
    echo "a 不在 5 到 15 之间"
fi
```

**for 循环**：
```bash
#!/bin/bash

# 遍历列表
for i in 1 2 3 4 5; do
    echo "数字：$i"
done

# 遍历范围
for i in {1..5}; do
    echo "数字：$i"
done

# C 风格 for 循环
for ((i=1; i<=5; i++)); do
    echo "计数：$i"
done

# 遍历文件
for file in *.sh; do
    echo "脚本文件：$file"
done

# 遍历命令输出
for user in $(cat /etc/passwd | cut -d: -f1); do
    echo "用户：$user"
done
```

**while 循环**：
```bash
#!/bin/bash

# 基本 while
count=1
while [ $count -le 5 ]; do
    echo "计数：$count"
    ((count++))
done

# 读取文件
while read line; do
    echo "行内容：$line"
done < "file.txt"

# 无限循环
while true; do
    echo "按 Ctrl+C 退出"
    sleep 1
done
```

**until 循环**：
```bash
#!/bin/bash
# until：条件为假时执行，直到条件为真

count=1
until [ $count -gt 5 ]; do
    echo "计数：$count"
    ((count++))
done
```

**case 分支**：
```bash
#!/bin/bash

echo "输入数字 (1-3):"
read num

case $num in
    1)
        echo "你选择了 1"
        ;;
    2)
        echo "你选择了 2"
        ;;
    3)
        echo "你选择了 3"
        ;;
    *)
        echo "无效选择"
        ;;
esac

# 匹配模式
echo "输入字符:"
read char

case $char in
    [a-z]|[A-Z])
        echo "字母"
        ;;
    [0-9])
        echo "数字"
        ;;
    *)
        echo "其他字符"
        ;;
esac
```

### 8. 函数

```bash
#!/bin/bash

# 定义函数
say_hello() {
    echo "Hello, World!"
}

# 调用函数
say_hello

# 带参数的函数
greet() {
    echo "你好, $1!"
    echo "你今年 $2 岁"
}

greet "张三" 25

# 带返回值的函数
add() {
    local sum=$(($1 + $2))
    echo $sum  # 通过 echo 返回值
}

result=$(add 10 20)
echo "结果：$result"

# 使用 return 返回状态码
check_file() {
    if [ -f $1 ]; then
        return 0  # 成功
    else
        return 1  # 失败
    fi
}

check_file "test.sh"
if [ $? -eq 0 ]; then
    echo "文件存在"
fi
```

### 9. 输入输出重定向

> [!info] 📚 来源
> - [Shell 输入/输出重定向 - 菜鸟教程](https://www.runoob.com/linux/linux-shell-io-redirections.html)

```bash
#!/bin/bash

# 输出重定向
echo "Hello" > file.txt      # 覆盖写入
echo "World" >> file.txt     # 追加写入

# 输入重定向
while read line; do
    echo $line
done < file.txt

# 错误重定向
ls 不存在的文件 2> error.log

# 同时重定向输出和错误
ls > output.log 2>&1
# 或
ls &> output.log

# 丢弃输出
ls > /dev/null 2>&1

# Here Document（多行文本）
cat << EOF
这是一段
多行文本
可以包含变量：$HOME
EOF

# Here String（单行）
grep "pattern" <<< "搜索这段文字"
```

### 10. 脚本调试

```bash
# 调试模式运行
bash -x script.sh    # 显示执行的每条命令
bash -v script.sh    # 显示读取的每行
bash -n script.sh    # 检查语法错误（不执行）

# 在脚本中启用调试
#!/bin/bash
set -x  # 开启调试
# ... 你的代码 ...
set +x  # 关闭调试

# 遇到错误立即退出
set -e  # 任何命令返回非零状态码就退出

# 使用未定义变量时报错
set -u

# 组合使用
set -euo pipefail
```

## 实用脚本示例

### 示例 1：自动备份脚本

```bash
#!/bin/bash
# backup.sh - 自动备份指定目录

# 配置
SOURCE_DIR="$HOME/projects"
BACKUP_DIR="$HOME/backups"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$BACKUP_DIR/backup.log"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 记录日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "开始备份..."

# 执行备份
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$SOURCE_DIR" 2>/dev/null

if [ $? -eq 0 ]; then
    log "备份成功：backup_$DATE.tar.gz"
    echo "备份完成！"
else
    log "备份失败！"
    echo "备份失败，请检查日志"
    exit 1
fi

# 删除 30 天前的备份
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +30 -delete
log "清理旧备份完成"
```

### 示例 2：批量重命名文件

```bash
#!/bin/bash
# rename.sh - 批量重命名文件

# 用法：./rename.sh .txt .md
# 将所有 .txt 文件改为 .md

old_ext=$1
new_ext=$2

if [ -z "$old_ext" ] || [ -z "$new_ext" ]; then
    echo "用法：$0 旧扩展名 新扩展名"
    echo "示例：$0 .txt .md"
    exit 1
fi

count=0
for file in *$old_ext; do
    if [ -f "$file" ]; then
        new_name="${file%$old_ext}$new_ext"
        mv "$file" "$new_name"
        echo "重命名：$file -> $new_name"
        ((count++))
    fi
done

echo "共重命名 $count 个文件"
```

### 示例 3：系统监控脚本

```bash
#!/bin/bash
# monitor.sh - 系统监控

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========== 系统监控 =========="
echo "时间：$(date)"
echo ""

# CPU 使用率
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
echo -e "CPU 使用率：${YELLOW}${cpu_usage}%${NC}"

# 内存使用
mem_info=$(free -h | grep Mem)
mem_used=$(echo $mem_info | awk '{print $3}')
mem_total=$(echo $mem_info | awk '{print $2}')
echo -e "内存使用：${mem_used} / ${mem_total}"

# 磁盘使用
echo ""
echo "磁盘使用："
df -h | grep -E "^/dev" | while read line; do
    usage=$(echo $line | awk '{print $5}' | tr -d '%')
    if [ $usage -gt 80 ]; then
        echo -e "${RED}$line${NC}"
    else
        echo -e "${GREEN}$line${NC}"
    fi
done

# 网络连接数
echo ""
echo "网络连接数：$(netstat -an | wc -l)"

# 运行的进程数
echo "运行进程数：$(ps aux | wc -l)"
```

### 示例 4：定时任务检查

```bash
#!/bin/bash
# cron_check.sh - 检查定时任务执行情况

TASK_NAME=$1
LOG_DIR="$HOME/logs"
ALERT_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK"

if [ -z "$TASK_NAME" ]; then
    echo "用法：$0 任务名称"
    exit 1
fi

LOG_FILE="$LOG_DIR/${TASK_NAME}_$(date +%Y%m%d).log"

if [ -f "$LOG_FILE" ]; then
    # 检查是否有错误
    if grep -q "ERROR\|FAILED\|失败" "$LOG_FILE"; then
        # 发送告警
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"🚨 任务 $TASK_NAME 执行失败！\"}" \
            "$ALERT_WEBHOOK"
        echo "发现错误，已发送告警"
    else
        echo "任务执行正常"
    fi
else
    echo "日志文件不存在：$LOG_FILE"
fi
```

## 最佳实践

### 1. 脚本头部规范

```bash
#!/bin/bash
#
# 脚本名称：script_name.sh
# 功能描述：简短描述脚本功能
# 作者：Your Name
# 创建日期：2026-03-07
# 用法：./script_name.sh [参数]
#
# 依赖：
#   - 命令1
#   - 命令2
#

set -euo pipefail  # 严格模式
IFS=$'\n\t'        # 设置字段分隔符
```

### 2. 变量命名

```bash
# 推荐：小写 + 下划线
file_name="test.txt"
user_count=100

# 常量：大写
readonly MAX_RETRY=3
readonly LOG_DIR="/var/log"

# 避免无意义的变量名
# 不推荐：x=1, temp="hello"
# 推荐：retry_count=1, temp_file="hello"
```

### 3. 错误处理

```bash
#!/bin/bash
set -euo pipefail

# 错误处理函数
error_exit() {
    echo "[ERROR] $1" >&2
    exit 1
}

# 检查命令是否存在
command -v jq >/dev/null 2>&1 || error_exit "需要安装 jq"

# 检查文件是否存在
[ -f "$1" ] || error_exit "文件不存在：$1"

# 捕获错误
trap 'error_exit "第 $LINENO 行发生错误"' ERR
```

### 4. 日志记录

```bash
#!/bin/bash

LOG_FILE="/var/log/script.log"

log() {
    local level=$1
    local message=$2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

log "INFO" "脚本开始执行"
log "WARN" "磁盘空间不足"
log "ERROR" "连接失败"
```

### 5. 参数解析

```bash
#!/bin/bash

# 简单参数
while getopts "f:o:h" opt; do
    case $opt in
        f) input_file="$OPTARG" ;;
        o) output_file="$OPTARG" ;;
        h) echo "用法：$0 -f 输入文件 -o 输出文件"; exit 0 ;;
        ?) echo "无效选项"; exit 1 ;;
    esac
done

# 检查必需参数
[ -z "$input_file" ] && { echo "请指定输入文件 -f"; exit 1; }
```

## 常见问题

**Q: `./script.sh: Permission denied` 怎么解决？**
A: 添加执行权限：`chmod +x script.sh`

**Q: 脚本在 Windows 编辑后在 Linux 运行报错？**
A: 换行符问题，转换格式：`dos2unix script.sh` 或 `sed -i 's/\r$//' script.sh`

**Q: 变量赋值时空格问题？**
A: Shell 变量赋值**等号两边不能有空格**
```bash
# 正确
name="hello"
# 错误
name = "hello"
```

**Q: 如何调试脚本？**
A: 使用 `bash -x script.sh` 或在脚本中添加 `set -x`

**Q: `command not found` 错误？**
A: 检查命令是否安装，或使用完整路径。Cron 环境变量有限，建议在脚本开头设置 PATH。

**Q: 如何让脚本在后台运行？**
A: 使用 `nohup ./script.sh > output.log 2>&1 &`

**Q: `$?` 是什么意思？**
A: 上一个命令的退出状态码，0 表示成功，非 0 表示失败

## 与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[AI学习/02-工具使用/Claude Code 定时任务自动化指南]] | Shell 脚本是 Claude Code 定时任务的执行载体 |
| [[N8N定时抓取热点资讯指南]] | N8N 可调用 Shell 脚本执行系统级任务 |
| [[linux/Ubuntu Server SSH 配置指南]] | Shell 是 SSH 远程操作的主要方式 |

## 相关文档
- [[AI学习/00-索引/MOC|AI学习索引]]

## 参考资料

### 官方资源
- [GNU Bash 官方手册](https://www.gnu.org/s/bash/manual/bash.html) - 完整官方文档
- [Bash man page](https://linux.die.net/man/1/bash) - 在线手册页

### 中文教程
- [Shell 教程 - 菜鸟教程](https://www.runoob.com/linux/linux-shell.html) - 入门教程
- [Bash 教程 - 网道](https://wangdoc.com/bash/) - 详细中文教程
- [Bash 脚本教程 - freeCodeCamp](https://www.freecodecamp.org/chinese/news/bash-scripting-tutorial-linux-shell-script-and-command-line-for-beginners/) - 初学者教程

### 进阶资源
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/) - 高级脚本指南
- [ShellCheck](https://www.shellcheck.net/) - Shell 脚本静态分析工具
- [GitHub - Shell 脚本教程](https://github.com/jaywcjlove/shell-tutorial) - 开源教程

### 实用工具
- [explainshell.com](https://explainshell.com/) - 命令解释工具
- [ShellCheck 在线](https://www.shellcheck.net/) - 脚本检查工具
