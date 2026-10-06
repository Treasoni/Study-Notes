---
url: "https://docs.openclaw.ai/gateway/security"
title: "Security - OpenClaw"
scraped_at: 2026-09-29T14:44:57+00:00
---

On this page
## On this page
Gateway & OpsGateway
OpenClaw ships with conservative defaults. On a regular host install the Gateway binds to loopback; most chat channels answer an unknown DM sender with a pairing code instead of processing the message; and group access is allowlisted, usually behind a mention gate. The exceptions are deliberate and documented: container images default to an exposed bind (pair that with auth - see the [exposure runbook](https://docs.openclaw.ai/gateway/security/exposure-runbook)), and a few workspace channels such as ClickClack trust workspace membership by default - each channel page states its exact defaults. Run on those defaults and you are in good shape, and one command tells you if you have drifted:
bashCopy code
```
openclaw security audit
```

The pages below are the deep end: the trust model, what the audit checks, and how to harden further as you expose more surface.
Agents with message-tool access can send across conversations and channel providers by default. If your deployment needs messaging confined to the current provider or conversation, configure [cross-provider messaging restrictions](https://docs.openclaw.ai/gateway/security/tool-permissions#cross-provider-messaging).
## Security pages
Understand the model:
  * [Security trust model](https://docs.openclaw.ai/gateway/security/trust-model) - One trust boundary per gateway, the boundary matrix, and the findings closed as no-action.
  * [Running the security audit](https://docs.openclaw.ai/gateway/security/running-the-audit) - What `openclaw security audit` checks and the order to fix findings in.
  * [Security audit checks](https://docs.openclaw.ai/gateway/security/audit-checks) - Reference catalog of every `checkId`, its severity, and its auto-fix support.
  * [Threat model](https://docs.openclaw.ai/security/THREAT-MODEL-ATLAS) - Adversarial threats to the OpenClaw platform and ClawHub, mapped to MITRE ATLAS.


Harden a deployment:
  * [Hardened baselines](https://docs.openclaw.ai/gateway/security/hardened-baseline) - Copy/paste configs that keep the Gateway local, paired, and tool-restricted.
  * [Access control and allowlists](https://docs.openclaw.ai/gateway/security/access-control) - DM policy, allowlists, DM session isolation, context visibility, command authorization.
  * [Prompt injection](https://docs.openclaw.ai/gateway/security/prompt-injection) - Untrusted content reaching the model, model choice, and the wrapping that bounds it.
  * [Tool and agent permissions](https://docs.openclaw.ai/gateway/security/tool-permissions) - Control-plane tools, node execution, plugins, sandboxing, per-agent profiles.
  * [Browser control risks](https://docs.openclaw.ai/gateway/security/browser-control) - What a real browser exposes, and the SSRF policy that bounds it.
  * [Network exposure](https://docs.openclaw.ai/gateway/security/network-exposure) - Bind, firewall, discovery, Gateway auth, Tailscale, reverse proxy, dangerous flags.
  * [Secrets, storage, and logs](https://docs.openclaw.ai/gateway/security/secrets-and-storage) - What lands on disk, which files hold credentials, and what transcripts contain.
  * [Secure file operations](https://docs.openclaw.ai/gateway/security/secure-file-operations) - Root-bounded file access, atomic writes, and archive extraction helpers.
  * [Dependency locking](https://docs.openclaw.ai/gateway/security/dependency-locking) - How published packages pin and resolve their dependency graph.


Expose and operate:
  * [Gateway exposure runbook](https://docs.openclaw.ai/gateway/security/exposure-runbook) - Pre-flight and rollback checklist before exposing the Gateway beyond loopback.
  * [Trusted proxy auth](https://docs.openclaw.ai/gateway/trusted-proxy-auth) - Running the Gateway behind a reverse proxy that supplies the operator identity.
  * [Rate limiting](https://docs.openclaw.ai/gateway/security/rate-limiting) - Every Gateway rate limit: lockouts, throttles, caps, and cooldowns.
  * [Operator incident response](https://docs.openclaw.ai/gateway/security/operator-incident-response) - Contain, rotate, audit, and collect evidence after a suspected compromise.


Run it from the CLI:
  * [`openclaw security`](https://docs.openclaw.ai/cli/security) - Run the audit, read findings, and apply the supported auto-fixes.
  * [`openclaw policy`](https://docs.openclaw.ai/cli/policy) - Inspect and test the tool policy the guidance above configures.


## Where each section moved
Every anchor this page used to publish still resolves here. Each entry below carries the original anchor and links to its new home.
**[Security trust model](https://docs.openclaw.ai/gateway/security/trust-model)**
  * [Scope: one trust boundary per gateway](https://docs.openclaw.ai/gateway/security/trust-model#scope-one-trust-boundary-per-gateway)
  * [Not vulnerabilities by design](https://docs.openclaw.ai/gateway/security/trust-model#not-vulnerabilities-by-design)
  * [Common findings closed as no-action](https://docs.openclaw.ai/gateway/security/trust-model#common-findings-closed-as-no-action)
  * [Gateway and node trust](https://docs.openclaw.ai/gateway/security/trust-model#gateway-and-node-trust)
  * [Reporting security issues](https://docs.openclaw.ai/gateway/security/trust-model#reporting-security-issues)


**[Running the security audit](https://docs.openclaw.ai/gateway/security/running-the-audit)**
  * [What the audit checks (high level)](https://docs.openclaw.ai/gateway/security/running-the-audit#what-the-audit-checks-high-level)
  * [Priority order when triaging findings](https://docs.openclaw.ai/gateway/security/running-the-audit#priority-order-when-triaging-findings)


**[Hardened baselines](https://docs.openclaw.ai/gateway/security/hardened-baseline)**
  * [Hardened baseline in 60 seconds](https://docs.openclaw.ai/gateway/security/hardened-baseline#hardened-baseline-in-60-seconds)
  * [Requester-scoped controls and prompt context](https://docs.openclaw.ai/gateway/security/hardened-baseline#requester-scoped-controls-and-prompt-context)
  * [Secure baseline (copy/paste)](https://docs.openclaw.ai/gateway/security/hardened-baseline#secure-baseline-copy/paste)
  * [Separate numbers (WhatsApp, Signal, Telegram)](https://docs.openclaw.ai/gateway/security/hardened-baseline#separate-numbers-whatsapp-signal-telegram)


**[Access control and allowlists](https://docs.openclaw.ai/gateway/security/access-control)**
  * [DM access: pairing, allowlist, open, disabled](https://docs.openclaw.ai/gateway/security/access-control#dm-access-pairing-allowlist-open-disabled)
  * [DM session isolation (multi-user mode)](https://docs.openclaw.ai/gateway/security/access-control#dm-session-isolation-multi-user-mode)
  * [Context visibility vs trigger authorization](https://docs.openclaw.ai/gateway/security/access-control#context-visibility-vs-trigger-authorization)


**[Prompt injection](https://docs.openclaw.ai/gateway/security/prompt-injection)**
  * [External content and untrusted-input wrapping](https://docs.openclaw.ai/gateway/security/prompt-injection#external-content-and-untrusted-input-wrapping)
  * [Bypass flags (keep off in production)](https://docs.openclaw.ai/gateway/security/prompt-injection#bypass-flags-keep-off-in-production)
  * [Reasoning and verbose output in groups](https://docs.openclaw.ai/gateway/security/prompt-injection#reasoning-and-verbose-output-in-groups)


**[Tool and agent permissions](https://docs.openclaw.ai/gateway/security/tool-permissions)**
  * [Node execution (`system.run`)](https://docs.openclaw.ai/gateway/security/tool-permissions#node-execution-system-run)
  * [Dynamic skills (watcher / remote nodes)](https://docs.openclaw.ai/gateway/security/tool-permissions#dynamic-skills-watcher-/-remote-nodes)
  * [Sub-agent delegation guardrail](https://docs.openclaw.ai/gateway/security/tool-permissions#sub-agent-delegation-guardrail)
  * [Per-agent access profiles (multi-agent)](https://docs.openclaw.ai/gateway/security/tool-permissions#per-agent-access-profiles-multi-agent)
  * [Read-only tools + read-only workspace](https://docs.openclaw.ai/gateway/security/tool-permissions#read-only-tools-+-read-only-workspace)
  * [No filesystem/shell access (provider messaging allowed)](https://docs.openclaw.ai/gateway/security/tool-permissions#no-filesystem/shell-access-provider-messaging-allowed)


**[Browser control risks](https://docs.openclaw.ai/gateway/security/browser-control)**
  * [Browser SSRF policy (strict by default)](https://docs.openclaw.ai/gateway/security/browser-control#browser-ssrf-policy-strict-by-default)


**[Network exposure](https://docs.openclaw.ai/gateway/security/network-exposure)**
  * [Docker port publishing with UFW](https://docs.openclaw.ai/gateway/security/network-exposure#docker-port-publishing-with-ufw)
  * [Gateway WebSocket auth](https://docs.openclaw.ai/gateway/security/network-exposure#gateway-websocket-auth)
  * [Tailscale Serve identity headers](https://docs.openclaw.ai/gateway/security/network-exposure#tailscale-serve-identity-headers)
  * [Reverse proxy configuration](https://docs.openclaw.ai/gateway/security/network-exposure#reverse-proxy-configuration)
  * [Flags tracked by the audit today](https://docs.openclaw.ai/gateway/security/network-exposure#flags-tracked-by-the-audit-today)
  * [All dangerous*/dangerously* keys in the config schema](https://docs.openclaw.ai/gateway/security/network-exposure#all-dangerous-dangerously-keys-in-the-config-schema)


**[Secrets, storage, and logs](https://docs.openclaw.ai/gateway/security/secrets-and-storage)**
  * [Deployment and host trust](https://docs.openclaw.ai/gateway/security/secrets-and-storage#deployment-and-host-trust)
  * [Workspace `.env` files](https://docs.openclaw.ai/gateway/security/secrets-and-storage#workspace-env-files)


**[Operator incident response](https://docs.openclaw.ai/gateway/security/operator-incident-response)**
  * [Rotate (assume compromise if secrets leaked)](https://docs.openclaw.ai/gateway/security/operator-incident-response#rotate-assume-compromise-if-secrets-leaked)


Was this useful?YesNo
Install OpenClawSet up TelegramFix GatewayBuild a plugin
Ask Molty
Ask Molty
Responses are generated using AI and may contain mistakes.
