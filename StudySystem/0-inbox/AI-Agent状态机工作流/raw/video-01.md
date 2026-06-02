---
title: "Building Multi agent Systems with Finite State Machines"
url: "https://www.youtube.com/watch?v=OD13PiXw60o"
channel: "AI Engineer"
speaker: "Adam Terlson"
publish_date: "2025-02-22"
duration: "17:11"
type: video
authority: 5
freshness: 5
completeness: 5
readability: 4
score: 4.8
classification: core_concepts
---

# Building Multi agent Systems with Finite State Machines

> **TL;DR**: Adam Terlson 在 AI Engineer 大会的演讲，论证 State Machine + Actor Model 是构建可控、可观测 LLM Agent 的"永恒基石"。演讲覆盖 Tool Use / Feedback / Orchestration / Chartering 等 Agentic 模式，全部用 State Charts 视角重新诠释。

## 关键论点
- AI Governance 是 Gartner 2025 年第二趋势，State Machine 是治理 agent 决策/行为的基础工具
- FSM 五要素：状态定义、转移逻辑、事件、守卫、操作
- Actor Model 提供并发和消息驱动通信，与 LLM 推理天然契合
- Chartering（自创术语）= 给 agent 一份"宪法"，约束行为边界

## 完整 Transcript

**[0:04]** hi I'm Adam charlson and in this video I'll walk you through how finite State machines provide a structured reliable foundation for building applications including AI agents as AI becomes more autonomous the challenge isn't just intelligence or model performance it's also how to build systems with predictability observability and control espe important qualities when orchestrating large language models so the year is 2025 and the top

**[0:38]** AI Trends as listed by Gartner and probably everyone else too is a gentic AI we're autonomous AI plans and acts to achieve all our hopes and dreams but the number two Trend called out by Gardner is just as if not more important and that is the development of AI governance platforms we humans need to find a way to manage the ethical legal and operational performance of agentic systems now State

**[1:09]** machines probably don't have much to offer to the ethical or perhaps legal challenges of AI governance but I believe they may have a foundational role to play in building platforms that effectively govern agent decision Mak and behavior so let's Dive Right In what is a finite State machine well it's a computational model of a system with States and transitions that are triggered by events the example shown

**[1:39]** here is for the game of rock paper scissors our game is defined by five key components the first are the state definitions this is a declarative uh set of system modes and configurations in our game it's the initial state of locking eyes the parallel states where players are selecting their throws all the way to the final State when the game is over there is transition Logic for how we move between these states when events

**[2:10]** occur like when we start the round uh but these can also be targetless transitions as is the case with rock paper and scissors on shoot we apply a guard which enforces valid transitions so on the case of shot we check if the throws match and if they do then we go back to select another throw otherwise we can continue on in the flow in each transition we can apply actions and effects side effects that

**[2:41]** are triggered by transitions like sending a message or updating context and context is store data that is used for transition logic and also uh final output now the lovely nerds out there are likely yelling at their screens at this point saying that's not a state machine it's a state chart you're right a state chart is an extension of the state machine that adds a richer vocabulary to the model including things

**[3:13]** like hierarchical and parallel states which I used in my game in this presentation however I may use these terms interchangeably it'll be okay a state chart models an applications Behavior but on its own it lacks a essential capabilities needed to build a whole application the actor model complements State charts by providing a framework for concurrent distributed and encapsulated execution that's right not an agent an

**[3:45]** actor so what is an actor uh an actor uh is an autonomous entity that interacts with other actors via message passing actors and software only have three capabilities they can send and receive messages they can update their internal State and they can create new actors and of course finite State machines can be used to define that actor's internal Behavior or logic so together State machines and

**[4:17]** actors create a scalable and maintainable application architecture a mentor of mine at Best Buy said that in more in his more than 40 years in it he's never met a finite State machine he did not like why would he today working as a senior principal security Architects say that and the answer is because of the significant advantages that state machines bring to the operator they are predictable they're traceable and auditable they're

**[4:50]** reliable and recoverable if you lose your current state you can actually recalculate it by playing your replaying your log of events if you only play back some of those events stopping at a certain point in time you can then create a new branch in history effectively traveling through time they're low latency they're declarative as we saw with the state chart itself they're easily tested you can do what's called modelbased testing

**[5:20]** where you can be programmatically certain that your tests are exercising every valid transition in your machine their modular and adaptable they're scalable and they allow you to handle the most complex error error scenarios even implementing what's called The Saga pattern for distributed transactions in the sagas pattern you have a transaction that takes place over multiple requests if a step in the process fails you can apply compensating

**[5:50]** transactions to undo the previous steps and get the customer back into a valid state of course they also come with challenges there's a limited uh flexibility to the system and if you're trying to model uh uh a system with thousands perhaps infinite number of states your state can really explode you have to model your transitions explicitly and you can sometimes have uh have an issue where an event lands on

**[6:21]** your machine that you haven't modeled yet and so thankfully your machine doesn't do anything in that case except for log it for remediation you do have to handle uh concurrency and parallelism because as I mentioned before the actor uh can only process one event at a time this is where something like Azure service bus sessions and AWS sqs 5o message groups would come into play versioning is a definite challenge

**[6:52]** as maybe you have a state in one version that goes away in the next now if you were to replay your log of events through your machine what state do you land in you have to take this into account and there's a learning curve associated with State machines I think that curve is a joy but you may be feeling something else right now what I want to draw your attention to is that these advantages brought by state machines are everything that llms

**[7:23]** are not llms are not predictable they're not traceable or auditable they're they're not reliable or recoverable they're not declarative or low latency Etc the opportunity is that by combining llms and state machines together we can build a system that leverages the strengths of one to mitigate the weaknesses of the other so we have our building blocks of agentic systems are actors enable

**[7:55]** autonomy and communication the state machine provides structure and enforces predictable behaviors and the llm enables Dynamic intelligence so let's put these building blocks into action in the agentic state machines pattern showcase our showcase begins as did the human race with tool use tool use is at the bottom of the autonomy chart because it really is foundational for the other patterns that follow that is it gives

**[8:27]** the llm the ability to act in tool use a description of available tools is passed to the llm including method names and and expected arguments and the llm returns a response describing to the caller how the tool should be called the llm doesn't call that method directly the llm then expects the next message uh in the flow to be the tool response this is motivated by especially needing to give additional capability

**[8:58]** and function ity to the llm allowing it to take action tools can also be used to improve response relevance via retrieval augmented generation in this example a model with a prompt to create a recipe is given a tool to fetch the inventory first so that the recipe returned uses only the ingredients that are actually available now right away we can talk about human in the loop human in the loop is something that state machines

**[9:28]** are natur natur Al very good at this doesn't have anything to do with agents but we all know that llms are famously unreliable so how do we put controls around its use of tools well we can simply add an intermediate intermediate approval step and wait for an authenticated and authorized message to direct what happens next in this example the admin first denies and then approves the request

**[9:59]** next feedback in feedback instead of having one agent we have two and agents just like humans improve over time with feedback we need to give llms time to think and iterating with feedback either from another agent another human or both can dramatically improve response quality in this example our recipe writer from before uh sends its output to the critic agent perhaps a specialist

**[10:31]** in nutrition the critic sends its feedback back like use less sugar and the recipe writer has the opportunity to improve its its response here we have two agents working directly together but what if we want a whole team of Agents well that is collaboration with collaboration multiple agents each specializing in their own small slice of a task work

**[11:03]** together to achieve a broader outcome this is motivated by the training limitations of llms and the scaling limitations of prompting them we can't achieve broad multifaceted goals with a single prompt to a model instead we create specialized units and compose them together into a broader workflow in this example of collaboration multiple agents work together to deliver a meal to a customer we have the recipe

**[11:35]** writer from before but also an agent specialized in procuring ingredients one that is responsible for preparing the meal getting feedback and finally publishing a report State machines don't need to have a final State and this example the report and any other context is used by the recipe writer as feedback for how it to continuously improve with State machines that flow is predictable and tightly

**[12:06]** governed but what if we want to change that what if we want to make the sequence of States itself determined by the llm and that is agentic orchestration with orchestration a centralized planning node can direct the next state this is helpful when reasoning around context is required to determine the next state for example by understanding if the goal has been achieved and whether it can exit the

**[12:38]** flow now the example that I'm showing here got a bit big so I apologize that it's hard to see but notice the bouncing back and forth between various States and the central planning agents the tool in this case that I gave to the planning agent was in fact a set of event emitters and then I implemented transition guards to enforce that these transitions are valid and direct to the appropriate state so we're definitely having fun now

**[13:11]** Beyond selecting the next state how can we take this even further well what if we gave the whole state chart over to the llm and asked it to generate it I call this agentic chartering I wasn't able to find much about this pattern online there may be a better name for it and if you know of one please let me know in the comments chartering is helpful when you want to separate your planning phase

**[13:42]** from your execution phase with chartering the agent has the capability of inventing a wholly new and novel process to achieve its goal with prompting and fine-tuning one can imagine llms being able to build these processes using off the-shelf patterns and tools like predetermined events known context available actors Etc so for example I hate postal junk mail when I get something sent to my

**[14:13]** house I do my best to get myself off whatever list they were using to send it to me wouldn't it be nice if I had a personal agent that could do this work for me to experiment with this I gave an article I found on privacy rights.org for how to remove myself from the White Pages data broker uh and I gave this process to 01 to build a new process uh and it did a remarkable good job especially considering this was done

**[14:43]** essentially zero shot with no examples uh given llms are also good at interpreting State charts visually just think we have 70 years of State charts s to train on we could add a visualization agent as feedback to the chartering agent to get uh on how to improve its plan that's the fun thing about agents whatever the problem is the solution is always to

**[15:14]** just add another agent so where is this graph leading I think the answer is towards emergence and now that's one pattern I haven't been able to express with a state chart yet but if we are going to achieve something that performs and feels like emergence I do not be I do not believe it will be because we've created a system model more closely to

**[15:45]** the human brain it'll be because we found a way to make Building agentic Systems feel like building with Legos all the best technology in my opinion has this quality in in common whether you're building an app with react native deploying it with GitHub actions or provisioning services on AWS with infrastructure as code each of these technologies have a model of composing specialized units together into a

**[16:15]** broader system that is greater than the sum of its parts so perhaps in achieving that the humble State machine may have a foundational role to play for the next 70 years as well a special thank you to xate the library I used for all the state charts and visualizations in this presentation if you haven't tried xstate already it's a really powerful tool for tackling system complexity and it's a joy to use

**[16:45]** especially with the changes they made in B5 if you want to see these patterns in action check out my demo red versus blue where I explore more about the operational side of State machines with a surprise emergence at the end please reach out to me on LinkedIn if you have any questions feedback or just want to connect thank you so much