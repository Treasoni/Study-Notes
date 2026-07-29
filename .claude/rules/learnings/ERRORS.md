# Errors

<!-- 每次追加新条目，超 100 行触发压缩 -->

## [ERR-20260729-001] beautify

**Logged**: 2026-07-29T15:40:00+08:00
**Priority**: high
**Status**: pending
**Area**: beautify

### Summary
用户报告"笔记显示有问题"时，误判为 BOM/callout 格式问题，忽略了编码乱码这个首要原因。

### Error
用户反馈：
```
笔记显示有问题
```
我首先检查了 BOM 和 callout 语法，花了一轮才意识到用户实际说的是"乱码"。

### Context
1. 用户报告 `linux/Linux网络信息获取与概念/` 目录下的笔记显示异常
2. 我通过 hex dump 发现文件有 UTF-8 BOM 和若干 callout 粘连问题，直接开始修复
3. 用户紧接着指出"主要问题是笔记是乱码啊"
4. 核实后发现正文中文字符全部损坏（mojibake），工作区源文件正常
5. 最终用工作区正确的正文内容替换了目标文件

### Root Cause
排查优先级错误：在 CJK 笔记场景中，编码问题（mojibake）比格式问题（BOM、callout）更常见且影响更严重，应作为首要排查项。

---