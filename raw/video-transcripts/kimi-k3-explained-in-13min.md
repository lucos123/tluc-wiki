---
title: "Kimi K3 explained in 13min.."
date: 2026-08-01
tags:
  - raw
  - video-transcript
source_type: video
url: "https://www.youtube.com/watch?v=rD20wJkPUB4"
channel: "Caleb Writes Code"
upload_date: "2026-07-21"
duration: "13m 20s"
---

# Kimi K3 explained in 13min..

**Channel**: Caleb Writes Code
**URL**: https://www.youtube.com/watch?v=rD20wJkPUB4
**Upload Date**: 2026-07-21
**Duration**: 13m 20s
**Transcript extracted**: 2026-08-01

---

## Transcript

The DeepSeek moment back in January 2025
was a pretty big deal. Not just because
DeepSeek practically caught up to OpenAI
when it comes to benchmarks, but it's
also the fact that DeepSeek trained
their model for a fraction of the cost
if you consider only the GPU rental
costs. Similarly, Qwen 1.5 has now
nearly caught up to Anthropic and
OpenAI, but not just in benchmarks, but
it's casting a broader question around
who will be leading AI innovation in the
model layer of the AI stack. People want
to know whether Chinese models will
become the next frontier in the AI race,
and how Chinese models like Qwen 1.5
will affect the demand for intelligence
from the application layer. These are
certainly interesting discussions to
talk about, and we can make a lot of fun
conjectures to debate how the rest of
the industry might shape up to. But,
what's really impressive about Qwen 1.5
is not just in the benchmarks alone, but
how it affects the layers below as we
look at the semiconductor industry and
how the economics of inference looks
like. So, in order to look at the bigger
picture, we have to look at the model
architecture and see how the ground is
shifting underneath us. And at a high
level, Qwen 1.5 is all about efficiency
and intelligence. And since there's a
lot to go through, let's start with what
we already all know, and then build our
understanding from there. Quick
disclaimer, this video does get slightly
more technical than usual as the video
goes on. But, I really think it's
important to at least get a grasp on why
innovations coming from Qwen 1.5 is so
unique. So, let's start by grounding our
discussion from what we all know, or at
least heard of by now, which is mixture
of experts. Ever since around 2024,
mixture of experts started to become
adopted as the industry standard, and a
large majority of models now use mixture
of experts at the core. The idea behind
mixture of experts is to activate only a
small portion of the model instead of
the entire model, largely to reduce the
compute overhead to process each token.
Now, depending on the model that you
choose, you'll have different levels of
sparsity of experts. Minimax M3
activates around 3.1% of experts.
Incline from Thinking Machine at 3.1%
Neumotron 3 Ultra activates around 4.3%
and now Chimera 3 around 1.8% expert
activated, which makes this model not
just the biggest in size among open
models, but one of the smallest
activation ratios. Chimera 3 is divided
into 896 experts and only 16 experts are
activated per token, which is how they
got to 1.8% activation ratio at any
given time. And even comparing this
model to their previous Chimera 2 model,
which was a 1 trillion parameters in
size, they not only grew their number of
experts more than double while
decreasing the activation of experts
from 2% to 1.8%, which goes to show how
they scale their model in size without
sacrificing efficiency. So, the question
is how does this efficiency here
actually look like when we run them on
GPUs in data centers. In other words,
does the efficiency also carry out when
it comes to inference? A model like
Chimera 3 that's this big is typically
spread across many GPUs in data centers.
Even at a lower precision, the model's
weight alone is scattered across nearly
six GPUs in Nvidia DGX B300 setup. And
this leaves very little room for the
context windows to be stored in the form
of KB cache and more. So, in a more
realistic deployment setup, your experts
will typically be spread across
supernode of 64 GPUs, which is what they
recommend, or even Nvidia NVL72
configuration containing 72 chips in a
single rack, which means every token
that passes through the model could be
doing many trips across GPUs
interconnected within the rack because
experts are spread across a wide array
of GPUs, which means now token will need
to travel from GPU to GPU to activate
experts that are scattered. And every
time data moves from one GPU to another
GPU, it adds a communication overhead.
KimiK3 added what's called Stable Latent
MoE, building on top of Mixture of
Experts. And if you have seen my recent
video on NeMoTron, it's very similar to
NeMoTron's Latent MoE, where the token
embedding is compressed into a lower
latent representation. Since token needs
to travel from GPU to GPU, having a much
more compressed token representation
helps reduce the communication overhead
depending on the compression ratio. And
since our token is compressed into a
lower dimension, it reduces the amount
of data that's actually passed between
the GPUs and also the compute that's
performed on them since the dimension is
reduced as well. This is what Latent MoE
does. We can see it from their diagram
of KimiK3 showing the down projection of
the token first, routed to experts with
two shared experts that's always
activated by default, and flowing the
rest through the pool of experts here.
And later, it gets projected back up to
the original dimension for softmax. And
this pool of experts that you see here
is typically spread across many GPUs in
a server. And the word stable in stable
latent MoE here likely refers to their
efforts in stabilizing the router during
training when it comes to selecting the
experts. Since KimiK3 practically split
the model into 896 experts, selecting
only 16 experts from a huge list of
experts is not a trivial task. The
router needs to consider the whole list
of experts with their own scores and
choose. And even a small variation can
throw off the router big time. In other
words, you can't have this many experts
and select this little without a strong
mechanism that help keep the balance in
training. Instead of using popular
methods like in the case of Deep Seek 33
or NeMoTron 3 Ultra that use bias to
nudge the router to pick experts by
penalizing overused experts and
promoting underused experts to reach
equilibrium, KimiK3 improved the
selection mechanism by using what's
called quantile balancing, which helps
expert allocation directly from the
distribution of router scores, kind of
like making each expert take the LSAT
and grading them by percentile curve,
rather than comparing them using a fixed
raw scores. This helps the router decide
which expert should be selected relative
to the rest of the experts in score.
Okay, the next component we'll get into
for Kimi K3 is this bottom left section
of the diagram. And this is really the
meat and bone when it comes to why Kimi
K3 is such a beautifully crafted model.
This section right here is what helped
contribute Kimi K3 to maintain six-time
decoding throughputs, while also scoring
higher than the status quo without
sacrificing the speed. And what makes
this entire thing possible is what's
called Kimi Delta attention, or KDA for
short. And surprisingly, KDA has already
been around since October 2025. So, Kimi
K3 essentially adopts what they already
reached 9 months ago into their new
model, but at a much bigger scale. So,
how does KDA really work? Because it
seems like it works really well. The
keyword here is the letter A, attention.
I'm sure we all heard of by now that
attention is expensive. But we also love
a model that can offer a 1 million
context window at the application layer.
And even here in the US, where we have
much more compute available, offering a
model at 1 million context window
without modifying the attention is sort
of foolish. The technical terminology
that we use is making something
quadratic complexity into sub-quadratic
or even linear. And there are so many
different ways that researchers have
contributed to make this happen. And one
of them is called linear attention. And
linear attention works exactly how it
sounds. How do we make our growing
compute demand more manageable as the
model scales? Models like Nemotron 3
uses what's called Mamba 2, which
replaces some of its attention layer
that's known to be expensive with a
recurrent state space memory. If this
sounds gibberish to you, basically the
core idea is having a predefined memory
cell where new information coming in
updates the old memory while old memory
is erased at a learned rate following a
decay schedule. For those who are
mathematically inclined, the equation
would look something like this where
alpha determines how much previous
memory has decayed and the new
information writes the current memory on
top. You might notice that this sounds a
lot like recurrent neural network and it
practically is, at least in how memory
is stored by the model. And this will
become more important later in the video
when we get into exactly how Kim i K3
optimizes even further. Now, building on
this learned decay idea, what if instead
of rewriting the memory with the new
value, we find the error instead and
only apply that error to correct our
memory to make sure that this is all
efficient. This method is called gated
delta net, which improves the decay
rule, as you can see, to not only decay
old memories according to schedule, but
also efficiently update the error
between its value and the predicted. So,
using gated delta net, we have more
efficiency in how the memory is updated.
And reading through the paper for gated
delta net, it explicitly says that the
challenge still is implementing gated
delta in a hardware efficient manner.
So, now we finally get to Kim i delta
attention, which is what Kim i K3
incorporates in their model. And
mathematically, Kim i delta simply
replaces the decay control in the gated
delta net with a function that gives you
a much more fine-grained control over
how memory is exactly decayed and
actually carries out through each
channel. Gated delta net couldn't
independently control how much
information is retained and forgotten,
and KDA essentially allows more granular
control of how information is actually
retained and forgotten channel by
channel at different rates. And in Kim
i's case, they interleave the Kim i
delta attention at a 3:1 ratio following
their ablation study that helped them
pick the more ideal ratio. And you can
see in the diagram here where they have
three KDA layers with one global
attention called gated MLA, making this
a hybrid linear attention by definition.
I mentioned earlier how this looks a lot
like a recurrent neural network. And the
reason why it's important here is
because when it comes to training, one
of the biggest drawbacks with RNN was
its inefficiency in training compared to
transformers because of the sequential
nature that made training difficult due
to temporal dependence. Following the
original paper in gated Delta net that
used chunk-wise parallel to optimize on
training, Kimi also optimized by
grouping multiple steps to help
parallelize training to deal with
temporal dependencies. And you can read
through their hardware efficient
chunk-wise algorithm here to get deeper
understanding into how they actually
work. Now, looking back at Kimi's
diagram, we covered stable latent movie,
we just covered Kimi Delta attention and
hybrid layers. One big thing that you
might have noticed here was this whole
section showing many red lines. The red
pipes here have a lot to do with how the
plumbing works in information moving
across the network. This is called
attention residual. And much like how
Kimi Delta attention was released 9
months before it was incorporated into
Kimi K3's official release, attention
residual was also released back in
March, so about 4 months before the
release of Kimi K3. Residual network in
general is sort of like this unsexy
blue-collar part of model architecture
since it's about creating streams for
communication to happen much like real
plumbing. Now, I did a thorough
explanation on the theory behind
residual network when I covered Deep
Seek MHC video for reference. But the
reason why we need this in the first
place is because typically we have so
many layers doing operations on top of
our input where by the time you get to
the end, the information gets distorted
so much that it becomes really difficult
to train looking back the deeper the
model gets. And residual network helps
us create the plumbing that's necessary
for information to carry layer by layer
without the pressure building up. So,
just like plumbing may be necessary to
relieve water pressure, residual network
help allow models to scale in layers by
creating additional streams for inputs
to retain its original state as it moves
through layers and modifications are
applied on top. And standard residual
connection in transformers did help, but
the drawback is that layers that are
deeper into the model often become
diluted since they know very little
about layers that are much earlier on.
Attention residual changes this by
allowing the current layer to
selectively pull information from
earlier residual states. And for Qwen
1.5 they're incorporated into a logical
block and grouping together to prevent
connection layer from becoming too
expensive. So, not only do we have
information flowing between layers,
grouping previous layers into a bigger
logical block helps reduce too much
thereby decreasing the interconnect
burden on GPUs. And looking at the
research paper for attention residual,
it showed very strong results in
comparison since it makes the model a
lot more expressive. And this is a great
addition to Qwen 1.5 model. Now, as a
closing note, I'm personally excited to
see how Qwen 1.5 actually runs on more
advanced chips here in the US. There's
already been talks of our government
potentially banning Qwen 1.5, but I
think that would be a huge mistake given
that we have so much gain in the US.
Even looking at just how much more
advanced we are in chip and the
infrastructure layer to unleash the
model potentially at a faster or
potentially cheaper inference than their
current pricing at $3 per million input
token and $15 per million output tokens.
I'm also really curious to see how this
number might look when new clouds in the
US get a hold of this open model and
serve them for general public use. And
it certainly paints an interesting
dilemma where Chinese models that are
shooting for efficiency could be run
more efficiently here in the US assuming
that we can leverage our stacks
underneath.
