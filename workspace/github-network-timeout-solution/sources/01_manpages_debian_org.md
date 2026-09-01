---
url: "https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html"
title: "libcurl-env(3) — libcurl4-doc — Debian experimental — Debian Manpages"
scraped_at: 2026-08-29T08:28:03+00:00
---

[MANPAGES](https://manpages.debian.org/)
[Skip Quicknav](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html#content)
  * [About Manpages](https://manpages.debian.org/about.html)
  * [Service Information](https://wiki.debian.org/manpages.debian.org)


/ [experimental](https://manpages.debian.org/contents-experimental.html) / [libcurl4-doc](https://manpages.debian.org/experimental/libcurl4-doc/index.html) / libcurl-env(3) 
links 
  * [language-indep link](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3)


table of contents 


other versions 
  * [trixie](https://manpages.debian.org/trixie/libcurl4-doc/libcurl-env.3.en.html) 8.14.1-2+deb13u4
  * [trixie-backports](https://manpages.debian.org/trixie-backports/libcurl4-doc/libcurl-env.3.en.html) 8.21.0-2~bpo13+1
  * [testing](https://manpages.debian.org/testing/libcurl4-doc/libcurl-env.3.en.html) 8.21.0-2
  * [unstable](https://manpages.debian.org/unstable/libcurl4-doc/libcurl-env.3.en.html) 8.22.0~rc3-1
  * [experimental](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html) 8.22.0~rc3-1+exp1


[Scroll to navigation](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html#panels)  
| Library Functions Manual  |  
| --- |  
# NAME[¶](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html#NAME)
libcurl-env - environment variables libcurl understands
# DESCRIPTION[¶](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html#DESCRIPTION)
libcurl reads and understands a set of environment variables that if set controls and changes behaviors. This is the full list of variables to set and description of what they do. Also note that curl, the command line tool, supports a set of additional environment variables independently of this. 

[scheme]_proxy
    When libcurl is given a URL to use in a transfer, it first extracts the scheme part from the URL and checks if there is a given proxy set for that in its corresponding environment variable. A URL like <https://example.com> makes libcurl use the **http_proxy** variable, while a URL like <ftp://example.com> uses the **ftp_proxy** variable. 
These proxy variables are also checked for in their uppercase versions, except the **http_proxy** one which is only used lowercase. Note also that some systems (like Windows) have a case insensitive handling of environment variables and then of course **HTTP_PROXY** still works.
An exception exists for the WebSocket **ws** and **wss** URL schemes, where libcurl first checks **ws_proxy** or **wss_proxy** but if they are not set, it falls back and tries the http and https versions instead if set.     This is a setting to set proxy for all URLs, independently of what scheme is being used. Note that the scheme specific variables overrides this one if set. 

[CURL_SSL_BACKEND](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html#CURL_SSL_BACKEND)
    When libcurl is built to support multiple SSL backends, it selects a specific backend at first use. If no selection is done by the program using libcurl, this variable's selection is used. Setting a name that is not a built-in alternative makes libcurl stay with the default. 
SSL backend names (case-insensitive): GnuTLS, mbedTLS, OpenSSL, Rustls, Schannel, wolfSSL     When the netrc feature is used (), this variable is checked as the primary way to find the "current" home directory in which the .netrc file is likely to exist.     When the netrc feature is used (), this variable is checked as the secondary way to find the "current" home directory (on Windows only) in which the .netrc file is likely to exist.     The filename used as netrc file when is used without _[CURLOPT_NETRC_FILE(3)](https://manpages.debian.org/experimental/libcurl4-doc/CURLOPT_NETRC_FILE.3.en.html)_. (Added in 8.16.0)     This has the same functionality as the option: it gives libcurl a comma-separated list of hostname patterns for which libcurl should not use a proxy.     When set and libcurl runs with an SSL backend that supports this feature, libcurl saves SSL secrets into the given filename. Using those SSL secrets, other tools (such as Wireshark) can decrypt the SSL communication and analyze/view the traffic. 
These secrets and this file might be sensitive. Users are advised to take precautions so that they are not stolen or otherwise inadvertently revealed.
# Debug Variables[¶](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html#Debug_Variables)
Debug variables are intended for internal use and are documented in .
# SEE ALSO[¶](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html#SEE_ALSO)
[libcurl-env-dbg(3)](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env-dbg.3.en.html)  
| 2026-08-27  | libcurl  |  
| --- | --- |  
|  Source file:   |  libcurl-env.3.en.gz (from [libcurl4-doc 8.22.0~rc3-1+exp1](http://snapshot.debian.org/package/curl/8.22.0~rc3-1+exp1/))   |  
| --- | --- |  
|  Source last updated:   |  2026-08-27T03:12:07Z   |  
|  Converted to HTML:   |  2026-08-27T08:49:15Z   |  
debiman df2f1b6, see [github.com/Debian/debiman](https://github.com/Debian/debiman/). Found a problem? See the [FAQ](https://manpages.debian.org/faq.html).
