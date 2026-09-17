---
url: "https://www.home-assistant.io/blog/2025/11/05/release-202511/"
title: "2025.11: Pick, automate, and a slice of pie 🥧 - Home Assistant"
scraped_at: 2026-09-17T16:41:13+00:00
---

Home Assistant 2025.11! 🎉
November is here, and we’ve been hard at work refining some of the main experiences that you interact with every day, and I think you’re going to love what we’ve built.
My personal favorite this release? The brand new target picker. 🎯
It’s one of those changes that seems simple on the surface, but makes such a huge difference in how you build automations. You can finally see exactly what you’re targeting, with full context about which device an entity belongs to and which area it’s in. No more guessing whether you’re controlling the right ceiling light when you have three of them!
But that’s just the beginning. We’re continuing with the automation editor improvements, this time with a completely redesigned dialog for adding triggers, conditions, and actions. It’s cleaner, easier to read, and sets the foundation for some really exciting stuff coming in future releases. 🤫
And speaking of making things clearer, you can now control exactly how entity names appear on your dashboard cards. Want to show just the entity name? The device name? The area? Or combine them? Even if you rename things, your dashboards will stay perfectly in sync. No more manual updates needed!
Oh, and energy dashboard fans will appreciate the new pie chart view for device energy, complete with totals displayed in the corner of every energy card. 🥧
Enjoy the release!
../Frenck
PS: Oh, and pssst… Don’t tell anyone 🤫, but there might be something exciting being released on November 19th. [Hit the bell on this announced YouTube stream to not miss it](https://www.youtube.com/watch?v=HSRvso6cbf0). Stay tuned! 😀
  * [A brand new target picker](https://www.home-assistant.io/blog/2025/11/05/release-202511/#a-brand-new-target-picker)
  * [A brand new way to add triggers, conditions, and actions in your automations](https://www.home-assistant.io/blog/2025/11/05/release-202511/#a-brand-new-way-to-add-triggers-conditions-and-actions-in-your-automations)
  * [Naming entities on your dashboard](https://www.home-assistant.io/blog/2025/11/05/release-202511/#naming-entities-on-your-dashboard)
  * [Progress for Home Assistant and Add-on updates](https://www.home-assistant.io/blog/2025/11/05/release-202511/#progress-for-home-assistant-and-add-on-updates)
  * [Integrations](https://www.home-assistant.io/blog/2025/11/05/release-202511/#integrations)
    * [New integrations](https://www.home-assistant.io/blog/2025/11/05/release-202511/#new-integrations)
    * [Noteworthy improvements to existing integrations](https://www.home-assistant.io/blog/2025/11/05/release-202511/#noteworthy-improvements-to-existing-integrations)
    * [Now available to set up from the UI](https://www.home-assistant.io/blog/2025/11/05/release-202511/#now-available-to-set-up-from-the-ui)
    * [Integration quality scale achievements](https://www.home-assistant.io/blog/2025/11/05/release-202511/#integration-quality-scale-achievements)
    * [Farewell to the following](https://www.home-assistant.io/blog/2025/11/05/release-202511/#farewell-to-the-following)
  * [Other noteworthy changes](https://www.home-assistant.io/blog/2025/11/05/release-202511/#other-noteworthy-changes)
    * [Improved logging efficiency](https://www.home-assistant.io/blog/2025/11/05/release-202511/#improved-logging-efficiency)
    * [The new Home Dashboard keeps getting smarter](https://www.home-assistant.io/blog/2025/11/05/release-202511/#the-new-home-dashboard-keeps-getting-smarter)
  * [Patch releases](https://www.home-assistant.io/blog/2025/11/05/release-202511/#patch-releases)
    * [2025.11.1 - November 7](https://www.home-assistant.io/blog/2025/11/05/release-202511/#2025111---november-7)
    * [2025.11.2 - November 14](https://www.home-assistant.io/blog/2025/11/05/release-202511/#2025112---november-14)
    * [2025.11.3 - November 21](https://www.home-assistant.io/blog/2025/11/05/release-202511/#2025113---november-21)
  * [Need help? Join the community](https://www.home-assistant.io/blog/2025/11/05/release-202511/#need-help-join-the-community)
  * [Backward-incompatible changes](https://www.home-assistant.io/blog/2025/11/05/release-202511/#backward-incompatible-changes)


_A huge thank you to all the contributors who made this release possible! And a special shout-out to[@bramkragten](https://github.com/bramkragten), [@JLo](https://github.com/jlpouffier), [@MindFreeze](https://github.com/MindFreeze), [@agners](https://github.com/agners), and [@piitaya](https://github.com/piitaya) who helped write the release notes this release. Also, [@silamon](https://github.com/silamon) and [@GemPolisher](https://github.com/GemPolisher) for putting effort into tweaking its contents. Thanks to them, these release notes are in great shape. ❤️_
## A brand new target picker 
Have you ever been building an automation and wondered, “Wait, which ceiling light is this?” when you see three entities all named “Ceiling light”? Or tried to figure out how many lights you’re actually controlling when you target an entire floor or area?
We’ve all been there. Until now, the target picker didn’t show you the full picture. You couldn’t see which device an entity belonged to or which area it was assigned to. And when you selected a floor or area as your target, you had no idea how many entities you were actually affecting. This uncertainty meant many of you stuck with targeting individual entities, even though larger targets (like areas and floors) can make your automations much more flexible.
The new target picker changes all that. Now you get full context for everything you’re targeting, and you can see exactly how many entities will be affected by your action.
Want to dig deeper? You can expand any floor, area, or device to see exactly which entities are included and where they’re coming from.
This makes it so much easier to build automations that scale with your home. When you target an area or floor, your automation automatically adapts as you add or remove devices. No more updating your automations every time you add a new light or sensor. Your automations just work, which is exactly how it should be.
## A brand new way to add triggers, conditions, and actions in your automations 
It’s no secret that we’re currently working hard on making automations easier to create. After the release of the automation sidebar [two releases ago](https://www.home-assistant.io/blog/2025/09/03/release-20259/#automation-editor-sidebar), we are now introducing a new dialog to add triggers, conditions, and actions.
The changes are purely cosmetic: the dialog is bigger, so the description of each block is simpler to read, with a two-pane layout to ease both navigation and block selection.
The building blocks (which are used to perform more complex conditions or sequences of actions, such as repeating actions or branching out your sequence into multiple paths) have been moved into the main dialog on a second tab. There is now a single entry point to add something to an automation instead of two, greatly reducing the number of buttons in complex automations.
As mentioned above, these changes are purely cosmetic, for now! But this new dialog is the foundation of what’s coming next, and we cannot wait to present that to you once it finally lands.
## Naming entities on your dashboard 
A few releases ago, we gave the entity picker a big upgrade by adding more context so you could easily see where each entity belongs ([May 2025 release](https://www.home-assistant.io/blog/2025/05/07/release-20255/#picking-entities)). In this release, we’re bringing that same flexibility to your dashboards.
You can now choose how names appear on your cards: show the entity, device, area, floor, or even combine them. This gives you full control over how your dashboards look and feel. For example, in a dedicated section for a specific device, you might choose to display only the entity name to avoid repeating the device name on every card.
Of course, you can still set a custom name if you want complete control over the text shown.
And the best part? If you rename an entity or device, your dashboards will automatically stay in sync. No more manual edits needed; everything just updates itself.
## Energy pie 
We’ve added a new layout to the devices energy graph: “pie” 🥧. You can toggle between the regular bar chart and the new pie chart by clicking the icon in the top-right corner.
Doing this made the top-right corner of the other energy cards feel empty, so we used that space to display the total energy for the selected period. For example, if the date picker is set to today, the total solar energy for today will be displayed in the corner of the solar production graph card.
## Progress for Home Assistant and Add-on updates 
With this release, you can now track the progress of updates to Home Assistant and Add-ons (managed by the Supervisor)! The progress includes the stages of downloading and unpacking, so the time required will vary based on your internet speed, CPU performance, and system load. As a result, the progress is not reflected as perfectly linear, but it does still provide a good estimate of how far along the update is.
## Integrations 
Thanks to our community for keeping pace with the new integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) and improvements to existing ones! You’re all awesome. 🥰
### New integrations 
We welcome the following new integrations in this release:
  * , added by [@kclif9](https://github.com/kclif9) The Actron Air integration allows you to control Actron Air air conditioning controllers in Home Assistant.
  * , added by [@niracler](https://github.com/niracler) Integrate with [Sunricher DALI](https://www.home-assistant.io/integrations/sunricher_dali), a platform for managing and monitoring DALI-based lighting systems.
  * , added by [@Lorenzo-Gasparini](https://github.com/Lorenzo-Gasparini) The [Fing](https://www.home-assistant.io/integrations/fing) integration provides network scanning, device detection, and presence monitoring capabilities using the Fing platform.
  * , added by [@erwindouna](https://github.com/erwindouna) Integrate with the [Firefly III project](https://www.firefly-iii.org/), a free open source personal finance manager with full transaction management, budgets, categories, and reports.
  * , added by [@epdevlab](https://github.com/epdevlab) Integrate with the [iNELS](https://www.home-assistant.io/integrations/inels) smart home system to manage lighting, heating, and automation components for enhanced home control.
  * **[Lunatone Gateway](https://www.home-assistant.io/integrations/lunatone)** , added by [@MoonDevLT](https://github.com/MoonDevLT) Integrate with [Lunatone Gateway](https://www.home-assistant.io/integrations/lunatone), enabling control and monitoring of DALI lighting systems through Lunatone’s DALI gateway interface.
  * , added by [@xE1H](https://github.com/xE1H) The Meteo.lt integration uses meteorological data from the [Lithuanian Hydrometeorological Service](https://www.meteo.lt/en/) (LHMT) to provide regional weather forecasts for locations in Lithuania.
  * **[Nintendo Parental Controls](https://www.home-assistant.io/integrations/nintendo_parental_controls)** , added by [@pantherale0](https://github.com/pantherale0) The [Nintendo Parental Controls](https://www.home-assistant.io/integrations/nintendo_parental_controls) integration connects with Nintendo’s parental management service, allowing you to monitor and manage device usage and restrictions.
  * , added by [@felipecrs](https://github.com/felipecrs) The [OpenRGB](https://www.home-assistant.io/integrations/openrgb) integration allows unified control of RGB lighting across various hardware brands and devices through the OpenRGB project.


### Noteworthy improvements to existing integrations 
It’s not just new integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) that have been added; existing integrations are also being constantly improved. Here are some of the noteworthy changes:
  * The [SwitchBot](https://www.home-assistant.io/integrations/switchbot) integration now supports garage door openers. Thanks [@zerzhang](https://github.com/zerzhang)!
  * [@tr4nt0r](https://github.com/tr4nt0r) added support for notifications to the [Habitica](https://www.home-assistant.io/integrations/habitica) integration. Nice work!
  * The [VegeHub](https://www.home-assistant.io/integrations/vegehub) integration now has support for switches to control actuators. Cool [@Thulrus](https://github.com/Thulrus)!
  * The [Portainer](https://www.home-assistant.io/integrations/portainer) integration gained support for switches, buttons, and sensors, so you can control and monitor all your containers! Well done [@erwindouna](https://github.com/erwindouna)!
  * The [Volvo](https://www.home-assistant.io/integrations/volvo) integration can now show the location of your car and has buttons to control it. We got [@thomasddn](https://github.com/thomasddn) to thank for that!
  * [ElevenLabs](https://www.home-assistant.io/integrations/elevenlabs) can now be used for speech-to-text. Thanks [@ehendrix23](https://github.com/ehendrix23)!
  * You can now control the LEDs of supported [UniFi](https://www.home-assistant.io/integrations/unifi) network devices! Thanks [@Sese-Schneider](https://github.com/Sese-Schneider)!
  * [@barneyonline](https://github.com/barneyonline) added binary sensors to the [Yardian](https://www.home-assistant.io/integrations/yardian) integration. Nice!
  * You can now set the temperature of your 3D printer’s tool and bed with the [OctoPrint](https://www.home-assistant.io/integrations/octoprint) integration. Thanks [@AmadeusW](https://github.com/AmadeusW)!
  * The [Niko Home Control](https://www.home-assistant.io/integrations/niko_home_control) integration now also adds your scenes into Home Assistant! Thanks [@VandeurenGlenn](https://github.com/VandeurenGlenn)!
  * Your [Control4](https://www.home-assistant.io/integrations/control4) climate devices (for example, thermostats) are now supported in Home Assistant. Thanks [@davidrecordon](https://github.com/davidrecordon)!
  * Support for controlling [Growatt](https://www.home-assistant.io/integrations/growatt_server) MIN/TLX inverters was added, and you can now enable grid charge! Thanks [@johanzander](https://github.com/johanzander)!
  * [@hanwg](https://github.com/hanwg) added event entities to the [Telegram](https://www.home-assistant.io/integrations/telegram_bot) bot integration. You can use these entities to more easily automate when you get a message, for example! Cool!
  * The [Xbox](https://www.home-assistant.io/integrations/xbox) integration now has support for images! It shows an image of the game you are currently playing, the avatar, and the Gamerpic for yourself and your friends. Thanks [@tr4nt0r](https://github.com/tr4nt0r)!
  * [@AndyTempel](https://github.com/AndyTempel) added support for solar production forecasting to [Victron Remote Monitoring](https://www.home-assistant.io/integrations/victron_remote_monitoring), so you can now use it in the energy dashboard to see a forecast of how much solar energy you will produce today!
  * The [Shelly](https://www.home-assistant.io/integrations/shelly) integration now supports climate and valve entities. Thanks [@thecode](https://github.com/thecode)!
  * [@starkillerOG](https://github.com/starkillerOG) improved the [Reolink](https://www.home-assistant.io/integrations/reolink) integration; it can now report bicycles and the type of person, vehicle, and animal. So you now know if a man or a woman is detected on your cameras. Great work!


### Now available to set up from the UI 
While most integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) can be set up directly from the Home Assistant user interface, some were only available using a YAML configuration. We keep moving more integrations to the UI, making them more accessible for everyone to set up and use.
The following integration is now available via the Home Assistant UI:
  * **[London Underground](https://www.home-assistant.io/integrations/london_underground)** by [@HarvsG](https://github.com/HarvsG)


### Integration quality scale achievements 
One thing we are incredibly proud of in Home Assistant is our [integration quality scale](https://www.home-assistant.io/docs/quality_scale/). This scale helps us and our contributors to ensure integrations are of high quality, maintainable, and provide the best possible user experience.
This release, we celebrate several integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) that have improved their quality scale:
  * **Seven integrations reached platinum** 🏆
    * [APC UPS Daemon](https://www.home-assistant.io/integrations/apcupsd), thanks to [@yuxincs](https://github.com/yuxincs)
    * [IMGW-PIB](https://www.home-assistant.io/integrations/imgw_pib), thanks to [@bieniu](https://github.com/bieniu)
    * [LG WebOS TV](https://www.home-assistant.io/integrations/webostv), thanks to [@thecode](https://github.com/thecode)
    * [Mealie](https://www.home-assistant.io/integrations/mealie), thanks to [@andrew-codechimp](https://github.com/andrew-codechimp)
    * [NextDNS](https://www.home-assistant.io/integrations/nextdns), thanks to [@bieniu](https://github.com/bieniu)
    * [ntfy](https://www.home-assistant.io/integrations/ntfy), thanks to [@tr4nt0r](https://github.com/tr4nt0r)
    * [Volvo](https://www.home-assistant.io/integrations/volvo), thanks to [@thomasddn](https://github.com/thomasddn)
  * **Four integrations reached silver** 🥈
    * [1-wire](https://www.home-assistant.io/integrations/onewire), thanks to [@epenet](https://github.com/epenet)
    * [Ubiquiti airOS](https://www.home-assistant.io/integrations/airos), thanks to [@CoMPaTech](https://github.com/CoMPaTech)
    * [LetPot](https://www.home-assistant.io/integrations/letpot), thanks to [@jpelgrom](https://github.com/jpelgrom)
    * [Switcher](https://www.home-assistant.io/integrations/switcher_kis), thanks to [@thecode](https://github.com/thecode)


This is a huge achievement for these integrations and their maintainers. The effort and dedication required to reach these quality levels is significant, as it involves extensive testing, documentation, error handling, and often complete rewrites of parts of the integration.
A big thank you to all the contributors involved! 👏
### Farewell to the following 
The following integrationsIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) are no longer available as of this release:
  * **Vultr** has been removed. The integration has not been working since the API v1 that it used was taken offline in September 2023.
  * **IBM Watson IoT Platform** has been removed. On September 8, 2020, IBM announced the withdrawal of its support for the IBM Watson IoT Platform and successively discontinued all versions until September 30, 2022.
  * **Plum Lightpad** has been removed. Their servers have been shut down, which made the integration non-functional.


## Other noteworthy changes 
There are many more improvements in this release; here are some of the other noteworthy changes:
  * [@thecode](https://github.com/thecode) added [group](https://www.home-assistant.io/integrations/group) support for valves, so you can group multiple valves into one.
  * Searching in data tables got a lot better; you can now search over multiple columns at once. Thanks [@wendevlin](https://github.com/wendevlin)!
  * Energy graphs now show the total of the period in the top-right corner. Great addition, [@MindFreeze](https://github.com/MindFreeze)!
  * Thanks to [@karwosts](https://github.com/karwosts), you can now use images from any integration providing images for your dashboard background.


### Improved logging efficiency 
If you’re using the Home Assistant Operating System, we have some great news for you! We’ve made our logging system way more efficient. 🚀
You might not realize it, but all those Home Assistant logs you can find in **Settings** > **System** > **Logs** were actually being stored on your disk twice. 🙈
Home Assistant OS keeps all logs for everything, including Home Assistant itself, in a very efficient way, even across restarts! But on top of that, we were also writing them to a log file in your Home Assistant configuration folder.
That’s not ideal. It takes twice the disk space, but more importantly, it causes unnecessary wear on your storage medium, which means it will fail sooner. This is especially concerning if you’re using an SD card in, for example, a Raspberry Pi.
As of this release, we’ve stopped writing logs to the configuration folder. You can still view and download all logs from the Home Assistant settings page, just like before. We’ve adapted that page to read the logs from the OS directly instead.
Tip
Are you more into the command line? No worries, our Home Assistant CLI has you covered. Check it out by running `ha core logs --help` for more information.
### The new Home Dashboard keeps getting smarter 
Following the improvements introduced in the latest releases, this release makes the experience even smoother and more intuitive.
We’ve simplified and reorganized things:
  * Suggested entities and favorites are now combined into a single, smart section, showing you what’s most relevant in one place.
  * Areas are now grouped by floor, making it easier to browse and understand your home’s layout at a glance.
  * The Lights, Climate, and Security views have been moved to their own dedicated dashboards, so you can access them directly under **Settings** > **Dashboards**. These dashboards now also include devices that aren’t assigned to any specific area, ensuring nothing is overlooked.


These improvements bring everything together more naturally, helping your Home Dashboard feel less like a setup and more like a true reflection of your home.
## Patch releases 
We will also release patch releases for Home Assistant 2025.11 in November. These patch releases only contain bug fixes. Our goal is to release a patch release once a week, aiming for Friday.
### 2025.11.1 - November 7 
  * Improve scan interval for Airthings Corentium Home 2 ([@LaStrada](https://github.com/LaStrada) - [#155694](https://github.com/home-assistant/core/pull/155694))
  * Remove `@progress_step` decorator from ZHA and Hardware integration ([@puddly](https://github.com/puddly) - [#155867](https://github.com/home-assistant/core/pull/155867))
  * Fix KNX Climate humidity DPT ([@farmio](https://github.com/farmio) - [#155942](https://github.com/home-assistant/core/pull/155942))
  * Truncate password before sending it to bcrypt ([@cdce8p](https://github.com/cdce8p) - [#155950](https://github.com/home-assistant/core/pull/155950))
  * Fix for corrupt restored state in miele consumption sensors ([@astrandb](https://github.com/astrandb) - [#155966](https://github.com/home-assistant/core/pull/155966))
  * Handle empty fields in SolarEdge config flow ([@tronikos](https://github.com/tronikos) - [#155978](https://github.com/home-assistant/core/pull/155978))
  * Fix SolarEdge unload failing when there are no sensors ([@tronikos](https://github.com/tronikos) - [#155979](https://github.com/home-assistant/core/pull/155979))
  * Bump aioamazondevices to 8.0.1 ([@chemelli74](https://github.com/chemelli74) - [#155989](https://github.com/home-assistant/core/pull/155989))
  * Fix Growatt integration authentication error for legacy config entries ([@johanzander](https://github.com/johanzander) - [#155993](https://github.com/home-assistant/core/pull/155993))
  * Bump tuya-device-sharing-sdk to 0.2.5 ([@epenet](https://github.com/epenet) - [#156014](https://github.com/home-assistant/core/pull/156014))
  * Bump onedrive-personal-sdk to 0.0.16 ([@zweckj](https://github.com/zweckj) - [#156021](https://github.com/home-assistant/core/pull/156021))
  * Fix the exception caused by the missing Foscam integration key ([@Foscam-wangzhengyu](https://github.com/Foscam-wangzhengyu) - [#156022](https://github.com/home-assistant/core/pull/156022))
  * Bump intents to 2025.11.7 ([@synesthesiam](https://github.com/synesthesiam) - [#156063](https://github.com/home-assistant/core/pull/156063))


### 2025.11.2 - November 14 
  * Bump cronsim to 2.7 ([@dgomes](https://github.com/dgomes) - [#155648](https://github.com/home-assistant/core/pull/155648))
  * Avoid firing discovery events when flows immediately create a config entry ([@puddly](https://github.com/puddly) - [#155753](https://github.com/home-assistant/core/pull/155753))
  * Remove arbitrary forecast limit for meteo_lt ([@xE1H](https://github.com/xE1H) - [#155877](https://github.com/home-assistant/core/pull/155877))
  * Fix progress step bugs ([@emontnemery](https://github.com/emontnemery) - [#155923](https://github.com/home-assistant/core/pull/155923))
  * Make sure to clean register callbacks when mobile_app reloads ([@TimoPtr](https://github.com/TimoPtr) - [#156028](https://github.com/home-assistant/core/pull/156028))
  * Bump pyportainer 1.0.13 ([@erwindouna](https://github.com/erwindouna) - [#155783](https://github.com/home-assistant/core/pull/155783))
  * Bump pyportainter 1.0.14 ([@erwindouna](https://github.com/erwindouna) - [#156072](https://github.com/home-assistant/core/pull/156072))
  * Log `HomeAssistantError`s in ZHA config flow ([@TheJulianJES](https://github.com/TheJulianJES) - [#156075](https://github.com/home-assistant/core/pull/156075))
  * Bump aio-ownet to 0.0.5 ([@jrieger](https://github.com/jrieger) - [#156157](https://github.com/home-assistant/core/pull/156157))
  * Fix MFA Notify setup flow schema ([@abmantis](https://github.com/abmantis) - [#156158](https://github.com/home-assistant/core/pull/156158))
  * Update xknx to 3.10.1 ([@farmio](https://github.com/farmio) - [#156177](https://github.com/home-assistant/core/pull/156177))
  * Forbid to choose state in Ukraine Alarm integration ([@PaulAnnekov](https://github.com/PaulAnnekov) - [#156183](https://github.com/home-assistant/core/pull/156183))
  * Fix set_absolute_position angle ([@starkillerOG](https://github.com/starkillerOG) - [#156185](https://github.com/home-assistant/core/pull/156185))
  * Fix config flow reconfigure for Comelit ([@chemelli74](https://github.com/chemelli74) - [#156193](https://github.com/home-assistant/core/pull/156193))
  * Bump pyvesync to 3.2.1 ([@cdnninja](https://github.com/cdnninja) - [#156195](https://github.com/home-assistant/core/pull/156195))
  * Fix Climate state reproduction when target temperature is `None` ([@mib1185](https://github.com/mib1185) - [#156220](https://github.com/home-assistant/core/pull/156220))
  * Foscam Integration with Legacy Model Compatibility ([@Foscam-wangzhengyu](https://github.com/Foscam-wangzhengyu) - [#156226](https://github.com/home-assistant/core/pull/156226))
  * Bump pypalazzetti lib from 0.1.19 to 0.1.20 ([@dotvav](https://github.com/dotvav) - [#156249](https://github.com/home-assistant/core/pull/156249))
  * Bump pySmartThings to 3.3.2 ([@joostlek](https://github.com/joostlek) - [#156250](https://github.com/home-assistant/core/pull/156250))
  * Correct migration to recorder schema 51 ([@emontnemery](https://github.com/emontnemery) - [#156267](https://github.com/home-assistant/core/pull/156267))
  * Improve logging of failing miele action commands ([@astrandb](https://github.com/astrandb) - [#156275](https://github.com/home-assistant/core/pull/156275))
  * Ituran: Don’t cache properties ([@shmuelzon](https://github.com/shmuelzon) - [#156281](https://github.com/home-assistant/core/pull/156281))
  * tplink: handle repeated, unknown thermostat modes gracefully ([@rytilahti](https://github.com/rytilahti) - [#156310](https://github.com/home-assistant/core/pull/156310))
  * Check collation of statistics_meta DB table ([@emontnemery](https://github.com/emontnemery) - [#156327](https://github.com/home-assistant/core/pull/156327))
  * Fix support for Hyperion 2.1.1 ([@antoniocifu](https://github.com/antoniocifu) - [#156343](https://github.com/home-assistant/core/pull/156343))
  * Update pyMill to 0.14.1 ([@Danielhiversen](https://github.com/Danielhiversen) - [#156396](https://github.com/home-assistant/core/pull/156396))
  * Prevent sensor updates caused by fluctuating “last seen” timestamps in Xbox integration ([@tr4nt0r](https://github.com/tr4nt0r) - [#156419](https://github.com/home-assistant/core/pull/156419))
  * Fix update progress in Teslemetry ([@Bre77](https://github.com/Bre77) - [#156422](https://github.com/home-assistant/core/pull/156422))
  * Bump pyvesync to 3.2.2 ([@cdnninja](https://github.com/cdnninja) - [#156423](https://github.com/home-assistant/core/pull/156423))
  * Fix lamarzocco update status ([@zweckj](https://github.com/zweckj) - [#156442](https://github.com/home-assistant/core/pull/156442))
  * Add firmware flashing debug loggers to hardware integrations ([@puddly](https://github.com/puddly) - [#156480](https://github.com/home-assistant/core/pull/156480))
  * URL-encode the RTSP URL in the Foscam integration ([@Foscam-wangzhengyu](https://github.com/Foscam-wangzhengyu) - [#156488](https://github.com/home-assistant/core/pull/156488))
  * Update Home Assistant base image to 2025.11.0 ([@sairon](https://github.com/sairon) - [#156517](https://github.com/home-assistant/core/pull/156517))
  * Bump pySmartThings to 3.3.3 ([@joostlek](https://github.com/joostlek) - [#156528](https://github.com/home-assistant/core/pull/156528))
  * Update bsblan to python-bsblan version 3.1.1 ([@liudger](https://github.com/liudger) - [#156536](https://github.com/home-assistant/core/pull/156536))
  * Bump reolink-aio to 0.16.5 ([@starkillerOG](https://github.com/starkillerOG) - [#156553](https://github.com/home-assistant/core/pull/156553))
  * Bump python-open-router to 0.3.3 ([@joostlek](https://github.com/joostlek) - [#156563](https://github.com/home-assistant/core/pull/156563))
  * Bump ZHA to 0.0.78 ([@TheJulianJES](https://github.com/TheJulianJES) - [#155937](https://github.com/home-assistant/core/pull/155937))
  * Bump ZHA to 0.0.79 ([@TheJulianJES](https://github.com/TheJulianJES) - [#156571](https://github.com/home-assistant/core/pull/156571))
  * Fix sfr_box entry reload ([@epenet](https://github.com/epenet) - [#156593](https://github.com/home-assistant/core/pull/156593))
  * Fix model_id in Husqvarna Automower ([@Thomas55555](https://github.com/Thomas55555) - [#156608](https://github.com/home-assistant/core/pull/156608))
  * Add debounce to Alexa Devices coordinator ([@chemelli74](https://github.com/chemelli74) - [#156609](https://github.com/home-assistant/core/pull/156609))


### 2025.11.3 - November 21 
  * Cache token info in Wallbox ([@hesselonline](https://github.com/hesselonline) - [#154147](https://github.com/home-assistant/core/pull/154147))
  * Bump version of python_awair to 0.2.5 ([@averybiteydinosaur](https://github.com/averybiteydinosaur) - [#155798](https://github.com/home-assistant/core/pull/155798))
  * Fix args passed to check_config script ([@tmonck](https://github.com/tmonck) - [#155885](https://github.com/home-assistant/core/pull/155885))
  * update methods to non deprecated methods in vesync ([@cdnninja](https://github.com/cdnninja) - [#155887](https://github.com/home-assistant/core/pull/155887))
  * Fix wrong BrowseError module in Kode ([@charrus](https://github.com/charrus) - [#155971](https://github.com/home-assistant/core/pull/155971))
  * Bump universal-silabs-flasher to v0.1.0 ([@puddly](https://github.com/puddly) - [#156291](https://github.com/home-assistant/core/pull/156291))
  * Reset state on error during VOIP announcement ([@jaminh](https://github.com/jaminh) - [#156384](https://github.com/home-assistant/core/pull/156384))
  * Bump pyiCloud to 2.2.0 ([@PaulCavill](https://github.com/PaulCavill) - [#156485](https://github.com/home-assistant/core/pull/156485))
  * Fix is_matching in samsungtv config flow ([@FredrikM97](https://github.com/FredrikM97) - [#156594](https://github.com/home-assistant/core/pull/156594))
  * Bump async-upnp-client to 0.46.0 ([@edenhaus](https://github.com/edenhaus) - [#156622](https://github.com/home-assistant/core/pull/156622))
  * Bump tplink-omada-api to 1.5.3 ([@MarkGodwin](https://github.com/MarkGodwin) - [#156645](https://github.com/home-assistant/core/pull/156645))
  * Fix missing description placeholders in MQTT subentry flow ([@jbouwh](https://github.com/jbouwh) - [#156684](https://github.com/home-assistant/core/pull/156684))
  * Fix missing `temperature_delta` device class translations ([@jbouwh](https://github.com/jbouwh) - [#156685](https://github.com/home-assistant/core/pull/156685))
  * Bump ohmepy and remove advanced_settings_coordinator ([@dan-r](https://github.com/dan-r) - [#156764](https://github.com/home-assistant/core/pull/156764))
  * Fix blocking call in cync ([@epenet](https://github.com/epenet) - [#156782](https://github.com/home-assistant/core/pull/156782))
  * Lamarzocco fix websocket reconnect issue ([@zweckj](https://github.com/zweckj) - [#156786](https://github.com/home-assistant/core/pull/156786))
  * Fix hvv_departures to pass config_entry explicitly to DataUpdateCoordinator ([@Copilot](https://github.com/apps/copilot-swe-agent) - [#156794](https://github.com/home-assistant/core/pull/156794))
  * Bump aioautomower to 2.7.1 ([@Thomas55555](https://github.com/Thomas55555) - [#156826](https://github.com/home-assistant/core/pull/156826))
  * Bump pySmartThings to 3.3.4 ([@joostlek](https://github.com/joostlek) - [#156830](https://github.com/home-assistant/core/pull/156830))
  * Bump universal-silabs-flasher to 0.1.2 ([@puddly](https://github.com/puddly) - [#156849](https://github.com/home-assistant/core/pull/156849))
  * Bump onedrive-personal-sdk to 0.0.17 ([@zweckj](https://github.com/zweckj) - [#156865](https://github.com/home-assistant/core/pull/156865))
  * Bump aiounifi to 88 ([@Sese-Schneider](https://github.com/Sese-Schneider) - [#156867](https://github.com/home-assistant/core/pull/156867))
  * Rework CloudhookURL setup for mobile app ([@TimoPtr](https://github.com/TimoPtr) - [#156940](https://github.com/home-assistant/core/pull/156940))
  * Bump go2rtc to 1.9.12 and go2rtc-client to 0.3.0 ([@edenhaus](https://github.com/edenhaus) - [#156948](https://github.com/home-assistant/core/pull/156948))
  * Update frontend to 20251105.1 ([@bramkragten](https://github.com/bramkragten) - [#156992](https://github.com/home-assistant/core/pull/156992))
  * Throttle Decora wifi updates ([@joostlek](https://github.com/joostlek) - [#156994](https://github.com/home-assistant/core/pull/156994))


## Need help? Join the community 
Home Assistant has a great community of users who are all more than willing to help each other out. So, join us!
Our very active [Discord chat server](https://www.home-assistant.io/join-chat) is an excellent place to be, and don’t forget to join our amazing [forums](https://community.home-assistant.io/).
Found a bug or issue? Please report it in our [issue tracker](https://github.com/home-assistant/core/issues) to get it fixed! Or check [our help page](https://www.home-assistant.io/help) for guidance on more places you can go.
Are you more into email? [Sign up for the Open Home Foundation Newsletter](https://www.home-assistant.io/newsletter) to get the latest on features, things happening in our community, and other projects that support the Open Home straight into your inbox.
## Backward-incompatible changes 
We do our best to avoid making changes to existing functionality that might unexpectedly impact your Home Assistant installation. Unfortunately, sometimes, it is inevitable.
We always make sure to document these changes to make the transition as easy as possible for you. This release has the following backward-incompatible changes:
Set assumed state to group if at least one child has assumed state
Previously, the group’s assumed state was always false, regardless of the state of its child entities.
This has now changed:
The group will now have an assumed state of `true` if at least one child entity has an assumed state. This makes the group’s assumed state reflect the uncertainty of its children more accurately. These domains have been added: switch, fan, light, and cover.
([@piitaya](https://github.com/piitaya) - [#154163](https://github.com/home-assistant/core/pull/154163)) ([group docs](https://www.home-assistant.io/integrations/group/))
Asuswrt
The `last_time_reachable` attribute has been removed from the `asuswrt` device tracker. Use the `last_changed` attribute instead in your automations.
([@ollo69](https://github.com/ollo69) - [#154219](https://github.com/home-assistant/core/pull/154219)) ([asuswrt docs](https://www.home-assistant.io/integrations/asuswrt/))
LG webOS TV
The state of LG webOS TV media player entities that do not have an automation trigger to turn on the device will be set to `unavailable` instead of `off`.
([@thecode](https://github.com/thecode) - [#155164](https://github.com/home-assistant/core/pull/155164)) ([webostv docs](https://www.home-assistant.io/integrations/webostv/))
Mealie
The `mealie` integration now requires Mealie version 2 or later.
Mealie version 1 is no longer supported. Version 2 was released in October 2024, so over a year ago. Given the differences between versions 1 and 2, we are no longer able to support or test backward compatibility with version 1.
([@andrew-codechimp](https://github.com/andrew-codechimp) - [#153203](https://github.com/home-assistant/core/pull/153203)) ([mealie docs](https://www.home-assistant.io/integrations/mealie/))
Motion Blinds
The tilt position of `motion_blinds` devices has been corrected to align with the Home Assistant standards. The new tilt position will be: 0 = closed/covering the window opening, 100 = open/letting light through. The previous tilt position can be converted to the new tilt position as follows:
  * `new` = `100 - old`
  * `current_tilt_position` = `100 -> 0`
  * `current_tilt_position` = `75 -> 25`
  * `current_tilt_position` = `50 -> 50`
  * `current_tilt_position` = `25 -> 75`
  * `current_tilt_position` = `0 -> 100`
  * `open_cover_tilt` -> `close_cover_tilt`
  * `close_cover_tilt` -> `open_cover_tilt`


Any automations concerning Motion Blinds devices that use the `current_tilt_position` attribute or use tilt open/close will need to be adjusted.
([@starkillerOG](https://github.com/starkillerOG) - [#149777](https://github.com/home-assistant/core/pull/149777)) ([motion_blinds docs](https://www.home-assistant.io/integrations/motion_blinds/))
Mobile app
The `mobile_app` integration, which supports the iPhone and Android companion apps, now handles zone-only updates better. When your companion app sends just the zone name (not the exact coordinates), the device tracker will show the zone’s friendly name.
The `person` entity now shows the zone’s friendly name (not its object ID) for custom zones. This might break existing automations that trigger on a person’s state.
As an example, if you have a zone named `zone.kids_school` with the friendly name `School`:
  * **Before** this change, the state of the corresponding `person` and `device_tracker` entities would be `kids_school` when the “Location Sent” in the companion app was set to send “Zone Name Only” and `School` when it was set to “Exact”.
  * **After** this change, the state of the corresponding `person` and `device_tracker` entities will be `School` for both the “Location Sent” settings in the companion app.


([@Ashus](https://github.com/Ashus) - [#149453](https://github.com/home-assistant/core/pull/149453)) ([mobile_app docs](https://www.home-assistant.io/integrations/mobile_app/))
Nederlandse Spoorwegen
The Nederlandse Spoorwegen entity is now displayed as a timestamp entity, rather than a string. Please adapt your automations and scripts.
([@joostlek](https://github.com/joostlek) - [#154011](https://github.com/home-assistant/core/pull/154011)) ([nederlandse_spoorwegen docs](https://www.home-assistant.io/integrations/nederlandse_spoorwegen/))
ONVIF
The `Speed` parameter in the ONVIF `GoToPreset` action is now optional.
The default of `0.5` is no longer set. If you want to restore the previous behavior you have to set `speed` to `0.5` in your action.
([@carlos-sarmiento](https://github.com/carlos-sarmiento) - [#149636](https://github.com/home-assistant/core/pull/149636)) ([onvif docs](https://www.home-assistant.io/integrations/onvif/))
OralB
In the OralB integration, states and attributes have changed.
In multiple places, spaces have been replaced with underscores:
  * Toothbrush state:
    * `flight menu` → `flight_menu`
    * `selection menu` → `selection_menu`
    * `final test` → `final_test`
    * `pcb test` → `pcb_test`
  * Brushing mode:
    * `daily clean` → `daily_clean`
    * `gum care` → `gum_care`
    * `tongue cleaning` → `tongue_cleaning`
    * `super sensitive` → `super_sensitive`
    * `deep clean` → `deep_clean`
  * Pressure:
    * `power button pressed` → `power_button_pressed`
    * `button pressed` → `button_pressed`
  * Sector:
    * `no sector` → `no_sector`
    * `sector 1` → `sector_1`
    * `sector 2` → `sector_2`
    * `sector 3` → `sector_3`
    * `sector 4` → `sector_4`


Automations should be updated to use the new states and attributes.
([@tr4nt0r](https://github.com/tr4nt0r) - [#153605](https://github.com/home-assistant/core/pull/153605)) ([oralb docs](https://www.home-assistant.io/integrations/oralb/))
Renault
The discovery of Renault functionality was previously based on assumptions that may have created invalid and non-functional entities. These will no longer be created.
([@epenet](https://github.com/epenet) - [#154137](https://github.com/home-assistant/core/pull/154137)) ([renault docs](https://www.home-assistant.io/integrations/renault/))
Traccar Server
The Traccar integration has been updated to use a more secure API Token for authentication. This is a required, one-time breaking change to align with Traccar’s security recommendations and ensure the integration continues to work.
This release migrates the integration away from the older username/password method, ensuring continued stability and security for all users while also allowing users with SSO-based setups to use the integration.
When you update Home Assistant, the existing Traccar integration will need to be re-authenticated:
  1. Generate an API Token on your Traccar server (you’ll find this option in your Traccar server’s user settings).
  2. Go to **Settings** > **Devices & services** > **Traccar Server**.
  3. Click “Reconfigure” and enter your new API Token when prompted.


Once you’ve done this, your Traccar devices and entities will work exactly as they did before.
([@pantherale0](https://github.com/pantherale0) - [#155297](https://github.com/home-assistant/core/pull/155297)) ([traccar_server docs](https://www.home-assistant.io/integrations/traccar_server/))
Xbox
The `Account tier` and `Gold tenure` sensors have been retired, as they no longer receive updates following the transition from Xbox Live Gold to Xbox Game Pass. Additionally, the `In party` and `In multiplayer` binary sensors have been removed, since they’ve been non-functional for quite some time.
([@tr4nt0r](https://github.com/tr4nt0r) - [#154891](https://github.com/home-assistant/core/pull/154891)) ([xbox docs](https://www.home-assistant.io/integrations/xbox/))
If you are a custom integration developer and want to learn about changes and new features available for your integration, be sure to follow our [developer blog](https://developers.home-assistant.io/blog/). The following changes are the most notable for this release:
  * [Changes to the recorder statistics API](https://developers.home-assistant.io/blog/2025/10/16/recorder-statistics-api-changes)
  * [Device filter has been removed from target selector](https://developers.home-assistant.io/blog/2025/10/14/device-filter-removed-from-target-selector)
  * [Service translations removed from WebSocket get_services and REST /api/services](https://developers.home-assistant.io/blog/2025/10/24/service-web-api-changes)
  * [TemperatureConverter.convert_interval deprecation](https://developers.home-assistant.io/blog/2025/11/04/convert-interval-deprecation/)
  * [Update coordinator now allows retriggering](https://developers.home-assistant.io/blog/2025/10/05/coordinator-retrigger)


## All changes 
Of course, there is a lot more in this release. You can find a list of all changes here: [Full changelog for Home Assistant Core 2025.11](https://www.home-assistant.io/changelogs/core-2025.11)
Back to top
