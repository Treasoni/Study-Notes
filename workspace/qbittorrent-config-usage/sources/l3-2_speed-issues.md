---
url: "https://github.com/qbittorrent/qBittorrent/wiki/Things-we-need-to-know-to-help-you-with-%27speed%27-issues"
title: "Things we need to know to help you with 'speed' issues · qbittorrent/qBittorrent Wiki · GitHub"
scraped_at: 2026-10-07T14:41:18+00:00
---

[Skip to content](https://github.com/qbittorrent/qBittorrent/wiki/Things-we-need-to-know-to-help-you-with-%27speed%27-issues#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/qbittorrent/qBittorrent/wiki/Things-we-need-to-know-to-help-you-with-%27speed%27-issues) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/qbittorrent/qBittorrent/wiki/Things-we-need-to-know-to-help-you-with-%27speed%27-issues) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/qbittorrent/qBittorrent/wiki/Things-we-need-to-know-to-help-you-with-%27speed%27-issues) to refresh your session. Dismiss alert
# Things we need to know to help you with 'speed' issues
Chocobo1 edited this page Sep 3, 2026 · [8 revisions](https://github.com/qbittorrent/qBittorrent/wiki/Things-we-need-to-know-to-help-you-with-'speed'-issues/_history)
# Do You Have Speed Problems?
If so, please do not ask for assistance here, go to the [Official qBittorrent support forum](http://forum.qbittorrent.org) and provide the answers to the following:
## Connection Speed
What your ISP has sold you is irrelevant, to calculate a starting place for settings requires a real time check of bandwidth/speed capability.
### Instructions
Turn off any and all BitTorrent clients that are running, open [Speedtest.net](http://www.speedtest.net) in a browser, run the test(s), then provide a screen shot of the results in your post.
## Version and Operating System
This is essential. Also before asking, please ensure that you are using the latest release for your OS. See the [news page](https://www.qbittorrent.org/news.php) first, as we do not support older versions of qBittorrent.
## qBittorrent Settings Information
  * Connections: Global maximum and per torrent
  * Listening port
  * Upload slots: Global maximum and per torrent
  * Half-open connection value
  * Is uTP on or off?
  * Rate limiting uTP?
  * Encryption on or off?
  * IPv6 on or off?
  * libtorrent version (use Help -> About -> Libraries to identify that)
  * Connection status? (the icon on the status bar will tell you)
  * DHT node count (on the status bar)
  * Are you using a proxy or a VPN?


## What type of user profile are you?
  * Do you seed more than download? or vice versa?
  * How many tasks do you expect to run on average?
  * Do you use the machine for other tasks simultaneous with BitTorrent downloads?
  * Are there other users on the LAN?


If a specific loaded task is a problem, please provide:
  * The status of the task.
  * Seed and Peer counts in bracketed form x(n)... The number in the bracket is possible, the number outside is actual.
  * Tracker status information.


If providing screen shots for any of the above, **please** hide the name column or obfuscate the name and/or hash id of the task along with 'access keys' in 'private' tracker URIs
Please note: We **DO NOT** need or want metadata file (.torrent) URIs or magnet links to downloadable content that is **NOT** open source or public domain material. Failure to comply with this will result in a warning and/or account removal.
[Go back to home](https://github.com/qbittorrent/qBittorrent/wiki)
## General
  * [Installing qBittorrent](https://github.com/qbittorrent/qBittorrent/wiki/Installing-qBittorrent)
  * [Frequently Asked Questions (FAQ)](https://github.com/qbittorrent/qBittorrent/wiki/Frequently-Asked-Questions)
  * [qBittorrent options (current and deprecated)](https://github.com/qbittorrent/qBittorrent/wiki/Explanation-of-Options-in-qBittorrent)
  * [How to use qBittorrent as a tracker](https://github.com/qbittorrent/qBittorrent/wiki/How-to-use-qBittorrent-as-a-tracker)
  * [How to use portable mode](https://github.com/qbittorrent/qBittorrent/wiki/How-to-use-portable-mode)
  * [How to bind your vpn to prevent ip leaks](https://github.com/qbittorrent/qBittorrent/wiki/How-to-bind-your-vpn-to-prevent-ip-leaks)


### Troubleshooting
  * [qBittorrent support forum](http://forum.qbittorrent.org/)
  * [I forgot my GUI lock password](https://github.com/qbittorrent/qBittorrent/wiki/I-forgot-my-UI-lock-password)
  * [I forgot my WebUI password](https://github.com/qbittorrent/qBittorrent/wiki/Web-UI-password-locked-on-qBittorrent-NO-X-%28qbittorrent-nox%29)


### External programs


### Search plugins
  * [List of unofficial search plugins](https://github.com/qbittorrent/search-plugins/wiki/Unofficial-search-plugins)


### Themes
  * [Developing custom UI themes](https://github.com/qbittorrent/qBittorrent/wiki/Create-custom-themes-for-qBittorrent)
  * [How to use custom UI themes](https://github.com/qbittorrent/qBittorrent/wiki/How-to-use-custom-UI-themes)
  * [List of unofficial themes](https://github.com/qbittorrent/qBittorrent/wiki/List-of-known-qBittorrent-themes)


### Translation
  * [How to translate qBittorrent](https://github.com/qbittorrent/qBittorrent/wiki/How-to-translate-qBittorrent)


## WebUI
### WebUI API  
| State  | Version  |  
| --- | --- |  
| qBittorrent >= 5.0  |  
| qBittorrent v4.1.0 - v4.6.x  |  
| qBittorrent v3.2.0 - v4.0.x  |  
| qBittorrent < v3.2.0  |  
### Authentication


### WebAPI clients
  * [List of unofficial WebAPI clients](https://github.com/qbittorrent/qBittorrent/wiki/List-of-unofficial-WebAPI-clients)


### Alternate WebUI
  * [Alternate WebUI usage](https://github.com/qbittorrent/qBittorrent/wiki/Alternate-WebUI-usage)
  * [Developing alternate WebUIs](https://github.com/qbittorrent/qBittorrent/wiki/Developing-alternate-WebUIs-\(WIP\))
  * [List of unofficial alternate WebUIs](https://github.com/qbittorrent/qBittorrent/wiki/List-of-known-alternate-WebUIs)


### Reverse proxy setup for WebUI access


### WebUI HTTPS configuration
  * [Let's Encrypt Certificates + Caddy2 Reverse Proxy](https://github.com/qbittorrent/qBittorrent/wiki/Linux-WebUI-HTTPS-with-Let's-Encrypt-&-Caddy2-reverse-proxy)
  * [Let's Encrypt certificates + NGINX reverse proxy - Linux](https://github.com/qbittorrent/qBittorrent/wiki/Linux-WebUI-HTTPS-with-Let's-Encrypt-certificates-and-NGINX-SSL-reverse-proxy)
  * [Let's Encrypt certificates - Linux](https://github.com/qbittorrent/qBittorrent/wiki/Linux-WebUI-setting-up-HTTPS-with-Let's-Encrypt-certificates)
  * [Self-signed SSL certificates - Linux](https://github.com/qbittorrent/qBittorrent/wiki/Linux-WebUI-setting-up-HTTPS-with-self-signed-SSL-certificates)


## Linux
  * [Running qBittorrent without X server (WebUI only)](https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-\(WebUI-only\))
  * [Running qBittorrent without X server (WebUI only, systemd service set up, Ubuntu 15.04 or newer)](https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-\(WebUI-only,-systemd-service-set-up,-Ubuntu-15.04-or-newer\))
  * [OpenVPN and qBittorrent without X server](https://github.com/qbittorrent/qBittorrent/wiki/OpenVPN-and-qBittorrent-without-X-server)


## Development
  * [How to write a search plugin](https://github.com/qbittorrent/search-plugins/wiki/How-to-write-a-search-plugin)
  * [Using VSCode for qBittorrent development](https://github.com/qbittorrent/qBittorrent/wiki/Using-VSCode-for-qBittorrent-development)
  * [Setup GDB with Qt pretty printers](https://github.com/qbittorrent/qBittorrent/wiki/Setup-GDB-with-Qt-pretty-printers)
  * [How to debug WebUI code](https://github.com/qbittorrent/qBittorrent/wiki/How-to-debug-the-WebUI-code)


### Compilation
[Common information for CMake](https://github.com/qbittorrent/qBittorrent/wiki/Compilation-with-CMake-common-information)
#### *BSD, Linux
  * [Debian / Ubuntu and derivatives (CMake)](https://github.com/qbittorrent/qBittorrent/wiki/Compilation-Debian,-Ubuntu,-and-derivatives)
  * [Debian / Ubuntu and derivatives (autotools/qmake)](https://github.com/qbittorrent/qBittorrent/wiki/Compilation-Debian-and-Ubuntu)
  * [Fully static binaries on Linux (glibc or musl)](https://github.com/qbittorrent/qBittorrent/wiki/Compilation-Fully-static-binaries-on-Linux-\(glibc-or-musl\))
  * [Raspberry Pi OS / DietPi](https://github.com/qbittorrent/qBittorrent/wiki/Compilation-Raspberry-Pi-OS-and-DietPi)
  * [Raspbian for LeMaker Banana Pro](https://github.com/qbittorrent/qBittorrent/wiki/Compilation-Raspbian-for-LeMaker-Banana-Pro)


#### macOS
  * [cmake (x86_64, arm64, cross-compilation, static linkage)](https://github.com/qbittorrent/qBittorrent/wiki/Compilation-macOS-\(x86_64,-arm64,-cross-compilation\))


#### Windows
  * [MSVC 2019 (CMake, static linkage)](https://github.com/qbittorrent/qBittorrent/wiki/Compilation-Windows-\(MSVC-2019,-64-bit,-static-linkage\))
  * [MSVC 2019 (qmake, static linkage)](https://github.com/qbittorrent/qBittorrent/wiki/Compiling-with-MSVC-2019-\(static-linkage\))


[Obsolete compilation guides](https://github.com/qbittorrent/qBittorrent/wiki/Obsolete-compilation-guides)
### Clone this wiki locally
You can’t perform that action at this time. 
