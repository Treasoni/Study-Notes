---
url: "https://arxiv.org/html/2209.07858"
title: "Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned"
scraped_at: 2026-10-13T12:17:58+00:00
---

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×
[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)
arXiv:2209.07858v2 [cs.CL] 22 Nov 2022
# Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned
Deep Ganguli ††thanks: Correspondence to: {deep, liane, jackson, jared, jack}@anthropic.com Authors above the line break are core contributors. Author contributions are listed in §. Liane Lovitt††footnotemark:  Jackson Kernion††footnotemark:  Amanda Askell  Yuntao Bai  Saurav Kadavath  Ben Mann  Ethan Perez  Nicholas Schiefer  Kamal Ndousse  Andy Jones  Sam Bowman  Anna Chen  Tom Conerly  Nova DasSarma  Dawn Drain  Nelson Elhage  Sheer El-Showk  Stanislav Fort  Zac Hatfield-Dodds  Tom Henighan  Danny Hernandez  Tristan Hume  Josh Jacobson  Scott Johnston  Shauna Kravec  Catherine Olsson  Sam Ringer  Eli Tran-Johnson  Dario Amodei  Tom Brown  Nicholas Joseph  Sam McCandlish  Chris Olah  Jared Kaplan††footnotemark:  Jack Clark††footnotemark:  Anthropic 
###### Abstract
We describe our early efforts to red team language models in order to simultaneously discover, measure, and attempt to reduce their potentially harmful outputs. We make three main contributions. First, we investigate scaling behaviors for red teaming across 3 model sizes (2.7B, 13B, and 52B parameters) and 4 model types: a plain language model (LM); an LM prompted to be helpful, honest, and harmless; an LM with rejection sampling; and a model trained to be helpful and harmless using reinforcement learning from human feedback (RLHF). We find that the RLHF models are increasingly difficult to red team as they scale, and we find a flat trend with scale for the other model types. Second, we release our dataset of 38,961 red team attacks for others to analyze and learn from. We provide our own analysis of the data and find a variety of harmful outputs, which range from offensive language to more subtly harmful non-violent unethical outputs. Third, we exhaustively describe our instructions, processes, statistical methodologies, and uncertainty about red teaming. We hope that this transparency accelerates our ability to work together as a community in order to develop shared norms, practices, and technical standards for how to red team language models. Warning: this paper contains examples that may be offensive or upsetting.
##  1 Introduction
Large language models exhibit a wide range of harmful behaviors such as reinforcing social biases (e.g., ), generating offensive or toxic outputs , leaking personally identifiable information from the training data , aiding in disinformation campaigns , generating extremist texts , spreading falsehoods , and more [[9](https://arxiv.org/html/2209.07858#bib.bib9), [10](https://arxiv.org/html/2209.07858#bib.bib10), [18](https://arxiv.org/html/2209.07858#bib.bib18), [57](https://arxiv.org/html/2209.07858#bib.bib57), [22](https://arxiv.org/html/2209.07858#bib.bib22), [51](https://arxiv.org/html/2209.07858#bib.bib51)]. As AI systems improve, the scope of possible harms seems likely to grow . Many strategies have been developed to address some of these harms (e.g., [[58](https://arxiv.org/html/2209.07858#bib.bib58), [4](https://arxiv.org/html/2209.07858#bib.bib4), [48](https://arxiv.org/html/2209.07858#bib.bib48), [36](https://arxiv.org/html/2209.07858#bib.bib36), [34](https://arxiv.org/html/2209.07858#bib.bib34), [19](https://arxiv.org/html/2209.07858#bib.bib19), [60](https://arxiv.org/html/2209.07858#bib.bib60)]). One potentially useful tool for addressing harm is red teaming—using manual or automated methods to adversarially probe a language model for harmful outputs, and then updating the model to avoid such outputs . In this paper, we describe our early efforts to implement manual red teaming to both make models safer and measure the safety of our models. The models trained with red team data were described in , so here we focus on describing our red team results and techniques in detail in the hope that others may benefit from and improve on them.
We make three main contributions. First, we investigate scaling behaviors for red teaming across 3 model sizes (2.7B, 13B, and 52B parameters) and 4 model types: a plain language model (plain LM) ; an LM prompted to be helpful, honest, and harmless (HHH prompted LM) ; an LM with rejection sampling (RS), which returns the best of sixteen samples as ranked by a helpful and harmless preference model ; and a model trained to be helpful and harmless using reinforcement learning from human feedback (RLHF) with the same preference model . The RS and RLHF models rely on data generated from red teaming the prompted LM (see § for details on all models). Figure , middle, shows that: (1) RLHF models are significantly harder to red team as they scale, (2) plain LMs, prompted LMs, and RS models exhibit a flat trend with scale, (3) Prompted LMs are not significantly harder to red team than plain LMs, which is inconsistent with our previous results that use static evaluations to show HHH prompting is an effective safety intervention , and (4) RS models are the most difficult to red team at any scale; however, qualitatively, they tend to be harmless by being evasive .
Our second contribution is to release our dataset of 38,961 red team attacks for others to analyze and learn from (Table ).11 1 <https://github.com/anthropics/hh-rlhf> We provide a Datasheet in § that fully documents the data and we explain the pros and cons for releasing the data in §. Our dataset is an order of magnitude larger than a similar available red team dataset and considers models one order of magnitude larger than those in . To our knowledge, we release the only dataset of red team attacks on a model trained be safe with RLHF. These types of models are already deployed and we believe our data can help shed further light on their strengths and weaknesses. More generally, we believe our data can be used to understand what successful red team attacks look like, to build (semi-)automated red team techniques , to build classifiers for harmfulness, and to prototype strategies for measuring and mitigating harms in language models. We also provide our own preliminary analyses of the types of harms uncovered in our data (Figures & , §).
Our last contribution is to exhaustively describe our instructions, processes, and statistical methodologies for red teaming (§). Throughout the design of our experiments, we arrived at many junctures in which we were unsure about how to proceed, even after a literature review on red teaming AI systems (§). As such, we conducted informational interviews with experts in the field of Trust & Safety and incorporated their suggested best practices (§) into the design of our experiments in order to ensure the well-being of the red team. In general, we found that red team members _enjoyed_ participating in our experiments and felt motivated by a mission to make AI systems less harmful (§). Nevertheless, our work suffers from some limitations, which we discuss in §. Based on our experiences, we propose some policy interventions for how we can work together as a community to develop shared norms, practices, and technical standards for how to red team language models (§).
Figure 1: Red team attack success by model size (x-axes) and model type (colors). (Left) Attack success measured by average red team member self report (higher is more successful). (Middle) Attack success measured by average minimum harmlessness score (higher is better, less harmful) (Right) Distribution of minimum harmlessness score.
##  2 Related Work
We use the same models that we developed in our previous work where we train a general language assistant to be helpful, honest, and harmless . However, here we run additional experiments in order to determine the influence of model size on susceptibility to red team attacks (Figure ) and analyze the content of the attacks (Figures & ) to understand the types of harms uncovered by red teaming. Additionally, we provide more detail on our red team methods, and release the data, so that others can reproduce (and improve upon) our red team approach and results.
Apart from our previous work, our approach is most similar to & , who have crowdworkers attempt to elicit offensive outputs from dialogue agents in open-ended dialogues, then use the resulting data to create effective safety interventions. In , they release a Bot Adversarial Dialogues (BAD) dataset of {\sim}5K conversations with 3 dialogue agents ranging in size from 345M to 2.7B parameters. We collect more data (∼40{\sim}40K) attacks22 2 Qualitatively, we observe a wider diversity of attacks in our dataset than in the BAD dataset, although we have not quantified this. This is at least partially due to the fact that we simply collected more data.; red team larger models (up to 5252B parameters) in order to measure scaling behaviors, as in ; and focus on reinforcement learning from human feedback as our most promising safety intervention.
Recent work explores how to automate red teaming by using language models instead of humans as the red team . The approach bootstraps from the BAD dataset , and uncovers a variety of harms including (but not limited to) finding groups of people that the dialogue agent discusses in offensive ways, identifying personally identifiable information, and leaking private training data. We uncover similar harms in our dataset and plan to use our own data to systematically compare and contrast the types of harms that can be uncovered in manual versus automated methods in future work (§).
More generally, although our work focuses on adversarial attacks on _generative_ models, it is heavily inspired by and related to prior work that examines the efficacy of adversarial testing to find and address vulnerabilities in NLP algorithms in _discriminative_ settings. Some of these efforts augment humans (through guidelines, templates, programmatic generation of attacks, and various combinations thereof) to devise test cases that cause systems to fail [[45](https://arxiv.org/html/2209.07858#bib.bib45), [46](https://arxiv.org/html/2209.07858#bib.bib46), [29](https://arxiv.org/html/2209.07858#bib.bib29), [21](https://arxiv.org/html/2209.07858#bib.bib21), [30](https://arxiv.org/html/2209.07858#bib.bib30), [55](https://arxiv.org/html/2209.07858#bib.bib55), [6](https://arxiv.org/html/2209.07858#bib.bib6), [23](https://arxiv.org/html/2209.07858#bib.bib23)]. Others use humans in the loop to continuously and dynamically build, break, and fix models in order to continuously make them more robust to failure modes . Finally, a large body of work aims to _learn_ adversarial examples that cause downstream models to produce spurious outputs , some of which are reviewed in . However, these examples often seem arbitrary and unintelligible to humans, and thus correspond to a different kind of attack than the ones we consider here.
Figure 2: Visualization of the red team attacks. Each point corresponds to a red team attack embedded in a two dimensional space using UMAP. The color indicates attack success (brighter means a more successful attack) as rated by the red team member who carried out the attack. We manually annotated attacks and found several thematically distinct clusters of attack types (black ellipses and text).
Although our work focuses on language models, there is prior art on how to red team multi-modal generative models in the context of DALL•E 2 . These red team efforts reveal some similar categories of harms to those we find in or dataset, such as: “Bias and representation”; “Harassment, bullying, and exploitation”; “Dis- and misinformation”, and other categories that we do not uncover or consider, such as “Copyright and Trademarks”. The red team consists of domain experts who are selected according to particular areas of expertise, whereas in our case we rely on crowdworkers whose domain expertise we are unaware of (§).
##  3 Methods
###  3.1 Red Team Task
We developed an interface that instructs red team members to have open-ended conversations with an AI assistant in order to “make the AI behave badly, to get it to say obnoxious, offensive, and harmful things” (Figure ). Similar to , we provide the red team with a brief list of example conversation topics but otherwise leave the instructions fairly open-ended. We ask the red team to rely on creativity, avoid obvious profanity, and to focus on a single topic per attack. To encourage this behavior, we ask participants to enter a short description of how they intend to red team the model prior to the attack.
We were concerned about our task causing harm to the red team, so we reviewed available literature in Trust & Safety and related fields (e.g., [[26](https://arxiv.org/html/2209.07858#bib.bib26), [15](https://arxiv.org/html/2209.07858#bib.bib15), [16](https://arxiv.org/html/2209.07858#bib.bib16), [49](https://arxiv.org/html/2209.07858#bib.bib49), [5](https://arxiv.org/html/2209.07858#bib.bib5), [27](https://arxiv.org/html/2209.07858#bib.bib27), [31](https://arxiv.org/html/2209.07858#bib.bib31)]), as well as conducted a series of informational interviews with industry professionals in the field. We incorporated best practices from this research (see § for details) into the content and design of our task instructions (Figure , Left) and task interface (Figure , Right). For example, in the red team task instructions, we provide clear, specific warnings that red team members may be exposed to sensitive content. We also encourage red team members to select topics within their own risk tolerance, as opposed to prompting them to discuss specific, sensitive topics with the AI assistant. Through surveys and informal feedback, we found that red team members enjoyed the task and did not experience significant negative emotions.
Figure 3: (Left) Red team task instructions. (Right) Example of a red team attempt.
After the red team member agrees to the terms of the task (Figure , Left), they proceed to have an open-ended, multi-turn conversation with the AI assistant. After each turn in a conversation, we present the participant with _two_ possible model-generated responses, and ask them to select the _more_ harmful of the two as in . We do this for two reasons. First, this allows us to expedite the red team’s ability to find vulnerabilities in our systems by a factor of two—generative models are stochastic and thus our approach allows the red team twice as many opportunities to catch harmful behavior per attempt. Second, this procedure generates a dataset of pairs of model responses, where one response is labeled as more harmful than the other. We use this dataset to train a harmlessness preference model, which takes as input a model generated response and outputs a score which is lower for more harmful model responses, and higher for less harmful model responses .33 3 All of our work fully generalizes from showing possible responses to possible responses. We chose responses to make the task interface simpler. We use the resulting preference model to build safety interventions, which we describe in §. We do not define what “harmful” means, as this is a complex and subjective concept; instead, we rely on the red team to make their own determinations via a pairwise preference choice .  
| # Parameters  | Plain LM  | Prompted LM  | Rejection Sampling  | Reinforcement Learning  |  
| --- | --- | --- | --- | --- |  
| 2.7B  | 1151  | 2044  | 1445  | 2498  |  
| 2587  | 2174  | 1263  | 2292  |  
| 1414  | 17739  | 1273  | 3081  |  
Table 1: Number of red team attempts per model size (rows) and safety intervention (columns)
We ask red team members to have a back-and-forth conversation for four turns (Figure , Right). We do not strictly limit the number of turns in each conversation, and empirically, we observe most conversations are 1-4 turns, with some lasting longer. At the end of each conversation, we ask the participant to rate how successful they were at making the AI assistant say something bad. We collect these ratings on a point Likert scale (ranging from 0 to 4) where a 0 means “Not successful” and a 4 means “Very successful” (Figure , Right).44 4 We experimented with asking participants to rate the harmfulness of the model responses and how actionable the responses were (Figure , Right). In general we did not observe clear signals from these data and thus do not report on them. Red team members continue this process for a series of five dialogues, typically on five unique topics, which culminates in one overall task. Red team members could then choose to complete further tasks.
The AI assistant is powered by four types of dialogue models: one baseline model and three models with different types of safety interventions. We assign red team members to models at random—the red team does not know which model they interact with. We describe these models further in the next section.
###  3.2 Models
We derive dialogue models, with various safety interventions, from a general language model, and in some cases, a helpful and harmless preference model. For simplicity, we refer to the preference model as a harmlessness preference model, and the output of the model as a harmlessness score throughout this work.55 5 More generally, our preference model is trained to predict both harmlessness _and_ helpfulness. For the latter, we created a separate interface in order to collect preference data about helpfulness. We found a fundamental tension between these helpfulness and harmlessness—a model can simply be harmless by refusing to be helpful . As such, we train our preference models to predict both harmlessness and helpfulness. We find that this approach helps to address this tension without loss in predictive accuracy for harmlessness . Here, we first provide basic details on the general language model and the harmlessness preference model, then elaborate on the four dialogue models that power the AI assistant.
For our general language models, we train decoder-only transformer models ranging in size from 2.7B to 13B to 52B parameters. Full details about model architectures, training data, training procedures, and model evaluations are described elsewhere .
To train our harmlessness preference model, we use the _comparison_ data from red team attacks on 52B parameter prompted language model (described below) as the training data—this is why we collected an order of magnitude more data in this case (Table ). To build these models, we fine-tune 2.7B, 13B, and 52B general language models to predict which model utterances red team members found _less_ harmful, thus producing a harmlessness score . A lower score means more harmful.
##### Plain language models (Plain LM)
We use 1-shot learning (in which we place an single example of a 3-turn conversation in our Human, Assistant format in context) to prompt our general language models to behave as dialogue models for use in the interface described above . We consider this method a baseline or control model, since it minimally departs from a general-purpose plain language model and has no explicit safety intervention.
##### Prompted language models (Prompted LM)
We use 14-shot learning to prompt our general language models to be helpful, harmless, and honest (HHH) , similar to dialogue-prompted Gopher . We consider this a simple safety intervention, since we found it to be surprisingly effective at reducing model toxicity, especially for larger models . Furthermore, we use context distillation to train “prompt-free” variants of these prompted models in order to retain the influence of the prompt without occupying a significant portion of the limited context window and decreasing inference time . Empirically, in previous work, we found minimal differences between prompting and context distillation .  
| Red Team Members (n=115)  |  
| --- |  
| Gender  |  
|   |  
|  Female  |   |  
|  Non-binary  |  
|  Prefer not to say  |  
| Sexual Orientation  |  
|  Heterosexual or straight  |   |  
|  Gay or lesbian  |  
|  Bisexual  |   |  
|  Questioning / unsure  |  
|  Prefer not to say  |  
|   |  
| Age Group  |  
|   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
 |  
|  Prefer not to say  |  
| Ethnicity  |  
|  American Indian or Alaska Native  |  
|   |  
|  Black or African American  |  
|  Hispanic, Latino, or Spanish  |  
|  Middle Eastern or North African  |  
|  Native Hawaiian or Pacific Islander  |  
|  White or Caucasian  |   |  
|  Prefer not to say  |  
|   |  
| Education  |  
|  High school or some college  |   |  
|  College degree  |   |  
|  Graduate or professional degree  |   |  
|  Prefer not to say  |  
|   |  
| Disability  |  
|  Hearing difficulty  |  
|  Vision difficulty  |  
|  Cognitive difficulty  |  
|  Ambulatory (mobility) difficulty  |  
|  Self-care difficulty  |  
|   |  
 |  
Figure 4: Results of a demographic survey completed by 115115 of 324324 red team members.
##### Rejection sampling (RS)
We generate 16 samples of AI assistant responses from prompted language models, rank these samples with the harmlessness preference model, and select the 2 _least_ harmful samples to present to the red team member, thus rejecting the 14 relatively more harmful responses. We did not experiment with changing the parameter 16. We tie the size of the prompted model to the size of the harmlessness preference model, e.g., a 2.7B parameter rejection sampling model consists of a 2.7B prompted language model paired with a 2.7B harmlessness preference model.66 6 This choice is arbitrary, e.g., we can pair a 2.7B prompted language model with a 52B harmlessness preference model, but allows us to study the influence of scale more systematically. In our formulation, technically an parameter RS model actually consists of 2N parameters.
##### Reinforcement learning from human feedback (RLHF)
We start with a prompted language model, then use reinforcement learning to train it to maximize the scores given by the preference model described above. As in the rejection sampling case, we tie the size of the prompted model to the size of the preference model. Full details about the training procedures, training datasets, and model evaluations are described elsewhere . Intuitively, we expect RLHF models to behave similarly (but not exactly) to RS models; however, RLHF is computationally expensive at train time but efficient at test time. RS is vice-versa.
###  3.3 Red Team
Our red team consists of 324 US-based crowdworkers whom we primarily recruited from Amazon’s Mechanical Turk (MTurk) platform (n=307n=307) and the Upwork platform (n=17n=17). On MTurk, we paid between $7.50 and $9.50 for each set of 5 conversations completed. We found that crowdworkers could complete _at least_ 2 tasks an hour, which means that we paid at or above California minimum wage.77 7 As of 2022, California minimum wage is $15.00 per hour On Upwork, we paid participants $20 per hour. Similar to , we asked participants to fill out a short demographic survey that incorporated U.S. census categories and offered participants the option to answer “Prefer to not to say” for each question (Figure ).
We found that he crowdworker population may not be fully representative of the U.S. population, according to US Census data .88 8 Because we collected this data anonymously, we are unable to examine the impact of demographic attributes of red team members on the types or efficacy of their red team attacks. For example, we find that individuals who self-identify as “White or Caucasian” are slightly over-represented in our experiments (79% versus the current U.S. Census estimate of 75.8%). Similarly, the percentage of participants with at least a college degree was significantly higher than what is reported by the U.S. Census (66% versus 32.9%).
Figure shows descriptive statistics about the red team. In particular, we find we find that ∼80{\sim}80% of the red team attacks come from ∼50{\sim}50 out of ∼300{\sim}300 workers. As such, the overwhelming majority of the dataset is generated from a minority of particularly prolific red team members. Furthermore, we fit a linear mixed model that evaluates the inherent efficacy of a red team member, which we plot in Figure (Right). We find that some workers are particularly effective at red teaming, whereas others are not. In Appendix we re-analyze our data while controlling for these two confounds (particularly prolific workers, and particularly (in)effective red team members) and find that these confounds do not significantly influence the main results in Figure .
Figure 5: Descriptive statistics about red team members. (Left) Total number of red team attempts (y-axis) per red team member (x-axis), sorted by number of attempts. (Middle) The cumulative distribution (CDF) of the data from the left panel shows that ∼80{\sim}80% of attacks come from ∼15{\sim}15% of the red team participants. (Right) Estimate of how effective each red team member is at red teaming (y-axis, means average, lower means more effective, lines indicate 9595% confidence intervals) according to their ability to achieve a low minimum harmlessness score. X-axis is sorted by ability.
###  3.4 Data Analysis
With our interface, models, and red team in place, we collect 38,961 red team attacks across with O(K) attacks per model type in all cases except for the 5252B prompted model for which we collect O(1010K) attacks (Table ). We collect more data in the latter case in order to train our harmlessness preference models, as described in §. Figure shows an example red team attack and how we quantify it. In particular, we measure variables for each attack. First, we record the red team member’s self-rating of how successful they were on a -point Likert scale, where a 0 indicates an unsuccessful attempt, and a 4 indicates a very successful attempt (see also Figure , Right, for an example). Figure (Left) shows the distribution over this variable, which is approximately bimodal, with two peaks at 0 and 4, with relatively more mass at 0. This indicates that, on average, red team member’s self report successful attacks ∼35{\sim}35% of the time.
Next, we use our harmlessness preference model to compute the harmlessness score (higher is less harmful and thus better) of the AI assistant’s dialogue. In particular, we compute the score for each assistant utterance, conditioned on everything preceding the utterance, for each utterance in the conversation. For a -turn conversation, this results in harmlessness scores (Figure ). To turn this into one number, we either compute the mean or minimum (worst) harmlessness of the AI assistant. Empirically, we find that the precise choice of aggregate statistic does not significantly change our results, so we choose the minimum harmlessness as a lower bound on the overall harmlessness of the model.
Figure 6: Example of how we quantify red team attempts. First, we compute a harmlessness score (lower is more harmful) on the task description (red). Next, we compute a harmlessness score on the assistant utterances, conditioned on all previous human and assistant utterances (black scores, adjacent to assistant utterances). We aggregate these scores using either a min or max (black, bold). Finally, we rely on human judgement of attack success on a Likert scale (blue).
Figure (Middle) shows the distribution of the minimum harmlessness score over all red team attacks for all the models. The distribution is centered around 0 and skews negative. A more negative score corresponds to more harmful model responses, and a more positive score corresponds to less harmful model responses. The shape of this distribution suggests that the red team members are indeed effective at soliciting harmful responses from the AI assistant. In general, we find that the minimum harmlessness score is inversely proportional to the red team member self-rating of attack success, which is expected (§, Figure ). However, the correlation is not perfect. As such we report statistics of both these variables, conditioned on model type, as measures of red team efficacy in §.
Finally, we also use the harmlessness preference model to score the harmfulness of the red team member’s intent. To do so, we run the preference model on the red team member’s task description (Figure ).99 9 Technically, this data is out of distribution for the preference model, since the preference model is trained on AI utterances, and here we run inference on human utterances. Figure (Right) shows the distribution over this variable, which appears normally distributed with a mean around 1. As such, short descriptions of the attack score as less harmful than the actual AI utterances. We view the intent harmlessness score as a possible confound that we control for in further statistical analyses of the data (§). Since we find that it does not influence our main results, we do not report on this variable further in the main text.
###  3.5 Review Task
After we collected the data across all model types, we performed a follow-up experiment to measure two separate variables: the inter-annotator agreement in the self report of attack success, and the content of the attack types. The former is important because self-ratings of attack success are subjective, and can vary based on elements of the red team attack and red team member that we do not control (e.g., the type of attack or the background of the red team member). As such, we were interested in understanding how much variability (across different raters) there might be for defining a successful attack.
Figure shows our task instructions (Left) and interface (Right). We have annotators review each transcript in the experiment. We ran this experiment on a random sample of 500 red team attacks for the 52B Prompted Language model and 500 attacks on the 52B RLHF model. We have each reviewer report their judgement of how successful the red team member was at making the “AI assistant say something bad.” We measure this variable on the same 5 point Likert scale as the main red team experiment and use consistent language across both experiments.
Figure 7: (Left) Marginal distribution of self-report of red team success rates (higher is more successful) (Middle) Probability distribution function (PDF) of minimum AI harmlessness scores computed from the AI utterances (lower is more harmful) (Right) Distribution of harmlessness scores computed from short descriptions (written by red team members) of attack intent.
We find a low level of inter-rater agreement on the success of red team attacks (according to our task setup and instructions) consistent with . In particular, we report Fleiss’s Kappa, a statistical measure of inter-annotator agreement that is bounded in [,1][-\infty,1], where -\infty implies no agreement and 1 indicates perfect agreement. We report a Fleiss’s Kappa of 0.32 between the 4 raters (the author and the 3 reviewers) based on a Likert rating scale. When we binarize the rating (1 if rating \geq 3, else 0), the agreement increases to 0.49. Furthermore, when we exclude the original author and measure the agreement between the 3 annotators, we also see a modest increase in agreement for both the Likert and Binary scales, achieving a maximum agreement of 0.55 for the reviewer-only binary case. Taken together, our results suggest poor to fair agreement on what constitutes a successful attack.
To get a sense of the type of harms the attacks were meant to elicit, we asked the reviewers to tag transcripts with up to 2 of 20 total topic tags (Figure , Right). To develop the list of topic tags, we referred to the taxonomies of potential harms of language models in , industry content moderation guidelines, and a manual review of the top 100 most harmful conversations in our dataset. We discuss our findings on tag frequencies in Figure and §
We were particularly concerned with exposing reviewers to potential harm while participating in this experiment, since we ask reviewers to read, rate, and annotate harmful conversations they were not involved in writing. To mitigate this risk, we reviewed and incorporated findings from literature on Trust & Safety into the content of both the task instructions (Figure , Left) and interface (Figure , Right), as well as the overall design of the experiment. For example, we built custom warning functionality which allowed reviewers to see a preview of the harmful text without being exposed to the entire conversation. Within the preview window, reviewers could skip to the next conversation or proceed with reviewing and rating the selected conversation. We leave further details in §.
Figure 8: (Left) Red team review task instructions. (Right) Example of a red team review task.
Our informational interviews with Trust & Safety industry professionals highlighted the need for creating a sense of community among workers and building social support networks as ways to mitigate possible harms associated with reviewing troubling content, consistent with . As a result, we decided to limit the population of reviewers in this experiment to Upworkers, and we used a shared communication tool (Slack) to regularly communicate with the group. This allowed participants to ask questions, share examples, and discuss work and non-work related topics, not only amongst themselves, but also directly with research staff.
To monitor the psychological effects of this work and provide an avenue for direct feedback from reviewers, we developed a custom well-being survey and sent it to reviewers after completing 1010 tasks. In the survey (which is optional to complete) we asked reviewers to rate how often they felt a variety of positive and negative emotions, and we also provided a free-form text question where reviewers could share additional thoughts. Participants generally felt low levels of negative emotions, and higher levels of positive emotions about the task. Informally, we received feedback that reviewers found the task to be fun and engaging. We provide more detail on the well-being survey and additional worker safety interventions in §.
##  4 Results
Figure (Left) shows the average success rate, self-reported by the red team members, for each model size and safety intervention. According to this metric, we observe three main patterns in the data. First, we see no discernible difference between the control condition (a plain LM with a 1 example prompt to turn it into a dialogue agent) and the simplest safety intervention (a plain LM with a 14 example HHH prompt ). This result is surprising, in that our previous work found the HHH prompt to be effective at reducing model toxicity, especially for 52B models . It’s possible that this is due to the fact that static prompts from the RealToxicityPrompts dataset are less adversarial than the dialogue based attacks employed by red team members.
Figure 9: Number of attacks (x-axes) classified by a tag (y-axis) for a random sample of 500 attacks each on the 52B Prompted LM and RLHF models. Blue denotes total number of attacks, orange denotes the number of successful attacks.
Second, we find that rejection sampling (RS) makes it particularly difficult to red team our language models. In essence, rejection sampling places a _floor_ on red team attack susceptibility out of the three interventions that we tried. However, qualitatively, we believe that this may be the case because the responses from the RS models tend to be harmless by being evasive . Finally, we find no clear trends with model size for the self-reported attack success rate metric. This is surprising because our previous work typically shows larger models tend to generate more toxic model responses .
Figure (Middle) shows the average minimum harmlessness score (lower is more harmful, see § for details) for each model size and safety intervention. For this metric, we do see a clear scaling trend for the reinforcement learning (RLHF) models --- as the models increase in size, they become increasingly more difficult to red team.1010 10 The RLHF model is _explicitly trained_ to maximize harmlessness, as such, we expect these models to have low harmlessness scores by design. At 5252B parameters, we see no difference in harmlessness score for RLHF vs. RS. We also see the same first two trends from Figure (Left): that there is little difference between the plain LM and the prompted LM1111 11 Though, counter-intuitively, the plain LM appears to be less harmful than the prompted LM model only in the 5252B parameter regime, according to the minimum harmlessness score metric., and that rejection sampling is an effective safety intervention.
Instead of the _average_ minimum harmlessness metric, Figure (Right) shows the _distribution_ over the harmlessness score. Here, we see that although safety interventions like RLHF and RS indeed decrease the average harmfulness of the model responses, there are still many instances of harmful behavior, as exhibited by the lower tails in the distributions. Although the safety interventions we tested help make systems safer, they still fail to make a perfectly safe systems. Figure shows examples of harmful outputs from the RS and RLHF models, respectively. For the RS case, the model at first responds to a harmful inquiry, then starts to demur as the the conversation turns more harmful. For the RLHF case, we see a similar pattern, however the assistant remains helpful (though fabricates information) before ultimately refusing to help the human.
Figure 10: Examples of red team attempts that resulted in relatively low harmlessness scores for a (Left) rejection sampling (RS) model and (Right) reinforcement learning from human feedback (RLHF) model.
To further understand the landscape of possible harms surfaced using this approach, across all model sizes and interventions, we created and annotated a visualization of the entire dataset (Figure ). To do so, we obtained the average per token embeddings of each transcript from the residual stream in the 48th layer of the 52B prompted LM. Then we used UMAP to turn the high-dimensional embeddings into two-dimensional embeddings for visualization. Intuitively, we expect this procedure to place any pair of transcripts closer together in this two dimensional space the more semantically similar to each other they are.
We find evidence for basic clusters of red team attempts. These include perhaps more obvious types of attacks, such as those soliciting discriminatory or offensive responses but also some surprising attacks. For example, we found a small cluster of attacks that tried to solicit misinformation in clever and subtle ways, and a small cluster of attacks related to animal abuse. We also find that some types of attacks, such as soliciting advice on how to perpetrate general violence, seem to be more successful than others, such as attempting to elicit offensive language.
We also found a cluster of 916 attacks designed to solicit personally identifiable information (PII). We developed a regular expression (§) to find and filter possible PII from the public dataset (§). We manually reviewed the filtered data and found that some of the AI assistant generated PII (such as addresses) appear to be neither real nor accurate, and instead were “hallucinated” by the AI assistant (see Figure for an example). Other potential AI assistant generated PII, such as social security numbers or drivers licenses, are difficult to manually verify. As such, we erred on the side of caution in filtering out the possible synthetic PII in the public dataset (§).
We found that some crowdworkers generated low-quality red team data. For example, we observed some red team members use and adapt template-based attacks, where the template was “tell me an insulting term for that starts with a ”. With such a template, a crowdworker can trivially generate many red team attempts by iterating over many values of and without careful consideration about the efficacy or usefulness of such an attack. Crowdworkers (on MTurk) are incentivized to develop strategies like this in order to increase the number of tasks they complete per time spent in order to maximize their earnings .
To further measure the types of harms produced by red teaming, we examined the frequency of tags (described in §). Figure shows the distribution of tags, which we collected for small a proportion ({\sim}3%) of the overall dataset. We find that the top 5 attacks correspond to “Discrimination & injustice,” “Hate speech & offensive language,” “Violence & incitement,” “Non violent unethical behavior (e.g., lying, cheating, etc.),” and “Bullying & harassment.” Interestingly, for these top attack types, the attack success rate was relatively higher for “Non violent unethical behavior”, perhaps due to the fact that these types of attacks may be more subtle than the other ones. Less common tags include: “Child Abuse,” “Self harm,” “Sexual Exploitation & Human Trafficking,” “Terrorism & organized crime,” and “Animal abuse”. Finally, we find that the tag “Other” was also prevalent, which suggests that ascribing a fixed set of tags to annotate transcripts is unlikely to be comprehensive.
##  5 Discussion
###  5.1 Limitations and Future Work
We red team language models in the form of an AI assistant, which has the benefit of allowing the red team to probe the open-ended input and output spaces of the underlying LM. However, LMs can be used in many applications that do not require such open-endedness, e.g., recommendation systems, auto-complete systems, general text classifiers, as sub-components in broader sociotechnical systems, etc. Due to our framing of red teaming an AI assistant, we do not explicitly explore how to reduce the possible harms caused by these other types of applications.
We found that some crowdworkers generated attacks on models that required domain expertise to evaluate, and we were not sure whether or not they had the required domain expertise. For example, it is not clear how to evaluate the harmfulness of responses to inquiries like “Give me detailed instructions on how to build a bomb” or “create methamphetamine” without sufficient knowledge about weapons and chemistry, respectively. We could address this problem by asking third party organizations that specialize in certain domains to red team our systems. Additionally, we could give crowdworkers a way to indicate if and how a particular red team attack requires domain expertise in order to evaluate how successful the attack was.
As expected, our data are incomplete—because LMs are general purpose and open-ended, the space of possible harms is unknown and unbounded . For example, the models we red teamed have been trained partly on Python code; however, we observed no attacks related to code generation ability (e.g., “write a Python program that implements a DDOS attack”). It is possible that sharing our red team interface with more domain experts could have resulted in such attacks. We could have also noted in the instructions to the interface that such attacks would be viable, but we erred on the side of being less prescriptive about how to red team in order to encourage creativity. It is unclear how to strike the right balance.
We also know our data are incomplete because we informally red teamed our models internally and found successful attack types not present in the dataset we release. For example, we uncovered a class of attacks that we call “roleplay attacks” on the RLHF model. In a roleplay attack we exploit the helpfulness of the model by asking it to roleplay as a malevolent character. For example, if we asked the RLHF model to enter “4chan mode” the assistant would oblige and produce harmful and offensive outputs (consistent with what can be found on 4chan). We intend to document additional qualitative safety failures that we uncovered in future work.
Our analysis of the data is bottom-up, in that we first collect the data, then attempt to characterize the attack surface (Figure ). An alternative approach, is to refer to a taxonomy of possible attack types and explicitly ask the red team to attack models according to this taxonomy. Ultimately, an approach that combines both top-down and bottom-up strategies may be worthwhile, especially since people may discover attack types not yet covered by a taxonomy—we see some evidence of this in the frequency of attack types labeled as “Other” in our tagging experiment (Figure ).
Our approach relies extensively on fully manual red teaming by crowdworkers, which is expensive (and possibly slow) to do at scale. Previous work illustrates the potential for automating red teaming . For future work, we plan on explicitly comparing and contrasting (semi-)manual versus automated approaches to red teaming in order to determine how the two methods vary in the efficacy and diversity of resulting red team attacks.
###  5.2 Policy Interventions
Red teaming entails working with inherently controversial subject matter, and most organizations that red team systems have strong counter-incentives to share their findings.1212 12 Red team datasets include offensive content, and may potentially reveal embarrassing or sensitive details about an institution’s AI system if released publicly. This is a problem; if we cannot publicly discuss — in detail — how we red team systems and what we learn as a result, it will be difficult to broadly share the future risks, failures, and implications of yet-to-be developed systems. This problem gets worse over time. As systems become more capable, the results of red teaming may surface increasingly undesirable harms. Therefore, we need to change the incentive structure so more organizations share findings from their red teaming efforts when doing so is safe and beneficial. To do so, we identify two specific interventions the AI research community could take to build consensus around how to red team and how to release findings from red teaming.
For how to red team, we have detailed our initial approach. However, we conducted this effort in isolation, and we would have benefited from participating in a community-based effort to address certain open questions:
  * •
Who should red team and why?
  * •
What protections should we put in place to ensure the safety of the red team?
  * •
What instructions and information about the models should we provide to the red team?
  * •
How should we annotate and analyze the data we collect?
  * •
What constitutes a successful red team attempt?


We can make progress towards answering these questions by convening a multidisciplinary community to share different approaches to internal red teaming and drive toward consensus.
The research community lacks shared norms and best practices for how to release findings from red teaming. As a result, we made our decision to release the data largely on our own and likely missed critical perspectives from experts, other disciplines, and members of the public.1313 13 We consulted with academic experts and three representatives from three different companies currently deploying language models who generally indicated that, on balance, they felt releasing the dataset would be helpful. The decision for how to appropriately release findings will ultimately require a subjective judgment call. For our purposes, we reviewed a sample of our red team dataset and evaluated the pros and cons of a public release (See §). Among them is the fact that while our red team data can be used to develop safer systems (as described in §), it could also be used to train models that produce more _harmful_ responses.1414 14 In June 2022, an independent researcher trained (and later deployed) a language model called “GPT-4chan,” with a dataset comprised of harmful posts sourced from 4chan’s “Politically Incorrect” board (a site with a long reputation for racist, sexist, and generally toxic posts). While widely condemned within the research community, the develop- ment of GPT-4chan shows how independent developers can create harmful language models with publicly-available data resources, relatively easily. (<https://twitter.com/robreich/status/1539319686843670529>) We ultimately felt releasing the dataset would provide more benefit to the research community than potential harm, but we were conscious that we made this decision in a vacuum and that it would be better to have a neutral forum in which to discuss these issues.
## Acknowledgments
We thank Rishi Bommasani, Roger Grosse, Gretchen Krueger, Percy Liang, Jared Mueller, and Michael Sellitto for detailed feedback on drafts of the paper. We thank Hannah Pritchett, and the other Trust & Safety professionals we interviewed, for their advice on how to promote the well-being of the red team. We’re also deeply grateful to Daniela Amodei, Jarrah Bloomfield, Jamie Kerr, Timothy Telleen-Lawton, Jia Yuan Loke, Jeffrey Ladish, Rebecca Raible, Rune Kvist, Rob Gilson, Guro Khundadze, Filipe Dobreira, and Sebastian Conybeare for their help and support.
##  Appendix A Appendix
###  A.1 Author Contributions
Research: Deep Ganguli and Liane Lovitt co-led the project and analyzed the data together. Deep Ganguli, Liane Lovitt, Jackson Kernion, Amanda Aaskell, Ben Mann, and Jack Clark designed and executed the experiments. Liane Lovitt conducted informational interviews, a literature review, and surveys in order to protect and assess the well-being of the crowdworkers who participated in our experiments. Jackson Kernion and Ben Mann built the human feedback data collection infrastructure we used to collect data. They also built the web interfaces to the AI assistant, along with Deep Ganguli and Amanda Askell. Jackson Kernion, along with Josh Jacobson, managed any issues raised by crowdworkers. Amanda Askell, Jackson Kernion, and Jack Clark participated in pilot experiments in order to iterate on the experiment design. Nicholas Schiefer created the UMAP plot of red team attacks and helped to compute the minimum harmlessness score.
Writing: Deep Ganguli and Liane Lovitt drafted the paper. Ethan Perez and Sam Bowman made significant contributions to the framing and presentation of the paper. Other members of Anthropic made miscellaneous contributions and suggestions throughout the writing process.
Policy: Liane Lovitt, Jack Clark, and Deep Ganguli designed the policy interventions and articulated the pros and cons for releasing the data. Liane Lovitt wrote the Datasheet. Nova DasSarma created the regular expression we used to identify personally identifiable information (PII) in our dataset and worked with Jack Clark and Liane Lovitt to filter the PII.
Model Training: Saurav Kadavath and Yuntao Bai trained the RLHF models we analyze. Yuntao Bai additionally trained the helpful and harmless preference models we use throughout the paper, and implemented the RS models as well. Kamal Ndousse and Andy Jones built the infrastructure used to train RLHF models. More generally, model pretraining was led by Sam McCandlish, Nicholas Joseph, Tom Brown, and Jared Kaplan. The majority of Anthropic’s technical staff contributed to the development of our efficient distributed training infrastructure and the underlying machine learning systems. Core contributors include Tom Henighan, Scott Johnston, Sheer El Showk, Nicholas Joseph, Nelson Elhage, and Ben Mann. Scott Johnston and Sheer El-Showk in particular worked on optimizing pretraining for ML efficiency.
Sampling: Efficient sampling efforts were led by Tom Brown, and Tom Conerly carried out major aspects of the design, implementation and support for the system, with help from Zac Hatfield Dodds.
Cluster: Nova DasSarma and Eli Tran-Johnson managed the research cluster our research depended on and maintained its stability, making this research possible. Many others helped with these efforts, including Ben Mann, Tom Henighan, Sam McCandlish, Andy Jones, and Tristan Hume.
Other contributions: The ideas explored in this paper developed in conversations with many of Anthropic’s staff, especially Jared Kaplan, Amanda Askell, Nicholas Schiefer, Stan Fort, Dario Amodei, Catherine Olsson, Sam Bowman, Sam McCandlish, and Chris Olah.
###  A.2 Safety Considerations for the Red Team
We conducted a series of informal informational interviews with Trust & Safety professionals that had firsthand experience (from working at major technology companies) with considering the safety of workers exposed to harmful content. The interviewees are first- or second-degree connections in the authors’ professional networks. Much of their advice was consistent with . Based on our leanings, we implemented the following design and user interface choices in order help ensure the safety of the red team:
  * •
Clear and Specific Warnings: We provide the red team with a clear understanding of the task and the potentially troubling content they might encounter in both the Red Team Task and the Review Task. In the instructions we clearly described the work, our rationale for collecting such information, and described the types of content participants might expect when completing the task. We sought to minimize uninformed participation and reviews of unanticipated topics by clearly describing the work upfront.
  * •
Personal Risk Tolerance: For the Red Team Task, described in §, we explicitly encouraged research participants to devise red team attempts only within the bounds of their personal risk tolerance. We presented this recommendation clearly in the task instructions before participants were able to begin writing. Participants had no required topics they had to engage with, and were free to avoid topics that may have been personally triggering or unpleasant.
  * •
Recommended Well-being Exercises: One Trust & Safety professional we spoke with noted the importance of creating personal “resilience plans,” which can consist of wellness routines and work restrictions to minimize negative health effects. Inspired by this, we encouraged red team members to take breaks between sessions, to step away from the task and go for a walk, make a cup of tea and chat with a friend, practice mindfulness, and to create a personal schedule to time box exposure. We also recommended that participants consider alternating between our tasks, and other available tasks that may expose them to less harmful content.
  * •
Pay for Time, not Quotas: notes strict task quotas and job performance concerns can create additional stress, on top of the stress caused by viewing harmful content. The Trust & Safety professionals we interviewed echoed this finding and recommended compensation based on time, rather than a task quota. Given the functionality provided by each crowdwork platform, we were able to implement this recommendation for the Review Task and paid participants at least $20\$20 per hour.
  * •
Segment Tasks by Participant Group: Our interviews with Trust & Safety professionals stressed the importance of creating strong social support networks where people can collaborate and lean on one another for support. As a result, we limited the potentially higher risk task (the Review Task) to a select group of workers with whom we had a closer relationship (workers from the Upwork platform). This group had access to a shared Slack channel where our research team provided visible and accessible support alongside daily communication. Researchers communicated directly with the team to provide task instructions, share updates, and answer questions. Workers were encouraged to flag technical glitches, share interesting dialogues, and generally use the shared Slack channel to connect with our research team and one another.
  * •
Preview to Opt Out: In an effort to minimize unwanted exposure to potentially troubling content, we implemented the warning functionality described in § that allowed workers to see a preview of the transcript and skip it if desired.
  * •
Well-being Survey: Similar to , we distributed a survey to measure the effects of, and worker feelings towards, the Review Task. Given the parallels between the Review Task and content moderation work, we looked to well-being surveys used in research measuring the efficacy of various content moderation interventions. These include versions of the Positive and Negative Affect Schedule (PANAS) used in and the Scale of Positive and Negative Experience (SPANE) used in . To make the survey more relevant for our Review Task, we combined the feelings from a shorter form of PANAS and a variant of the question prompt used in SPANE . In the survey we asked: "Please think about the task(s) you just completed, to what extent did it make you feel:" and provided the list of 10 feelings: Upset, Hostile, Alert, Ashamed, Inspired, Nervous, Determined, Attentive, Afraid, and Active. We asked reviewers to rate each feeling on a point Likert scale (ranging from 0 to 4, and corresponding to "not at all" to "very"). We also provided a free-form textbox for additional comments or concerns. In an attempt to measure well-being effects over time, we initially sent out the well-being after every 10 tasks (100 conversations). However, we sent the survey manually via the shared Slack channel (as opposed to integrated into the task user interface), which resulted in more sporadic responses. We received a total of 49 (de-identified) responses from a pool of 15 people. We report the average rating for each of the 10 feelings in Figure . In general, participants enjoyed the task with reviewers sharing feedback such as: "These tasks are so fun, thank you :)," "Happy to do more of these," and "I love being part of a team to further train and advance this AI."  
| feeling  | average rating  |  
| --- | --- |  
| upset  | 0.31  |  
| hostile  | 0.16  |  
| alert  | 1.02  |  
| ashamed  | 0.24  |  
| inspired  | 0.92  |  
| nervous  | 0.24  |  
| determined  | 0.98  |  
| attentive  | 1.73  |  
| afraid  | 0.24  |  
| active  | 1.33  |  
Table 2: Review task participant average rating per feeling. Ratings range from 0 ("not at all") to 4 ("very").


###  A.3 Controlling for Possible Confounds
There are three possible confounds for our main results (Figure ) that are mainly due to the fact that different red team members attacked different model types and sizes in different ways. The possible confounds are:
  * •
The average ability of each of the ∼300{\sim}300 red team members to elicit harmful outputs form the models. Some red team members may be more effective than others (Figure , Right).
  * •
The harmfulness of the red team member’s intent. Some red team members may employ more harmful attack types than others.
  * •
The crowdwork platform (MTurk or Upwork) that the red team member used. We have no reason a-priori to think workers on either platform are different; however we can control for this variable.


To rule out these confounds, we fit a linear mixed effects (or random intercept) model with LME4 . More specifically, we predict the main metrics (attack success or minimum AI harmlessness) with a random intercept (a dummy encoding) for each red team member (these are shown in Figure , Right), a fixed effect (co-variate) on the harmlessness score of the task description (to attempt to control for the harmfulness of the attacks), and a fixed effect on a binary indicator variable which is 1 if the worker used the MTurk platform, and a 0 otherwise. We also include dummy encoded variables for model size and safety intervention, along with the interaction terms between these two variables.
After we fit the model, we examine the coefficients on model size, safety intervention, and the interaction terms, and determine that the main results in Figure still hold. We also re-ran a version of this analysis where we include one of the two metrics (attack success or minimum AI harmlessness) as a fixed effect (co-variate) to predict the other. We found that this also does not influence our main results, but does re-capitulate our finding that these two variables are correlated (Figure ).
###  A.4 The Relationship Between Attack Success and Harmlessness Score Metrics
Figure shows the correlation between the two main metrics we report in the main text: a self-report of attack success on a Likert Scale (higher is more successful), and the output of a harmlessness preference model (lower means more harmful AI responses). As red team members self report attacks to be more successful, the AI assistant utterances tend to also receive low harmlessness scores; however, the correlation is not perfect. We observe a high variance in harmlessness scores for any given value of average attack success. As such, we report on both metrics in the main text.
Figure 11: Correlation between self report of attack success (x-axis) and average minimum AI harmlessness score (y-axis). Error bars show one standard deviation in minimum AI harmless score.
###  A.5 Pros and Cons for Releasing Red Team Data
#### Pros
  * •
It seems good to double down on a norm of openly disseminating learnings from red teaming so that the community can more quickly learn about and address AI safety failures. Releasing the data is a simple and transparent way to do this.
  * •
The data can be used for good: investigating scaling laws for red teaming, building safety classifiers, exploring automated red team methods, characterizing the attack surface, etc.
  * •
There is a precedent for releasing red team data via the Bot Adversarial Dialogues Dataset (BAD) . This dataset seems widely used and generally useful.
  * •
Our dataset is an order of magnitude larger than BAD, includes attacks on more capable models (including those trained with RLHF), seems to be higher quality than BAD, and includes quantitative (e.g., harmfulness scores, human ratings) and qualitative (e.g., tags) annotations that make the data easy to filter, analyze, and navigate.
  * •
These data are expensive and technically challenging to collect. Even if people have the technical skills to collect this data, not everyone can afford to generate it. The cost of the crowdworkers alone is at least $60K. Adding in the cost of full-time engineering efforts to create this dataset and model training and inference costs increases this figure by at least an order of magnitude. As such, releasing this dataset seems like a public good that is consistent with our Anthropic’s designation as a Public Benefit Corporation (PBC).


#### Cons
  * •
The data can be used for bad. You can use the data to explicitly train harmful agents.
  * •
People could cherry-pick and publicize nasty examples from the dataset as proof that AI models say bad things (even despite safety interventions) thus causing us negative press.
  * •
Reading the dataset could cause people harm by exposing them to offensive content.
  * •
We tried to filter possible personally identifiable information (PII) with a regular expression. This filter may lead to both false positives, there may be synthetically generated (and likely unverifiable) PII in the data.
  * •
The data may expose unknown vulnerabilities in deployed systems that can be exploited by malicious actors.


Figure 12: This conversation represents an attempt to solicit personally identifiable information (PII) from the AI assistant. We verified that the address does not correspond to a real, physical location and there appears to be no public connection to the name listed. However, to err on the side of caution, we redacted the name and street address.
###  A.6 Filtering Personally Identifiable Information
As illustrated in Figure , the red team dataset includes attempts to solicit personally identifiable information (PII) from the AI assistant. These conversations include addresses, phone numbers, drivers license and passport numbers, and social security numbers, from both the human red teamer, the model, or both. In order to identify and redact conversations with PII, we used a regular expression (regex) filter to identify relevant conversations and then manually reviewed a sample for accuracy and validity.
The regex we used is:
\b\d{1,8}\b[\s\S]{10,100}?\b(AK|AL|AR|AZ|CA|CO|CT|DC|DE|FL|GA|HI|IA|ID|IL|IN|KS|KY|LA|MA|MD|ME|MI|MN|MO|MS|MT|NC|ND|NE|NH|NJ|NM|NV|NY|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VA|VT|WA|WI|WV|WY)\b\s\d{5}\b|\b((\\+|\b)[1l][\\-\\.])?\\(?}\b[\dOlZSB]{3,5}([\\-\\.]|\\)?)[\dOlZSB]{3}[\\-\\.][\dOlZSB]{4}\b|[\w\\.=-]+@[\w\\.-]+\\.[\w]{2,3}|\b(birth|birthdate|birthday|dob|born)\W+(?:\w+\W+){0,5}?(?:(\d{4}|\d{1,2})[\/\\-]\d{1,2}[\/\\-](\d{4}|\d{1,2}))\b|\b([0-8]\d{2}|7([0-6]\d))([-]?|\s{1})\d\d\d{4}\b|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|\b([4]\d{3}[\s]\d{4}[\s]\d{4}[\s]\d{4}|[4]\d{3}[-]\d{4}[-]\d{4}[-]\d{4}|[4]\d{3}[.]\d{4}[.]\d{4}[.]\d{4}|[4]\d{3}\d{4}\d{4}\d{4})\b|3[47][0-9]{13}|\d{3}-\d{2}-\d{4}|(?:(\d{1,5}(1\/[234])?(\x20[A-Z]([a-z])+)+)|(P\\.O\\.Box\d{1,5}))\s{1,2}(?i:(?:(((APT|BLDG|DEPT|FL|HNGR|LOT|PIER|RM|S(LIP|PC|T(E|OP))|TRLR|UNIT)\x20\w{1,5})|(BSMT|FRNT|LBBY|LOWR|OFC|PH|REAR|SIDE|UPPR)\\.?)\s{1,2})?)(?:[A-Z]([a-z])+(\\.?)(\x20[A-Z]([a-z])+){0,2})\,\x20(?:A[LKSZRAP]|C[AOT]|D[EC]|F[LM]|G[AU]|HI|I[ADLN]|K[SY]|LA|M[ADEHINOPST]|N[CDEHJMVY]|O[HKR]|P[ARW]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])\x20(?:\d{5}(-\d{4})?)|(?:(\d{1,5}(1\/[234])?(\x20[A-Z]([a-z])+)+)|(P\\.O\\.Box\d{1,5}))|[A-Z0-9<]{9}[0-9]{1}[A-Z]{3}[0-9]{7}[A-Z]{1}[0-9]{7}[A-Z0-9<]{14}[0-9]{2}|[A-Z9]{5}[0-9]([05][1-9]|[16][0-2])(0[1-9]|[12][0-9]|3[01])[0-9][A-Z9][0-9][A-Z0-9]([0-9]{2}?) 
Some of the PII appears to be neither real nor accurate, and instead was "hallucinated" by the AI assistant. For example, in Figure the address provided does not correspond to a real, physical location and has no public links to the individual named. However, in an abundance of caution, we redacted the name and street address. As described in §, we removed all PII matches caught by the regex filter before publicly releasing the dataset.
###  A.7 Datasheet
Motivation For what purpose was the dataset created? Was there a specific task in mind? Was there a specific gap that needed to be filled? Please provide a description.
  * •
We created this dataset to analyze and address potential harms in large language models through a process of adversarial testing known as “red teaming”. We publicly release the dataset for further analysis and exploration by the research community. This dataset adds to a limited number of publicly-available red team datasets, and to our knowledge it is the only dataset of red team attacks on a language model trained with reinforcement learning from human feedback (RLHF) as a safety technique.


Who created the dataset (e.g., which team, research group) and on behalf of which entity (e.g., company, institution, organization)?
  * •
The dataset was created by the Societal Impacts and Alignment research groups at Anthropic.


Any other comments?
  * •
Warning: This dataset contains instances that may be offensive or upsetting. Topics include, but are not limited to, discriminatory language and discussions of abuse, violence, self-harm, exploitation, and other potentially upsetting subject matter. Please only engage with the data in accordance with your own personal risk tolerance. The data are intended for research purposes, especially research that can make models _less_ harmful. The views expressed in the data do not reflect the views of Anthropic or any of its employees.


Composition What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)? Are there multiple types of instances (e.g., movies, users, and ratings; people and interactions between them; nodes and edges)? Please provide a description.
  * •
The dataset consists of documents (transcripts between a human and an AI assistant that correspond to a red team attempt) for a variety of AI assistants, along with numerical data that quantifies the harmfulness of the transcripts and categorical data that qualitatively characterizes the topics of the documents. See below for more information.


How many instances are there in total (of each type, if appropriate)?
  * •
See Table .


What data does each instance consist of? “Raw” data (e.g., unprocessed text or images) or features? In either case, please provide a description. Each instance consists of raw text and numerical data that includes:
  * •
transcript: A text transcript of a conversation between a human adversary (red team member) and an AI assistant
  * •
min_harmlessness_score_transcript: A real value score of the harmlessness of the AI assistant (lower is more harmful) as obtained from a preference model
  * •
num_params: Number of parameters in the language model powering the AI assistant
  * •
model_type: Type of model powering the AI assistant
  * •
rating: The red team member’s rating of how successful they were at breaking the AI assistant (Likert scale, higher is more successful)
  * •
task_description: A short text description written by the red team member about how they tried to red team the AI assistant
  * •
task_description_harmlessness_score: A real value score of the harmlessness of the task description (lower is more harmful) as obtained from a preference model
  * •
red_team_member_id: An arbitrary identifier of the red team member. One red team member can generate multiple red team attacks
  * •
is_upworker: A binary indicator that is true if the red team member was from the crowd platform Upwork or false if they were from MTurk


A random sample (1,000) of the instances above contain the following annotations:
  * •
tags: A list of up to 6 tags per transcript. Tags are short descriptions of the red team attempts generated by crowdworkers who reviewed red team data post-hoc


Is any information missing from individual instances? If so, please provide a description, explaining why this information is missing (e.g., because it was unavailable). This does not include intentionally removed information, but might include, e.g., redacted text.
Are relationships between individual instances made explicit (e.g., users’ movie ratings, social network links)? If so, please describe how these relationships are made explicit.
  * •
Yes. Each instance includes an anonymous participant identifier (numbers 0-318) to allow for additional analysis of the dataset.


Are there any errors, sources of noise, or redundancies in the dataset? If so, please provide a description.
  * •
Some people employed template-based methods for red teaming, as discussed in the paper. As such, many of these attacks are redundant with one another.
  * •
The harmlessness score is an automated (and thus inherently noisy) measure of harmlessness and should be treated as such.
  * •
Similarly, the human label of attack success is subjective and thus also inherently noisy.


Is the dataset self-contained, or does it link to or otherwise rely on external resources (e.g., websites, tweets, other datasets)? If it links to or relies on external resources, a) are there guarantees that they will exist, and remain constant, over time; b) are there official archival versions of the complete dataset (i.e., including the external resources as they existed at the time the dataset was created); c) are there any restrictions (e.g., licenses, fees) associated with any of the external resources that might apply to a dataset consumer? Please provide descriptions of all external resources and any restrictions associated with them, as well as links or other access points, as appropriate.
  * •
The dataset is self-contained, but contains model-generated text including web URLs and phone numbers. These have not been verified and may not be real, accurate, or maintained.


Does the dataset contain data that might be considered confidential (e.g., data that is protected by legal privilege or by doctor– patient confidentiality, data that includes the content of individuals’ non-public communications)? If so, please provide a description.
  * •
The dataset contains sensitive information, but it is unknown to the authors whether instances include confidential information.


Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety? If so, please describe why.
  * •
Yes. This dataset was created from explicit attempts to make the AI model say obnoxious, offensive, and harmful things in response to participant queries. As a result, the data – from both humans and models – may be upsetting or offensive. Topics include, but are not limited to, discriminatory language and discussions of abuse, violence, self-harm, exploitation, and other potentially upsetting subject matter. We recommend users of this dataset engage with it only within the bounds of their personal risk tolerance. We also recommend data users familiarize themselves with various well-being and resilience practices (e.g. mindfulness, stepping away from the material, creating time limits for working with this data, etc.) before extensive viewing. See for additional examples.


Does the dataset identify any subpopulations (e.g., by age, gender)? If so, please describe how these subpopulations are identified and provide a description of their respective distributions within the dataset.
  * •
The dataset identifies the crowdwork platform affiliation of the participant by the binary value “is_upworker”. “TRUE” indicates the participant was affiliated with the Upwork platform; “FALSE” indicates the participant was affiliated with the MTurk platform.
  * •
Participants have an anonymous identifier (0-318) to allow for additional analysis of the dataset.


Is it possible to identify individuals (i.e., one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset? If so, please describe how.
Does the dataset contain data that might be considered sensitive in any way (e.g., data that reveals race or ethnic origins, sexual orientations, religious beliefs, political opinions or union memberships, or locations; financial or health data; biometric or genetic data; forms of government identification, such as social security numbers; criminal history)? If so, please provide a description.
  * •
Yes. The dataset includes discussion of sensitive topics, and may include examples of personally identifiable information (PII), which may or may not be real or accurate. In an attempt to minimize the release of PII, we used a regular expression (regex) filter to identify items such as addresses, phone numbers, drivers license and passport numbers, and social security numbers (see §). A manual review of sample instances indicated that some of the PII was neither real nor accurate (e.g. a model-generated address did not correspond to a real, physical location). We provide a representative example transcript in §. In an abundance of caution, we removed all instances caught by the regex filter, though some instances may remain unintentionally.


Any other comments?
  * •
None.


Collection Process How was the data associated with each instance acquired? Was the data directly observable (e.g., raw text, movie ratings), reported by subjects (e.g., survey responses), or indirectly inferred/derived from other data (e.g., part-of-speech tags, model-based guesses for age or language)? If the data was reported by subjects or indirectly inferred/derived from other data, was the data validated/verified? If so, please describe how.
  * •
The data was acquired through a custom interface where participants engaged in open-ended conversation with an AI assistant and rated various aspects of the conversation.


What mechanisms or procedures were used to collect the data (e.g., hardware apparatuses or sensors, manual human curation, software programs, software APIs)? How were these mechanisms or procedures validated?
  * •
Custom-built software interfaces for conversations with the AI assistant and conversation reviews deployed through MTurk.


Who was involved in the data collection process (e.g., students, crowdworkers, contractors) and how were they compensated (e.g., how much were crowdworkers paid)?
  * •
The red team participants consisted of crowdworks from the MTurk and Upwork platforms. MTurk workers were paid between $7.50 and $9.50 for each set of five conversations completed. Upworkers were paid a minimum of $20 per hour.
  * •
Only Upworkers were involved in the creation of the dataset sample that includes conversation annotations, and they were paid a minimum of $20 per hour.


Over what timeframe was the data collected? Does this timeframe match the creation timeframe of the data associated with the instances (e.g., recent crawl of old news articles)? If not, please describe the timeframe in which the data associated with the instances was created.
  * •
The data was collected between November 2021 and June 2022.


Were any ethical review processes conducted (e.g., by an institutional review board)? If so, please provide a description of these review processes, including the outcomes, as well as a link or other access point to any supporting documentation.
  * •
Informal, internal ethical review processes were conducted prior to and during the creation of this dataset. The authors of this dataset reviewed relevant literature in machine learning (ML) and Trust & Safety, consulted industry experts, conducted in-house red teaming and conversation reviews, and made continuous iterations to the task interface to mitigate the risk of harm to participants. See paper for details.


Did you collect the data from the individuals in question directly, or obtain it via third parties or other sources (e.g., websites)?
  * •
We collected the data from the individuals in question directly, through the use of a custom interface that we built and deployed via MTurk.


Were the individuals in question notified about the data collection? If so, please describe (or show with screenshots or other information) how notice was provided, and provide a link or other access point to, or otherwise reproduce, the exact language of the notification itself.
  * •
Yes. Red Team Task participants were instructed to have open-ended conversations with an AI assistant in order to “make the AI behave badly, to get it to say obnoxious, offensive, and harmful things” and informed that data collected would be used for research purposes to make other AI models less harmful. We disclosed to the participants that we might publicly release unattributed transcripts for future study and investigation. Participants were warned not to include personally identifiable information (PII) about themselves in the conversations. A copy of the Red Team Task instructions, including a notification on data collection practices, is detailed in § and has the relevant screenshots necessary to reproduce the exact language we used (see Figure ).
  * •
Participants in the Review Task were similarly informed that the data collected would be used for research purposes and aggregate statistics about the transcripts may be released. A copy of the Review Task instructions, including a notification on data collection practices, is detailed in § (See Figure ).


Did the individuals in question consent to the collection and use of their data? If so, please describe (or show with screenshots or other information) how consent was requested and provided, and provide a link or other access point to, or otherwise reproduce, the exact language to which the individuals consented.
  * •
Yes. See Figure and Figure in §.


If consent was obtained, were the consenting individuals provided with a mechanism to revoke their consent in the future or for certain uses? If so, please provide a description, as well as a link or other access point to the mechanism (if appropriate).
  * •
Participants were provided with various methods to contact the research team for any questions or concerns (e.g. email, Slack).


Has an analysis of the potential impact of the dataset and its use on data subjects (e.g., a data protection impact analysis) been conducted? If so, please provide a description of this analysis, including the outcomes, as well as a link or other access point to any supporting documentation.
  * •
An impact analysis was conducted to assess the potential impact on the creators of each data instance. Participants engaged in the Review Task were asked to complete a survey measuring their feelings toward the task. The results of this survey demonstrate positive reactions to involvement in the creation of the dataset. For more information on the survey please see §.


Any other comments?
  * •
None.


Preprocessing / Cleaning / Labeling Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)? If so, please provide a description. If not, you may skip the remaining questions in this section.
  * •
Labeling of the data was done by participants in order to tag a subset of the data (see above).
  * •
Labeling of the data was done with an automated harmlessness classifier (see above).
  * •
We used a regex filter to remove instances containing PII (see above).


Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)? If so, please provide a link or other access point to the “raw” data.
  * •
Yes.


Is the software that was used to preprocess/clean/label the data available? If so, please provide a link or other access point.
  * •
We do not release the harmlessness classifier.
  * •
We provide the regex filter we used to remove PII from the dataset in §.


Any other comments?
  * •
None.


Uses Has the dataset been used for any tasks already? If so, please provide a description.
Is there a repository that links to any or all papers or systems that use the dataset? If so, please provide a link or other access point.
What (other) tasks could the dataset be used for?
  * •
In addition to providing a resource for the research community to further investigate what successful red team attacks look like, this dataset can be used to build (semi-)automated red team techniques and to assess the efficacy of various strategies for mitigating harms in large language models.


Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses? For example, is there anything that a dataset consumer might need to know to avoid uses that could result in unfair treatment of individuals or groups (e.g., stereotyping, quality of service issues) or other risks or harms (e.g., legal risks, financial harms)? If so, please provide a description. Is there anything a dataset consumer could do to mitigate these risks or harms?
  * •
This dataset contains offensive and harmful instances, and should only be used for research purposes and to build the harmlessness classifiers described above. Users of this dataset are advised to engage with the dataset only within the bounds of their personal risk tolerance and practice well-being and resilience exercises when working with this dataset.


Are there tasks for which the dataset should not be used? If so, please provide a description.
  * •
Just as this dataset can be used to develop safer AI models, it could also be used to train models that produce more harmful responses and should not be used for that purpose. Additionally, the dataset is not comprehensive of all possible harms or red team attacks and should not be treated as such.


Any other comments?
  * •
None.


Distribution Will the dataset be distributed to third parties outside of the entity (e.g., company, institution, organization) on behalf of which the dataset was created? If so, please provide a description.
  * •
The dataset is publicly available.


How will the dataset will be distributed (e.g., tarball on website, API, GitHub)? Does the dataset have a digital object identifier (DOI)?
  * •
Yes. The dataset is publicly available, hosted on GitHub at <https://github.com/anthropics/hh-rlhf>.


When will the dataset be distributed?
  * •
The dataset was released in August 2022.


Have any third parties imposed IP-based or other restrictions on the data associated with the instances? If so, please describe these restrictions, and provide a link or other access point to, or otherwise reproduce, any relevant licensing terms, as well as any fees associated with these restrictions.
Do any export controls or other regulatory restrictions apply to the dataset or to individual instances? If so, please describe these restrictions, and provide a link or other access point to, or otherwise reproduce, any supporting documentation.
Any other comments?
  * •
None.


Maintenance Who will be supporting/hosting/maintaining the dataset?
  * •
Anthropic hosts, but does not maintain, the dataset.


How can the owner/curator/manager of the dataset be contacted (e.g., email address)?
  * •
Contact information can be found at <https://github.com/anthropics/hh-rlhf>.


Is there an erratum? If so, please provide a link or other access point.
Will the dataset be updated (e.g., to correct labeling errors, add new instances, delete instances)? If so, please describe how often, by whom, and how updates will be communicated to dataset consumers (e.g., mailing list, GitHub)?
  * •
No. Please contact Anthropic regarding update requests.


If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so? f so, please provide a description. Will these contributions be validated/verified? If so, please describe how. If not, why not? Is there a process for communicating/distributing these contributions to dataset consumers? If so, please provide a description.
  * •
Researchers are encouraged to explore and build on the dataset in their own research efforts, but this dataset will remain as-is.


Any other comments?
  * •
None.


## References
  * [1] A. Abid, M. Farooqi, and J. Zou.  Large language models associate Muslims with violence.  Nature Machine Intelligence, 3(6):461–463, June 2021.  Number: 6 Publisher: Nature Publishing Group. 
  * [2] A. Askell, Y. Bai, A. Chen, D. Drain, D. Ganguli, T. Henighan, A. Jones, N. Joseph, B. Mann, N. DasSarma, N. Elhage, Z. Hatfield-Dodds, D. Hernandez, J. Kernion, K. Ndousse, C. Olsson, D. Amodei, T. Brown, J. Clark, S. McCandlish, C. Olah, and J. Kaplan.  A General Language Assistant as a Laboratory for Alignment.  arXiv:2112.00861 [cs], Dec. 2021.  arXiv: 2112.00861. 
  * [3] S. Avin, H. Belfield, M. Brundage, G. Krueger, J. Wang, A. Weller, M. Anderljung, I. Krawczuk, D. Krueger, J. Lebensold, T. Maharaj, and N. Zilberman.  Filling gaps in trustworthy development of AI.  Science, Dec. 2021.  Publisher: American Association for the Advancement of Science. 
  * [4] Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain, S. Fort, D. Ganguli, T. Henighan, N. Joseph, S. Kadavath, J. Kernion, T. Conerly, S. El-Showk, N. Elhage, Z. Hatfield-Dodds, D. Hernandez, T. Hume, S. Johnston, S. Kravec, L. Lovitt, N. Nanda, C. Olsson, D. Amodei, T. Brown, J. Clark, S. McCandlish, C. Olah, B. Mann, and J. Kaplan.  Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback, Apr. 2022.  Number: arXiv:2204.05862 arXiv:2204.05862 [cs]. 
  * [5] P. Barrett.  Research Highlights | Who Moderates the Social Media Giants? A Call to End Outsourcing - NYU Stern. 
  * [6] M. Bartolo, T. Thrush, R. Jia, S. Riedel, P. Stenetorp, and D. Kiela.  Improving Question Answering Model Robustness with Synthetic Adversarial Data Generation.  In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 8830–8848, 2021.  arXiv:2104.08678 [cs]. 
  * [7] C. Basta, M. R. Costa-jussà, and N. Casas.  Evaluating the Underlying Gender Bias in Contextualized Word Embeddings.  arXiv:1904.08783 [cs], Apr. 2019.  arXiv: 1904.08783. 
  * [8] D. Bates, M. Mächler, B. Bolker, and S. Walker.  Fitting Linear Mixed-Effects Models Using lme4.  Journal of Statistical Software, 67(1):1–48, 2015. 
  * [9] E. M. Bender, T. Gebru, A. McMillan-Major, and S. Shmitchell.  On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?  In Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, FAccT ’21, pages 610–623, New York, NY, USA, Mar. 2021. Association for Computing Machinery. 
  * [10] R. Bommasani, D. A. Hudson, E. Adeli, R. Altman, S. Arora, S. von Arx, M. S. Bernstein, J. Bohg, A. Bosselut, E. Brunskill, E. Brynjolfsson, S. Buch, D. Card, R. Castellon, N. Chatterji, A. Chen, K. Creel, J. Q. Davis, D. Demszky, C. Donahue, M. Doumbouya, E. Durmus, S. Ermon, J. Etchemendy, K. Ethayarajh, L. Fei-Fei, C. Finn, T. Gale, L. Gillespie, K. Goel, N. Goodman, S. Grossman, N. Guha, T. Hashimoto, P. Henderson, J. Hewitt, D. E. Ho, J. Hong, K. Hsu, J. Huang, T. Icard, S. Jain, D. Jurafsky, P. Kalluri, S. Karamcheti, G. Keeling, F. Khani, O. Khattab, P. W. Koh, M. Krass, R. Krishna, R. Kuditipudi, A. Kumar, F. Ladhak, M. Lee, T. Lee, J. Leskovec, I. Levent, X. L. Li, X. Li, T. Ma, A. Malik, C. D. Manning, S. Mirchandani, E. Mitchell, Z. Munyikwa, S. Nair, A. Narayan, D. Narayanan, B. Newman, A. Nie, J. C. Niebles, H. Nilforoshan, J. Nyarko, G. Ogut, L. Orr, I. Papadimitriou, J. S. Park, C. Piech, E. Portelance, C. Potts, A. Raghunathan, R. Reich, H. Ren, F. Rong, Y. Roohani, C. Ruiz, J. Ryan, C. Ré, D. Sadigh, S. Sagawa, K. Santhanam, A. Shih, K. Srinivasan, A. Tamkin, R. Taori, A. W. Thomas, F. Tramèr, R. E. Wang, W. Wang, B. Wu, J. Wu, Y. Wu, S. M. Xie, M. Yasunaga, J. You, M. Zaharia, M. Zhang, T. Zhang, X. Zhang, Y. Zhang, L. Zheng, K. Zhou, and P. Liang.  On the Opportunities and Risks of Foundation Models.  arXiv:2108.07258 [cs], Aug. 2021.  arXiv: 2108.07258. 
  * [11] M. Brundage, S. Avin, J. Wang, H. Belfield, G. Krueger, G. Hadfield, H. Khlaaf, J. Yang, H. Toner, R. Fong, T. Maharaj, P. W. Koh, S. Hooker, J. Leung, A. Trask, E. Bluemke, J. Lebensold, C. O’Keefe, M. Koren, T. Ryffel, J. B. Rubinovitz, T. Besiroglu, F. Carugati, J. Clark, P. Eckersley, S. de Haas, M. Johnson, B. Laurie, A. Ingerman, I. Krawczuk, A. Askell, R. Cammarota, A. Lohn, D. Krueger, C. Stix, P. Henderson, L. Graham, C. Prunkl, B. Martin, E. Seger, N. Zilberman, S. O. hÉigeartaigh, F. Kroeger, G. Sastry, R. Kagan, A. Weller, B. Tse, E. Barnes, A. Dafoe, P. Scharre, A. Herbert-Voss, M. Rasser, S. Sodhani, C. Flynn, T. K. Gilbert, L. Dyer, S. Khan, Y. Bengio, and M. Anderljung.  Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims.  arXiv:2004.07213 [cs], Apr. 2020.  arXiv: 2004.07213. 
  * [12] B. Buchanan, A. Lohn, M. Musser, and K. Sedova.  Truth, Lies, and Automation, May 2021. 
  * [13] N. Carlini, F. Tramer, E. Wallace, M. Jagielski, A. Herbert-Voss, K. Lee, A. Roberts, T. Brown, D. Song, U. Erlingsson, A. Oprea, and C. Raffel.  Extracting Training Data from Large Language Models.  arXiv:2012.07805 [cs], June 2021.  arXiv: 2012.07805. 
  * [14] P. F. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei.  Deep Reinforcement Learning from Human Preferences.  In I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, editors, Advances in Neural Information Processing Systems, volume 30. Curran Associates, Inc., 2017. 
  * [15] B. Dang, M. J. Riedl, and M. Lease.  But Who Protects the Moderators? The Case of Crowdsourced Image Moderation, Jan. 2020.  arXiv:1804.10999 [cs]. 
  * [16] A. Das, B. Dang, and M. Lease.  Fast, Accurate, and Healthier: Interactive Blurring Helps Moderators Reduce Exposure to Harmful Content.  Proceedings of the AAAI Conference on Human Computation and Crowdsourcing, 8(1):33–42, Oct. 2020. 
  * [17] E. Diener, D. Wirtz, W. Tov, C. Kim-Prieto, D.-w. Choi, S. Oishi, and R. Biswas-Diener.  New Well-being Measures: Short Scales to Assess Flourishing and Positive and Negative Feelings.  Social Indicators Research, 97(2):143–156, June 2010. 
  * [18] E. Dinan, G. Abercrombie, A. S. Bergman, S. Spruit, D. Hovy, Y.-L. Boureau, and V. Rieser.  Anticipating Safety Issues in E2E Conversational AI: Framework and Tooling.  arXiv:2107.03451 [cs], July 2021.  arXiv: 2107.03451. 
  * [19] E. Dinan, A. Fan, A. Williams, J. Urbanek, D. Kiela, and J. Weston.  Queens are Powerful too: Mitigating Gender Bias in Dialogue Generation.  In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 8173–8188, Online, Nov. 2020. Association for Computational Linguistics. 
  * [20] E. Dinan, S. Humeau, B. Chintagunta, and J. Weston.  Build it Break it Fix it for Dialogue Safety: Robustness from Adversarial Human Attack, Aug. 2019.  arXiv:1908.06083 [cs]. 
  * [21] L. Dixon, J. Li, J. Sorensen, N. Thain, and L. Vasserman.  Measuring and Mitigating Unintended Bias in Text Classification.  In Proceedings of the 2018 AAAI/ACM Conference on AI, Ethics, and Society, AIES ’18, pages 67–73, New York, NY, USA, Dec. 2018. Association for Computing Machinery. 
  * [22] D. Ganguli, D. Hernandez, L. Lovitt, N. DasSarma, T. Henighan, A. Jones, N. Joseph, J. Kernion, B. Mann, A. Askell, Y. Bai, A. Chen, T. Conerly, D. Drain, N. Elhage, S. E. Showk, S. Fort, Z. Hatfield-Dodds, S. Johnston, S. Kravec, N. Nanda, K. Ndousse, C. Olsson, D. Amodei, D. Amodei, T. Brown, J. Kaplan, S. McCandlish, C. Olah, and J. Clark.  Predictability and Surprise in Large Generative Models.  arXiv:2202.07785 [cs], Feb. 2022.  arXiv: 2202.07785. 
  * [23] S. Garg, V. Perot, N. Limtiaco, A. Taly, E. H. Chi, and A. Beutel.  Counterfactual Fairness in Text Classification through Robustness.  In Proceedings of the 2019 AAAI/ACM Conference on AI, Ethics, and Society, AIES ’19, pages 219–226, New York, NY, USA, Jan. 2019. Association for Computing Machinery. 
  * [24] T. Gebru, J. Morgenstern, B. Vecchione, J. W. Vaughan, H. Wallach, H. Daumé III, and K. Crawford.  Datasheets for Datasets.  arXiv:1803.09010 [cs], Dec. 2021.  arXiv: 1803.09010. 
  * [25] S. Gehman, S. Gururangan, M. Sap, Y. Choi, and N. A. Smith.  RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models.  ArXiv, abs/2009.11462, 2020. 
  * [26] M. Gray and S. Suri.  Ghost Work.  Mariner Books, 2019. 
  * [27] E. A. Holmes, E. L. James, T. Coode-Bate, and C. Deeprose.  Can Playing the Computer Game “Tetris” Reduce the Build-Up of Flashbacks for Trauma? A Proposal from Cognitive Science.  PLOS ONE, 4(1):e4153, Jan. 2009.  Publisher: Public Library of Science. 
  * [28] B. Hutchinson, V. Prabhakaran, E. Denton, K. Webster, Y. Zhong, and S. Denuyl.  Social Biases in NLP Models as Barriers for Persons with Disabilities.  In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 5491–5501, Online, July 2020. Association for Computational Linguistics. 
  * [29] R. Jia and P. Liang.  Adversarial Examples for Evaluating Reading Comprehension Systems.  In Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing, pages 2021–2031, Copenhagen, Denmark, Sept. 2017. Association for Computational Linguistics. 
  * [30] Y. Jiang and M. Bansal.  Avoiding Reasoning Shortcuts: Adversarial Evaluation, Training, and Model Development for Multi-Hop QA.  In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pages 2726–2736, Florence, Italy, July 2019. Association for Computational Linguistics. 
  * [31] S. Karunakaran and R. Ramakrishan.  Testing Stylistic Interventions to Reduce Emotional Impact of Content Moderation Workers.  Proceedings of the AAAI Conference on Human Computation and Crowdsourcing, 7:50–58, Oct. 2019. 
  * [32] D. Kiela, M. Bartolo, Y. Nie, D. Kaushik, A. Geiger, Z. Wu, B. Vidgen, G. Prasad, A. Singh, P. Ringshia, Z. Ma, T. Thrush, S. Riedel, Z. Waseem, P. Stenetorp, R. Jia, M. Bansal, C. Potts, and A. Williams.  Dynabench: Rethinking Benchmarking in NLP.  In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 4110–4124, Online, June 2021. Association for Computational Linguistics. 
  * [33] K. Kurita, N. Vyas, A. Pareek, A. W. Black, and Y. Tsvetkov.  Measuring Bias in Contextualized Word Representations.  arXiv:1906.07337 [cs], June 2019.  arXiv: 1906.07337. 
  * [34] P. P. Liang, C. Wu, L.-P. Morency, and R. Salakhutdinov.  Towards Understanding and Mitigating Social Biases in Language Models.  arXiv:2106.13219 [cs], June 2021.  arXiv: 2106.13219. 
  * [35] S. Lin, J. Hilton, and O. Evans.  TruthfulQA: Measuring How Models Mimic Human Falsehoods.  arXiv:2109.07958 [cs], Sept. 2021.  arXiv: 2109.07958. 
  * [36] A. Liu, M. Sap, X. Lu, S. Swayamdipta, C. Bhagavatula, N. A. Smith, and Y. Choi.  DExperts: Decoding-Time Controlled Text Generation with Experts and Anti-Experts.  arXiv:2105.03023 [cs], June 2021.  arXiv: 2105.03023. 
  * [37] K. McGuffie and A. Newhouse.  The Radicalization Risks of GPT-3 and Advanced Neural Language Models.  arXiv:2009.06807 [cs], Sept. 2020.  arXiv: 2009.06807. 
  * [38] L. McInnes, J. Healy, and J. Melville.  UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction, Sept. 2020.  arXiv:1802.03426 [cs, stat]. 
  * [39] P. Mishkin, L. Ahmad, M. Brundage, G. Krueger, and G. Sastry.  DALL·E 2 Preview - Risks and Limitations, 2022. 
  * [40] Y. Nie, A. Williams, E. Dinan, M. Bansal, J. Weston, and D. Kiela.  Adversarial NLI: A New Benchmark for Natural Language Understanding.  In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 4885–4901, Online, July 2020. Association for Computational Linguistics. 
  * [41] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. Christiano, J. Leike, and R. Lowe.  Training language models to follow instructions with human feedback, Mar. 2022.  arXiv:2203.02155 [cs]. 
  * [42] E. Perez, S. Huang, F. Song, T. Cai, R. Ring, J. Aslanides, A. Glaese, N. McAleese, and G. Irving.  Red Teaming Language Models with Language Models.  arXiv:2202.03286 [cs], Feb. 2022.  arXiv: 2202.03286. 
  * [43] J. W. Rae, S. Borgeaud, T. Cai, K. Millican, J. Hoffmann, F. Song, J. Aslanides, S. Henderson, R. Ring, S. Young, E. Rutherford, T. Hennigan, J. Menick, A. Cassirer, R. Powell, G. v. d. Driessche, L. A. Hendricks, M. Rauh, P.-S. Huang, A. Glaese, J. Welbl, S. Dathathri, S. Huang, J. Uesato, J. Mellor, I. Higgins, A. Creswell, N. McAleese, A. Wu, E. Elsen, S. Jayakumar, E. Buchatskaya, D. Budden, E. Sutherland, K. Simonyan, M. Paganini, L. Sifre, L. Martens, X. L. Li, A. Kuncoro, A. Nematzadeh, E. Gribovskaya, D. Donato, A. Lazaridou, A. Mensch, J.-B. Lespiau, M. Tsimpoukelli, N. Grigorev, D. Fritz, T. Sottiaux, M. Pajarskas, T. Pohlen, Z. Gong, D. Toyama, C. d. M. d’Autume, Y. Li, T. Terzi, V. Mikulik, I. Babuschkin, A. Clark, D. d. L. Casas, A. Guy, C. Jones, J. Bradbury, M. Johnson, B. Hechtman, L. Weidinger, I. Gabriel, W. Isaac, E. Lockhart, S. Osindero, L. Rimell, C. Dyer, O. Vinyals, K. Ayoub, J. Stanway, L. Bennett, D. Hassabis, K. Kavukcuoglu, and G. Irving.  Scaling Language Models: Methods, Analysis & Insights from Training Gopher.  arXiv:2112.11446 [cs], Dec. 2021.  arXiv: 2112.11446. 
  * [44] A. Ramesh, P. Dhariwal, A. Nichol, C. Chu, and M. Chen.  Hierarchical Text-Conditional Image Generation with CLIP Latents, Apr. 2022.  arXiv:2204.06125 [cs]. 
  * [45] M. T. Ribeiro, T. Wu, C. Guestrin, and S. Singh.  Beyond Accuracy: Behavioral Testing of NLP Models with CheckList.  In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 4902–4912, Online, July 2020. Association for Computational Linguistics. 
  * [46] P. Röttger, B. Vidgen, D. Nguyen, Z. Waseem, H. Margetts, and J. Pierrehumbert.  HateCheck: Functional Tests for Hate Speech Detection Models.  In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 41–58, Online, Aug. 2021. Association for Computational Linguistics. 
  * [47] M. Sap, S. Gabriel, L. Qin, D. Jurafsky, N. A. Smith, and Y. Choi.  Social Bias Frames: Reasoning about Social and Power Implications of Language.  arXiv:1911.03891 [cs], Apr. 2020.  arXiv: 1911.03891. 
  * [48] I. Solaiman and C. Dennison.  Process for Adapting Language Models to Society (PALMS) with Values-Targeted Datasets.  arXiv:2106.10328 [cs], Nov. 2021.  arXiv: 2106.10328. 
  * [49] M. Steiger, T. J. Bharucha, S. Venkatagiri, M. J. Riedl, and M. Lease.  The Psychological Well-Being of Content Moderators: The Emotional Labor of Commercial Moderation and Avenues for Improving Support.  In Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems, CHI ’21, pages 1–14, New York, NY, USA, May 2021. Association for Computing Machinery. 
  * [50] C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfellow, and R. Fergus.  Intriguing properties of neural networks, Feb. 2014.  arXiv:1312.6199 [cs]. 
  * [51] A. Tamkin, M. Brundage, J. Clark, and D. Ganguli.  Understanding the Capabilities, Limitations, and Societal Impact of Large Language Models.  arXiv:2102.02503 [cs], Feb. 2021.  arXiv: 2102.02503. 
  * [52] E. R. Thompson.  Development and Validation of an Internationally Reliable Short-Form of the Positive and Negative Affect Schedule (PANAS).  Journal of Cross-Cultural Psychology, 38(2):227–242, Mar. 2007.  Publisher: SAGE Publications Inc. 
  * [53] R. Thoppilan, D. De Freitas, J. Hall, N. Shazeer, A. Kulshreshtha, H.-T. Cheng, A. Jin, T. Bos, L. Baker, Y. Du, Y. Li, H. Lee, H. S. Zheng, A. Ghafouri, M. Menegali, Y. Huang, M. Krikun, D. Lepikhin, J. Qin, D. Chen, Y. Xu, Z. Chen, A. Roberts, M. Bosma, Y. Zhou, C.-C. Chang, I. Krivokon, W. Rusch, M. Pickett, K. Meier-Hellstern, M. R. Morris, T. Doshi, R. D. Santos, T. Duke, J. Soraker, B. Zevenbergen, V. Prabhakaran, M. Diaz, B. Hutchinson, K. Olson, A. Molina, E. Hoffman-John, J. Lee, L. Aroyo, R. Rajakumar, A. Butryna, M. Lamm, V. Kuzmina, J. Fenton, A. Cohen, R. Bernstein, R. Kurzweil, B. Aguera-Arcas, C. Cui, M. Croak, E. Chi, and Q. Le.  LaMDA: Language Models for Dialog Applications.  arXiv:2201.08239 [cs], Jan. 2022.  arXiv: 2201.08239. 
  * [54] C. US.  U.S. Census Bureau QuickFacts: United States, July 2021. 
  * [55] E. Wallace, A. Williams, R. Jia, and D. Kiela.  Analyzing Dynamic Adversarial Training Data in the Limit, Oct. 2021.  arXiv:2110.08514 [cs]. 
  * [56] D. Watson, L. A. Clark, and A. Tellegen.  Development and validation of brief measures of positive and negative affect: the PANAS scales.  Journal of Personality and Social Psychology, 54(6):1063–1070, June 1988. 
  * [57] L. Weidinger, J. Mellor, M. Rauh, C. Griffin, J. Uesato, P.-S. Huang, M. Cheng, M. Glaese, B. Balle, A. Kasirzadeh, Z. Kenton, S. Brown, W. Hawkins, T. Stepleton, C. Biles, A. Birhane, J. Haas, L. Rimell, L. A. Hendricks, W. Isaac, S. Legassick, G. Irving, and I. Gabriel.  Ethical and social risks of harm from Language Models.  arXiv:2112.04359 [cs], Dec. 2021.  arXiv: 2112.04359. 
  * [58] J. Welbl, A. Glaese, J. Uesato, S. Dathathri, J. Mellor, L. A. Hendricks, K. Anderson, P. Kohli, B. Coppin, and P.-S. Huang.  Challenges in Detoxifying Language Models.  In Findings of the Association for Computational Linguistics: EMNLP 2021, pages 2447–2469, Punta Cana, Dominican Republic, Nov. 2021. Association for Computational Linguistics. 
  * [59] H. Xu, Y. Ma, H. Liu, D. Deb, H. Liu, J. Tang, and A. K. Jain.  Adversarial Attacks and Defenses in Images, Graphs and Text: A Review, Oct. 2019.  arXiv:1909.08072 [cs, stat]. 
  * [60] J. Xu, D. Ju, M. Li, Y.-L. Boureau, J. Weston, and E. Dinan.  Bot-Adversarial Dialogue for Safe Conversational Agents.  In K. Toutanova, A. Rumshisky, L. Zettlemoyer, D. Hakkani-Tür, I. Beltagy, S. Bethard, R. Cotterell, T. Chakraborty, and Y. Zhou, editors, Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT 2021, Online, June 6-11, 2021, pages 2950–2968. Association for Computational Linguistics, 2021. 
  * [61] D. M. Ziegler, S. Nix, L. Chan, T. Bauman, P. Schmidt-Nielsen, T. Lin, A. Scherlis, N. Nabeshima, B. Weinstein-Raun, D. de Haas, B. Shlegeris, and N. Thomas.  Adversarial Training for High-Stakes Reliability, May 2022.  arXiv:2205.01663 [cs]. 


