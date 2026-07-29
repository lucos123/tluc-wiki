---
title: "The Art of Loop Engineering: How to Build Agents That Improve Over Time"
date: 2026-07-29
tags:
  - raw
  - video-transcript
source_type: video
url: "https://www.youtube.com/watch?v=jPPiZ22DY3g"
channel: "LangChain"
upload_date: "2026-07-23"
duration: "46m 8s"
---

# The Art of Loop Engineering: How to Build Agents That Improve Over Time

**Channel**: LangChain
**URL**: https://www.youtube.com/watch?v=jPPiZ22DY3g
**Upload Date**: 2026-07-23
**Duration**: 46m 8s
**Transcript extracted**: 2026-07-29

---

## Transcript

Agents are new kind of software, endless
inputs and non-deterministic outputs.
Build them the old way
and they break.
>> [music]
>> Enter LangSmith, the agent engineering
platform. It's model agnostic, cloud
agnostic, and framework agnostic.
Organizations shipping the best agents
iterate with a system, and we call that
system the agent development life cycle.
Build, test, deploy, and monitor.
>> You build with our open-source
frameworks.
Deep Agents, LangChain, or LangGraph.
LangSmith Fleet enables anyone to build
agents
>> without code.
Test [music] agents using evals and
experiments.
Deploy changes in one click with
LangSmith deployment.
>> Monitor every interaction from a single
dashboard.
>> Governance is built into every stage of
the agent development cycle
>> with LangSmith LLM Gateway.
LangSmith Engine helps you improve
agents autonomously and move through the
development life cycle more quickly.
>> LangSmith Engine is your agent for agent
engineering.
>> Hey folks.
Um my name is Sydney. Just going to give
uh folks maybe like 15 more seconds to
join, but we'll get started with the art
of loop engineering here soon.
>> All right, let's get started. So,
welcome to
uh our latest LangChain webinar on the
art of loop engineering. Um so, the
subtext here is how we build agents that
improve over time.
Uh just general reminders, um if you
have any questions, feel free to drop
them in the chat or the Q&A. Um because
we have a lot of
uh folks tuning in today, I'm going to
wait to answer questions at the end, but
feel free to send them anytime.
And I think on the Q&A, you can also
upvote questions if there are any that
you really want to get answered.
All right, so just starting with a quick
intro here. Um my name is Sydney. I am a
uh project manager on the open source uh
sorry, product manager on the open
source team at LangChain. Was previously
a software engineer. Um and I'm super
excited to talk about how you can do
loop engineering both with our open
source frameworks and LangSmith and our
um kind of commercial platform.
So,
uh as a company, provides the platform
for what we call the agent development
life cycle. And core to that agent
development life life cycle is uh the
primitive of loops. So, that's what
we're going to talk about today.
So, first, I'm going to talk about why
loops matter.
Um so, if we zoom out and think about
why agents matter in the first place,
it's because they can take action and do
work for us.
Um
and
agents are really only as useful as the
kind of model and harness that you build
them around. And so, the model has some
like fixed level of intelligence, and
then you can make it for useful for your
given use case um by building harness
around it that connects it to your
workflows.
Um and so part of building a robust
harness is building loops in.
Um I have kind of these four points
outlined here and we'll dive into how
those correspond to different loops. Um
but
another important piece here is uh
continuous integration. So, having loops
built into like every agent that you
build, making sure that um every time
you run an agent, it can get better and
improve from that run. Um
so, let's kind of jump into to our
levels of loops here.
So, the first loop is the core agent
loop. Um we've been talking about this
at LangChain
basically ever since uh LLMs gained
popularity. Um and this is that that
action-taking loop. And so, what happens
here um is
basically the the basic
agent model and tool loop. So, first, a
model receives context for a given task.
Then, it calls tools to complete given
work for that task. Tools return
observations. And then the model kind of
continues in that core loop until it's
done with the given task.
Um and so, when we talk about loop
engineering here, what does that mean at
loop level one? That means that you're
giving
the model the right tools for the given
task. Um and then also that you're
selecting the right model. So, given the
complexity of tasks coming in, you want
to match the model intelligence to those
so that you can kind of optimize along
the cost axis.
And then
for tools, you can also do kind of
prompt engineering here, right? Like are
your tool descriptions good enough that
the model uses them effectively? Um and
so, really like this is a pretty simple
loop, but um
at every level there's like
optimizations you can make.
And so, the power in the agent loop
specifically is that the model has the
discretion to take action and then also
decide when it's done with actions for a
given task.
For each of these kind of loop levels,
I'm going to talk about an example
agent. Um it's really not not uh
an example, but rather an agent that we
use every day at LangChain.
So, this is our docs improvement agent.
Um so, we'll start with the very basic
infrastructure here.
We send a docs improvement request. The
model plans and drafts changes. And then
we give it tools to
um
you know, clone the docs repository,
read existing docs, write new docs, um
and then open a pull request with an
appropriate diff and description.
So, this is like very basic docs writer
agent.
So, the second loop is probably the loop
that started to popular popularize the
term loops in the first place.
And that's the what you might call like
a slash goal loop or a verification
loop. Um and this adds reliability to
agents basically via like grading and
rubric criteria. So, what does this look
like? You can see outlined in purple
here, I have that like core agent loop.
Um but now we have this green grader. Um
and so,
you send a request, uh the model and
tools, we have that core loop, and it
returns a result. So, that's like one
agent cycle. Um and then that gets fed
into our grader, which decides if the
task that came in with the initial
request is actually complete.
Um so, agent attempts a task.
That's part one. And then the actual
loop that we're talking about here is
the grader scoring against given
criteria.
If those criteria are not met, we feed
it back into the into the agent loop.
And then if those criteria are met, then
we move to done.
So, one basic example might be like,
you know, {slash} goal, implement this
new feature in my code base, um and
don't stop until all tests are passing
and coverage is at 95%. Um and so, your
agent, your coding agent, maybe Claude
code, deep agents code, would take a
pass at implementing that new feature,
um and then
once it takes the pass, then we have
that grader run over the criteria.
One interesting thing that I'll call out
with {slash} goal, um or verification
loops, we've uh added support for this
in Dcode, which is our like terminal
coding agent based on deep agents, and
one unique feature of our {slash} goal
implementation specifically is, when you
give it a goal, it actually gives you
criteria to review. So, like a specific
basically rubric that is going to be
checked every time.
Um and so, that allows you like a little
bit more transparency into um
the criteria that you're scoring uh
success against. I think Codex and
Claude code don't have that kind of
finer grained level of control.
And then, I'll also note, because Dcode
and deep agents are open source, we
allow you to plug in this like goal or
rubric middleware into any of your
agents. So, if you're like, "Oh, great.
I love building, you know, langchain
agents with create agent or deep agents
with create deep agent, but I actually
want it to be kind of more reliable and
trustworthy against the like end goal."
You can just plug in that middleware to
support that.
So, uh what does this look like for our
docs agent? We have the docs improvement
request coming in.
Core agent loop opens a pull request, um
and then the grader agent ensures that
all links resolve and that CI passes uh
before an actual done notification,
right? Like, it's a little bit of a
waste of a human reviewer's time to
review a docs PR if there's tons of
faulty links, for example.
the last thing that I'll note about
verification loops is that they're
particularly powerful when
um you want to use like a cheaper model
but still for more challenging tasks.
So, in the same way that we saw folks
early on using that to do list to keep
models on track, um
the kind of greater verification loop
can help to keep those like major agent
cycles on track, especially if you know
your model is not like quite as
powerful.
All right. So, the third loop is the
event-driven loop. The reason that I'm
excited about this loop is because it is
what makes me personally actually use
agents.
Um and so
agents become more powerful when they
are like looped into the actual systems
where they're relevant. So, what do I
mean by this? Um the TLDR is basically
like I want to be able to use my agents
in Slack and in GitHub
um and
in any of the places where I'm like
having important conversations with
people.
And so, I think this one might be the
most
of a like stretch to call a loop, but
really the loop is like
you are able to trigger the agent in the
system where it's relevant and then
inherently you're making some other
system better. Um and so you've got this
like improvement loop.
so, what do those triggers actually look
like? Um they can be scheduled or they
can be event-driven. For example, I have
a background agent that runs over my
calendar every morning um and gives me a
summary of my day and you know anything
that I might need to prep, etc.
Or I have an email assistant agent um
that is triggered on a specific event.
So, Sydney has received an email, like
great, let's kick off her email
assistant that will kind of read the
email, draft a reply, decide if it's
spam or if it's worth surfacing to me,
etc.
Um, again, I I'm pretty excited about
this one because I think agents don't
have that much value unless they're
incredibly easy to use.
Um,
you can see in the diagram at the right,
uh we have the event trigger, then our
nested verification loops, and the core
agent loop, and then also a like system
update, which again is
how we
modeled this one as a loop.
Also note in these diagrams, I'm doing
the um kind of like Russian doll thing
of like nesting every loop in itself.
You don't necessarily have to do that
for all four loops. For example, you
could just nest a core agent loop in
with an event-driven loop. You don't
need the verification loop, but um just
kind of to demonstrate that they are all
composable.
So tying this back to our docs writer
event, what does this uh actually look
like? So,
we have a channel called docs please. Um
I can send it a Slack message and say,
"Hey, can you please update our deep
agents docs to showcase the value of
verification loops on a new uh
you know, {slash} goal or {slash} rubric
page."
Um then agent
core agent runs, drafts a PR, my
verification loop decides if links
resolve and CI passes, we actually go
ahead and send a Slack notification back
that's like, "Here's your PR, Sydney,
like please review." Um and then we have
this merged live and like discoverable
docs enhancement. And hopefully this can
really help to illustrate why this
event-driven loop um is a loop, which is
like now those changes are live, and I
can go look at the docs, um
which will motivate me to start another
or trigger another event, which kicks
off my docs agent.
So, this one is particularly relevant
when you're like improving, um,
systems where the agent is embedded.
All right.
Maybe I said the most exciting loop for
the goal loop, but I take it back. I
think the self-improvement loop is
actually the most exciting.
Um, so we'll call this one the hill
climbing loop, the learning loop,
self-improvement loop,
all things of that nature.
Um, so this automates improvement, and
we can automate improvement by
finding signal in traces. So, this is
really the foundation of what LangChain
the company is built on, which is that,
uh, to build agents, you really need to
have insight into what they're doing. As
you saw in our new awesome intro video,
um, agents are non-deterministic, and
so, unlike previous code where like,
you know, observability showed you,
um,
exact or unlike previous code where the
truth was kind of in the code itself,
you could tell exactly what it's going
to do, um, the story is actually in
traces for agents. And so, you need that
trace signal to tell you how to improve
your agent.
So, let's talk a little bit more about
what this means. Um,
we run our docs agent, um,
it
or actually, I'll I'll do the docs
example on the next page. Um, let me
talk a little bit more theoretically
here. So, we run our agent in response
to an event trigger.
The greater eventually decides that it's
met the criteria. We update some system,
and then in the background, after the
main agent run is done, we run an agent
over that trace, or maybe traces in bulk
for this agent. Um, and that sort of
helper agent, which at LangChain we call
it engine,
um, is able to detract detect various
failure modes from the trace itself. So,
what does that look like? Maybe a tool
was called with improper arguments.
Maybe a critical tool call was missed
because the relevant context wasn't
there.
maybe there were certain docs writing
preferences that
I have across requests that are not
being respected when I make my docs
please requests. Um so, identifying
recurring issues or kind of gaps in the
core harness.
Um and then
the super exciting part is that this
agent has the capability to
update the prompts, tools, skills,
memory, basically anything that's part
of that core harness. Um
and port that back to the source code.
Um and so, this outer loop makes each
inner loop more effective. Um and and I
have 30 minutes to talk and have saved a
lot of time for this loop in particular
because there's a lot to discuss here.
the first kind of category of things
that you can do with the hill climbing
loop are improve those like base
kind of procedural things like um tool
descriptions, prompts, I would even say
like skills that are more procedural. Um
and that's like if your agent is not
taking the right trajectory and it's
something that you can inform with those
kind of hard-coded prompts. Um
then you can
extract that signal from traces.
The second category is more like memory
information. So, information that's um
persisted across runs. Um
so, let's take let's go back to the
email assistant example. Um
I probably want my email assistant to
respond differently to my boss versus my
co-worker, right? I would be a little
bit more informal with my co-worker um
and and more formal with my boss.
And so it's important to me that my
email assistant understands the
relationships that I have to different
people who are sending me emails
and the kind of email styles that I want
to use.
And so
if I get an email from my boss and my
email assistant drafts a reply that's
super informal
and before it sends obviously cuz I
probably want a human in the loop here,
I would say hey like wait that's that's
my boss. Let's be you know more formal.
I would hope that it would actually
remember that guidance for future runs.
And so one job that this background
agent can do is kind of memory
consolidation again so that the harness
is like learning over time. And a lot of
that comes in the form of like user
preferences etc.
yeah. So kind of procedural stuff and
then more semantic stuff is what you can
extract.
The final note that I'll add on this
hill climbing loop slide is that
it's actually really hard to close this
loop if you don't have good emails. So
it's pretty hard to have confidence
merging changes to your like core
harness if you don't have emails that
can help you justify those changes. So
engine or you know your assistant agent
has made some change to its added a
skill and changed a prompt and updated
memory for some user like how you feel
confidence with that merge is probably
like running your email suite and making
sure there's no regressions or even
actually that there's
that there's improvements on some tasks.
Um so just bringing this back to our
kind of core example
um what do we do with our docs writing
agent? Well, we run
engine again our LangSmith agent over
our traces and then we can Um, update
all those things that I was talking
about on the last slide.
Uh, one really important note that I'll
add here is that
we talk about like automating things
with loops, right? The value of an agent
at loop one is to automate things. The
value of a greater at loop two is to
like automate with reliability. Um,
you're basically adding like automated
checks.
The value at loop three is like in some
ways you're automating continuous
improvements in a system, and then loop
four, um, or or sorry, for loop three
you're like
automating improvements to the system
itself as in like your documentation.
And then loop four, the most powerful
loop arguably, is automating
improvements to your agent. So,
self-improving. Um, that being said, a
lot of things that agents do are still
really sensitive. Um, and so human
approval totally has its place, um, in
any of these loops.
As I have here in blue, automation does
not necessarily
mean removing humans, it means just like
using them when human review or
discretion or judgment adds value and
not wasting time when it doesn't. Um,
now let's talk about this at each loop
level. So,
um, let's go back to the email
assistant. Um, if there's a send email
tool, I probably want uh, human approval
in that cycle at least for, um, people
that are important. So, you can still
add human approval at, uh,
core, you know, important or sensitive
tool calls. For like a transaction, for
example, before my travel agent books
travel for me, I probably want to click
like, yes, that flight looks great. Um,
the second is you can add, uh, human
loop into the like greater or verifier
cycle, right? So, um,
basically plugging in some form of human
approval in that green stage of the loop
we were talking about.
The third,
human approval on like workflow
artifacts or results. So, in our docs
writer
example, we always have to have human
approval on those PRs before they merge.
And then the fourth is
approving
harness and like code changes to your
core agent is pretty important. I think
you can start to
Man, now I'm thinking about loop five,
which is like
if you actually have a RL or basically
like a learning environment where you
can then like propose changes to your
harness and run all of your emails
against them and then decide if they
meet some threshold of like improved
behavior, then you auto merge. That's
like level five.
But yeah, I think for most development
teams, the actual like changing to
source code of an agent is going to
require some form of human review.
So, humans still important, but
are not quite as important as they used
to be.
Putting it all together, just going to
do a kind of a quick recap over the
loops we've talked about.
I'm going to leave a couple of extra
minutes for questions here cuz I do
think we have a lot of folks and
everyone has good questions about loops
on Twitter, so I'm sure there will be
some good ones here. So, first, the
agent loop the agent loop does the work.
Model calls tools, tools allow the agent
to take action, and then the fact that
this is done in a loop
makes it more powerful.
The verification loop improves quality,
especially for cases where
models aren't as powerful and need more
of that like check checked work model.
The event-driven loop helps to scale
execution and make sure that agents
actually get used and are used to like
improve systems.
And then the fourth, my favorite, is the
hill climbing loop. Call it the learning
loop, self-improvement loop. And this
improves your agent system over time.
And so, we have the key takeaway here is
the advantage is not just in the agent
that you build to automate work, but
rather in the loops that you build
around it.
Loops basically like amplify impact. We
know agents are impactful, so building
loops helps them do more.
Going to
hit it back to the main screen here and
then happy to answer questions.
Okay, great. First question. I would
assume there's some kind of memory
system for these advanced loops.
How do you decide what information to
save such that multiple agents are
involved in loop
have the right context to do their work?
That is an excellent question. Perhaps
our next webinar will be on
memory.
I would recommend for folks to check out
our new deep agent memory docs, which do
kind of a very deep dive into
all of the aspects of memory, when you
read it, when you write it, what's worth
being saved, how different memories
interact, etc. But, I'll give a quick
overview here.
Which is yes, there's totally a memory
system especially involved in that loop
four. I I think you can almost argue
that like information that's persisted
across runs is some form of memory and
that's like inherently what we're doing
with loop four. And so, I think maybe
unfortunately my answer is that like the
information that is saved is very
specific to the agent itself.
That being said, uh
evals can really help you determine if
the information that you're saving is
helping your agents like trajectory and
performance.
and the the one other thing that I'll
plug here
is that I think there's like two main
types of memory stores that we're
thinking about a lot at LangChain right
now. One is like
man, we all use coding agents so much.
Like wouldn't it be great if they could
traverse our repository super
efficiently? And for that, you can build
in like um
memory into your repository via a wiki
structure.
And then you can also build kind of like
personal wikis that have more of that
like semantic knowledge. Um and I would
recommend checking out open wiki, which
we just released built on top of deep
agents to help you kind of build out
that uh initial memory system for your
agent. And then Loop Four can help you
update that system.
Um okay, looks like the next question
is,
uh what are the best practices for
designing your grader? And how does this
work?
where correctness or your reward signal,
if you will, is ambiguous or difficult
to quantify.
That's a good question. Um
I think the very basic
kind of verification loop that we think
about is
uh
let's see. I'm I'm going to pivot my
answer here. So, the basic loop that we
can use as an example, as I mentioned,
is the like slash goal example in Claude
code or other coding agents.
I think the like explicit criteria
really help here.
Um if you're able to have a human in the
loop
to score the criteria that your agent is
coming up with for a given goal, and
then use that to basically
train the model that comes up with the
Um that's probably best. Um so like if
your reward signal is ambiguous or
different uh difficult to quantify, then
you like probably need some human
annotation and signal on examples that
you can use to like um
basically train your your criteria
generator end evaluator.
any example public repositories to
demonstrate this concept? Yeah, great
question. Um
so we
uh have deep agents, which is our core
um agent building library at LangChain.
It's fully open source, and that I think
does a great job of demonstrating
loops one and two. So core agent loop
and then verification loop with that
like rubric or gold middleware.
in terms of good examples for three and
four,
so the fourth one I would say like
trying out LangSmith and Agent is the
best way to sort of get a feel for like,
"Wow, I'm I'm tracing my um agent runs
and like I can already see improvements
and suggestions being made back to that
repository."
the third, I would say the best place to
try that is maybe with our fleet agent.
Um so that's like a no-code agent
builder, but comes built in with all of
these automatic um
connectors like Slack, Gmail, etc. Um we
also have for like a code version of
that. We call it managed deep agents. Um
but that's the best way to like start
with integrations um and triggers.
I think the last thing I'll say is we
also have like open source email
assistants throughout the eras of like
LangChain development um and and all
have triggers as well.
Um the next question is how does greater
work in a sub-agent architecture? Does
it always evaluate against the main
agent in a deep agent context? Yeah,
great question. So, the Rubric
middleware inherently is tied to that
like main agent loop, but you actually
could assign
like Rubric middleware or graders to sub
agents specifically. Um so, if you have
like a very task-focused sub agent that
you wanted to add uh kind of greater
loops onto, um you could do that.
[clears throat] And that's kind of the
beauty of LangChain's like composable um
middleware stack.
Oh, the next question is great. Um how
do you deal with latency when you
implement loops?
That's a good question. So, basically
loops are like inherently going to add
latency.
if your model is not doing a good enough
job and you So, you have like tons of
greater loops, for example,
it's really just a trade-off of like
do you care a ton about correctness and
quality, or do you care a ton about
cost? Um so, one thing you could do is
like
if you if you don't care that much about
cost, uh you could use a more powerful
model, which probably doesn't need quite
as strict about like greater loop.
yeah, that would be that would be my
kind of first push um is just you need
to like optimize your needs for latency
and cost. Um
in terms of the other loops, I don't
think like latency is actually a huge
thing there. Like the event-driven one
is more of a systems thing.
The model loop, I guess.
One one idea here is like adding
guardrails. So, you might want to like
have sub agents um which are also called
in that loop, like time out after a
given amount of time, or set a max
number of
um cycles, and then your agent like
returns to the main user. Um so, you can
definitely put up like guardrails to
control. Um and then I don't think
latency is like a huge thing on the
learning loop side. Probably the issue
there is like do you have enough data to
make um
good choices about harness changes?
Um what are the biggest problems agent
builders are solving with loops on your
team?
That's a great question. Um
we have lots of
awesome
um internal agents built on our
LangChain open source.
So I'm kind of um
going through all of those.
I'll say one really interesting one is
our like go-to-market agent um that's
accessible in Slack has a really awesome
memory system um and I think we're
working on improving that memory system
with loops by not only pulling from data
sources like right when the agent is
triggered, but also just trying to like
distill other
domain knowledge from resources like
um you know, email, Slack, etc. into
things that are going to be relevant for
that agent and its communication. So
that's kind of the like event-driven
memory self-improvement loops.
another one is
in terms of self-improvement stuff, just
improving our repository context
um and looking at traces.
Uh one thing I actually didn't mention
with the learning loop that's really
interesting is like not only can you
make sure that your agent is doing the
right thing, but is your agent doing
the thing efficiently and correctly? So
like is the tool called trajectory
efficient? And if not, why not? And how
can you fix that? Um and so that's like
a very interesting research problem
we're working on with coding agents
specifically.
Um cool. Uh human in the loop question.
On human in the loop, how do you balance
the bottleneck of requiring human
approval
uh with the need to scale these agentic
workflows in a production environment.
That's a great question.
sort of two things here.
One is
I think if you're
the if you can defer human approval um
to
someone who it's not uh
challenged to
um approve things, then that's good. So,
for example, like with the travel agent,
if the human approval relies on the like
user of the travel agent, that like
totally scales with a production
environment.
The other thing that I would say is
if you can use some model discretion to
decide when human approval um is
absolutely necessary, that can help to
kind of reduce the number of like
approval requests that you're getting.
For example, like with the email agent,
I don't really need
human approval to say like, "Yes, this
is spam. Don't um don't reply." Maybe
just like for my most sensitive emails,
I want like human in the loop there. Um
And then I would also say making sure
um you have all of the like human in the
loop requests
that are essential in a place that's
very accessible for people. So, this
comes back to the like event-driven
loop, right? Which is like
as soon as the docs agent has a PR
that's ready to go, uh we send a Slack
message with a ping so that you like
keep the human in the loop, right? Like
one of the worst things is if you have
an agent doing valuable work, but it's
not getting the approval it needs. And
so, if you can leverage integrations um
so that the human in the loop flow is
super easy for folks, then uh that helps
a lot.
Um all right. For agents developed with
LangGraph, in addition to using graders
to tweak prompts and tool descriptions,
uh do you use them to optimize the
structure of the graph?
This is a great question. Um, I think we
see more folks building with
deep agents right now. So, just around
that like core agent loop, but we
definitely do see folks still building
with LangGraph for those more like
bespoke, kind of custom workflows where
you're mixing more, um, agentic and
deterministic steps.
we have not trained agents specifically
to update, well, actually no. I think
agent could update LangGraph code if you
wanted it to. Um,
and that definitely ties into the like
trajectory of tool calls, etc. So,
basically my answer is yes, and I think
the key for a lot of teams, just as
they've learned at the like
levels one, two, and three, uh, is that
your like self-improvement agent does
often have to be like tailored to your
use case, right? So, like it needs to be
very context-aware, um, of what kind of
improvements you might want to be making
to your system and just like your system
in general.
How do we address context rot in a loop?
That's a good question. I think this
could go in a lot of different
directions, so I'm not exactly sure how
to answer it, but um,
one interesting thing that I'll add is
that we're considering, uh, you know,
lots of teams are struggling right now
with
increased
cost associated with their agent runs,
uh, just because like state-of-the-art
models are getting more expensive, um,
as things run in these crazy loops, like
it's not super sustainable. And so,
prompt compression can be really
helpful, uh, especially prompt
compression if like I have a Claude code
session where I've
started talking about like,
you know, three different things in
series and I'm like only focused on the
most recent thing, like in the
background compressing those old
prompts, etc., can help to like address
context rot in those longer-running
loops.
So, I think
addressing context drought really is
just a like context engineering game. Um
yeah. Hopefully that answers that
question. If there's like more specifics
you're looking for, happy to help.
How do we build evals for scientific
agents where we do not have a ground
truth?
This question might be above my pay
grade, which is okay. it's great to have
uh questions that I don't know the
answer to. Um
yeah, I don't know the answer to this
one. I think having uh humans involved
in like
Well, okay. Actually, I have an
interesting answer to this one, which
like points at more questions, but
we recently released a blog post on eval
engineering. And that basically helps
you auto-generate evals from live traces
and the context of your repository.
And so, I would say I would point in
that direction, which is
basically like
you probably need some way to test if
your agent run was successful against
some criteria that you have. Um and if
you give an agent the context of your
challenge and trace context,
it can do a like pretty good job of
generating evals. So, that's like an an
interesting research question is like
would that
do a good job at automated-ish eval
generation
where your
uh agent doesn't have
ground truth.
Good question. I will forward along to
some of our
our more researchy folks.
Uh what best best practices do you
implement to make a mental model of work
um and changes made to the
uh by the agent loop.
work and changes made by the agent loop.
I would say version control
is great for
changes made If you mean changes made by
the agent loop for like the
self-improving one, version control.
Uh work done by the agent, I think like
trajectory views of traces are very
interesting. Um and also just traces are
super key here, right? Like what the
heck did my agent do? You're only going
to figure it out if [clears throat] you
go through the trace. And also, if your
tools have like breadcrumbs of impact.
Hopefully that answers that.
Okay, great question. How do you measure
um and prove that the verification loop
improves production outcomes rather than
just increasing latency and cost? And do
you have a reference architecture that
you would recommend?
my favorite quote that I heard this week
that I probably need to tweet about is
this just sounds like an eval in a
trench coat. Um and that's exactly what
this is. So,
uh how do you
prove that it improves production
outcomes? Like you can't unless you have
online evals.
and all like offline evals are great,
too.
Um and do you have a reference
architecture? I mean, I think I would
just point to our like stack that helps
with the agent development life life
cycle. Um build, test, monitor, deploy.
So, we're building with open source,
we're testing before deployment, deploy,
observe. We use the results from
observation to make improvements to the
base
harness. [clears throat]
And then, yeah, you know, we're at the
test step step again.
yeah, that's that's really the only way
to know.
And then, the last note that I'll have
here is like increasing latency and
cost. Yes, if it improves your outcomes,
maybe that's like a trade-off that's
worth it.
But again, you can like play the
optimization game between like
where does my like greater and
verification loop help and like what
power model should I use? For example,
if I don't care that much about latency,
but like cost is a factor,
you could use a
like cheaper model and just like accept
the latency of the greater verification
How do you deal with planner
to looping and token optimization for
complex queries?
Great question. I feel like
>> [clears throat]
>> I've kind of piecemeal answered this
through some of the other questions, but
context engineering and like prompt
compression is definitely an important
factor here,
especially as like
you are doing more loops, you can you
can probably compress some of the like
earlier iterations and histories, right?
Because like
once you re-enter that like try again
loop for an agent,
it probably makes sense to compress most
of the other like attempts
just work with like the current state of
the artifact and the rubric criteria and
goal.
yeah.
And then I I sort of talked about um
how you can trade off cost and latency
with loops.
Uh the hill climbing loops performance
would depend on the evals loop and
the the evals loop and work as planned.
Do you have any insights on
automatically improving evals over time
and the efficiency of that loop as well?
That's a great question. I've been
finding myself happy learning more and
more about evals by the week um
because they're just like such an
essential part of this cycle.
I think I mean the word automatically
here like just points me
>> directly into like another oh an agent
could help with that thing.
but I think the important part of like
automating eval generation is that
there's like some
understanding of the context of your
what your agent is doing and like what
the success criteria are.
Um and again I will point at the new
skill that we just released on eval
engineering that basically can look at
traces and help to generate evals from
those but it also has the like base
context of the
um repository and agent. And then I'll
also note that that skill actually it's
it's meant for a coding agent to help
you extract evals.
Um but it is pretty interactive like it
asks you the human lots of questions
about like the context in which you want
to generate these evals etc. It almost
like interviews you. Um
and then the other thing that I'll note
on evals and Nick from our open source
team just released a great blog on like
how we think about evals for deep agents
is um
you kind of want like two types of
evals. One almost reminds me of like a
unit test. It's like a baseline
functionality thing. Um so like is the
agent doing the like bare minimum and
and not regressing in terms of behavior?
And then the other one is like a
uh challenging integration test almost
where it's like more of an end-to-end
thing or even like a
um shoot for the stars sort of eval that
you can like hill climb on. Um and so I
think making sure that your eval suite
has both of those is good and especially
making sure that your baseline ones
um are really good is great.
I think I have time for just one more
question here.
Um oh, great question. Uh for the hill
climbing loop, what types of changes are
better in the harness? Changing code and
architecture, some more runtime stuff,
or updating memory {slash} skills
{slash} prompts?
This is a fantastic question. So, um
I can't, unfortunately, say which is
better.
But, what I would push folks to
generally try to do is like keep the
agent architecture relatively similar,
like trust in the power of that core
agent loop,
update the memory and skills and prompts
and see how far you can get with that.
Because like most of the time the reason
the agent does something wrong is not
necessarily cuz the model isn't powerful
enough, but just cuz it doesn't have the
right information.
Um and so, I would lean towards like try
to update memory and skills and prompts
first. And then, if there are important
architecture changes, for example,
something like man, the agent is never
following this compliance step, like
then you can definitely, uh
you know, add like deterministic code or
change the runtime structure there. So,
first, more of the memory stuff, second,
more of the runtime stuff, especially if
it's like I needed to take this
deterministic step.
Um all righty. Well, thank you folks for
all the questions. I just have a couple
more uh things to chat about here. So,
the
the first is that we're expanding our
Interrupt conference. Um and so, we now
have Interrupt 2026 planned in New York
City, uh September 24th, and then
Interrupt 2026 in London, um on the 13th
of October. So, super exciting
all there.
Thank you so much for attending. Um if
you have more questions, feel free to
bug me on on
yeah, much appreciated.
