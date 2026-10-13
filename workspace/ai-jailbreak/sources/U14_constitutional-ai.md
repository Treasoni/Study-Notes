[Skip to main content](https://arxiv.org/abs/2212.08073#content)
Press Enter to search · [Advanced search](https://arxiv.org/search/advanced)
# Computer Science > Computation and Language
**arXiv:2212.08073** (cs) 
[Submitted on 15 Dec 2022]
#  Title:Constitutional AI: Harmlessness from AI Feedback
Authors:[Yuntao Bai](https://arxiv.org/search/cs?searchtype=author&query=Bai,+Y), [Saurav Kadavath](https://arxiv.org/search/cs?searchtype=author&query=Kadavath,+S), [Sandipan Kundu](https://arxiv.org/search/cs?searchtype=author&query=Kundu,+S), [Amanda Askell](https://arxiv.org/search/cs?searchtype=author&query=Askell,+A), [Jackson Kernion](https://arxiv.org/search/cs?searchtype=author&query=Kernion,+J), [Andy Jones](https://arxiv.org/search/cs?searchtype=author&query=Jones,+A), [Anna Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+A), [Anna Goldie](https://arxiv.org/search/cs?searchtype=author&query=Goldie,+A), [Azalia Mirhoseini](https://arxiv.org/search/cs?searchtype=author&query=Mirhoseini,+A), [Cameron McKinnon](https://arxiv.org/search/cs?searchtype=author&query=McKinnon,+C), [Carol Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+C), [Catherine Olsson](https://arxiv.org/search/cs?searchtype=author&query=Olsson,+C), [Christopher Olah](https://arxiv.org/search/cs?searchtype=author&query=Olah,+C), [Danny Hernandez](https://arxiv.org/search/cs?searchtype=author&query=Hernandez,+D), [Dawn Drain](https://arxiv.org/search/cs?searchtype=author&query=Drain,+D), [Deep Ganguli](https://arxiv.org/search/cs?searchtype=author&query=Ganguli,+D), [Dustin Li](https://arxiv.org/search/cs?searchtype=author&query=Li,+D), [Eli Tran-Johnson](https://arxiv.org/search/cs?searchtype=author&query=Tran-Johnson,+E), [Ethan Perez](https://arxiv.org/search/cs?searchtype=author&query=Perez,+E), [Jamie Kerr](https://arxiv.org/search/cs?searchtype=author&query=Kerr,+J), [Jared Mueller](https://arxiv.org/search/cs?searchtype=author&query=Mueller,+J), [Jeffrey Ladish](https://arxiv.org/search/cs?searchtype=author&query=Ladish,+J), [Joshua Landau](https://arxiv.org/search/cs?searchtype=author&query=Landau,+J), [Kamal Ndousse](https://arxiv.org/search/cs?searchtype=author&query=Ndousse,+K), [Kamile Lukosuite](https://arxiv.org/search/cs?searchtype=author&query=Lukosuite,+K), [Liane Lovitt](https://arxiv.org/search/cs?searchtype=author&query=Lovitt,+L), [Michael Sellitto](https://arxiv.org/search/cs?searchtype=author&query=Sellitto,+M), [Nelson Elhage](https://arxiv.org/search/cs?searchtype=author&query=Elhage,+N), [Nicholas Schiefer](https://arxiv.org/search/cs?searchtype=author&query=Schiefer,+N), [Noemi Mercado](https://arxiv.org/search/cs?searchtype=author&query=Mercado,+N), [Nova DasSarma](https://arxiv.org/search/cs?searchtype=author&query=DasSarma,+N), [Robert Lasenby](https://arxiv.org/search/cs?searchtype=author&query=Lasenby,+R), [Robin Larson](https://arxiv.org/search/cs?searchtype=author&query=Larson,+R), [Sam Ringer](https://arxiv.org/search/cs?searchtype=author&query=Ringer,+S), [Scott Johnston](https://arxiv.org/search/cs?searchtype=author&query=Johnston,+S), [Shauna Kravec](https://arxiv.org/search/cs?searchtype=author&query=Kravec,+S), [Sheer El Showk](https://arxiv.org/search/cs?searchtype=author&query=Showk,+S+E), [Stanislav Fort](https://arxiv.org/search/cs?searchtype=author&query=Fort,+S), [Tamera Lanham](https://arxiv.org/search/cs?searchtype=author&query=Lanham,+T), [Timothy Telleen-Lawton](https://arxiv.org/search/cs?searchtype=author&query=Telleen-Lawton,+T), [Tom Conerly](https://arxiv.org/search/cs?searchtype=author&query=Conerly,+T), [Tom Henighan](https://arxiv.org/search/cs?searchtype=author&query=Henighan,+T), [Tristan Hume](https://arxiv.org/search/cs?searchtype=author&query=Hume,+T), [Samuel R. Bowman](https://arxiv.org/search/cs?searchtype=author&query=Bowman,+S+R), [Zac Hatfield-Dodds](https://arxiv.org/search/cs?searchtype=author&query=Hatfield-Dodds,+Z), [Ben Mann](https://arxiv.org/search/cs?searchtype=author&query=Mann,+B), [Dario Amodei](https://arxiv.org/search/cs?searchtype=author&query=Amodei,+D), [Nicholas Joseph](https://arxiv.org/search/cs?searchtype=author&query=Joseph,+N), [Sam McCandlish](https://arxiv.org/search/cs?searchtype=author&query=McCandlish,+S), [Tom Brown](https://arxiv.org/search/cs?searchtype=author&query=Brown,+T), [Jared Kaplan](https://arxiv.org/search/cs?searchtype=author&query=Kaplan,+J)
View a PDF of the paper titled Constitutional AI: Harmlessness from AI Feedback, by Yuntao Bai and 50 other authors
[View PDF](https://arxiv.org/pdf/2212.08073) [HTML (experimental)](https://arxiv.org/html/2212.08073v1)
> Abstract:As AI systems become more capable, we would like to enlist their help to supervise other AIs. We experiment with methods for training a harmless AI assistant through self-improvement, without any human labels identifying harmful outputs. The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'. The process involves both a supervised learning and a reinforcement learning phase. In the supervised phase we sample from an initial model, then generate self-critiques and revisions, and then finetune the original model on revised responses. In the RL phase, we sample from the finetuned model, use a model to evaluate which of the two samples is better, and then train a preference model from this dataset of AI preferences. We then train with RL using the preference model as the reward signal, i.e. we use 'RL from AI Feedback' (RLAIF). As a result we are able to train a harmless but non-evasive AI assistant that engages with harmful queries by explaining its objections to them. Both the SL and RL methods can leverage chain-of-thought style reasoning to improve the human-judged performance and transparency of AI decision making. These methods make it possible to control AI behavior more precisely and with far fewer human labels.   
| Subjects:  |  Computation and Language (cs.CL); Artificial Intelligence (cs.AI)  |  
| --- | --- |  
| Cite as:  | [arXiv:2212.08073](https://arxiv.org/abs/2212.08073) [cs.CL]  |  
| (or  [arXiv:2212.08073v1](https://arxiv.org/abs/2212.08073v1) [cs.CL] for this version)   |  
|  <https://doi.org/10.48550/arXiv.2212.08073> Focus to learn more arXiv-issued DOI via DataCite  |  
## Submission history
From: Jared Kaplan [[view email](https://arxiv.org/show-email/7a8c5024/2212.08073)] **[v1]** Thu, 15 Dec 2022 06:19:23 UTC (1,083 KB) 
Full-text links:
## Access Paper:
View a PDF of the paper titled Constitutional AI: Harmlessness from AI Feedback, by Yuntao Bai and 50 other authors


[ view license ](http://creativecommons.org/licenses/by/4.0/ "Rights to this article")
### Current browse context:
cs.CL
Change to browse by: 
### References & Citations


### [ 2 blog links](https://arxiv.org/tb/2212.08073)
([what is this?](https://info.arxiv.org/help/trackback.html)) 
export BibTeX citation Loading...
## BibTeX formatted citation
×
loading...
Data provided by: 
### Bookmark
Bibliographic Tools
# Bibliographic and Citation Tools
Bibliographic Explorer Toggle
Bibliographic Explorer _([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))_
Connected Papers Toggle
Connected Papers _([What is Connected Papers?](https://www.connectedpapers.com/about))_
Litmaps Toggle
Litmaps _([What is Litmaps?](https://www.litmaps.co/))_
scite.ai Toggle
scite Smart Citations _([What are Smart Citations?](https://www.scite.ai/))_
Code, Data, Media
# Code, Data and Media Associated with this Article
alphaXiv Toggle
alphaXiv _([What is alphaXiv?](https://alphaxiv.org/))_
Links to Code Toggle
CatalyzeX Code Finder for Papers _([What is CatalyzeX?](https://www.catalyzex.com))_
DagsHub Toggle
DagsHub _([What is DagsHub?](https://dagshub.com/))_
GotitPub Toggle
Gotit.pub _([What is GotitPub?](http://gotit.pub/faq))_
Huggingface Toggle
Hugging Face _([What is Huggingface?](https://huggingface.co/huggingface))_
ScienceCast Toggle
ScienceCast _([What is ScienceCast?](https://sciencecast.org/welcome))_
Demos
# Demos
Replicate Toggle
Replicate _([What is Replicate?](https://replicate.com/docs/arxiv/about))_
Spaces Toggle
Hugging Face Spaces _([What is Spaces?](https://huggingface.co/docs/hub/spaces))_
Spaces Toggle
TXYZ.AI _([What is TXYZ.AI?](https://txyz.ai))_
Related Papers
# Recommenders and Search Tools
Link to Influence Flower
Influence Flower _([What are Influence Flowers?](https://influencemap.cmlab.dev/))_
Core recommender toggle
CORE Recommender _([What is CORE?](https://core.ac.uk/services/recommender))_


About arXivLabs 
# arXivLabs: experimental projects with community collaborators
arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.
Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.
Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).
[Which authors of this paper are endorsers?](https://arxiv.org/auth/show-endorsers/2212.08073) | [Disable MathJax](javascript:setMathjaxCookie\(\)) ([What is MathJax?](https://info.arxiv.org/help/mathjax.html)) 


<!-- 来源: https://arxiv.org/abs/2212.08073 -->
