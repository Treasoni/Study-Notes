# sources/web 取证清单（第 3 章专用）

官方**没有** Web UI 操作文档，第 3 章的功能面只能读前端源码。以下文件全部经 jsDelivr 缓存到本目录，**缓存下来的才算证据**。

基线：`https://cdn.jsdelivr.net/gh/slskd/slskd@master/`（`@master`，对应版本锚点 0.26.0 之后的 master 快照；与 0.26.0 的差异未逐行核对）。

| 本地文件 | 来源 URL（`https://cdn.jsdelivr.net/gh/slskd/slskd@master/` 之后） | 支撑小节 |
| --- | --- | --- |
| `components_App.jsx` | `src/web/src/components/App.jsx` | 3.3（导航项、Agent 模式、主题、Pending Action、New Version 弹窗） |
| `components_Search_Searches.jsx` | `src/web/src/components/Search/Searches.jsx` | 3.1（搜索入口、输入框 placeholder） |
| `components_Search_List_SearchList.jsx` | `src/web/src/components/Search/List/SearchList.jsx` | 3.1（搜索列表列名与排序） |
| `components_Search_List_SearchListRow.jsx` | `src/web/src/components/Search/List/SearchListRow.jsx` | 3.1（单行单元格：Locked/Ended） |
| `components_Search_List_SearchActionIcon.jsx` | `src/web/src/components/Search/List/SearchActionIcon.jsx` | 3.1（列表操作图标） |
| `components_Search_SearchStatusIcon.jsx` | `src/web/src/components/Search/SearchStatusIcon.jsx` | 3.1（搜索状态取值与图标语义） |
| `components_Search_Detail_SearchDetail.jsx` | `src/web/src/components/Search/Detail/SearchDetail.jsx` | 3.1（排序两项、三个开关默认值、筛选输入框、分页 +5） |
| `components_Search_Detail_SearchDetailHeader.jsx` | `src/web/src/components/Search/Detail/SearchDetailHeader.jsx` | 3.1（Search Again / Stop / Delete 按钮） |
| `components_Search_Response.jsx` | `src/web/src/components/Search/Response.jsx` | 3.1（结果卡片头部/元信息/目录补全入口）、3.2（下载按钮三态） |
| `components_Shared_FileList.jsx` | `src/web/src/components/Shared/FileList.jsx` | 3.1（结果文件表列名、锁定图标） |
| `lib_searches.js` | `src/web/src/lib/searches.js` | 3.1（**筛选语法与语义的唯一真源**） |
| `components_Transfers_Transfers.jsx` | `src/web/src/components/Transfers/Transfers.jsx` | 3.2（按 direction 复用同一视图） |
| `components_Transfers_TransfersHeader.jsx` | `src/web/src/components/Transfers/TransfersHeader.jsx` | 3.2（批量操作分组与状态过滤清单） |
| `components_Transfers_TransferList.jsx` | `src/web/src/components/Transfers/TransferList.jsx` | 3.2（传输表列、单文件重试/插队、状态文案） |
| `components_Transfers_TransferGroup.jsx` | `src/web/src/components/Transfers/TransferGroup.jsx` | 3.2（按用户/目录分组） |
| `lib_transfers.js` | `src/web/src/lib/transfers.js` | 3.2（重试/取消/清除的状态判定） |
| `components_Dashboard_Dashboard.jsx` | `src/web/src/components/Dashboard/Dashboard.jsx` | 3.3（历史区间 24h/7d/30d/90d/180d/1y/All、数据块） |
| `components_Browse_Browse.jsx` | `src/web/src/components/Browse/Browse.jsx` | 3.3（目录树、IndexedDB `slskd-browse`、分隔符、500ms 轮询） |
| `components_Users_Users.jsx` | `src/web/src/components/Users/Users.jsx` | 3.3（用户名查询、localStorage 记忆） |
| `components_Rooms_Rooms.jsx` | `src/web/src/components/Rooms/Rooms.jsx` | 3.3（房间列表/加入） |
| `components_Chat_Chat.jsx` | `src/web/src/components/Chat/Chat.jsx` | 3.3（会话列表、5 秒轮询、acknowledge） |
| `components_System_System.jsx` | `src/web/src/components/System/System.jsx` | 3.3（七个页签与路由名） |
| `components_System_Info_index.jsx` | `src/web/src/components/System/Info/index.jsx` | 3.3（Info 页：Check for Updates / Get Privileges / Restart / Shut Down） |
| `components_System_Options_index.jsx` | `src/web/src/components/System/Options/index.jsx` | 3.3、3.4（Options 只读；`remote_configuration` 才解锁 Edit/Debug View） |
| `components_System_Shares_index.jsx` | `src/web/src/components/System/Shares/index.jsx` | 3.3、3.9（Rescan Shares / Cancel Scan / 排除表） |
| `components_System_Files_index.jsx` | `src/web/src/components/System/Files/index.jsx` | 3.3（Files 页两个子页签 Download/Incomplete） |
| `components_System_Data_index.jsx` | `src/web/src/components/System/Data/index.jsx` | 3.3、3.2（Clear All Completed Uploads/Downloads） |
| `components_System_Events_index.jsx` | `src/web/src/components/System/Events/index.jsx` | 3.3（事件表 Id/Timestamp/Type/Data + 分页） |
| `components_System_Logs_index.jsx` | `src/web/src/components/System/Logs/index.jsx` | 3.3（日志表 Timestamp/Level/Message） |
| `lib_util.js` | `src/web/src/lib/util.js` | 3.1（`formatAttributes` 渲染规则） |
| `lib_options.js` | `src/web/src/lib/options.js` | 3.4（`/options/yaml*` 端点） |
| `lib_server.js` | `src/web/src/lib/server.js` | 3.3（连接/断开） |
| `lib_users.js` | `src/web/src/lib/users.js` | 3.2、3.3（取目录内容） |
| `lib_files.js` | `src/web/src/lib/files.js` | 3.3（Files 页 API） |
| `config.js` | `src/web/src/config.js` | 3.3、3.4（localStorage key、API 基址） |
| `Blacklist.cs` | `src/slskd/Core/Blacklist.cs` | 3.9（格式枚举与 `#`/空行跳过） |
| `blacklist_cidr.txt` | `tests/slskd.Tests.Unit/Data/Blacklist/cidr.txt` | 3.9（**CIDR 清单文件的真实格式**，EX-17） |
| `blacklist_p2p.txt` | `tests/slskd.Tests.Unit/Data/Blacklist/p2p.txt` | 3.9（P2P 格式对照） |
| `blacklist_dat.txt` | `tests/slskd.Tests.Unit/Data/Blacklist/dat.txt` | 3.9（DAT 格式对照） |

## 未取到 / 降级处理

| 缺什么 | 影响的小节 | 正文里的降级标注 |
| --- | --- | --- |
| 官方 Web UI 操作文档（不存在） | 3.0–3.3 | §3.0 显式声明「官方无操作文档」+ 取证层级 |
| 热重载 / 待重启日志的**实际输出文本** | 3.4（EX-37） | EX-37 标「日志原文未取证，仅据源码语义与 Web UI 的 'Pending Action' 提示推写，待实测核对」 |
| `data.jsdelivr.com` 目录清单（仅用于列文件，未随章节长期保存） | — | 不作为正文证据，只作抓取路径依据 |
| 「页面内 JS 交互的真实手感」（折行、虚拟滚动等渲染细节） | 3.1、3.2 | 涉及交互手感处标「源码可读，实际效果需自测」 |
