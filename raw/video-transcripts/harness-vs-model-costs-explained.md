---
title: "Harness vs Model costs explained.."
date: 2026-08-12
tags:
  - raw
  - video-transcript
source_type: video
url: "https://www.youtube.com/watch?v=8ji5vURIllM"
channel: "Caleb Writes Code"
upload_date: "2026-08-12"
duration: "9m 39s"
---

# Harness vs Model costs explained..

**Channel**: Caleb Writes Code
**URL**: https://www.youtube.com/watch?v=8ji5vURIllM
**Upload Date**: 2026-08-12
**Duration**: 9m 39s
**Transcript extracted**: 2026-08-12

---

## Transcript

Back when OpenAI announced their first
reasoning model 01, the cost of
intelligence was pretty expensive even
by today's standard. Fast forward to
about two years later, GPT 5.6 Soul is
not only about two to three times
cheaper, GBT 5.6 is significantly better
in performance. So clearly the cost of
intelligence has dropped by a lot. And
as a consequence, somewhat mirroring
Jeban's paradox, the falling cost of
intelligence allowed more people to use
AI given how accessible it became. But
there's another angle worth considering
here, and that's the AR race between
open and closed proprietary models. Open
models were notoriously behind in
comparison to closed models when it
comes to performance by about 6 to 18
months depending on the time frame that
you look at. And it wasn't until 2025
when open models really started to
compete. And in 2026, with the rise of
models like Kim K3, Quen 3.8 Max,
DeepSync V4, and GLM 5.2, two open
models have now become a strong
alternative, especially looking at how
they're taking up so much space in the
leaderboard, as you can see. But the
cost of the model is very different than
the cost of the harness that surrounds
the model. Most people that use AI
through chat, the harness is very thin,
meaning you're almost working directly
with the model. And that's still the
dominant way that most people use AI.
But a small majority of the people or
early adopters of AI use a much thicker
harness like claude code, cursor, open
code, code codex and client. And this in
comparison, you're no longer working
directly with the model, but instead
you're working through this external
medium called the harness. And there's a
huge difference in cost when we compare
the two use cases where according to
Enthropic, you can spend four to 15
times more in cost just by virtue of
using an agent or multi- aent systems.
Take a look at this short prompt that I
just created. This prompt asks my
harness to create a file containing the
alphabet. And it takes about 25 tokens
in total, which is extremely small.
Which means even at Opus 5's pricing,
this prompt that I just created should
only cost about 0.00001
to 5, which is extremely cheap. And the
model responds back with, let's say, 500
tokens. The total cost is still 1 cent.
But when I bring the same prompt over to
Cloud Code, for example, with a thicker
harness, the cost immediately jumps to
37 cents for the entire exchange, which
is nearly 30 times more expensive right
off the bat. The biggest contributor to
this kind of price jump is the overhead
that exists in the harness layer.
Harnesses like Cloud Code, Pi, Open
Code, Klein, and Cursor add anything
from 8,000 to 30,000 tokens on all
messages going to the model. sort of
like a toll you have to pay in order to
get to the model. And this very overhead
is called a system prompt. And every
single harness has some amount of system
prompt. Harnesses like cloud code tend
to have a bigger system prompt because
as we all know, cloud code comes with a
lot of features out of the box. Like you
can see from this list of commands that
cloud code comes with. And each of these
features need to be described in the
system prompt so that the model
understands how to interact with that
harness. So when I give these coding
agents but give them the same prompt
from earlier and using the same Opus 5
model, you think that the price to get
the job done should be around the same
but in reality they fluctuate a lot
where cloud code costs about 37, open
code costs about 11, client costs 7 and
PI costs about 2.5. Pretty wide gap here
in pricing depending on what harness I
choose. Now harnesses like client are
open source. So you can directly go to
their repository on GitHub to actually
read how long and also how they
structure their system prompt to
understand how it works under the hood.
And one thing to keep in mind when it
comes to using a harness is that your
prompt isn't just sent once to the model
and the model then responds back in a
single turn. While this might be common
in a chat application, in agentic
applications, there's actually a bit of
oscillation that happens back and forth
between the model, just like a loop that
goes recursively between the harness and
the model until the model finally
decides that the job is done. For
example, my initial request might go to
the model and the model might decide to
first check if the file already exists
in my computer. And the harness will
then go ahead and check my computer and
send the result back to the model. And
the model then ask the harness again to
create a file. And the harness will then
go to my computer and actually create
the file. And finally, the model will
ask the harness to write the contents in
the file that it just created. As you
can see, there's a lot of back and forth
for even a simple task that happens
between the harness and the model. And
for longer duration tasks, like creating
an entire website from scratch that
could easily take 10 to 20 minutes in
one shot, you can imagine just how many
round trips that might happen between
the harness and the model until the
website is finally created. And each
trip here costs a lot of money since
every message going to the model not
only contains information about my
computer but also a large system prompt
as we discussed earlier that acts like a
tollgate. But what if there was a way to
reduce the pricing here by simply
caching our prompt so that even when we
send a large payload to the model, we
can just reuse the previously calculated
stored cache to save time and save cost.
This is actually extremely common among
inference providers that offer prompt
caching which is important for
harnessings. As you can imagine,
leveraging this prompt caching feature
where the server temporarily holds the
KV cache can save a lot of cost for
users who are trying to maximize their
subscription or API costs. And that's
why when we go to websites like
anthropics pricing page that shows API
costs across their models, it shows you
different pricing for prompt caching. In
fact, Enthropic offers up to one hour
prompt caching at a higher pricing as
well, which gives harnesses the ability
to save costs on tasks that might take
longer, like building an entire website
or deep researching a topic. And from
the infrastructure side, proming could
actually be pretty lucrative if you
think about it from anthropic side. A
single Nvidia H100 GPU easily retails
for $3 per hour for rentals. And
depending on the KV cache quantization,
you could easily fit an entire 1 million
context window into a single H100. Which
means even if Enthropic secures 12
different spots for the 1 million
context window to be stored for 5
minutes each, the hourly revenue for
prompt caching for an single H100 card
is around $70 per hour, which is huge.
The biggest assumption here, of course,
is that if Enthropic could find a way to
quantize a 1 million context into a
single H100 card that offers 80 GB of
VRAM, but that's kind of beside the
point. Now, the pricing model changes a
bit when we get into 1 hour cash rights
because reserving an hour of GPU time
can be quite expensive. And my
assumption here is that Enthropic
probably kicks out an unused memory from
GPU to a nearby SSD since memory is
cheaper long-term there. and just simply
load them back up to the GPU based on
demand as the harness requires it, which
is why they can offer a much cheaper $10
per million input token rights. Now, as
much as all of this is really
fascinating to talk about, you probably
wouldn't even want to think about this
when we're using coding agents. And
common ways vendors use to keep their
people within the walled garden is by
offering a subscription model on their
model layer and letting the harness be
used under that subscription. Frontier
apps like Chachib, Claude, Gemini all
offer subscription. In this way, you're
not having an anxiety attack in the
middle of your work wondering how much
your agent is actually spending, but
instead you're drawing your AI use cases
without worrying about cost since usage
limits will be refreshed periodically.
Enthropic might offer a subscription
that bundles all their models under
their pro plan for $20 a month, allowing
users to use different harnesses like
Cloud Code, Cloud Co-work, and Cloud
Chat. all under that same subscription.
And with this subscription, you also
have the ability to swap out different
anthropic models like Opus, Sonnet, and
Haiku. And for the time being, Fable
having its own usage window as well.
Same thing for OpenAI where you can use
OpenAI's Chachd Plus subscription to use
Chachd Codeex and more. And at the same
time, mixing different models all
metered based on the same subscription
model. But what if you wanted a more
flexible subscription plan that doesn't
lock you in to a specific vendor? And
also, we saw earlier in the video how
openweight models are catching up in
leaderboard. What if I wanted to have a
subscription plan that lets me try openw
weightights models with various
harnesses? That's why you need to try
client pass, the sponsor of today's
video. Klein Pass is a subscription
model that allows you to group many
openweight models under the same plan.
Klein Pass has models like Kim K3, GLM
5.2, to DeepSc V4 Pro within one
subscription model. This means you now
have a subscription curated for new
openweight models that get introduced
and you can all work within one
subscription that is metered based on
usage. And you can also bring your
client pass to other harnesses, which
means your subscription is not limited
to client's harness, but you can carry
your client pass subscription to
different harnesses that you might use
on a daily basis instead. And for a
limited time, you can get a $1.99 first
month just for you guys and then $9.99
per month after that. I'll have the link
in the description below for you to try
out climb
