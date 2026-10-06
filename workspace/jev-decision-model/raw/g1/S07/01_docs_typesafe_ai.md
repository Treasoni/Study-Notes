---
url: "https://docs.typesafe.ai/introduction/quickstart"
title: "Quick start - TypeSafe AI"
scraped_at: 2026-09-20T15:10:32+00:00
---

> ## Documentation Index
> Fetch the complete documentation index at: [/llms.txt](https://docs.typesafe.ai/llms.txt)
> Use this file to discover all available pages before exploring further.
[Skip to main content](https://docs.typesafe.ai/introduction/quickstart#content-area)
##  Try it: the Playground
  1. **Open the[Playground](https://console.typesafe.ai/playground)** and log in.
  2. **Paste any text** as the state.


Sample state

```
Hi, I've been trying to connect my Stripe account for 3 days and the integration keeps failing. I'm losing sales. Please help ASAP.

```

  1. **Add a question.** Try a Noul question: `"Does this message express urgency?"`



```

  "urgency": {
    "type": "noul",
    "instructions": "Does this message express urgency?"



```

  1. **Add more questions.** Mix Noul, Choice, and Score in one call and see all results at once.


##  Call it: the API
  1. **Get your API key** from the [dashboard](https://console.typesafe.ai/keys)
  2. **Make a POST request** to the API endpoint
  3. **Review the[API Reference](https://docs.typesafe.ai/api)** for all the details.



```
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <API_KEY>
Content-Type: application/json

```

###  Sample cURL command

```
curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @-'EOF'

    "state": "Hi, I've been trying to connect my Stripe account for 3 days and the integration keeps failing. I'm losing sales. Please help ASAP.",
    "model": "jev-latest",
    "questions": {
      "urgency": {
        "type": "noul",
        "instructions": "Does this message express urgency?"





```

###  Request body

```

  "state": "Hi, I've been trying to connect my Stripe account for 3 days and the integration keeps failing. I'm losing sales. Please help ASAP.",
  "model": "jev-latest",
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "Which team should handle this",
      "criteria": {
        "billing": "Payment or subscription issues",
        "technical": "Bugs or integration problems",
        "sales": "Pricing or account questions"


    "frustration": {
      "type": "score",
      "instructions": "How frustrated the customer appears",
      "criteria": [
        "Calm, just stating facts",
        "Frustrated but civil",
        "Very angry, strong language"


    "is_urgent": {
      "type": "noul",
      "instructions": "The message conveys urgency or time-sensitivity"




```

###  Response body

```

  "model": "jev-1.13.0",
  "answers": {
    "department": {
      "type": "choice",
      "choice": "technical",
      "confidence": 0.78,
      "probabilities": {
        "technical": 0.85,
        "sales": 0.0,
        "billing": 0.15


    "frustration": {
      "type": "score",
      "score": 1.0,
      "confidence": 1.0,
      "legend": {
        "0": "Calm, just stating facts",
        "1": "Frustrated but civil",
        "2": "Very angry, strong language"

      "probabilities": {
        "0": 0.0,
        "1": 1.0,
        "2": 0.0


    "is_urgent": {
      "type": "noul",
      "noul": 1.0


  "usage": {
    "input_tokens": 392,
    "output_tokens": 65



```

See the [API Reference](https://docs.typesafe.ai/api) for all the details.
##  Code it: the Python SDK
  1. **Install the SDK** (requires Python >= 3.10).


With pip

```
pip install typesafe-sdk

```

With uv

```
uv add typesafe-sdk

```

  1. **Use the SDK.** The client reads `TYPESAFE_API_KEY` from the environment and calls `jev-latest` by default.



```
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()

ticket = "Hi, I've been trying to connect my Stripe account for 3 days and the integration keeps failing. I'm losing sales. Please help ASAP."

response = client.system_one(
    state=ticket,
    questions={
        "department": Choice(
            instructions="Which team should handle this",
            criteria={
                "billing": "Payment or subscription issues",
                "technical": "Bugs or integration problems",
                "sales": "Pricing or account questions",


        "frustration": Score(
            instructions="How frustrated the customer appears",
            criteria=[
                "Calm, just stating facts",
                "Frustrated but civil",
                "Very angry, strong language",


        "is_urgent": Noul(
            instructions="The message conveys urgency or time-sensitivity",




print(response.answers["department"].choice)  # "technical"
print(response.answers["frustration"].score)  # 1.0
print(response.answers["is_urgent"].noul)     # 1.0

```

See [client SDKs](https://docs.typesafe.ai/sdk) for installation options and detailed usage.
##  Vibe it: the agent skill
  1. **[Install the TypeSafe skill](https://docs.typesafe.ai/agent-skill#installation)** using the Claude Code plugin or `npx skills add typesafe-ai/skills --skill typesafe-ai`. You can also [read SKILL.md on GitHub](https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md).


  * Claude Code
  * Other agents
  * Copy to your agent


Run these two commands in your terminal:

```
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai

```


```
npx skills add typesafe-ai/skills --skill typesafe-ai

```

Choose your agent when prompted. Installation is project-local by default; add `-g` to install globally.
Paste this prompt into your coding agent:

```
Install the TypeSafe skill. If you're in Claude Code, run `claude plugin marketplace add typesafe-ai/skills`, then `claude plugin install typesafe@typesafe-ai`. If you're in another agent, run `npx skills add typesafe-ai/skills --skill typesafe-ai` and select your agent. Use one installation method. You can read the skill directly at https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md (raw: https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md). Then use the TypeSafe skill when working on this project.

```

  1. **Tell your coding agent** to use the TypeSafe skill as you build!


Coding agent prompt

```
Let's build a simple CLI that uses the TypeSafe API to evaluate a set of supplied documents on multiple dimensions. Use the TypeSafe skill to understand how to use the TypeSafe API and how to structure the system. Ask me questions about what kinds of documents I want to evaluate and on what dimensions.

```

See the [Agent Skill](https://docs.typesafe.ai/agent-skill) page for more details.
Was this page helpful?
