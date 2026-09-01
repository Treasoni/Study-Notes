---
url: "https://curl.se/libcurl/c/libcurl-env.html"
title: "libcurl - environment variables"
scraped_at: 2026-08-29T08:38:46+00:00
---

[curl](https://curl.se/) / [libcurl](https://curl.se/libcurl/) / [API](https://curl.se/libcurl/c/) / **Environment variables**
#  Environment variables libcurl understands 
**Related:** [All functions](https://curl.se/libcurl/c/allfuncs.html) [Errors](https://curl.se/libcurl/c/libcurl-errors.html) [Examples](https://curl.se/libcurl/c/example.html) [Symbols](https://curl.se/libcurl/c/symbols-in-versions.html)
## Name
libcurl-env - environment variables libcurl understands 
## Description
libcurl reads and understands a set of environment variables that if set controls and changes behaviors. This is the full list of variables to set and description of what they do. Also note that curl, the command line tool, supports a set of additional environment variables independently of this. 
[scheme]_proxy
When libcurl is given a URL to use in a transfer, it first extracts the scheme part from the URL and checks if there is a given proxy set for that in its corresponding environment variable. A URL like <https://example.com> makes libcurl use the http_proxy variable, while a URL like <ftp://example.com> uses the ftp_proxy variable. 
These proxy variables are also checked for in their uppercase versions, except the http_proxy one which is only used lowercase. Note also that some systems (like Windows) have a case insensitive handling of environment variables and then of course HTTP_PROXY still works. 
An exception exists for the WebSocket ws and wss URL schemes, where libcurl first checks ws_proxy or wss_proxy but if they are not set, it falls back and tries the http and https versions instead if set. 
ALL_PROXY
This is a setting to set proxy for all URLs, independently of what scheme is being used. Note that the scheme specific variables overrides this one if set. 
CURL_SSL_BACKEND
When libcurl is built to support multiple SSL backends, it selects a specific backend at first use. If no selection is done by the program using libcurl, this variable's selection is used. Setting a name that is not a built-in alternative makes libcurl stay with the default. 
SSL backend names (case-insensitive): GnuTLS, mbedTLS, OpenSSL, Rustls, Schannel, wolfSSL 
HOME
When the netrc feature is used ([CURLOPT_NETRC](https://curl.se/libcurl/c/CURLOPT_NETRC.html)), this variable is checked as the primary way to find the "current" home directory in which the .netrc file is likely to exist. 
USERPROFILE
When the netrc feature is used ([CURLOPT_NETRC](https://curl.se/libcurl/c/CURLOPT_NETRC.html)), this variable is checked as the secondary way to find the "current" home directory (on Windows only) in which the .netrc file is likely to exist. 
NETRC
The filename used as netrc file when [CURLOPT_NETRC](https://curl.se/libcurl/c/CURLOPT_NETRC.html) is used without [CURLOPT_NETRC_FILE](https://curl.se/libcurl/c/CURLOPT_NETRC_FILE.html). (Added in [8.16.0](https://curl.se/ch/8.16.0.html)) 
NO_PROXY
This has the same functionality as the [CURLOPT_NOPROXY](https://curl.se/libcurl/c/CURLOPT_NOPROXY.html) option: it gives libcurl a comma-separated list of hostname patterns for which libcurl should not use a proxy. 
SSLKEYLOGFILE
When set and libcurl runs with an SSL backend that supports this feature, libcurl saves SSL secrets into the given filename. Using those SSL secrets, other tools (such as Wireshark) can decrypt the SSL communication and analyze/view the traffic. 
These secrets and this file might be sensitive. Users are advised to take precautions so that they are not stolen or otherwise inadvertently revealed. 
## Debug variables
Debug variables are intended for internal use and are documented in [libcurl-env-dbg](https://curl.se/libcurl/c/libcurl-env-dbg.html). 
## See also
[libcurl-env-dbg](https://curl.se/libcurl/c/libcurl-env-dbg.html)(3) 
This HTML page was made with [roffit](https://daniel.haxx.se/projects/roffit/). 
