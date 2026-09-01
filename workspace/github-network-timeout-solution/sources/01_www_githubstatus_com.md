---
url: "https://www.githubstatus.com/"
title: "GitHub Status"
scraped_at: 2026-08-29T08:27:56+00:00
---

[ GitHub Octicon logo ](https://www.githubstatus.com/)
[ Subscribe to UpdatesSubscribe ](https://www.githubstatus.com/)
Get email notifications whenever GitHub **creates** , **updates** or **resolves** an incident. 
Get text message notifications whenever GitHub **creates** or **resolves** an incident. 
Get incident updates and maintenance status messages in Slack. 
[Subscribe via Slack](https://subscriptions.statuspage.io/slack_authentication/kickoff?page_code=kctbh9vrtdwd)
By subscribing you acknowledge our [Privacy Policy](https://help.github.com/articles/github-privacy-statement/). In addition, you agree to the Atlassian [Cloud Terms of Service](https://www.atlassian.com/legal/cloud-terms-of-service) and acknowledge Atlassian's [Privacy Policy](https://www.atlassian.com/legal/privacy-policy).
Get webhook notifications whenever GitHub **creates** an incident, **updates** an incident, **resolves** an incident or **changes** a component status. 
Visit our [support site](https://github.com/support). 
Get the [Atom Feed](https://www.githubstatus.com/history.atom) or [RSS Feed](https://www.githubstatus.com/history.rss). 
##  All Systems Operational 
##  [About This Site](https://www.githubstatus.com/#about-this-site)
Check GitHub Enterprise Cloud status by region: - Australia: [au.githubstatus.com](https://au.githubstatus.com) - EU: [eu.githubstatus.com](https://eu.githubstatus.com) - Japan: [jp.githubstatus.com](https://jp.githubstatus.com) - US: [us.githubstatus.com](https://us.githubstatus.com/)
Uptime over the past 90 days. [View historical uptime.](https://www.githubstatus.com/uptime)
Git Operations  ? Operational 
90 days ago 
100.0 % uptime 
Today
Webhooks  ? Operational 
90 days ago 
99.99 % uptime 
Today
Visit www.githubstatus.com for more information  Operational 
API Requests  ? Operational 
90 days ago 
99.81 % uptime 
Today
Issues  ? Operational 
90 days ago 
99.88 % uptime 
Today
Pull Requests  ? Operational 
90 days ago 
99.88 % uptime 
Today
Actions  ? Operational 
90 days ago 
99.25 % uptime 
Today
Packages  ? Operational 
90 days ago 
100.0 % uptime 
Today
Pages  ? Operational 
90 days ago 
99.65 % uptime 
Today
Copilot  Operational 
90 days ago 
99.64 % uptime 
Today
Codespaces  ? Operational 
90 days ago 
99.97 % uptime 
Today
Copilot AI Model Providers  Operational 
90 days ago 
99.89 % uptime 
Today
Operational 
Degraded Performance 
Partial Outage 
Major Outage 
Maintenance 
Major outage 
Partial outage 
No downtime recorded on this day. 
No data exists for this day. 
had a major outage. 
had a partial outage. 
### Related
No incidents or maintenance related to this downtime.
## Past Incidents
Aug 29, 2026
No incidents reported today.
Aug 28, 2026
No incidents reported.
Aug 27, 2026
[Disruption with GitHub Billing](https://www.githubstatus.com/incidents/5bn0vk444m1w)
**Resolved** - This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available. Aug 27, 19:44 UTC 
**Update** - No material change since the previous update. Service conditions remain stable following the mitigation, and we have not observed any further customer impact. We are actively monitoring the service while implementing targeted fixes to address the underlying root cause. Aug 27, 17:58 UTC 
**Update** - Our mitigation continues to hold, and service conditions remain stable. We are continuing to investigate the concentrated workload responsible for the issue and are preparing additional preventative improvements. We have not identified a material change in customer impact since the previous update. We will provide another update as the investigation progresses. Aug 27, 16:20 UTC 
**Update** - Our mitigation is still holding as we continue to investigate to find the root cause. Aug 27, 14:49 UTC 
**Update** - We are continuing to monitor the mitigation that we have applied for the billing page disruption. Aug 27, 01:35 UTC 
**Update** - We've applied a mitigation to unblock Copilot usage and have observed recovery for this particular impact. We're continuing to investigate and apply mitigations for the billing page disruption while monitoring to ensure Copilot remains recovered. Aug 27, 00:31 UTC 
**Update** - We are currently investigating increased errors with billing services. Customers may observe failed billing budget page loads, and users of the Copilot CLI may observe failures starting or continuing sessions. Aug 26, 23:42 UTC 
**Investigating** - We are investigating reports of impacted performance for some GitHub services. Aug 26, 23:37 UTC 
[Incident with Copilot AI Model Providers](https://www.githubstatus.com/incidents/tx9qn4khd664)
**Resolved** - This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available. Aug 27, 12:12 UTC 
**Update** - The issues with our upstream model provider have been mitigated, and Kimi K3 is once again available in Copilot products and IDE surfaces.We will continue monitoring to ensure stability. Aug 27, 12:12 UTC 
**Update** - Copilot AI Model Providers is experiencing degraded performance. We are continuing to investigate. Aug 27, 11:58 UTC 
**Update** - We are experiencing degraded availability for the Kimi K3 model in Copilot products and IDE surfaces. This is due to an issue with an upstream model provider. While we work with them to resolve the issue, we recommend choosing another model or selecting 'Auto' to continue using Copilot. Aug 27, 10:43 UTC 
**Investigating** - We are investigating reports of degraded availability for Copilot AI Model Providers Aug 27, 10:04 UTC 
[Incident with Actions and Pull Requests](https://www.githubstatus.com/incidents/kfspvrz14xr0)
**Resolved** - On August 26, 2026, from 21:55 UTC to 23:58 UTC, 2.6% of workflow runs triggered by pull request events were delayed, with the impact rising as high as 25% at its peak. Some users also experienced delays in pull request merge-commit generation, mergeability information, and merge-button availability. Actions and Pull Requests fully recovered by 23:58 UTC; the incident was resolved at 00:26 UTC after normal operation was confirmed. Background jobs that process pull request updates and generate merge commits were impacted by timeouts reaching a single partition of git data. This resulted in a backlog in pull request merge-commit processing, delaying pull request-triggered GitHub Actions workflows and some mergeability information. We reduced workload, shifted traffic away from affected infrastructure, and restored the affected service component to a healthy state. Together, these actions helped drain the backlog and restore normal operations. We are working to improve resource saturation detection and to eliminate customer impact in this scenario by isolating impact, placing better bounds on retries, and strengthening backpressure to make our systems more resilient under load. Aug 27, 00:26 UTC 
**Monitoring** - The degradation affecting Actions and Pull Requests has been mitigated. We are monitoring to ensure stability. Aug 27, 00:26 UTC 
**Update** - We confirmed full recovery beginning at 23:58 UTC. Actions workflow runs and pull request merges are operating normally. We will now resolve the incident while continuing to monitor service health. Aug 27, 00:25 UTC 
**Update** - We've applied mitigations and are seeing recovery in Actions workflow runs and blocked pull request merges. We're continuing to monitor for sustained health of merge commit creates before resolving. Aug 27, 00:01 UTC 
**Update** - We are investigating elevated delays and timeouts affecting Actions workflow runs triggered by pull request events. 20% of actions runs have delayed starts of more than 5 minutes and up to 4% of runs failed to trigger. We are actively working on mitigation and will provide updates as we learn more. Aug 26, 22:57 UTC 
**Investigating** - We are investigating reports of degraded performance for Actions and Pull Requests Aug 26, 22:56 UTC 
Aug 26, 2026
[Incident with Actions](https://www.githubstatus.com/incidents/y1t7p9fzrlj2)
**Resolved** - On August 26, 2026 from 15:02 to 15:45 UTC, Actions jobs failed to start. The following 2 hours until 17:40 UTC, Actions runs were delayed starting by more than 5 minutes as the system caught up with delayed load. This impact was triggered by saturation of writes to the database primary used by the service processing triggers for Actions workflows. The primary was failed over, but the system did not fully recover. The saturation was caused by growing daily peak load combined with an upstream issue in GitHub’s event processing infrastructure, <https://www.githubstatus.com/incidents/hcbtzksccj2f>, which caused burst amplification of already-high load. Downstream throttles that were later used to recover were set ~10% too high to protect the system. At 15:45 UTC, throttling combined with service restarts recovered the service’s core health. Those throttles were gradually raised between 15:54 and 17:22 to restore full webhook processing for Actions runs. This ramp was deliberately slow to ensure we did not re-overwhelm the system given our original throttling was now known to be incorrectly set. The queue of webhook events was fully burned down at 17:40 UTC. 3.7% of larger-runner jobs, along with some scale-set self-hosted jobs, remained stuck in queued or “waiting for runner” state. We deployed a change to force-revoke jobs in this state, and they transitioned to failed at 18:40 UTC, about 50 minutes after incident mitigation. Releasing these jobs also freed hosted concurrency for larger-runner jobs. Customers using concurrency groups saw longer impact due to a separate issue where runners assigned to a subset of jobs disconnected before the force-revoke mitigation was deployed, which prevented runner acquisition from progressing and left jobs in a waiting-for-runner state. This was resolved at 01:00 UTC on August 27. Some runs triggered during the 15:02-15:45 UTC incident window encountered a bug that left them showing as queued even after service recovery. In the backend, these runs had already failed and will automatically move to canceled state 24 hours after creation. As follow-up, we are fixing the root cause of this queued state and improving our ability to bulk-cancel affected runs. Several changes to improve the general scalability of this part of Actions were already complete and deploying to production. Rollout of those changes will be complete within the next 24 hours. Further work to improve scale, resiliency, and more graceful degradation of Actions workflows are in flight. We are also taking a repair item to accelerate clearing of stuck queued or waiting jobs in similar future cases. Aug 26, 18:01 UTC 
**Update** - All inbound queues have recovered and Actions is operating as expected. 3.7% of jobs assigned to larger runners during the early stage of this incident are stuck waiting for runner assignment. Those will be canceled within the hour. Other runners are successfully processing all new jobs. Aug 26, 18:00 UTC 
**Monitoring** - The degradation affecting Actions has been mitigated. We are monitoring to ensure stability. Aug 26, 17:54 UTC 
**Update** - We are continuing to observe recovery and expect actions inbound queues to be back to normal in <30min. Work will continue to flow through the system subject to per-customer concurrency limits. Aug 26, 17:32 UTC 
**Update** - We are continuing to observe recovery and delayed queues are burning down. Some customers will continue to see increased delays until all throttled work has been completed - we expect this within the next hour. Aug 26, 16:50 UTC 
**Update** - Pages is operating normally. Aug 26, 16:49 UTC 
**Update** - We believe we've identified and addressed the issue and are ramping traffic back up slowly to ensure it doesn't recur. Some customers will continue to see delays as we ramp up. Aug 26, 16:14 UTC 
**Update** - primary failover briefly improved performance but did not fully mitigate, we've throttled inbound traffic and are investigating upstream Vitess issues Aug 26, 15:48 UTC 
**Update** - We've identified an issue with a database primary and are failing over to a replica immediately Aug 26, 15:23 UTC 
**Update** - Pages is experiencing degraded performance. We are continuing to investigate. Aug 26, 15:12 UTC 
**Investigating** - We are investigating reports of degraded availability for Actions Aug 26, 15:11 UTC 
[Disruption with some GitHub services](https://www.githubstatus.com/incidents/hcbtzksccj2f)
**Resolved** - This incident has been resolved. Thank you for your patience and understanding as we addressed this issue. A detailed root cause analysis will be shared as soon as it is available. Aug 26, 16:07 UTC 
**Investigating** - We are investigating reports of impacted performance for some GitHub services. Aug 26, 15:09 UTC 
Aug 25, 2026
No incidents reported.
Aug 24, 2026
[Actions delays in starting runs](https://www.githubstatus.com/incidents/lyppgxbq1nyk)
**Resolved** - On August 24, 2026, between 13:33 UTC and 14:04 UTC, 3.8% of Actions runs experienced start delays over 5 minutes with 1.25% of Actions runs failing outright. The incident was caused by a disk failure on a node hosting one of many service instances responsible for processing runner assignment events. Typically, pods on unhealthy nodes are removed and replaced automatically without impact. In this case, although the node was severely degraded and unable to perform disk operations, it continued sending healthy signals, preventing the system from immediately moving its work elsewhere. During this period, events assigned to the affected component accumulated until an automatic rebalance redirected processing to healthy components at 13:54 UTC. The queue backlog was cleared at 14:00 UTC, and processing returned to normal by 14:04 UTC. To prevent a recurrence, we are improving detection and automated remediation for unhealthy nodes that aren’t fully offline. We are also strengthening application-level resiliency, so stalled consumers are automatically removed quickly and their work reassigned without waiting for the affected node to recover. Aug 24, 14:34 UTC 
**Monitoring** - The degradation affecting Actions has been mitigated. We are monitoring to ensure stability. Aug 24, 14:26 UTC 
**Update** - Failures while queuing and running Actions jobs for a subset of customers are now resolving. We are monitoring for full recovery. Aug 24, 14:22 UTC 
**Investigating** - We are investigating reports of degraded performance for Actions Aug 24, 13:56 UTC 
[Elevated errors on Fable 5 due to upstream provider](https://www.githubstatus.com/incidents/wt3hjqcrczfg)
**Resolved** - On August 24th, 2026, between approximately 06:35 and 07:25 UTC, the Copilot service experienced a degradation of the Claude Fable 5 model due to an issue with our upstream provider. Users encountered elevated error rates when using Claude Fable 5, with requests sometimes failing mid-response. No other models were impacted.The issue was resolved by a mitigation put in place by our provider. GitHub is working with our provider to further improve the resiliency of the service to prevent similar incidents in the future. Aug 24, 07:58 UTC 
**Update** - We are experiencing degraded availability for the Fable model in Copilot products and IDE surfaces. This is due to an issue with the upstream model provider. While we work with them to resolve the issue, we recommend choosing another model or selecting 'Auto' to continue using Copilot. Aug 24, 07:12 UTC 
**Investigating** - We are investigating reports of degraded availability for Copilot AI Model Providers Aug 24, 07:12 UTC 
Aug 23, 2026
No incidents reported.
Aug 22, 2026
No incidents reported.
Aug 21, 2026
[Degraded Git Operations over SSH](https://www.githubstatus.com/incidents/wms44hv62t3p)
**Resolved** - On August 21, 2026, between 14:00 and 14:07 UTC, dotcom Git operations over SSH were degraded. Successful Git operations over SSH fell by more than 95% for during the peak impact window, making clone, fetch, or push over SSH effectively unavailable to most users for approximately four minutes. Git operations over HTTPS were not affected. The incident was caused by a software defect in our load-balancing infrastructure that was triggered by a configuration change. The defect only occurred when connections passed through multiple layers of load balancers running the new configuration, which meant it was not detected during canary testing. We mitigated the incident by rolling back the configuration change. We are adding regression coverage for multi-layer load-balancer configurations and improving monitoring and alerting for Git operations over SSH to reduce our time to detection and mitigation of similar issues in the future. Aug 21, 14:00 UTC 
[Intermittent failures creating agent tasks](https://www.githubstatus.com/incidents/bhbcjn4n3jzp)
**Resolved** - Between 13:57 UTC on August 20 and 00:37 UTC on August 21, 2026, some users of the Copilot Cloud Agent experienced delays of up to 60 to 90 minutes in seeing the status and results of their agent tasks. The agent tasks themselves continued to run and complete during this time; only the visibility of their status was delayed.The cause was a regional outage in a third-party cloud database service that Copilot uses to store agent task status. We failed over the affected database to a healthy region, added processing capacity to work through the backlog, and restored normal operation once the underlying service recovered. No task data was lost during the incident.To prevent repetition of similar incidents, we are removing the database configuration that made us vulnerable to this regional outage and improving our database failover procedures. Aug 21, 00:37 UTC 
**Update** - We are seeing gradual recovery in Copilot Cloud Agent task status visibility as we deploy a fix for the root cause. Session output remains delayed by approximately one hour while remediation continues. Aug 20, 20:37 UTC 
**Update** - We are continuing to observe gradual recovery for Copilot Cloud Agent task status visibility. Session output continues to be delayed by approximately 1 hour as our remediation steps take effect. Aug 20, 19:35 UTC 
**Update** - We are continuing to observe gradual recovery for Copilot Cloud Agent task status visibility, with session output delayed by approximately 1 hour. We have taken additional steps to accelerate the recovery and expect this to take effect within the next hour. Aug 20, 18:45 UTC 
**Update** - We are continuing to observe gradual recovery for Copilot Cloud Agent task status visibility, with session output delayed by approximately 1 hour. We have taken additional steps to accelerate the recovery and are continuing to monitor the impact. Aug 20, 18:04 UTC 
**Update** - We are observing gradual recovery for Copilot Cloud Agent task status visibility, with session output delayed approximately 1 hour. We have taken additional steps to accelerate the recovery and are continuing to monitor the impact. Aug 20, 17:32 UTC 
**Update** - We are seeing signs of recovery for Copilot Cloud Agent task status visibility, but this recovery is slower than anticipated. We are pursuing additional mitigating measures to accelerate recovery. Aug 20, 17:05 UTC 
**Update** - Users are experiencing delays when starting tasks using Copilot Cloud Agent and are not be able to see the status of these tasks. Copilot Cloud Agent tasks are still being completed. We have identified the cause of the issue and are putting mitigations in place to return service to normal levels. We will provide another update about the expected recovery time shortly. Aug 20, 16:14 UTC 
**Update** - We are experiencing issues with Copilot Cloud Agent tasks, resulting in newly started tasks not properly displaying on-going progress. These Copilot Cloud Agent tasks are still being completed correctly but lack proper visibility. We are actively investigating the issue and will provide updates as we learn more. Aug 20, 15:41 UTC 
**Update** - We have identified the problematic component and are working to fail over to a healthy instance. Further updates will be provided as we perform mitigations. Aug 20, 15:01 UTC 
**Update** - Users may experience delays when starting tasks using Copilot Cloud Agent. We are actively investigating the issue and will provide updates as we learn more. Aug 20, 14:51 UTC 
**Investigating** - We are investigating reports of impacted performance for some GitHub services. Aug 20, 14:43 UTC 
Aug 20, 2026
Aug 19, 2026
No incidents reported.
Aug 18, 2026
[Intermittent failures in runner group and runner-related permissions pages](https://www.githubstatus.com/incidents/bmpybhnrky3x)
**Resolved** - On August 18, 2026, between 05:02 UTC and 11:30 UTC, customers were unable to view or manage Actions Runners and Runner Groups through the GitHub UI and API. The issue was caused by failures in backend requests reading runner and runner group data. The failures were caused by an expired authentication certificate unique to this service. The certificate had been rotated in KeyVault, but a step to enable use at runtime had been paused to prevent recurrence of previous incidents triggered by this operation. The impact was mitigated by completing the enablement of the new certificate in the backend system. We have added additional monitoring to this and other certificates. This service is also in the process of being replaced as part of our availability and scale work, bringing this authentication path and secret management in line with patterns across all GitHub services. Aug 18, 11:42 UTC 
**Update** - We have applied a mitigation and are seeing recovery signals. We will continue monitoring recovery and providing updates. Aug 18, 11:24 UTC 
**Update** - We have identified the source of a communication issue between Actions services and are working toward mitigation. Customers may experience failure to load runner groups and runner-related permissions issues when using Larger Runners. Aug 18, 10:41 UTC 
**Monitoring** - We are investigating reports of failure to load runner groups and runner-related permissions for customers using larger runners. Aug 18, 07:40 UTC 
**Investigating** - We are investigating reports of impacted performance for some GitHub services. Aug 18, 07:40 UTC 
[Incident with Actions](https://www.githubstatus.com/incidents/gx7js8bd0jpz)
**Resolved** - On August 18, 2026, between 05:02 UTC and 11:30 UTC, customers were unable to run jobs on Actions Larger Runners and were unable to view or manage Actions Runners and Runner Groups through the GitHub UI and API. These issues were caused by failures in backend requests resolving essential metadata for starting Larger Runner workflow runs and for reading runner and runner group data. The failures were caused by an expired authentication certificate unique to this service. The certificate had been rotated in KeyVault, but a step to enable use at runtime had been paused to prevent recurrence of previous incidents that had been triggered by this operation. We mitigated the issues by completing the enablement of the new certificate in the backend system. We have added additional monitoring to this and other certificates. The relevant service is also in the process of being replaced as part of our availability and scale work, bringing this authentication path and secret management in line with patterns across all GitHub services. Aug 18, 10:23 UTC 
**Investigating** - We are investigating reports of impacted performance for some GitHub services. Aug 18, 09:36 UTC 
Aug 17, 2026
[Incident with GitHub.com](https://www.githubstatus.com/incidents/zkxwbgr0cnmx)
**Resolved** - On August 17, 2026, from 13:28–21:15 UTC (7h 47m), GitHub.com experienced elevated errors and latency across Issues, Pull Requests, APIs, Actions, and Copilot. At peak, web/API error rates were approximately 20%, while archive and raw-content downloads reached approximately 50%. SAML/OIDC authentication, SCIM, and Team Sync were also affected, as well as Actions workflows in GHEC with Data Residency that depend on public workflow step definitions hosted on GitHub.com. Most services recovered by 16:36 UTC as our Central US datacenter recovered; Actions was degraded until approximately 18:03 UTC; and Copilot Token Service fully recovered by 21:02. Some of the failing traffic was moved from Central US to Northern Virginia where it was served successfully until the network failure in Central US was debugged and resolved. Delayed replies to a single internal endpoint triggered a latent retry bug in VS Code that amplified traffic by approximately 10x and caused delayed recovery for the Copilot Token Service. The immediate cause of the failure was network saturation on load balancers in Central US due to a new peak in traffic. Originally this was caused by an Istio sidecar pod reaching its concurrency limits and failing to auto scale correctly because of a misconfigured policy that watched host service but not sidecar limits. One failure cascaded to more and eventually four HAProxy nodes exhausted their flow limits, degrading the gateway auth path and causing widespread authentication latency and failures. The problem was worsened by optimistic retry logic which overloaded internal load balancers. Pausing HAProxy on those nodes simultaneously produced immediate broad recovery. The retry storm in Northern VA was fixed by 1) temporarily reducing gateway retry logic with a PR and 2) blocking inbound Copilot Token Service token requests at the load balancers with a 403, and then gradually ramping back up traffic per-site to allow callers to succeed. Residual Copilot authentication failures continued because client retry behavior amplified load: a failed token operation could generate many extra requests and enter a retry loop. Copilot Token Service traffic increased from a normal 7–9K RPS to 70–100K RPS. Reducing gateway authentication retries and blocking retry-triggering responses stabilized Copilot Token Service and completed recovery. Complicating factors that impeded recovery included a number of scraping attacks on codeload endpoints. To prevent recurrence, our follow-up actions include: - Correcting autoscaling policies to account for service-mesh sidecar concurrency and capacity. - Auditing Istio request, concurrency, and scaling limits across affected services. - Reviewing retry limits and backoff behavior across gateways and clients. - Addressing the VS Code retry behavior that amplified Copilot token traffic. - Improving load-balancer capacity monitoring and regional failover safeguards. Aug 17, 21:15 UTC 
**Update** - We are continuing to apply mitigations to address sporadic Copilot authentication failures in some applications. We expect full recovery within the next 30 minutes. Copilot usage via the GitHub CLI and GitHub App are unaffected. Aug 17, 20:45 UTC 
**Update** - Issues is operating normally. Aug 17, 20:22 UTC 
**Update** - We are continuing to investigate sporadic failures affecting Copilot authentication in some applications. Copilot usage via the GitHub CLI and GitHub App are unaffected. Aug 17, 20:08 UTC 
**Update** - We are continuing to investigate sporadic authentication failures. We have partially disabled authentication token retries and have seen improvement, and we are monitoring impact before fully applying this mitigation. Aug 17, 19:13 UTC 
**Update** - API Requests is operating normally. Aug 17, 19:01 UTC 
**Update** - API Requests is experiencing degraded availability. We are continuing to investigate. Aug 17, 18:48 UTC 
**Update** - The degradation affecting Git Operations has been mitigated. We are monitoring to ensure stability. Aug 17, 18:23 UTC 
**Update** - We identified the problematic component and have taken corrective actions, but we are seeing residual impact in the form of sporadic authentication failures. We are continuing to apply additional mitigations and investigate the remaining impact. Aug 17, 18:11 UTC 
**Update** - Issues is experiencing degraded performance. We are continuing to investigate. Aug 17, 17:36 UTC 
**Update** - We identified the problematic component and have taken corrective actions, but we are seeing residual impact across numerous services. We are continuing to apply additional mitigations and investigate the remaining impact. Aug 17, 17:34 UTC 
**Update** - Git Operations is experiencing degraded performance. We are continuing to investigate. Aug 17, 17:30 UTC 
**Update** - The degradation affecting API Requests, Actions, Git Operations, Issues, Pages, Pull Requests and Webhooks has been mitigated. We are monitoring to ensure stability. Aug 17, 16:59 UTC 
**Update** - We identified the problematic component and have taken corrective actions. There are strong signs of recovery but we are still working to completely restore service, with error rates still remaining slightly elevated. We will post further updates as recovery continues. Aug 17, 16:36 UTC 
**Update** - We are experiencing high error rates around 20% for web experiences and api traffic. Archive downloads and raw repository content downloads are experiencing an approximate 50% error rate. SAML and OIDC authentication, SCIM, and Team Sync are also impacted. We are still working to identify the root cause and will continue to post updates as we learn more and perform mitigation. Aug 17, 16:16 UTC 
**Update** - We are experiencing high error rates around 20% for web experiences and api traffic. Archive downloads and raw repository content downloads are experiencing an approximate 50% error rate. SAML and OIDC authentication, SCIM, and Team Sync are also impacted. We are currently performing mitigations and will post updates as we progress. Aug 17, 15:42 UTC 
**Update** - Webhooks is experiencing degraded performance. We are continuing to investigate. Aug 17, 15:40 UTC 
**Update** - Git Operations is experiencing degraded performance. We are continuing to investigate. Aug 17, 15:21 UTC 
**Update** - Pages is experiencing degraded performance. We are continuing to investigate. Aug 17, 15:10 UTC 
**Update** - API Requests is experiencing degraded availability. We are continuing to investigate. Aug 17, 15:01 UTC 
**Update** - Webhooks is experiencing degraded availability. We are continuing to investigate. Aug 17, 14:58 UTC 
**Update** - We are experiencing high error rates around 20% for web experiences and api traffic. Archive downloads and raw repository content downloads are experiencing an approximate 50% error rate. SAML and OIDC authentication, SCIM, and Team Sync are also impacted. We are currently performing mitigations based on our investigation thus far and are monitoring for improvement. Aug 17, 14:58 UTC 
**Update** - Actions is experiencing degraded availability. We are continuing to investigate. Aug 17, 14:58 UTC 
**Update** - Pull Requests is experiencing degraded availability. We are continuing to investigate. Aug 17, 14:54 UTC 
**Update** - Issues is experiencing degraded availability. We are continuing to investigate. Aug 17, 14:49 UTC 
**Update** - Pull Requests is experiencing degraded availability. We are continuing to investigate. Aug 17, 14:45 UTC 
**Update** - Copilot is experiencing degraded availability. We are continuing to investigate. Aug 17, 14:31 UTC 
**Update** - We are experiencing high error rates around 20% for web experiences and api traffic. Archive downloads and raw repository content downloads are experiencing an approximate 50% error rate. SAML and OIDC authentication, SCIM, and Team Sync are also impacted. Investigations are on-going and we will continue to provide updates as we discover more information. Aug 17, 14:24 UTC 
**Update** - We are experiencing high error rates around 20% for web experiences and api traffic. Archive downloads and raw repository content downloads are experiencing an approximate 50% error rate. Investigations are on-going into the root cause, and updates will continue to be provided as we investigate. Aug 17, 14:04 UTC 
**Update** - Pull Requests is experiencing degraded performance. We are continuing to investigate. Aug 17, 13:58 UTC 
**Update** - Issues is experiencing degraded performance. We are continuing to investigate. Aug 17, 13:46 UTC 
**Update** - We are seeing an approximate 20% error rate across numerous experiences including Pull Requests, Issues, and others. Investigations are currently under way and we will be posting updates as they become available Aug 17, 13:45 UTC 
**Update** - Webhooks is experiencing degraded performance. We are continuing to investigate. Aug 17, 13:44 UTC 
**Update** - Actions is experiencing degraded performance. We are continuing to investigate. Aug 17, 13:42 UTC 
**Update** - API Requests is experiencing degraded performance. We are continuing to investigate. Aug 17, 13:41 UTC 
**Investigating** - We are investigating reports of impacted performance for some GitHub services. Aug 17, 13:40 UTC 
Aug 16, 2026
No incidents reported.
Aug 15, 2026
No incidents reported.
[← Incident History](https://www.githubstatus.com/history)
### Subscribe to our developer newsletter
Get tips, technical guides, and best practices. Twice a month. Right in your inbox.
[Subscribe](https://resources.github.com/newsletter/)
