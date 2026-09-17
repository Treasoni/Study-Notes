---
url: "https://www.home-assistant.io/blog/2025/10/01/release-202510/"
title: "2025.10: Undo, redo, and draw me too - Home Assistant"
scraped_at: 2026-09-17T16:40:27+00:00
---

Boo! 👻
We just [celebrated our birthday](https://www.home-assistant.io/blog/2025/09/17/home-assistant-turns-12/) 🥳, which means it is time for spooky season; get ready for Halloween! And, hello to the October release of Home Assistant 2025.10! 🎃
This release iterates on some of the features we introduced in the last couple of releases, but also introduces some brand-new ones!
The highlight of this release is definitely the iterations of the automation editor, which gained a sidebar last release, and now has gained undo/redo functionality, a resizable sidebar, improved copy/paste, and more! Thanks for all the feedback you provided on the previous release; it made a massive difference in this release.
Using multiple wake words for voice assistants is now possible, which opens up a lot of possibilities, especially for dual-language households (like mine 😉). Dashboards get more intelligent by suggesting entities based on your usage patterns, and the AI Task can now generate images, which I’m curious to see what the community will do with it!
Enjoy the release!
../Frenck
  * [Automation editor](https://www.home-assistant.io/blog/2025/10/01/release-202510/#automation-editor)
    * [The sidebar is resizable](https://www.home-assistant.io/blog/2025/10/01/release-202510/#the-sidebar-is-resizable)
    * [The overflow menu is back](https://www.home-assistant.io/blog/2025/10/01/release-202510/#the-overflow-menu-is-back)
    * [Repeat repeat repeat repeat](https://www.home-assistant.io/blog/2025/10/01/release-202510/#repeat-repeat-repeat-repeat)
    * [Automation editor feedback](https://www.home-assistant.io/blog/2025/10/01/release-202510/#automation-editor-feedback)
  * [AI Task - Draw me a sheep](https://www.home-assistant.io/blog/2025/10/01/release-202510/#ai-task---draw-me-a-sheep)
  * [Dashboards get smarter - let your home suggest what to show](https://www.home-assistant.io/blog/2025/10/01/release-202510/#dashboards-get-smarter---let-your-home-suggest-what-to-show)
  * [Voice](https://www.home-assistant.io/blog/2025/10/01/release-202510/#voice)
  * [Integrations](https://www.home-assistant.io/blog/2025/10/01/release-202510/#integrations)
    * [New integrations](https://www.home-assistant.io/blog/2025/10/01/release-202510/#new-integrations)
    * [Noteworthy improvements to existing integrations](https://www.home-assistant.io/blog/2025/10/01/release-202510/#noteworthy-improvements-to-existing-integrations)
    * [Integration quality scale achievements](https://www.home-assistant.io/blog/2025/10/01/release-202510/#integration-quality-scale-achievements)
    * [Now available to set up from the UI](https://www.home-assistant.io/blog/2025/10/01/release-202510/#now-available-to-set-up-from-the-ui)
  * [Other noteworthy changes](https://www.home-assistant.io/blog/2025/10/01/release-202510/#other-noteworthy-changes)
    * [New more information dialog for media player entities](https://www.home-assistant.io/blog/2025/10/01/release-202510/#new-more-information-dialog-for-media-player-entities)
    * [Sync zooming charts in the history panel](https://www.home-assistant.io/blog/2025/10/01/release-202510/#sync-zooming-charts-in-the-history-panel)
    * [Template & YAML editors get a toolbar](https://www.home-assistant.io/blog/2025/10/01/release-202510/#template--yaml-editors-get-a-toolbar)
  * [Patch releases](https://www.home-assistant.io/blog/2025/10/01/release-202510/#patch-releases)
    * [2025.10.1 - October 3](https://www.home-assistant.io/blog/2025/10/01/release-202510/#2025101---october-3)
    * [2025.10.2 - October 10](https://www.home-assistant.io/blog/2025/10/01/release-202510/#2025102---october-10)
    * [2025.10.3 - October 17](https://www.home-assistant.io/blog/2025/10/01/release-202510/#2025103---october-17)
    * [2025.10.4 - October 24](https://www.home-assistant.io/blog/2025/10/01/release-202510/#2025104---october-24)
  * [Need help? Join the community](https://www.home-assistant.io/blog/2025/10/01/release-202510/#need-help-join-the-community)
  * [Backward-incompatible changes](https://www.home-assistant.io/blog/2025/10/01/release-202510/#backward-incompatible-changes)


_A huge thank you to all the contributors who made this release possible! And a special shout-out to[@JLo](https://github.com/jlpouffier), [@laupalombi](https://github.com/laupalombi), and [@piitaya](https://github.com/piitaya) who helped write the release notes this release. Also, [@googanhiem](https://github.com/googanhiem), [@SeraphicRav](https://github.com/SeraphicRav), [@tronikos](https://github.com/tronikos), and [@richardpolzer](https://github.com/richardpolzer) for putting effort into tweaking its contents. Thanks to them, these release notes are in great shape. ❤️_
## Automation editor 
In the [last release](https://www.home-assistant.io/blog/2025/09/03/release-20259/), we introduced a new layout for the automation editor, and your feedback has been invaluable in helping us refine it!
This release fixes a few of the most common issues we managed to gather from all of you. Thanks for all the feedback! ❤️
### The sidebar is resizable 
Working on an action that is too complex for a small sidebar? Maybe one with a few YAML fields? You can now resize the sidebar to adapt the layout to your current task!
### CTRL+V 
We previously introduced keyboard shortcuts to copy and cut.
Pasting was more complex to bring to life because you can paste a block (trigger, condition, action) in many different locations in your automation. In this release, we introduce a really simple pattern. If you previously copied a block, you can paste it below any block simply by selecting it and pressing CTRL+V.
Another very simple, but very welcome, quality-of-life improvement to the automation editor!
### The overflow menu is back 
We initially relocated the overflow menu (the menu that appears when you click the `⋮`) with all the options related to a block on the sidebar, thinking this would make the flow cleaner.
Due to popular demand and helpful feedback that some actions were more difficult to reach (such as testing a condition or running an action), we decided to bring it back to the main section of the editor as well.
### Undo/Redo 
We’ve all been there: you’re building a complex automation, make a mistake, and want to revert it, only to find out that it’s really not simple. Up until now, the only way to revert some unsaved changes made to an automation was to close it and start over again… A very painful workflow.
This release introduces an Undo functionality (and its associated Redo). You can now undo up to 75 steps back in your automation editing history (and redo them if you want). Standard keyboard shortcuts (CTRL+Z and CTRL+Y) are also available! An amazing contribution from [@jpbede](https://github.com/jpbede), thanks!
### Repeat repeat repeat repeat 
Finally, we noticed some unwanted complexity in our [“repeat” building block](https://www.home-assistant.io/docs/scripts/#repeat-a-group-of-actions), which allows you to repeat one or multiple actions for as long as you need to.
This complexity stemmed from the fact that we were trying to cover four main use cases in a single block.
We decided to split this building block into four smaller ones, with simpler descriptions explaining each use case. Nice!
Here’s how they were separated:
  * **Repeat multiple times** - Repeat a sequence of actions a fixed number of times.
  * **Repeat until** - Repeat a sequence of actions until a condition is satisfied. The condition is checked after each run of the sequence.
  * **Repeat while** - Repeat a sequence of actions as long as a condition is satisfied. The condition is checked before each run of the sequence.
  * **Repeat for each** - Repeat a sequence for each element of a list.


Note
For our advanced users: This evolution is only cosmetic. The YAML format of the repeat block does not change; this means your existing automations will not be affected by this change.
### Automation editor feedback 
Tip
One of Home Assistant’s greatest strengths is our community. We’re building this automation editor together, and your input will shape where it goes next. There are two ways to get involved:
  * [Share your thoughts in our survey](https://forms.gle/ATWcTAj8bMbiGfUE7)
  * [Join the conversation in the automations & scripts development channel on Discord](https://discord.com/channels/330944238910963714/1351529028112224359)


## AI Task - Draw me a sheep 
In [2025.8](https://www.home-assistant.io/blog/2025/08/06/release-20258/), we introduced [a way to generate data using the LLM of your choice](https://www.home-assistant.io/blog/2025/08/06/release-20258/#integrate-ai-into-your-workflow-using-ai-task), paving the way to more AI-driven automations, dashboards, and other smart home interactions.
In this release, we introduce a way to generate images!
Now every time someone rings your doorbell, you can receive a notification with a cartoon version of the doorbell snapshot. [@JLo](https://github.com/jlpouffier) has made this example a reality, and here’s his demo with the associated automation!
Automation details

```
alias: Demo Doorbell
triggers:
  - trigger: state
    entity_id:
      - binary_sensor.doorbell_demo
    to: "on"
actions:
  - action: notify.mobile_app_iphone
    data:
      title: "🔔 Doorbell "
      message: Processing image ...
      data:
        tag: doorbell
  - action: ai_task.generate_data
    data:
      task_name: Doorbell description
      instructions: |-
        Someone rang my doorbell.

        Instructions:
        - Describe the scene, describe every person on the scene
        - Count People
        - Count Animals
      entity_id: ai_task.ai_task_gpt_4o
      structure:
        summary:
          description: -
            Summary of the scene and the people inside it. Keep it under 180
            characters
          selector:
            text: null
        person_count:
          description: Number of person in the scene
          selector:
            number: null
        animal_count:
          description: Number of animal in the scene
          selector:
            number: null
      attachments:
        media_content_id: media-source://media_source/local/doorbell_test.png
        media_content_type: image/png
        metadata:
          title: doorbell_test.png
          thumbnail: null
          media_class: image
          children_media_class: null
          navigateIds:
            - {}
            - media_content_type: app
              media_content_id: media-source://media_source
    response_variable: ai
  - action: notify.mobile_app_iphone
    data:
      title: -
        🔔 Doorbell ({{ai.data.person_count}} 🧑🏻‍🦱 / {{ai.data.animal_count}}
        🐊)
      message: "{{ai.data.summary}}"
      data:
        tag: doorbell
  - action: ai_task.generate_image
    data:
      task_name: Manga
      instructions: Transform this image into a super cute manga!
      entity_id: ai_task.google_ai_task
      attachments:
        media_content_id: media-source://media_source/local/doorbell_test.png
        media_content_type: image/png
        metadata:
          title: doorbell_test.png
          thumbnail: null
          media_class: image
          children_media_class: null
          navigateIds:
            - {}
            - media_content_type: app
              media_content_id: media-source://media_source
    response_variable: ai_image
    enabled: true
  - action: notify.mobile_app_iphone
    data:
      title: -
        🔔 Doorbell ({{ai.data.person_count}} 🧑🏻‍🦱 / {{ai.data.animal_count}}
        🐊)
      message: "{{ai.data.summary}}"
      data:
        tag: doorbell
        image: http://homeassistant.local:8123{{ai_image.url}}
    enabled: true
mode: single
```

YAML
Copy
Image generation is already working great, and we cannot wait to see what you will build with this!
## Dashboards get smarter - let your home suggest what to show 
In the last release, we introduced the Home dashboard, offering a simpler way to control and monitor your smart home if you don’t have the time, energy, or need to customize your own dashboard in detail.
Now we’ve added a new concept: sections of suggested entities. This follows a basic algorithm that suggests entities you have interacted with the most in the past. It then shows these entities based on the hour of the day, with only relevant controls being suggested.
Adding prediction entities to any dashboard
If you’re creating a manual dashboard with sections, you can integrate these prediction controls directly into it. The setup follows a section-based approach:
  1. Add a new section.
  2. Open and edit the YAML of that section.
  3. Replace the entire section YAML with the following snippet:



```
strategy:
  type: common-controls
  title: Common controls
```

YAML
Copy
Tip
One of Home Assistant’s greatest strengths is our community. We’re building this dashboard together, and your input will shape where it goes next. There are two ways to get involved:
  * [Share your thoughts in our survey](https://docs.google.com/forms/d/e/1FAIpQLSd2pOf7WWNxmvcC8lH3NM5Ssf63y2pN3xP9HdlY09pr9goPqQ/viewform?usp=dialog)
  * [Join the conversation in the dashboard development channel on Discord](https://discord.com/channels/330944238910963714/1351536906437005313)


## Voice 
### Hello, hola 
For a very long time, ESPHome-based voice assistants (even the tiny Atom Echo) secretly [supported multiple wake words](https://www.home-assistant.io/blog/2024/06/26/voice-chapter-7/#3x-wake-words-and-2x-accuracy) under the hood. With this release, we’re finally opening up this feature to you!
You can now define two wake words and two assistants for every voice assistant in your home!
This makes it straightforward to support dual-language households by assigning different wake words to different languages. For example, _“Okay Nabu”_ could be used for French, while _“Hey Jarvis”_ is used for English.
Multiple wake words and assistants can be used for other purposes as well. Want to keep your local and cloud-based voice assistants separate? Easy! _“Okay Nabu”_ could be used for a cloud-based assistant while _“Hey Jarvis”_ is used for a local one.
We’d love to hear feedback on how you plan to use multiple wake words in your home!
### Beep boop 
After a voice command, Assist responds with a short confirmation like _“Turned on the lights”_ or _“Brightness set”_. This lets you know that it understood your command and took the appropriate actions. However, if you’re in the same room as the voice assistant, this confirmation can feel redundant since you can see or hear that the appropriate actions were taken.
Starting with this release, Assist will detect if your voice command’s actions all took place within the same area as the satellite device. If so, a short confirmation “beep” will be played instead of the full verbal response. Besides being less verbose, this also serves as a quick reminder that your voice command only affected the current area.
Note
This feature does not work for AI-enabled Assistants, as they can generate a wide variety of responses that can’t be replaced with a simple beep.
## Integrations 
Thanks to our community for keeping pace with the new integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) and improvements to existing ones! You’re all awesome 🥰
### New integrations 
We welcome the following new integrations in this release:
  * , added by [@Przemko92](https://github.com/Przemko92) The Compit integration allows you to integrate air conditioning, ventilation, and heating controllers with Home Assistant.
  * , added by [@Kinachi249](https://github.com/Kinachi249) Connect your GE Lighting Cync smart devices—including smart lighting (formerly known as C by GE)—with Home Assistant.
  * , added by [@sarahseidman](https://github.com/sarahseidman) Connect your Droplet devices to Home Assistant. Droplet accurately monitors your home’s water usage in real time.
  * , added by [@richardpolzer](https://github.com/richardpolzer) Integrate your ekey bionyx biometric access control systems to receive events for individual finger scans and digital inputs in your smart home.
  * , added by [@jdejaegh](https://github.com/jdejaegh) Get accurate weather data from Belgium’s Royal Meteorological Institute (IRM-KMI) for precise regional forecasting.
  * **[Libre Hardware Monitor](https://www.home-assistant.io/integrations/libre_hardware_monitor)** , added by [@Sab44](https://github.com/Sab44) Monitor your computer’s hardware sensors, including CPU temperature, GPU usage, fan speeds, and system performance metrics.
  * , added by [@erwindouna](https://github.com/erwindouna) Manage and monitor your Docker containers, keeping track of the status of your running containers.
  * **[Smart Meter B Route](https://www.home-assistant.io/integrations/route_b_smart_meter)** , added by [@SeraphicRav](https://github.com/SeraphicRav) Connect your smart meter via the B Route protocol—designed for the Japanese market—to access real-time energy consumption data.
  * , added by [@maretodoric](https://github.com/maretodoric) Set up secure remote backup locations using SFTP/SSH protocols for your Home Assistant backups and data storage.
  * **[Usage Prediction](https://www.home-assistant.io/integrations/usage_prediction)** , added by [@balloob](https://github.com/balloob) An internal integration that provides predictions of what entities you are most likely to interact with. Used by our new Home dashboard.
  * **[Victron Remote Monitoring](https://www.home-assistant.io/integrations/victron_remote_monitoring)** , added by [@AndyTempel](https://github.com/AndyTempel) The Victron Remote Monitoring (VRM) integration pulls site statistics and solar production and consumption forecasts from Victron Energy’s VRM portal.


### Noteworthy improvements to existing integrations 
It is not just new integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) that have been added; existing integrations are also being constantly improved. Here are some of the noteworthy changes to existing integrations:
  * [Philips Hue](https://www.home-assistant.io/integrations/hue) expanded with support for MotionAware sensors on the new [Hue Bridge Pro](https://www.philips-hue.com/nl-nl/p/hue-hue-bridge-pro/8720169155114)! Thanks, [@marcelveldt](https://github.com/marcelveldt)!
  * [LG](https://github.com/LG-ThinQ-Integration) added support to the [LG ThinQ](https://www.home-assistant.io/integrations/lg_thinq) integration to now provide energy usage sensors for better energy monitoring of your devices! Nice!
  * Amazing work from [@natekspencer](https://github.com/natekspencer): [Litter-Robot](https://www.home-assistant.io/integrations/litterrobot) got several enhancements: last feeding sensors, food dispensed today tracking, next feeding sensors, gravity mode switch, and globe light settings for Litter-Robot 4!
  * [AccuWeather](https://www.home-assistant.io/integrations/accuweather) now provides hourly forecasts, giving you more detailed weather predictions throughout the day! Thanks, [@bieniu](https://github.com/bieniu)!
  * The [Blue Current](https://www.home-assistant.io/integrations/blue_current) integration got a new start charge session action for managing your EV charging! Nice work, [@NickKoepr](https://github.com/NickKoepr)!
  * The [Ecowitt](https://www.home-assistant.io/integrations/ecowitt) integration now supports the LDS01 sensor! Great addition, [@GSzabados](https://github.com/GSzabados)!
  * [Reolink](https://www.home-assistant.io/integrations/reolink) cameras got several new features including encoding select entity, Home Hub siren support, and color temperature support for light entities! Awesome work from [@starkillerOG](https://github.com/starkillerOG)!
  * Geocaching enthusiasts will love the new cache sensors added to the [Geocaching](https://www.home-assistant.io/integrations/geocaching) integration by [@marc7s](https://github.com/marc7s)! Nice if you have hidden one!
  * [Lutron Caseta](https://www.home-assistant.io/integrations/lutron_caseta) now supports multi-tap actions for more advanced button control! Thanks, [@rlopezdiez](https://github.com/rlopezdiez)!
  * Thanks to [@alexqzd](https://github.com/alexqzd), [SmartThings](https://www.home-assistant.io/integrations/smartthings) air conditioners can now control the AC display light!
  * [Shelly](https://www.home-assistant.io/integrations/shelly) devices received massive updates including illuminance sensor for Plug US Gen4, presence component entities, virtual buttons support, object-based entities, presence zone component support, and cable unplugged sensor for Flood Gen4! Great work from [@chemelli74](https://github.com/chemelli74), [@bieniu](https://github.com/bieniu), and [@thecode](https://github.com/thecode)!
  * The [SwitchBot](https://www.home-assistant.io/integrations/switchbot) integration expanded device support with Plug Mini EU, RelaySwitch 2PM, and K11+ Vacuum! Thanks, [@zerzhang](https://github.com/zerzhang)!
  * The [SwitchBot Cloud](https://www.home-assistant.io/integrations/switchbot_cloud) integration got several improvements including AC off support, humidifier platform, Plug-Mini-EU support, and Climate Panel support! Great work from [@SeraphicRav](https://github.com/SeraphicRav) and [@XiaoLing-git](https://github.com/XiaoLing-git)!
  * Thanks to [@timmo001](https://github.com/timmo001), the [System Bridge](https://www.home-assistant.io/integrations/system_bridge) integration now includes a power usage sensor for better system monitoring!
  * Exciting to see that the [Tasmota](https://www.home-assistant.io/integrations/tasmota) integration now supports camera functionality! Nice addition from [@anishsane](https://github.com/anishsane)!
  * Using the [Tibber](https://www.home-assistant.io/integrations/tibber) integration? It now provides 15-minute price data, which goes into effect on October 1st. Good timing, [@Danielhiversen](https://github.com/Danielhiversen)!
  * The [Tuya](https://www.home-assistant.io/integrations/tuya) integration received extensive updates with support for various new device categories and sensors: energy sensors for TDQ devices, power sensors for ZNDB devices, energy sensors for DLQ devices, solar inverter support, energy consumption for several smart switches, PM10 air quality monitoring, motor rotation mode for curtains that support it, charge state for siren alarms, cooking thermometer support, cat toilet support, electric desk support, white noise machine support, and water quality sensor support! What an impressive list! Thanks, [@zzysszzy](https://github.com/zzysszzy), [@rokam](https://github.com/rokam), and [@mhalano](https://github.com/mhalano)!
  * The [Workday](https://www.home-assistant.io/integrations/workday) integration now has a calendar that you can view from the calendar sidebar! Thanks, [@gjohansson-ST](https://github.com/gjohansson-ST)!
  * The [ntfy](https://www.home-assistant.io/integrations/ntfy) integration got a big upgrade! You can now send richer, customizable notifications with tags, icons, URLs, and attachments. Plus, with the new event platform, you can subscribe to topics and trigger automations from incoming messages. Thanks, [@tr4nt0r](https://github.com/tr4nt0r)!


### Integration quality scale achievements 
One thing we are incredibly proud of in Home Assistant is our [integration quality scale](https://www.home-assistant.io/docs/quality_scale/). This scale helps us and our contributors to ensure integrations are of high quality, maintainable, and provide the best possible user experience.
This release, we celebrate several integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) that have improved their quality scale:
  * **3 integrations reached platinum** 🏆
    * [Android TV Remote](https://www.home-assistant.io/integrations/androidtv_remote), thanks to [@tronikos](https://github.com/tronikos)
    * [Miele](https://www.home-assistant.io/integrations/miele), thanks to [@astrandb](https://github.com/astrandb)
    * [Sleep as Android](https://www.home-assistant.io/integrations/sleep_as_android), thanks to [@tr4nt0r](https://github.com/tr4nt0r)
  * **2 integrations reached silver** 🥈
    * [Samsung Smart TV](https://www.home-assistant.io/integrations/samsungtv), thanks to [@chemelli74](https://github.com/chemelli74)
    * [Whirlpool Appliances](https://www.home-assistant.io/integrations/whirlpool), thanks to [@abmantis](https://github.com/abmantis)
  * **3 integrations reached bronze** 🥉
    * [NextDNS](https://www.home-assistant.io/integrations/nextdns), thanks to [@bieniu](https://github.com/bieniu)
    * [Opower](https://www.home-assistant.io/integrations/opower), thanks to [@tronikos](https://github.com/tronikos)
    * [Sonos](https://www.home-assistant.io/integrations/sonos), thanks to [@PeteRager](https://github.com/PeteRager)


This is a huge achievement for these integrations and their maintainers. The effort and dedication required to reach these quality levels is significant, as it involves extensive testing, documentation, error handling, and often complete rewrites of parts of the integration.
A big thank you to all the contributors involved! 👏
### Now available to set up from the UI 
While most integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) can be set up directly from the Home Assistant user interface, some were only available using YAML configuration. We keep moving more integrations to the UI, making them more accessible for everyone to set up and use.
The following integrations are now available via the Home Assistant UI:
  * **[Nederlandse Spoorwegen (NS)](https://www.home-assistant.io/integrations/nederlandse_spoorwegen)** , done by [@heindrichpaul](https://github.com/heindrichpaul)
  * , done by [@Tommatheussen](https://github.com/Tommatheussen)


## Other noteworthy changes 
There are many more improvements in this release; here are some of the other noteworthy changes:
  * The “Logbook” has been renamed to “Activity” in the UI. This better reflects its purpose of showing a timeline of activities and events in your Home Assistant instance.
  * [Matter](https://www.home-assistant.io/integrations/matter) continues to expand with occupancy sensing hold time, climate running state for heat/cool fans, and thermostat outdoor temperature sensors! Great contributions from [@lboue](https://github.com/lboue) and [@virtualbitzz](https://github.com/virtualbitzz)!
  * Lawn mower entities now support start mowing and dock intents for better voice control! Thanks, [@piitaya](https://github.com/piitaya)!
  * The [analog clock](https://www.home-assistant.io/blog/2025/09/03/release-20259/#analog-clock) we introduced last release got some more options! You can now enable a smooth motion for the seconds hand. Beautiful, [@timmo001](https://github.com/timmo001)!
  * Need the version of the [Home Assistant Mobile Companion App](https://companion.home-assistant.io/) you are using? If you have installed the latest versions of our apps, the version is now shown on the about page in the settings menu! Nice one, [@TimoPtr](https://github.com/TimoPtr)!
  * The [thermostat card](https://www.home-assistant.io/dashboards/thermostat/) now supports [water heater entities](https://www.home-assistant.io/integrations/water_heater/). Thanks, [@karwosts](https://github.com/karwosts)!
  * Thanks to [@cr7pt0gr4ph7](https://github.com/cr7pt0gr4ph7), the add-on configuration UI has gotten support for more complex configurations; this means you will get a better experience when configuring add-ons with more complex options (like lists or user accounts). Well done!
  * Talking about add-ons, we now include switch entities for those, making it easier to control your add-ons. Thanks, [@felipecrs](https://github.com/felipecrs)!
  * Using a [webhook trigger](https://www.home-assistant.io/docs/automation/trigger/#webhook-trigger) in your automation? You can now make it even more dynamic by using a template for the `webhook_id`. Thanks, [@RoboMagus](https://github.com/RoboMagus)!
  * We now have support for `MCF` (1000 Cubic Feet) as an alternate unit of measure for volume, thanks to [@ekobres](https://github.com/ekobres), [@xtimmy86x](https://github.com/xtimmy86x) added `m/min` for speed sensors, and [@pioto](https://github.com/pioto) added `inH₂O` pressure unit support. Nice!


### New more information dialog for media player entities 
This one, we have [@jpbede](https://github.com/jpbede) and [@matthiasdebaat](https://github.com/matthiasdebaat) to thank for! The ‘more information’ dialogs for media players have a revamped design, offering a cleaner and more intuitive interface.
### Sync zooming charts in the history panel 
When you have multiple charts in the history panel, zooming in on one chart will now automatically zoom in on all other charts as well. This makes it easier to compare data across different entities. Well done, [@birrejan](https://github.com/birrejan)!
### Template & YAML editors get a toolbar 
[@TCWORLD](https://github.com/TCWORLD) has contributed a toolbar for the YAML and template code editors in our UI. This solves an issue where the previous floating button would float over the content of the editor and obscure it from view.
The new toolbar also includes undo and redo buttons, bringing [the same convenient undo and redo functionality](https://www.home-assistant.io/blog/2025/10/01/release-202510/#undoredo) we introduced for the automation editor to these code editors as well. Plus, there’s a nice little copy button to quickly copy your code! Nice!
## Patch releases 
We will also release patch releases for Home Assistant 2025.10 in October. These patch releases only contain bug fixes. Our goal is to release a patch release once a week, aiming for Friday.
### 2025.10.1 - October 3 
  * Bump airOS dependency ([@CoMPaTech](https://github.com/CoMPaTech) - [#153065](https://github.com/home-assistant/core/pull/153065))
  * Bump airOS module for alternative login url ([@CoMPaTech](https://github.com/CoMPaTech) - [#153317](https://github.com/home-assistant/core/pull/153317))
  * Bump aiohasupervisor to 0.3.3 ([@agners](https://github.com/agners) - [#153344](https://github.com/home-assistant/core/pull/153344))
  * Do not reset the adapter twice during ZHA options flow migration ([@puddly](https://github.com/puddly) - [#153345](https://github.com/home-assistant/core/pull/153345))
  * Fix Nord Pool 15 minute interval ([@gjohansson-ST](https://github.com/gjohansson-ST) - [#153350](https://github.com/home-assistant/core/pull/153350))
  * Explicitly check for None in raw value processing of modbus ([@alengwenus](https://github.com/alengwenus) - [#153352](https://github.com/home-assistant/core/pull/153352))
  * Set config entry to None in ProxmoxVE ([@mib1185](https://github.com/mib1185) - [#153357](https://github.com/home-assistant/core/pull/153357))
  * Explicit pass in the config entry to coordinator in airtouch4 ([@mib1185](https://github.com/mib1185) - [#153361](https://github.com/home-assistant/core/pull/153361))
  * Add Roborock mop intensity translations ([@starkillerOG](https://github.com/starkillerOG) - [#153380](https://github.com/home-assistant/core/pull/153380))
  * Correct blocking update in ToGrill with lack of notifications ([@elupus](https://github.com/elupus) - [#153387](https://github.com/home-assistant/core/pull/153387))
  * Bump python-roborock to 2.49.1 ([@Lash-L](https://github.com/Lash-L) - [#153396](https://github.com/home-assistant/core/pull/153396))
  * Pushover: Handle empty data section properly ([@linuxkidd](https://github.com/linuxkidd) - [#153397](https://github.com/home-assistant/core/pull/153397))
  * Increase onedrive upload chunk size ([@zweckj](https://github.com/zweckj) - [#153406](https://github.com/home-assistant/core/pull/153406))
  * Bump pyportainer 1.0.2 ([@erwindouna](https://github.com/erwindouna) - [#153326](https://github.com/home-assistant/core/pull/153326))
  * Bump pyportainer 1.0.3 ([@erwindouna](https://github.com/erwindouna) - [#153413](https://github.com/home-assistant/core/pull/153413))
  * Disable thinking for unsupported gemini models ([@Shulyaka](https://github.com/Shulyaka) - [#153415](https://github.com/home-assistant/core/pull/153415))
  * Fix Satel Integra creating new binary sensors on YAML import ([@Tommatheussen](https://github.com/Tommatheussen) - [#153419](https://github.com/home-assistant/core/pull/153419))
  * Update `markdown` field description in ntfy integration ([@tr4nt0r](https://github.com/tr4nt0r) - [#153421](https://github.com/home-assistant/core/pull/153421))
  * Fix Z-Wave RGB light turn on causing rare `ZeroDivisionError` ([@TheJulianJES](https://github.com/TheJulianJES) - [#153422](https://github.com/home-assistant/core/pull/153422))
  * Bump aiohomekit to 3.2.19 ([@bdraco](https://github.com/bdraco) - [#153423](https://github.com/home-assistant/core/pull/153423))
  * Fix sentence-casing in user-facing strings of `slack` ([@NoRi2909](https://github.com/NoRi2909) - [#153427](https://github.com/home-assistant/core/pull/153427))
  * Add missing translation for media browser default title ([@timmo001](https://github.com/timmo001) - [#153430](https://github.com/home-assistant/core/pull/153430))
  * Fix missing powerconsumptionreport in Smartthings ([@joostlek](https://github.com/joostlek) - [#153438](https://github.com/home-assistant/core/pull/153438))
  * Update Home Assistant base image to 2025.10.0 ([@agners](https://github.com/agners) - [#153441](https://github.com/home-assistant/core/pull/153441))
  * Disable baudrate bootloader reset for ZBT-2 ([@puddly](https://github.com/puddly) - [#153443](https://github.com/home-assistant/core/pull/153443))
  * Add translation for turbo fan mode in SmartThings ([@joostlek](https://github.com/joostlek) - [#153445](https://github.com/home-assistant/core/pull/153445))
  * Fix next event in workday calendar ([@gjohansson-ST](https://github.com/gjohansson-ST) - [#153465](https://github.com/home-assistant/core/pull/153465))
  * Update OVOEnergy to 3.0.1 ([@timmo001](https://github.com/timmo001) - [#153476](https://github.com/home-assistant/core/pull/153476))
  * Fix missing parameter pass in onedrive ([@zweckj](https://github.com/zweckj) - [#153478](https://github.com/home-assistant/core/pull/153478))
  * Bump pyTibber to 0.32.2 ([@Danielhiversen](https://github.com/Danielhiversen) - [#153484](https://github.com/home-assistant/core/pull/153484))
  * Bump reolink-aio to 0.16.1 ([@starkillerOG](https://github.com/starkillerOG) - [#153489](https://github.com/home-assistant/core/pull/153489))
  * Fix VeSync zero fan speed handling ([@cdnninja](https://github.com/cdnninja) - [#153493](https://github.com/home-assistant/core/pull/153493))
  * Bump universal-silabs-flasher to 0.0.35 ([@puddly](https://github.com/puddly) - [#153500](https://github.com/home-assistant/core/pull/153500))
  * Debounce updates in Idasen Desk ([@abmantis](https://github.com/abmantis) - [#153503](https://github.com/home-assistant/core/pull/153503))
  * Z-Wave to support migrating from USB to socket with same home ID ([@balloob](https://github.com/balloob) - [#153522](https://github.com/home-assistant/core/pull/153522))
  * When discovering a Z-Wave adapter, always configure add-on in config flow ([@balloob](https://github.com/balloob) - [#153575](https://github.com/home-assistant/core/pull/153575))


### 2025.10.2 - October 10 
  * Prevent reloading the ZHA integration while adapter firmware is being updated ([@puddly](https://github.com/puddly) - [#152626](https://github.com/home-assistant/core/pull/152626))
  * Wallbox fix Rate Limit issue for multiple chargers ([@hesselonline](https://github.com/hesselonline) - [#153074](https://github.com/home-assistant/core/pull/153074))
  * Fix power device classes for system bridge ([@timmo001](https://github.com/timmo001) - [#153201](https://github.com/home-assistant/core/pull/153201))
  * Bump PyCync to 0.4.1 ([@Kinachi249](https://github.com/Kinachi249) - [#153401](https://github.com/home-assistant/core/pull/153401))
  * Updated VRM client and accounted for missing forecasts ([@AndyTempel](https://github.com/AndyTempel) - [#153464](https://github.com/home-assistant/core/pull/153464))
  * Bump python-roborock to 2.50.2 ([@Lash-L](https://github.com/Lash-L) - [#153561](https://github.com/home-assistant/core/pull/153561))
  * Bump aioamazondevices to 6.2.8 ([@chemelli74](https://github.com/chemelli74) - [#153592](https://github.com/home-assistant/core/pull/153592))
  * Switch Roborock to v4 of the code login api ([@Lash-L](https://github.com/Lash-L) - [#153593](https://github.com/home-assistant/core/pull/153593))
  * Fix MQTT Lock state reset to unknown when a reset payload is received ([@jbouwh](https://github.com/jbouwh) - [#153647](https://github.com/home-assistant/core/pull/153647))
  * Gemini: Use default model instead of recommended where applicable ([@Shulyaka](https://github.com/Shulyaka) - [#153676](https://github.com/home-assistant/core/pull/153676))
  * Fix ViCare pressure sensors missing unit of measurement ([@CFenner](https://github.com/CFenner) - [#153691](https://github.com/home-assistant/core/pull/153691))
  * Bump pyvesync to 3.1.0 ([@cdnninja](https://github.com/cdnninja) - [#153693](https://github.com/home-assistant/core/pull/153693))
  * Modbus Fix message_wait_milliseconds is no longer applied ([@peetersch](https://github.com/peetersch) - [#153709](https://github.com/home-assistant/core/pull/153709))
  * Bump opower to 0.15.6 ([@tronikos](https://github.com/tronikos) - [#153714](https://github.com/home-assistant/core/pull/153714))
  * Version bump pydaikin to 2.17.0 ([@fredrike](https://github.com/fredrike) - [#153718](https://github.com/home-assistant/core/pull/153718))
  * Version bump pydaikin to 2.17.1 ([@fredrike](https://github.com/fredrike) - [#153726](https://github.com/home-assistant/core/pull/153726))
  * Fix missing google_assistant_sdk.send_text_command ([@tronikos](https://github.com/tronikos) - [#153735](https://github.com/home-assistant/core/pull/153735))
  * Bump airOS to 0.5.5 using formdata for v6 firmware ([@CoMPaTech](https://github.com/CoMPaTech) - [#153736](https://github.com/home-assistant/core/pull/153736))
  * Align Shelly `presencezone` entity to the new API/firmware ([@bieniu](https://github.com/bieniu) - [#153737](https://github.com/home-assistant/core/pull/153737))
  * Synology DSM: Don’t reinitialize API during configuration ([@oyvindwe](https://github.com/oyvindwe) - [#153739](https://github.com/home-assistant/core/pull/153739))
  * Upgrade python-melcloud to 0.1.2 ([@Sander0542](https://github.com/Sander0542) - [#153742](https://github.com/home-assistant/core/pull/153742))
  * Fix sensors availability check for Alexa Devices ([@chemelli74](https://github.com/chemelli74) - [#153743](https://github.com/home-assistant/core/pull/153743))
  * Bump aioamazondevices to 6.2.9 ([@chemelli74](https://github.com/chemelli74) - [#153756](https://github.com/home-assistant/core/pull/153756))
  * Remove stale entities from Alexa Devices ([@chemelli74](https://github.com/chemelli74) - [#153759](https://github.com/home-assistant/core/pull/153759))
  * vesync correct fan set modes ([@cdnninja](https://github.com/cdnninja) - [#153761](https://github.com/home-assistant/core/pull/153761))
  * Handle ESPHome discoveries with uninitialized Z-Wave antennas ([@balloob](https://github.com/balloob) - [#153790](https://github.com/home-assistant/core/pull/153790))
  * Fix Tuya cover position when only control is available ([@epenet](https://github.com/epenet) - [#153803](https://github.com/home-assistant/core/pull/153803))
  * Bump pySmartThings to 3.3.1 ([@joostlek](https://github.com/joostlek) - [#153826](https://github.com/home-assistant/core/pull/153826))
  * Catch update exception in AirGradient ([@joostlek](https://github.com/joostlek) - [#153828](https://github.com/home-assistant/core/pull/153828))
  * Add motion presets to SmartThings AC ([@joostlek](https://github.com/joostlek) - [#153830](https://github.com/home-assistant/core/pull/153830))
  * Fix delay_on and auto_off with multiple triggers ([@Petro31](https://github.com/Petro31) - [#153839](https://github.com/home-assistant/core/pull/153839))
  * Fix PIN validation for Comelit SimpleHome ([@chemelli74](https://github.com/chemelli74) - [#153840](https://github.com/home-assistant/core/pull/153840))
  * Bump aiocomelit to 1.1.1 ([@chemelli74](https://github.com/chemelli74) - [#153843](https://github.com/home-assistant/core/pull/153843))
  * Limit SimpliSafe websocket connection attempts during startup ([@bachya](https://github.com/bachya) - [#153853](https://github.com/home-assistant/core/pull/153853))
  * Handle timeout errors gracefully in Nord Pool services ([@gjohansson-ST](https://github.com/gjohansson-ST) - [#153856](https://github.com/home-assistant/core/pull/153856))
  * Add plate_count for Miele KM7575 ([@derytive](https://github.com/derytive) - [#153868](https://github.com/home-assistant/core/pull/153868))
  * Fix restore cover state for Comelit SimpleHome ([@chemelli74](https://github.com/chemelli74) - [#153887](https://github.com/home-assistant/core/pull/153887))
  * fix typo in icon assignment of AccuWeather integration ([@CFenner](https://github.com/CFenner) - [#153890](https://github.com/home-assistant/core/pull/153890))
  * Add missing translation string for Satel Integra subentry type ([@Tommatheussen](https://github.com/Tommatheussen) - [#153905](https://github.com/home-assistant/core/pull/153905))
  * Do not auto-set up ZHA zeroconf discoveries during onboarding ([@TheJulianJES](https://github.com/TheJulianJES) - [#153914](https://github.com/home-assistant/core/pull/153914))
  * `sharkiq` dependency bump to 1.4.2 ([@Freebien](https://github.com/Freebien) - [#153931](https://github.com/home-assistant/core/pull/153931))
  * Fix HA hardware configuration message for Thread without HAOS ([@TheJulianJES](https://github.com/TheJulianJES) - [#153933](https://github.com/home-assistant/core/pull/153933))
  * Adjust OTBR config entry name for ZBT-2 ([@TheJulianJES](https://github.com/TheJulianJES) - [#153940](https://github.com/home-assistant/core/pull/153940))
  * Bump pylamarzocco to 2.1.2 ([@zweckj](https://github.com/zweckj) - [#153950](https://github.com/home-assistant/core/pull/153950))
  * Bump holidays to 0.82 ([@gjohansson-ST](https://github.com/gjohansson-ST) - [#153952](https://github.com/home-assistant/core/pull/153952))
  * Fix update interval for AccuWeather hourly forecast ([@bieniu](https://github.com/bieniu) - [#153957](https://github.com/home-assistant/core/pull/153957))
  * Bump env-canada to 0.11.3 ([@michaeldavie](https://github.com/michaeldavie) - [#153967](https://github.com/home-assistant/core/pull/153967))
  * Fix empty llm api list in chat log ([@arturpragacz](https://github.com/arturpragacz) - [#153996](https://github.com/home-assistant/core/pull/153996))
  * Don’t mark ZHA coordinator as via_device with itself ([@joostlek](https://github.com/joostlek) - [#154004](https://github.com/home-assistant/core/pull/154004))
  * Filter out invalid Renault vehicles ([@epenet](https://github.com/epenet) - [#154070](https://github.com/home-assistant/core/pull/154070))
  * Bump aioamazondevices to 6.4.0 ([@chemelli74](https://github.com/chemelli74) - [#154071](https://github.com/home-assistant/core/pull/154071))
  * Bump brother to version 5.1.1 ([@bieniu](https://github.com/bieniu) - [#154080](https://github.com/home-assistant/core/pull/154080))
  * Fix for multiple Lyrion Music Server on a single Home Assistant server for Squeezebox ([@peteS-UK](https://github.com/peteS-UK) - [#154081](https://github.com/home-assistant/core/pull/154081))
  * Z-Wave: ESPHome discovery to update all options ([@balloob](https://github.com/balloob) - [#154113](https://github.com/home-assistant/core/pull/154113))
  * Add missing entity category and icons for smlight integration ([@piitaya](https://github.com/piitaya) - [#154131](https://github.com/home-assistant/core/pull/154131))
  * Update frontend to 20251001.2 ([@bramkragten](https://github.com/bramkragten) - [#154143](https://github.com/home-assistant/core/pull/154143))
  * IOmeter bump version v0.2.0 ([@jukrebs](https://github.com/jukrebs) - [#154150](https://github.com/home-assistant/core/pull/154150))
  * Bump deebot-client to 15.1.0 ([@edenhaus](https://github.com/edenhaus) - [#154154](https://github.com/home-assistant/core/pull/154154))
  * Fix Shelly RPC cover update when the device is not initialized ([@thecode](https://github.com/thecode) - [#154159](https://github.com/home-assistant/core/pull/154159))
  * Fix shelly remove orphaned entities ([@thecode](https://github.com/thecode) - [#154182](https://github.com/home-assistant/core/pull/154182))


### 2025.10.3 - October 17 
  * Bump aioasuswrt to 1.5.1 ([@kennedyshead](https://github.com/kennedyshead) - [#153209](https://github.com/home-assistant/core/pull/153209))
  * PushSafer: Handle empty data section properly ([@LennartC](https://github.com/LennartC) - [#154109](https://github.com/home-assistant/core/pull/154109))
  * Remove redudant state write in Smart Meter Texas ([@srirams](https://github.com/srirams) - [#154126](https://github.com/home-assistant/core/pull/154126))
  * Fix state class for Overkiz water consumption ([@Yvan13120](https://github.com/Yvan13120) - [#154164](https://github.com/home-assistant/core/pull/154164))
  * Bump frontend 20251001.4 ([@piitaya](https://github.com/piitaya) - [#154218](https://github.com/home-assistant/core/pull/154218))
  * Bump aioamazondevices to 6.4.1 ([@chemelli74](https://github.com/chemelli74) - [#154228](https://github.com/home-assistant/core/pull/154228))
  * Move URL out of Mealie strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154230](https://github.com/home-assistant/core/pull/154230))
  * Move URL out of Mastodon strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154231](https://github.com/home-assistant/core/pull/154231))
  * Move URL out of Switcher strings.json ([@thecode](https://github.com/thecode) - [#154240](https://github.com/home-assistant/core/pull/154240))
  * Remove URL from ViCare strings.json ([@CFenner](https://github.com/CFenner) - [#154243](https://github.com/home-assistant/core/pull/154243))
  * Fix August integration to handle unavailable OAuth implementation at startup ([@bdraco](https://github.com/bdraco) - [#154244](https://github.com/home-assistant/core/pull/154244))
  * Fix Yale integration to handle unavailable OAuth implementation at startup ([@bdraco](https://github.com/bdraco) - [#154245](https://github.com/home-assistant/core/pull/154245))
  * Move url like strings to placeholders for nibe ([@elupus](https://github.com/elupus) - [#154249](https://github.com/home-assistant/core/pull/154249))
  * Add description placeholders in Uptime Kuma config flow ([@tr4nt0r](https://github.com/tr4nt0r) - [#154252](https://github.com/home-assistant/core/pull/154252))
  * Add description placeholders to pyLoad config flow ([@tr4nt0r](https://github.com/tr4nt0r) - [#154254](https://github.com/home-assistant/core/pull/154254))
  * Fix home wiziard total increasing sensors returning 0 ([@jbouwh](https://github.com/jbouwh) - [#154264](https://github.com/home-assistant/core/pull/154264))
  * Bump pyprobeplus to 1.1.0 ([@pantherale0](https://github.com/pantherale0) - [#154265](https://github.com/home-assistant/core/pull/154265))
  * Update Snoo strings.json to include weaning_baseline ([@dschafer](https://github.com/dschafer) - [#154268](https://github.com/home-assistant/core/pull/154268))
  * Move Electricity Maps url out of strings.json ([@jpbede](https://github.com/jpbede) - [#154284](https://github.com/home-assistant/core/pull/154284))
  * Bump aioamazondevices to 6.4.3 ([@chemelli74](https://github.com/chemelli74) - [#154293](https://github.com/home-assistant/core/pull/154293))
  * Move URL out of Overkiz Config Flow descriptions ([@iMicknl](https://github.com/iMicknl) - [#154315](https://github.com/home-assistant/core/pull/154315))
  * AsusWRT: Pass only online clients to the device list from the API ([@Vaskivskyi](https://github.com/Vaskivskyi) - [#154322](https://github.com/home-assistant/core/pull/154322))
  * Move Ecobee authorization URL out of strings.json ([@ogruendel](https://github.com/ogruendel) - [#154332](https://github.com/home-assistant/core/pull/154332))
  * Move URLs out of SABnzbd strings.json ([@shaiu](https://github.com/shaiu) - [#154333](https://github.com/home-assistant/core/pull/154333))
  * Move developer url out of strings.json for coinbase setup flow ([@ogruendel](https://github.com/ogruendel) - [#154339](https://github.com/home-assistant/core/pull/154339))
  * Fix Bluetooth discovery for devices with alternating advertisement names ([@bdraco](https://github.com/bdraco) - [#154347](https://github.com/home-assistant/core/pull/154347))
  * Bump opower to 0.15.7 ([@tronikos](https://github.com/tronikos) - [#154351](https://github.com/home-assistant/core/pull/154351))
  * update pysqueezebox lib to 0.13.0 ([@wollew](https://github.com/wollew) - [#154358](https://github.com/home-assistant/core/pull/154358))
  * Move URL out of sfr_box strings.json ([@epenet](https://github.com/epenet) - [#154364](https://github.com/home-assistant/core/pull/154364))
  * Move translatable URLs out of strings.json for huawei lte ([@sonianuj287](https://github.com/sonianuj287) - [#154368](https://github.com/home-assistant/core/pull/154368))
  * Bump aioairq to 0.4.7 ([@Sibgatulin](https://github.com/Sibgatulin) - [#154386](https://github.com/home-assistant/core/pull/154386))
  * Bump aiocomelit to 1.1.2 ([@chemelli74](https://github.com/chemelli74) - [#154393](https://github.com/home-assistant/core/pull/154393))
  * Use `async_schedule_reload` instead of `async_reload` for ZHA ([@puddly](https://github.com/puddly) - [#154397](https://github.com/home-assistant/core/pull/154397))
  * Move igloohome API access URL into constant placeholders ([@DannyS95](https://github.com/DannyS95) - [#154430](https://github.com/home-assistant/core/pull/154430))
  * Add missing`long_press` entry for trigger_type in strings.json for Hue ([@mvdwetering](https://github.com/mvdwetering) - [#154437](https://github.com/home-assistant/core/pull/154437))
  * Move translatable URLs out of strings.json for isy994 ([@sonianuj287](https://github.com/sonianuj287) - [#154464](https://github.com/home-assistant/core/pull/154464))
  * OpenUV: Fix update by skipping when protection window is null ([@wbyoung](https://github.com/wbyoung) - [#154487](https://github.com/home-assistant/core/pull/154487))
  * Bump aioamazondevices to 6.4.4 ([@chemelli74](https://github.com/chemelli74) - [#154538](https://github.com/home-assistant/core/pull/154538))
  * Move URL out of Nuheat strings.json ([@tstabrawa](https://github.com/tstabrawa) - [#154580](https://github.com/home-assistant/core/pull/154580))
  * Bump pyvesync version to 3.1.2 ([@cdnninja](https://github.com/cdnninja) - [#154650](https://github.com/home-assistant/core/pull/154650))


### 2025.10.4 - October 24 
  * Bump aioautomower to v2.3.1 ([@Thomas55555](https://github.com/Thomas55555) - [#151795](https://github.com/home-assistant/core/pull/151795))
  * Fix history coordinator in Tesla Fleet and Teslemetry ([@Bre77](https://github.com/Bre77) - [#153068](https://github.com/home-assistant/core/pull/153068))
  * Increase connect and configuration time for rfxtrx ([@alec-pinson](https://github.com/alec-pinson) - [#153834](https://github.com/home-assistant/core/pull/153834))
  * Return default temp range if API responds 0 in Huum. ([@vincentwolsink](https://github.com/vincentwolsink) - [#153871](https://github.com/home-assistant/core/pull/153871))
  * Improve error message for unsupported hardware in Overkiz ([@iMicknl](https://github.com/iMicknl) - [#154314](https://github.com/home-assistant/core/pull/154314))
  * Bump pyprobeplus to 1.1.1 ([@pantherale0](https://github.com/pantherale0) - [#154523](https://github.com/home-assistant/core/pull/154523))
  * Move translatable URL out of strings.json for airnow integration ([@akanksha106-code](https://github.com/akanksha106-code) - [#154557](https://github.com/home-assistant/core/pull/154557))
  * Moved non-translatable elements out of strings.json for nuki ([@sonianuj287](https://github.com/sonianuj287) - [#154682](https://github.com/home-assistant/core/pull/154682))
  * Handle location scope in Tesla Fleet vehicle coordinator ([@Bre77](https://github.com/Bre77) - [#154731](https://github.com/home-assistant/core/pull/154731))
  * Fix units for Shelly TopAC EVE01-11 sensors ([@bieniu](https://github.com/bieniu) - [#154740](https://github.com/home-assistant/core/pull/154740))
  * Fix pterodactyl server config link ([@electricsteve](https://github.com/electricsteve) - [#154758](https://github.com/home-assistant/core/pull/154758))
  * Move URL out of Tomorrow.io strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154759](https://github.com/home-assistant/core/pull/154759))
  * Move URL out of TheThingsNetwork strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154760](https://github.com/home-assistant/core/pull/154760))
  * Move url out of simplisafe strings ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154762](https://github.com/home-assistant/core/pull/154762))
  * Move url out of sensorpush_cloud strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154768](https://github.com/home-assistant/core/pull/154768))
  * Move URLs out of strings.json for auth ([@jbouwh](https://github.com/jbouwh) - [#154769](https://github.com/home-assistant/core/pull/154769))
  * Move url out of starline strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154773](https://github.com/home-assistant/core/pull/154773))
  * Move url out of orsoenergy strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154776](https://github.com/home-assistant/core/pull/154776))
  * Move url out of motionblinds strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154777](https://github.com/home-assistant/core/pull/154777))
  * Move url out of rachio strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154781](https://github.com/home-assistant/core/pull/154781))
  * Move url out of Flume strings.json ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154787](https://github.com/home-assistant/core/pull/154787))
  * Remove opower violation from hassfest requirements check ([@cdce8p](https://github.com/cdce8p) - [#154797](https://github.com/home-assistant/core/pull/154797))
  * Bump opower to 0.15.8 ([@tronikos](https://github.com/tronikos) - [#154811](https://github.com/home-assistant/core/pull/154811))
  * Move url out of nightscout strings and change to field descriptions ([@andrew-codechimp](https://github.com/andrew-codechimp) - [#154812](https://github.com/home-assistant/core/pull/154812))
  * vesync show fan speed for smart tower fans ([@cdnninja](https://github.com/cdnninja) - [#154842](https://github.com/home-assistant/core/pull/154842))
  * Bump bring-api to v1.1.1 ([@tr4nt0r](https://github.com/tr4nt0r) - [#154854](https://github.com/home-assistant/core/pull/154854))
  * Bump PyCync to 0.4.2 ([@Kinachi249](https://github.com/Kinachi249) - [#154856](https://github.com/home-assistant/core/pull/154856))
  * Bump aioamazondevices to 6.4.6 ([@chemelli74](https://github.com/chemelli74) - [#154865](https://github.com/home-assistant/core/pull/154865))
  * YoLink remove unsupported remoters ([@matrixd2](https://github.com/matrixd2) - [#154918](https://github.com/home-assistant/core/pull/154918))
  * Fix BrowseError import in yamaha_musiccast media_player.py ([@wimb0](https://github.com/wimb0) - [#154980](https://github.com/home-assistant/core/pull/154980))
  * Remove async-modbus exception from hassfest requirements check ([@cdce8p](https://github.com/cdce8p) - [#154988](https://github.com/home-assistant/core/pull/154988))
  * Lametric remove translatable URL ([@erwindouna](https://github.com/erwindouna) - [#154991](https://github.com/home-assistant/core/pull/154991))
  * Add SensorDeviceClass and unit for LCN humidity sensor. ([@alengwenus](https://github.com/alengwenus) - [#155044](https://github.com/home-assistant/core/pull/155044))
  * Add shared BleakScanner to probe_plus ([@pantherale0](https://github.com/pantherale0) - [#155051](https://github.com/home-assistant/core/pull/155051))
  * Improve migration to Uptime Kuma v2.0.0 ([@tr4nt0r](https://github.com/tr4nt0r) - [#155055](https://github.com/home-assistant/core/pull/155055))
  * Move URL out of system_bridge strings.json ([@MichaelMKKelly](https://github.com/MichaelMKKelly) - [#155067](https://github.com/home-assistant/core/pull/155067))
  * Update aioairzone to v1.0.2 ([@Noltari](https://github.com/Noltari) - [#155088](https://github.com/home-assistant/core/pull/155088))
  * Bump pydroplet version to 2.3.4 ([@sarahseidman](https://github.com/sarahseidman) - [#155103](https://github.com/home-assistant/core/pull/155103))
  * Bump holidays to 0.83 ([@gjohansson-ST](https://github.com/gjohansson-ST) - [#155107](https://github.com/home-assistant/core/pull/155107))


## Need help? Join the community 
Home Assistant has a great community of users who are all more than willing to help each other out. So, join us!
Our very active [Discord chat server](https://www.home-assistant.io/join-chat) is an excellent place to be, and don’t forget to join our amazing [forums](https://community.home-assistant.io/).
Found a bug or issue? Please report it in our [issue tracker](https://github.com/home-assistant/core/issues) to get it fixed! Or check [our help page](https://www.home-assistant.io/help) for guidance on more places you can go.
Are you more into email? [Sign up for the Open Home Foundation Newsletter](https://www.home-assistant.io/newsletter) to get the latest news about features, things happening in our community, and other projects that support the Open Home straight into your inbox.
## Backward-incompatible changes 
We do our best to avoid making changes to existing functionality that might unexpectedly impact your Home Assistant installation. Unfortunately, sometimes, it is inevitable.
We always make sure to document these changes to make the transition as easy as possible for you. This release has the following backward-incompatible changes:
Targeting labels in automations and scripts
Configuration and diagnostic entities with a label assigned to them will now be targeted/affected by service actions targeting that label. Previously, those entity categories were ignored on service action calls targeting labels.
If you have an automation or script with an action targeting a label, make sure that only entities that should be affected have that label assigned, even if they are config or diagnostic entities.
([@abmantis](https://github.com/abmantis) - [#149309](https://github.com/home-assistant/core/pull/149309)) ([labels docs](https://www.home-assistant.io/docs/organizing/labels/))
HERE Travel Time
HERE deprecated the previous free tier. The new Base Plan has 5000 free requests per month. The automatic update interval of the HERE Travel Time integration changed from 5 minutes to 30 minutes, so one route can be supported without costs.
([@eifinger](https://github.com/eifinger) - [#147222](https://github.com/home-assistant/core/pull/147222)) ([here_travel_time docs](https://www.home-assistant.io/integrations/here_travel_time/))
Home Connect
The Home Connect Alarm clock entity has been removed from the time platform, please use the number entity instead.
([@Diegorro98](https://github.com/Diegorro98) - [#152188](https://github.com/home-assistant/core/pull/152188)) ([home_connect docs](https://www.home-assistant.io/integrations/home_connect/))
Shelly
Removed previously deprecated extra attributes, please review your automations.
**Shelly Gas:**
  * The Detected attribute of the Gas entity has been removed, the Gas detected entity should be used instead.
  * The Self test attribute of the Operation entity has been removed, the Self test entity should be used instead.


**Shelly Air:**
  * The Operational hours of the Lamp Life entity has been removed, if you still want that info please use a template entity.


([@chemelli74](https://github.com/chemelli74) - [#140386](https://github.com/home-assistant/core/pull/140386)) ([shelly docs](https://www.home-assistant.io/integrations/shelly/))
Slide Local
The effect of the property “invert position” is extended from the position itself to the status (open or closed). With this adjustment, it is no longer necessary to use cover templates to invert the position to correct the status. If you have covers with inverted position and are using the state in automations, you must adjust the automations accordingly.
([@dontinelli](https://github.com/dontinelli) - [#150418](https://github.com/home-assistant/core/pull/150418)) ([slide_local docs](https://www.home-assistant.io/integrations/slide_local/))
SmartThings
The `windFree` preset mode for the air conditioner has been renamed to `wind_free` to allow translation to happen. Please adapt automations accordingly.
([@joostlek](https://github.com/joostlek) - [#152833](https://github.com/home-assistant/core/pull/152833)) ([smartthings docs](https://www.home-assistant.io/integrations/smartthings/))
Tibber
Switch Tibber electricity pricing to 15-minute intervals.
  * The `tibber.get_prices` action now returns 15-minute data instead of hourly.
  * The `price_level` attribute is removed and no longer supported.
  * The `intraday_price_ranking` attribute is now scaled to (0,1) to better support 15-minute prices.


([@Danielhiversen](https://github.com/Danielhiversen) - [#151881](https://github.com/home-assistant/core/pull/151881)) ([tibber docs](https://www.home-assistant.io/integrations/tibber/))
Zabbix
We removed official support for Zabbix 5.0 from the integration. While this does not directly break connections to Zabbix 5.0, future updates will not check for compatibility with this version. Note that Zabbix 5 LTS left its support window in May of 2025.
([@nolsto](https://github.com/nolsto) - [#149450](https://github.com/home-assistant/core/pull/149450)) ([zabbix docs](https://www.home-assistant.io/integrations/zabbix/))
ZHA
Removes the extra ZHA specific cover entity attributes, their values were no longer populated.
  * `target_lift_position`
  * `target_tilt_position`


([@jeverley](https://github.com/jeverley) - [#142534](https://github.com/home-assistant/core/pull/142534)) ([zha docs](https://www.home-assistant.io/integrations/zha/))
ZhongHong
ZhongHong’s climate entities `set_fan_mode` action behavior has changed.
The fan mode values are now converted to lowercase instead of uppercase to ensure compliance with the standard convention.
If you have automations relying on uppercase fan mode values, you will need to update them to use lowercase values instead.
([@Blear](https://github.com/Blear) - [#151559](https://github.com/home-assistant/core/pull/151559)) ([zhong_hong docs](https://www.home-assistant.io/integrations/zhong_hong/))
If you are a custom integration developer and want to learn about changes and new features available for your integration: Be sure to follow our [developer blog](https://developers.home-assistant.io/blog/). The following changes are the most notable for this release:
  * [Deprecate hass argument in service helpers](https://developers.home-assistant.io/blog/2025/09/22/deprecate-hass-argument-service-helpers)
  * [Improved API for registering platform entity services](https://developers.home-assistant.io/blog/2025/09/25/entity-services-api-changes/)


## All changes 
Of course, there is a lot more in this release. You can find a list of all changes made here: [Full changelog for Home Assistant Core 2025.10](https://www.home-assistant.io/changelogs/core-2025.10)
Back to top
