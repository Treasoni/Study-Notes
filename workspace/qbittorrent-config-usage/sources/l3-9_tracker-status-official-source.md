---
source_id: LB-9
origin: qbittorrent/qBittorrent.git (branch: master, commit df402f91d456)
fetched_via: curl -sL https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/<path>
fetched_at: 2026-10-16
evidence_form: fetched (excerpts of upstream raw files; excerpts only, unmodified)
tier: primary
---

# LB-9 · Tracker 「状态」的官方显示串（桌面版与 WebUI）

本文件为上游原始文件的**逐字片段**（python 按行截取，未重排、未改写）。每行前缀为该行在**上游原始文件中的行号**。

用途：旧散记《qBittorrent的Tracker》给过一张状态表，但**漏了 `Tracker error` 与 `Unreachable` 两个状态**，并把 `Updating` 当成状态（源码里它是一个**标记**）。本文件给出界面实际会显示的全部字符串与其判定位置。

上游文件与规模：

- `src/base/bittorrent/trackerentrystatus.h` — 91 行
- `src/gui/trackerlist/trackerlistmodel.cpp` — 798 行
- `src/webui/www/private/scripts/prop-trackers.js` — 344 行

## 片段 1：`src/base/bittorrent/trackerentrystatus.h` 行 40-47 —— 状态枚举（这组数值就是 WebUI 的 `status`）

40:     enum class TrackerEndpointState
41:     {
42:         NotContacted = 1,
43:         Working = 2,
44:         NotWorking = 4,
45:         TrackerError = 5,
46:         Unreachable = 6
47:     };

## 片段 2：`src/gui/trackerlist/trackerlistmodel.cpp` 行 66-69 与 216-233 —— 桌面版的状态串

66:     const char STR_WORKING[] = QT_TRANSLATE_NOOP("TrackerListModel", "Working");
67:     const char STR_DISABLED[] = QT_TRANSLATE_NOOP("TrackerListModel", "Disabled");
68:     const char STR_TORRENT_DISABLED[] = QT_TRANSLATE_NOOP("TrackerListModel", "Disabled for this torrent");
69:     const char STR_PRIVATE_MSG[] = QT_TRANSLATE_NOOP("TrackerListModel", "This torrent is private");

216: QString TrackerListModel::Item::statusText() const
217: {
218:     if (isUpdating)
219:         return TrackerListModel::tr("Updating...");
220: 
221:     switch (status)
222:     {
223:     case BitTorrent::TrackerEndpointState::Working:
224:         return TrackerListModel::tr(STR_WORKING);
225:     case BitTorrent::TrackerEndpointState::NotWorking:
226:         return TrackerListModel::tr("Not working");
227:     case BitTorrent::TrackerEndpointState::TrackerError:
228:         return TrackerListModel::tr("Tracker error");
229:     case BitTorrent::TrackerEndpointState::Unreachable:
230:         return TrackerListModel::tr("Unreachable");
231:     case BitTorrent::TrackerEndpointState::NotContacted:
232:         return TrackerListModel::tr("Not contacted yet");
233:     }

## 片段 3：`src/webui/www/private/scripts/prop-trackers.js` 行 46-63 —— WebUI 的状态串与数值映射

46:     const trackerStatusText = (tracker) => {
47:         if (tracker.updating)
48:             return "QBT_TR(Updating...)QBT_TR[CONTEXT=TrackerListWidget]";
49:         switch (tracker.status) {
50:             case 0:
51:                 return "QBT_TR(Disabled)QBT_TR[CONTEXT=TrackerListWidget]";
52:             case 1:
53:                 return "QBT_TR(Not contacted yet)QBT_TR[CONTEXT=TrackerListWidget]";
54:             case 2:
55:                 return "QBT_TR(Working)QBT_TR[CONTEXT=TrackerListWidget]";
56:             case 4:
57:                 return "QBT_TR(Not working)QBT_TR[CONTEXT=TrackerListWidget]";
58:             case 5:
59:                 return "QBT_TR(Tracker error)QBT_TR[CONTEXT=TrackerListWidget]";
60:             case 6:
61:                 return "QBT_TR(Unreachable)QBT_TR[CONTEXT=TrackerListWidget]";
62:         }
63:     };

## 读法（供正文落笔时对齐口径）

- **`Updating...` 不是状态**：源码里 `isUpdating` / `tracker.updating` 是独立布尔量，为真时**先于** `switch` 返回（`trackerlistmodel.cpp:218-219`、`prop-trackers.js:47-48`），所以它只是「正在更新」的临时显示，稍等即会被真实状态顶替。
- **WebUI 的数值**：`0` 是 WebUI 侧的 `Disabled`（C++ 枚举里没有 0，枚举从 `NotContacted = 1` 起）；`1 / 2 / 4 / 5 / 6` 与枚举一一对应；**数值 3 未被使用**。
- **桌面版另有两条并非「状态」的说明串**：`Disabled for this torrent`（因这个种子被禁，`trackerlistmodel.cpp:68`）与 `This torrent is private`（私种，`trackerlistmodel.cpp:69`）。
- 本文件**不含**各状态「该怎么办」的处置建议——那属教程性建议，需另有来源或标为经验，不得由状态名反推。

