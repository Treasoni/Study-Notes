# 更新报告：04_HACS安装_Docker三种路径与国内加速.md

- 更新日期：2026-08-08
- 更新模式：patch-in-place
- 处理范围：仅 4.4 节 + 追加更新记录；4.1 / 4.2 / 4.3 / 小结 未过时，未改动

## 变更摘要

1. **4.4 第 1 条（gh-proxy 前缀代理）**
   - 移除已失效的 `mirror.ghproxy.com`、`ghfast.top`（2026-08-08 实测拒连）
   - 实测可用名单更新为 `gh-proxy.com` / `ghproxy.net`，示例命令保留 `gh-proxy.com`
2. **4.4 第 2 条（hacs-china 极速版）**
   - `get.hacs.vip` 从「可用性待实测」改为「已于 2026-08-08 失效（443 拒连），勿再使用」
   - 补充 Gitee 手动安装兜底路径 `gitee.com/hacs-china`（实测存活）
3. **4.4 第 3 条（GitHub API 代理）**
   - 移除已失效的 `ghapi.hacs.vip/api`（与 get.hacs.vip 同一基础设施）
   - 保留 `ghapi-cf.hacs.vip/api`、`hacs-china.chrome7.com/api`（服务器仍响应，完整路径需按需验证）
4. **文末**：追加 `## 更新记录` 表
5. **frontmatter**：`updated` 保持 2026-08-08（当天创建当天更新，无需改动）

## 未处理风险

- **API 代理端点未完整验证**：`ghapi-cf.hacs.vip/api`、`hacs-china.chrome7.com/api` 仅验证到服务器层响应（裸路径 404 属正常，代理前缀只在 `/api/...` 子路径生效），完整功能需在 HACS「选项」里填真实集成列表测试。
- **代理域名时效性**：gh-proxy 类免费服务随时可能失效，本报告结论截至 2026-08-08，实操前仍应按 4.4 警告先实测。
- **GitHub 首次授权无法加速**：本次更新未改变该约束。

## 来源

- [hacs-china（GitHub）](https://github.com/hacs-china/)
- [hacs-china（Gitee 镜像）](https://gitee.com/hacs-china)
- [HACS 极速版！ - 瀚思彼岸论坛](https://bbs.hassbian.com/forum.php?mod=viewthread&tid=15505)
- [Home Assistant 的 HACS 下载加速思路 | 极客日志](https://zeeklog.com/home-assistant-de-hacs-xia-zai-jia-su-si-lu)
- 当日实测：curl 探测各代理域名 HTTP 状态
