---
url: "https://www.home-assistant.io/integrations/persistent_notification/"
title: "Persistent Notification - Home Assistant"
scraped_at: 2026-09-17T16:39:47+00:00
---

The **Persistent Notification** integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) can be used to show a notification on the frontend that has to be dismissed by the user.
## Automation 
Persistent notification [triggers](https://www.home-assistant.io/docs/automation/trigger) enable automations to be triggered when persistent notifications are updated. Triggers can be limited to a specific notification by providing an ID for `notification_id`, or when this value is omitted the automation will trigger for any notification ID. If no `update_type` is provided, the automation will trigger for the following update types: `added`, `removed`, `updated`, or `current`. By providing one or more of these values to the `update_type` option, the automation triggers only on these `update_type` events.
Review the [Automating Home Assistant](https://www.home-assistant.io/getting-started/automation/) getting started guide on automations or the [Automation](https://www.home-assistant.io/docs/automation/) documentation for full details.
An example of a persistent notification trigger in YAML:

```
automation:
  - triggers:
      - trigger: persistent_notification
        # Optional. Possible values: added, removed, updated, current
        update_type:
          - added
          - removed
        # Optional.
        notification_id: invalid_config
```

YAML
Copy
See [Automation Trigger Variables: Persistent Notification](https://www.home-assistant.io/docs/automation/templating/#persistent-notification) for additional trigger data available for conditions or actions.
## List of actions 
The Persistent Notification integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) provides the following actions. Each link below opens a dedicated page with examples, parameters, and a step-by-step UI walkthrough.
  * [Create notification](https://www.home-assistant.io/actions/persistent_notification.create/) (`persistent_notification.create`) Creates a persistent notification in the Home Assistant frontend.
  * [Dismiss notification](https://www.home-assistant.io/actions/persistent_notification.dismiss/) (`persistent_notification.dismiss`) Removes a single persistent notification from the Home Assistant frontend.
  * [Dismiss all notifications](https://www.home-assistant.io/actions/persistent_notification.dismiss_all/) (`persistent_notification.dismiss_all`) Removes all persistent notifications from the Home Assistant frontend.


For an overview of every action across all integrations, see the [actions reference](https://www.home-assistant.io/actions/).
## Use as a notifier 
Persistent notifications can also be used as a pre-configured notifier for the [Notify integration](https://www.home-assistant.io/integrations/notify/) when that integration is loaded. It is available as `notify.persistent_notification`. This lets you use it with features that require a notifier, such as [notify action groups](https://www.home-assistant.io/integrations/group/#notify-action-groups) or the [Alert integration](https://www.home-assistant.io/integrations/alert/).
You can place the following attribute inside `data` for extended functionality:
  * `notification_id`: When a notification ID is given, it overwrites the notification if one with that ID already exists.


####  **Help us improve our documentation**
Suggest an edit to this page, or provide/view feedback for this page. 


Back to top
