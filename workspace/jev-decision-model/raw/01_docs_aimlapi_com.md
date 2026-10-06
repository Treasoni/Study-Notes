---
url: "https://docs.aimlapi.com/api-references/decision-models/typesafe/jev"
title: "Jev | AI/ML API Documentation"
scraped_at: 2026-09-20T15:10:09+00:00
---

For the complete documentation index, see [llms.txt](https://docs.aimlapi.com/llms.txt). This page is also available as [Markdown](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev.md).
On this page
This documentation is valid for the following list of our models:
  * `typesafe/jev`


[Try in Playground](https://aimlapi.com/app/typesafe/jev)
##  Model Overview
Jev is TypeSafe's first "System One" model: a structured decision model that returns typed answers (yes/no, choice, score) with calibrated probabilities instead of generated text. It is built for routing, classification, triage and other in-app decision points where a fast, predictable verdict matters more than prose — typically answering in well under a second. Text input only, 32K context.
How to make the first API call
**1️⃣ Required setup (don’t skip this)** ▪ **Create an account:** Sign up on the AI/ML API website (if you don’t have one yet). ▪ **Generate an API key:** In your account dashboard, create an API key and make sure it’s **enabled** in the UI.
**2️ Copy the code example** At the bottom of this page, pick the snippet for your preferred programming language (Python / Node.js) and copy it into your project.
**3️ Update the snippet for your use case** ▪ **Insert your API key:** replace `<YOUR_AIMLAPI_KEY>` with your real AI/ML API key. ▪ **Select a model:** set the `model` field to the model you want to call. ▪ **Provide input:** put the content to evaluate in `state` and describe what to decide in `questions`.
**4️ (Optional) Tune the request** See the API schema below for the three question types (`noul`, `choice`, `score`) and their `criteria`.
**5️ Run your code** Run the updated code in your development environment.
For a detailed walkthrough, use our .
##  API Schema
posthttps://api.aimlapi.com/v1/decisions
Body
application/json
modelstring · enumRequiredPossible values: `typesafe/jev`
stateany ofRequired
The content to evaluate: a string, a JSON object, or an array of texts. Text only.
Example: `Help! My payments have been failing for 3 days.`
stringOptional
or
objectOptional
Show properties
or
any[]Optional
Show properties
questionsobjectRequired
Map of question key → typed question. Every key comes back in `answers` with a typed result.
Show properties
Responses
200
Successful response.
application/json
modelstringRequired
Resolved model version that answered.
Example: `typesafe/jev`
answersobjectRequired
One typed answer per question key from the request.
Show properties
usageobjectRequired
Token usage reported by the provider.
Show properties
post/v1/decisions

```
curl -L \
  --request POST \
  --url 'https://api.aimlapi.com/v1/decisions' \
  --header 'Authorization: Bearer <YOUR_AIMLAPI_KEY>' \
  --header 'Content-Type: application/json' \
  --data '{
      "model": "typesafe/jev",
      "state": "Help! My payments have been failing for 3 days and nobody answers support.",
      "questions": {
        "is_urgent": {
          "type": "noul",
          "instructions": "Does this convey urgency?"
        "department": {
          "type": "choice",
          "instructions": "Which team should handle this?",
          "criteria": {
            "billing": "Payments, invoicing, refunds",
            "technical": "Bugs, outages, integrations",
            "sales": "Pricing, upgrades, new accounts"
        "frustration": {
          "type": "score",
          "instructions": "How frustrated is the customer?",
          "criteria": [
            "Calm",
            "Frustrated",
            "Very angry"

```

200
Successful response.

```
  "model": "typesafe/jev",
  "answers": {
    "ANY_ADDITIONAL_PROPERTY": {
      "type": "noul",
      "noul": 1
  "usage": {
    "input_tokens": 1,
    "output_tokens": 1

```

##  Code Example
Python
JavaScript

```
import requests
response = requests.post(
    "https://api.aimlapi.com/v1/decisions",
    headers={
        "Authorization": "Bearer <YOUR_AIMLAPI_KEY>",
        "Content-Type": "application/json",
    json={
        "model": "typesafe/jev",
        "state": "Help! My payments have been failing for 3 days and nobody answers support.",
        "questions": {
            "is_urgent": {
                "type": "noul",
                "instructions": "Does this convey urgency?",
            "department": {
                "type": "choice",
                "instructions": "Which team should handle this?",
                "criteria": {
                    "billing": "Payments, invoicing, refunds",
                    "technical": "Bugs, outages, integrations",
                    "sales": "Pricing, upgrades, new accounts",
            "frustration": {
                "type": "score",
                "instructions": "How frustrated is the customer?",
                "criteria": ["Calm", "Frustrated", "Very angry"],
print(response.json())
```


```
const response = await fetch('https://api.aimlapi.com/v1/decisions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <YOUR_AIMLAPI_KEY>',
    'Content-Type': 'application/json',
  body: JSON.stringify({
    model: 'typesafe/jev',
    state: 'Help! My payments have been failing for 3 days and nobody answers support.',
    questions: {
      is_urgent: {
        type: 'noul',
        instructions: 'Does this convey urgency?',
      department: {
        type: 'choice',
        instructions: 'Which team should handle this?',
        criteria: {
          billing: 'Payments, invoicing, refunds',
          technical: 'Bugs, outages, integrations',
          sales: 'Pricing, upgrades, new accounts',
      frustration: {
        type: 'score',
        instructions: 'How frustrated is the customer?',
        criteria: ['Calm', 'Frustrated', 'Very angry'],
console.log(await response.json());
```

Response

```
  "model": "typesafe/jev-1.13-20260917",
  "answers": {
    "is_urgent": {
      "type": "noul",
      "noul": 0.96
    "department": {
      "type": "choice",
      "choice": "billing",
      "confidence": 0.97,
      "probabilities": {
        "billing": 0.98,
        "technical": 0.02,
        "sales": 0
    "frustration": {
      "type": "score",
      "score": 1.3,
      "confidence": 0.55,
      "legend": {
        "0": "Calm",
        "1": "Frustrated",
        "2": "Very angry"
      "probabilities": {
        "0": 0,
        "1": 0.7,
        "2": 0.3
  "usage": {
    "input_tokens": 403,
    "output_tokens": 73
  "meta": {
    "usage": {
      "credits_used": 47,
      "usd_spent": 0.0000235

```

[ PreviousTypeSafe ](https://docs.aimlapi.com/api-references/decision-models/typesafe)[ NextHow can I work with my API keys? ](https://docs.aimlapi.com/faq/how-can-i-work-with-my-api-keys)
Last updated 2 days ago
Was this helpful?
