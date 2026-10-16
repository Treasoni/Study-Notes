---
source_id: LB-10
origin: qbittorrent/qBittorrent.git (branch: master, commit df402f91d456)
fetched_via: curl -sL https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/<path>
fetched_at: 2026-10-16
evidence_form: fetched (excerpts of upstream raw files; excerpts only, unmodified)
tier: primary
---

# LB-10 · WebUI「对外访问与安全」的界面字段、配置键与默认值（官方源码取证）

本文件为上游原始文件的**逐字片段**（python 按行截取，只保留含 `<string>` / `name="` / `return value` 的行，并保证多行 `<string>` 完整；未重排、未改写）。每行前缀为该行在**上游原始文件中的行号**。

背景：三册正文此前只在**上册 §2.6 的动手实践**里、以**社区经验（LA-4）**的身份提到过 `WebUI\HostHeaderValidation` 与 `WebUI\CSRFProtection`——只说了「关掉它们可以绕开强制 https」，**没给默认值与语义**。本文件把这组字段升格为可核对的官方口径。

上游文件与规模：

- `src/gui/optionsdialog.ui` — 4454 行（WebUI 页 `tabWebUIPage` 自 3712 行起）
- `src/base/preferences.cpp` — 2222 行（WebUI 配置键的取值与工厂默认值）

## 片段 1：`src/gui/optionsdialog.ui` —— `Options → WebUI` 页的字段与开关串

### 1a. 总开关、绑定地址 / 端口 / UPnP（行 3742-3808）

3742:              <widget class="QGroupBox" name="checkWebUI">
3743:               <property name="title">
3744:                <string>Web User Interface (Remote control)</string>
3746:               <property name="checkable">

3768:                   <widget class="QLabel" name="lblWebUIAddress">
3769:                    <property name="text">
3770:                     <string>IP address:</string>
3775:                   <widget class="QLineEdit" name="textWebUIAddress">
3776:                    <property name="toolTip">
3777:                     <string>IP address that the Web UI will bind to.
3778: Specify an IPv4 or IPv6 address. You can specify &quot;0.0.0.0&quot; for any IPv4 address,
3779: &quot;::&quot; for any IPv6 address, or &quot;*&quot; for both IPv4 and IPv6.</string>
3784:                   <widget class="QLabel" name="lblWebUIPort">
3785:                    <property name="text">
3786:                     <string>Port:</string>
3791:                   <widget class="QSpinBox" name="spinWebUIPort">
3792:                    <property name="minimum">
3795:                    <property name="maximum">
3798:                    <property name="value">
3806:                 <widget class="QCheckBox" name="checkWebUIUPnP">
3807:                  <property name="text">
3808:                   <string>Use UPnP / NAT-PMP to forward the port from my router</string>

### 1b. HTTPS 与认证（行 3816-3894）

3816:                 <widget class="QGroupBox" name="checkWebUIHttps">
3817:                  <property name="title">
3818:                   <string>&amp;Use HTTPS instead of HTTP</string>
3820:                  <property name="checkable">
3823:                  <property name="checked">
3826:                  <layout class="QGridLayout" name="gridLayout_11">
3828:                    <widget class="QLabel" name="lblSslCertStatus"/>
3831:                    <widget class="QLabel" name="lblWebUICrt">
3832:                     <property name="text">
3833:                      <string>Certificate:</string>
3838:                    <widget class="FileSystemPathLineEdit" name="textWebUIHttpsCert" native="true"/>
3841:                    <widget class="QLabel" name="lblSslKeyStatus"/>
3844:                    <widget class="QLabel" name="lblWebUIKey">
3845:                     <property name="text">
3846:                      <string>Key:</string>

3882:                       <widget class="QLabel" name="lblWebUIUsername">
3883:                        <property name="text">
3884:                         <string>Username:</string>
3889:                       <widget class="QLineEdit" name="textWebUIUsername"/>
3892:                       <widget class="QLabel" name="lblWebUIPassword">
3893:                        <property name="text">
3894:                         <string>Password:</string>

### 1c. 三个防护开关 + Host 头校验（行 4184-4229）

4184:                    <widget class="QCheckBox" name="checkClickjacking">
4185:                     <property name="text">
4186:                      <string>Enable clickjacking protection</string>
4191:                    <widget class="QCheckBox" name="checkCSRFProtection">
4192:                     <property name="text">
4193:                      <string>Enable Cross-Site Request Forgery (CSRF) protection</string>
4198:                    <widget class="QCheckBox" name="checkSecureCookie">
4199:                     <property name="text">
4200:                      <string>Enable cookie Secure flag (requires HTTPS or localhost connection)</string>
4205:                    <widget class="QGroupBox" name="groupHostHeaderValidation">
4206:                     <property name="title">
4207:                      <string>Enable Host header validation</string>

4223:                         <widget class="QLineEdit" name="textServerDomains">
4224:                          <property name="toolTip">
4225:                           <string>Whitelist for filtering HTTP Host header values.
4226: In order to defend against DNS rebinding attack,
4227: you should put in domain names used by WebUI server.
4228: 
4229: Use ';' to split multiple entries. Can use wildcard '*'.</string>

### 1d. 反向代理支持（行 4267-4287）

4267:                 <widget class="QGroupBox" name="groupEnableReverseProxySupport">
4268:                  <property name="title">
4269:                   <string>Enable reverse proxy support</string>
4271:                  <property name="checkable">

4278:                      <widget class="QLabel" name="lblReverseProxiesList">
4279:                       <property name="text">
4280:                        <string>Trusted proxies list:</string>
4285:                      <widget class="QLineEdit" name="textTrustedReverseProxiesList">
4286:                       <property name="toolTip">
4287:                        <string>Specify reverse proxy IPs (or subnets, e.g. 0.0.0.0/24) in order to use forwarded client address (X-Forwarded-For header). Use ';' to split multiple entries.</string>

## 片段 2：`src/base/preferences.cpp` —— WebUI 配置键的工厂默认值

只取**声明默认值的 getter 行**（`return value(u"WebUI/…", <默认>)`）。默认值即该调用的第二参数；下表汇总，逐字片段见 2a。

| 配置键 | 源码行 | 工厂默认值 |
| --- | --- | --- |
| `WebUI/Enabled` | 776 | 由构建传入（未见固定常量，**不猜**） |
| `WebUI/LocalHostAuth` | 789 | `true` |
| `WebUI/AuthSubnetWhitelistEnabled` | 802 | `false` |
| `WebUI/ServerDomains` | 842 | `*` |
| `WebUI/Address` | 855 | `*` |
| `WebUI/Port` | 868 | `8080` |
| `WebUI/UseUPnP` | 882 | `false` |
| `WebUI/Username` | 895 | `admin` |
| `WebUI/Password_PBKDF2` | 908 | 无默认（空值，待首次设置） |
| `WebUI/MaxAuthenticationFailCount` | 934 | `5` |
| `WebUI/BanDuration` | 947 | `3600`（秒） |
| `WebUI/SessionTimeout` | 960 | `3600` |
| `WebUI/SessionsCountLimit` | 973 | `15` |
| `WebUI/ClickjackingProtection` | 986 | **`true`** |
| `WebUI/CSRFProtection` | 999 | **`true`** |
| `WebUI/SecureCookie` | 1012 | **`true`** |
| `WebUI/HostHeaderValidation` | 1025 | **`true`** |
| `WebUI/HTTPS/Enabled` | 1038 | `false` |
| `WebUI/HTTPS/CertificatePath` | 1051 | 无默认（空） |
| `WebUI/HTTPS/KeyPath` | 1064 | 无默认（空） |
| `WebUI/ReverseProxySupportEnabled` | 1129 | `false` |
| `WebUI/TrustedReverseProxiesList` | 1142 | 无默认（空） |

### 2a. 逐字片段（行号 ↔ 键 ↔ 默认值）

776:     return value(u"WebUI/Enabled"_s, defaultValue);

789:     return value(u"WebUI/LocalHostAuth"_s, true);

802:     return value(u"WebUI/AuthSubnetWhitelistEnabled"_s, false);

842:     return value<QString>(u"WebUI/ServerDomains"_s, u"*"_s);

855:     return value<QString>(u"WebUI/Address"_s, u"*"_s).trimmed();

868:     return value<quint16>(u"WebUI/Port"_s, 8080);

882:     return value(u"WebUI/UseUPnP"_s, false);

895:     return value<QString>(u"WebUI/Username"_s, u"admin"_s);

908:     return value<QByteArray>(u"WebUI/Password_PBKDF2"_s);

934:     return value<int>(u"WebUI/MaxAuthenticationFailCount"_s, 5);


960:     return value<int>(u"WebUI/SessionTimeout"_s, 3600);

973:     return value<int>(u"WebUI/SessionsCountLimit"_s, 15);

986:     return value(u"WebUI/ClickjackingProtection"_s, true);

999:     return value(u"WebUI/CSRFProtection"_s, true);

1012:     return value(u"WebUI/SecureCookie"_s, true);

1025:     return value(u"WebUI/HostHeaderValidation"_s, true);

1038:     return value(u"WebUI/HTTPS/Enabled"_s, false);

1051:     return value<Path>(u"WebUI/HTTPS/CertificatePath"_s);

1064:     return value<Path>(u"WebUI/HTTPS/KeyPath"_s);

1129:     return value(u"WebUI/ReverseProxySupportEnabled"_s, false);

1142:     return value<QString>(u"WebUI/TrustedReverseProxiesList"_s);

## 读法（供正文落笔时对齐口径）

- **四个防护开关的默认值都是 `true`**：`ClickjackingProtection`(986) / `CSRFProtection`(999) / `SecureCookie`(1012) / `HostHeaderValidation`(1025)。把它们设成 `false` 是**关掉**默认开启的防护，不是「打开某个功能」。
- **`HostHeaderValidation` 的用途有官方 tooltip**：防 **DNS rebinding**（`optionsdialog.ui:4225-4229`）；配套的 `Server domains` 默认 `*`(842)。
- **绑定地址默认 `*`**（`WebUI/Address`, 855），官方 tooltip 写明 `*` 表示 IPv4 与 IPv6 都监听（`optionsdialog.ui:3777-3779`）；端口默认 `8080`(868)。
- **HTTPS 默认关**（`WebUI/HTTPS/Enabled`, 1038 = `false`），要开需填 `Certificate:` 与 `Key:`（`optionsdialog.ui:3831-3846`）。
- **反向代理默认关**（`ReverseProxySupportEnabled`, 1129 = `false`）；开启后填 `Trusted proxies list`，官方 tooltip 说明其目的是**用转发后的客户端地址**（`X-Forwarded-For`，`optionsdialog.ui:4285-4287`）。
- 本文件**不含**「要不要暴露到公网」「怎么签证书」「反向代理怎么配」的**操作步骤**——那属教程 / 环境相关，需另有来源（官方 wiki 链接见 `optionsdialog.ui:4294`），本册不代为给出。

