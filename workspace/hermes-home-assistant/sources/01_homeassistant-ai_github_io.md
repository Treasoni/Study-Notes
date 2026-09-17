---
url: "https://homeassistant-ai.github.io/ha-mcp/setup/"
title: "Home Assistant MCP Setup Wizard"
scraped_at: 2026-09-17T16:43:49+00:00
---

[Skip to content](https://homeassistant-ai.github.io/ha-mcp/setup/#main-content)
##  1How is your MCP server running?
RecommendedQuick
### HA Custom Component
Runs inside Home Assistant — every install type
### Alternative methods
Quick
### HA app (add-on)
Home Assistant OS / Supervised only
Complex
### Docker
Container
Complex
### uvx (Python)
Run the HTTP server via Python
Not recommended
### Local stdio
Legacy — known transport issues; fine for the demo server
##  2Select Your AI Client
### Claude Desktop
Anthropic
stdio
### Claude Code
Anthropic
stdioHTTP
### Cursor
Anysphere
stdioHTTP
### VS Code
Microsoft
stdioHTTP
### GitHub Copilot Agents
GitHub
stdioHTTP
### Windsurf
Codeium
stdioHTTP
### Cline
Cline
stdioHTTP
### Copilot CLI
GitHub
stdioHTTP
### ChatGPT
OpenAI
HTTPBETA
### Claude.ai
Anthropic
HTTP
### Gemini CLI
Google
stdioHTTP
### JetBrains IDEs
JetBrains
stdioHTTP
### Zed
Zed Industries
stdioHTTP
### Continue
Continue.dev
stdioHTTP
### Raycast
Raycast
stdioHTTP
### Codex
OpenAI
stdioHTTP
### Open WebUI
Open WebUI
HTTP
### OpenCode
Anomaly
stdioHTTP
### Antigravity
Google
stdio
### Gemini Spark
Google
HTTPBETA
### Hermes Agent
Nous Research
stdioHTTP
##  3Local or remote access?
Quick
### Local
Same machine or home network
Advanced
### Remote (internet)
Reach your server from anywhere over secure HTTPS
## Architecture Overview
Your Computer
AI Client + ha-mcp
→
HTTP/HTTPS*
Home Assistant
API
Local / Remote Network
ha-mcp runs as a subprocess on your computer, connecting directly to Home Assistant.
* HTTPS recommended for remote networks
Desktop
Laptop
→
HTTP*
ha-mcp Server
→
Home Assistant
Local Network (LAN)
The ha-mcp server runs in or beside Home Assistant and listens on your local network. Multiple clients can connect.
* Should not be exposed externally (No HTTPS). Use Remote for internet access.
AI Client
Anywhere
→
HTTPS
Reverse Proxy
SSL Certificate
→
HTTP
ha-mcp
Secret URL
→
Home Assistant
Your Network
Access from anywhere via secure HTTPS tunnel. Required for ChatGPT, Claude.ai web clients.
##  4Select Your Platform
Choose the operating system of your client machine.
### macOS
### Linux
### Windows
### Docker
##  5How will clients reach it remotely?
Expose your MCP server securely to the internet
Quick
### Built-in webhook
Nabu Casa or an existing reverse proxy — no extra setup
Quick
### Nabu Casa / Webhook Proxy
Uses your existing HA reverse proxy
Advanced
### Cloudflare Tunnel
Free, no port forwarding needed
Advanced
### Custom Reverse Proxy
Caddy, Nginx, Traefik, etc.
##  4Your Configuration
### Client Configuration
### Replace these placeholders (delete the surrounding `[object Object]` braces too):
← Start Over
## Demo server (local stdio)
Prefer to run ha-mcp locally over stdio, or just try the public demo Home Assistant? These per-OS walkthroughs cover it. stdio has known transport issues; not recommended for a permanent setup.
### macOS
Local or the Home Assistant App
Demo server
[RecommendedHome Assistant app (add-on)Local or remote · no access token](https://homeassistant-ai.github.io/ha-mcp/guide-addon)[Local install (stdio)Local machine only · needs a long-lived token](https://homeassistant-ai.github.io/ha-mcp/guide-macos)
### Linux
Local or the Home Assistant App
Demo server
[RecommendedHome Assistant app (add-on)Local or remote · no access token](https://homeassistant-ai.github.io/ha-mcp/guide-addon)[Local install (stdio)Claude Desktop or Claude Code · needs a long-lived token](https://homeassistant-ai.github.io/ha-mcp/guide-linux)
### Windows
Local or the Home Assistant App
Demo server
[RecommendedHome Assistant app (add-on)Local or remote · no access token](https://homeassistant-ai.github.io/ha-mcp/guide-addon)[Local install (stdio)Local machine only · needs a long-lived token](https://homeassistant-ai.github.io/ha-mcp/guide-windows)
