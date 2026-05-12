# What is harness engineering?
> 作者: Werner Heijstek
> 发布时间: 2026-04-24T15:32:10+00:00
> 原文链接: https://www.softwareimprovementgroup.com/blog/what-is-harness-engineering/

---

## In this article​

-   [Summary](#elementor-toc__heading-anchor-0)

-   [AI coding in 2026: from assistants to agents](#elementor-toc__heading-anchor-1)

-   [What is harness engineering?](#elementor-toc__heading-anchor-2)

-   [Why harness engineering matters: the governance gap](#elementor-toc__heading-anchor-3)

-   [Harness engineering vs. prompt and context engineering](#elementor-toc__heading-anchor-4)

-   [Three harness engineering misconceptions](#elementor-toc__heading-anchor-5)

-   [How to build an agent harness](#elementor-toc__heading-anchor-6)

-   [Why software portfolio governance is the harness](#elementor-toc__heading-anchor-7)

-   [How to get started with harness engineering](#elementor-toc__heading-anchor-8)

-   [About the author](#elementor-toc__heading-anchor-9)

-   [Frequently asked questions](#elementor-toc__heading-anchor-10)

## Summary

Harness engineering, coined by Mitchell Hashimoto in February 2026, is the practice of designing the full environment an AI agent operates within. It turns out [software portfolio governance](https://www.softwareimprovementgroup.com/ai-code-governance/) is exactly what a production-grade harness is made of and what’s needed to make AI agents reliable enough to trust in production.

## AI coding in 2026: from assistants to agents

Three years ago, a professional developer using AI felt novel; today, it’s expected. As we cited in our [AI boardroom gap report](https://www.softwareimprovementgroup.com/ai-boardroom-gap-2026/), 90% of technology professionals now use AI at work.

And it’s no longer just in start-ups or vibe coders experimenting with this technology. the rapid adoption of AI is also present in the enterprise, according to [A16Z research](https://www.a16z.news/p/ai-adoption-by-the-numbers), almost one-third of the Fortune 500 and one-fifth of the Global 2000 have real enterprise AI deployments in their organizations. That same research also states that the primary enterprise use case of AI, by far, is coding.

And the productivity results are becoming tangible. According to the latest DX report: developers save an average of [3.9 hours per week](https://getdx.com/report/ai-assisted-engineering-Q1-impact-report/) with AI coding tools. That might not sound like a lot, but that’s about 10% on a full-time work week.

That said, AI innovation continues rapidly.

For example, I think many would be surprised that [the well-known term ‘Vibe Coding’ was only introduced in February of 2025](https://en.wikipedia.org/wiki/Vibe_coding). It became Collins Dictionary’s [Word of the Year](https://www.webpronews.com/vibe-coding-how-ais-casual-revolution-conquered-the-dictionary-and-reshaped-tech) before the year was out.

And by 2026, while the world is trying to catch its breath and slowly getting used to AI-coding assistants being able to draft code, suggest fixes, and speeding up routine tasks, the next thing is already here: Agentic AI.

Imagine digital software “workers” that can plan, write, test, and repair code all on their own. AI agent deployment has jumped from [11% to 54% of enterprises](https://kpmg.com/us/en/media/news/q4-ai-pulse.html) in just two years, but the infrastructure to govern what those agents produce hasn’t kept pace.

Which begs the question: if agents can build an entire system in days, what kind of system does it produce? That’s what we looked at i[n another article](https://www.softwareimprovementgroup.com/blog/agentic-ai-works-best-with-human-in-the-loop/). That said, I also think you should treat agents as junior engineers, [Tech Radar Pro](https://www.techradar.com/pro/ai-agents-can-only-be-trusted-as-junior-engineers) recently published my view on that here if you want to read more about it.

This time I want to talk about something related, a new term that might make other terms like prompt engineering and context engineering obsolete: Harness Engineering.

![A visual representation of the harness engineering hores/rider metaphor from the pov of the rider.](images/img_001.jpg)

## What is harness engineering?

Harness engineering is the discipline that closes the gap between deploying agents and governing what they produce.

In simple terms, harness engineering is the practice of designing the full environment that an AI agent operates within: the rules it follows, the checks it must pass, and the feedback loops that prevent the same mistake from recurring.

This might sound overwhelming.

It isn’t.

The quality gates, architecture standards, and governance infrastructure that good software engineering has always required are exactly what a production-grade harness is made of.

### Who coined the term harness engineering?

Mitchell Hashimoto, co-founder of [HashiCorp](https://www.hashicorp.com/en) and creator of [Terraform](https://developer.hashicorp.com/terraform), introduced the concept in February 2026 in a [personal blog post.](https://mitchellh.com/writing/harness-engineering) In his article he described a discipline he’d developed while working with AI agents: every time an agent made a mistake, he engineered a permanent fix into the agent’s environment, so that specific mistake became structurally impossible to repeat.

He called it “engineering the harness.”

Days later, OpenAI engineer Ryan Lopopolo [published a field report that put numbers behind the idea](https://openai.com/index/harness-engineering/). His team had spent five months building a production product with zero manually written lines of code. The codebase reached one million lines, managed across roughly 1,500 automated pull requests. The humans in the room were not writing code. They were designing the environment that made reliable code generation possible. Martin Fowler followed with a [formal taxonomy](https://martinfowler.com/articles/exploring-gen-ai/34-harness-engineering.html). Within weeks, the term had entered the core vocabulary of AI engineering.

### How does harness engineering work?

The formula Hashimoto’s work gave us is simple: **Agent = Model + Harness**.

The model is the raw capability. The harness is everything else: the instruction files that tell the agent how to behave in your codebase, the validation loops that catch bad outputs, the quality checks that prevent known failure modes from recurring.

The horse metaphor captures it well and it’s one that we heard before at Software Improvement Group (SIG).
At SIG’s 2025 SIGNAL event, [Prof. Dr. Catholijn Jonker](https://www.linkedin.com/in/catholijn-jonker-88933b1/), Head of the Interactive Intelligence Group at [TU Delft](https://www.tudelft.nl/ewi/over-de-faculteit/afdelingen/intelligent-systems/interactive-intelligence/people/current-group-members/catholijn-m-jonker) and Professor of Explainable AI at [Leiden University](https://www.universiteitleiden.nl/medewerkers/catholijn-jonker#tab-1), used precisely this image to describe the challenge of hybrid intelligence.

A horse, she argued, is a powerful engine with a mind of its own. You can’t steer it turn by turn, especially in a cutting horse scenario where the animal is reacting faster than any human instruction could follow.

_“It \[a horse\] has an intelligence of its own. If there is suddenly a gap in the floor or something happens, the horse will swerve. It will jump— whatever it needs to do to avoid disaster and you are supposed to stay on it, right? And you have these rains in your hand and your legs to steer the animal in the right direction, right? That’s the idea”_ – Prof. Dr. Catholijn Jonker, [SIGNAL 2025 Keynote: Hybrid intelligence: Building the bridge between human and AI](https://www.youtube.com/watch?v=oWdZ_7ZZg-0&t=232s)

The rider’s job is to design the relationship, set the direction, and stay in control at the right moments.

She wasn’t talking about harness engineering. The term didn’t exist yet. But the principle was the same: an AI agent is a powerful but directionless horse.

Left unattended, it runs fast but veers off course. Run ten simultaneously and the problem multiplies. The harness is the complete set of reins, constraints, and feedback loops that turn a wild horse into a workhorse.

## Why harness engineering matters: the governance gap

AI agent adoption is accelerating faster than most organizations realize. [KPMG’s Q4 2025 AI Pulse Survey](https://kpmg.com/us/en/media/news/q4-ai-pulse.html) found that 54% of organizations are now actively deploying AI agents across core operations; up from just 11% two years ago and 33% in mid-2024. That is nearly a fivefold increase in production deployment in just 24 months.

That speed is what makes governance urgent. Organizations that haven’t built the infrastructure to govern AI-generated code are no longer ahead of the curve but will fall behind. [Gartner put a boardroom number on the problem](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) in June 2025, predicting that over 40% of agentic AI projects would be canceled by end of 2027.

The reasons cited have nothing to do with the technology: inadequate risk controls, unclear business value, and governance gaps that organizations hadn’t built the maturity to close.

The failure pattern at the code level is equally consistent. [A March 2026 survey of 700 enterprise engineering practitioners](https://www.prnewswire.com/news-releases/harness-report-reveals-ai-coding-accelerates-development-devops-maturity-in-2026-isnt-keeping-pace-302710937.html) — conducted by independent research firm Coleman Parkes — found that among teams using AI coding tools at high frequency, 51% reported more code quality problems and 53% reported more security vulnerabilities since adopting those tools.

The agents were producing code faster than the delivery systems could validate it.

This is exactly the topic I recently discussed with Luc Brandts in a recent episode of the SIGNAL podcast.

## Harness engineering vs. prompt and context engineering

These three concepts are regularly conflated. They shouldn’t be.

### Prompt engineering defined

Prompt engineering optimizes individual interactions; phrasing, structure, and examples within a single exchange. It improves the quality of what you ask the model in one turn.

### Context engineering defined

Context engineering manages what the model sees; retrieval, compression, and context window management. It controls the information the model reasons over at any given moment.

### Harness engineering defined

Harness engineering designs the entire world the agent operates in: tools, knowledge sources, validation logic, architectural constraints, feedback loops, memory, and lifecycle management. It governs what the model can do and what it is prevented from doing.

While prompt and context engineering are necessary, they are not sufficient.

When an agent runs autonomously for hours across a codebase, making hundreds of decisions without supervision, individual prompt quality matters far less than the system it operates inside.

[Two engineering teams using the same underlying model can see a 40-point difference in task completion rates based entirely on their harness design](https://harness-engineering.ai/blog/agent-harness-complete-guide/). The gap between top models, by comparison, is typically 1 to 3 points. The model is increasingly a commodity, while the harness will become the differentiator.

## Three harness engineering misconceptions

Setting up a harness is a new initiative. Naturally, there are some common misconceptions floating around. So, before getting into what a mature AI engineering harness looks like, it’s worth clearing up three assumptions that tend to slow teams down before they’ve even started.

### Misconception 1: A good AGENTS.md file is enough

A single markdown file of rules is a useful starting point, but it decays fast. As the system evolves, the file becomes stale. [Field experience shows that static guide files degrade rapidly](https://www.epsilla.com/blogs/2026-03-12-harness-engineering); a mature harness is structured, verifiable, and actively maintained, not a fixed document.

### Misconception 2: Better models mean you need less harness

This is the most dangerous misconception in circulation. Field evidence shows the opposite. Stronger models operating in an under-engineered environment still drift, still accumulate context errors, still hit the same compounding reliability problems. The harness requirement grows with the scope of what you’re asking agents to do. SIG’s own research found that agent-only code scored 1.1/5 on maintainability and 2.2/5 on architecture, while human-in-the-loop code scored 3.1/5 and 4.4/5 respectively. [The difference came down to four factors](https://www.softwareimprovementgroup.com/blog/agentic-ai-works-best-with-human-in-the-loop/): design boundaries, test strategy, dependency hygiene, and scope control. All four are harness properties, not model properties.

### Misconception 3: Guard rails are the same thing as a harness

Guard rails (CI/CD checks, pipeline security scans, quality gates) are the crash barriers on the side of the road. They limit damage when you go off course. The harness is broader. It includes guard rails, but also context engineering: giving AI the right information before it generates anything. Guard rails catch errors after they happen. The harness prevents many errors from happening in the first place.

## How to build an agent harness

A successful agent harness combines artifacts (the things you build) with the practices that use them. Below, I’ve added a handy framework recently made by my colleague [Floris van Leeuwen](https://www.linkedin.com/in/floris-leeuwen/?locale=en), Technical Consultant at Software Improvement Group.

![](images/img_002.png)

Let’s take a deeper look at what this means.

### 1\. Guides

The foundational component most teams start with is a guide file, such as AGENTS.md or CLAUDE.md. These are placed at the root of a repository. [Hashimoto’s own AGENTS.md for the Ghostty terminal project is a documented example](https://mitchellh.com/writing/harness-engineering): each line corresponds to a specific observed failure.

Before an agent generates a single line of code, it needs a shared mental model of the system it’s working in. Guides give AI and the team a way to understand the codebase: architecture docs, code explanations, domain glossaries, and onboarding material. Draft them with AI, verify with humans, and manage them alongside code.

This is the digital equivalent of onboarding a new developer, except it happens at the start of every session.

### 2\. Context engineering

Guides tell the agent what the system is. Context engineering tells the agent what matters for this specific task. That means [functional and non-functional](https://www.softwareimprovementgroup.com/blog/non-functional-requirements-software-quality/) requirements, trade-offs the agent cannot infer from code alone (security vs. usability, for example), and explicit instructions on what should and should not happen.

This is providing the agent with a carrot; you are directing the agent toward the right outcome before it starts.

### 3\. Sensors

Automated checks that flag problems before they reach review. A linter catches a style violation, a type checker flags a mismatch, a security scanner detects a vulnerability — the agent reads the error, corrects the code, and retries within the same session. Where possible, connect sensors in-loop [via MCP](https://www.softwareimprovementgroup.com/mcp/) so feedback is immediate and deterministic.

Our [Sigrid platform](https://www.softwareimprovementgroup.com/sigrid/) is an example of this: rule-based, repeatable analysis that produces the same findings every time, giving agents a reliable signal to correct against.

### 4\. Monitoring

Sensors catch what can be automated. Monitoring catches what sensors miss. Human review, risk-based and calibrated to business criticality, covers misdiagnosed errors, misunderstood instructions, and unnecessary changes.

One specific risk worth flagging: false confidence from AI-assisted review. When both the code and the reviewer are AI-assisted, errors that look correct can slip through.

Robust human control at key checkpoints is the stick that keeps the system in line.

Together, these four components compound over time. Each guide updated, each sensor configured, each context instruction refined improves every future agent session in a way that model upgrades cannot replicate.

## Why software portfolio governance is the harness

SIG has been measuring exactly this for 25 years.

Organizations have always needed a harness around their software development. Before AI, that harness consisted of test departments, procedures, code review, and the four-eyes principle.

These controls existed to make sure what got built was what was needed, and that it met the standards the business required. That harness needs to be stronger, more automated, and more tightly integrated into the development process, as AI moves at a tempo that manual controls cannot match.

When an AI agent produces code, the governance question should be the same one that applies to any code entering a production codebase: is it maintainable? Secure? Consistent with the architecture? Free of the [technical debt](https://www.softwareimprovementgroup.com/blog/what-is-technical-debt/) patterns already identified?

AI amplifies whatever is already in place. Organizations with strong foundations go faster and build better. Organizations with technical debt, poor architecture, and ungoverned portfolios accumulate more problems, a lot more quickly.

Organizations that already govern [code quality at portfolio level](https://www.softwareimprovementgroup.com/use-case/artificial-intelligence/ai-code-governance/) have built the foundation that harness engineering requires. The harness formalizes that foundation for AI-generated output.

The thing is: You cannot design a harness that enforces standards you haven’t defined. And you cannot define standards without visibility into the current state of your portfolio.

Professor Jonker’s framing from the Signal Keynote adds one more dimension. She mentioned how the horse and rider improve together over time. A new horse learns from experienced rider, a new rider learns from experienced horse. That co-evolution is only possible if the relationship is structured enough to be legible.

A governance infrastructure is what makes that feedback loop work at organizational scale: it records what the agent or AI coding assistant did, evaluates it against a defined standard, and feeds the result back into the system.

## How to get started with harness engineering

Harness engineering is not a future concept. The gap between teams that apply it and teams that don’t is already measurable in output quality, error recurrence rates, and the speed at which AI-assisted development scales.

Four starting points worth acting on now:

### 1\. Get visibility first

You cannot govern what you cannot see. Understand the state of your code quality, security posture, and architecture before adding AI to the equation. Visibility comes before acceleration.

### 2\. Build your harness before scaling agents

Don’t adopt agentic workflows without the infrastructure to govern them. Deploy context files, enforcement hooks, and verification gates for one team or system first. Learn before you scale.

### 3\. Wire quality gates into the execution path

Automated checks on security, test coverage, and maintainability should run during and before AI-generated code reaches review. If your governance infrastructure already defines those standards at portfolio level, connecting them to agent output is the natural next step.

### 4\. Measure outcomes, not output

Lines of code generated is not a productivity metric. It is an output metric. Track maintainability trends, security posture changes, and architecture quality alongside commit frequency and merge throughput.

If you want to understand where your codebase stands before you scale, SIG’s [AI code governance page](https://www.softwareimprovementgroup.com/ai-code-governance/) is a good place to start. Or [reach out directly](https://www.softwareimprovementgroup.com/contact/?utm_source=Blog&utm_medium=Blog&utm_campaign=Organic), we work with engineering and IT leaders on solving exactly this problem every day.

## About the author

[![Picture of Werner Heijstek](images/img_003.png)](https://www.softwareimprovementgroup.com/our-authors/werner-heijstek/)

[

#### Werner Heijstek

](https://www.softwareimprovementgroup.com/our-authors/werner-heijstek/)

Werner Heijstek is the Senior Director at Software Improvement Group and host of the SIGNAL podcast, a monthly show where we turn complex IT topics into business clarity.

## Frequently asked questions

### What is harness engineering?

Harness engineering is the practice of designing the full environment an AI agent operates within: the rules it follows, the checks it must pass, and the feedback loops that prevent the same mistake from recurring. It covers everything around the model — context files, enforcement hooks, and verification gates — that turns an unpredictable agent into a reliable one.

### Who coined the term harness engineering?

Mitchell Hashimoto, co-founder of HashiCorp and creator of Terraform, introduced the term in February 2026. His core discipline: every time an AI agent makes a mistake, engineer a permanent fix into the agent’s environment so that mistake becomes structurally impossible to repeat. The formula he gave the field is simple: Agent = Model + Harness.

### What is the difference between harness engineering and prompt engineering?

Prompt engineering optimizes a single interaction — the phrasing, structure, and examples in one exchange with the model. Harness engineering governs the entire environment the agent operates in across every session: the tools it can access, the standards it must meet, and the feedback loops that catch and correct errors in real time. Prompt engineering improves one turn. Harness engineering determines what the agent can and cannot do across all of them.

### What is the difference between harness engineering and context engineering?

Context engineering manages what the model sees at any given moment — retrieval, compression, and context window management. It is one component of the harness. Harness engineering is broader: it includes context engineering, but also enforcement hooks that block non-compliant output and verification gates that require empirical proof before a task is marked complete.

### What does a harness engineering setup look like in practice?

Most teams start with a guide file — typically AGENTS.md or CLAUDE.md — placed at the root of a repository. It contains coding standards, project structure, and a growing list of anti-patterns based on observed agent failures. From there, a production-grade harness adds enforcement hooks (linters, type checkers, security scanners that block non-compliant output in real time) and verification gates (passing test suites, successful builds, security scans required before any task is marked complete).

### Do better AI models reduce the need for a harness?

No. This is one of the most common misconceptions in the field. Stronger models operating in an under-engineered environment still drift, accumulate context errors, and repeat the same failure patterns. SIG’s own research found that agent-only code scored 1.1/5 on maintainability regardless of model used, while human-in-the-loop code with governance infrastructure in place scored 3.1/5. The gap came down to four harness properties: design boundaries, test strategy, dependency hygiene, and scope control — not model capability.

### What is an AGENTS.md file?

An AGENTS.md file is the foundational component of a harness. It sits at the root of a repository and tells the agent how to behave in that codebase: project structure, build and test commands, coding conventions, and a list of anti-patterns the team has identified from previous agent sessions. It grows incrementally — one rule added each time an agent repeats a mistake. Mitchell Hashimoto’s own AGENTS.md for the Ghostty terminal project is a well-documented public example of this discipline in practice.

### How does software quality governance relate to harness engineering?

In a way, they are the same thing, applied to AI-generated code. The quality gates, security checks, architecture standards, and maintainability requirements that organizations apply to production code are not separate from the harness — they are the harness. Organizations that already govern code quality at portfolio level have built the foundation harness engineering requires. The harness formalizes that foundation for AI-generated output. You cannot design a harness that enforces standards you haven’t defined, and you cannot define standards without visibility into the current state of your portfolio.