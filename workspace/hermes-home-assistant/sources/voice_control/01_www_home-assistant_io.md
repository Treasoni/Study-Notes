---
url: "https://www.home-assistant.io/voice_control/"
title: "Assist - Talk to your smart home with Home Assistant - Home Assistant"
scraped_at: 2026-09-17T16:39:03+00:00
---

Assist is the voice assistant built into Home Assistant. It lets you control your smart home with natural language, and it can run fully on your own hardware, so your voice commands stay private. Assist works in the Home Assistant companion app, on dedicated voice hardware like the [Home Assistant Voice Preview Edition](https://www.home-assistant.io/voice-pe/), and on devices you build yourself with [ESPHome](https://www.esphome.io/components/voice_assistant/).
Look for the Assist icon at the top right of your dashboard to try it out right away.
Assist is built on an open voice foundation and powered by knowledge contributed by our community. It can work locally or, if you prefer, use one of the latest large language models to handle more conversational requests.
## Getting started 
When you configure voice assistant hardware made for Home Assistant, it will use a wizard to help you configure your system and get started to use voice.
Our recommended voice assistant hardware is the [Home Assistant Voice Preview Edition](https://www.home-assistant.io/voice-pe/).
In case your hardware does not support our wizard, do not worry. Here are two detailed guides based on how you plan to process your voice (Locally, or using Home Assistant Cloud voice services)
  * [I plan to process my voice locally](https://www.home-assistant.io/voice_control/voice_remote_local_assistant/)
  * [I plan to use Home Assistant Cloud](https://www.home-assistant.io/voice_control/voice_remote_cloud_assistant/) (recommended as it is the simplest)


## Expand and experiment 
Once your setup is up and running and you follow the [best practices](https://www.home-assistant.io/voice_control/best_practices), check all the possibilities we found for [Expanding your Assist setup](https://www.home-assistant.io/voice_control/expanding_assist), and further experiment with different setups like [wake words](https://www.home-assistant.io/voice_control/about_wake_word/). Do you want to talk to Super Mario? Or another figure? If you want Assist to respond in a fun way, you can create an assistant with an [AI personality](https://www.home-assistant.io/voice_control/assist_create_open_ai_personality/).
To further improve your setup, try building other voice assistant satellite devices that allow you to add Assist with wake words to all your rooms:
  * Enable [wake word detection on your Android phone](https://www.home-assistant.io/voice_control/android/#using-wake-word-detection-on-android) to activate Assist hands-free by saying “Hey Jarvis” or “Hey Nabu”, even when your phone is locked.
  * You can use [ESPHome](https://www.esphome.io/components/voice_assistant/) to create your own awesome voice assistant satellites based on inexpensive ESP32 microcontrollers, like [@piitaya](https://github.com/piitaya) did with his 3D-printed R5 droid. Follow our tutorial to [create your own for just $13](https://www.home-assistant.io/voice_control/thirteen-usd-voice-remote/).
  * Another alternative voice satellite solution is the experimental [Linux-Voice-Assistant](https://github.com/OHF-Voice/linux-voice-assistant) project that uses the [ESPHome](https://www.esphome.io/components/voice_assistant/) protocol. It allows you to build a Linux-based voice assistant smart speaker that runs on any x64 or ARM64 hardware capable of handling local, on-device audio processing. This approach provides greater flexibility for customization. Because it runs on a full Linux system, it also gives you access to significantly more local computing resources for additional features and other integrations on the same satellite. On HAOS, you can run it using the [Assist Satellite](https://github.com/OHF-Voice/apps/tree/main/assist_satellite) App if your Home Assistant machine has a connected microphone and speaker.
  * If you are interested in a voice assistant that is not always listening, consider using Assist on an analog phone. It will only listen when you pick up the horn, and the responses are for your ears only. Follow our tutorial to create your own [analog phone voice assistant](https://www.home-assistant.io/voice_control/worlds-most-private-voice-assistant/).


## Supported languages and sentences 
Assist aims to support more languages than other voice assistants, but this is still a work in progress, and we need your help.
Check supported languages here
Choose your language Afrikaans Albanian Amharic Arabic Armenian Azerbaijani Basque Bengali Bosnian Bulgarian Burmese Cantonese Catalan Chinese (Cantonese) Chinese (Mandarin) Croatian Czech Danish Dutch English Estonian Filipino Finnish French Galician Georgian German Greek Gujarati Hebrew Hindi Hungarian Icelandic Indonesian Irish Italian Japanese Javanese Kannada Kazakh Khmer Korean Lao Latvian Lithuanian Luxembourgish Macedonian Malay Malayalam Maltese Marathi Mongolian Nepali Norwegian Bokmål Pashto Persian Polish Portuguese Romanian Russian Serbian Shanghainese Sinhala Slovak Slovenian Somali Spanish Sundanese Swahili Swahili Swedish Tamil Telugu Thai Turkish Ukrainian Urdu Uzbek Vietnamese Welsh Zulu
Chinese (Mandarin)
  * Choose your language
  * Afrikaans
  * Albanian
  * Amharic
  * Arabic
  * Armenian
  * Azerbaijani
  * Basque
  * Bengali
  * Bosnian
  * Bulgarian
  * Burmese
  * Cantonese
  * Catalan
  * Chinese (Cantonese)
  * Chinese (Mandarin)
  * Croatian
  * Czech
  * Danish
  * Dutch
  * English
  * Estonian
  * Filipino
  * Finnish
  * French
  * Galician
  * Georgian
  * German
  * Greek
  * Gujarati
  * Hebrew
  * Hindi
  * Hungarian
  * Icelandic
  * Indonesian
  * Irish
  * Italian
  * Japanese
  * Javanese
  * Kannada
  * Kazakh
  * Khmer
  * Korean
  * Lao
  * Latvian
  * Lithuanian
  * Luxembourgish
  * Macedonian
  * Malay
  * Malayalam
  * Maltese
  * Marathi
  * Mongolian
  * Nepali
  * Norwegian Bokmål
  * Pashto
  * Persian
  * Polish
  * Portuguese
  * Romanian
  * Russian
  * Serbian
  * Shanghainese
  * Sinhala
  * Slovak
  * Slovenian
  * Somali
  * Spanish
  * Sundanese
  * Swahili
  * Swahili
  * Swedish
  * Tamil
  * Telugu
  * Thai
  * Turkish
  * Ukrainian
  * Urdu
  * Uzbek
  * Vietnamese
  * Welsh
  * Zulu


Local
Not supported
Needs more work
Usable
Fully supported
Home Assistant Cloud
Not supported
Needs more work
Usable
Fully supported
Assist already supports a wide range of [languages](https://developers.home-assistant.io/docs/voice/intent-recognition/supported-languages). Use the [built-in sentences](https://www.home-assistant.io/voice_control/builtin_sentences) to control entities and areas, or [create your own sentences](https://www.home-assistant.io/voice_control/custom_sentences/).
Did Assist not understand your sentence? [Contribute them](https://www.home-assistant.io/voice_control/contribute-voice).
_Assist was introduced in Home Assistant 2023.2._
## Related topics 
  * [ Build a $13 voice remote using an esphome device ](https://www.home-assistant.io/voice_control/thirteen-usd-voice-remote/)
  * [ Best practices with assist ](https://www.home-assistant.io/voice_control/best_practices/)


## Related links 
  * [Home Assistant Cloud](https://www.nabucasa.com/config/assist/)
  * [Voice Preview Edition](https://support.nabucasa.com/hc/categories/24451727188125)


####  **Help us improve our documentation**
Suggest an edit to this page, or provide/view feedback for this page. 


Back to top
