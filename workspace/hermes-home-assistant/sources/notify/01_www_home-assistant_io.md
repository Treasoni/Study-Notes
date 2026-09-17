---
url: "https://www.home-assistant.io/integrations/notify/"
title: "Notifications - Home Assistant"
scraped_at: 2026-09-17T16:40:51+00:00
---

The **Notify** integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) makes it possible to send notifications to a wide variety of platforms. To use it, you have to set up at least one notification target (notifier). Check the [integrations list](https://www.home-assistant.io/integrations/#notifications) for one that fits your use case.
If you want to send notifications to the Home Assistant web interface, you may use the [Persistent Notification integration](https://www.home-assistant.io/integrations/persistent_notification/). It is available as an automatically configured notifier. See [its documentation](https://www.home-assistant.io/integrations/persistent_notification/) for more details.
Note
**Building block integration**
This notifications is a building block integration that cannot be added to your Home Assistant directly but is used and provided by other integrations.
A building block integration differs from the typical integration that connects to a device or service. Instead, other integrations that do integrate a device or service into Home Assistant use this notifications building block to provide entities, services, and other functionality that you can use in your automations or dashboards.
If one of your integrations features this building block, this page documents the functionality the notifications building block offers.
## The state of a notify entity 
The state of a notify entity is the date and time when a message was last sent.
Screenshot showing the state of a notify entity in [Settings > Tools > States](https://my.home-assistant.io/redirect/developer_states)
In addition, the entity can have the following states:
  * **Unavailable** : The entity is currently unavailable.
  * **Unknown** : The state is not yet known.


## List of actions 
The Notifications integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) provides the following actions. Each link below opens a dedicated page with examples, parameters, and a step-by-step UI walkthrough.
  * [Send a notification](https://www.home-assistant.io/actions/notify.notify/) (`notify.notify`) Sends a notification message to selected targets.
  * [Send a persistent notification](https://www.home-assistant.io/actions/notify.persistent_notification/) (`notify.persistent_notification`) Sends a notification that is visible in the notifications panel.
  * [Send a notification message](https://www.home-assistant.io/actions/notify.send_message/) (`notify.send_message`) Sends a notification message to one or more notify entities.


For an overview of every action across all integrations, see the [actions reference](https://www.home-assistant.io/actions/).
The notification actions serve different purposes:
  * **Send a notification message** (`notify.send_message`): sends a message to one or more notify entities selected as targets. Use this action when the notification destination is available as a notify entity.
  * **Send a persistent notification** (`notify.persistent_notification`): creates a notification in the Home Assistant notifications panel.
  * **Send a notification** (`notify.notify`): shorthand for the first notify action Home Assistant can find. The destination is therefore not explicitly selected and the message might not be sent where you expect. Choose a specific action or notify entity when the destination matters.


## Companion app notifications 
A common notification integration is via the Home Assistant Companion app for Android or iOS. If your phone is available as a notify entity, use the **Send a notification message** action and select that phone as the target. Some older setups may still provide a phone-specific action such as `notify.mobile_app_your_phone_name`. Refer to the [Companion app documentation](https://companion.home-assistant.io/docs/notifications/notifications-basic) for many customization options.
With any of these integrations, the **Message** field in the automation editor is the main text that will be sent. Other fields are optional, and some integrations support additional **Data** or **Target** information to customize the action. For more details, refer to their integration documentation.
Notifications can also be sent using [notify action groups](https://www.home-assistant.io/integrations/group/#notify-action-groups). These allow you to send notifications to multiple devices with a single call, or to update which device is notified by only changing it in a single place.
## Notifications automation examples 
Notifications are most useful when Home Assistant sends them at the right moment, such as when something needs your attention or when you want a message to stay visible in the interface. The examples below show two common ways to use notification actions in automations.
Tip
You don’t need to edit YAML to use these examples. Copy a YAML snippet from this page, open the automation editor in Home Assistant, and press `Ctrl`+`V` (or `Cmd`+`V` on Mac). Home Assistant automatically converts the pasted YAML into the visual editor format, whether it’s a full automation, a single trigger, a condition, or an action.
### Automation: send a notification when the garage door stays open 
This automation sends a message to your phone when the garage door has been open for 10 minutes.
  * **Trigger** : State 
    * **Entity** : Garage door (`binary_sensor.garage_door`)
    * **To** : On
    * **For** : 00:10:00
  * **Action** : Send a notification message 
    * **Target** : My Device (`notify.my_device`)
    * **Message** : The garage door has been open for 10 minutes.


YAML example for a garage door notification
AutomationAutomations in Home Assistant allow you to automatically respond to things that happen in and around your home.[ [Learn more]](https://www.home-assistant.io/docs/automation/)

```
alias: "Notify when the garage door stays open"
triggers:
  - trigger: state
    entity_id: binary_sensor.garage_door
    to: "on"
    for: "00:10:00"
actions:
  - action: notify.send_message
    target:
      entity_id: notify.my_device
    data:
      message: 
        The garage door has been open for 10 minutes.
```

YAML
Copy
### Automation: show a persistent notification when a leak is detected 
This automation shows a notification in the Home Assistant interface when a leak sensor detects moisture.
  * **Trigger** : State 
    * **Entity** : Kitchen leak sensor (`binary_sensor.kitchen_leak`)
    * **To** : On
  * **Action** : Send a persistent notification 
    * **Title** : Water leak detected
    * **Message** : The kitchen leak sensor detected moisture.


YAML example for a leak notification
AutomationAutomations in Home Assistant allow you to automatically respond to things that happen in and around your home.[ [Learn more]](https://www.home-assistant.io/docs/automation/)

```
alias: "Show a kitchen leak notification"
triggers:
  - trigger: state
    entity_id: binary_sensor.kitchen_leak
    to: "on"
actions:
  - action: notify.persistent_notification
    data:
      : "Water leak detected"
      message: "The kitchen leak sensor detected moisture."
```

YAML
Copy
## Testing a notification action 
After you set up a [notifier](https://www.home-assistant.io/integrations/#notifications), test its action in **Tools**.
  1. Go to [**Settings** > **Tools** > **Actions**](https://my.home-assistant.io/redirect/developer_services).
  2. From the **Action** dropdown menu, choose the action you want to test, such as **Send a notification message** or **Send a persistent notification**.
  3. If you are testing `notify.send_message`, select one or more targets using **Entity** , **Device** , **Area** , **Floor** , or **Label**.
  4. In **Message** , enter the notification text.
  5. Select **Perform action**.


####  **Help us improve our documentation**
Suggest an edit to this page, or provide/view feedback for this page. 


Back to top
