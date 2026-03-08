#!/bin/bash
# AI 新闻收集 Launchd 任务安装脚本

set -e

# 配置路径
PLIST_SOURCE="$(pwd)/com.user.ai-news-daily.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.user.ai-news-daily.plist"
LOG_DIR="/Users/zhqznc/Documents/新闻/logs"
LABEL="com.user.ai-news-daily"

echo "=== AI 新闻收集 Launchd 任务安装 ==="
echo

# 1. 创建日志目录
echo "1. 创建日志目录..."
mkdir -p "$LOG_DIR"
echo "   ✓ 日志目录: $LOG_DIR"
echo

# 2. 复制 plist 文件
echo "2. 复制 plist 配置文件..."
cp "$PLIST_SOURCE" "$PLIST_DEST"
echo "   ✓ 已复制到: $PLIST_DEST"
echo

# 3. 设置文件权限
echo "3. 设置文件权限..."
chmod 644 "$PLIST_DEST"
echo "   ✓ 权限已设置为 644"
echo

# 4. 验证 plist 语法
echo "4. 验证 plist 语法..."
if plutil -lint "$PLIST_DEST" | grep -q "OK"; then
    echo "   ✓ plist 语法验证通过"
else
    echo "   ✗ plist 语法有误，请检查"
    exit 1
fi
echo

# 5. 检查是否已加载旧版本
if launchctl list | grep -q "$LABEL"; then
    echo "5. 检测到旧版本任务，正在卸载..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
    echo "   ✓ 旧版本已卸载"
else
    echo "5. 未检测到旧版本任务"
fi
echo

# 6. 加载任务
echo "6. 加载 Launchd 任务..."
launchctl load "$PLIST_DEST"
echo "   ✓ 任务已加载"
echo

# 7. 验证任务已加载
echo "7. 验证任务状态..."
if launchctl list | grep -q "$LABEL"; then
    echo "   ✓ 任务已成功加载"
    echo
    echo "=== 安装完成！==="
    echo
    echo "任务信息："
    echo "  Label: $LABEL"
    echo "  执行时间: 每天早上 9:00"
    echo "  执行命令: cd /Users/zhqznc/Documents/新闻 && claude --dangerously-skip-permissions -p \"收集今天的AI新闻总结成文档\""
    echo
    echo "日志位置："
    echo "  标准输出: $LOG_DIR/ai-news-stdout.log"
    echo "  错误日志: $LOG_DIR/ai-news-error.log"
    echo
    echo "常用命令："
    echo "  立即测试执行: launchctl start $LABEL"
    echo "  查看任务状态: launchctl list | grep $LABEL"
    echo "  卸载任务:     launchctl unload $PLIST_DEST"
    echo "  查看输出日志: cat $LOG_DIR/ai-news-stdout.log"
    echo "  查看错误日志: cat $LOG_DIR/ai-news-error.log"
    echo
    read -p "是否立即测试执行？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在执行测试..."
        launchctl start "$LABEL"
        echo "已触发测试，请稍等片刻后查看日志："
        echo "  tail -f $LOG_DIR/ai-news-stdout.log"
    fi
else
    echo "   ✗ 任务加载失败"
    exit 1
fi
