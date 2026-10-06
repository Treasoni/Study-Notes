# 落盘校验报告

基线提交：`6520105c`（vault 自动备份在我落盘前的最后一次快照）

## A. 回滚点是否等于改动前状态
  ✅ 11 个文件的 pristine 均等于基线提交（逐字符，行尾归一后）

## B. 行尾保留
  ✅ 01_为什么感觉都一样是范畴错误.md                    CRLF
  ✅ 02_多用户一词三义.md                          CRLF
  ✅ 03_隔离强度梯度.md                           CRLF
  ✅ 04_同层内部怎么分.md                          CRLF
  ✅ 05_Octop回答的是不是另一个问题.md                 LF
  ✅ 06_谁把谁当参照.md                           LF
  ✅ 07_选型框架与决策树.md                         CRLF
  ✅ _merged.md                             CRLF
  ✅ final_note.md                          CRLF
  ✅ 自托管 Agent 平台选型.md                      LF
  ✅ 03_outline.md                          CRLF

## C. 附录表结构（每章行数 / 每行管道数 / 原文列是否带反引号）
  ✅ 01_为什么感觉都一样是范畴错误.md                    附录 [28] 行，管道数全部为 5
  ✅ 02_多用户一词三义.md                          附录 [24] 行，管道数全部为 5
  ✅ 03_隔离强度梯度.md                           附录 [13] 行，管道数全部为 5
  ✅ 04_同层内部怎么分.md                          附录 [15] 行，管道数全部为 5
  ✅ 05_Octop回答的是不是另一个问题.md                 附录 [17] 行，管道数全部为 5
  ✅ 06_谁把谁当参照.md                           附录 [26] 行，管道数全部为 5
  ✅ 07_选型框架与决策树.md                         附录 [5] 行，管道数全部为 5
  ✅ _merged.md                             附录 [28, 24, 13, 15, 17, 26, 5] 行，管道数全部为 5
  ✅ final_note.md                          附录 [28, 24, 13, 15, 17, 26, 5] 行，管道数全部为 5
  ✅ 自托管 Agent 平台选型.md                      附录 [28, 24, 13, 15, 17, 26, 5] 行，管道数全部为 5

## D. 第 4 章标题翻译
  ✅ 01_为什么感觉都一样是范畴错误.md                    旧 0 / 新 0
  ✅ 02_多用户一词三义.md                          旧 0 / 新 0
  ✅ 03_隔离强度梯度.md                           旧 0 / 新 0
  ✅ 04_同层内部怎么分.md                          旧 0 / 新 1
  ✅ 05_Octop回答的是不是另一个问题.md                 旧 0 / 新 0
  ✅ 06_谁把谁当参照.md                           旧 0 / 新 0
  ✅ 07_选型框架与决策树.md                         旧 0 / 新 0
  ✅ _merged.md                             旧 0 / 新 1
  ✅ final_note.md                          旧 0 / 新 2
  ✅ 自托管 Agent 平台选型.md                      旧 0 / 新 2
  ✅ 03_outline.md                          旧 0 / 新 1

## E. 正文残留的英文（≥2 个 ASCII 词的串，排除 wikilink 与表格原文列）
  01_为什么感觉都一样是范畴错误.md：4 处，去重 4 种
      · ACP runner
      · Claude Code
      · Codex CLI
      · OpenHands issue
  02_多用户一词三义.md：1 处，去重 1 种
      · agent ID
  03_隔离强度梯度.md：1 处，去重 1 种
      · agent X
  04_同层内部怎么分.md：0 处，去重 0 种
  05_Octop回答的是不是另一个问题.md：0 处，去重 0 种
  06_谁把谁当参照.md：3 处，去重 1 种
      · ACP runner
  07_选型框架与决策树.md：1 处，去重 1 种
      · ACP runner
  _merged.md：4 处，去重 4 种
      · ACP runner
      · Claude Code
      · Codex CLI
      · OpenHands issue
  final_note.md：5 处，去重 5 种
      · ACP runner
      · AI Agent
      · Claude Code
      · Codex CLI
      · OpenHands issue
  自托管 Agent 平台选型.md：5 处，去重 5 种
      · ACP runner
      · AI Agent
      · Claude Code
      · Codex CLI
      · OpenHands issue

## F. 每章 4 份副本的附录表逐字一致
  ✅ ch1 28 行，4 份副本逐字相同
  ✅ ch2 24 行，4 份副本逐字相同
  ✅ ch3 13 行，4 份副本逐字相同
  ✅ ch4 15 行，4 份副本逐字相同
  ✅ ch5 17 行，4 份副本逐字相同
  ✅ ch6 26 行，4 份副本逐字相同
  ✅ ch7 5 行，4 份副本逐字相同

## G. 组装本的「关于引文」callout
  ✅ final_note.md                          callout 1 次
  ✅ 自托管 Agent 平台选型.md                      callout 1 次

## H. 夹在两个汉字之间的空格（英译中留下的空隙）
  ✅ 除「第 N 章/层 」这种刻意的标签空格外，没有其它汉字间空格

---

## 总判定

**✅ 全部通过**
