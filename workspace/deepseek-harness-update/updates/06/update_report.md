# Update Report · id 06 · DeepSeek-Harness 常见坑与速查.md

## 摘要

- **动作**：update（整篇重写，patch-in-place）
- **新标题**：DeepSeek-Harness 插件开发速查与排错
- **新职责**：Ch5 插件开发速查——坑/命令/工具契约/配置引用/模型协议/生态
- **frontmatter**：title/tags 更新；`updated: 2026-08-15`；`status: updated`

## 变更点

1. **5.1 坑清单按插件开发环节重排**：路径必须绝对、inject 未就绪、git 安装不跑 build、Windows `ctx.bash` 重复注册等前置。
2. **5.2 命令速查扩充 `dsh plugin` 全家族**（add/remove、本地目录、git#sha、tarball）与 `--dump-config` / `--dump-default-config` 排查。
3. **新增 5.3 工具契约速查**：defineTool 字段表、hook 扩展点表、长任务（ctx.jobs.start）/取消（exec.signal）/异步通知（exec.agent.inject）。
4. **新增 5.4 配置引用速查**：多层补丁树、`!!js` 运行时值、launcher 规则、HMR 与关闭行为（原热重载/关闭内容保留）。
5. V4 协议降为 5.5 模型协议参考；5.6 生态资源保留并更新下一步指向。

## 来源

- S1–S11 综合；V4 协议沿用 2026-08-13 素材。

## 未处理风险

- 原「MISSING_CREDENTIAL / UNKNOWN_MODEL / 401」三类模型报错条目在本版移除，改由 5.5 模型协议参考覆盖；如需要可补回。
- 与父级 MOC 描述行待 P5 同步。
