# 上下文与派发纪律

目标是少读、批派、前缀稳定。配套规则：`common/prompt-cache.md`（前缀顺序与稳定性）、`research-tools.md`（抓取工具选择）。

## 读文件

1. 单文件超过 ~15 KB 时不要整文件 Read：先读有界摘要，再按需定点读。
   - 摘要：`python .claude/scripts/note-digest.py <file>`
   - 定点读：`Read` 的 `offset` / `limit`，或先用 `Grep` 定位小节
2. 需要连续读多份同类文件时，先合并成一份再读一次：`python .claude/scripts/merge_files.py --input-dir <dir>`（默认产出 `<dir>/_merged.md`）。
3. 不要把整页正文、整份素材复制进下游提示词；给路径、锚点、来源 ID。

## 派发子代理

1. **批派，不单元派**：写作每批 ≤3 章；资料收集每阶段 2–3 个批量子代理，一个代理负责一组来源或透镜。
2. 同类子代理并发 ≤4；能续写就不新开——同一子代理连续处理后续单元，优于开新兄弟代理重读同一份材料。
3. 派发提示只放：固定职责、输出格式、来源纪律 + 末尾参数块（任务、路径、检索位置）；不内联大段正文。
4. 要求子代理只回结论、摘要、引用和来源 ID，不回贴原文。
5. 确定性拼接、统计、格式归一交给脚本或父流程，不派推理代理做搬运。

## 维护

本文件与 `scripts/note-digest.py`、`scripts/merge_files.py` 同批生效；变更后按 `common/sync-workflow.md` 走 `.agent-sync` 同步与校验，不要在生成目录手改。
