---
url: "https://docs.openclaw.ai/start/teams"
title: "Team setup - OpenClaw"
scraped_at: 2026-09-29T14:44:34+00:00
---

On this page
## On this page
Get startedSetup guides and reference
This guide sets up one OpenClaw gateway that a whole team uses: a bot in the workspace chat you already have, shared sessions everyone can open and steer in the Control UI, and roles that bound what each person can do. It is the same product as the [personal assistant setup](https://docs.openclaw.ai/start/openclaw) - team operation is configuration, not a separate edition.
For an always-on Linux deployment with Cloudflare Access, GitHub identity sync, role bootstrap, and operations, follow [Deploy a team server](https://docs.openclaw.ai/gateway/team-server).
## Before you begin
  * A host for the Gateway that stays on: a small VPS, an office Mac, or any [supported install target](https://docs.openclaw.ai/install).
  * OpenClaw installed and onboarded on that host - see [Getting started](https://docs.openclaw.ai/start/getting-started).
  * A chat workspace the team already uses (Discord, Google Chat, Mattermost, Microsoft Teams, Slack, Telegram, ...) - see [Channels](https://docs.openclaw.ai/channels).
  * A strong latest-generation model. Shared gateways see more varied input than a solo setup, and modern models are substantially more resistant to prompt injection - see [Security](https://docs.openclaw.ai/gateway/security/prompt-injection).
  * Optional: teammates' GitHub accounts, if you want verified identity and commit credit.


## One trust boundary
A gateway is one trust domain. Everyone who can message a tool-enabled agent shares that agent's delegated tool authority, and everyone with operator access shares one control plane. That is the right model for a team whose members already trust each other - session ownership, presence, and [roles](https://docs.openclaw.ai/gateway/operator-scopes#named-operator-roles) are collaboration guardrails inside the boundary, not isolation between adversaries.
If you need to serve mutually untrusted people or organizations, run one gateway per tenant instead: [Multi-tenant hosting](https://docs.openclaw.ai/gateway/multi-tenant-hosting).
## Step 1: Give the team access to the Gateway
The Gateway binds to loopback by default. Give teammates access through authenticated ingress instead of a public bind:
  * **Tailnet (recommended):** put the host on your tailnet and enable [Tailscale Serve](https://docs.openclaw.ai/gateway/tailscale). With `gateway.auth.allowTailscale`, Control UI sign-in can use each person's Tailscale identity - no shared secret to distribute.
  * **Trusted proxy:** front the Gateway with an identity-aware proxy such as Cloudflare Access - see [Trusted proxy auth](https://docs.openclaw.ai/gateway/trusted-proxy-auth).
  * **Shared secret:** token or password auth works for small teams, but everyone uses one owner profile instead of per-person identity - see [Authentication](https://docs.openclaw.ai/gateway/authentication).


The identity-backed options are worth the setup: they are what turns "someone did something" into "who did what" in the session UI and commit credit below.
## Step 2: Connect the team chat
Connect the channel your team lives in. Example: a Slack bot, allowed in one team channel, that replies when mentioned:
json5Copy code
```
{  channels: {    slack: {      enabled: true,      mode: "socket",      appToken: { source: "env", provider: "default", id: "SLACK_APP_TOKEN" },      botToken: { source: "env", provider: "default", id: "SLACK_BOT_TOKEN" },      groupPolicy: "allowlist",      channels: {        "<SLACK_CHANNEL_ID>": { requireMention: true },    },  },}
```

Group chats are a first-class deployment. The defaults are already team-shaped. Group access is allowlisted per room, and replies require a mention. DMs stay on the pairing default: the first time a teammate DMs the bot they get a pairing code. Approve it with `openclaw pairing approve slack <code>`. So the bot participates when addressed and stays quiet otherwise. In a private room whose members you trust, that is all the gating you need. For broad or public rooms, add sender allowlists and `contextVisibility` - see [Groups](https://docs.openclaw.ai/channels/groups).
If the same people should be allowed across several channels, define the list once as an [access group](https://docs.openclaw.ai/channels/access-groups) and reference it from each channel's allowlist.
## Step 3: Sign the team in to the Control UI
With per-person sign-in, each teammate opens the [Control UI](https://docs.openclaw.ai/web/control-ui) through the ingress from step 1. Each one gets a durable Gateway profile: display name, avatar, and per-person appearance preferences. Shared-secret connections use the same owner profile. With Cloudflare Access or Tailscale Serve, GitHub-backed sign-in verifies the account behind the profile - see [User model](https://docs.openclaw.ai/concepts/user-model).
Teammates can also create and import [personal skills](https://docs.openclaw.ai/tools/skills#personal-skills-on-a-shared-gateway) under **Plugins → Skills** without permission to change shared Gateway configuration. Skills stay personal until explicitly shared with the team. A session retains its selected revisions when another teammate joins; changing its assignee does not replace its skills. Your existing workspace skills remain in place, and extra channel identities for one operator do not enable the team-specific guidance.
## Step 4: Work in shared sessions
A conversation that starts in the team channel can continue as a session the whole team can open, steer, and take over. [Multi-user mode](https://docs.openclaw.ai/concepts/multi-user) gives every session three layers of attribution: an immutable creator, an assignable owner, and the history of people who actually prompted. Assign sessions like GitHub issues from the session context menu. Multi-user mode also adds live [presence](https://docs.openclaw.ai/concepts/presence). Presence shows who is viewing and who is typing, with drafts that never reach the model or the transcript.
For coding work, verified GitHub identity pays off at the commit: with **Git co-author credit** enabled, commits from a shared session carry `Co-authored-by` trailers for the people who steered it, and generated pull requests link back to the session so reviewers can read the conversation that produced the diff.
Teammates can add their own provider accounts under **Settings → Profile → Connected accounts** , using the sign-in methods offered by each provider. Their new sessions prefer that account without making it a Gateway-wide default. Collaborators use the session's selected account, and shared same-provider failover can still apply - see [Per-person model accounts](https://docs.openclaw.ai/concepts/multi-user#per-person-model-accounts).
To let teammates read selected sessions from a personal Gateway without controlling that machine, use [Session Share](https://docs.openclaw.ai/plugins/session-share). The source operator chooses session groups and pairs a node that advertises only the two read-only session commands. Shared transcripts appear under that node in the team Control UI; viewing requires permission to view others' sessions, and does not allow continuing the source session.
## Step 5: Bound what each person can do
Named operator roles bind authenticated profiles to a policy: which sessions they can touch, which agents they can use, a maximum set of operator scopes, and whether their new sessions must be sandboxed:
json5Copy code
```
{  gateway: {    roles: {      default: "guest",      definitions: {        maintainer: {          sessions: { others: "write" },          agents: ["roboclaw"],          scopes: ["operator.read", "operator.write", "operator.approvals"],        guest: {          sessions: { others: "view" },          agents: ["roboclaw"],          scopes: ["operator.read", "operator.write"],          sandbox: "required",    },  },}
```

Assign roles with the `users.setRole` Gateway method; see [Named operator roles](https://docs.openclaw.ai/gateway/operator-scopes#named-operator-roles) for the full policy surface and [Permission modes](https://docs.openclaw.ai/gateway/permission-modes) for per-session tool posture.
### Coding as a guest
A sandbox-required guest can work without an administrator role. With the default `workspaceAccess: "none"`, file and shell tools use a writable private workspace, not the shared agent workspace. Managed skill instructions stay read-only. Child sessions inherit the parent's sandbox requirement, even when the agent's default sandbox mode is off.
Local container sandboxes have no network by default. If guests need to clone public repositories or install project-local dependencies, explicitly enable outbound networking for the coding agent, for example:
json5Copy code
```
{  agents: {    entries: {      roboclaw: {        sandbox: {          workspaceAccess: "none",          docker: { network: "bridge" },    },  },}
```

Network access does not grant host execution or inject shared credentials. Use a sandbox image with the required runtimes already installed; the read-only root filesystem still prevents system package installation. Enabling egress allows requests to destinations reachable from the container, so use a restricted container network when that access needs tighter controls. See [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing#workspace-access) for workspace and network policy.
## Verify
  * Mention the bot in the allowed team channel and confirm it replies there.
  * Open the Control UI as two different people: both should see the session, its owner avatar, and each other's presence.
  * Run `openclaw security audit` on the host and resolve anything it flags about inbound access or exposure.


## When to split things up
  * **Separate workspaces or personas** (projects that must not share memory or files): use multiple agents on one gateway - see [Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent).
  * **Mutually untrusted users, customers, or organizations:** separate gateways, ideally separate OS users or hosts - see [Multi-tenant hosting](https://docs.openclaw.ai/gateway/multi-tenant-hosting) and [Security](https://docs.openclaw.ai/gateway/security).


## Related
  * [Why OpenClaw: working together](https://docs.openclaw.ai/start/why-openclaw#working-together) - the team collaboration surfaces in one place
  * [Multi-user mode](https://docs.openclaw.ai/concepts/multi-user) - ownership, participants, and owner filtering in depth
  * [Operator scopes](https://docs.openclaw.ai/gateway/operator-scopes) - connection roles, scopes, and role assignment
  * [Groups](https://docs.openclaw.ai/channels/groups) - group behavior, mention gating, and context visibility
  * [Security](https://docs.openclaw.ai/gateway/security) - the trust model behind the one-boundary rule


Was this useful?YesNo
Install OpenClawSet up TelegramFix GatewayBuild a plugin
Ask Molty
Ask Molty
Responses are generated using AI and may contain mistakes.
