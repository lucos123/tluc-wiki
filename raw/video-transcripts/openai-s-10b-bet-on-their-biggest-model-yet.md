---
title: "OpenAI's $10B Bet on their biggest model yet"
date: 2026-08-01
tags:
  - raw
  - video-transcript
source_type: video
url: "https://www.youtube.com/watch?v=KkDhn5Ixw5A"
channel: "Caleb Writes Code"
upload_date: "2026-07-14"
duration: "9m 14s"
---

# OpenAI's $10B Bet on their biggest model yet

**Channel**: Caleb Writes Code
**URL**: https://www.youtube.com/watch?v=KkDhn5Ixw5A
**Upload Date**: 2026-07-14
**Duration**: 9m 14s
**Transcript extracted**: 2026-08-01

---

## Transcript

When Sam Altman asked Andre Karpathy
whether LLM should be made smarter or
faster, his response was smarter model
as the answer. And many people would
probably prefer a smart model over a
fast model given the same option. And we
often look at benchmarks that show
intelligence before even look at the
speed. But what about speed? And how
fast should LLMs really be? Most
flagship models are currently served at
around 60 tokens per second looking at
OpenRouter. Opus 4.8 at around 60 tokens
per second, Fable 5 around 40 tokens per
second, and GPT 5.6 Soul also at around
40 tokens per second. Why can't
companies just simply push all their
flagship models from this band to a much
higher band like 750 tokens per second?
I mean, the difference between a 60
token per second on the left compared to
750 tokens per second on the right seems
pretty huge. So, shouldn't companies
like OpenAI, Anthropic, models
to run at much faster speed instead?
Typically, as you move towards the right
in the X axis here, the higher the
capital expenditure to actually achieve
them at scale. And this increased
capital expenditure comes down to the
cost of graphics cards. So, in a way,
there is this hardware barrier between
GPUs like Nvidia and AMD and more
specific chips like Rock and Cerebras
chips. And the price difference between
them is huge where Cerebras system can
easily cost 20 to 50 times more than
normal GPU configuration. And yet,
OpenAI is offering their GPT 5.6 Soul
model with both traditional GPUs at 40
to 50 tokens per second here and also at
750 tokens per second powered by
Cerebras chips. So, if companies like
OpenAI have to spend so much capital
expenditure to gain 18 to 20 times in
speed, why on earth is OpenAI offering
their model using Cerebras chips? OpenAI
actually already has a model that they
have been offering at more than 1,000
tokens per second called GPT 5.3 Codex
Spark, which was announced back in
February. And most people find this
model fast but dumb. Most likely because
they traded off less intelligent model
to run faster since they tend to be
smaller. So, until now, what we found is
that aggregate demand for faster LLMs
tend to dry up as you move to the right
of this x-axis since companies like
OpenAI push smaller models to the right
since it makes more economical sense.
And from the user side, most people
prefer to
served at 50 tokens per second rather
than 20 times faster but less
intelligent model on the right. So, if
that's true, did OpenAI just invert this
entire assumption by serving their
biggest and most intelligent model in
both spectrums here. But first, quick
shoutout for Merlin AI sponsoring this
video. Merlin AI is an all-in-one AI
tool and they're offering a special
heavy discount. As you continue to work
with AI, you realize that every AI tool
is good at something. So, sometimes you
go to chat GPT and other times you go to
Claude or even Gemini, which means my
conversations are all scattered. And
worse, I have to pay multiple
subscriptions at the same time. One
thing I find cool about Merlin is the
ability to actually choose all top AI
models to chat with while keeping my
conversation in one place. I can also
use their deep research feature to
expand on topics that I'm really
interested in. And Merlin is able to
help me generate this report on
semiconductors as you can see. And
pricing is really the big part. ChatGPT,
Claude, and Gemini each cost around $20
per month and paying for each really
adds up fast and most people don't fully
use up their credits. But Merlin AI
offers cheaper pricing since Merlin buys
API credits in bulk and charges only for
what users typically need. And right
now, you can get a 75% discount with
promo code and only pay $5 per month
until the deal lasts. Link in the
description below. OpenAI didn't
disclose the size of the GPT 5.6 sold,
but it's safe to assume that the model
is sized at at least 2 trillion
parameters and possibly up to 4 trillion
parameters in size, which by all measure
is a large model. And taking such large
model from 40 tokens per second and
moving it all the way to 750 tokens per
second is not for the faint of heart
because of the huge capital expenditure
along the way. One way to look at this
is by looking at the chart from Nvidia
where they broke down their system
showing the throughput on the Y axis and
responsiveness on the X axis. Now, if
this graph confuses you, you're not
alone. It took me a bit of practice to
frame my thinking to get this as well.
What you're seeing here essentially is
this. If you want to promise your users
to serve the model at, let's say, 340
tokens per second at all times using
Nvidia B300 chips can get you a
throughput at about 450,000 tokens per
second at the data center level with 1
MW power, which means you can have about
1,324
concurrent active users where every
single users will experience up to 340
tokens per second. So, as long as only
users access your system at the same
time, you can honor your word to your
customer that you will meet the 300
tokens per second SLA. What you're not
seeing here in this chart is the
Cerebrus chips. And even if we make an
educated guess to draw this line, say,
using the same Cerebrus chip can get you
450,000 tokens generated per second, but
at 750 tokens per second per user. In
this case, you can only have 600
concurrent active users, which is more
than two times less concurrent active
users compared to Nvidia, but the users
that do have access to Cerebrus chips
are generated at more than two times the
speed. And assuming GPT-5.6 Soul is a 2
trillion parameter model, which is a low
estimation, the hardware cost just to
fit the model with Nvidia chips is 14
Nvidia B300 chips, and in the case of
Cerebrus, 90 WSE-3 chips, and the cost
difference here is huge. So, is this
thing even worth it for OpenAI just to
provide their most capable model at
lightning speed? Here's where things get
interesting. Currently, Codex already
offers an option to run the model at 1.5
times the speed, and it explicitly says
that it will draw more usage in
exchange. And the keyword here is usage.
In order for OpenAI to drive their
revenue, they need to encourage more of
their users away from free subscription
and convert them to the $200 per month
pro membership. And one of the best way
to push their users in that direction is
by draining their usage faster, leaving
more users wanting more token allowance
by signing up for higher plans. And
going back to our price difference
between Nvidia GPU and Cerebrus chips,
the capex in this case for OpenAI isn't
actually in the hardware cost since they
didn't buy Cerebrus chips, but instead
they made a $10 billion deal with
Cerebrus to rent their 750 MW worth of
compute from their data center through
2028, which means OpenAI has the next 30
months to make this $10 billion deal
worth the price tag. And a large portion
of OpenAI's revenue source comes from
the ChatGPT subscription. So, for the
sake of simple analysis here, let's
assume that OpenAI will only serve their
Cerebrus chip-backed GPT 5.6 soul
through their subscription model only.
Though in reality, they'll probably
collect revenue from all three sources.
OpenAI's $200 per month pro membership
would bring them about $6,000 per users
for the next 30 months, which means they
have to theoretically convert about 1.6
million users to the pro membership,
which is about 0.16%
of their 1 billion monthly active users.
And the fastest way to get this
conversion is by draining their token
allowance and setting a premium cost for
processing your requests faster through
Cerebrus chips instead. Like we saw
earlier, OpenAI already charges their
users higher usage when they select 1.5x
speed, but for the same tokens at the
end of the day. So, effectively,
Cerebras chips that offer up to 750
tokens per second SLA, which practically
for the users could be 18.5 times speed
up, which is huge. And it'll likely
drain your token allowance that much
faster, depending on how optimized Open
AI actually made their model to run on
Cerebras chips. Now, like I said, in
reality, their revenue will probably be
collected not just from subscription
alone, but through business and API as
well. And beyond Codex through
subscription, people might deploy a
low-latency app through API, reaching
Cerebras chip for workflows that need a
fast inference. So, these would all
collectively create demand for Cerebras
chips separate to the back of the napkin
math that we just did on subscription
revenue thesis alone. Now, one element
we haven't discussed is token efficiency
or cost of tokens, which adds yet
another dimension to this entire
equation and changes the economics
upside down once again. More and more
models like Grok 4.5 that we just saw
from SpaceX AI are becoming token
efficient, where models use less tokens
to get the same job done. So, in a way,
token efficiency works diametrically
opposite to token speed, at least from
the Frontier Labs who are trying to
encourage more token usage for higher
revenue. All of these are, I think, such
interesting factors to consider as the
AI race continues to unfold and we're
seeing more competition driving Frontier
Labs to not only offer their models
smarter, but also faster and also more
cost-efficient.
