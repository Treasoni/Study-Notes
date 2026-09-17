---
url: "https://www.home-assistant.io/docs/scripts/service-calls/"
title: "Performing actions - Home Assistant"
scraped_at: 2026-09-17T16:39:34+00:00
---

Various integrations allow performing actionsActions are used in several places in Home Assistant. As part of a script or automation, actions define what is going to happen once a trigger is activated. In scripts, an action is called _sequence_.[ [Learn more]](https://www.home-assistant.io/docs/automation/action/) when a certain event occurs. The most common one is performing an action when an automation triggerA trigger is a set of values or conditions of a platform that are defined to cause an automation to run.[ [Learn more]](https://www.home-assistant.io/docs/automation/trigger/) happens. But an action can also be called from a scriptScripts are components that allow you to specify a sequence of actions to be executed by Home Assistant when turned on.[ [Learn more]](https://www.home-assistant.io/docs/scripts/), a dashboard, or via voice command devices such as Amazon Echo.
The configuration options to perform action are the same between all integrations and are described on this page.
Examples on this page will be given as part of an automation integration configuration but different approaches can be used for other integrations too.
Tip
Use the **Actions** tab under [**Settings** > **Tools** > **Actions**](https://my.home-assistant.io/redirect/developer_services) to discover available actions.
### The basics 
Perform the action `homeassistant.turn_on` on the entityAn entity represents a sensor, actor, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. An entity is usually part of a device or a service.[ [Learn more]](https://www.home-assistant.io/docs/configuration/entities_domains/) `light.living_room`, which is a [light group](https://www.home-assistant.io/integrations/group/). This turns on every light that is a member of the group. You can also use `entity_id: all` and it will turn on all possible entities.

```
action: homeassistant.turn_on
target:
  entity_id: light.living_room
```

YAML
Copy
### Targeting areas and devices 
Instead of targeting an entity, you can also target an areaAn area in Home Assistant is a [logical grouping](https://www.home-assistant.io/docs/organizing/) of devices and entities that represents a room or space in your home, such as the living room, kitchen, or garage.[ [Learn more]](https://www.home-assistant.io/docs/organizing/areas/) or deviceA device is a model representing a physical or logical unit that contains entities.. Or a combination of these. This is done with the `target` key.
A `target` is a map that contains at least one of the following: `area_id`, `device_id`, `entity_id`. Each of these can be a list. The values should be lower-cased.
The following example uses a single action to turn on the lights in the living room area, 2 additional light devices and 2 additional light entities:

```
action: light.turn_on
target:
  area_id: living_room
  device_id:
    - ff22a1889a6149c5ab6327a8236ae704
    - 52c050ca1a744e238ad94d170651f96b
  entity_id:
    - light.hallway
    - light.landing
```

YAML
Copy
### Passing data to the action 
You can also specify other parameters beside the entity to target. For example, the `light.turn_on` action allows specifying the brightness.

```
action: light.turn_on
target:
  entity_id: light.living_room
data:
  brightness: 120
  rgb_color: [255, 0, 0]
```

YAML
Copy
A full list of the parameters for an action can be found on the documentation page of each integration, in the same way as it’s done for the `light.turn_on` [action](https://www.home-assistant.io/actions/light.turn_on/).
### Use templates to decide which action to perform 
You can use [templating](https://www.home-assistant.io/docs/templating/) support to dynamically choose which action to perform. For example, you can perform a certain action based on if a light is on.

```
action: 
  {% if states('sensor.temperature') | float  15 %}
    switch.turn_on
  {% else %}
    switch.turn_off
  {% endif %}
entity_id: switch.ac
```

YAML
Copy
### Using the Actions developer tool 
You can use the **Actions** developer tool to test data to pass in an action. For example, you may test turning a [light group](https://www.home-assistant.io/integrations/group/) on or off.
To turn a light group on or off, pass the following info:
  * Domain: `homeassistant`
  * Action: `turn_on`
  * Action data: `{ "entity_id": "light.kitchen" }`


### Use templates to determine the attributes 
Templates can also be used for the data that you pass to the action.

```
action: thermostat.set_temperature
target:
  entity_id: 
    {% if is_state('device_tracker.paulus', 'home') %}
      thermostat.upstairs
    {% else %}
      thermostat.downstairs
    {% endif %}
data:
  temperature: "{{ 22 - distance(states.device_tracker.paulus) }}"
```

YAML
Copy
You can use a template returning a native dictionary as well, which is useful if the attributes to be set depend on the situation.

```
action: climate.set_temperature
data: 
  {% if states('sensor.temperature_living')  19 %}
    {"hvac_mode": "heat", "temperature": 19 }
  {% else %}
    {"hvac_mode": "auto" }
  {% endif %}
```

YAML
Copy
### Use templates to handle response data 
Some actions may respond with data that can be used in automation. This data is called _action response data_. Action response data is typically used for data that is dynamic or large and which may not be suited for use in entity state. Examples of action response data are upcoming calendar events for the next week or detailed driving directions.
Templates can also be used for handling response data. The action can specify a `response_variable`. This is the [variable](https://www.home-assistant.io/docs/scripts/#variables) that contains the response data. You can define any name for your `response_variable`. This example performs an action and stores the response in the variable called `agenda`.

```
action: calendar.get_events
target:
  entity_id: calendar.school
data:
  duration:
    hours: 24
response_variable: agenda
```

YAML
Copy
You may then use the response data in the variable `agenda` in another action in the same script. The example below sends a notification using the response data.
Important
Which data fields can be used in an action depends on the type of notification that is used.

```
action: notify.gmail_com
data:
  target: "gduser1@workspacesamples.dev"
  title: "Daily agenda for {{ now().date() }}"
  message: -
    Your agenda for today:
    <p
    {% for event in agenda['calendar.school'].events %}
    {{ event.start}}: {{ event.summary }}<br
    {% endfor %}
    </p
```

YAML
Copy
###  `homeassistant` actions 
There are four `homeassistant` actions that aren’t tied to any single domain, these are:
  * `homeassistant.turn_on` - Turns on an entity (that supports being turned on), such as an `automation` or `switch`.
  * `homeassistant.turn_off` - Turns off an entity (that supports being turned off), such as an `automation` or `switch`.
  * `homeassistant.toggle` - Turns off an entity that is on, or turns on an entity that is off (that supports being turned on and off)
  * `homeassistant.update_entity` - Request the update of an entity, rather than waiting for the next scheduled update, for example [Google travel time](https://www.home-assistant.io/integrations/google_travel_time/) sensor, a [template sensor](https://www.home-assistant.io/integrations/template/), or a [light](https://www.home-assistant.io/integrations/light/)


Complete action details and examples can be found on the [Home Assistant integration](https://www.home-assistant.io/integrations/homeassistant#actions) page.
####  **Help us improve our documentation**
Suggest an edit to this page, or provide/view feedback for this page. 


Back to top
