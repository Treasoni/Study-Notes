---
url: "https://github.com/openai/codex"
title: "GitHub - openai/codex: Lightweight coding agent that runs in your terminal · GitHub"
scraped_at: 2026-09-04T11:41:00+00:00
---

[Skip to content](https://github.com/openai/codex#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/openai/codex) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/openai/codex) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/openai/codex) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/openai/codex).
/ Public
  * [ Notifications ](https://github.com/login?return_to=%2Fopenai%2Fcodex) You must be signed in to change notification settings
  * [ Fork 18.6k ](https://github.com/login?return_to=%2Fopenai%2Fcodex)
  * [ Star  121k ](https://github.com/login?return_to=%2Fopenai%2Fcodex)


[**4643** Branches](https://github.com/openai/codex/branches)[**1295** Tags](https://github.com/openai/codex/tags)
Go to file
Open more actions menu
## Latest commit
and
copyberry
[Gate unified exec TTY support behind a feature flag (](https://github.com/openai/codex/commit/3c837e568c24e4281bba4abdf3bc3c398f3fff13)[#42718](https://github.com/openai/codex/pull/42718)[)](https://github.com/openai/codex/commit/3c837e568c24e4281bba4abdf3bc3c398f3fff13)
Open commit detailsfailure
Sep 4, 2026
[3c837e5](https://github.com/openai/codex/commit/3c837e568c24e4281bba4abdf3bc3c398f3fff13) · Sep 4, 2026
## History
[10,245 Commits](https://github.com/openai/codex/commits/main/)
Open commit details
10,245 Commits
## Folders and files  
| Name  | Name  | Last commit message  | Last commit date  |  
| --- | --- | --- | --- |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
 |  
|   |   |  
|   |   |  
 |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
| [.markdownlint-cli2.yaml](https://github.com/openai/codex/blob/main/.markdownlint-cli2.yaml ".markdownlint-cli2.yaml")  | [.markdownlint-cli2.yaml](https://github.com/openai/codex/blob/main/.markdownlint-cli2.yaml ".markdownlint-cli2.yaml")  |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
| [workspace_root_test_launcher.bat.tpl](https://github.com/openai/codex/blob/main/workspace_root_test_launcher.bat.tpl "workspace_root_test_launcher.bat.tpl")  | [workspace_root_test_launcher.bat.tpl](https://github.com/openai/codex/blob/main/workspace_root_test_launcher.bat.tpl "workspace_root_test_launcher.bat.tpl")  |  
| [workspace_root_test_launcher.sh.tpl](https://github.com/openai/codex/blob/main/workspace_root_test_launcher.sh.tpl "workspace_root_test_launcher.sh.tpl")  | [workspace_root_test_launcher.sh.tpl](https://github.com/openai/codex/blob/main/workspace_root_test_launcher.sh.tpl "workspace_root_test_launcher.sh.tpl")  |  
| View all files |  
## Repository files navigation
**Codex CLI** is a coding agent from OpenAI that runs locally on your computer. 
If you want Codex in your code editor (VS Code, Cursor, Windsurf), [install in your IDE.](https://developers.openai.com/codex/ide) If you want the desktop app experience, run `codex app` or visit [the Codex App page](https://chatgpt.com/codex?app-landing-page=true). If you are looking for the _cloud-based agent_ from OpenAI, **Codex Web** , go to [chatgpt.com/codex](https://chatgpt.com/codex). 
## Quickstart
### Installing and running Codex CLI
Run the following on Mac or Linux to install Codex CLI:

```
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Run the following on Windows to install Codex CLI:

```
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

The standalone installers download from `https://releases.openai.com/codex` by default and fall back to GitHub Releases if a metadata or asset download is unavailable. To force GitHub Releases, set `CODEX_INSTALLER_USE_RELEASES_OPENAI_COM` to `false` (`0` and `no` are also accepted):

```
curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_INSTALLER_USE_RELEASES_OPENAI_COM=false sh
```


```
$env:CODEX_INSTALLER_USE_RELEASES_OPENAI_COM='false'; irm https://chatgpt.com/codex/install.ps1 | iex
```

Codex CLI can also be installed via the following package managers:

```
# Install using npm
npm install -g @openai/codex
```


```
# Install using Homebrew
brew install --cask codex
```

Then simply run `codex` to get started.
You can also go to the [latest GitHub Release](https://github.com/openai/codex/releases/latest) and download the appropriate binary for your platform.
Each GitHub Release contains many executables, but in practice, you likely want one of these:
  * macOS 
    * Apple Silicon/arm64: `codex-aarch64-apple-darwin.tar.gz`
    * x86_64 (older Mac hardware): `codex-x86_64-apple-darwin.tar.gz`
  * Linux 
    * x86_64: `codex-x86_64-unknown-linux-musl.tar.gz`
    * arm64: `codex-aarch64-unknown-linux-musl.tar.gz`


Each archive contains a single entry with the platform baked into the name (e.g., `codex-x86_64-unknown-linux-musl`), so you likely want to rename it to `codex` after extracting it.
### Using Codex with your ChatGPT plan
Run `codex` and select **Sign in with ChatGPT**. We recommend signing into your ChatGPT account to use Codex as part of your Plus, Pro, Business, Edu, or Enterprise plan. [Learn more about what's included in your ChatGPT plan](https://help.openai.com/en/articles/11369540-codex-in-chatgpt).
You can also use Codex with an API key, but this requires [additional setup](https://developers.openai.com/codex/auth#sign-in-with-an-api-key).
  * [**Codex Documentation**](https://developers.openai.com/codex)
  * [**Installing & building**](https://github.com/openai/codex/blob/main/docs/install.md)


This repository is licensed under the [Apache-2.0 License](https://github.com/openai/codex/blob/main/LICENSE).
## About
Lightweight coding agent that runs in your terminal
### Resources
### Contributing
### Security policy
### Stars
**121.4k** stars
### Watchers
**623** watching
### Forks
[**18.6k** forks](https://github.com/openai/codex/forks)
## Releases
## Packages
## Used by
## Contributors
## Languages
You can’t perform that action at this time. 
