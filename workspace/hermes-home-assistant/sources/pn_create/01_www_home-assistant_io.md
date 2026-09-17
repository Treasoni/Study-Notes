---
url: "https://www.home-assistant.io/actions/persistent_notification.create/"
title: "Create notification - Home Assistant"
scraped_at: 2026-09-17T16:40:42+00:00
---

The **Create notification** action shows a persistent notification in the Home Assistant frontend. The notification stays visible until someone dismisses it, which makes it useful for messages that need attention, such as a reminder or a warning from an automation.
## Using this action from the user interface 
If you prefer building automations and scripts visually, Home Assistant walks you through this action step by step. You pick what to target, tweak a few options, and save. No YAML knowledge required.
To use this action in an automation or script:
  1. Go to [**Settings** > **Automations & scenes**](https://my.home-assistant.io/redirect/automations).
  2. Open an existing automation or script, or select **Create** to start a new one.
  3. If you’re setting up a new automation, add a trigger in the **When** section. Scripts don’t need a trigger.
  4. In the **Then do** section, select **Add action**.
  5. From the search box, search for and select **Persistent notification: Create**.
  6. Provide a **Message** and, if you want, a **Title** and a **Notification ID**.
  7. Select **Save**.


This action does not support targets. In the UI, you are not prompted to choose an area, device, entity, or label.
### Options in the UI 
Message
The body of the notification. Supports Markdown formatting.
Title (Optional)
The title of the notification.
Notification ID (Optional)
An identifier for the notification. When you reuse the same ID, the existing notification is overwritten instead of a new one being added.
## Using this action in YAML 
If you work directly in YAML, or you want to know exactly what Home Assistant does under the hood, this section has the technical reference. It lists the field names you use in YAML, their types, and which ones are required.
In YAML, refer to this action as `persistent_notification.create`. A basic example looks like this:
ActionActions are used in several places in Home Assistant. As part of a script or automation, actions define what is going to happen once a trigger is activated. In scripts, an action is called *sequence*.[ [Learn more]](https://www.home-assistant.io/docs/automation/action/)

```
action: persistent_notification.create
data:
  message: "Your message goes here"
  : "Custom subject"
```

YAML
Copy
This creates a notification with a fixed title and message.
### Options in YAML 
message string Required
The body of the notification. Supports Markdown formatting.
title string (Optional)
The title of the notification.
notification_id string (Optional)
An identifier for the notification. When you reuse the same ID, the existing notification is overwritten instead of a new one being added.
## Markdown support 
The message supports the [Markdown formatting syntax](https://daringfireball.net/projects/markdown/syntax). Some examples are:
  * Headline 1: `# Headline`
  * Headline 2: `## Headline`
  * Newline: `\n`
  * Bold: `**My bold text**`
  * Italic: `*My italic text*`
  * Link: `[Link](https://www.home-assistant.io/)`
  * Image: `![image](/local/my_image.jpg)`


Note
`/local/` in this context refers to the `.homeassistant/www/` folder.
## Show runtime information 
To show runtime information, use a [template](https://www.home-assistant.io/docs/templating/). For example:
ActionActions are used in several places in Home Assistant. As part of a script or automation, actions define what is going to happen once a trigger is activated. In scripts, an action is called *sequence*.[ [Learn more]](https://www.home-assistant.io/docs/automation/action/)

```
action: persistent_notification.create
data:
  : 
    Thermostat is {{ state_attr('climate.thermostat', 'hvac_action') }}
  message: "Temperature {{ state_attr('climate.thermostat', 'current_temperature') }}"
```

YAML
Copy
## Try it yourself 
Ready to test this? Open [**Settings** > **Tools** > **Actions**](https://my.home-assistant.io/redirect/developer_services), search for this action, fill in the fields, and select **Perform action**. You see what happens on your actual entitiesAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) without writing a line of YAML.
## Still stuck? 
The Home Assistant community is quick to help: join [Discord](https://discord.gg/home-assistant) for real-time chat, post on the [community forum](https://community.home-assistant.io) with the action you’re calling and what you expected to happen, or share on [our subreddit /r/homeassistant](https://reddit.com/r/homeassistant).
Tip
AI assistants like ChatGPT or Claude can also explain actions or suggest the right one when you describe what you want in plain language.
## Related actions 
These actions work well alongside this one:
  * [Dismiss notification](https://www.home-assistant.io/actions/persistent_notification.dismiss/): Removes a single persistent notification from the Home Assistant frontend.
  * [Dismiss all notifications](https://www.home-assistant.io/actions/persistent_notification.dismiss_all/): Removes all persistent notifications from the Home Assistant frontend.


####  **Help us improve our documentation**
Suggest an edit to this page, or provide/view feedback for this page. 


Back to top
