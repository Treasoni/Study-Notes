---
source_id: LB-7
origin: qbittorrent/qBittorrent.git (branch: master, commit df402f91d456)
fetched_via: curl -sL https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/<path>
fetched_at: 2026-10-16
evidence_form: fetched (excerpts of upstream raw files; excerpts only, unmodified)
tier: primary
---

# LB-7 · 代理（Proxy Server）字段与配置键（官方源码取证）

本文件为上游原始文件的**逐字片段**（用 python 直接按行截取，未重排、未改写）。每行前缀为该行在**上游原始文件中的行号**。

背景：官方选项说明页（`sources/l2-1_options-explained.md:105` 的 `### Proxy server`）只给一句说明句、**不列任何字段**，因此代理字段一律以源码为准。

上游文件与规模：

- `src/gui/optionsdialog.ui` — 4454 行
- `src/base/net/proxytype.h` — 48 行
- `src/base/net/proxyconfigurationmanager.cpp` — 106 行
- `src/base/preferences.cpp` — 2222 行

## 片段 1：`src/gui/optionsdialog.ui` 行 2159-2345 —— `Options → Connection → Proxy Server` 的界面字段

2159:              <widget class="QGroupBox" name="groupProxy">
2160:               <property name="enabled">
2161:                <bool>true</bool>
2162:               </property>
2163:               <property name="title">
2164:                <string>Proxy Server</string>
2165:               </property>

2172:                     <string>Type:</string>
2173:                    </property>
2174:                   </widget>
2175:                  </item>
2176:                  <item>
2177:                   <widget class="QComboBox" name="comboProxyType"/>
2178:                  </item>

2182:                     <string>Host:</string>
2183:                    </property>
2184:                   </widget>
2185:                  </item>
2186:                  <item>
2187:                   <widget class="QLineEdit" name="textProxyIP"/>
2188:                  </item>

2192:                     <string>Port:</string>
2193:                    </property>
2194:                   </widget>
2195:                  </item>
2196:                  <item>
2197:                   <widget class="QSpinBox" name="spinProxyPort">
2198:                    <property name="minimum">

2232:                   <string>Some functions are unavailable with the chosen proxy type!</string>
2233:                  </property>

2237:                 <widget class="QCheckBox" name="checkProxyHostnameLookup">
2238:                  <property name="toolTip">
2239:                   <string>If checked, hostname lookups are done via the proxy</string>
2240:                  </property>
2241:                  <property name="text">
2242:                   <string>Perform hostname lookup via proxy</string>
2243:                  </property>

2247:                 <widget class="QGroupBox" name="checkProxyAuth">
2248:                  <property name="enabled">

2271:                      <widget class="QLineEdit" name="textProxyUsername"/>
2272:                     </item>

2281:                      <widget class="QLineEdit" name="textProxyPassword">
2282:                       <property name="echoMode">

2300:                 <widget class="QGroupBox" name="checkProxyBitTorrent">
2301:                  <property name="title">
2302:                   <string>Use proxy for BitTorrent purposes</string>
2303:                  </property>

2312:                    <widget class="QCheckBox" name="checkProxyPeerConnections">
2313:                     <property name="toolTip">
2314:                      <string>Otherwise, the proxy server is only used for tracker connections</string>
2315:                     </property>
2316:                     <property name="text">
2317:                      <string>Use proxy for peer connections</string>
2318:                     </property>

2325:                 <widget class="QCheckBox" name="checkProxyRSS">
2326:                  <property name="toolTip">
2327:                   <string>RSS feeds will use proxy</string>
2328:                  </property>
2329:                  <property name="text">
2330:                   <string>Use proxy for RSS purposes</string>
2331:                  </property>

2338:                 <widget class="QCheckBox" name="checkProxyMisc">
2339:                  <property name="toolTip">
2340:                   <string>Search engine, software updates or anything else will use proxy</string>
2341:                  </property>
2342:                  <property name="text">
2343:                   <string>Use proxy for general purposes</string>
2344:                  </property>


## 片段 2：`src/base/net/proxytype.h` 行 39-45 —— 代理「类型」下拉的全部取值

39:         enum class ProxyType
40:         {
41:             None = 0,
42:             HTTP = 1,
43:             SOCKS5 = 2,
44:             SOCKS4 = 5
45:         };


## 片段 3：`src/base/net/proxyconfigurationmanager.cpp` 行 31, 50-56, 58-66 —— 配置键与默认值

31: #define SETTINGS_KEY(name) (u"Network/Proxy/" name)

50:     , m_storeProxyType {SETTINGS_KEY(u"Type"_s)}
51:     , m_storeProxyIP {SETTINGS_KEY(u"IP"_s)}
52:     , m_storeProxyPort {SETTINGS_KEY(u"Port"_s)}
53:     , m_storeProxyAuthEnabled {SETTINGS_KEY(u"AuthEnabled"_s)}
54:     , m_storeProxyUsername {SETTINGS_KEY(u"Username"_s)}
55:     , m_storeProxyPassword {SETTINGS_KEY(u"Password"_s)}
56:     , m_storeProxyHostnameLookupEnabled {SETTINGS_KEY(u"HostnameLookupEnabled"_s)}

58:     m_config.type = m_storeProxyType.get(ProxyType::None);
59:     if ((m_config.type < ProxyType::None) || (m_config.type > ProxyType::SOCKS4))
60:         m_config.type = ProxyType::None;
61:     m_config.ip = m_storeProxyIP.get((m_config.type == ProxyType::None) ? u""_s : u"0.0.0.0"_s);
62:     m_config.port = m_storeProxyPort.get(8080);
63:     m_config.authEnabled = m_storeProxyAuthEnabled;
64:     m_config.username = m_storeProxyUsername;
65:     m_config.password = m_storeProxyPassword;
66:     m_config.hostnameLookupEnabled = m_storeProxyHostnameLookupEnabled.get(true);


## 片段 4：`src/base/preferences.cpp` 行 2082-2118 —— 三个「用途」开关的配置键（BitTorrent / RSS / Misc）

2082: bool Preferences::useProxyForBT() const
2083: {
2084:     return value<bool>(u"Network/Proxy/Profiles/BitTorrent"_s);
2085: }

2087: void Preferences::setUseProxyForBT(const bool value)
2088: {
2089:     if (value == useProxyForBT())
2090:         return;
2091: 
2092:     setValue(u"Network/Proxy/Profiles/BitTorrent"_s, value);
2093: }

2095: bool Preferences::useProxyForRSS() const
2096: {
2097:     return value<bool>(u"Network/Proxy/Profiles/RSS"_s);
2098: }

2108: bool Preferences::useProxyForGeneralPurposes() const
2109: {
2110:     return value<bool>(u"Network/Proxy/Profiles/Misc"_s);
2111: }


## 片段 5（附）：`src/base/preferences.cpp` 行 1127-1137 —— WebUI 反向代理支持开关（供后续「远程访问」章节使用）

1127: bool Preferences::isWebUIReverseProxySupportEnabled() const
1128: {
1129:     return value(u"WebUI/ReverseProxySupportEnabled"_s, false);
1130: }
1131: 
1132: void Preferences::setWebUIReverseProxySupportEnabled(const bool enabled)
1133: {
1134:     if (enabled == isWebUIReverseProxySupportEnabled())
1135:         return;
1136: 
1137:     setValue(u"WebUI/ReverseProxySupportEnabled"_s, enabled);

