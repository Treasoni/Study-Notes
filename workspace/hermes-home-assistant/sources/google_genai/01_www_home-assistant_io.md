---
url: "https://www.home-assistant.io/integrations/google_generative_ai_conversation/"
title: "Google Gemini - Home Assistant"
scraped_at: 2026-09-17T16:38:24+00:00
---

The **Google Gemini** integrationIntegrations connect and integrate Home Assistant with your devices, services, and more.[ [Learn more]](https://www.home-assistant.io/getting-started/concepts-terminology/#integrations) adds a conversation agent, speech-to-text, and text-to-speech entities powered by [Google Gemini](https://ai.google.dev/) to Home Assistant. The conversation agent can optionally be allowed to control Home Assistant.
Controlling Home Assistant is done by providing the AI access to the Assist API of Home Assistant. You can control what devices and entities it can access from the [exposed entities page](https://my.home-assistant.io/redirect/voice_assistants). The AI can provide you information about your devices and control them.
This integration does not integrate with [sentence triggers](https://www.home-assistant.io/docs/automation/trigger/#sentence-trigger).
This integration requires an API key to use, [which you can generate here](https://aistudio.google.com/app/apikey), and to be in one of the [available regions](https://ai.google.dev/gemini-api/docs/available-regions).
## Configuration 
To add the **Google Gemini** service to your Home Assistant instance, use this My button:
Manual configuration steps
If the above My button doesn’t work, you can also perform the following steps manually:
  * Browse to your Home Assistant instance.
  * Go to **[Settings> Devices & services](https://my.home-assistant.io/redirect/integrations)**.
  * In the bottom right corner, select the button.
  * From the list, select **Google Gemini**.
  * Follow the instructions on screen to complete the setup.


## Generate an API Key 
The API key is used to authenticate requests to the Google Gemini API. To generate an API key take the following steps:
  * Visit the [API Keys page](https://aistudio.google.com/app/apikey) to retrieve the API key you’ll use to configure the integration.


On the same page, you can see your plan: _free of charge_ if the associated Google Cloud project doesn’t have billing, or _pay-as-you-go_ if the associated Google Cloud project has billing enabled. Comparison of the plans is available [at this pricing page](https://ai.google.dev/pricing). The major differences include: the free of charge plan is rate limited, and free prompts/responses are used for product improvement.
## Options 
To define options for Google Gemini, follow these steps:
  1. In Home Assistant, go to **[Settings> Devices & services](https://my.home-assistant.io/redirect/integrations)**.
  2. If multiple instances of Google Gemini are configured, choose the instance you want to configure.
  3. On the card, select the cogwheel .
     * If the card does not have a cogwheel, the integration does not support options for this service.
  4. Edit the options, then select **Submit** to save the changes.


Instructions
Instructions for the AI on how it should respond to your requests. It is written using [Home Assistant Templating](https://www.home-assistant.io/docs/templating/).
Control Home Assistant
If the model is allowed to interact with Home Assistant. It can only control or provide information about entities that are [exposed](https://www.home-assistant.io/voice_control/voice_remote_expose_devices/) to it.
Recommended settings
If enabled, the recommended model and settings are chosen.
If you choose to not use the recommended settings, you can configure the following options:
Model
Model used to generate response.
Temperature
Creativity allowed in the responses. Higher values produce a more random and varied response. A temperature of zero will be deterministic.
Top P
Probability threshold for top-p sampling.
Top K
Number of top-scored tokens to consider during generation.
Maximum Tokens to Return in Response
The maximum number of words or “tokens” that the AI model should generate.
Thinking budget
The token budget for internal reasoning before the model generates a response (Gemini 2.5 models only). Set this to `-1` to let the model decide automatically, `0` to disable reasoning (not available for Gemini 2.5 Pro), or a positive number for a custom budget.
Thinking level
The level of internal reasoning for Gemini 3 models. For Gemini Flash series models, you can choose **Minimal** , **Auto** , **Low** , **Medium** , or **High**. For Gemini 3.1 Pro, you can choose **Auto** , **Low** , **Medium** , or **High**. This setting is ignored for Gemini 2.5 models, which use the thinking budget instead.
Safety settings
Thresholds for different [harmful categories](https://ai.google.dev/gemini-api/docs/safety-settings).
Enable Google Search tool
Enables the model to [query Google Search](https://ai.google.dev/gemini-api/docs/grounding). This can only be enabled when the “Control Home Assistant” setting is set to “No control”. See below for a workaround using it with “Assist”.
## Google Search 
Due to an API limitation we cannot have the [Google Search tool](https://ai.google.dev/gemini-api/docs/grounding) together with other tools. Request fails with `400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Tool use with function calling is unsupported', 'status': 'INVALID_ARGUMENT'}}`. But you can do the following workaround that exposes a script to voice assistants. The script calls a Google Gemini Conversation that only has the Google Search tool enabled.
Workaround for Google Search tool
  1. Add a second Google Gemini conversation agent.
  2. Select **Configure**
  3. In the **Control Home Assistant** section, uncheck **Assist** and any other options.
  4. Uncheck **Recommended model settings**
  5. Select **Submit**
  6. Check **Enable Google Search tool**
  7. Increase **Maximum tokens to return in response**
  8. Select **Submit**
  9. Create a script (**Settings** > **Automations & scenes** > **Scripts** > **Create script**)
  10. Select 3 dots > **Edit in YAML** and enter the following (edit the `conversation.google_generative_ai_2` to match the entity created from the 1st step):

```
sequence:
  - action: conversation.process
    metadata: {}
    data:
      agent_id: conversation.google_generative_ai_2
      : "{{ query }}"
    response_variable: result
  - variables:
      result:
        response: "{{ result.response.speech.plain.speech }}"
  - stop: ""
    response_variable: result
alias: "Assist: Search Google"
description: -
  Uses Google Search to answer questions that are completely unrelated to
  the smart home, and focus on current events or information in real time,
  such as the current president, last night's game results, or release
  dates.
fields:
  query:
    selector:
      text: null
    name: Query
    description: The query to search Google for
    required: true
```

YAML
Copy
  11. Select **Save script**
  12. Select 3 dots > **Settings** > **Voice assistants**
  13. Check **Expose** **Assist**


## Using Google Gemini text-to-speech in automations 
The **Google Gemini** integration adds a text-to-speech entity. To play a spoken message from an automation or script, use the [**Speak**](https://www.home-assistant.io/actions/tts.speak/) action and select your Google Gemini text-to-speech entity as the target.
To speak a message from an automation or a script:
  1. Go to [**Settings** > **Automations & scenes**](https://my.home-assistant.io/redirect/automations).
  2. Open an existing automation or script, or select **Create automation** > **Create new automation**.
  3. If you are setting up a new automation, add a trigger in the **When** section. Scripts do not need a trigger. They run when something else calls them.
  4. In the **Then do** section, select **Add action**.
  5. Select what you want to control. Under **By target** , select your Google Gemini text-to-speech entity.
  6. From the actions shown for that target, select **Speak**. To choose a Gemini voice, set `voice` in **Options**. For supported options, see [Google Gemini text-to-speech action options](https://www.home-assistant.io/integrations/google_generative_ai_conversation/#google-gemini-text-to-speech-action-options).
  7. Select the **Media player entity** to play the message on, set the **Message** , and set any other options you want to use.
  8. Select **Save**.


Example YAML configuration

```
action: tts.speak
target:
  entity_id: tts.google_ai_tts
data:
  media_player_entity_id: media_player.living_room
  message: "Say cheerfully: Have a wonderful day!"
  options:
    voice: achernar
```

YAML
Copy
### Google Gemini text-to-speech action options 
####  Configuration Variables 
[Looking for your configuration file?](https://www.home-assistant.io/docs/configuration/)
voice string (Optional)
The voice name to use for the generated speech. The default is `zephyr`. For available voices, see the [Google AI speech generation documentation](https://ai.google.dev/gemini-api/docs/speech-generation#voices).
Google Gemini detects the input language automatically. For supported languages, see the [Google AI speech generation documentation](https://ai.google.dev/gemini-api/docs/speech-generation#languages).
## Talking to Super Mario 
You can use Google Gemini to follow the [Super Mario voice assistant tutorial](https://www.home-assistant.io/voice_control/assist_create_open_ai_personality/) and let him control devices in your home.
The tutorial uses OpenAI, but you can follow the same approach with the Google Gemini integration.
## Video tutorial 
This video tutorial explains how Google Gemini can be set up, how you can send an AI-generated message to your smart speaker when you arrive home, and how you can analyze an image taken from your doorbell camera as soon as someone rings the doorbell.
## Troubleshooting 
  * To aid in diagnosing issues it may help to turn up verbose logging by adding these to your `configuration.yaml`The configuration.yaml file is the main configuration file for Home Assistant. It lists the integrations to be loaded and their specific configurations. In some cases, the configuration needs to be edited manually directly in the configuration.yaml file. Most integrations can be configured in the UI.[ [Learn more]](https://www.home-assistant.io/docs/configuration/):



```
logger:
  logs:
    homeassistant.components.conversation: debug
    homeassistant.components.conversation.chat_log: debug
    homeassistant.components.google_generative_ai_conversation: debug
```

YAML
Copy
## Removing the integration 
### To remove an integration instance from Home Assistant 
  1. Go to [**Settings** > **Devices & services**](https://my.home-assistant.io/redirect/integrations) and select the integration card.
  2. From the list of devices, select the integration instance you want to remove.
  3. Next to the entry, select the three dots menu. Then, select **Delete**.


## Related topics 
  * [ Exposing entities to assist ](https://www.home-assistant.io/voice_control/voice_remote_expose_devices/)
  * [ Create an ai personality ](https://www.home-assistant.io/voice_control/assist_create_open_ai_personality/)


## Related links 
  * [Google Gemini API key](https://aistudio.google.com/app/apikey)


####  **Help us improve our documentation**
Suggest an edit to this page, or provide/view feedback for this page. 


Back to top
