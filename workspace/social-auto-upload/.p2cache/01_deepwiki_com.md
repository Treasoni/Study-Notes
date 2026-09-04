---
url: "https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management"
title: "Authentication and Cookie Management | dreammis/social-auto-upload | DeepWiki"
scraped_at: 2026-09-04T16:19:36+00:00
---

Index your code with Devin
[DeepWiki](https://deepwiki.com/)
[DeepWiki](https://deepwiki.com/)
[dreammis/social-auto-upload ](https://github.com/dreammis/social-auto-upload "Open repository")
Index your code with
Devin
Edit WikiShare
Last indexed: 23 August 2026 ([1c66b7](https://github.com/dreammis/social-auto-upload/commits/1c66b7db))
  * [Social Auto Upload System Overview](https://deepwiki.com/dreammis/social-auto-upload/1-social-auto-upload-system-overview)
  * [Getting Started and Installation](https://deepwiki.com/dreammis/social-auto-upload/1.1-getting-started-and-installation)
  * [AI Agent Integration and Skills System](https://deepwiki.com/dreammis/social-auto-upload/1.2-ai-agent-integration-and-skills-system)
  * [Core Utilities and Shared Infrastructure](https://deepwiki.com/dreammis/social-auto-upload/2.1-core-utilities-and-shared-infrastructure)
  * [Tencent (WeChat Channels) Uploader](https://deepwiki.com/dreammis/social-auto-upload/5.2-tencent-\(wechat-channels\)-uploader)
  * [YouTube, Weibo, Alipay, and Hupu Uploaders](https://deepwiki.com/dreammis/social-auto-upload/5.8-youtube-weibo-alipay-and-hupu-uploaders)
  * [Authentication and Cookie Management](https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management)
  * [Platform Request Objects and Dispatch](https://deepwiki.com/dreammis/social-auto-upload/7.1-platform-request-objects-and-dispatch)
  * [Bilibili CLI and biliup Integration](https://deepwiki.com/dreammis/social-auto-upload/7.2-bilibili-cli-and-biliup-integration)
  * [Example Scripts and Usage Patterns](https://deepwiki.com/dreammis/social-auto-upload/8-example-scripts-and-usage-patterns)


# Authentication and Cookie Management
Relevant source files
  * [uploader/alipay_uploader/__init__.py](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/uploader/alipay_uploader/__init__.py)
  * [uploader/alipay_uploader/main.py](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/uploader/alipay_uploader/main.py)


## Overview
The authentication and cookie management system provides a unified interface for managing user sessions across multiple social media platforms. The system primarily uses Playwright's `storage_state` mechanism to persist authentication sessions as JSON files, enabling automated video uploads without manual login intervention. Authentication is initiated through QR code scanning, with real-time status updates delivered via Server-Sent Events (SSE) in the web UI or direct terminal output in the CLI.
The system consists of three primary components:
  * **Cookie Generation** (`myUtils/login.py`, `uploader/*/main.py`) - Handles QR code-based authentication flows.
  * **Cookie Validation** (`myUtils/auth.py`) - Verifies cookie validity by navigating to platform-specific URLs.
  * **CDP-based Extraction** (`export_douyin_cookie.sh`) - A specialized tool for extracting cookies from an existing Chrome instance via the Chrome DevTools Protocol.


Sources: [myUtils/login.py1-11](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L1-L11) [myUtils/auth.py1-14](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/auth.py#L1-L14) [export_douyin_cookie.sh1-6](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/export_douyin_cookie.sh#L1-L6)
## System Architecture
**Diagram: Authentication System Architecture**
The architecture supports both a legacy web-backend flow (using `myUtils/login.py` and `sau_backend.py`) and a modern CLI-first flow. Platform-specific type codes route requests to handlers that interact with the local filesystem and SQLite database.
Sources: [sau_backend.py358-382](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/sau_backend.py#L358-L382) [myUtils/auth.py105-121](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/auth.py#L105-L121) [myUtils/login.py30-91](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L30-L91) [uploader/alipay_uploader/main.py136-180](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/uploader/alipay_uploader/main.py#L136-L180)
## QR Code Login Flow
The system uses QR code-based authentication. In the web interface, base64-encoded QR images are streamed via SSE. In the CLI, QR codes are printed directly to the terminal using the `segno` library.
**Diagram: SSE-Based QR Code Authentication Flow**
### QR Code Utilities (`utils/login_qrcode.py`)
Common QR code operations are abstracted in `utils/login_qrcode.py`:
  * `save_data_url_image`: Converts base64 data URLs to PNG files [utils/login_qrcode.py18-28](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/utils/login_qrcode.py#L18-L28)
  * `decode_qrcode_from_path`: Uses OpenCV (`cv2.QRCodeDetector`) to extract the text content from a QR image [utils/login_qrcode.py38-54](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/utils/login_qrcode.py#L38-L54)
  * `print_terminal_qrcode`: Uses `segno` to print the QR code in the terminal. It attempts a compact Unicode display but falls back to ASCII if the terminal environment is incompatible [utils/login_qrcode.py70-89](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/utils/login_qrcode.py#L70-L89)


Sources: [utils/login_qrcode.py1-89](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/utils/login_qrcode.py#L1-L89) [myUtils/login.py47-54](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L47-L54) [sau_backend.py358-382](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/sau_backend.py#L358-L382)
## Cookie Generation and Storage
### Platform Generators (`myUtils/login.py`)
Generators follow a standard lifecycle:
  1. **Launch** : Launch Chromium with options from `get_browser_options()` (handles `LOCAL_CHROME_PATH` and `LOCAL_CHROME_HEADLESS`) [myUtils/login.py13-27](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L13-L27)
  2. **Stealth** : Apply `set_init_script` to evade bot detection [myUtils/login.py42](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L42-L42)
  3. **Capture** : Extract the login QR code and push to `status_queue` for the SSE backend [myUtils/login.py47-51](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L47-L51)
  4. **Monitor** : Use `page.on('framenavigated', ...)` to detect when the user has successfully logged in and the page redirects [myUtils/login.py52-58](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L52-L58)
  5. **Persist** : Save `context.storage_state` to `cookiesFile/{uuid}.json` [myUtils/login.py66-71](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L66-L71)
  6. **Register** : Insert the record into the `user_info` table in `database.db` [myUtils/login.py82-89](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L82-L89)


### CDP-Based Extraction (`export_douyin_cookie.sh`)
For environments where automated login is blocked (e.g., high-risk IP), the `export_douyin_cookie.sh` tool allows manual extraction:
  * It connects to a running Chrome instance via the Remote Debugging Port (9222) [export_douyin_cookie.sh37-43](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/export_douyin_cookie.sh#L37-L43)
  * It uses a Python script with `websocket-client` to call `Network.getAllCookies` [export_douyin_cookie.sh96-99](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/export_douyin_cookie.sh#L96-L99)
  * It evaluates JavaScript in the browser context to extract `localStorage` data for relevant origins (`douyin.com`, `bytedance.com`) [export_douyin_cookie.sh128-175](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/export_douyin_cookie.sh#L128-L175)
  * The resulting JSON is compatible with the system's uploader requirements [export_douyin_cookie.sh180-208](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/export_douyin_cookie.sh#L180-L208)


Sources: [myUtils/login.py30-91](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L30-L91) [export_douyin_cookie.sh1-233](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/export_douyin_cookie.sh#L1-L233)
## Cookie Validation (`myUtils/auth.py`)
Validation ensures that a stored session is still active before attempting an upload.  
| Function  | Platform  | Validation Logic  |  
| --- | --- | --- |  
| `cookie_auth_douyin`  | Douyin  | Navigates to upload page; checks if "扫码登录" (Scan to Login) text is present [myUtils/auth.py15-40](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/auth.py#L15-L40)  |  
| `cookie_auth_tencent`  | Tencent  | Navigates to post creation; checks for "微信小店" selector [myUtils/auth.py43-58](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/auth.py#L43-L58)  |  
| `cookie_auth_ks`  | Kuaishou  | Navigates to publish page; checks for "机构服务" selector [myUtils/auth.py61-77](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/auth.py#L61-L77)  |  
| `cookie_auth_xhs`  | XHS  | Navigates to upload page; checks for "手机号登录" or "扫码登录" text [myUtils/auth.py80-102](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/auth.py#L80-L102)  |  
Sources: [myUtils/auth.py15-103](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/auth.py#L15-L103)
## Multi-Platform Storage Strategy
The system uses two primary locations for cookie storage:
  1. **`cookiesFile/`**: Used by the legacy backend and`myUtils/login.py`. Files are typically named with UUIDs [myUtils/login.py69-71](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L69-L71)
  2. **`cookies/[platform_name]/`**: Used by the modern CLI and specific uploader classes (e.g.,`AlipayVideo`). Files are typically named `account.json` or `douyin_{account}.json` [uploader/alipay_uploader/main.py65-68](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/uploader/alipay_uploader/main.py#L65-L68) [export_douyin_cookie.sh60-62](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/export_douyin_cookie.sh#L60-L62)


The `sau_cli.py` utility `resolve_account_file()` (referenced in docs) bridges these locations by checking both absolute paths and platform-specific subdirectories.
Sources: [uploader/alipay_uploader/main.py60-69](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/uploader/alipay_uploader/main.py#L60-L69) [myUtils/login.py69-71](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/myUtils/login.py#L69-L71) [export_douyin_cookie.sh59-62](https://github.com/dreammis/social-auto-upload/blob/1c66b7db/export_douyin_cookie.sh#L59-L62)
Dismiss
Refresh this wiki
Enter email to refresh
### On this page
  * [Authentication and Cookie Management](https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management#authentication-and-cookie-management)
  * [QR Code Utilities (`utils/login_qrcode.py`)](https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management#qr-code-utilities-utilslogin_qrcodepy)
  * [Cookie Generation and Storage](https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management#cookie-generation-and-storage)
  * [Platform Generators (`myUtils/login.py`)](https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management#platform-generators-myutilsloginpy)
  * [CDP-Based Extraction (`export_douyin_cookie.sh`)](https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management#cdp-based-extraction-export_douyin_cookiesh)
  * [Cookie Validation (`myUtils/auth.py`)](https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management#cookie-validation-myutilsauthpy)
  * [Multi-Platform Storage Strategy](https://deepwiki.com/dreammis/social-auto-upload/6-authentication-and-cookie-management#multi-platform-storage-strategy)


