---
title: "第06章：ARP与邻居发现"
tags: [linux, network]
created: 2026-07-29
updated: 2026-07-29
status: complete
source_project: linux-network-info-concepts
---
# ARP 涓庨偦灞呭彂鐜?
## 浠庝竴涓棶棰樺紑濮?
涓ゅ彴鏈哄櫒鍦ㄥ悓涓€涓簩灞傜綉缁滐紙姣斿杩炲湪鍚屼竴涓氦鎹㈡満涓婏級锛孉 瑕佸彂涓€涓?IP 鍖呯粰 B銆侫 鐭ラ亾 B 鐨?IP 鍦板潃锛坄192.168.1.5`锛夛紝浣嗕互澶綉甯х殑鐩爣鍦板潃闇€瑕佺殑鏄?**MAC 鍦板潃**锛岃€屼笉鏄?IP 鍦板潃銆侫 鎬庝箞鐭ラ亾 B 鐨?MAC 鏄粈涔堬紵

杩欎釜"IP 鍒?MAC"鐨勬槧灏勫氨鏄湰绔犺瑙ｅ喅鐨勬牳蹇冮棶棰樸€傛槧灏勮〃鐢?**ARP 鍗忚**锛圛Pv4锛夋垨 **NDP**锛圛Pv6锛夌淮鎶わ紝鑰?`ip neigh` 灏辨槸鎴戜滑鏌ョ湅鍜屾搷浣滆繖寮犺〃鐨勫懡浠ゃ€?
> [!note] 鍓嶇疆鐭ヨ瘑
> 璇绘湰绔犲墠锛屼綘搴旇浜嗚В MAC 鍦板潃锛? 瀛楄妭鐨勭綉鍗＄‖浠跺湴鍧€锛夊拰 IP 鍦板潃鐨勫熀鏈尯鍒€傚鏋滀綘瀵?MAC 鍦板潃涓嶅お鐔熸倝锛屽缓璁厛璇荤浜岀珷"缃戠粶鎺ュ彛涓庨摼璺眰淇℃伅"銆?
---

## ARP 鍗忚鏍稿績姒傚康

### 骞挎挱璇锋眰锛屽崟鎾洖澶?
ARP锛圓ddress Resolution Protocol锛屽湴鍧€瑙ｆ瀽鍗忚锛夌殑宸ヤ綔鍘熺悊闈炲父绠€鍗曪紝鍙湁涓や釜姝ラ锛?
```
涓绘満 A (192.168.1.2, MAC: aa:aa:aa:aa:aa:aa)
鎯虫壘 B (192.168.1.5) 鐨?MAC

Step 1: 骞挎挱  鈹€鈹€鈫?浜ゆ崲鏈?鈹€鈹€鈫?鎵€鏈夊悓缃戞璁惧
          "璋佹槸 192.168.1.5锛熻鍛婅瘔 aa:aa:aa:aa:aa:aa"
          鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?          鈹?鐩爣 MAC: FF:FF:FF:FF:FF:FF  鈫?骞挎挱鍦板潃
          鈹?婧?MAC:    aa:aa:aa:aa:aa:aa  鈫?A 鑷繁鐨?MAC
          鈹?璇锋眰:      192.168.1.5 鐨?MAC 鏄皝锛?          鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
Step 2: 鍗曟挱  鈫愨攢鈹€ 鍙湁 B 鍥炲
          "192.168.1.5 鏄垜锛屾垜鐨?MAC 鏄?bb:bb:bb:bb:bb:bb"
          鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?          鈹?鐩爣 MAC: aa:aa:aa:aa:aa:aa  鈫?鍗曟挱鐩存帴鍙戠粰 A
          鈹?婧?MAC:    bb:bb:bb:bb:bb:bb  鈫?B 鍝嶅簲
          鈹?鍥炲:      192.168.1.5 鈫?bb:bb:bb:bb:bb:bb
          鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

鍏抽敭鐗瑰緛锛?
| 鐗瑰緛 | 璇存槑 |
|------|------|
| **骞挎挱璇锋眰** | 鐩爣 MAC 濉?`FF:FF:FF:FF:FF:FF`锛屽悓涓€骞挎挱鍩熷唴鎵€鏈夎澶囬兘浼氭敹鍒?|
| **鍗曟挱鍥炲** | 鍙湁鐩爣 IP 瀵瑰簲鐨勮澶囧洖澶嶏紝鍥炲鏄崟鎾紙鐩存帴鍙戠粰璇锋眰鑰咃級 |
| **缂撳瓨** | 瑙ｆ瀽缁撴灉瀛樺叆鍐呮牳鐨?ARP 缂撳瓨锛堥偦灞呰〃锛夛紝鍚庣画涓嶅啀骞挎挱 |
| **瓒呮椂** | 鏉＄洰鏈夌敓瀛樻椂闂达紙閫氬父鍑犲崄绉掑埌鍑犲垎閽燂級锛岃秴鏃跺悗閲嶆柊鎺㈡祴 |
| **鍗忚鏍囪瘑** | 浠ュお缃戝抚涓?EtherType = `0x0806` 琛ㄧず ARP |

> [!tip] 鎶撳寘楠岃瘉
> 鍙互鐢?`tcpdump -i eth0 arp` 鎶撳埌 ARP 璇锋眰鍜屽洖澶嶅寘銆備綘浼氱湅鍒板箍鎾姹傜殑 MAC 鐩爣鍦板潃鍏ㄦ槸 `ff:ff:ff:ff:ff:ff`锛岃€屽洖澶嶆槸鍗曟挱銆?
### ARP 鍙湪鍚屼竴骞挎挱鍩熷唴宸ヤ綔

杩欐槸 **闈炲父鍏抽敭** 鐨勪竴鐐癸細ARP 涓嶈兘璺ㄨ矾鐢卞櫒宸ヤ綔銆傚鏋滅洰鏍?IP 涓嶅湪鍚屼竴瀛愮綉锛屼富鏈轰細鎶婂寘鍙戠粰榛樿缃戝叧锛岀劧鍚庣敤 ARP 瑙ｆ瀽 **缃戝叧鐨?MAC**锛岃€岄潪鐩爣 IP 鐨?MAC銆?
```
# 鏈満 IP: 192.168.1.2/24
# 榛樿缃戝叧: 192.168.1.1
# 鐩爣: 8.8.8.8锛堜笉鍦ㄥ悓涓€瀛愮綉锛?
# 鏈満鍒ゆ柇锛?.8.8.8 涓嶅湪 192.168.1.0/24 鍐?# 琛屼负锛欰RP 鏌ヨ鐨勬槸 192.168.1.1锛堢綉鍏筹級鐨?MAC锛屼笉鏄?8.8.8.8 鐨?```

---

## 閭诲眳鐘舵€佹満璇﹁В

ARP 缂撳瓨涓殑姣忎釜鏉＄洰閮芥湁涓€涓?*鐘舵€?*锛屾爣蹇楃潃璇ユ槧灏勭殑"淇′换绋嬪害"銆傜悊瑙ｈ繖浜涚姸鎬佹槸鎺掗殰鐨勫熀纭€銆?
```
                    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                    鈹? PERMANENT 鈹? 鈫?闈欐€侀厤缃紝姘镐笉瓒呮椂
                    鈹斺攢鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹?                          鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹?    鈹? FAILED   鈹傗梽鈹€鈹€鈹€鈹?鍒氭坊鍔? 鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹攢鈹€鈹€鈹€鈹?                         鈹?瑙ｆ瀽鎴愬姛
                    鈹屸攢鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹€鈹?                    鈹?REACHABLE 鈹? 鈫?鏈€杩戠‘璁よ繃鍙揪
                    鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹?                         鈹?瓒呮椂锛堢害 30s锛?                    鈹屸攢鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹?                    鈹? STALE  鈹? 鈫?鍙兘杩樺彲鐢紝浣嗘湭楠岃瘉
                    鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹?                         鈹?瑕佸彂鍖呯粰杩欎釜閭诲眳
                    鈹屸攢鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹?                    鈹? DELAY  鈹? 鈫?寤惰繜楠岃瘉鏈燂紙绾?5s锛?                    鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹?                         鈹?浠嶇劧娌＄‘璁?                    鈹屸攢鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹?                    鈹? PROBE  鈹? 鈫?鍙戝崟鎾帰娴嬶紙鏈€澶?3 娆★級
                    鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹?                    鎴愬姛锛忊攤 澶辫触
                 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                 鈻?               鈻?            鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?            鈹俁EACHABLE 鈹?  鈹? FAILED  鈹?            鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

### 鐘舵€佽瑙?
| 鐘舵€?| 鍚箟 | 鍏稿瀷瑙﹀彂鏉′欢 |
|------|------|-------------|
| **REACHABLE** | 鏈€杩戠‘璁よ繃鍙揪锛屾槧灏勬湁鏁?| 鍒氬畬鎴?ARP 瑙ｆ瀽 / 鏀跺埌瀵圭鍥炲 |
| **STALE** | 鏉＄洰瓒呮椂锛屽彲鑳戒粛鍙敤浣嗘湭楠岃瘉 | REACHABLE 瓒呮椂锛堥粯璁ょ害 30-45 绉掞級 |
| **DELAY** | 闇€瑕佸彂鏁版嵁浜嗭紝浣嗗厛绛変竴灏忎細鍎?| STALE 鐘舵€佷笅鏈夋祦閲忚鍙戠粰杩欎釜 IP |
| **PROBE** | 姝ｅ湪鍙戝崟鎾帰娴嬬‘璁?| DELAY 瓒呮椂锛堢害 5 绉掞級鍚庝粛鏈敹鍒扮‘璁?|
| **FAILED** | 涓嶅彲杈?| PROBE 閲嶈瘯澶辫触 |
| **PERMANENT** | 闈欐€佹潯鐩紝姘镐笉瓒呮椂 | 閫氳繃 `ip neigh add ... nud permanent` 娣诲姞 |

> [!warning] STALE 涓嶆槸"鍧?鐨勭姸鎬?
> STALE 鍙〃绀?鏈変竴娈垫椂闂存病纭浜?銆傚鏋滄槧灏勫疄闄呬笂浠嶆槸姝ｇ‘鐨勶紝浠?STALE 鍙戞暟鎹寘鏃惰蛋 DELAY 鈫?PROBE 娴佺▼锛屾垚鍔熷悗浼氬洖鍒?REACHABLE锛岀敤鎴峰熀鏈棤鎰熺煡銆?
### 瓒呮椂鍙傛暟璋冧紭

```bash
# 鏌ョ湅 ARP 鐩稿叧瓒呮椂鍙傛暟
sysctl net.ipv4.neigh.default.gc_stale_time
# 榛樿鍊? 60 绉?# 鍚箟: 浠?REACHABLE 鍙樹负 STALE 鐨勬椂闂?
sysctl net.ipv4.neigh.default.base_reachable_time
# 榛樿鍊? 30 绉?# 鍚箟: REACHABLE 鐘舵€佺殑鍩虹瓒呮椂鏃堕棿

sysctl net.ipv4.neigh.default.retrans_time_ms
# 榛樿鍊? 1000 姣
# 鍚箟: PROBE 鐘舵€佺殑閲嶈瘯闂撮殧
```

---

## `ip neigh show` 杈撳嚭瑙ｈ

`ip neigh` 鏄?iproute2 涓鐞嗛偦灞呰〃鐨勫懡浠わ紝鏇夸唬鏃х殑 `arp -a`銆?
### 鍩烘湰鐢ㄦ硶

```bash
# 鏌ョ湅鎵€鏈夐偦灞呮潯鐩?ip neigh show

# 杈撳嚭绀轰緥
192.168.1.1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
192.168.1.5 dev eth0 lladdr 11:22:33:44:55:66 STALE
192.168.1.10 dev eth0 FAILED
fe80::1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
172.17.0.2 dev docker0 lladdr 02:42:ac:11:00:02 REACHABLE
```

### 杈撳嚭瀛楁瑙ｈ

```
192.168.1.1        dev eth0        lladdr aa:bb:cc:dd:ee:ff      REACHABLE
鈹斺攢鈹€鈹€鈹€ 閭诲眳 IP      鈹斺攢鈹€ 鎵€灞炵綉鍗?   鈹斺攢鈹€ 瀵圭 MAC 鍦板潃             鈹斺攢鈹€ 鐘舵€?   (鍙惈 IPv6)        (澶氫釜缃戝崱鏃?       (lladdr = link layer
                      鍖哄垎鎺ュ彛)          address)
```

### 甯哥敤杩囨护

```bash
# 鍙湅鏌愪釜鎺ュ彛鐨勯偦灞?ip neigh show dev eth0

# 鍙湅 IPv6 閭诲眳锛圢DP 鏉＄洰锛?ip neigh show dev eth0 | grep "inet6"   # 鎴?ip -6 neigh show

# 鍙煡鐪?REACHABLE 鐘舵€佺殑
ip neigh show | grep REACHABLE

# 鍙煡鐪?FAILED 鐨勶紙鍙兘鏈夐棶棰樼殑锛?ip neigh show | grep FAILED

# JSON 杈撳嚭锛堥€傚悎鑴氭湰瑙ｆ瀽锛?ip -j neigh show
```

### 涓庢棫鍛戒护瀵规瘮

```bash
# 鏃у懡浠わ紙net-tools锛?arp -a            # 鏌ョ湅 ARP 琛?arp -d 192.168.1.5  # 鍒犻櫎鏉＄洰

# 鏂板懡浠わ紙iproute2锛?ip neigh show     # 鏌ョ湅閭诲眳琛?ip neigh delete 192.168.1.5 dev eth0  # 鍒犻櫎鏉＄洰
```

> [!note] `ip neigh` vs `arp`
> `ip neigh` 鏄唴鏍?netlink 鎺ュ彛鐨勭洿鎺ュ皝瑁咃紝鏀寔 **IPv4锛圓RP锛夊拰 IPv6锛圢DP锛?* 缁熶竴杈撳嚭锛岃€屾棫 `arp` 鍛戒护鍙敮鎸?IPv4銆傚湪鐜颁唬鍙戣鐗堜笂锛屽缁堜娇鐢?`ip neigh`銆?
---

## `ip neigh flush` 娓呴櫎閭诲眳琛?
褰撲綘鎬€鐤戦偦灞呰〃涓湁杩囨湡鎴栭敊璇殑鏉＄洰鏃讹紝娓呯┖鍚庤鍐呮牳閲嶆柊瑙ｆ瀽鏄竴绉嶅父鐢ㄧ殑鎺掗殰鎵嬫銆?
### 娓呯┖鎵€鏈夋潯鐩?
```bash
# 娓呯┖鎵€鏈夐偦灞呮潯鐩?ip neigh flush all

# 杈撳嚭绀轰緥
192.168.1.1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE removed
192.168.1.5 dev eth0 lladdr 11:22:33:44:55:66 STALE removed
192.168.1.10 dev eth0 FAILED removed
```

### 鎸夋潯浠惰繃婊ゆ竻闄?
```bash
# 鍙竻绌烘煇涓帴鍙ｇ殑
ip neigh flush dev eth0

# 鍙竻绌?NUD_FAILED 鐘舵€佺殑
ip neigh flush nud failed

# 鍙竻绌烘寚瀹?IP
ip neigh flush 192.168.1.5 to 192.168.1.5

# 缁勫悎鏉′欢
ip neigh flush dev eth0 nud stale
```

### flush 鐨勫吀鍨嬩娇鐢ㄥ満鏅?
| 鍦烘櫙 | 鎿嶄綔 | 璇存槑 |
|------|------|------|
| 缃戝叧 MAC 鍙樻洿 | `ip neigh flush dev eth0` | 缃戝叧鏇存崲纭欢鍚庢棫鏄犲皠澶辨晥 |
| VM/瀹瑰櫒杩佺Щ | `ip neigh flush dev br0` | 杩佺Щ鍚?IP 鏈彉浣?MAC 鍙樹簡 |
| 棰戠箒鍑虹幇 FAILED | `ip neigh flush nud failed` | 娓呯悊涓嶅彲杈炬潯鐩伩鍏嶈〃婊?|
| 鎬€鐤?ARP 缂撳瓨闂 | `ip neigh flush all` | 璁╂墍鏈夋潯鐩噸鏂拌В鏋?|

> [!tip] flush 鍚庨獙璇?
> 娓呯┖鍚庤繍琛?`ping 192.168.1.1` 瑙﹀彂 ARP 閲嶆柊瑙ｆ瀽锛岀劧鍚?`ip neigh show` 纭鏂版潯鐩槸 REACHABLE銆?
### 闈欐€佹坊鍔犳潯鐩?
```bash
# 娣诲姞涓€涓?PERMANENT锛堟案涓嶈秴鏃讹級鐨勯潤鎬佹潯鐩?ip neigh add 192.168.1.100 lladdr de:ad:be:ef:00:01 nud permanent dev eth0

# 娣诲姞涓€涓?REACHABLE 鏉＄洰锛堜篃浼氳秴鏃讹級
ip neigh add 192.168.1.200 lladdr de:ad:be:ef:00:02 nud reachable dev eth0

# 鍒犻櫎闈欐€佹潯鐩?ip neigh delete 192.168.1.100 dev eth0
```

> [!warning] 璋ㄦ厧浣跨敤 PERMANENT
> 闈欐€?MAC 缁戝畾鍙湪鏋佸皯鏁板満鏅笅闇€瑕侊紙濡傜壒瀹氬畨鍏ㄨ姹傦級銆備竴鏃﹀绔‖浠舵洿鎹紝浣犱細鏀跺埌 **IP 閫氫絾瀹為檯涓嶉€?* 鐨勮寮傛晠闅溿€傚鏁板満鏅笅璁╁唴鏍歌嚜鍔ㄧ鐞嗗嵆鍙€?
---

## IPv6 NDP 鍙栦唬 ARP

IPv6 涓病鏈?ARP 鍗忚锛屽畠鐨勮鑹茬敱 **NDP锛圢eighbor Discovery Protocol锛岄偦灞呭彂鐜板崗璁級** 鏇夸唬銆?
### 鏍稿績宸紓

| 瀵规瘮缁村害 | ARP锛圛Pv4锛?| NDP锛圛Pv6锛?|
|---------|-----------|-------------|
| **鍗忚鍩虹** | 鐙珛鐨?ARP 鍗忚锛圗therType=0x0806锛?| 鍩轰簬 ICMPv6锛圱ype 135/136锛?|
| **浼犺緭鏂瑰紡** | 骞挎挱 (L2 broadcast) | 澶氭挱 (L2 multicast锛屼笉鍙戝埌鏃犲叧鑺傜偣) |
| **瀹夊叏鎬?* | 鏃犲唴缃繚鎶わ紝鏄撹 ARP 娆洪獥 | 鏀寔 SEND锛圫ecure Neighbor Discovery锛?|
| **鍦板潃瑙ｆ瀽** | ARP 璇锋眰/鍥炲 | 閭诲眳璇锋眰 NS / 閭诲眳鍏憡 NA |
| **鍏朵粬鍔熻兘** | 浠呭湴鍧€瑙ｆ瀽 | 杩樺寘鎷矾鐢卞櫒鍙戠幇銆佹棤鐘舵€佸湴鍧€鑷姩閰嶇疆(SLAAC)銆侀噸澶嶅湴鍧€妫€娴?DAD) |
| **鍐呮牳鎺ュ彛** | `ip neigh` 缁熶竴绠＄悊 | 鍚屼竴寮犻偦灞呰〃锛宍ip neigh` 鍚屾牱閫傜敤 |

### NDP 鐨勬牳蹇冩秷鎭?
```
NDP 閭诲眳璇锋眰 (Neighbor Solicitation, ICMPv6 Type 135)
  鈹€鈹€鈫?澶氭挱鍒扮洰鏍囪妭鐐圭殑琚姹傝妭鐐瑰鎾湴鍧€
  鈹€鈹€鈫?"璋佹槸 fe80::1234?"

NDP 閭诲眳鍏憡 (Neighbor Advertisement, ICMPv6 Type 136)
  鈫愨攢鈹€ 鍗曟挱鍥炲
  鈫愨攢鈹€ "fe80::1234 鏄垜锛屾垜鐨?MAC 鏄?aa:bb:cc:dd:ee:ff"
```

```bash
# 鏌ョ湅 IPv6 閭诲眳鏉＄洰锛堝拰 IPv4 鐢ㄥ悓涓€涓懡浠わ級
ip -6 neigh show

# 杈撳嚭绀轰緥
fe80::1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
fe80::1234 dev eth0 lladdr 11:22:33:44:55:66 STALE
```

> [!note] 閭诲眳琛ㄧ粺涓€绠＄悊
> 鍦?Linux 鍐呮牳灞傞潰锛孉RP锛圛Pv4锛夊拰 NDP锛圛Pv6锛夌殑瑙ｆ瀽缁撴灉瀛樺湪 **鍚屼竴寮犻偦灞呰〃** 涓€俙ip neigh show` 涓嶅尯鍒嗗崗璁紝IPv4 鍜?IPv6 鏉＄洰骞舵帓杈撳嚭銆傜敤 `ip -4 neigh show` 鍙湅 IPv4锛宍ip -6 neigh show` 鍙湅 IPv6銆?
---

## ARP 琛ㄦ孩鍑轰笌 `gc_thresh` 鎺掗殰

### 闂鐜拌薄

鍦ㄨ緝澶ц妯＄殑浜屽眰缃戠粶锛堝 Kubernetes 闆嗙兢鑺傜偣鏁拌緝澶氥€丏HCP 瀛愮綉寰堝ぇ锛夋垨棰戠箒寤虹珛/鏂紑杩炴帴鐨勫満鏅笅锛孉RP 琛ㄥ彲鑳戒細鍗犳弧銆傚崰婊″悗鐨勫吀鍨嬬棁鐘讹細

- 鍐呮牳鏃ュ織鍑虹幇 `neighbour: arp_cache: neighbor table overflow!`
- 鏂扮殑 AP R瑙ｆ瀽澶辫触锛屽鑷?`ping` 閫氫絾瀵圭杩炴帴寮傚父
- `dmesg | tail` 鑳界湅鍒扮浉鍏宠鍛?
### 涓変釜鍏抽敭鍙傛暟

鍐呮牳鐢ㄤ笁涓弬鏁版帶鍒?ARP 琛ㄧ殑鍨冨溇鍥炴敹锛圙C锛夛細

```bash
sysctl net.ipv4.neigh.default.gc_thresh1   # 杞笅闄愶紙榛樿 128锛?sysctl net.ipv4.neigh.default.gc_thresh2   # 杞笂闄愶紙榛樿 512锛?sysctl net.ipv4.neigh.default.gc_thresh3   # 纭笂闄愶紙榛樿 1024锛?```

| 鍙傛暟 | 浣滅敤 | 琛屼负 |
|------|------|------|
| `gc_thresh1` | 鏈€灏忎繚鐣欐暟 | 鏉＄洰灏戜簬杩欎釜鏁版椂锛孏C 涓嶄細涓诲姩鍥炴敹 |
| `gc_thresh2` | 杞笂闄?| 瓒呰繃杩欎釜鏁版椂锛孏C 寮€濮嬪皾璇曞洖鏀?**STALE** 鏉＄洰 |
| `gc_thresh3` | 纭笂闄?| 瓒呰繃杩欎釜鏁版椂锛岀洿鎺ユ嫆缁濇柊鏉＄洰锛堝紑濮嬩涪鍖咃級 |

### 鎺掓煡姝ラ

```bash
# 1. 鏌ョ湅褰撳墠閭诲眳琛ㄥぇ灏?ip neigh show | wc -l

# 2. 鏌ョ湅褰撳墠 GC 鍙傛暟
sysctl net.ipv4.neigh.default.gc_thresh1
sysctl net.ipv4.neigh.default.gc_thresh2
sysctl net.ipv4.neigh.default.gc_thresh3

# 3. 妫€鏌ュ唴鏍告棩蹇楁槸鍚︽湁婧㈠嚭璀﹀憡
dmesg | grep -i "neighbor table overflow"

# 4. 鐪?FAILED 鏉＄洰鏄惁杩囧
ip neigh show | grep FAILED | wc -l
```

### 瀹氫綅鍘熷洜

ARP 琛ㄦ孩鍑洪€氬父鏈変互涓嬪師鍥狅細

1. **瀛愮綉杩囧ぇ**锛堝 `/16` 鐢氳嚦 `/8` 鐨勫瓙缃戯級锛孉RP 鏉＄洰杩滃浜?`gc_thresh3`
2. **澶栭儴鎵弿**锛孖P 鎵弿宸ュ叿鍙戝嚭澶ч噺璇锋眰锛屼骇鐢熷ぇ閲?FAILED 鏉＄洰
3. **瀹瑰櫒/VM 棰戠箒鍒涘缓閿€姣?*锛孖P 涓嶆柇鍙樺寲锛屾棫鐨?STALE/FALED 鏉＄洰鍫嗙Н
4. **缃戠粶璁惧鏁呴殰**锛屾煇浜?IP 鍙嶅鍙揪/涓嶅彲杈撅紝瀵艰嚧鐘舵€侀绻佸垏鎹?
### 涓存椂淇

```bash
# 璋冨ぇ gc_thresh锛堜复鏃剁敓鏁堬紝閲嶅惎鍚庢仮澶嶏級
sysctl -w net.ipv4.neigh.default.gc_thresh1=512
sysctl -w net.ipv4.neigh.default.gc_thresh2=2048
sysctl -w net.ipv4.neigh.default.gc_thresh3=4096

# 娓呯┖ FAILED 鏉＄洰閲婃斁绌洪棿
ip neigh flush nud failed
```

### 鎸佷箙鍖栭厤缃?
```bash
# 鍐欏叆 /etc/sysctl.conf 鎴?/etc/sysctl.d/99-arp.conf
cat >> /etc/sysctl.d/99-arp.conf << 'EOF'
# ARP 琛?GC 鍙傛暟璋冧紭锛堥€傜敤浜庡ぇ浜屽眰缃戠粶锛?net.ipv4.neigh.default.gc_thresh1 = 512
net.ipv4.neigh.default.gc_thresh2 = 2048
net.ipv4.neigh.default.gc_thresh3 = 4096
EOF

# 绔嬪嵆鐢熸晥
sysctl -p /etc/sysctl.d/99-arp.conf
```

> [!warning] gc_thresh3 涓嶆槸瓒婂瓒婂ソ
> 姣忎釜閭诲眳鏉＄洰绾﹀崰鐢?256 瀛楄妭鍐呮牳鍐呭瓨銆傝缃繃澶э紙濡傚崄鍑犱竾锛変細娑堣€楀ぇ閲忓唴鏍稿唴瀛樸€傛牴鎹疄闄呴渶瑕佽缃紝Kubernetes 闆嗙兢寤鸿璁句负鑺傜偣鏁扮殑 2-3 鍊嶃€?
---

## 鏈珷灏忕粨

- **ARP 鍗忚** 閫氳繃骞挎挱璇锋眰 / 鍗曟挱鍥炲锛屽皢 IP 鍦板潃瑙ｆ瀽涓?MAC 鍦板潃锛?*鍙湪鍚屼竴骞挎挱鍩熷唴宸ヤ綔**
- **閭诲眳鐘舵€佹満** 鏄悊瑙?ARP 缂撳瓨琛屼负鐨勫叧閿細REACHABLE锛堟渶杩戠‘璁わ級鈫?STALE锛堣秴鏃讹級鈫?DELAY锛堢瓑寰咃級鈫?PROBE锛堟帰娴嬶級鈫?FAILED锛堝け璐ワ級锛孭ERMANENT 鏄潤鎬佺粦瀹?- `ip neigh show` 鏄煡鐪嬮偦灞呰〃鐨勬爣鍑嗗懡浠わ紝鏀寔 `-j` JSON 杈撳嚭鍜屾寜鎺ュ彛/鐘舵€佽繃婊わ紝**缁熶竴绠＄悊 IPv4锛圓RP锛夊拰 IPv6锛圢DP锛?*
- `ip neigh flush` 娓呯┖閭诲眳琛ㄦ槸甯歌鎺掗殰鎵嬫锛屽彲閰嶅悎杩囨护鏉′欢瀹氬悜娓呴櫎
- **IPv6 鐢?NDP 鏇夸唬 ARP**锛屽熀浜?ICMPv6 澶氭挱锛屾洿楂樻晥瀹夊叏锛屼絾鍐呮牳浣跨敤鍚屼竴寮犻偦灞呰〃绠＄悊
- **ARP 琛ㄦ孩鍑?* 鐢?`gc_thresh1/2/3` 鎺у埗锛岃秴杩囩‖涓婇檺浼氬鑷村唴鏍镐涪鍖咃紝鍙牴鎹瓙缃戣妯￠€傚綋璋冨ぇ
- 鎺掓煡 ARP 闂鐨勫熀鏈€濊矾锛歚ip neigh show | wc -l` 鈫?`dmesg | grep "neighbor table overflow"` 鈫?瀹氫綅鍘熷洜 鈫?`ip neigh flush nud failed` 鈫?璋冩暣 `gc_thresh`

### 涓嬬珷棰勫憡

涓嬩竴绔犳垜浠皢浠庢暟鎹摼璺眰锛圠2锛夎穬鍗囧埌浼犺緭灞傦紙L4锛夛紝瀛︿範 **Socket 杩炴帴涓庝紶杈撳眰淇℃伅**銆備綘浼氱湅鍒板浣曠敤 `ss` 鏇夸唬 `netstat` 鏌ョ湅 TCP/UDP 杩炴帴鐘舵€併€佽В璇?Recv-Q/Send-Q 鐨勫惈涔夛紝浠ュ強濡備綍閫氳繃 TCP 鐘舵€佹満璇婃柇杩炴帴闂銆?
---

*绔犺妭缂栧彿锛?6 | 璁″垝绡囧箙锛氱煭 | 浠ｇ爜绀轰緥锛氭湁*

