---
url: "https://www.home-assistant.io/blog/2025/07/02/release-20257/"
title: "2025.7: That's the question - Home Assistant"
scraped_at: 2026-09-17T16:42:05+00:00
---

Home Assistant 2025.7! 🎉
Whew! It’s hot out there! 🌡️ While most of Europe is dealing with a heat wave right now, we’re here to cool things down with an exciting July release that’s packed with features I’m genuinely excited about.
Before we dive in, if you missed it, we recently published [Voice Chapter 10](https://www.home-assistant.io/blog/2025/06/25/voice-chapter-10/) where we explored moving beyond reactive voice assistants that only respond when you talk to them. Instead, we envisioned a future where your voice assistant can be conversational and initiate conversations. Speaking of that, this release delivers on that vision in a big way!
I’m absolutely stoked about the new Ask Question action for Assist! 🗣️ This is something that sets Home Assistant apart from every other voice assistant out there. Finally, your voice assistant can take the initiative and ask _you_ what your smart home should do. No more waiting for wake words, your assistant can start the conversation when it makes sense. It’s the kind of feature that gets me really excited thinking about all the possibilities.
The redesigned Area card is another winner! 🏠 I’ll probably be replacing a few tile cards I’ve been using to navigate to my area dashboards with this new, more flexible version. It integrates beautifully with the Sections dashboard and gives you so many more options for controlling your spaces.
And that’s just the beginning! We’ve got integration sub-entries making integrations even more extensible, full-screen code editors for those lengthy YAML and template edits, and tons of quality-of-life improvements throughout.
Stay cool, and enjoy the release!
../Frenck
  * [Let Assist ask the questions!](https://www.home-assistant.io/blog/2025/07/02/release-20257/#let-assist-ask-the-questions)
  * [Redesigned Area card](https://www.home-assistant.io/blog/2025/07/02/release-20257/#redesigned-area-card)
  * [Improving the Areas dashboard overview](https://www.home-assistant.io/blog/2025/07/02/release-20257/#improving-the-areas-dashboard-overview)
  * [Integration sub-entries](https://www.home-assistant.io/blog/2025/07/02/release-20257/#integration-sub-entries)
  * [Integration page gets an overhaul](https://www.home-assistant.io/blog/2025/07/02/release-20257/#integration-page-gets-an-overhaul)
  * [Integrations](https://www.home-assistant.io/blog/2025/07/02/release-20257/#integrations)
    * [New integrations](https://www.home-assistant.io/blog/2025/07/02/release-20257/#new-integrations)
    * [Noteworthy improvements to existing integrations](https://www.home-assistant.io/blog/2025/07/02/release-20257/#noteworthy-improvements-to-existing-integrations)
    * [Integration quality scale achievements](https://www.home-assistant.io/blog/2025/07/02/release-20257/#integration-quality-scale-achievements)
    * [Now available to set up from the UI](https://www.home-assistant.io/blog/2025/07/02/release-20257/#now-available-to-set-up-from-the-ui)
    * [Farewell to the following](https://www.home-assistant.io/blog/2025/07/02/release-20257/#farewell-to-the-following)
  * [Other noteworthy changes](https://www.home-assistant.io/blog/2025/07/02/release-20257/#other-noteworthy-changes)
  * [Full-screen code editors](https://www.home-assistant.io/blog/2025/07/02/release-20257/#full-screen-code-editors)
  * [Improved dashboard creation experience](https://www.home-assistant.io/blog/2025/07/02/release-20257/#improved-dashboard-creation-experience)
  * [Patch releases](https://www.home-assistant.io/blog/2025/07/02/release-20257/#patch-releases)
    * [2025.7.1 - July 4](https://www.home-assistant.io/blog/2025/07/02/release-20257/#202571---july-4)
    * [2025.7.2 - July 14](https://www.home-assistant.io/blog/2025/07/02/release-20257/#202572---july-14)
    * [2025.7.3 - July 18](https://www.home-assistant.io/blog/2025/07/02/release-20257/#202573---july-18)
    * [2025.7.4 - July 28](https://www.home-assistant.io/blog/2025/07/02/release-20257/#202574---july-28)
  * [Need help? Join the community!](https://www.home-assistant.io/blog/2025/07/02/release-20257/#need-help-join-the-community)
  * [Backward-incompatible changes](https://www.home-assistant.io/blog/2025/07/02/release-20257/#backward-incompatible-changes)


## Let Assist ask the questions! 
In our latest [roadmap](https://www.home-assistant.io/blog/2025/05/09/roadmap-2025h1/), we shared our goal to make Assist more conversational. Until now, Assist was mostly transactional, meaning when you would say something, you would get a response or it would perform an action, and that would be the end of it (unless some LLM magic jumped in). With this release, we’re taking a big step forward: meet the new Ask Question action.
This lets you build custom conversations from the comfort of our automation engine. Ask a question, handle the answer, and keep the interaction going.
This action even allows you to define expected answers so that our extremely fast speech engine, Speech-to-Phrase, can train on them. Yes, fully local, custom conversations!
To help you get started, we have provided a blueprint that covers the most common use case — Asking a closed Yes/No question:
This blueprint allows you to focus on what you want to do if you answer positively or negatively to any question that your voice assistant will ask. The blueprint supports 50 different ways of saying “Yes” and “No” (including phrases like “Make it so” and “Let’s not”). Here it is in action!
In case you want to dive deeper into conversation building, here is an example on how to ask a question and process the different answers:
Example YAML automation actions
This example asks the user what kind of music they want to listen to, and then plays the selected genre or artist on a media player.

```
actions:
  - action: assist_satellite.ask_question
    data:
      entity_id: assist_satellite.living_room_voice_assistant
      preannounce: true   # optional
      preannounce_media_id: media-source://...   # optional
      question: "What kind of music do you want to listen to?"
      answers:
        - id: genre
          sentences:
            - "genre {genre}"
        - id: artist
          sentences:
            - "artist {artist}"
    response_variable: answer
  - choose:
      - conditions: "{{ answer.id == 'genre' }}"
        sequence:
          - action: music_assistant.play_media
            data:
              media_id: "My {{ answer.slots.genre }} playlist"
              media_type: playlist
            target:
              entity_id: media_player.living_room_speakers
      - conditions: "{{ answer.id == 'artist' }}"
        sequence:
          - action: music_assistant.play_media
            data:
              media_id: "{{ answer.slots.artist }}"
              media_type: artist
            target:
              entity_id: media_player.living_room_speakers
```

YAML
Copy
## Redesigned Area card 
Originally introduced a few years ago, the [Area card](https://www.home-assistant.io/dashboards/area/) offered a way to display an areaAn area in Home Assistant is a [logical grouping](https://www.home-assistant.io/docs/organizing/) of devices and entities that represents a room or space in your home, such as the living room, kitchen, or garage.[ [Learn more]](https://www.home-assistant.io/docs/organizing/areas/) overview within the dashboard. However, it wasn’t fully compatible with the [Sections](https://www.home-assistant.io/dashboards/sections/) dashboard, which limited its practical use in that context.
The card has now been completely redesigned with a look and feel similar to the [Tile card](https://www.home-assistant.io/dashboards/tile/). It integrates seamlessly into the Sections dashboard thanks to its flexible layouts. You can choose between a compact version that shows only an icon and the area name, or a more detailed view featuring elements like your camera feed and buttons to toggle your lights or fans.
The control section itself has also been revamped, allowing you to choose which controls to include and rearrange them as you want. As a result of these changes, if you’re currently using the area cards, you’ll need to reconfigure the controls on them.
Additionally, the card now supports controlling [cover](https://www.home-assistant.io/integrations/cover/) entitiesAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/).
## Improving the Areas dashboard overview 
The April release introduced an experimental [Areas dashboard](https://www.home-assistant.io/dashboards/dashboards/#areas-dashboard), designed to automatically generate a ready-to-use interface based on the configured areas within the home. However, the preview could become cluttered if you had a lot of devices in a room.
This release introduces an all-new overview that leverages the redesigned Area card, making it easy to view and control your main devices by room with a single click. It also acts as a navigation hub, giving you quick access to detailed views of each area.
Please note that this is experimental, meaning it is subject to change and may not always work as intended. We would love your feedback if you notice some aspects we can improve. The community’s dashboards, shared over the years, have helped shape this design, and we would love to see how it works with a wide variety of your homes. Even if you already have the perfect dashboard built for your home, try it!
**Use[this feedback form](https://forms.clickup.com/2533032/f/2d9n8-32191/NK2MUOVKXQVH2L0NHI) to let us know your thoughts!**
## Integration sub-entries 
Ever wondered why you had to enter your API keys for every AI agent you created, even though they all used the same key? Or why you had to authenticate for every calendar you added, regardless of the fact that they all shared the same account? Or why you couldn’t add MQTT devices from the UI?
This release solves that with the introduction of integration sub-entries. This allows you to add a sub-entry to an existing integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) entry. In practice, this means that your integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) entry has your credentials, and all the sub-entries use these credentials. In the sub-entry, you can then configure what should be done with these credentials, such as fetching a specific calendar, adding three AI agents with different prompts using the same OpenAI account, or in the case of MQTT, configuring devices that are connected to your MQTT broker.
The following integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) now support sub-entries as of this release: [Anthropic](https://www.home-assistant.io/integrations/anthropic), [Google Generative AI](https://www.home-assistant.io/integrations/google_generative_ai_conversation), [MQTT](https://www.home-assistant.io/integrations/mqtt), [Ollama](https://www.home-assistant.io/integrations/ollama), [OpenAI Conversation](https://www.home-assistant.io/integrations/openai_conversation), and [Telegram Bot](https://www.home-assistant.io/integrations/telegram_bot).
## Integration page gets an overhaul 
The integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) page got a big overhaul! It now has support for sub-entries, allowing you to easily add a sub-entry to an integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) entry along with being able to see which devices and services belong to which sub-entry.
But we took the opportunity to do more. Instead of just showing your integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) entries, it now also shows the devices and services provided by that configuration entry. This makes it much easier to manage your devices and see the relationship between your devices and their integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) at a glance.
## Integrations 
Thanks to our community for keeping pace with the new integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) and improvements to existing ones! You’re all awesome 🥰
### New integrations 
We welcome the following new integrations in this release:
  * , added by [@LoSk-p](https://github.com/LoSk-p) Monitor air quality and environmental conditions with the Altruist sensor, providing local data for temperature, humidity, PM2.5/PM10, CO2, noise levels, and more.
  * **[PlayStation Network](https://www.home-assistant.io/integrations/playstation_network)** , added by [@JackJPowell](https://github.com/JackJPowell) Integrate with the PlayStation Network to track your currently playing games and display game information on your dashboard.
  * , added by [@michaelheyman](https://github.com/michaelheyman) Monitor your Tilt Pi hydrometer for brewing temperature and specific gravity measurements during your brewing process.
  * , added by [@Thulrus](https://github.com/Thulrus) Monitor and control your garden with the Vegetronix VegeHub, gathering sensor data and controlling irrigation relays for automated plant care.


### Noteworthy improvements to existing integrations 
It is not just new integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) that have been added; existing integrations are also being constantly improved. Here are some of the noteworthy changes to existing integrations:
  * Love that song? [@marcelveldt](https://github.com/marcelveldt) added a button entityAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) to [Music Assistant](https://www.home-assistant.io/integrations/music_assistant) that lets you add the currently playing item to your favorites with a single click. It works with queues, external sources, and even radio stations!
  * [ESPHome](https://www.home-assistant.io/integrations/esphome) now supports sub-devices! Thanks to [@bdraco](https://github.com/bdraco), you can now represent multiple logical devices with a single ESP device in Home Assistant. This is particularly useful for RF bridges, Modbus gateways, and other devices that can control multiple devices. This feature requires the soon-to-be-released ESPHome 2025.7. Awesome addition!
  * [Paperless-ngx](https://www.home-assistant.io/integrations/paperless_ngx) now includes an update entityAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) to keep your document management system up to date. Thanks, [@fvgarrel](https://github.com/fvgarrel)!
  * Battery management control has been added to [HomeWizard](https://www.home-assistant.io/integrations/homewizard) with [@DCSBL](https://github.com/DCSBL) implementing battery group mode, allowing you to modify the charging and discharging behavior of your HomeWizard batteries!
  * [Reolink](https://www.home-assistant.io/integrations/reolink) cameras received a ton of love (again) from [@starkillerOG](https://github.com/starkillerOG)! New features include IR brightness control, baby cry sensitivity adjustment, privacy mask switches, and full support for both PoE and WiFi floodlights with multiple command ID pushes. Impressive!
  * [@mib1185](https://github.com/mib1185) added an update entityAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) to the [Immich](https://www.home-assistant.io/integrations/immich) integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations). Nice!
  * The [Homee](https://www.home-assistant.io/integrations/homee) integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) expanded significantly! [@Taraman17](https://github.com/Taraman17) added a siren platform for security alerts and support for the HeatIt Thermostat TF056. Nice!
  * Energy monitoring got better in [Adax](https://www.home-assistant.io/integrations/adax) with [@parholmdahl](https://github.com/parholmdahl) adding energy sensors, so you can track your heating consumption!
  * [@ViViDboarder](https://github.com/ViViDboarder) made [Ollama](https://www.home-assistant.io/integrations/ollama) more flexible by adding a config option for controlling the think parameter. More control over your local AI!
  * Samsung refrigerator owners! [@mswilson](https://github.com/mswilson) added ice bites control and water filter replacement/usage sensors to the [SmartThings](https://www.home-assistant.io/integrations/smartthings) integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations).
  * [Russound RIO](https://www.home-assistant.io/integrations/russound_rio) got a major upgrade from [@noahhusby](https://github.com/noahhusby), adding sub-device support plus new number and switch entitiesAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) for enhanced zone control.
  * [@chemelli74](https://github.com/chemelli74) expanded [Alexa Devices](https://www.home-assistant.io/integrations/alexa_devices) with sensor platforms and additional binary sensors. Now you can get more data from your Echo devices!
  * [Matter](https://www.home-assistant.io/integrations/matter) keeps growing! [@lboue](https://github.com/lboue) added dishwasher alarm support and battery storage capabilities. Thanks!
  * YAML fans will appreciate [@frenck](https://github.com/frenck) adding unique ID support to [Trend](https://www.home-assistant.io/integrations/trend) integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) configuration.
  * The [LaMetric](https://www.home-assistant.io/integrations/lametric) Time got an update entityAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) as well, thanks [@joostlek](https://github.com/joostlek)!
  * [Google Generative AI](https://www.home-assistant.io/integrations/google_generative_ai_conversation) now defaults to the newer, faster Gemini 2.5 Flash model. A noteworthy performance boost by [@tronikos](https://github.com/tronikos)!
  * [Google Generative AI](https://www.home-assistant.io/integrations/google_generative_ai_conversation) now supports text-to-speech (TTS) with 30 voices and 24 languages. It supports fine-grained control over style and sound, for example, “Say cheerfully: Have a wonderful day!”. Thanks [@lanthaler](https://github.com/lanthaler)!
  * [Enphase Envoy](https://www.home-assistant.io/integrations/enphase_envoy) users get detailed DC voltage and current readings from their solar panels thanks to [@Bidski](https://github.com/Bidski). This is perfect for monitoring individual panel health and optimizing production!
  * [@zerzhang](https://github.com/zerzhang) brought evaporative humidifier support to [SwitchBot](https://www.home-assistant.io/integrations/switchbot), expanding your climate control options.


### Integration quality scale achievements 
One thing we are incredibly proud of in Home Assistant is our [integration quality scale](https://www.home-assistant.io/docs/quality_scale/). This scale helps us and our contributors to ensure integrations are of high quality, maintainable, and provide the best possible user experience.
This release, we celebrate several integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) that have improved their quality scale:
  * **2 integrations reached platinum** 🏆
    * [Bosch Alarm](https://www.home-assistant.io/integrations/bosch_alarm), thanks to [@sanjay900](https://github.com/sanjay900)
    * [Home Connect](https://www.home-assistant.io/integrations/home_connect), thanks to [@Diegorro98](https://github.com/Diegorro98)
  * **1 integration reached gold** 🥇
    * [ista EcoTrend](https://www.home-assistant.io/integrations/ista_ecotrend), thanks to [@tr4nt0r](https://github.com/tr4nt0r)
  * **1 integration reached silver** 🥈
    * [KNX](https://www.home-assistant.io/integrations/knx), thanks to [@farmio](https://github.com/farmio)
  * **2 integrations reached bronze** 🥉
    * [Samsung TV](https://www.home-assistant.io/integrations/samsungtv), thanks to [@chemelli74](https://github.com/chemelli74)
    * [Telegram Bot](https://www.home-assistant.io/integrations/telegram_bot), thanks to [@hanwg](https://github.com/hanwg)


This is a huge achievement for these integrations and their maintainers. The effort and dedication required to reach these quality levels is significant, as it involves extensive testing, documentation, error handling, and often complete rewrites of parts of the integration.
A big thank you to all the contributors involved! 👏
### Now available to set up from the UI 
While most integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) can be set up directly from the Home Assistant user interface, some were only available using YAML configuration. We keep moving more integrations to the UI, making them more accessible for everyone to set up and use.
The following integration is now available via the Home Assistant UI:
  * , done by [@hanwg](https://github.com/hanwg)


### Farewell to the following 
The following integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) are also no longer available as of this release:
  * **JuiceNet** has been removed as they shut down their API services.


## Other noteworthy changes 
There are many more improvements in this release; here are some of the other noteworthy changes:
  * [Shopping list](https://www.home-assistant.io/integrations/shopping_list) now has a complete intent function that allows you to check off or mark items on your shopping list as completed, making it easier to interact with your shopping lists using voice commands. Thanks, [@Lesekater](https://github.com/Lesekater)!
  * Device and entityAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) management got better! [@emontnemery](https://github.com/emontnemery) made it so Home Assistant now restores user customizations when you re-add deleted devices or entitiesAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/). No more losing your carefully crafted names and settings!
  * The [Template](https://www.home-assistant.io/integrations/template) integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) received a major boost from [@Petro31](https://github.com/Petro31)! You can now use variables, icons, and pictures across all compatible template platforms, create trigger-based template alarm control panels, locks, vacuum entitiesAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/), and fans. Plus, there’s a new `label_description` template method that allows you to dynamically fetch the description you’ve added to a label from your templates. This is a noteworthy enhancement for better template organization.
  * Camera snapshots just got better! [@edenhaus](https://github.com/edenhaus) added support for taking snapshots via [go2rtc](https://www.home-assistant.io/integrations/go2rtc). There is nothing for you to do on this one, it works out of the box, but it is nice to know snapshots are now faster and take fewer resources from your system.
  * [Object selectors](https://www.home-assistant.io/docs/blueprint/selectors/#object-selector) now support fields and multiple selections, thanks to [@piitaya](https://github.com/piitaya). These additions are particularly interesting for integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) and blueprint developers, as they provide much more flexibility in your UI representations.
  * Wind direction sensors got a visual upgrade with [@edenhaus](https://github.com/edenhaus) adding range icons for the `wind_direction` sensor device class. Different icons are now shown depending on the state of wind direction sensors, which is indeed a nice visual upgrade!


## Full-screen code editors 
Working with snippets of YAML or templates in Home Assistant just got a BIG improvement! We’ve added a new full-screen mode for all code editors throughout the interface.
Whether you’re editing automations, scripts, templates, or any other YAML configuration, you can now expand the code editor to take up your entire screen. This is especially helpful when working with longer configurations or when you need more space to see your code clearly.
Simply click the maximize button in the top-right corner of any code editor to enter full screen mode. Press the button again to return to the normal view.
This makes building a more complex and advanced smart home more comfortable and productive, especially on smaller mobile or tablet screens where every pixel of editing space counts!
## Improved dashboard creation experience 
The dialog for adding a new dashboard has been redesigned with a cleaner interface that matches recent redesigns we’ve seen to other dialogs. This improvement was designed by [@marcinbauer85](https://github.com/marcinbauer85) and implemented by [@quinnter](https://github.com/quinnter). Great teamwork!
## Patch releases 
We will also release patch releases for Home Assistant 2025.7 in July. These patch releases only contain bug fixes. Our goal is to release a patch release every Friday.
### 2025.7.1 - July 4 
Happy Fourth of July! 🇺🇸
  * Set timeout for remote calendar ([@Thomas55555](https://github.com/Thomas55555) - [#147024](https://github.com/home-assistant/core/pull/147024))
  * Fix missing port in samsungtv ([@epenet](https://github.com/epenet) - [#147962](https://github.com/home-assistant/core/pull/147962))
  * Bump ZHA to 0.0.62 ([@puddly](https://github.com/puddly) - [#147966](https://github.com/home-assistant/core/pull/147966))
  * Bump aiounifi to v84 ([@Kane610](https://github.com/Kane610) - [#147987](https://github.com/home-assistant/core/pull/147987))
  * Fix state being incorrectly reported in some situations on Music Assistant players ([@marcelveldt](https://github.com/marcelveldt) - [#147997](https://github.com/home-assistant/core/pull/147997))
  * Bump hass-nabucasa from 0.104.0 to 0.105.0 ([@ludeeus](https://github.com/ludeeus) - [#148040](https://github.com/home-assistant/core/pull/148040))
  * Fix Telegram bots using plain text parser failing to load on restart ([@hanwg](https://github.com/hanwg) - [#148050](https://github.com/home-assistant/core/pull/148050))
  * Bump pyenphase to 2.2.0 ([@catsmanac](https://github.com/catsmanac) - [#148070](https://github.com/home-assistant/core/pull/148070))
  * Cancel enphase mac verification on unload. ([@catsmanac](https://github.com/catsmanac) - [#148072](https://github.com/home-assistant/core/pull/148072))
  * Bump aioamazondevices to 3.2.3 ([@chemelli74](https://github.com/chemelli74) - [#148082](https://github.com/home-assistant/core/pull/148082))
  * Update frontend to 20250702.1 ([@bramkragten](https://github.com/bramkragten) - [#148131](https://github.com/home-assistant/core/pull/148131))
  * [ci] Fix typing issue with aiohttp and aiosignal ([@cdce8p](https://github.com/cdce8p) - [#148141](https://github.com/home-assistant/core/pull/148141))
  * Bump venstarcolortouch to 0.21 ([@mlfreeman2](https://github.com/mlfreeman2) - [#148152](https://github.com/home-assistant/core/pull/148152))


### 2025.7.2 - July 14 
  * Squeezebox: Fix track selection in media browser ([@Hypfer](https://github.com/Hypfer) - [#147185](https://github.com/home-assistant/core/pull/147185))
  * Squeezebox: Fix tracks not having thumbnails ([@Hypfer](https://github.com/Hypfer) - [#147187](https://github.com/home-assistant/core/pull/147187))
  * Bump pysmlight to v0.2.7 ([@tl-sl](https://github.com/tl-sl) - [#148101](https://github.com/home-assistant/core/pull/148101))
  * Fix REST sensor charset handling to respect Content-Type header ([@bdraco](https://github.com/bdraco) - [#148223](https://github.com/home-assistant/core/pull/148223))
  * Fix UTF-8 encoding for REST basic authentication ([@bdraco](https://github.com/bdraco) - [#148225](https://github.com/home-assistant/core/pull/148225))
  * Bump pylamarzocco to 2.0.10 ([@zweckj](https://github.com/zweckj) - [#148233](https://github.com/home-assistant/core/pull/148233))
  * Bump sharkiq to 1.1.1 ([@funkybunch](https://github.com/funkybunch) - [#148244](https://github.com/home-assistant/core/pull/148244))
  * bump motionblinds to 0.6.29 ([@starkillerOG](https://github.com/starkillerOG) - [#148265](https://github.com/home-assistant/core/pull/148265))
  * Bump aiowebostv to 0.7.4 ([@thecode](https://github.com/thecode) - [#148273](https://github.com/home-assistant/core/pull/148273))
  * Bump `gios` to version 6.1.0 ([@bieniu](https://github.com/bieniu) - [#148274](https://github.com/home-assistant/core/pull/148274))
  * Restore httpx compatibility for non-primitive REST query parameters ([@bdraco](https://github.com/bdraco) - [#148286](https://github.com/home-assistant/core/pull/148286))
  * Bump pyenphase to 2.2.1 ([@catsmanac](https://github.com/catsmanac) - [#148292](https://github.com/home-assistant/core/pull/148292))
  * Add lamp states to smartthings selector ([@jvits227](https://github.com/jvits227) - [#148302](https://github.com/home-assistant/core/pull/148302))
  * Fix Switchbot cloud plug mini current unit Issue ([@XiaoLing-git](https://github.com/XiaoLing-git) - [#148314](https://github.com/home-assistant/core/pull/148314))
  * Bump pyswitchbot to 0.68.1 ([@zerzhang](https://github.com/zerzhang) - [#148335](https://github.com/home-assistant/core/pull/148335))
  * Handle binary coils with non default mappings in nibe heatpump ([@elupus](https://github.com/elupus) - [#148354](https://github.com/home-assistant/core/pull/148354))
  * Bump aioamazondevices to 3.2.8 ([@chemelli74](https://github.com/chemelli74) - [#148365](https://github.com/home-assistant/core/pull/148365))
  * Create own clientsession for lamarzocco ([@zweckj](https://github.com/zweckj) - [#148385](https://github.com/home-assistant/core/pull/148385))
  * Bump pylamarzocco to 2.0.11 ([@zweckj](https://github.com/zweckj) - [#148386](https://github.com/home-assistant/core/pull/148386))
  * Bump pySmartThings to 3.2.7 ([@joostlek](https://github.com/joostlek) - [#148394](https://github.com/home-assistant/core/pull/148394))
  * Bump uiprotect to version 7.14.2 ([@RaHehl](https://github.com/RaHehl) - [#148453](https://github.com/home-assistant/core/pull/148453))
  * Bump hass-nabucasa from 0.105.0 to 0.106.0 ([@ludeeus](https://github.com/ludeeus) - [#148473](https://github.com/home-assistant/core/pull/148473))
  * Revert “Deprecate hddtemp” ([@edenhaus](https://github.com/edenhaus) - [#148482](https://github.com/home-assistant/core/pull/148482))
  * Fix entity_id should be based on object_id the first time an entity is added ([@jbouwh](https://github.com/jbouwh) - [#148484](https://github.com/home-assistant/core/pull/148484))
  * Bump aioimmich to 0.10.2 ([@mib1185](https://github.com/mib1185) - [#148503](https://github.com/home-assistant/core/pull/148503))
  * Add workaround for sub units without main device in AVM Fritz!SmartHome ([@mib1185](https://github.com/mib1185) - [#148507](https://github.com/home-assistant/core/pull/148507))
  * Add Home Connect resume command button when an appliance is paused ([@Diegorro98](https://github.com/Diegorro98) - [#148512](https://github.com/home-assistant/core/pull/148512))
  * Use the link to the issue instead of creating new issues at Home Connect ([@Diegorro98](https://github.com/Diegorro98) - [#148523](https://github.com/home-assistant/core/pull/148523))
  * Ensure response is fully read to prevent premature connection closure in rest command ([@jpbede](https://github.com/jpbede) - [#148532](https://github.com/home-assistant/core/pull/148532))
  * Fix for Renson set Breeze fan speed ([@krmarien](https://github.com/krmarien) - [#148537](https://github.com/home-assistant/core/pull/148537))
  * Remove vg argument from miele auth flow ([@astrandb](https://github.com/astrandb) - [#148541](https://github.com/home-assistant/core/pull/148541))
  * Bump aiohttp to 3.12.14 ([@bdraco](https://github.com/bdraco) - [#148565](https://github.com/home-assistant/core/pull/148565))
  * Update frontend to 20250702.2 ([@bramkragten](https://github.com/bramkragten) - [#148573](https://github.com/home-assistant/core/pull/148573))
  * Fix Google Cloud 504 Deadline Exceeded ([@luuquangvu](https://github.com/luuquangvu) - [#148589](https://github.com/home-assistant/core/pull/148589))
  * Fix - only enable AlexaModeController if at least one mode is offered ([@jbouwh](https://github.com/jbouwh) - [#148614](https://github.com/home-assistant/core/pull/148614))
  * snoo: use correct value for right safety clip binary sensor ([@falconindy](https://github.com/falconindy) - [#148647](https://github.com/home-assistant/core/pull/148647))
  * Bump nyt_games to 0.5.0 ([@hexEF](https://github.com/hexEF) - [#148654](https://github.com/home-assistant/core/pull/148654))
  * Fix Charge Cable binary sensor in Teslemetry ([@Bre77](https://github.com/Bre77) - [#148675](https://github.com/home-assistant/core/pull/148675))
  * Bump PyViCare to 2.50.0 ([@CFenner](https://github.com/CFenner) - [#148679](https://github.com/home-assistant/core/pull/148679))
  * Fix hide empty sections in mqtt subentry flows ([@jbouwh](https://github.com/jbouwh) - [#148692](https://github.com/home-assistant/core/pull/148692))
  * Bump aioshelly to 13.7.2 ([@thecode](https://github.com/thecode) - [#148706](https://github.com/home-assistant/core/pull/148706))
  * Bump aioamazondevices to 3.2.10 ([@chemelli74](https://github.com/chemelli74) - [#148709](https://github.com/home-assistant/core/pull/148709))


### 2025.7.3 - July 18 
  * Handle connection issues after websocket reconnected in homematicip_cloud ([@hahn-th](https://github.com/hahn-th) - [#147731](https://github.com/home-assistant/core/pull/147731))
  * Fix Shelly `n_current` sensor removal condition ([@bieniu](https://github.com/bieniu) - [#148740](https://github.com/home-assistant/core/pull/148740))
  * Bump pySmartThings to 3.2.8 ([@joostlek](https://github.com/joostlek) - [#148761](https://github.com/home-assistant/core/pull/148761))
  * Bump Tesla Fleet API to 1.2.2 ([@Bre77](https://github.com/Bre77) - [#148776](https://github.com/home-assistant/core/pull/148776))
  * Use ffmpeg for generic cameras in go2rtc ([@edenhaus](https://github.com/edenhaus) - [#148818](https://github.com/home-assistant/core/pull/148818))
  * Add guard to prevent exception in Sonos Favorites ([@PeteRager](https://github.com/PeteRager) - [#148854](https://github.com/home-assistant/core/pull/148854))
  * Fix button platform parent class in Teslemetry ([@Bre77](https://github.com/Bre77) - [#148863](https://github.com/home-assistant/core/pull/148863))
  * Bump pyenphase to 2.2.2 ([@catsmanac](https://github.com/catsmanac) - [#148870](https://github.com/home-assistant/core/pull/148870))
  * Bump gios to version 6.1.1 ([@bieniu](https://github.com/bieniu) - [#148414](https://github.com/home-assistant/core/pull/148414))
  * Bump `gios` to version 6.1.2 ([@bieniu](https://github.com/bieniu) - [#148884](https://github.com/home-assistant/core/pull/148884))
  * Bump async-upnp-client to 0.45.0 ([@StevenLooman](https://github.com/StevenLooman) - [#148961](https://github.com/home-assistant/core/pull/148961))
  * Pass Syncthru entry to coordinator ([@joostlek](https://github.com/joostlek) - [#148974](https://github.com/home-assistant/core/pull/148974))
  * Update frontend to 20250702.3 ([@bramkragten](https://github.com/bramkragten) - [#148994](https://github.com/home-assistant/core/pull/148994))
  * Bump PySwitchbot to 0.68.2 ([@bdraco](https://github.com/bdraco) - [#148996](https://github.com/home-assistant/core/pull/148996))
  * Ignore MQTT sensor unit of measurement if it is an empty string ([@jbouwh](https://github.com/jbouwh) - [#149006](https://github.com/home-assistant/core/pull/149006))
  * Bump aioamazondevices to 3.5.0 ([@chemelli74](https://github.com/chemelli74) - [#149011](https://github.com/home-assistant/core/pull/149011))


### 2025.7.4 - July 28 
  * Keep entities of dead Z-Wave devices available ([@AlCalzone](https://github.com/AlCalzone) - [#148611](https://github.com/home-assistant/core/pull/148611))
  * Fix warning about failure to get action during setup phase ([@mback2k](https://github.com/mback2k) - [#148923](https://github.com/home-assistant/core/pull/148923))
  * Fix a bug in rainbird device migration that results in additional devices ([@allenporter](https://github.com/allenporter) - [#149078](https://github.com/home-assistant/core/pull/149078))
  * Fix multiple webhook secrets for Telegram bot ([@hanwg](https://github.com/hanwg) - [#149103](https://github.com/home-assistant/core/pull/149103))
  * Bump pyschlage to 2025.7.2 ([@dknowles2](https://github.com/dknowles2) - [#149148](https://github.com/home-assistant/core/pull/149148))
  * Fix Matter light get brightness ([@jvmahon](https://github.com/jvmahon) - [#149186](https://github.com/home-assistant/core/pull/149186))
  * Fix brightness_step and brightness_step_pct via lifx.set_state ([@Djelibeybi](https://github.com/Djelibeybi) - [#149217](https://github.com/home-assistant/core/pull/149217))
  * Add Z-Wave USB migration confirm step ([@MartinHjelmare](https://github.com/MartinHjelmare) - [#149243](https://github.com/home-assistant/core/pull/149243))
  * Add fan off mode to the supported fan modes to fujitsu_fglair ([@crevetor](https://github.com/crevetor) - [#149277](https://github.com/home-assistant/core/pull/149277))
  * Update Tesla OAuth Server in Tesla Fleet ([@Bre77](https://github.com/Bre77) - [#149280](https://github.com/home-assistant/core/pull/149280))
  * Update slixmpp to 1.10.0 ([@gaaf](https://github.com/gaaf) - [#149374](https://github.com/home-assistant/core/pull/149374))
  * Bump aioamazondevices to 3.5.1 ([@chemelli74](https://github.com/chemelli74) - [#149385](https://github.com/home-assistant/core/pull/149385))
  * Bump pysuezV2 to 2.0.7 ([@jb101010-2](https://github.com/jb101010-2) - [#149436](https://github.com/home-assistant/core/pull/149436))
  * Bump habiticalib to v0.4.1 ([@tr4nt0r](https://github.com/tr4nt0r) - [#149523](https://github.com/home-assistant/core/pull/149523))


## Need help? Join the community! 
Home Assistant has a great community of users who are all more than willing to help each other out. So, join us!
Our very active [Discord chat server](https://www.home-assistant.io/join-chat) is an excellent place to be, and don’t forget to join our amazing [forums](https://community.home-assistant.io/).
Found a bug or issue? Please report it in our [issue tracker](https://github.com/home-assistant/core/issues) to get it fixed! Or check [our help page](https://www.home-assistant.io/help) for guidance on more places you can go.
Are you more into email? [Sign up for the Open Home Foundation Newsletter](https://www.home-assistant.io/newsletter) to get the latest news about features, things happening in our community, and other projects that support the Open Home straight into your inbox.
## Backward-incompatible changes 
We do our best to avoid making changes to existing functionality that might unexpectedly impact your Home Assistant installation. Unfortunately, sometimes, it is inevitable.
We always make sure to document these changes to make the transition as easy as possible for you. This release has the following backward-incompatible changes:
Google Calendar
The previously deprecated Google Calendar `add_event` actionActions are used in several places in Home Assistant. As part of a script or automation, actions define what is going to happen once a trigger is activated. In scripts, an action is called _sequence_.[ [Learn more]](https://www.home-assistant.io/docs/automation/action/) has been removed and replaced by the `create_event` entity-based actionActions are used in several places in Home Assistant. As part of a script or automation, actions define what is going to happen once a trigger is activated. In scripts, an action is called _sequence_.[ [Learn more]](https://www.home-assistant.io/docs/automation/action/).
If you use the `add_event` actionActions are used in several places in Home Assistant. As part of a script or automation, actions define what is going to happen once a trigger is activated. In scripts, an action is called _sequence_.[ [Learn more]](https://www.home-assistant.io/docs/automation/action/) in your automations or scripts, you will need to update them to use the new `create_event` actionActions are used in several places in Home Assistant. As part of a script or automation, actions define what is going to happen once a trigger is activated. In scripts, an action is called _sequence_.[ [Learn more]](https://www.home-assistant.io/docs/automation/action/) instead.
([@epenet](https://github.com/epenet) - [#146432](https://github.com/home-assistant/core/pull/146432)) ([google docs](https://www.home-assistant.io/integrations/google))
Meater
The states of the Meater probe cook state have been changed to support translations and make them more consistent with other integrations.
The following states have been changed:
  * `Not Started` -> `not_started`
  * `Configured` -> `configured`
  * `Started` -> `started`
  * `Ready For Resting` -> `ready_for_resting`
  * `Resting` -> `resting`
  * `Slightly Underdone` -> `slightly_underdone`
  * `Finished` -> `finished`
  * `Slightly Overdone` -> `slightly_overdone`
  * `OVERCOOK!` -> `overcooked`


If you use these states in your automations or scripts, you will need to update them to use the new state values.
([@joostlek](https://github.com/joostlek) - [#146958](https://github.com/home-assistant/core/pull/146958)) ([meater docs](https://www.home-assistant.io/integrations/meater))
Miele
The internal representation of states for hob plates has changed. This is a breaking change when these states are used in automations or templates.
No user action is needed if these hob state sensors are used for visual display only.
Please review and update applicable automations and templates according to the following state changes:
  * `0` -> `plate_step_0`
  * `1` -> `plate_step_1`
  * …
  * `18` -> `plate_step_18`
  * `110` -> `plate_step_warm`
  * `117` -> `plate_step_boost`
  * `118` -> `plate_step_boost`
  * `217` -> `plate_step_boost`
  * `220` -> `plate_step_warm`


If you use these states in your automations or scripts, you will need to update them to use the new state values.
([@astrandb](https://github.com/astrandb) - [#144992](https://github.com/home-assistant/core/pull/144992)) ([miele docs](https://www.home-assistant.io/integrations/miele))
Plex Media Server
The previously deprecated `plex.scan_for_clients` actionActions are used in several places in Home Assistant. As part of a script or automation, actions define what is going to happen once a trigger is activated. In scripts, an action is called _sequence_.[ [Learn more]](https://www.home-assistant.io/docs/automation/action/) has been removed in favor of the “Scan Clients” `button` entityAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/). If you use this actionActions are used in several places in Home Assistant. As part of a script or automation, actions define what is going to happen once a trigger is activated. In scripts, an action is called _sequence_.[ [Learn more]](https://www.home-assistant.io/docs/automation/action/) in your automations or scripts, you will need to update them to use the new entityAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) instead.
([@epenet](https://github.com/epenet) - [#146608](https://github.com/home-assistant/core/pull/146608)) ([plex docs](https://www.home-assistant.io/integrations/plex))
If you are a custom integration developer and want to learn about changes and new features available for your integration: Be sure to follow our [developer blog](https://developers.home-assistant.io/blog/).
## All changes 
Of course, there is a lot more in this release. You can find a list of all changes made here: [Full changelog for Home Assistant Core 2025.7](https://www.home-assistant.io/changelogs/core-2025.7)
Back to top
