---
title: "第05章：DNS解析与域名信息"
tags: [linux, network]
created: 2026-07-29
updated: 2026-07-29
status: complete
source_project: linux-network-info-concepts
---
# DNS 瑙ｆ瀽涓庡煙鍚嶄俊鎭?
褰撲綘杈撳叆 `baidu.com` 骞舵寜涓嬪洖杞︼紝娴忚鍣ㄩ渶瑕佹壘鍒拌繖涓煙鍚嶅搴旂殑 IP 鍦板潃鎵嶈兘寤虹珛杩炴帴銆傝繖涓粠"鍩熷悕"鍒?IP"鐨勮浆鎹㈣繃绋嬶紝灏辨槸 **DNS 瑙ｆ瀽锛圖omain Name System resolution锛?*銆傚畠鏄簰鑱旂綉閫氫俊鐨勭涓€姝モ€斺€斿鏋滆繖涓€姝ュけ璐ワ紝浣犺繛涓嶄笂浠讳綍缃戠珯锛岃€?`ping` 鍜?`ip addr` 鐪嬪埌鐨勭綉缁滈厤缃彲鑳藉畬鍏ㄦ甯搞€?
鏈珷鏄叏涔︽渶闀跨殑涓€绔狅紝鍥犱负 DNS 鏄疄闄呮帓闅滀腑**鏈€甯稿嚭闂**鐨勭幆鑺傦紝鑰屼笖 Linux 涓婄殑 DNS 浣撶郴缁忓巻浜嗗娆℃紨鍙橈紝鏂拌€侀厤缃苟瀛橈紝鏋佸叾瀹规槗韪╁潙銆備綘灏嗗鍒帮細DNS 鍒板簳鏄€庝箞宸ヤ綔鐨勩€丩inux 涓婂摢浜涙枃浠舵帶鍒?DNS銆佷互鍙婂浣曠敤 `dig`/`resolvectl` 绛夊伐鍏风簿鍑嗗畾浣嶉棶棰樸€?
---

## DNS 瑙ｆ瀽瀹屾暣娴佺▼锛氫粠娴忚鍣ㄥ埌 DNS 鏈嶅姟鍣?
> [!note] 涓€鍙ヨ瘽鐞嗚В DNS
> DNS 鏈川涓婃槸涓€涓?*鍒嗗竷寮忕殑閿€兼暟鎹簱**鈥斺€旈敭鏄煙鍚嶏紙濡?`www.example.com`锛夛紝鍊兼槸 IP 鍦板潃锛堝 `93.184.216.34`锛夈€傛煡璇㈢殑杩囩▼灏辨槸娌跨潃杩欎釜鍒嗗竷寮忔暟鎹簱鐨勯摼鏉￠€愮骇鏌ユ壘銆?
涓嬮潰浠ュ湪娴忚鍣ㄤ腑杈撳叆 `www.example.com` 涓轰緥锛屽畬鏁磋蛋涓€閬?DNS 瑙ｆ瀽鐨勬祦绋嬨€?
### 绗竴姝ワ細娴忚鍣ㄧ紦瀛樻鏌?
娴忚鍣ㄨ嚜韬淮鎶や簡涓€涓?DNS 缂撳瓨銆傚鏋滀箣鍓嶆煡杩?`www.example.com` 涓旂紦瀛樻湭杩囨湡锛屾祻瑙堝櫒鐩存帴鐢ㄧ紦瀛樼殑 IP锛?*涓嶅彂閫佷换浣曠綉缁滆姹?*銆備綘鍙互閫氳繃 `chrome://net-internals/#dns`锛圕hrome锛夋垨 `about:networking#dns`锛團irefox锛夋煡鐪嬫祻瑙堝櫒 DNS 缂撳瓨銆?
### 绗簩姝ワ細鎿嶄綔绯荤粺缂撳瓨妫€鏌?
濡傛灉娴忚鍣ㄧ紦瀛樻病鍛戒腑锛屾祻瑙堝櫒浼氳皟鐢ㄦ搷浣滅郴缁熺殑瑙ｆ瀽鎺ュ彛銆傚湪 Linux 涓婏紝鎿嶄綔绯荤粺锛堝 systemd-resolved锛変篃浼氱淮鎶や竴涓?DNS 缂撳瓨銆傜敤 `resolvectl statistics` 鍙互鐪嬪埌缂撳瓨鍛戒腑鎯呭喌銆?
### 绗笁姝ワ細璇诲彇 `/etc/hosts`

濡傛灉鎿嶄綔绯荤粺缂撳瓨涔熸病鏈夛紝Linux 浼氭鏌?`/etc/hosts` 鏂囦欢銆傝繖涓枃浠舵槸**闈欐€佺殑鍩熷悕鈫扞P 鏄犲皠琛?*锛屼紭鍏堢骇閫氬父楂樹簬 DNS 鏌ヨ鈥斺€旇繖鏄?`/etc/nsswitch.conf` 涓?`hosts: files dns` 鐨勫惈涔夛紙"鍏堟煡鏂囦欢锛屽啀鏌?DNS"锛夈€?
```bash
# /etc/hosts 绀轰緥
127.0.0.1       localhost
127.0.1.1       my-laptop
192.168.1.10    dev-server.internal
# 涓嬮潰杩欒鍙互鐢ㄦ潵涓存椂灞忚斀鏌愪釜鍩熷悕锛堝己鍒舵寚鍚?127.0.0.1锛?127.0.0.1       unwanted-ads.example.com
```

> [!tip] `/etc/hosts` 鐨勫疄鐢ㄥ満鏅?> - **寮€鍙戠幆澧?*锛氬皢 `my-app.local` 鎸囧悜鏈満 `127.0.0.1`锛屾柟渚挎湰鍦拌皟璇?> - **灞忚斀鍩熷悕**锛氬皢骞垮憡鍩熷悕鎸囧悜 `127.0.0.1` / `0.0.0.0`
> - **绱ф€ョ粫杩?DNS 鏁呴殰**锛氬鏋?DNS 鏈嶅姟鍣ㄦ寕浜嗭紝鍙互鍦?hosts 閲屼复鏃跺啓鍏ュ叧閿煙鍚?
### 绗洓姝ワ細鏌ヨ DNS 瑙ｆ瀽鍣?
濡傛灉 `/etc/hosts` 涓篃娌℃湁锛孡inux 灏嗘煡璇㈤厤缃殑 DNS 瑙ｆ瀽鍣ㄣ€傚湪鐜颁唬 Ubuntu 绯荤粺涓婏紝杩欎釜瑙ｆ瀽鍣ㄩ€氬父鏄?**systemd-resolved** 鐨?stub resolver锛坄127.0.0.53`锛夛紝瀹冨厖褰撴湰鍦?DNS 浠ｇ悊锛岃礋璐ｇ紦瀛樸€佽浆鍙戝拰 DNSSEC 楠岃瘉銆?
### 绗簲姝ワ細閫掑綊鏌ヨ鍒版潈濞?DNS

瑙ｆ瀽鍣ㄤ粠鏍?DNS 鏈嶅姟鍣ㄥ紑濮嬶紝閫愮骇鍚戜笅鏌ヨ锛屾渶缁堝埌杈?`www.example.com` 鐨勬潈濞?DNS 鏈嶅姟鍣ㄣ€傚畬鏁寸殑閫掑綊杩囩▼濡備笅锛?
```
瀹㈡埛绔?鈫?鏈湴瑙ｆ瀽鍣?(127.0.0.53)
       鈫?   閫掑綊鏌ヨ寮€濮?       鈫?   鏍?DNS 鏈嶅姟鍣?         鈫? 杩斿洖 .com 椤剁骇鍩熸湇鍔″櫒鍦板潃
       鈫?   .com 椤剁骇鍩熸湇鍔″櫒      鈫? 杩斿洖 example.com 鏉冨▉鏈嶅姟鍣ㄥ湴鍧€
       鈫?   example.com 鏉冨▉鏈嶅姟鍣? 鈫? 杩斿洖 www.example.com 鐨?IP 鍦板潃
       鈫?   鏈湴瑙ｆ瀽鍣ㄧ紦瀛樼粨鏋滐紝杩斿洖缁欏鎴风
```

> [!tip] `+trace` 鍙傛暟鍙互浜茬溂鐪嬪埌杩欎釜閾炬潯
> `dig www.example.com +trace` 浼氫竴姝ユ灞曠ず浠庢牴鍒版潈濞佺殑瀹屾暣鏌ヨ杩囩▼锛屾湰绔犲悗闈細璇︾粏婕旂ず銆?
### 绗叚姝ワ細娴忚鍣ㄥ彂璧?HTTP 杩炴帴

鎷垮埌 IP 鍦板潃鍚庯紝娴忚鍣ㄧ粓浜庡彲浠ュ彂璧?TCP 杩炴帴锛屽紑濮?HTTP 璇锋眰銆傝嚦姝わ紝DNS 瑙ｆ瀽鐨勪娇鍛藉畬鎴愩€?
```
瀹屾暣閾捐矾锛?娴忚鍣ㄧ紦瀛?鈫?鎿嶄綔绯荤粺缂撳瓨 鈫?/etc/hosts 鈫?DNS 瑙ｆ瀽鍣?鈫?鏍?DNS 鈫?TLD 鈫?鏉冨▉ DNS
                                  鈫?                           锛堝埌杩欎竴姝ユ墠鍙戠綉缁滃寘锛?```

---

## DNS 璁板綍绫诲瀷璇﹁В

DNS 涓嶅彧鏄?鍩熷悕鈫扞P"鐨勭畝鍗曟槧灏勩€傚畠鏄竴涓赴瀵岀殑鏁版嵁搴擄紝姣忔潯璁板綍绉颁负涓€涓?**璧勬簮璁板綍锛圧esource Record, RR锛?*锛屾湁涓嶅悓绫诲瀷銆?
### 鏍稿績璁板綍绫诲瀷閫熸煡

| 璁板綍绫诲瀷 | 鍏ㄧО | 浣滅敤 | 鏌ヨ鍛戒护 |
|---------|------|------|---------|
| **A** | Address Record | 鍩熷悕 鈫?IPv4 鍦板潃 | `dig example.com A` |
| **AAAA** | IPv6 Address Record | 鍩熷悕 鈫?IPv6 鍦板潃 | `dig example.com AAAA` |
| **CNAME** | Canonical Name | 鍩熷悕鍒悕锛堝煙鍚?鈫?鍙︿竴涓煙鍚嶏級 | `dig www.example.com CNAME` |
| **MX** | Mail Exchange | 閭欢鏈嶅姟鍣紙鍚紭鍏堢骇锛?| `dig example.com MX` |
| **NS** | Name Server | 鍩熷悕鐨勬潈濞?DNS 鏈嶅姟鍣?| `dig example.com NS` |
| **TXT** | Text Record | 浠绘剰鏂囨湰淇℃伅锛堝父鐢ㄤ簬 SPF/DKIM 楠岃瘉锛?| `dig example.com TXT` |
| **SOA** | Start of Authority | 鍖哄煙鐨勬潈濞佷俊鎭紙鍒锋柊闂撮殧銆佺鐞嗗憳閭绛夛級 | `dig example.com SOA` |

### A 璁板綍

鏈€鍩烘湰鐨勮褰曪紝灏嗗煙鍚嶆槧灏勫埌涓€涓?IPv4 鍦板潃銆備竴涓煙鍚嶅彲浠ユ湁澶氭潯 A 璁板綍瀹炵幇**DNS 杞璐熻浇鍧囪　**銆?
```bash
$ dig baidu.com A +short
39.156.66.10
110.242.68.66

# 涓や釜 IP鈥斺€旂櫨搴︾敤浜?DNS 杞锛屾瘡娆¤В鏋愬彲鑳芥嬁鍒颁笉鍚?IP
```

### AAAA 璁板綍

涓?A 璁板綍鍔熻兘鐩稿悓锛屼絾杩斿洖鐨勬槸 IPv6 鍦板潃銆?
```bash
$ dig baidu.com AAAA +short
# 濡傛灉鍩熷悕娌℃湁 IPv6 鍦板潃锛岃繖閲屾病鏈夎緭鍑?```

### CNAME 璁板綍

灏嗗煙鍚嶆寚鍚戝彟涓€涓煙鍚嶃€侰NAME 璁板綍鏈韩涓嶈繑鍥?IP鈥斺€斿鎴风闇€瑕佸啀鏌ヤ竴娆＄洰鏍囧煙鍚嶇殑 A/AAAA 璁板綍銆?
> [!warning] CNAME 鐨勫父瑙侀櫡闃?> - CNAME 璁板綍涓嶈兘涓庡叾浠栬褰曠被鍨嬪叡瀛樹簬鍚屼竴涓煙鍚嶄笂
> - 鏍瑰煙鍚嶏紙濡?`example.com`锛夐€氬父涓嶈兘鐢?CNAME锛屽洜涓?NS/SOA 璁板綍浼氬啿绐佲€斺€旇繖灏辨槸涓轰粈涔堝緢澶氱綉绔欐妸 `www.example.com` 鍋?CNAME 鍒?`example.com`锛岃€?`example.com` 鏈韩鐢?A 璁板綍

```bash
# 寰堝 CDN 鏈嶅姟鐢?CNAME 鎸囧悜鍔犻€熷煙鍚?$ dig www.baidu.com CNAME +short
www.a.shifen.com.

# 瀹㈡埛绔渶瑕佸啀鏌ヤ竴娆?A 璁板綍鎵嶈兘鎷垮埌 IP
$ dig www.a.shifen.com A +short
39.156.66.14
110.242.68.3
```

### MX 璁板綍

鎸囧畾鍩熷悕鐨勯偖浠舵湇鍔″櫒鍦板潃銆傛瘡涓?MX 璁板綍甯︽湁涓€涓?**浼樺厛绾э紙preference锛?* 瀛楁锛屾暟鍊艰秺灏忎紭鍏堢骇瓒婇珮銆?
```bash
$ dig gmail.com MX +short
30 alt3.gmail-smtp-in.l.google.com.
10 alt1.gmail-smtp-in.l.google.com.
40 alt4.gmail-smtp-in.l.google.com.
20 alt2.gmail-smtp-in.l.google.com.
5  gmail-smtp-in.l.google.com.
```

杩欓噷 `gmail-smtp-in.l.google.com` 浼樺厛绾?5锛堟渶楂橈級锛宍alt1` 浼樺厛绾?10锛堝鐢級锛屼互姝ょ被鎺ㄣ€傚彂浠舵湇鍔″櫒浼氬厛灏濊瘯浼樺厛绾ф渶楂樼殑锛屽け璐ュ悗渚濇灏濊瘯澶囩敤銆?
### NS 璁板綍

鎸囧畾鍝釜 DNS 鏈嶅姟鍣ㄦ槸鏌愪釜鍩熷悕鐨勬潈濞佹湇鍔″櫒銆傝繖鏄?DNS 濮旀淳鏈哄埗鐨勬牳蹇冦€?
```bash
$ dig baidu.com NS +short
ns3.baidu.com.
ns7.baidu.com.
dns.baidu.com.
ns4.baidu.com.
ns2.baidu.com.
```

### TXT 璁板綍

瀛樺偍浠绘剰鏂囨湰淇℃伅锛岃骞挎硾鐢ㄤ簬鍩熷悕鎵€鏈夋潈楠岃瘉鍜岄偖浠跺畨鍏ㄣ€?
```bash
# SPF 璁板綍鈥斺€斿０鏄庡摢浜涙湇鍔″櫒鍙互浠ｈ〃璇ュ煙鍚嶅彂閭欢
$ dig gmail.com TXT +short
"v=spf1 redirect=_spf.google.com"
"v=spf1 include:_spf.google.com ~all"
"google-site-verification=..._LpQc"
```

甯歌鐢ㄩ€旓細
- **SPF**锛圫ender Policy Framework锛夛細澹版槑鍚堟硶鐨勫彂浠舵湇鍔″櫒
- **DKIM**锛氶偖浠剁鍚嶉獙璇佸叕閽?- **DMARC**锛氶偖浠堕獙璇佸け璐ユ椂鐨勫鐞嗙瓥鐣?- **鍩熷悕鎵€鏈夋潈楠岃瘉**锛氫簯鏈嶅姟鍟嗚浣犳坊鍔?TXT 璁板綍璇佹槑浣犳帶鍒惰鍩熷悕

### SOA 璁板綍

鍖哄煙锛坺one锛夌殑**鏉冨▉鍏冩暟鎹褰?*銆傛瘡涓煙鍚嶆湁涓斾粎鏈変竴涓?SOA 璁板綍锛屽寘鍚互涓嬪叧閿瓧娈碉細

```bash
$ dig baidu.com SOA
...
baidu.com.  7200  IN  SOA  dns.baidu.com.  sa.baidu.com. (
                        2024072201  ; serial锛堝簭鍒楀彿锛屽尯鍩熺増鏈爣璇嗭級
                        300         ; refresh锛堜粠鏈嶅姟鍣ㄥ埛鏂伴棿闅旓紝绉掞級
                        300         ; retry锛堝埛鏂板け璐ュ悗閲嶈瘯闂撮殧锛岀锛?                        2592000     ; expire锛堜粠鏈嶅姟鍣ㄦ暟鎹繃鏈熸椂闂达紝绉掞級
                        7200        ; minimum锛堝惁瀹氱紦瀛?TTL锛岀锛?)
```

> [!tip] SOA 鐨?serial 瀛楁鏄?DNS 鎺掗殰绁炲櫒"
> 褰撲綘鐨?DNS 淇敼娌℃湁鐢熸晥鏃讹紝鐢?`dig example.com SOA` 鏌ョ湅 serial 鍙枫€傚鏋滀笌浣犻鏈熺殑涓嶄竴鑷达紝璇存槑 DNS 鏈嶅姟鍣ㄤ笂鐨勫尯鍩熸枃浠舵病鏈夋洿鏂版垨鍚屾銆?
### 璁板綍绫诲瀷鏌ヨ閫氱敤鍐欐硶

```bash
# 鎸囧畾璁板綍绫诲瀷
dig baidu.com A          # A 璁板綍
dig baidu.com AAAA       # AAAA 璁板綍
dig baidu.com MX         # MX 璁板綍
dig baidu.com NS         # NS 璁板綍
dig baidu.com TXT        # TXT 璁板綍
dig baidu.com SOA        # SOA 璁板綍
dig baidu.com CNAME      # CNAME 璁板綍
dig baidu.com ANY        # 鎵€鏈夎褰曠被鍨嬶紙娉ㄦ剰锛氬緢澶?DNS 鏈嶅姟鍣ㄤ笉鏀寔 ANY 鏌ヨ锛?
# +short 绠€鍖栬緭鍑?dig baidu.com MX +short

# +noall +answer 鍙樉绀哄洖绛旈儴鍒嗭紙姣?+short 鐣ヨ缁嗭級
dig baidu.com MX +noall +answer
```

---

## Linux DNS 閰嶇疆鏂囦欢浣撶郴

Linux 涓婄殑 DNS 瑙ｆ瀽涓嶆槸"涓€涓枃浠舵悶瀹?鐨勭畝鍗曚簨鎯呫€?*涓変釜鏂囦欢**鏋勬垚涓€鏉″畬鏁寸殑瑙ｆ瀽閾捐矾锛岀悊瑙ｅ畠浠殑鍗忎綔鍏崇郴鏄帓鏌?DNS 闂鐨勫叧閿€?
### 閰嶇疆鏂囦欢閾捐矾

```
/etc/nsswitch.conf
    鈫?鎺у埗"浠ヤ粈涔堥『搴忔煡"
/etc/hosts
    鈫?闈欐€佹槧灏勶紙浼樺厛绾ч珮锛?/etc/resolv.conf
    鈫?鎸囧畾 DNS 鏈嶅姟鍣紙浼樺厛绾т綆锛?DNS 鏈嶅姟鍣紙濡?8.8.8.8 鎴?127.0.0.53锛?```

### 绗竴鐜細`/etc/nsswitch.conf`

**NSS锛圢ame Service Switch锛?* 鏄?Linux 绯荤粺瑙ｆ瀽鍚嶇О锛堢敤鎴枫€佺粍銆佷富鏈哄悕绛夛級鐨勭粺涓€妗嗘灦銆傚浜庝富鏈哄悕瑙ｆ瀽锛屽畠鍐冲畾浜?鍏堟煡浠€涔堛€佸啀鏌ヤ粈涔?鐨勯『搴忋€?
```bash
$ grep hosts /etc/nsswitch.conf
hosts:          files dns
```

甯歌閰嶇疆鍙婂叾鍚箟锛?
| 閰嶇疆 | 鍚箟 |
|------|------|
| `hosts: files dns` | 鍏堟煡 `/etc/hosts`锛屾病鎵惧埌鍐嶆煡 DNS |
| `hosts: dns files` | 鍏堟煡 DNS锛屾病鎵惧埌鍐嶆煡 `/etc/hosts`锛堟瀬灏戣锛?|
| `hosts: files mdns4_minimal [NOTFOUND=return] dns` | Ubuntu 榛樿閰嶇疆锛屽厛鏌?hosts锛屽啀鏌?mDNS锛屾渶鍚庢煡 DNS |

> [!note] mDNS 鏄粈涔堬紵
> `mdns4_minimal` 鏄?**Multicast DNS**锛堥浂閰嶇疆缃戠粶鍗忚锛孉vahi 瀹炵幇锛夈€傚畠鍏佽鍚屼竴灞€鍩熺綉鍐呯殑璁惧閫氳繃 `.local` 鍩熷悕浜掔浉鍙戠幇鈥斺€旀瘮濡?`my-printer.local` 涓嶉渶瑕?DNS 鏈嶅姟鍣ㄥ氨鑳借В鏋愩€俙[NOTFOUND=return]` 鐨勬剰鎬濇槸锛氬鏋?mDNS 鏄庣‘杩斿洖"鏌ヤ笉鍒?锛堣€屼笉鏄秴鏃讹級锛屽氨涓嶅啀缁х画鏌?DNS 浜嗐€?
娴嬭瘯 NSS 瑙ｆ瀽閾捐矾鐨勫懡浠わ細

```bash
# 浣跨敤 NSS 鎺ュ彛鏌ヨ锛屼笉璧?dig/nslookup锛屽畬鏁存ā鎷熷簲鐢ㄥ眰瑙ｆ瀽琛屼负
$ getent hosts baidu.com
39.156.66.10     baidu.com
110.242.68.66    baidu.com

# 濡傛灉淇敼浜?/etc/hosts锛実etent 鑳界珛鍒诲弽鏄犻『搴忓彉鍖?# 鑰?dig 濮嬬粓鐩存帴鏌?DNS锛屼笉鍙?nsswitch.conf 褰卞搷
```

> [!warning] `getent hosts` vs `dig` 鐨勫尯鍒?> - `getent hosts`锛氳蛋 NSS 閾捐矾锛坄nsswitch.conf` 鈫?`/etc/hosts` 鈫?DNS锛夛紝**瀹屽叏妯℃嫙搴旂敤琛屼负**
> - `dig`锛氱洿鎺ュ悜 DNS 鏈嶅姟鍣ㄥ彂閫佽姹傦紝**璺宠繃 NSS 鍜?`/etc/hosts`**
> - 鎺掗殰鏃朵袱鑰呴兘瑕佺敤锛歚dig` 娴?DNS 鏈嶅姟鍣ㄦ湰韬槸鍚︽甯革紝`getent hosts` 娴嬬郴缁熻В鏋愰摼璺槸鍚︽甯?
### 绗簩鐜細`/etc/hosts`

闈欐€佷富鏈哄悕鏄犲皠鏂囦欢銆傛牸寮忛潪甯哥畝鍗曪細

```
IP鍦板潃    涓绘満鍚?[鍒悕...]
```

```bash
$ cat /etc/hosts
127.0.0.1       localhost
127.0.1.1       pop-os
192.168.1.10    nas.home
::1             localhost ip6-localhost ip6-loopback
```

> [!tip] `/etc/hosts` 鐨勮皟璇曟妧宸?> 濡傛灉鎯充复鏃?灞忚斀"鏌愪釜鍩熷悕鎸囧悜鍏剁湡瀹?IP锛屽彲浠ュ湪 hosts 涓姞鍏ワ細
> ```
> 127.0.0.1  tracking.example.com
> ```
> 杩欐牱鎵€鏈夋寚鍚?`tracking.example.com` 鐨勮姹傞兘浼氬彂鍒版湰鏈猴紙琚嫆缁濓級銆傛敼瀹屽悗绔嬪嵆鐢熸晥锛屼笉闇€瑕侀噸鍚换浣曟湇鍔°€?
### 绗笁鐜細`/etc/resolv.conf`

浼犵粺涓婅繖涓枃浠剁洿鎺ユ寚瀹?DNS 鏈嶅姟鍣ㄥ湴鍧€銆備絾鍦ㄧ幇浠?Linux 涓婏紝**瀹冨線寰€鏄竴涓鍙烽摼鎺?*锛岀敱 systemd-resolved 鎴?NetworkManager 鑷姩绠＄悊銆?
```bash
$ ls -l /etc/resolv.conf
lrwxrwxrwx 1 root root 39 ... /etc/resolv.conf -> ../run/systemd/resolve/stub-resolv.conf

$ cat /etc/resolv.conf
# 杩欐槸 systemd-resolved 绠＄悊鐨勬枃浠?nameserver 127.0.0.53
options edns0 trust-ad
search .
```

鍏抽敭瀛楁锛?
| 瀛楁 | 鍚箟 | 绀轰緥 |
|------|------|------|
| `nameserver` | DNS 鏈嶅姟鍣ㄥ湴鍧€锛堟渶澶?3 涓級 | `nameserver 8.8.8.8` |
| `search` | 鎼滅储鍩燂紝杈撳叆鐭煙鍚嶆椂鑷姩杩藉姞 | `search example.com` 璁?`ping dev` 鑷姩鏌ヨ `dev.example.com` |
| `options` | 瑙ｆ瀽閫夐」 | `ndots:5` 鎺у埗"澶氬皯涓偣鎵嶇畻瀹屾暣鍩熷悕"銆乣timeout:2` 瓒呮椂绉掓暟 |

> [!warning] 鏈€甯歌鐨?DNS 韪╁潙鐐癸細鎵嬪姩缂栬緫 `/etc/resolv.conf`
> 鍦?Ubuntu 16.04+ 涓婏紝`/etc/resolv.conf` 鏄竴涓鍙烽摼鎺ユ寚鍚?systemd-resolved 绠＄悊鐨勬枃浠躲€?*鎵嬪姩缂栬緫杩欎釜鏂囦欢浼氳 systemd-resolved 瀹氭湡瑕嗙洊**銆?>
> 姝ｇ‘鍋氭硶锛氫娇鐢?`resolvectl` 鎴栭厤缃?`/etc/systemd/resolved.conf`銆?
---

## systemd-resolved 涓?resolvectl

systemd-resolved 鏄?systemd 瀹舵棌鐨?DNS 瑙ｆ瀽鏈嶅姟銆傚畠鍦ㄧ幇浠?Linux 鍙戣鐗堬紙Ubuntu 16.04+銆丏ebian 11+銆丗edora銆丄rch Linux锛変笂骞挎硾浣跨敤锛屼絾瀹冪殑琛屼负涓庝紶缁熺殑 DNS 閰嶇疆鏂瑰紡鏈夊緢澶т笉鍚岋紝鏄?**Linux DNS 鎺掗殰涓渶澶х殑"鍧?鏉ユ簮**銆?
### Stub Resolver 鏋舵瀯

```
搴旂敤杩涚▼锛堟祻瑙堝櫒銆乧url 绛夛級
    鈫?鏌ヨ 127.0.0.53:53
systemd-resolved锛坰tub resolver锛岀洃鍚?127.0.0.53:53锛?    鈫?    鈹溾攢鈹€ 缂撳瓨鍛戒腑 鈫?鐩存帴杩斿洖
    鈹溾攢鈹€ /etc/hosts 鈫?鏌ラ潤鎬佹槧灏?    鈹斺攢鈹€ 杞彂鍒颁笂娓?DNS 鈫?8.8.8.8 / 114.114.114.114 / ...
```

systemd-resolved 鍦?`127.0.0.53` 涓婂惎鍔ㄤ竴涓湰鍦?DNS 浠ｇ悊锛岃礋璐ｏ細

1. **缂撳瓨 DNS 鏌ヨ缁撴灉**锛堝噺灏戦噸澶嶆煡璇級
2. **绠＄悊 `/etc/hosts`**锛坰tub 妯″紡锛屼絾涔熷彲閰嶇疆涓哄彧璇伙級
3. **DNSSEC 楠岃瘉**锛堝彲閫夛級
4. **姣忔帴鍙?DNS 閰嶇疆**锛堜笉鍚岀綉缁滄帴鍙ｅ彲浣跨敤涓嶅悓 DNS 鏈嶅姟鍣級
5. **mDNS 鏀寔**锛堥€氳繃 `.local` 鍩熷悕锛?
### 妯″紡閫夋嫨

systemd-resolved 鏈変笁绉嶈繍琛屾ā寮忥紝鍐冲畾浜?`/etc/resolv.conf` 鐨勫唴瀹癸細

| 妯″紡 | resolv.conf 鎸囧悜 | 鐗圭偣 |
|------|------------------|------|
| **stub**锛堥粯璁わ級 | `/run/systemd/resolve/stub-resolv.conf` | `nameserver 127.0.0.53`锛屾墍鏈夋煡璇㈢粡杩?systemd-resolved |
| **direct** | `/run/systemd/resolve/resolv.conf` | 鐩存帴濉啓涓婃父 DNS 鏈嶅姟鍣ㄥ湴鍧€锛岀粫寮€ systemd-resolved |
| **static** | 鎵嬪姩绠＄悊 `/etc/resolv.conf` | systemd-resolved 涓嶇鐞?resolv.conf |

### resolvectl 鍛戒护璇﹁В

`resolvectl` 鏄?systemd-resolved 鐨勭鐞嗗懡浠よ宸ュ叿銆?
#### 鏌ョ湅褰撳墠 DNS 閰嶇疆

```bash
$ resolvectl status
Global
       Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
resolv.conf mode: stub

Link 2 (enp0s3)
    Current Scopes: DNS
         Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 192.168.1.1    鈫?褰撳墠缃戝崱鐨?DNS 鏈嶅姟鍣?       DNS Servers: 192.168.1.1    鈫?閰嶇疆鐨勬墍鏈?DNS 鏈嶅姟鍣紙DHCP 鑾峰彇锛?        DNS Domain: home            鈫?DNS 鎼滅储鍩?```

鍏抽敭淇℃伅瑙ｈ锛?
- **Global** 閮ㄥ垎锛氬叏灞€璁剧疆锛屽崗璁惎鐢ㄧ姸鎬併€丏NSSEC 閰嶇疆
- **Link N** 閮ㄥ垎锛氭瘡涓綉缁滄帴鍙ｇ嫭绔嬬殑 DNS 閰嶇疆
- **Current DNS Server**锛氬綋鍓嶆鍦ㄤ娇鐢ㄧ殑 DNS 鏈嶅姟鍣紙鍙兘鏄涓腑鏈€蹇殑涓€涓級
- **resolv.conf mode**锛氬綋鍓?`/etc/resolv.conf` 鐨勭敓鎴愭ā寮?
#### DNS 鏌ヨ锛堟浛浠?dig 鐨勭郴缁熺骇鏌ヨ锛?
```bash
# 閫氳繃 systemd-resolved 鏌ヨ鍩熷悕
$ resolvectl query baidu.com
baidu.com: 39.156.66.10               -- link: enp0s3
           110.242.68.66              -- link: enp0s3

# 鍙嶅悜鏌ヨ
$ resolvectl query 8.8.8.8
8.8.8.8: dns.google                   -- link: enp0s3

# 鏌ョ湅鐗瑰畾鎺ュ彛鐨?DNS 閰嶇疆
$ resolvectl dns enp0s3
Link 2 (enp0s3): 192.168.1.1

# 鏌ョ湅鐗瑰畾鎺ュ彛鐨?DNS 鎼滅储鍩?$ resolvectl domain enp0s3
Link 2 (enp0s3): home
```

> [!note] `resolvectl query` vs `dig`
> - `resolvectl query` 璧?systemd-resolved 鐨勫畬鏁撮摼璺紙鍚紦瀛樺拰 `/etc/hosts`锛?> - `dig` 鐩存帴鍚戞寚瀹?DNS 鏈嶅姟鍣ㄥ彂鏌ヨ锛岀粫杩?systemd-resolved
> - 鎺掗殰鏃朵袱鑰呯殑宸紓鏈韩灏辨槸淇℃伅锛氬鏋?`dig` 姝ｅ父浣?`resolvectl query` 澶辫触锛岄棶棰樺湪 systemd-resolved 鑰屼笉鏄綉缁?
#### DNS 缂撳瓨绠＄悊

```bash
# 鏌ョ湅缂撳瓨缁熻
$ resolvectl statistics
Cache statistics:
    Current Cache Size: 78          鈫?褰撳墠缂撳瓨鏉＄洰鏁?          Cache Hits: 1243          鈫?鍛戒腑娆℃暟锛堣秺澶ц鏄庣紦瀛樻晥鏋滆秺濂斤級
        Cache Misses: 567           鈫?鏈懡涓鏁?DNSSEC verdicts:
              Secure: 0
            Insecure: 0
               Bogus: 0
       Indeterminate: 0

# 鍒锋柊 DNS 缂撳瓨锛堟帓闅滀腑鏈€甯哥敤鐨勬搷浣滀箣涓€锛?$ resolvectl flush-caches

# 楠岃瘉缂撳瓨宸叉竻绌?$ resolvectl statistics | grep "Current Cache Size"
Current Cache Size: 0
```

> [!tip] `flush-caches` 鐨勪娇鐢ㄦ椂鏈?> 褰撲綘淇敼浜?DNS 璁板綍锛堝鏇存崲浜嗙綉绔?IP锛夛紝浣嗘湰鏈轰粛鐒惰В鏋愬埌鏃?IP 鏃讹紝鍏堟墽琛?`resolvectl flush-caches` 娓呴櫎 systemd-resolved 缂撳瓨銆傚鏋滄竻闄ゅ悗杩樻槸鏃?IP锛岃鏄庨棶棰樺湪涓婄骇 DNS 鐨?TTL 缂撳瓨銆?
#### 绠＄悊姣忔帴鍙?DNS 閰嶇疆

杩欐槸 systemd-resolved 鏈€寮哄ぇ鐨勭壒鎬т箣涓€鈥斺€?*姣忎釜缃戠粶鎺ュ彛鍙互鏈夌嫭绔嬬殑 DNS 閰嶇疆**銆?
```bash
# 鏌ョ湅姣忎釜鎺ュ彛鐨?DNS 閰嶇疆
$ resolvectl status

# 鎵嬪姩璁剧疆鏌愪釜鎺ュ彛鐨?DNS锛堜复鏃讹紝閲嶅惎鍚庡け鏁堬級
$ sudo resolvectl dns enp0s3 8.8.8.8 8.8.4.4

# 璁剧疆鎼滅储鍩?$ sudo resolvectl domain enp0s3 example.com

# 姘镐箙閰嶇疆锛氬啓 /etc/systemd/resolved.conf
$ cat /etc/systemd/resolved.conf
[Resolve]
DNS=8.8.8.8 8.8.4.4
Domains=example.com
# FallbackDNS=1.1.1.1   鈫?褰撴墍鏈夋帴鍙ｆ寚瀹氱殑 DNS 閮戒笉鍙敤鏃剁殑澶囩敤
# DNSSEC=allow-downgrade

$ sudo systemctl restart systemd-resolved
```

---

## dig 鍛戒护璇﹁В

`dig`锛圖omain Information Groper锛夋槸 DNS 鏌ヨ鐨?*棣栭€夊伐鍏?*銆傚畠鐏垫椿銆佷俊鎭赴瀵屻€佸彲鑴氭湰鍖栥€備笌 `nslookup` 鐩告瘮锛宍dig` 鏇磋缁嗐€佹洿鍙帶銆?
### 鍩烘湰鏌ヨ

```bash
$ dig baidu.com

; <<>> DiG 9.18.28-0ubuntu0.22.04.1-Ubuntu <<>> baidu.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 46253
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232

;; QUESTION SECTION:
;baidu.com.                     IN      A

;; ANSWER SECTION:
baidu.com.              5       IN      A       39.156.66.10
baidu.com.              5       IN      A       110.242.68.66

;; Query time: 4 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Wed Jul 29 00:00:00 CST 2026
;; MSG SIZE  rcvd: 70
```

杈撳嚭瑙ｈ锛?
| 瀛楁 | 鍚箟 |
|------|------|
| `status: NOERROR` | 鏌ヨ鎴愬姛锛坄NXDOMAIN` 琛ㄧず鍩熷悕涓嶅瓨鍦級 |
| `flags: qr rd ra` | `qr`=鏌ヨ鍝嶅簲, `rd`=鏈熸湜閫掑綊, `ra`=鏀寔閫掑綊 |
| `QUESTION SECTION` | 鏌ョ殑鏄粈涔堬紙`baidu.com. IN A` = 鏌?baidu.com 鐨?A 璁板綍锛?|
| `ANSWER SECTION` | 杩斿洖鐨勭粨鏋?|
| `5 IN A 39.156.66.10` | TTL=5 绉? 璁板綍绫?IN(Internet), 绫诲瀷=A, 鍊?39.156.66.10 |
| `SERVER: 127.0.0.53#53` | 鍝釜 DNS 鏈嶅姟鍣ㄨ繑鍥炵殑锛堣繖閲屾樉绀?systemd-resolved 鐨?stub锛?|
| `Query time: 4 msec` | 鏌ヨ鑰楁椂 |

### +short锛氱畝鍖栬緭鍑?
褰撳彧闇€瑕?IP 鍦板潃鍒楄〃鏃讹紝`+short` 鍘婚櫎鎵€鏈夊厓淇℃伅锛?
```bash
$ dig baidu.com +short
39.156.66.10
110.242.68.66
```

瀵硅剼鏈壒鍒弸濂斤細

```bash
# 鎶婅В鏋愮粨鏋滆祴鍊肩粰鍙橀噺
IP=$(dig baidu.com +short | head -1)
echo $IP
# 杈撳嚭锛?9.156.66.10
```

### +noall +answer锛氱簿纭帶鍒惰緭鍑?
`dig` 鐨?寮€鍏?妯″紡闈炲父鐏垫椿锛屽彲浠ョ簿纭帶鍒舵樉绀哄摢浜涙钀斤細

```bash
# 鍙樉绀?ANSWER SECTION
dig baidu.com +noall +answer
baidu.com.              5       IN      A       39.156.66.10
baidu.com.              5       IN      A       110.242.68.66

# 鍙樉绀虹粺璁′俊鎭?dig baidu.com +noall +stats
```

甯哥敤寮€鍏崇粍鍚堬細

| 缁勫悎 | 鐢ㄩ€?|
|------|------|
| `+noall +answer` | 鏈€甯哥敤锛屽彧鏄剧ず绛旀 |
| `+noall +short` | 绾?IP 鍒楄〃锛岄€傚悎鑴氭湰 |
| `+noall +stats` | 鍙樉绀烘煡璇㈢粺璁?|
| `+noall +authority +additional` | DNS 鎺掗殰鏃舵煡鐪嬫潈濞佸拰闄勫姞淇℃伅 |

### @server锛氭寚瀹?DNS 鏈嶅姟鍣?
榛樿鎯呭喌涓?`dig` 浣跨敤绯荤粺閰嶇疆鐨?DNS 鏈嶅姟鍣紙`/etc/resolv.conf` 涓寚瀹氱殑锛夈€傞€氳繃 `@` 鍙互鎸囧畾浠绘剰 DNS 鏈嶅姟鍣細

```bash
# 浣跨敤 Google 鍏叡 DNS
$ dig @8.8.8.8 baidu.com +short
39.156.66.10
110.242.68.66

# 浣跨敤 Cloudflare DNS
$ dig @1.1.1.1 baidu.com +short
39.156.66.10
110.242.68.66

# 浣跨敤鍥藉唴 DNS
$ dig @114.114.114.114 baidu.com +short
39.156.66.10
110.242.68.66
```

> [!tip] 涓轰粈涔堣鎸囧畾 DNS 鏈嶅姟鍣紵
> 姣旇緝涓嶅悓 DNS 鏈嶅姟鍣ㄧ殑杩斿洖缁撴灉锛屽彲浠ュ垽鏂綘鐨?DNS 瑙ｆ瀽鍣ㄦ槸鍚﹁繑鍥炰簡姝ｇ‘鎴栨渶鏂扮殑缁撴灉銆傛瘮濡備慨鏀逛簡鍩熷悕 DNS 璁板綍鍚庯紝鐢?`dig @8.8.8.8` 涓?`dig @浣犵殑DNS` 瀵规瘮锛屽彲浠ュ垽鏂槸 DNS 鏈嶅姟鍣ㄧ紦瀛橀棶棰樿繕鏄綉缁滈棶棰樸€?
### +trace锛氳拷韪畬鏁村娲鹃摼

杩欐槸 `dig` 鏈€寮哄ぇ鐨勬帓闅滃姛鑳姐€傚畠妯℃嫙 DNS 瑙ｆ瀽鍣ㄧ殑閫掑綊鏌ヨ杩囩▼锛屼粠鏍规湇鍔″櫒寮€濮嬩竴姝ユ杩借釜锛?
```bash
$ dig baidu.com +trace
```
杈撳嚭闈炲父闀匡紝浣嗙粨鏋勬竻鏅帮細

```
.                       518336  IN      NS      a.root-servers.net.      鈫?浠庢牴寮€濮?.                       518336  IN      NS      b.root-servers.net.
.                       518336  IN      NS      ...锛?3 鍙版牴鏈嶅姟鍣級
;; Received 281 bytes from 199.7.83.42#53(l.root-servers.net) in 4 ms

com.                    172800  IN      NS      a.gtld-servers.net.     鈫?.com 椤剁骇鍩?com.                    172800  IN      NS      b.gtld-servers.net.
com.                    172800  IN      NS      ...锛?3 鍙?TLD 鏈嶅姟鍣級
;; Received 1093 bytes from 192.5.6.30#53(a.gtld-servers.net) in 26 ms

baidu.com.              172800  IN      NS      ns2.baidu.com.          鈫?baidu.com 鐨勬潈濞佹湇鍔″櫒
baidu.com.              172800  IN      NS      ns3.baidu.com.
baidu.com.              172800  IN      NS      ns4.baidu.com.
baidu.com.              172800  IN      NS      ns7.baidu.com.
baidu.com.              172800  IN      NS      dns.baidu.com.
;; Received 364 bytes from 192.42.93.30#53(g.gtld-servers.net) in 148 ms

baidu.com.              5       IN      A       39.156.66.10            鈫?鏈€缁堢殑绛旀
baidu.com.              5       IN      A       110.242.68.66
;; Received 70 bytes from 110.242.68.3#53(ns4.baidu.com) in 12 ms
```

> [!warning] `+trace` 鐨勬帓闅滀环鍊?> 濡傛灉鏌愪釜鍩熷悕瑙ｆ瀽澶辫触锛宍+trace` 鍙互绮惧噯瀹氫綅闂鍑哄湪閾炬潯鐨勫摢涓幆鑺傦細
> - 鏍规湇鍔″櫒鏌ヤ笉鍒?鈫?鍙兘鏄槻鐏闃绘柇浜?DNS 鏌ヨ锛堟鏌?53 绔彛 UDP 鍑虹珯锛?> - TLD 鏈嶅姟鍣ㄦ煡涓嶅埌 鈫?鍙兘鍩熷悕涓嶅瓨鍦?> - 鏉冨▉鏈嶅姟鍣ㄦ病鍝嶅簲 鈫?鍙兘鏄煙鍚?NS 璁板綍閰嶇疆閿欒鎴栨潈濞佹湇鍔″櫒瀹曟満
> - 鏉冨▉鏈嶅姟鍣ㄨ繑鍥炰簡閿欒鐨?IP 鈫?DNS 鍔寔

### -x锛氬弽鍚戞煡璇紙IP 鍒板煙鍚嶏級

```bash
$ dig -x 8.8.8.8 +short
dns.google.

$ dig -x 114.114.114.114 +short
public1.114dns.com.
```

鍙嶅悜鏌ヨ閫氳繃 **PTR 璁板綍**瀹炵幇銆侷SP 鍜屼簯鏈嶅姟鍟嗛€氬父浼氫负鍏綉 IP 閰嶇疆 PTR 璁板綍锛屼絾瀹跺涵瀹藉甫鍜屽緢澶?VPS 榛樿涓嶉厤缃€?
### 鎸囧畾璁板綍绫诲瀷

鏈珷鍓嶉潰宸叉紨绀鸿繃锛岃繖閲屾眹鎬绘垚琛ㄦ牸锛?
```bash
dig baidu.com A                  # A 璁板綍
dig baidu.com AAAA               # AAAA 璁板綍
dig baidu.com MX                 # MX 璁板綍
dig baidu.com NS                 # NS 璁板綍
dig baidu.com TXT                # TXT 璁板綍
dig baidu.com SOA                # SOA 璁板綍
dig baidu.com CNAME              # CNAME 璁板綍
```

### 鎵归噺鏌ヨ涓庤剼鏈簲鐢?
```bash
# 鎵归噺鏌ヨ澶氫釜鍩熷悕
for domain in baidu.com google.com github.com; do
    echo "$domain: $(dig +short $domain | head -1)"
done
# 杈撳嚭锛?# baidu.com: 39.156.66.10
# google.com: 142.250.80.46
# github.com: 140.82.121.3

# 鐩戞帶鍩熷悕 IP 鍙樺寲
watch -n 60 'dig +short baidu.com | sort'
```

### dig 甯哥敤閫夐」閫熸煡

| 閫夐」 | 浣滅敤 | 绀轰緥 |
|------|------|------|
| `+short` | 绠€鍖栬緭鍑猴紝鍙樉绀哄€?| `dig baidu.com +short` |
| `+trace` | 杩借釜閫掑綊鏌ヨ閾捐矾 | `dig baidu.com +trace` |
| `+noall +answer` | 鍙樉绀虹瓟妗堟 | `dig baidu.com +noall +answer` |
| `+noall +short` | 绾€艰緭鍑猴紝閫傚悎鑴氭湰 | `dig baidu.com +short` |
| `@server` | 鎸囧畾 DNS 鏈嶅姟鍣?| `dig @8.8.8.8 baidu.com` |
| `-x IP` | 鍙嶅悜鏌ヨ | `dig -x 8.8.8.8` |
| `+time=5` | 璁剧疆瓒呮椂绉掓暟 | `dig @8.8.8.8 baidu.com +time=5` |
| `+tries=2` | 璁剧疆閲嶈瘯娆℃暟 | `dig @8.8.8.8 baidu.com +tries=2` |

---

## nslookup 涓?host 蹇€熸煡璇?
铏界劧 `dig` 鏄閫夛紝浣?`nslookup` 鍜?`host` 涔熸湁鍚勮嚜鐨勯€傜敤鍦烘櫙銆?
### nslookup

`nslookup` 鏇剧粡鏄?DNS 鏌ヨ鐨勬爣閰嶅伐鍏凤紝浜や簰寮忓拰鍗曞懡浠ゆā寮忛兘鏀寔銆?
**鍗曞懡浠ゆā寮?*锛?
```bash
# 鍩烘湰鏌ヨ
$ nslookup baidu.com
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   baidu.com
Address: 39.156.66.10
Name:   baidu.com
Address: 110.242.68.66

# 鎸囧畾璁板綍绫诲瀷
$ nslookup -type=MX gmail.com
gmail.com       mail exchanger = 30 alt3.gmail-smtp-in.l.google.com.
gmail.com       mail exchanger = 10 alt1.gmail-smtp-in.l.google.com.
...

# 鎸囧畾 DNS 鏈嶅姟鍣?$ nslookup baidu.com 8.8.8.8
```

**浜や簰妯″紡**锛堣緭鍏?`nslookup` 鐩存帴鍥炶溅杩涘叆锛夛細

```
$ nslookup
> server 8.8.8.8          # 璁剧疆 DNS 鏈嶅姟鍣?Default server: 8.8.8.8
> set type=MX             # 璁剧疆鏌ヨ绫诲瀷
> gmail.com               # 鏌ヨ
...
> exit
```

> [!note] `nslookup` vs `dig`
> `nslookup` 鐨勪紭鍔挎槸杈撳嚭鏇寸畝娲併€佸浜烘洿鍙嬪ソ锛涘姡鍔挎槸淇℃伅閲忓皯銆佷笉鏀寔 `+trace`銆傛棩甯稿揩閫熸煡涓€涓嬬敤 `nslookup` 娌￠棶棰橈紝**娣卞害鎺掗殰鏃惰鐢?`dig`**銆?
### host

`host` 鏄笁鑰呬腑鏈€绠€娲佺殑锛岃緭鍑烘瀬鑷寸簿绠€锛岄€傚悎蹇€熸煡鐪嬶細

```bash
$ host baidu.com
baidu.com has address 39.156.66.10
baidu.com has address 110.242.68.66
baidu.com mail is handled by 10 mx.maillb.baidu.com.
baidu.com mail is handled by 20 mx1.baidu.com.
baidu.com mail is handled by 15 mx.n.shifen.com.
baidu.com mail is handled by 20 jpmx.baidu.com.

# 鎸囧畾璁板綍绫诲瀷
$ host -t MX gmail.com
gmail.com mail is handled by 30 alt3.gmail-smtp-in.l.google.com.
gmail.com mail is handled by 10 alt1.gmail-smtp-in.l.google.com.
...

# 鎸囧畾 DNS 鏈嶅姟鍣?$ host baidu.com 8.8.8.8
```

閫傜敤浜庤剼鏈腑蹇€熻幏鍙栬В鏋愮粨鏋滐細

```bash
host baidu.com 2>/dev/null | grep "has address" | awk '{print $NF}'
```

### 涓夊伐鍏峰姣?
| 宸ュ叿 | 杈撳嚭璇︾粏搴?| 浜や簰妯″紡 | `+trace` | 鑴氭湰鍙嬪ソ | 鎺ㄨ崘浣跨敤鍦烘櫙 |
|------|-----------|---------|----------|---------|------------|
| `dig` | 鏈€璇︾粏 | 涓嶆敮鎸?| 鏀寔 | 寰堝ソ | 娣卞害鎺掗殰銆佸垎鏋愩€佽剼鏈?|
| `nslookup` | 涓瓑 | 鏀寔 | 涓嶆敮鎸?| 涓€鑸?| 鏃ュ父蹇€熸煡璇?|
| `host` | 鏈€绮剧畝 | 涓嶆敮鎸?| 涓嶆敮鎸?| 鏈€濂?| 鑴氭湰銆佺畝鍗曢獙璇?|

---

## 甯歌 DNS 鎺掓煡鍦烘櫙

鍓嶉潰瀛﹀畬浜嗙悊璁虹煡璇嗗拰宸ュ叿锛岀幇鍦ㄦ潵鐪嬪嚑涓疄闄呮帓鏌ュ満鏅紝鎶婄煡璇嗕覆璧锋潵銆?
### 鍦烘櫙涓€锛?缃戠珯鎵撲笉寮€锛屾槸涓嶆槸 DNS 鐨勯棶棰橈紵"

```bash
# 绗竴姝ワ細纭鍩熷悕鑳戒笉鑳借В鏋愶紙缁曞紑 systemd-resolved锛?dig www.baidu.com +short
# 濡傛灉杩斿洖 IP 鈫?DNS 娌￠棶棰橈紝闂涓嶅湪 DNS 瑙ｆ瀽
# 濡傛灉娌℃湁杩斿洖 鈫?DNS 鍑洪棶棰樹簡锛岀户缁帓鏌?
# 绗簩姝ワ細纭鍝釜 DNS 鏈嶅姟鍣ㄥ嚭闂锛堟寚瀹氫笉鍚?DNS 瀵规瘮锛?dig @8.8.8.8 www.baidu.com +short
dig @114.114.114.114 www.baidu.com +short
# 濡傛灉鍏叡 DNS 鑳借В鏋愪絾绯荤粺閰嶇疆鐨?DNS 涓嶈兘 鈫?浣犵敤鐨?DNS 鏈嶅姟鍣ㄦ湁闂
# 濡傛灉閮戒笉鑳?鈫?鍙兘鏄綉缁滀笉閫氭垨鍩熷悕鐪熺殑涓嶅瓨鍦?
# 绗笁姝ワ細妫€鏌ョ郴缁熻В鏋愰摼璺?getent hosts www.baidu.com
# 濡傛灉 getent 澶辫触浣?dig 鎴愬姛 鈫?闂鍦?NSS 閰嶇疆鎴?systemd-resolved
# 濡傛灉 getent 鎴愬姛浣?dig 涔熸垚鍔?鈫?涓€鍒囨甯革紝闂涓嶅湪 DNS
```

### 鍦烘櫙浜岋細"鏀逛簡 DNS 璁板綍锛屼絾鏈満杩樻槸鏃?IP"

```bash
# 绗竴姝ワ細妫€鏌?systemd-resolved 缂撳瓨
resolvectl statistics
# 鐪?Cache Hits 鍜?Cache Misses 鐨勬瘮渚?
# 绗簩姝ワ細娓呯┖缂撳瓨
resolvectl flush-caches

# 绗笁姝ワ細纭娓呯┖鍚庢槸鍚﹁兘鎷垮埌鏂?IP
dig www.example.com +short

# 濡傛灉杩樻槸鏃?IP 鈫?涓婃父 DNS 鏈嶅姟鍣ㄧ紦瀛樻湭杩囨湡锛屽彧鑳界瓑 TTL
# TTL 鐢卞煙鍚嶆墍鏈夎€呰缃紝鍦?dig 缁撴灉涓彲浠ョ湅鍒帮細
dig www.example.com +noall +answer
# www.example.com.  300  IN  A  1.2.3.4
#                  ^^^ TTL=300 绉?= 5 鍒嗛挓
```

### 鍦烘櫙涓夛細"鍩熷悕瑙ｆ瀽鍒颁簡閿欒鐨?IP锛堝彲鑳借鍔寔锛?

```bash
# 鐢ㄤ笉鍚?DNS 鏈嶅姟鍣ㄥ姣?echo "Google DNS:"
dig @8.8.8.8 example.com +short

echo "Cloudflare DNS:"
dig @1.1.1.1 example.com +short

echo "绯荤粺 DNS:"
dig example.com +short

# 濡傛灉绯荤粺 DNS 杩斿洖鐨?IP 涓庡叾浠栦笉涓€鑷?鈫?鍙兘鏄?DNS 鍔寔
# 鐢?+trace 纭鏉冨▉鏈嶅姟鍣ㄨ繑鍥炵殑姝ｇ‘缁撴灉
dig @8.8.8.8 example.com +trace | grep "example.com."
```

### 鍦烘櫙鍥涳細"鍐呯綉鍩熷悕锛堢鏈夊煙鍚嶏級瑙ｆ瀽涓嶄簡"

```bash
# 妫€鏌?/etc/hosts 鏄惁鏈夐厤缃?grep internal-server /etc/hosts

# 妫€鏌?systemd-resolved 鐨勬悳绱㈠煙
resolvectl status | grep "DNS Domain"

# 妫€鏌?NSS 閰嶇疆
grep hosts /etc/nsswitch.conf

# 妫€鏌ユ槸鍚﹀惎鐢ㄤ簡 mDNS锛?local 鍩熷悕蹇呴』鐢?mDNS锛?resolvectl status | grep "mDNS"

# 灏濊瘯鐩存帴閫氳繃鏉冨▉鏈嶅姟鍣ㄦ煡璇紙濡傛灉鑳借闂殑璇濓級
dig @鍐呯綉DNS鏈嶅姟鍣↖P internal-server.internal A +short
```

### 鍦烘櫙浜旓細"ping 鍩熷悕鑳介€氾紝浣嗘祻瑙堝櫒涓嶈涓轰粈涔堬紵"

杩欏彲鑳芥槸鍥犱负锛?
1. **娴忚鍣ㄦ湁鑷繁鐨?DNS 缂撳瓨** 鈫?娓呯┖娴忚鍣?DNS 缂撳瓨锛坄chrome://net-internals/#dns`锛?2. **娴忚鍣ㄤ娇鐢?HTTPS DNS锛圖oH锛?* 鈫?鏌愪簺娴忚鍣ㄩ粯璁ゅ惎鐢?DNS over HTTPS锛岀粫杩囩郴缁?DNS
3. **CNAME 璁板綍瑙ｆ瀽闂** 鈫?娴忚鍣ㄩ渶瑕侀澶栬В鏋?CNAME 鎸囧悜鐨勭洰鏍囧煙鍚?
```bash
# 纭鍩熷悕鏄惁鏈?CNAME 璁板綍
dig example.com CNAME +noall +answer

# 濡傛灉鏈夛紝鎵嬪姩瑙ｆ瀽鐩爣鍩熷悕
dig 鐩爣鍩熷悕.com A +short

# 妫€鏌ユ槸鍚︽敮鎸?IPv6 浣?IPv6 缃戠粶鏈夐棶棰?dig example.com AAAA +short
# 濡傛灉鏈?AAAA 璁板綍杩斿洖锛屽皾璇曠鐢?IPv6 娴嬭瘯
```

---

## 鏈珷灏忕粨

- **DNS 瑙ｆ瀽娴佺▼**浠庢祻瑙堝櫒缂撳瓨寮€濮嬶紝缁忚繃鎿嶄綔绯荤粺缂撳瓨銆乣/etc/hosts`銆佹湰鍦拌В鏋愬櫒锛屾渶缁堥€氳繃閫掑綊鏌ヨ鍒拌揪鏉冨▉ DNS 鏈嶅姟鍣?- **DNS 璁板綍绫诲瀷**涓?A/AAAA 鏄渶鍩烘湰鐨勫煙鍚嶅埌 IP 鏄犲皠锛孋NAME 鐢ㄤ簬鍒悕锛孧X 鐢ㄤ簬閭欢璺敱锛孨S 鐢ㄤ簬鍩熷悕濮旀淳锛孴XT 鐢ㄤ簬楠岃瘉鍜岄偖浠跺畨鍏紝SOA 鏄尯鍩熺殑鏉冨▉鍏冩暟鎹?- **Linux DNS 閰嶇疆鏂囦欢閾捐矾**涓?`nsswitch.conf` 鈫?`/etc/hosts` 鈫?`/etc/resolv.conf`銆備娇鐢?`getent hosts` 娴嬭瘯瀹屾暣閾捐矾锛宍dig` 娴嬭瘯 DNS 鏈嶅姟鍣ㄦ湰韬?- **systemd-resolved** 鍦?`127.0.0.53` 鍚姩 stub 瑙ｆ瀽鍣紝绠＄悊缂撳瓨銆佹瘡鎺ュ彛 DNS 鍜?DNSSEC銆俙resolvectl` 鏄鐞嗗伐鍏凤紝`flush-caches` 鏄渶甯哥敤鐨勬帓闅滄搷浣?- **`dig`** 鏄?DNS 鎺掗殰鐨勯閫夊伐鍏封€斺€擿+short` 绠€鍖栬緭鍑恒€乣+trace` 杩借釜濮旀淳閾俱€乣@server` 鎸囧畾 DNS 鏈嶅姟鍣ㄣ€乣-x` 鍙嶅悜鏌ヨ銆俙nslookup` 閫傚悎蹇€熸煡璇紝`host` 閫傚悎鑴氭湰
- **DNS 缂撳瓨**鐢?systemd-resolved 绠＄悊锛岀敤 `resolvectl statistics` 鏌ョ湅鍛戒腑鎯呭喌锛宍resolvectl flush-caches` 娓呯┖缂撳瓨
- **鎺掗殰涓夋璧?*锛歚dig` 娴?DNS 鏈嶅姟鍣ㄦ湰韬?鈫?`getent hosts` 娴嬬郴缁熼摼璺?鈫?瀵规瘮涓嶅悓 DNS 鏈嶅姟鍣ㄥ垽鏂槸鍚﹁鍔寔

### 涓嬬珷棰勫憡

涓嬩竴绔犳垜浠洖鍒伴摼璺眰锛屾繁鍏?**ARP 鍗忚涓庨偦灞呭彂鐜?*銆備綘浼氬鍒?IP 鍦板潃鏄浣曢€氳繃 ARP 鍗忚杞崲涓?MAC 鍦板潃鐨勶紝浠ュ強 Linux 涓婇偦灞呰〃鐨勭姸鎬佹満锛圧EACHABLE/STALE/FAILED锛夊拰 `ip neigh` 鍛戒护鐨勫畬鏁寸敤娉曗€斺€旇繖鏄悊瑙?鍚屼竴灞€鍩熺綉鍐呬袱鍙版満鍣ㄥ浣曢€氫俊"鐨勫叧閿€?
---

*绔犺妭缂栧彿锛?5 | 璁″垝绡囧箙锛氶暱 | 瀹為檯绡囧箙锛氬疄鎴樼瑪璁帮紙姒傚康 + 鍛戒护鎿嶄綔锛?

