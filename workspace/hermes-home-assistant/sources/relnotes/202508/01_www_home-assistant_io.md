---
url: "https://www.home-assistant.io/blog/2025/08/06/release-20258/"
title: "2025.8: The summer of AI ☀️ - Home Assistant"
scraped_at: 2026-09-17T16:41:26+00:00
---

Home Assistant 2025.8! 🎉
In most parts of the world, summer mode is in full effect! ☀️ Many at the [Open Home Foundation](https://www.openhomefoundation.org/) and many of our contributors are enjoying a well-deserved break from work and open source. I hope that you are maybe enjoying a well-deserved break as well! 🏖️
Summer breaks or not, we are currently very busy with our next **product launch**! In case you have missed it, this upcoming Wednesday, August 13 (12:00 PM PT, 3:00 PM ET, 21:00 CEST), we will have [an extra live stream to announce the next big thing](https://www.youtube.com/watch?v=Z-pUkM6XIuA) in the Home Assistant Connect series! Be sure to [head over to YouTube to hit the reminder button](https://www.youtube.com/watch?v=Z-pUkM6XIuA) so you don’t miss it! **Z-Wave is not dead!** 🌊
Alright, on to the release! We keep moving during summer and are excited to bring you the August release of Home Assistant!
Let’s start with my personal favorite of this release: The improved experience when viewing a group, for example, a group helper with lights. 💡 When viewing such a group entity, you can now control the individual members of that group directly in that dialog. Super useful! I’m pretty sure that will be used a lot in our house.
But as the release title suggests, this release brings in an important foundation for new AI opportunities in Home Assistant: **AI Tasks**. Think of it as a way to delegate tasks to AI and get back the result of that task in a structured way so it can be used. Sounds vague? Dive into the release notes below!
Enjoy the release!
../Frenck
  * [AI in Home Assistant in 2025](https://www.home-assistant.io/blog/2025/08/06/release-20258/#ai-in-home-assistant-in-2025)
    * [Streaming Text-to-Speech for Home Assistant Cloud](https://www.home-assistant.io/blog/2025/08/06/release-20258/#streaming-text-to-speech-for-home-assistant-cloud)
    * [Integrate AI into your workflow using AI Task](https://www.home-assistant.io/blog/2025/08/06/release-20258/#integrate-ai-into-your-workflow-using-ai-task)
    * [Work faster with Suggest with AI buttons](https://www.home-assistant.io/blog/2025/08/06/release-20258/#work-faster-with-suggest-with-ai-buttons)
  * [Area dashboard improvements](https://www.home-assistant.io/blog/2025/08/06/release-20258/#area-dashboard-improvements)
  * [Integrations](https://www.home-assistant.io/blog/2025/08/06/release-20258/#integrations)
    * [New integrations](https://www.home-assistant.io/blog/2025/08/06/release-20258/#new-integrations)
    * [Noteworthy improvements to existing integrations](https://www.home-assistant.io/blog/2025/08/06/release-20258/#noteworthy-improvements-to-existing-integrations)
    * [Integration quality scale achievements](https://www.home-assistant.io/blog/2025/08/06/release-20258/#integration-quality-scale-achievements)
    * [Now available to set up from the UI](https://www.home-assistant.io/blog/2025/08/06/release-20258/#now-available-to-set-up-from-the-ui)
  * [Other noteworthy changes](https://www.home-assistant.io/blog/2025/08/06/release-20258/#other-noteworthy-changes)
    * [Control individual members of a group](https://www.home-assistant.io/blog/2025/08/06/release-20258/#control-individual-members-of-a-group)
    * [Weekdays in time trigger](https://www.home-assistant.io/blog/2025/08/06/release-20258/#weekdays-in-time-trigger)
    * [Energy flow on your energy dashboard](https://www.home-assistant.io/blog/2025/08/06/release-20258/#energy-flow-on-your-energy-dashboard)
  * [Patch releases](https://www.home-assistant.io/blog/2025/08/06/release-20258/#patch-releases)
    * [2025.8.1 - August 11](https://www.home-assistant.io/blog/2025/08/06/release-20258/#202581---august-11)
    * [2025.8.2 - August 15](https://www.home-assistant.io/blog/2025/08/06/release-20258/#202582---august-15)
    * [2025.8.3 - August 21](https://www.home-assistant.io/blog/2025/08/06/release-20258/#202583---august-21)
  * [Need help? Join the community!](https://www.home-assistant.io/blog/2025/08/06/release-20258/#need-help-join-the-community)
  * [Backward-incompatible changes](https://www.home-assistant.io/blog/2025/08/06/release-20258/#backward-incompatible-changes)


## AI in Home Assistant in 2025 
We introduced our first AI integration in Home Assistant 2023.2 where users could let OpenAI handle their interactions with Home Assistant Voice. Since that time, AI has seen a big surge in popularity within the Home Assistant community for _all kinds_ of use cases. Funny notifications when the laundry is done, analyzing what’s happening on a camera or skipping the song when AI determines [it’s a country song](https://www.reddit.com/r/homeautomation/comments/1at0re0/out_of_my_42_automations_this_is_my_best_one_by/) 😅.
Though AI gets many people excited, there are still people who would prefer not to have this technology in their smart homes. We want to accommodate everyone’s choices, whether that’s to use AI or not. These features won’t appear unless you set up an AI integration and configure some specific settings.
Last year, we sat down to determine how all these use cases, all complicated to achieve, could be made accessible to everyone. The first thing that came out of this was [integration sub-entries](https://www.home-assistant.io/blog/2025/07/02/release-20257/#integration-sub-entries), which we shipped in the last release. It allows users to configure their Ollama server or API key for OpenAI _once_ , and then create many different agents using different models or configuration underneath. In this release we’re building two new things you can optionally enable via these new sub-entries for AI integrations: _AI tasks_ and _Suggest with AI_. We’re also introducing a new integration, OpenRouter, which is a unified LLM interface giving access to over 400 extra LLM models.
Big thanks to our AI community contributors: [@AllenPorter](https://github.com/AllenPorter), [@shulyaka](https://github.com/shulyaka), [@tronikos](https://github.com/tronikos), [@IvanLH](https://github.com/IvanLH), and [@joostlek](https://github.com/joostlek)!
### Streaming Text-to-Speech for Home Assistant Cloud 
When you use Home Assistant Voice to talk to an AI, you can do a lot more than just control your home. LLMs can summarize the state of your home, and when using LLMs from Google and OpenAI, they can search the web to answer your questions with up-to-date information. This is great, but these answers can become quite long. Previously, voice responses wouldn’t begin until the AI had finished generating the entire answer, so longer replies meant a longer wait before anything was read aloud.
When a user waits for Home Assistant Voice to respond, long wait times really hurt the experience. We have overhauled Home Assistant so our Text-to-Speech system can start generating the response audio before the full response is done generating. Last release we launched this for [Piper](https://my.home-assistant.io/create-link/?redirect=supervisor_addon&addon=core_piper), our local Text-to-Speech system. In this release we’re making this available to the voices included in [Home Assistant Cloud](https://www.nabucasa.com) – the best way of supporting the Home Assistant project.
This improvement will especially benefit users who use local AI (which can be slow in generating responses) or users who play long announcements on their speakers.
### Integrate AI into your workflow using AI Task 
AI Task is a new integration that allows you to generate data using AI. After you add the “AI Task” sub-entry in your AI of choice, the entity will appear in the integration. This allows you to attach files or cameras and ask it what is happening. The output can either be given in text or formatted in a data structure of your choice. This is all accessible from the new `ai_task.generate_data` action, which can be embedded in automations, scripts, and template entities.
Below is an example of a template entity that updates every five minutes and counts the number of chickens in the coop. [Example inspired by this blog post.](https://houndhillhomestead.com/google-gemini-powered-goose-coop-door/)

```
template:
  - triggers:
      - trigger: homeassistant
        event: start
      - trigger: time_pattern
        minutes: "/5"
    actions:
      - action: ai_task.generate_data
        data:
          task_name: Count chickens
          instructions: -
            This is the inside of my goose coop. How many birds (chickens, geese, and
            ducks) are inside the coop?
          structure:
            birds:
              selector:
                number:
          attachments:
            media_content_id: media-source://camera/camera.chicken_coop
            media_content_type: image/jpeg
        response_variable: result
    sensor:
      - name: "Chickens"
        state: "{{ result.data.birds }}"
        state_class: total
```

YAML
Copy
To help get started with AI task, we’ve prepared a blueprint to analyze camera footage:
### Work faster with Suggest with AI buttons 
The AI Task integration has one extra feature under its belt: default entities. You can go to [**Settings** > **System** > **General**](https://my.home-assistant.io/redirect/general) and configure what AI Task entity you want to use as the default. With a default set, you no longer have to specify an entity when generating data, making it easier to share blueprints.
Setting a default also does more: When a default is configured, and only then, a new type of button will start showing up in different places in Home Assistant:
This button is not visible by default and will only appear if you enable it in the “AI suggestions” settings. For this release, the button has been added to the save dialog for automations and scripts. It helps users come up with a name, description, category, and label, while taking into account your current labels and other automation/script names. Keep in mind that generating this text sends the full contents of the automation or script, along with the names of your other automations/scripts and labels, to the LLM. So, this may be a task you will want to relegate to your shiny new local LLM.
## Area dashboard improvements 
We’ve added a small improvement to the areas dashboard based on your feedback. You can now choose to show the first camera in an area, or its image or icon, in the area dashboard editor. It’s a simple way to make certain area cards stand out a bit more—especially handy if you want quicker visual access to specific spaces.
## Integrations 
Thanks to our community for keeping pace with the new integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) and improvements to existing ones! You’re all awesome 🥰
### New integrations 
We welcome the following new integrations in this release:
  * , added by [@joostlek](https://github.com/joostlek) Access over 400 different large language models through the OpenRouter API, providing a unified interface for AI integrations in your automations.
  * **[Ubiquiti UISP airOS](https://www.home-assistant.io/integrations/airos)** , added by [@CoMPaTech](https://github.com/CoMPaTech) Monitor and manage airOS devices through their local API, providing performance metrics and device status information of your wireless point-to-point infrastructure.
  * , added by [@tr4nt0r](https://github.com/tr4nt0r) Monitor the uptime and status of your services and websites with Uptime Kuma, keeping track of your infrastructure health directly in Home Assistant.
  * , added by [@thomasddn](https://github.com/thomasddn) Connect your Volvo vehicle to Home Assistant for remote monitoring of battery status, location, and other vehicle information.


This release also has new virtual integrations. Virtual integrations are stubs that are handled by other (existing) integrations to help with findability. These ones are new:
  * , provided by [Whirlpool Appliances](https://www.home-assistant.io/integrations/whirlpool), added by [@thost96](https://github.com/thost96)
  * , provided by [Fibaro](https://www.home-assistant.io/integrations/fibaro), added by [@rappenze](https://github.com/rappenze)


### Noteworthy improvements to existing integrations 
It is not just new integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) that have been added; existing integrations are also being constantly improved. Here are some of the noteworthy changes to existing integrations:
  * The [PlayStation Network](https://www.home-assistant.io/integrations/playstation_network) integration received major updates from [@tr4nt0r](https://github.com/tr4nt0r) and [@JackJPowell](https://github.com/JackJPowell), adding sensors to track your and your friends’ online status, currently playing game, and last online time. Also a binary sensor for your PS Plus subscription status, and a notification platform. PS Vita is now supported as well!
  * [Reolink](https://www.home-assistant.io/integrations/reolink) cameras got multiple enhancements from [@starkillerOG](https://github.com/starkillerOG): WiFi signal sensors for IP cameras, post-recording time controls, and pre-recording entities.
  * The [AI Task](https://www.home-assistant.io/integrations/ai_task) and [OpenAI Conversation](https://www.home-assistant.io/integrations/openai_conversation) integrations now support camera and file attachments, thanks to [@balloob](https://github.com/balloob).
  * [YoLink](https://www.home-assistant.io/integrations/yolink) device support expanded with [@matrixd2](https://github.com/matrixd2) adding support for the YS8009, YS7A12, and YS6614 devices.
  * [@ricohageman](https://github.com/ricohageman) added dew point sensors to the [Awair](https://www.home-assistant.io/integrations/awair) integration.
  * [@bieniu](https://github.com/bieniu) enhanced both [GIOS](https://www.home-assistant.io/integrations/gios) and [IMGW PIB](https://www.home-assistant.io/integrations/imgw_pib) integrations with new sensors, including water flow monitoring for IMGW PIB.
  * [WiZ](https://www.home-assistant.io/integrations/wiz) now supports fans, added by [@arturpragacz](https://github.com/arturpragacz).
  * [SwitchBot Cloud](https://www.home-assistant.io/integrations/switchbot_cloud) gained fan platform support from [@XiaoLing-git](https://github.com/XiaoLing-git).
  * [Velux](https://www.home-assistant.io/integrations/velux) windows with rain sensors can now detect precipitation, thanks to [@wollew](https://github.com/wollew).
  * [SmartThings](https://www.home-assistant.io/integrations/smartthings) added vacuum support, implemented by [@jennoian](https://github.com/jennoian).
  * [AmberElectric](https://www.home-assistant.io/integrations/amberelectric) now provides forecast services, added by [@madpilot](https://github.com/madpilot).
  * [OSO Energy](https://www.home-assistant.io/integrations/osoenergy) got holiday mode services and custom away mode functionality from [@osohotwateriot](https://github.com/osohotwateriot).
  * [Nord Pool](https://www.home-assistant.io/integrations/nordpool) gained normalized price indices service, thanks to [@gjohansson-ST](https://github.com/gjohansson-ST).
  * [Matter](https://www.home-assistant.io/integrations/matter) continues to expand with microwave oven and temperature control device support from [@lboue](https://github.com/lboue).
  * [@noahhusby](https://github.com/noahhusby) added play media support to [Russound RIO](https://www.home-assistant.io/integrations/russound_rio).
  * [Pi-hole](https://www.home-assistant.io/integrations/pi_hole) users can now leverage API v6 functionality, enabled by [@HarvsG](https://github.com/HarvsG).
  * [Immich](https://www.home-assistant.io/integrations/immich) users can now upload files directly through a new action, implemented by [@mib1185](https://github.com/mib1185).
  * [KNX](https://www.home-assistant.io/integrations/knx) now includes a new group monitor with improved filtering and search options, thanks to [@philippwaller](https://github.com/philippwaller).


### Integration quality scale achievements 
One thing we are incredibly proud of in Home Assistant is our [integration quality scale](https://www.home-assistant.io/docs/quality_scale/). This scale helps us and our contributors to ensure integrations are of high quality, maintainable, and provide the best possible user experience.
This release, we celebrate several integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) that have improved their quality scale:
  * **5 integrations reached platinum** 🏆
    * [AirGradient](https://www.home-assistant.io/integrations/airgradient), thanks to [@joostlek](https://github.com/joostlek)
    * [inexogy](https://www.home-assistant.io/integrations/discovergy), thanks to [@jpbede](https://github.com/jpbede)
    * [EHEIM Digital](https://www.home-assistant.io/integrations/eheimdigital), thanks to [@autinerd](https://github.com/autinerd)
    * [Pegel Online](https://www.home-assistant.io/integrations/pegel_online), thanks to [@mib1185](https://github.com/mib1185)
    * [Tankerkönig](https://www.home-assistant.io/integrations/tankerkoenig), thanks to [@mib1185](https://github.com/mib1185)
  * **3 integrations reached silver** 🥈
    * [Amazon Alexa Devices](https://www.home-assistant.io/integrations/alexa_devices), thanks to [@chemelli74](https://github.com/chemelli74)
    * [Homee](https://www.home-assistant.io/integrations/homee), thanks to [@Taraman17](https://github.com/Taraman17)
    * [Mealie](https://www.home-assistant.io/integrations/mealie), thanks to [@andrew-codechimp](https://github.com/andrew-codechimp)
  * **2 integrations reached bronze** 🥉
    * [Onkyo](https://www.home-assistant.io/integrations/onkyo), thanks to [@arturpragacz](https://github.com/arturpragacz)
    * [Ring](https://www.home-assistant.io/integrations/ring), thanks to [@sdb9696](https://github.com/sdb9696)


This is a huge achievement for these integrations and their maintainers. The effort and dedication required to reach these quality levels is significant, as it involves extensive testing, documentation, error handling, and often complete rewrites of parts of the integration.
A big thank you to all the contributors involved! 👏
### Now available to set up from the UI 
While most integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) can be set up directly from the Home Assistant user interface, some were only available using YAML configuration. We keep moving more integrations to the UI, making them more accessible for everyone to set up and use.
The following integration is now available via the Home Assistant UI:
  * , done by [@avedor](https://github.com/avedor)


## Other noteworthy changes 
There are many more improvements in this release; here are some of the other noteworthy changes:
  * Home Assistant’s interface has received a refresh for better accessibility! The primary color and button colors have been updated to meet [WCAG AA accessibility standards](https://www.w3.org/WAI/WCAG2AA-Conformance), improving contrast and readability throughout the interface. All buttons have been redesigned with distinct styles, sizes, and visual priority variants, making it much easier to distinguish between primary, secondary, and less prominent actions. This marks the beginning of a broader effort to update other UI components for improved accessibility and consistency across Home Assistant.
  * [@mib1185](https://github.com/mib1185) added a new device class for **absolute humidity** with support for both sensor and number entitiesAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/). Nice!
  * Group management was improved by [@piitaya](https://github.com/piitaya), who added the ability to reorder members within a group, making it easier to organize your device groups exactly how you want them. Thanks!
  * System diagnostics was extended by [@balloob](https://github.com/balloob) with the addition of a device analytics dump download feature. Awesome!
  * The [History Stats](https://www.home-assistant.io/integrations/history_stats) integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) now includes a preview in the options flow, thanks to [@karwosts](https://github.com/karwosts). This makes it easier to configure your history statistics.
  * The [Template](https://www.home-assistant.io/integrations/template) integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) received a massive update from [@Petro31](https://github.com/Petro31)! Here’s what’s new: 
    * Trigger-based numeric sensors can now be set to unknown state
    * The cover, fan, light, lock, and vacuum platforms are now supported in the UI
    * Availability templates are now supported in the UI for all available platforms
    * Preview entity has been added to the UI for alarm control panel and select platforms
    * Template locks now support the opening state
    * The alarm control panel, fan, light, lock, switch, and vacuum platforms now support all optimistic YAML modes


### Control individual members of a group 
[Groups](https://www.home-assistant.io/integrations/group) are a great way to control multiple entitiesAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) at once, but sometimes you want to control individual members of a group.
So, for this release, [@piitaya](https://github.com/piitaya) and [@MindFreeze](https://github.com/MindFreeze) improved the entity information dialog to show the individual members of a light and cover group, allowing you to control them directly from that dialog. Super useful!
### Weekdays in time trigger 
The [time trigger](https://www.home-assistant.io/docs/automation/trigger/#time-trigger) is already very useful, but [@hmmbob](https://github.com/hmmbob) had [a feature request](https://github.com/orgs/home-assistant/discussions/26) that could improve it even more.
He suggested adding the ability to specify weekdays in the time trigger, allowing users to create automations that only trigger at a specific time on specific days of the week.
This feature has been implemented in this release, allowing you to specify the weekdays in the time trigger. This is especially useful for automations that need to run on specific days, such as weekdays or weekends.
### Energy flow on your energy dashboard 
The Home Assistant energy dashboard is great, but as of this release it’s even a little better!
Based on the [Sankey Chart custom card](https://github.com/MindFreeze/ha-sankey-chart), [@MindFreeze](https://github.com/MindFreeze) added a new energy flow visualization for the energy dashboard, which shows exactly where your energy is coming from and where it is going to.
Really cool addition to the energy dashboard [@MindFreeze](https://github.com/MindFreeze)!
## Patch releases 
We will also release patch releases for Home Assistant 2025.8 in August. These patch releases only contain bug fixes. Our goal is to release a patch release once a week, aiming for Friday.
### 2025.8.1 - August 11 
  * Make Tuya complex type handling explicit ([@epenet](https://github.com/epenet) - [#149677](https://github.com/home-assistant/core/pull/149677))
  * Fix Enigma2 startup hang ([@BlackBadPinguin](https://github.com/BlackBadPinguin) - [#149756](https://github.com/home-assistant/core/pull/149756))
  * Fix dialog enhancement switch for Sonos Arc Ultra ([@PeteRager](https://github.com/PeteRager) - [#150116](https://github.com/home-assistant/core/pull/150116))
  * Bump ZHA to 0.0.67 ([@puddly](https://github.com/puddly) - [#150132](https://github.com/home-assistant/core/pull/150132))
  * Bump airOS to 0.2.6 improving device class matching more devices ([@CoMPaTech](https://github.com/CoMPaTech) - [#150134](https://github.com/home-assistant/core/pull/150134))
  * Handle HusqvarnaWSClientError ([@Thomas55555](https://github.com/Thomas55555) - [#150145](https://github.com/home-assistant/core/pull/150145))
  * Fix Progettihwsw config flow ([@gaspa85](https://github.com/gaspa85) - [#150149](https://github.com/home-assistant/core/pull/150149))
  * Bump imgw_pib to version 1.5.3 ([@bieniu](https://github.com/bieniu) - [#150178](https://github.com/home-assistant/core/pull/150178))
  * Fix description of `button.press` action ([@NoRi2909](https://github.com/NoRi2909) - [#150181](https://github.com/home-assistant/core/pull/150181))
  * Migrate unique_id only if monitor_id is present in Uptime Kuma ([@tr4nt0r](https://github.com/tr4nt0r) - [#150197](https://github.com/home-assistant/core/pull/150197))
  * Silence vacuum battery deprecation for built in integrations ([@MartinHjelmare](https://github.com/MartinHjelmare) - [#150204](https://github.com/home-assistant/core/pull/150204))
  * Bump ZHA to 0.0.68 ([@puddly](https://github.com/puddly) - [#150208](https://github.com/home-assistant/core/pull/150208))
  * Bump hass-nabucasa from 0.111.1 to 0.111.2 ([@ludeeus](https://github.com/ludeeus) - [#150209](https://github.com/home-assistant/core/pull/150209))
  * Fix JSON serialization for ZHA diagnostics download ([@puddly](https://github.com/puddly) - [#150210](https://github.com/home-assistant/core/pull/150210))
  * Ignore MQTT vacuum battery warning ([@MartinHjelmare](https://github.com/MartinHjelmare) - [#150211](https://github.com/home-assistant/core/pull/150211))
  * Handle Unifi Protect BadRequest exception during API key creation ([@RaHehl](https://github.com/RaHehl) - [#150223](https://github.com/home-assistant/core/pull/150223))
  * Fix Tibber coordinator ContextVar warning ([@MartinHjelmare](https://github.com/MartinHjelmare) - [#150229](https://github.com/home-assistant/core/pull/150229))
  * Fix handing for zero volume error in Squeezebox ([@peteS-UK](https://github.com/peteS-UK) - [#150265](https://github.com/home-assistant/core/pull/150265))
  * Fix error on startup when no Apps or Radio plugins are installed for Squeezebox ([@peteS-UK](https://github.com/peteS-UK) - [#150267](https://github.com/home-assistant/core/pull/150267))
  * Volvo: fix missing charging power options ([@thomasddn](https://github.com/thomasddn) - [#150272](https://github.com/home-assistant/core/pull/150272))
  * Constraint num2words to 0.5.14 ([@edenhaus](https://github.com/edenhaus) - [#150276](https://github.com/home-assistant/core/pull/150276))
  * Volvo: fix distance to empty battery ([@thomasddn](https://github.com/thomasddn) - [#150278](https://github.com/home-assistant/core/pull/150278))
  * Add GPT-5 support ([@Shulyaka](https://github.com/shulyaka) - [#150281](https://github.com/home-assistant/core/pull/150281))
  * Volvo: Skip unsupported API fields ([@thomasddn](https://github.com/thomasddn) - [#150285](https://github.com/home-assistant/core/pull/150285))
  * Remove misleading “the” from Launch Library configuration ([@NoRi2909](https://github.com/NoRi2909) - [#150288](https://github.com/home-assistant/core/pull/150288))
  * Set suggested display precision on Volvo energy/fuel consumption sensors ([@steinmn](https://github.com/steinmn) - [#150296](https://github.com/home-assistant/core/pull/150296))
  * Bump airOS to 0.2.7 supporting firmware 8.7.11 ([@CoMPaTech](https://github.com/CoMPaTech) - [#150298](https://github.com/home-assistant/core/pull/150298))
  * Update knx-frontend to 2025.8.9.63154 ([@philippwaller](https://github.com/philippwaller) - [#150323](https://github.com/home-assistant/core/pull/150323))
  * Update frontend to 20250811.0 ([@bramkragten](https://github.com/bramkragten) - [#150404](https://github.com/home-assistant/core/pull/150404))
  * Handle empty electricity RAW sensors in Tuya ([@epenet](https://github.com/epenet) - [#150406](https://github.com/home-assistant/core/pull/150406))
  * Lower Z-Wave firmware check delay ([@MartinHjelmare](https://github.com/MartinHjelmare) - [#150411](https://github.com/home-assistant/core/pull/150411))
  * Fix issue with Tuya suggested unit ([@epenet](https://github.com/epenet) - [#150414](https://github.com/home-assistant/core/pull/150414))


### 2025.8.2 - August 15 
  * Add pymodbus to package constraints ([@epenet](https://github.com/epenet) - [#150420](https://github.com/home-assistant/core/pull/150420))
  * Fix enphase_envoy non existing via device warning at first config. ([@catsmanac](https://github.com/catsmanac) - [#149010](https://github.com/home-assistant/core/pull/149010))
  * Handle non-streaming TTS case correctly ([@synesthesiam](https://github.com/synesthesiam) - [#150218](https://github.com/home-assistant/core/pull/150218))
  * Pi_hole - Account for auth succeeding when it shouldn’t ([@HarvsG](https://github.com/HarvsG) - [#150413](https://github.com/home-assistant/core/pull/150413))
  * Bump habiticalib to version 0.4.2 ([@tr4nt0r](https://github.com/tr4nt0r) - [#150417](https://github.com/home-assistant/core/pull/150417))
  * Fix optimistic set to false for template entities ([@Petro31](https://github.com/Petro31) - [#150421](https://github.com/home-assistant/core/pull/150421))
  * Fix error of the Powerfox integration in combination with the new Powerfox FLOW adapter ([@DavidCraftDev](https://github.com/DavidCraftDev) - [#150429](https://github.com/home-assistant/core/pull/150429))
  * Bump python-snoo to 0.7.0 ([@kevin-david](https://github.com/kevin-david) - [#150434](https://github.com/home-assistant/core/pull/150434))
  * Fix brightness command not sent when in white color mode ([@wedsa5](https://github.com/wedsa5) - [#150439](https://github.com/home-assistant/core/pull/150439))
  * Bump cookidoo-api to 0.14.0 ([@miaucl](https://github.com/miaucl) - [#150450](https://github.com/home-assistant/core/pull/150450))
  * Fix YoLink valve state when device running in class A mode ([@matrixd2](https://github.com/matrixd2) - [#150456](https://github.com/home-assistant/core/pull/150456))
  * Additional Fix error on startup when no Apps or Radio plugins are installed for Squeezebox ([@peteS-UK](https://github.com/peteS-UK) - [#150475](https://github.com/home-assistant/core/pull/150475))
  * Fix re-auth flow for Volvo integration ([@thomasddn](https://github.com/thomasddn) - [#150478](https://github.com/home-assistant/core/pull/150478))
  * Improve Z-Wave manual config flow step description ([@MartinHjelmare](https://github.com/MartinHjelmare) - [#150479](https://github.com/home-assistant/core/pull/150479))
  * Add missing boost2 code for Miele hobs ([@astrandb](https://github.com/astrandb) - [#150481](https://github.com/home-assistant/core/pull/150481))
  * Bump airOS to 0.2.8 ([@CoMPaTech](https://github.com/CoMPaTech) - [#150504](https://github.com/home-assistant/core/pull/150504))
  * Bump aiowebostv to 0.7.5 ([@thecode](https://github.com/thecode) - [#150514](https://github.com/home-assistant/core/pull/150514))
  * Bump bleak-retry-connector to 4.0.1 ([@bdraco](https://github.com/bdraco) - [#150515](https://github.com/home-assistant/core/pull/150515))
  * Bump aiodhcpwatcher to 1.2.1 ([@bdraco](https://github.com/bdraco) - [#150519](https://github.com/home-assistant/core/pull/150519))
  * Bump python-snoo to 0.8.1 ([@Lash-L](https://github.com/Lash-L) - [#150530](https://github.com/home-assistant/core/pull/150530))
  * Bump uv to 0.8.9 ([@edenhaus](https://github.com/edenhaus) - [#150542](https://github.com/home-assistant/core/pull/150542))
  * Bump python-snoo to 0.8.2 ([@Lash-L](https://github.com/Lash-L) - [#150569](https://github.com/home-assistant/core/pull/150569))
  * Change Snoo to use MQTT instead of PubNub ([@Lash-L](https://github.com/Lash-L) - [#150570](https://github.com/home-assistant/core/pull/150570))
  * Make sure we update the api version in philips_js discovery ([@elupus](https://github.com/elupus) - [#150604](https://github.com/home-assistant/core/pull/150604))
  * Bump pymiele to 0.5.3 ([@astrandb](https://github.com/astrandb) - [#150216](https://github.com/home-assistant/core/pull/150216))
  * Bump pymiele to 0.5.4 ([@astrandb](https://github.com/astrandb) - [#150605](https://github.com/home-assistant/core/pull/150605))
  * Bump airOS to 0.2.11 ([@CoMPaTech](https://github.com/CoMPaTech) - [#150627](https://github.com/home-assistant/core/pull/150627))
  * Bump uiprotect to 7.21.1 ([@bdraco](https://github.com/bdraco) - [#150657](https://github.com/home-assistant/core/pull/150657))
  * Bump onvif-zeep-async to 4.0.3 ([@bdraco](https://github.com/bdraco) - [#150663](https://github.com/home-assistant/core/pull/150663))
  * Bump python-snoo to 0.8.3 ([@Lash-L](https://github.com/Lash-L) - [#150670](https://github.com/home-assistant/core/pull/150670))
  * Fix missing labels for subdiv in workday ([@gjohansson-ST](https://github.com/gjohansson-ST) - [#150684](https://github.com/home-assistant/core/pull/150684))
  * Improve handling decode errors in rest ([@gjohansson-ST](https://github.com/gjohansson-ST) - [#150699](https://github.com/home-assistant/core/pull/150699))


### 2025.8.3 - August 21 
  * Bump to zcc-helper==3.6 ([@markhannon](https://github.com/markhannon) - [#150608](https://github.com/home-assistant/core/pull/150608)) ([zimi docs](https://www.home-assistant.io/integrations/zimi/))
  * fix(amberelectric): add request timeouts ([@JP-Ellis](https://github.com/JP-Ellis) - [#150613](https://github.com/home-assistant/core/pull/150613)) ([amberelectric docs](https://www.home-assistant.io/integrations/amberelectric/))
  * Bump renault-api to 0.4.0 ([@epenet](https://github.com/epenet) - [#150624](https://github.com/home-assistant/core/pull/150624)) ([renault docs](https://www.home-assistant.io/integrations/renault/))
  * Update hassfest package exceptions ([@cdce8p](https://github.com/cdce8p) - [#150744](https://github.com/home-assistant/core/pull/150744))
  * Bump boschshcpy to 0.2.107 ([@tschamm](https://github.com/tschamm) - [#150754](https://github.com/home-assistant/core/pull/150754)) ([bosch_shc docs](https://www.home-assistant.io/integrations/bosch_shc/))
  * Fix for bosch_shc: ‘device_registry.async_get_or_create’ referencing a non existing ‘via_device’ ([@tschamm](https://github.com/tschamm) - [#150756](https://github.com/home-assistant/core/pull/150756)) ([bosch_shc docs](https://www.home-assistant.io/integrations/bosch_shc/))
  * Fix volume step error in Squeezebox media player ([@peteS-UK](https://github.com/peteS-UK) - [#150760](https://github.com/home-assistant/core/pull/150760)) ([squeezebox docs](https://www.home-assistant.io/integrations/squeezebox/))
  * Show charging power as 0 when not charging for the Volvo integration ([@thomasddn](https://github.com/thomasddn) - [#150797](https://github.com/home-assistant/core/pull/150797)) ([volvo docs](https://www.home-assistant.io/integrations/volvo/))
  * Pin gql to 3.5.3 ([@joostlek](https://github.com/joostlek) - [#150800](https://github.com/home-assistant/core/pull/150800))
  * Bump opower to 0.15.2 ([@tronikos](https://github.com/tronikos) - [#150809](https://github.com/home-assistant/core/pull/150809)) ([opower docs](https://www.home-assistant.io/integrations/opower/))
  * Include device data in Withings diagnostics ([@joostlek](https://github.com/joostlek) - [#150816](https://github.com/home-assistant/core/pull/150816)) ([withings docs](https://www.home-assistant.io/integrations/withings/))
  * Abort Nanoleaf discovery flows with user flow ([@joostlek](https://github.com/joostlek) - [#150818](https://github.com/home-assistant/core/pull/150818)) ([nanoleaf docs](https://www.home-assistant.io/integrations/nanoleaf/))
  * Bump yt-dlp to 2025.08.11 ([@joostlek](https://github.com/joostlek) - [#150821](https://github.com/home-assistant/core/pull/150821)) ([media_extractor docs](https://www.home-assistant.io/integrations/media_extractor/))
  * Initialize the coordinator’s data to include data.options. ([@LG-ThinQ-Integration](https://github.com/LG-ThinQ-Integration) - [#150839](https://github.com/home-assistant/core/pull/150839)) ([lg_thinq docs](https://www.home-assistant.io/integrations/lg_thinq/))
  * Handle Z-Wave RssiErrorReceived ([@MartinHjelmare](https://github.com/MartinHjelmare) - [#150846](https://github.com/home-assistant/core/pull/150846)) ([zwave_js docs](https://www.home-assistant.io/integrations/zwave_js/))
  * Use correct unit and class for the Imeon inverter sensors ([@Imeon-Energy](https://github.com/Imeon-Energy) - [#150847](https://github.com/home-assistant/core/pull/150847)) ([imeon_inverter docs](https://www.home-assistant.io/integrations/imeon_inverter/))
  * Bump holidays to 0.79 ([@gjohansson-ST](https://github.com/gjohansson-ST) - [#150857](https://github.com/home-assistant/core/pull/150857)) ([workday docs](https://www.home-assistant.io/integrations/workday/)) ([holiday docs](https://www.home-assistant.io/integrations/holiday/))
  * Bump aiorussound to 4.8.1 ([@noahhusby](https://github.com/noahhusby) - [#150858](https://github.com/home-assistant/core/pull/150858)) ([russound_rio docs](https://www.home-assistant.io/integrations/russound_rio/))
  * Add missing unsupported reasons to list ([@agners](https://github.com/agners) - [#150866](https://github.com/home-assistant/core/pull/150866)) ([hassio docs](https://www.home-assistant.io/integrations/hassio/))
  * Fix icloud service calls ([@epenet](https://github.com/epenet) - [#150881](https://github.com/home-assistant/core/pull/150881)) ([icloud docs](https://www.home-assistant.io/integrations/icloud/))
  * Bump pysmartthings to 3.2.9 ([@joostlek](https://github.com/joostlek) - [#150892](https://github.com/home-assistant/core/pull/150892)) ([smartthings docs](https://www.home-assistant.io/integrations/smartthings/))
  * Fix PWA theme color to match darker blue color scheme in 2025.8 ([@balloob](https://github.com/balloob) - [#150896](https://github.com/home-assistant/core/pull/150896)) ([frontend docs](https://www.home-assistant.io/integrations/frontend/))
  * Bump bleak-retry-connector to 4.0.2 ([@bdraco](https://github.com/bdraco) - [#150899](https://github.com/home-assistant/core/pull/150899)) ([bluetooth docs](https://www.home-assistant.io/integrations/bluetooth/))
  * update pyatmo to v9.2.3 ([@cgtobi](https://github.com/cgtobi) - [#150900](https://github.com/home-assistant/core/pull/150900)) ([netatmo docs](https://www.home-assistant.io/integrations/netatmo/))
  * Fix structured output object selector conversion for OpenAI ([@balloob](https://github.com/balloob) - [#150916](https://github.com/home-assistant/core/pull/150916)) ([openai_conversation docs](https://www.home-assistant.io/integrations/openai_conversation/))
  * Matter valve Open command doesn’t support TargetLevel=0 ([@kepstin](https://github.com/kepstin) - [#150922](https://github.com/home-assistant/core/pull/150922)) ([matter docs](https://www.home-assistant.io/integrations/matter/))
  * Bump ESPHome minimum stable BLE version to 2025.8.0 ([@bdraco](https://github.com/bdraco) - [#150924](https://github.com/home-assistant/core/pull/150924)) ([esphome docs](https://www.home-assistant.io/integrations/esphome/))
  * Bump imgw-pib to version 1.5.4 ([@bieniu](https://github.com/bieniu) - [#150930](https://github.com/home-assistant/core/pull/150930)) ([imgw_pib docs](https://www.home-assistant.io/integrations/imgw_pib/))
  * Fix update retry for Imeon inverter integration ([@Imeon-Energy](https://github.com/Imeon-Energy) - [#150936](https://github.com/home-assistant/core/pull/150936)) ([imeon_inverter docs](https://www.home-assistant.io/integrations/imeon_inverter/))
  * Bump python-mystrom to 2.5.0 ([@elsi06](https://github.com/elsi06) - [#150947](https://github.com/home-assistant/core/pull/150947)) ([mystrom docs](https://www.home-assistant.io/integrations/mystrom/))
  * Ask user for Z-Wave RF region if country is missing ([@MartinHjelmare](https://github.com/MartinHjelmare) - [#150959](https://github.com/home-assistant/core/pull/150959)) ([zwave_js docs](https://www.home-assistant.io/integrations/zwave_js/))
  * Bump onvif-zeep-async to 4.0.4 ([@bdraco](https://github.com/bdraco) - [#150969](https://github.com/home-assistant/core/pull/150969)) ([onvif docs](https://www.home-assistant.io/integrations/onvif/))
  * Except ujson from license check ([@emontnemery](https://github.com/emontnemery) - [#150980](https://github.com/home-assistant/core/pull/150980))
  * Enable country site autodetection in Alexa Devices ([@chemelli74](https://github.com/chemelli74) - [#150989](https://github.com/home-assistant/core/pull/150989)) ([alexa_devices docs](https://www.home-assistant.io/integrations/alexa_devices/))
  * Update frontend to 20250811.1 ([@bramkragten](https://github.com/bramkragten) - [#151005](https://github.com/home-assistant/core/pull/151005)) ([frontend docs](https://www.home-assistant.io/integrations/frontend/))


## Need help? Join the community! 
Home Assistant has a great community of users who are all more than willing to help each other out. So, join us!
Our very active [Discord chat server](https://www.home-assistant.io/join-chat) is an excellent place to be, and don’t forget to join our amazing [forums](https://community.home-assistant.io/).
Found a bug or issue? Please report it in our [issue tracker](https://github.com/home-assistant/core/issues) to get it fixed! Or check [our help page](https://www.home-assistant.io/help) for guidance on more places you can go.
Are you more into email? [Sign up for the Open Home Foundation Newsletter](https://www.home-assistant.io/newsletter) to get the latest news about features, things happening in our community, and other projects that support the Open Home straight into your inbox.
## Backward-incompatible changes 
We do our best to avoid making changes to existing functionality that might unexpectedly impact your Home Assistant installation. Unfortunately, sometimes, it is inevitable.
We always make sure to document these changes to make the transition as easy as possible for you. This release has the following backward-incompatible changes:
Android Debug Bridge (ADB)
Android Debug Bridge media players entities now report to be off where they previously reported to be in standby state.
If you have automations or scripts that rely on the Android Debug Bridge media player reporting standby state, you will need to update them to use the new `off` state.
([@emontnemery](https://github.com/emontnemery) - [#148130](https://github.com/home-assistant/core/pull/148130)) ([documentation](https://www.home-assistant.io/integrations/androidtv))
Apple TV
Apple TV media players entities now report to be off where they previously reported to be in standby state.
If you have automations or scripts that rely on the Apple TV media player reporting standby state, you will need to update them to use the new `off` state.
([@emontnemery](https://github.com/emontnemery) - [#148132](https://github.com/home-assistant/core/pull/148132)) ([documentation](https://www.home-assistant.io/integrations/apple_tv))
Cambridge Audio
Cambridge Audio media players entities now report to be off where they previously reported to be in standby state.
If you have automations or scripts that rely on the Cambridge Audio media player reporting standby state, you will need to update them to use the new `off` state.
([@emontnemery](https://github.com/emontnemery) - [#148133](https://github.com/home-assistant/core/pull/148133)) ([documentation](https://www.home-assistant.io/integrations/cambridge_audio))
Ecovacs
The battery property on vacuum entities is being removed in Home Assistant. Therefore, this property is now removed from this integration and is replaced by a battery level sensor.
Please review your automations, scripts or cards using the battery property and update the code to use the battery sensor instead.
([@mib1185](https://github.com/mib1185) - [#149084](https://github.com/home-assistant/core/pull/149084)) ([@edenhaus](https://github.com/edenhaus) - [#149581](https://github.com/home-assistant/core/pull/149581)) ([documentation](https://www.home-assistant.io/integrations/ecovacs))
Husqvarna Automower
The summary field of calendar events provided by the Husqvarna Automower calendar platform has been updated to include the device name as a prefix. This change improves clarity when multiple mowers are used, but may affect automations relying on the previous summary format.
([@Thomas55555](https://github.com/Thomas55555) - [#147405](https://github.com/home-assistant/core/pull/147405)) ([documentation](https://www.home-assistant.io/integrations/husqvarna_automower))
LOOKin
LOOKin media players entities now report to be off where they previously reported to be in standby state.
If you have automations or scripts that rely on the LOOKin media player reporting standby state, you will need to update them to use the new `off` state.
([@emontnemery](https://github.com/emontnemery) - [#148134](https://github.com/home-assistant/core/pull/148134)) ([documentation](https://www.home-assistant.io/integrations/lookin))
Matter
The battery property on vacuum entities is being removed in Home Assistant. Therefore, this property is now removed from this integration and is replaced by a battery level sensor.
Please review your automations, scripts or cards using the battery property and update the code to use the battery sensor instead.
([@MartinHjelmare](https://github.com/MartinHjelmare) - [#150061](https://github.com/home-assistant/core/pull/150061)) ([documentation](https://www.home-assistant.io/integrations/matter))
Mediaroom
Mediaroom media players entities now report to be off where they previously reported to be in standby state.
If you have automations or scripts that rely on the Mediaroom media player reporting standby state, you will need to update them to use the new `off` state.
([@emontnemery](https://github.com/emontnemery) - [#148135](https://github.com/home-assistant/core/pull/148135)) ([documentation](https://www.home-assistant.io/integrations/mediaroom))
Miele
The battery property on vacuum entities is being removed in Home Assistant. Therefore, this property is now removed from this integration and is replaced by a battery level sensor.
Please review your automations, scripts or cards using the battery property and update the code to use the battery sensor instead.
([@astrandb](https://github.com/astrandb) - [#148765](https://github.com/home-assistant/core/pull/148765)) ([documentation](https://www.home-assistant.io/integrations/miele))
Reolink
The Reolink Wi-Fi signal strength sensor has changed from an indicator value between 0 and 4 (amount of bars) to a value in dBm between -85 dBm and -30 dBm.
Note that all values in this range are possible, but roughly the old values can be converted like this:
  * 0 > -85 dBm
  * 1 > -75 dBm
  * 2 > -65 dBm
  * 3 > -55 dBm
  * 4 > -45 dBm


([@starkillerOG](https://github.com/starkillerOG) - [#149191](https://github.com/home-assistant/core/pull/149191)) ([documentation](https://www.home-assistant.io/integrations/reolink))
Roborock
The battery property on vacuum entities is being removed in Home Assistant. Therefore, this property is now removed from this integration and is replaced by a battery level sensor.
Please review your automations, scripts or cards using the battery property and update the code to use the battery sensor instead.
([@luca-angemi](https://github.com/luca-angemi) - [#150126](https://github.com/home-assistant/core/pull/150126)) ([documentation](https://www.home-assistant.io/integrations/roborock))
Roku
Roku media players entities now report to be off where they previously reported to be in standby state.
If you have automations or scripts that rely on the Roku media player reporting standby state, you will need to update them to use the new `off` state.
([@emontnemery](https://github.com/emontnemery) - [#148137](https://github.com/home-assistant/core/pull/148137)) ([documentation](https://www.home-assistant.io/integrations/roku))
Snapcast
Snapcast media players entities now report to be off where they previously reported to be in standby state.
If you have automations or scripts that rely on the Snapcast media player reporting standby state, you will need to update them to use the new `off` state.
([@emontnemery](https://github.com/emontnemery) - [#148138](https://github.com/home-assistant/core/pull/148138)) ([documentation](https://www.home-assistant.io/integrations/snapcast))
Sony PlayStation 4
Sony PlayStation 4 media players entities now report to be off where they previously reported to be in standby state.
If you have automations or scripts that rely on the Sony PlayStation 4 media player reporting standby state, you will need to update them to use the new `off` state.
([@emontnemery](https://github.com/emontnemery) - [#148136](https://github.com/home-assistant/core/pull/148136)) ([documentation](https://www.home-assistant.io/integrations/ps4))
Templates
Returning `None` from a template binary sensor’s state template is now interpreted as `unknown` state instead of as `off` state.
If this behavior is not desired, you need to adjust your templates to return `False` explicitly.
([@epenet](https://github.com/epenet) - [#128861](https://github.com/home-assistant/core/pull/128861)) ([documentation](https://www.home-assistant.io/integrations/template))
Tuya
The battery property on vacuum entities is being removed in Home Assistant. Therefore, this property is now removed from this integration and is replaced by a battery level sensor.
Please review your automations, scripts or cards using the battery property and update the code to use the battery sensor instead.
([@epenet](https://github.com/epenet) - [#150086](https://github.com/home-assistant/core/pull/150086)) ([documentation](https://www.home-assistant.io/integrations/tuya))
UniFi Protect
Support for UniFi Protect installations running on versions below 6.0.0 has been removed.
This change is necessary as we are migrating the Home Assistant integration to use the new UniFi Protect Public API, which is only available in current versions.
If you are running an older version of UniFi Protect, you will need to upgrade to at least version 6.0.0 in order to continue using this integration.
You can read more about the 6.0 release in Ubiquiti’s official blog post: 🔗 [Introducing Protect 6.0](https://blog.ui.com/article/introducing-protect-6-0)
Note on future updates: The Public API is still under active development and may change over time. As we continue to migrate more features of the integration to use the Public API, it is likely that the minimum required version of UniFi Protect will increase further in upcoming Home Assistant releases. We will make these changes step by step as the API evolves and new capabilities become available.
**What do I need to do?**
Upgrade your UniFi Protect installation to version 6.0.0 or later.
Be prepared for possible further minimum version increases in the future.
If you are already using version 6.0.0 or newer, and the user in use has sufficient permissions, the integration will attempt to automatically create a new API key. If this succeeds, no further action is required. If it fails, a reauthentication will be triggered, requiring you to re-enter your password and provide your API key manually.
([@RaHehl](https://github.com/RaHehl) - [#149126](https://github.com/home-assistant/core/pull/149126)) ([documentation](https://www.home-assistant.io/integrations/unifiprotect))
Whirlpool Appliances
The door state for washer/dryer machines is now reported as a binary sensor instead of being part of the main machine state sensor, which now reports only the cycle states. Users relying on this state in automations or scripts will need to update their configurations to use the new binary sensor.
([@abmantis](https://github.com/abmantis) - [#144078](https://github.com/home-assistant/core/pull/144078)) ([documentation](https://www.home-assistant.io/integrations/whirlpool))
Z-Wave
With this release, you will need to update your zwave-js-server instance. You must use zwave-js-server 3.2.1 or greater (schema 44).
  * If you use the Z-Wave JS add-on, you need at least version 0.20.0.
  * If you use the Z-Wave JS UI add-on, you need at least version [4.8.0](https://github.com/hassio-addons/addon-zwave-js-ui/releases/tag/v4.8.0).
  * If you use the Z-Wave JS UI Docker container, you need at least version [10.11.0](https://github.com/zwave-js/zwave-js-ui/releases/tag/v10.11.0).
  * If you run your own Docker container or some other installation method, you will need to update your zwave-js-server instance to at least 3.2.1.


([@MartinHjelmare](https://github.com/MartinHjelmare) - [#149616](https://github.com/home-assistant/core/pull/149616)) ([documentation](https://www.home-assistant.io/integrations/zwave_js))
If you are a custom integration developer and want to learn about changes and new features available for your integration: Be sure to follow our [developer blog](https://developers.home-assistant.io/blog/). The following changes are the most notable for this release:
  * [Handling open file limit in add-ons since OS 16](https://developers.home-assistant.io/blog/2025/07/14/home-assistant-os-16-open-file-limit/)
  * [The media player STANDBY state is deprecated](https://developers.home-assistant.io/blog/2025/07/16/media-player-standby-state-deprecated)
  * [The result attribute has been removed from the FlowResult typed dict](https://developers.home-assistant.io/blog/2025/07/31/result-removed-from-flowresult/)
  * [Updated guidelines for helper integrations linking to other integration’s device](https://developers.home-assistant.io/blog/2025/07/18/updated-pattern-for-helpers-linking-to-devices)
  * [Vacuum battery properties are deprecated](https://developers.home-assistant.io/blog/2025/07/02/vacuum-battery-properties-deprecated/)


## All changes 
Of course, there is a lot more in this release. You can find a list of all changes made here: [Full changelog for Home Assistant Core 2025.8](https://www.home-assistant.io/changelogs/core-2025.8)
Back to top
