---
url: "https://github.com/abhigyanpatwari/GitNexus/issues/1811"
title: "Encoding Failure in Windows PowerShell with Chinese Directory Paths · Issue #1811 · abhigyanpatwari/GitNexus · GitHub"
scraped_at: 2026-09-10T15:43:20+00:00
---

[Skip to content](https://github.com/abhigyanpatwari/GitNexus/issues/1811#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/abhigyanpatwari/GitNexus/issues/1811) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/abhigyanpatwari/GitNexus/issues/1811) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/abhigyanpatwari/GitNexus/issues/1811) to refresh your session. Dismiss alert
/ Public
  * ###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/abhigyanpatwari/GitNexus/issues/1811).
  * [ Notifications ](https://github.com/login?return_to=%2Fabhigyanpatwari%2FGitNexus) You must be signed in to change notification settings
  * [ Fork 5.2k ](https://github.com/login?return_to=%2Fabhigyanpatwari%2FGitNexus)
  * [ Star  47.2k ](https://github.com/login?return_to=%2Fabhigyanpatwari%2FGitNexus)


#  Encoding Failure in Windows PowerShell with Chinese Directory Paths
New issue
Copy link
New issue
Copy link
Closed
Closed
[Encoding Failure in Windows PowerShell with Chinese Directory Paths](https://github.com/abhigyanpatwari/GitNexus/issues/1811#top)#1811
Copy link
Labels
[Something isn't working](https://github.com/abhigyanpatwari/GitNexus/issues?q=state%3Aopen%20label%3A%22bug%22)Something isn't working
## Description
opened [on May 25, 2026](https://github.com/abhigyanpatwari/GitNexus/issues/1811#issue-4514080816)
Issue body actions
### Area
gitnexus (CLI / core / indexing / MCP server)
### Summary
PowerShell Fails to Resolve Directory Paths Containing Chinese Characters Due to Encoding Mismatch
### Context
_No response_
### Expected behavior
running sucessful
### Actual behavior
Analysis failed: COPY failed for File: IO exception: Cannot open file. path: C:\Project\XXXX\code.gitnexus\lbug - Error 3: The system cannot find the path specified. Error: COPY failed for File: IO exception: Cannot open file. path: C:\Project\XXXX\code.gitnexus\lbug - Error 3: The system cannot find the path specified. at loadGraphToLbug (file:///C:/Users/yisen/AppData/Roaming/npm/node_modules/gitnexus/dist/core/lbug/lbug-adapter.js:557:23) at process.processTicksAndRejections (node:internal/process/task_queues:104:5) at async runFullAnalysis (file:///C:/Users/yisen/AppData/Roaming/npm/node_modules/gitnexus/dist/core/run-analyze.js:415:13) at async analyzeCommand (file:///C:/Users/yisen/AppData/Roaming/npm/node_modules/gitnexus/dist/cli/analyze.js:314:24) at async Command. (file:///C:/Users/yisen/AppData/Roaming/npm/node_modules/gitnexus/dist/cli/lazy-action.js:16:9)
### Steps to reproduce
npx gitnexus analyze
### Environment
windows 11 powershell
### Logs / screenshots
_No response_
Reactions are currently unavailable
## Activity
[Sign up for free](https://github.com/signup?return_to=https://github.com/abhigyanpatwari/GitNexus/issues/1811)**to join this conversation on GitHub.** Already have an account? [Sign in to comment](https://github.com/login?return_to=https://github.com/abhigyanpatwari/GitNexus/issues/1811)
## Metadata
## Metadata
### Assignees
No one assigned
### Labels
[Something isn't working](https://github.com/abhigyanpatwari/GitNexus/issues?q=state%3Aopen%20label%3A%22bug%22)Something isn't working
### Projects
No projects
### Milestone
No milestone
### Relationships
None yet
### Development
No branches or pull requests
## Issue actions
  * Open in GitHub Copilot app


You can’t perform that action at this time. 
