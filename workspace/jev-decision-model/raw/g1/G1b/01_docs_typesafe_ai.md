---
url: "https://docs.typesafe.ai/patterns"
title: "Patterns - TypeSafe AI"
scraped_at: 2026-09-20T15:10:43+00:00
---

> ## Documentation Index
> Fetch the complete documentation index at: [/llms.txt](https://docs.typesafe.ai/llms.txt)
> Use this file to discover all available pages before exploring further.
[Skip to main content](https://docs.typesafe.ai/patterns#content-area)
TypeSafe is designed to sit within a larger system, powering decisions with AI. Learning to think in terms of discrete, atomic decisions that compose into complex system behavior is a key skill for getting the most out of TypeSafe. This section assumes you know the [TypeSafe primitives](https://docs.typesafe.ai/primitives) and understand [how confidence works](https://docs.typesafe.ai/confidence). If not, read those first.
##  The patterns  
| Pattern  | What it does  | Benefits  |  
| --- | --- | --- |  
| [Speculative Fan-Out](https://docs.typesafe.ai/patterns/fan-out)  | Send many questions in a single call, including speculative ones, and let your code decide what’s relevant  | Cost, Speed  |  
| [Confidence-Gated Routing](https://docs.typesafe.ai/patterns/confidence-routing)  | Utilize confidence as a second decision axis to build safer systems  | Reliability, Safety  |  
| [Composite Scoring](https://docs.typesafe.ai/patterns/composite-scoring)  | Combine several dimensions of analysis into a single score  | Cost, Reliability, Speed  |  
| Classify a user’s intent and route to the appropriate handler  | Cost, Speed  |  
We’re always keen to learn how people are making use of our primitives. If you’ve found a killer use case you think should be mentioned here, feel free to drop us a note!
Was this page helpful?
