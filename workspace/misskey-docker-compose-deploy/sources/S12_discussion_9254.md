---
url: "https://github.com/misskey-dev/misskey/discussions/9254"
title: "Changing Instance Domain · misskey-dev/misskey · Discussion #9254 · GitHub"
scraped_at: 2026-09-15T12:30:34+00:00
---

[Skip to content](https://github.com/misskey-dev/misskey/discussions/9254#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/misskey-dev/misskey/discussions/9254) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/misskey-dev/misskey/discussions/9254) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/misskey-dev/misskey/discussions/9254) to refresh your session. Dismiss alert
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).
/ Public
  * ###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).
  * [ Notifications ](https://github.com/login?return_to=%2Fmisskey-dev%2Fmisskey) You must be signed in to change notification settings
  * [ Fork 1.6k ](https://github.com/login?return_to=%2Fmisskey-dev%2Fmisskey)
  * [ Star  11.3k ](https://github.com/login?return_to=%2Fmisskey-dev%2Fmisskey)


#  Changing Instance Domain  #9254
[ icecake0107  ](https://github.com/icecake0107) asked this question in [Q&A](https://github.com/misskey-dev/misskey/discussions/categories/q-a)
[ Changing Instance Domain ](https://github.com/misskey-dev/misskey/discussions/9254#top) #9254
[ icecake0107  ](https://github.com/icecake0107)
Dec 3, 2022 · 1 comments · 4 replies 
[ Answered ](https://github.com/misskey-dev/misskey/discussions/9254#discussioncomment-4301304) [Return to top](https://github.com/misskey-dev/misskey/discussions/9254#top)
Discussion options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).


Quote reply
edited
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).


## 
[ icecake0107 ](https://github.com/icecake0107) [ Dec 3, 2022 ](https://github.com/misskey-dev/misskey/discussions/9254#discussion-4623854)  
|  Hi dear Misskey friends, I have a Misskey instance running but I would like to change the domain (from `foo.com` to `bar.io`). I am not sure what the impact would be to the existing accounts, like for a user's Following & Followers/Avatar..., do they need to reconnect after the domain change? 🤔 If so how to do that? Thanks in advance! 😄  |  
| --- |  
You must be logged in to vote
All reactions
Answered by [ ThatOneCalculator ](https://github.com/ThatOneCalculator) [ Dec 3, 2022 ](https://github.com/misskey-dev/misskey/discussions/9254#discussioncomment-4301304)
I would highly recommend _**not**_ changing your URL. Due to how the Fediverse/ActivityPub works, changing your URL will most likely result in entirely broken federation.
##  Replies:  1 comment  · 4 replies 
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).


Quote reply
### 
[ ThatOneCalculator ](https://github.com/ThatOneCalculator) [ Dec 3, 2022 ](https://github.com/misskey-dev/misskey/discussions/9254#discussioncomment-4301304)  
|  I would highly recommend _**not**_ changing your URL. Due to how the Fediverse/ActivityPub works, changing your URL will most likely result in entirely broken federation.  |  
| --- |  
Marked as answer 
You must be logged in to vote
All reactions
4 replies 
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).


Quote reply
edited
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).


#### 
[codingneko](https://github.com/codingneko) [ Nov 12, 2023 ](https://github.com/misskey-dev/misskey/discussions/9254#discussioncomment-7546613)  
|  You did change yours tho, how'd you do it? I'm curious  |  
| --- |  
All reactions
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).


Quote reply
#### 
[ThatOneCalculator](https://github.com/ThatOneCalculator) [ Nov 12, 2023 ](https://github.com/misskey-dev/misskey/discussions/9254#discussioncomment-7546972)  
| 
  1. I changed it with my servers running Firefish, not Misskey
  2. The whole process involved multiple custom scripts talking both to the server API and the database directly and was overall extremely janky. I wouldn't recommend that anyone try and recreate what I did tbh.

 |  
| --- |  
All reactions
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).


Quote reply
#### 
[codingneko](https://github.com/codingneko) [ Nov 12, 2023 ](https://github.com/misskey-dev/misskey/discussions/9254#discussioncomment-7547268)  
|  I honestly don't consider myself knowledgable enough to even attempt this, but it still amazes ms to this day you could do it. Also, can't remember this... you did the migration about 4 months ago right? do all Firefish accounts show up as 4 months old in remote instances? or were you able to make remote instances know the real creation dates of the accounts? 🤔  |  
| --- |  
All reactions
Comment options
###  Uh oh! 
There was an error while loading. [Please reload this page](https://github.com/misskey-dev/misskey/discussions/9254).


Quote reply
#### 
[ThatOneCalculator](https://github.com/ThatOneCalculator) [ Nov 12, 2023 ](https://github.com/misskey-dev/misskey/discussions/9254#discussioncomment-7547430)  
|  It was neither 4 months ago nor the real dates, because it reused data from calckey.social. The database from calckey.social and firefish.social are carbon-copies that were kept in-sync until the migration was complete, meaning no user data, remote or local, was ever altered in a meaningful way.  |  
| --- |  
All reactions
Answer selected by [icecake0107](https://github.com/icecake0107)
[Sign up for free](https://github.com/join?source=comment-repo) **to join this conversation on GitHub**. Already have an account? [Sign in to comment](https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fmisskey-dev%2Fmisskey%2Fdiscussions%2F9254)
Category 
Labels 
None yet 
3 participants 
You can’t perform that action at this time. 
