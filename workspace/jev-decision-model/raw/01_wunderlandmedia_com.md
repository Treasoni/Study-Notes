---
url: "https://wunderlandmedia.com/jev-not-deterministic-732-decisions-three-runs"
title: "Jev Is Not Deterministic (I Measured It) | Wunderlandmedia"
scraped_at: 2026-09-20T15:10:07+00:00
---

[Wunderlandmedia](https://wunderlandmedia.com/)Close menu
[ 01.Web Development ](https://wunderlandmedia.com/services/web-development)[ 02.SEO Consulting ](https://wunderlandmedia.com/services/seo-consulting)[ 03.AI Consulting ](https://wunderlandmedia.com/services/ai-consulting)[ 04.Portfolio ](https://wunderlandmedia.com/portfolio)[ 05.About ](https://wunderlandmedia.com/about)[ 06.Blog ](https://wunderlandmedia.com/blog)
# I Ran the Same 732 Decisions Through Jev Three Times. It's Not Deterministic.
### Three runs of 732 Jev decisions: only 24 percent came back identical. What the drift actually costs you, and where a threshold belongs.
Kemal Esensoy·Modified on September 19, 2026
Artificial Intelligence
TypeSafe says Jev is stable across runs. I believed it. I wrote it into a document I was going to put in front of clients, as one of the three properties that make the model worth building on.
Then I spent six cents checking. Jev is not deterministic, and the sentence I had written said it was.
It is close enough to true that the document still stands. But the difference between what I wrote and what I measured is exactly the difference between a claim a client can catch you on and a claim that survives them checking. So here is the whole thing: what I ran, what moved, what it cost me, and where I would put a threshold now.
## What I actually ran
My blog has 183 published posts. I have a small script, `bin/jev`, that sends every one of them to Jev with the same four questions attached: is there real first-hand experience in this, does it read machine-written, does the meta description give anyone a reason to click, does the title lead with the words people actually search for.
That is 732 separate judgements. One run took **20.1 seconds** at eight parallel requests, burned 445,794 input tokens, and cost **$0.0187**. Output tokens are free, because there is no output. Jev writes nothing at all, it returns numbers.
The reason that matters to me is that the old version of this job was reading a sample of eight posts by hand during [an SEO audit](https://wunderlandmedia.com/ai-seo-audit-workflow) and hoping the other 175 were fine. At under two cents for the whole archive, sampling stopped being a thing I had to defend.
If you want the boring-but-important part about who owns what you send it, I went through [all four of Jev's legal documents](https://wunderlandmedia.com/typesafe-ai-jev-terms-of-service-gdpr) separately.
## Only 24 percent of the answers came back identical
I ran the same 732 decisions three times and diffed them.
177 answers were bit-identical across all three runs. That is 24 percent. The other 555 moved.
Before you close the tab: they did not move much.  
| Drift between runs  | Value  |  
| --- | --- |  
| Median  | 0.010  |  
| p90  | 0.030  |  
| p99  | 0.050  |  
| Worst case anywhere  | 0.070  |  
Seven hundredths, across 732 decisions, as the single worst thing that happened. The flagged-post count came out 56, 56, and 57.
So Jev is not deterministic in the sense I had claimed, and "the same input gives the same answer" is wrong. "The same input gives an answer within about a tenth" is right, and it is the version I should have written down. A model that returns 0.72, then 0.68, then 0.71 is not unreliable. It is a measurement with an error bar, and I had been treating it as a lookup table.
## The wobble lives in the middle of the range
A post scoring 0.03 on first-hand experience came back 0.03 in all three runs. A post scoring 0.72 came back 0.68 in the next one. The drift is not spread evenly, and that turns out to be the useful part.  
| Where the answer sat  | Mean drift  |  
| --- | --- |  
| Under 0.15  | 0.004  |  
| 0.15 to 0.40  | 0.018  |  
| 0.40 to 0.70  | 0.020  |  
| 0.70 to 0.85  | 0.016  |  
| Over 0.85  | 0.007  |  
When Jev is sure, it barely moves. The confident ends of the scale are effectively frozen, at both ends.
Everything that wobbles sits in the middle, where the model has not made up its mind. Which is the behaviour you would want if you designed it on purpose: the uncertainty shows up as movement, in the same place the model is already telling you it is uncertain.
## Twelve decisions flipped, and ten of them were my fault
Of 732 decisions, **12 crossed a threshold and changed the verdict** between runs. Drift costs you nothing until it crosses a line you care about, and twelve is the number of times it did.
Twelve out of 732 is 1.6 percent, and I would have shrugged at that number if I had not looked at which twelve.
Ten of the twelve were the same question: `slop_shapes`, my "does this read machine-written" check, with the cutoff at 0.70.
That cutoff is sitting in the worst possible place. The `slop_shapes` scores across my archive run from 0.36 to 0.85 with a median of 0.55, so the distribution is one compressed lump and 0.70 lands inside the thick part of it. Dozens of posts sit within 0.03 of the line. A drift of 0.02 tips a handful over every run, and the flip rate I measured is not the model being flaky, it is me having drawn the line through a crowd.
The other two cutoffs, both at 0.40, sit in a gap between two clusters. They produced one flip each.
**Put the threshold in a valley, not in a crowd.** Look at the actual distribution of your scores before you pick a number, and if the histogram has a dip in it, that dip is where the cutoff goes. This is not a Jev thing. It is true of any scored classifier, and I had simply never had to think about it before, because I had never had 183 scores to look at.
## Tight is a better promise than deterministic
Here is what I changed in the client document.
Out: "It is deterministic. The same input gives the same answer."
In: movement under a tenth is noise, movement over it is a finding.
The second one is a worse marketing line and a much better thing to sell, for three reasons that all point the same way. A client who checks will find the first claim is false, and there goes the rest of your credibility in that meeting. The second claim gives them something to act on, because a contract dimension going from 0.2 to 0.7 across a revision is now unambiguously real, and a dimension that moved 0.03 is unambiguously not. And "here is the error bar" is the sentence a technical buyer has been waiting to hear from anyone selling them AI, which is most of [what their LinkedIn feed is not telling them](https://wunderlandmedia.com/ai-myths-your-linkedin-feed-keeps-repeating).
You still cannot do this with a generative model. Ask an LLM to compare two contract versions twice and you get two different essays, and there is no arithmetic you can perform on an essay. The whole reason to reach for a scoring model is that 0.7 minus 0.2 is a number your alerting can read.
## What this changes about what you would build
Nothing on my list died. The delta-based products got sharper, because now I know what size of delta counts.
The thing I would build first, and the thing I would suggest you build first, is a gate. You already send a pile of things to an expensive model. Screen all of them for a fraction of a cent, and only let the survivors through. It cuts a bill somebody is already paying, which makes it the easiest version of this conversation you will ever have.
After that, roughly in order of how hard they are to deliver:
  * **Triage.** Route inbound enquiries, score every review instead of a quarterly sample, check every draft against the brand voice rules nobody follows.
  * **Monitoring and absence detection.** Score a contract, score its next revision, alert on the gap. Or run one yes-or-no question per tender requirement against your draft response, and ship the list of zeros. Absence is the thing generative models are worst at, because they will confidently tell you the response is comprehensive.
  * **Trajectory.** Churn shows up in the slope of support sentiment weeks before it shows up in a cancellation. This one needs the stability, and now I know how much of it I have.
  * **Your own engineering.** A risk score on every pull request, on-call alerts deduplicated before they page anyone, a regression suite for your own prompts that does not drift while you are trying to measure whether your prompt drifted.


That last group is where I would start if you want to feel it yourself this week. No procurement, no client, and you already own the data.
## Where I would not point it
Some of this I knew going in and some of it I found by being wrong.
It does not do arithmetic. It does not compare dates, because it reads them as text rather than as ordered quantities. Extract the pieces with it, then do the comparison in code. It is not hardened against text written to manipulate a verdict, so anything a stranger typed is data and never instructions. It generates nothing, so a chatbot built on it is a category error rather than a limitation. And for one document, read once, a person is fine. The value is in volume, or in the same question asked repeatedly over time.
The failure mode worth naming is the one I nearly shipped: treating a cheap judgement as a free judgement and wiring it into something that did not need judging at all. Half of what gets sold as AI automation is [a cron job with a model bolted to it](https://wunderlandmedia.com/ai-automations-expensive-cron-jobs), and a decision model makes that mistake cheaper to make, not harder.
## The part I have not measured
I have run the screening side properly, 183 posts, three times, numbers above. The gate in front of a live production LLM I have not built or measured yet, so the cost saving I described is reasoning, not a result. When I have run it, I will publish whatever it says, including if it says the gate was not worth the wiring.
The other thing I would do differently: I calibrated my thresholds against one run before I knew any of this. All four of them came out of a single pass over the archive. Two of them landed fine by luck, and one of them landed in a crowd. If you are setting up something similar, run it three times first and look at the spread before you pick a single number.
I build this kind of thing for clients at [wunderlandmedia.com](https://wunderlandmedia.com), usually starting with a backfill over whatever archive they are already sitting on, because a chart of the last two years sells the monitoring subscription better than any deck I could write.
Find these posts useful? Mark Wunderlandmedia as a preferred source on Google — my articles will then show up more often in your Search results, AI Overviews and AI Mode.
[Set as preferred source](https://www.google.com/preferences/source?q=wunderlandmedia.com)
### About the Author
#### Kemal Esensoy
Kemal Esensoy, founder of Wunderlandmedia, started his journey as a freelance web developer and designer. He conducted web design courses with over 3,000 students. Today, he leads an award-winning full-stack agency specializing in web development, SEO, and digital marketing.
Jev Is Not Deterministic (I Measured It) | Wunderlandmedia
