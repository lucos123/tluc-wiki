## Findings - Transcript
[0:01] Agents are a new kind of software. Endless inputs and nondeterministic outputs. Build them the old way and they
[0:08] break. [music] Enter Langmith, the agent engineering
[0:14] platform. It's model agnostic, cloud agnostic, and framework agnostic.
[0:20] Organizations shipping the best agents iterate with a system, and we call that system the agent development life cycle.
[0:27] Build, test, deploy and monitor. [music] You build with our open- source frameworks.
[0:34] Deep agents, Langchain or Langraph. Langmith fleet enables anyone to build
[0:40] agents [music] without code.
[0:45] Test [music] agents using evalu.
[0:50] Deploy changes in one click with Langmith deployment.
[0:56] [music] Monitor every interaction from a single dashboard.
[1:02] [music] Governance is built into every stage of
[1:07] the agent development cycle [music] with Langmith OLM Gateway.
[1:12] Langmith Engine helps you improve agents autonomously and move through the development life cycle more quickly.
[1:19] [music] Langmith Engine is your agent for agent engineering.
[1:42] Hey folks, um my name is Sydney. Just going to give uh folks maybe like 15
[1:47] more seconds to join, but we'll get started with the art of loop engineering here soon.
[2:03] All right, let's get started. So, welcome to uh our latest link chain
[2:09] webinar on the art of loop engineering. Um so, kind of subtext here is how we
[2:14] build agents that improve over time. Uh just general reminders um if you have
[2:19] any questions feel free to drop them in the chat or the Q&A. Um because we have a lot of uh folks tuning in today. I'm
[2:26] going to wait to answer questions at the end, but feel free to send them anytime. And I think on the Q&A you can also
[2:32] upvote questions if there are any that you really want to get answered.
[2:38] All right. So just starting with a quick intro here. Um my name is Sydney. I am a
[2:44] uh project manager on the open source uh sorry product manager on the open source team at linkchain was previously a
[2:50] software engineer um and I'm super excited to talk about how you can do
[2:56] loop engineering both with our open source frameworks and linksmith and our um kind of commercial platform. So,
[3:03] Lingchain uh as a company provides the platform for what we call the agent development life cycle and core to that
[3:10] agent development life cycle is uh the primitive of loops. So, that's what we're going to talk about today.
[3:19] So, first I'm going to talk about why loops matter. Um, so if we zoom out and
[3:26] think about why agents matter in the first place, it's because they can take action and do work for us. Um, and
[3:36] agents are really only as useful as the kind of model and harness that you build
[3:41] them around. And so the model has some like fixed level of intelligence and then you can make it for useful for your
[3:47] given use case um by building harness around it that connects it to your
[3:53] workflows. Um and so part of building a robust harness is building loops in um I
[4:00] have kind of these four points outlined here and we'll dive into how those correspond to different loops. Um but
[4:07] another important piece here is uh continuous integration. So having loops built into like every agent that you
[4:14] build, making sure that um every time you run an agent, it can get better and
[4:20] improve from that run. Um so let's kind of jump into to our levels of loops
[4:25] here. So the first loop is the core agent
[4:30] loop. Um we've been talking about this at Langchain basically ever since uh LM
[4:36] gained popularity. Um and this is that that action taking loop. And so what happens here um is basically the the
[4:44] basic agent model and tool loop. So first a
[4:49] model receives context for a given task. Then it calls tools to complete given
[4:56] work for that task. Tools return observations and then the model kind of continues in that core loop until it's
[5:02] done with a given task. Um, and so when we talk about loop engineering here, what does that mean at loop level one?
[5:10] That means that you're giving the model the right tools for the given task. Um, and then also that you're selecting the
[5:16] right model. So given the complexity of tasks coming in, you want to match the model intelligence to those so that you
[5:23] can kind of optimize along the cost axis. And then for tools, you can also
[5:28] do kind of prompt engineering here, right? like are your tool descriptions good enough that the model uses them
[5:34] effectively? Um and so really like this is a pretty simple loop, but um at every
[5:40] level there's like optimizations you can make. And so the power in the agent loop
[5:46] specifically is that the model has the discretion to take action and then also decide when it's done with actions for a
[5:53] given task. For each of these kind of loop levels,
[5:58] I'm going to talk about an example agent. Um it's really not not uh an
[6:03] example but rather an agent that we use every day at link chain. So this is our docs improvement agent. Um so we'll
[6:10] start with the very basic infrastructure here. We send a docs improvement request. The model plans and drafts
[6:18] changes and then we give it tools to um you know clone the docs repository, read
[6:24] existing docs, write new docs um and then open a pull request with an appropriate diff and description. So
[6:31] this is like very basic docs writer agent.
[6:36] So the second loop is probably the loop that started to popular popularize the term loops in the first place and that's
[6:44] the what you might call like a slashgoal loop or a verification loop. Um and this
[6:49] adds reliability to agents basically via like grading and rubric criteria. So
[6:56] what does this look like? You can see outlined in purple here I have that like core agent loop. Um but now we have this
[7:03] green greater. Um and so you send a request uh the model and tools we have
[7:11] that core loop and it returns a result. So that's like one agent cycle. Um and
[7:16] then that gets fed into our greater which decides if the task that came in
[7:21] with the initial request is actually complete. Um so agent attempts a task.
[7:27] That's part one. And then the actual loop that we're talking about here is the greater scoring against given
[7:33] criteria. If those criteria are not met, we feed it back into into the agent
[7:38] loop. And then if those criteria are met, then we move to done. So one basic
[7:44] example might be like, you know, slashgoal implement this new feature in my codebase um and don't stop until all
[7:53] tests are passing and coverage is at 95%. Um and so your agent, your coding
[7:58] agent, maybe claude code, deep agents code would take a pass at implementing
[8:03] that new feature. Um and then once it takes the pass, then we have that
[8:09] greater run over the criteria. One interesting thing that I'll call out with slashgoal um or verification loops,
[8:17] we've uh added support for this in decode which is our like terminal coding agent based on deep agents. And one
[8:24] unique feature of our/goal implementation specifically is when you give it a goal, it actually gives you
[8:30] criteria to review. So like a specific basically rubric that is going to be checked every time. Um and so that
[8:38] allows you like a little bit more transparency into um the criteria that
[8:44] you're scoring uh success against. I think codeex and cloud code don't have that kind of finer grained level of
[8:50] control. And then I'll also note because decode and deep agents are open source,
[8:55] we allow you to plug in this like goal or rubric middleware into any of your agents. So if you're like, oh great, I
[9:02] love building, you know, link chain agents with create agent or deep agents with create deep agent, but I actually
[9:09] want it to be kind of more reliable and trustworthy against the like end goal. You can just plug in that middleware to
[9:14] support that. So uh what does this look like for our docs agent? We have the docs improvement
[9:21] request coming in. Core agent loop opens a pull request. Um, and then the greater
[9:27] agent ensures that all links resolve and that CI passes uh before an actual done
[9:34] notification, right? Like it's a little bit of a waste of a human reviewer's time to review a doc's PR if there's
[9:40] tons of um faulty links, for example. Um the last thing that I'll note about
[9:46] verification loops is that they are particularly powerful when um you want
[9:52] to use like a cheaper model but still for more challenging tasks. So, in the
[9:58] same way that we saw folks early on using the to-do list to keep models on track, um the kind of greater
[10:05] verification loop can help to keep those like major agent cycles on track, especially if you know your model is not
[10:11] like quite as powerful.
[10:16] All right, so the third loop is the event driven loop. The reason that I'm
[10:22] excited about this loop is because it is what makes me personally actually use agents. Um, and so agents become more
[10:30] powerful when they are like looped into the actual systems where they're relevant. So what do I mean by this? Um,
[10:36] the TLDDR is basically like I want to be able to use my agents in Slack and in GitHub um, and in any of the places
[10:44] where I'm like having important conversations with people. And so I think this one might be the most of a
[10:51] like stretch to call a loop, but really the loop is like you are able to trigger the agent in the system where it's
[10:58] relevant and then inherently you're making some other system better. Um, and so you've got this like improvement
[11:04] loop. Um, so what do those triggers actually look like? Um, they can be
[11:10] scheduled or they can be event driven. For example, I have a background agent
[11:15] that runs over my calendar every morning um and gives me a summary of my day and
[11:21] you know anything that I might need to prep, etc. Or I have an email assistant agent um that is triggered on a specific
[11:29] event. So Sydney has received an email like great, let's kick off her email assistant that will kind of read the
[11:35] email, draft a reply, decide if it's spam or if it's worth surfacing to me,
[11:41] etc. Um, again, I I'm pretty excited about this one because I think agents don't
[11:47] have that much value unless they're incredibly easy to use. Um,
[11:52] you can see in the diagram at the right, uh, we have the event trigger, then our nested verification loops and the core
[11:59] agent loop, and then also a like system update, which again is, um, how we model
[12:07] this one as a loop. I'll also note in these diagrams I'm doing the um kind of like Russian doll
[12:13] thing of like nesting every loop in itself. You don't necessarily have to do that for all four loops. For example,
[12:18] you could just nest a core agent loop in with an event driven loop. You don't need the verification loop but um just
[12:26] kind of to demonstrate that they are all composable. So tying this back to our docs writer
[12:31] event, what does this uh actually look like? So we have a channel called docs
[12:38] please. Um I can send it a slack message and say hey can you please update our
[12:43] deep agents docs to showcase the value of verification loops on a new uh you
[12:50] know slashgoal or slrubric page. Um then agent core agent runs drafts a PR my
[12:58] verification loop decides if links resolve and CI passes we actually go
[13:04] ahead and send a Slack notification back that's like here's your PR Sydney like please review um and then we have this
[13:11] merged live and like discoverable docs enhancement and hopefully this can really help to illustrate why this event
[13:18] driven loop um is a loop which is like Now those changes are live and I can go
[13:24] look at the docs um which will motivate me to start another or trigger another
[13:30] event which kicks off my docs agent. So this one is particularly relevant when
[13:35] you're like improving um systems where the agent is embedded.
[13:42] All right, maybe I said the most exciting loop for the goal loop, but I take it back. I
[13:48] think the self-improvement loop is actually the most exciting. Um so we'll call this one the hill climbing loop,
[13:54] the learning loop, self-improvement loop, all things of that nature. Um so this
[14:00] automates improvement and we can automate improvement by finding signal
[14:05] in traces. So this is really the foundation of what link chain the company is built on, which is that uh to
[14:13] build agents, you really need to have insight into what they're doing. As you saw in our new awesome intro video, um
[14:20] agents are non-deterministic. And so unlike previous code where like you know
[14:25] observability showed you um exact or or unlike previous code where the truth was
[14:31] kind of in the code itself, you could tell exactly what it's going to do. Um the story is actually in traces for
[14:36] agents and so you need that trace signal to tell you how to improve your agent.
[14:41] So let's talk a little bit more about what this means. Um, we run our docs agent. Um, it or actually I I'll do the
[14:51] docs example on the next page. Um, let me talk a little bit more theoretically here. So, we run our agent in response
[14:57] to an event trigger. The greater eventually decides that it's met the criteria. we update some system and then
[15:05] in the background after the main agent run is done we run an agent over that
[15:11] trace or maybe traces in bulk for this agent. Um and that sort of helper agent
[15:16] which at lingch chain we call engine um is able to detract detect various
[15:22] failure modes from the trace itself. So what does that look like? Maybe a tool
[15:27] was called with improper arguments. Maybe a critical tool call was missed
[15:33] because the relevant context wasn't there. Um maybe there were certain docs
[15:38] writing preferences that I have across requests that are not being respected
[15:44] when I make my docs please requests. Um so identifying recurring issues or kind
[15:49] of gaps in the core harness. Um, and then the super exciting part is that
[15:55] this agent has the capability to update the prompts, tools, skills, memory,
[16:02] basically anything that's part of that core harness. Um, and port that back to
[16:07] the source code. Um, and so this outer loop makes each inner loop more effective. Um, and and I have 30 minutes
[16:16] to talk and have saved a lot of time for this loop in particular because there's a lot to discuss here. So the first kind
[16:23] of category of things that you can do with the hill climbing loop are improve
[16:28] those like base kind of procedural things like um tool descriptions and
[16:35] prompts. I would even say like skills that are more procedural. Um and that's
[16:41] like if your agent is not taking the right trajectory and it's something that you can inform with those kind of
[16:47] hard-coded prompts um then you can extract that signal from traces. The
[16:53] second category is more like memory information. So information that's um
[17:00] persisted across runs. Um so let's take let's go back to the email assistant
[17:06] example. Um, I probably want my email assistant to respond differently to my
[17:14] boss versus my co-orker, right? I would be a little bit more informal with my co-worker um, and and more formal with
[17:20] my boss. And so, it's important to me that my email assistant understands the relationships that I have to different
[17:27] people who are sending me emails um, and the kind of email styles that I want to use. And so if I get an email from my
[17:35] boss and my email assistant drafts a reply that's super informal and before it sends obviously because I probably
[17:42] want a human in the loop here. I would say hey like wait that's that's my boss let's be you know more formal. Um I
[17:49] would hope that it would actually remember that guidance for future runs. And so one job that this background
[17:55] agent can do is kind of memory consolidation again so that the harness is like learning over time and a lot of
[18:03] that comes in the form of like user preferences etc. Um yeah so kind of procedural stuff and
[18:10] then more semantic stuff is what you can extract. The final note that I'll add on this
[18:16] hill climbing loop slide is that uh it's actually really hard to close this loop
[18:21] if you don't have good eval. Um so it's pretty hard to have confidence merging
[18:28] changes to your like core harness if you don't have evals that can help you justify those changes. So engine or you
[18:36] know your assistant agent has made some change to it's added a skill and changed a prompt and updated memory for some
[18:43] user like how do you feel confidence uh with that merge is probably like running
[18:48] your eval suite and making sure there's no regressions or even actually that there's um that there's improvements on
[18:54] some tasks. Um so just bringing this back to our kind of core example um what do we do
[19:01] with our docs writing agent? Well, we run engine again, our linksmith agent
[19:07] over our traces. Um, and then we can um update all those things that I was
[19:12] talking about on the last slide. Uh, one really important note that I'll
[19:19] add here is that we talk about like automating things with loops, right? The value of an agent at loop one is to
[19:26] automate things. The value of a greater at loop two is to like automate with
[19:32] reliability. Um you're basically adding like automated checks. The value at loop
[19:38] three is like in some ways you're automating continuous improvements in a system. And then loop four um or or
[19:47] sorry for loop three you're like automating improvements to the system itself as in like your documentation.
[19:53] And then loop four, the most powerful loop arguably is automating improvements to your agent. So self-improving. Um
[20:01] that being said, a lot of things that agents do are still really sensitive. Um and so human approval totally has its
[20:07] place um in any of these loops. As I have here in blue, automation does not necessarily uh mean removing humans. It
[20:14] means just like using them when human review or discretion or judgment adds
[20:20] value and not wasting time when it doesn't. Um now let's talk about this at
[20:25] each loop level. So um let's go back to the email assistant. Um if there's a
[20:33] send email tool, I probably want uh human approval in that cycle at least
[20:38] for um people that are important. So you can still add human approval at uh core
[20:46] you know important or sensitive tool calls for like a transaction for example before my travel agent books travel for
[20:53] me I probably want to click like yes that flight looks great. Um the second is you can add uh human loop
[21:01] into the like greater or verifier cycle right so um basically plugging in some
[21:06] form of human approval in that green stage of the loop we were talking about the third uh human approval on like
[21:14] workflow artifacts or results. So in our docs writer uh example we always have to
[21:19] have human approval on those PRs um before they merge. And then the fourth
[21:25] is uh approving harness and like code changes to your core agent is pretty
[21:31] important. I think you can start to man now I'm thinking about loop five which is like if you actually have a RL uh or
[21:40] basically like a learning environment where you can then like propose changes to your harness and run all of your
[21:46] emails against them and then decide if they meet some threshold of like improved behavior then you automerge.
[21:52] that's like level five. Um, but uh, yeah, I think for most development
[21:58] teams, the actual like changing to source code of an agent is going to
[22:03] require some form of human review. So, humans still important, but um, are not
[22:09] quite as important as they used to be.
[22:15] Putting it all together, just going to do kind of a quick recap over the loops we've talked about. Um
[22:21] I'm going to leave a couple of extra minutes for questions here because I do think we have a lot of folks and everyone has good questions about loops
[22:26] on Twitter. So I'm sure there will be some good ones here. Um so first the agent loop it the agent loop does the
[22:33] work model calls tools. Tools allow the agent to take action and then the fact that this is done in a loop um makes it
[22:39] more powerful. The verification loop improves quality especially for cases where uh models aren't as powerful and
[22:47] need more of that like check checked work model. Um the event driven loop
[22:52] helps to scale execution and make sure that agents actually get used and are used to like improve systems. Um and
[23:01] then the fourth, my favorite is the hill climbing loop. Call it the learning loop, self-improvement loop. Um and this
[23:07] improves your agent system over time. Um and so we have the key takeaway here
[23:13] is the advantage is not just in the agent that you build to automate work but rather in the loops that you build
[23:18] around it. Um loops basically like amplify impact. We know agents are impactful so building loops helps them
[23:26] do more. Um all right
[23:33] pivot back to the main screen here and then happy to answer questions.
[23:46] Okay, great. First question. I would assume there's some kind of memory system for these advanced loops. Um, how
[23:52] do you decide what information to save such that multiple agents are involved in loop? Um, have the right context to
[23:59] do their work? That is an excellent question. Perhaps our next webinar will be on memory. Um, I would recommend for
[24:07] folks to check out our new deep agents memory docs which do kind of a very deep
[24:12] dive into um all of the aspects of memory when you read it, when you write
[24:19] it, what's worth um being saved, how different memories interact, etc. But
[24:24] I'll give a quick overview here. Uh, which is yes, there's totally a memory
[24:30] system especially involved in that loop four. I I think you can almost argue
[24:35] that like information that's persisted across runs is some form of memory and that's like inherently what we're doing
[24:41] with loop 4. Um and so I think maybe unfortunately my answer is that like the
[24:48] information that is saved is very um specific to the agent itself. Um, that
[24:55] being said, uh, eval can really help you determine if the information that you're saving is helping your agents like
[25:02] trajectory and performance. Um, and that the one other thing that I'll plug here
[25:07] is that I think there's like two main types of memory stores that we're
[25:13] thinking about a lot at link chain right now. One is like, man, we all use coding agents so much. Like, wouldn't it be
[25:19] great if they could traverse our repositories super efficiently? And for that you can build in like um memory
[25:26] into your repository via a wiki structure. And then you can also build
[25:32] kind of like personal wiks that have more of that like semantic knowledge. Um
[25:37] and I would recommend checking out open wiki which we just released built on top of deep deep agents to help you kind of
[25:43] build out that uh initial memory system for your agent and then loop 4 can help
[25:48] you update that system. Um, okay. Looks like the next question
[25:54] is, uh, what are the best practices for designing your greater and how does this
[25:59] work? Um, where correctness or your reward signal,
[26:05] if you will, is ambiguous or difficult to quantify. That's a good question. Um
[26:13] I think the very basic um kind of verification loop that we think
[26:20] about is uh let's see I'm I'm going to pivot my answer here. So the basic verification
[26:26] loop that we can use as an example as I mentioned is the like slash goal example in cloud code or other coding agents. Um
[26:35] I think the like explicit criteria really help here. Um, if you're able to
[26:40] have a human in the loop to score the criteria that your agent is coming up
[26:47] with for a given goal and then use that to basically train the model that comes
[26:52] up with the criteria, um, that's probably best. Um, so like if your reward signal is ambiguous or diff uh
[27:00] difficult to quantify, then you like probably need some human annotation and signal on examples that you can use to
[27:07] like um basically train your your criteria generator and evaluator.
[27:16] Um any example public repositories to demonstrate this concept? Yeah, great
[27:23] question. Um so we uh have deep agents which is our core um agent building
[27:30] library at link chain. It's fully open source and that I think does a great job of demonstrating loops one and two. So
[27:36] core agent loop and then verification loop with that like rubric or goal middleware. Um in terms of good examples
[27:44] for three and four. So the fourth one I would say like trying out linksmith and
[27:50] engine is the best way to sort of get a feel for like wow I'm I'm tracing my um agent runs and like I can already see
[27:56] improvements and suggestions being made back to that repository. Um the third I
[28:02] would say the best place to try that is maybe with our fleet agent. Um, so
[28:07] that's like a no code agent builder, but comes built in with all of these automatic um, connectors like Slack,
[28:15] Gmail, etc. Um, we also have for like a code version of that. We call it manage deep agents. Um, but that's the best way
[28:22] to like start with integrations um, and triggers.
[28:29] I think the last thing I'll say is we also have like open source email assistance throughout the eras of like link chain development. Um and and
[28:36] they'll have triggers as well.
[28:41] Uh the next question is how does greeter work in a sub aent architecture? Does it always evaluate against the main agent
[28:48] in a deep agent context? Yeah, great question. So the rubric middleware inherently is tied to that like main
[28:54] agent loop, but you actually could assign um like rubric middleware or
[29:00] graders to sub aents specifically. Um, so if you had like a very task focused sub agent that you wanted to add, uh,
[29:08] kind of greater loops onto, um, you could do that. [clears throat] And that's kind of the beauty of Lingchain's like composable uh, middleware stack.
[29:17] Oh, the next question is greet. Um, how do you deal with latency when you implement loops? That's a good question.
[29:25] So basically loops are like inherently going to add latency. Um if your model
[29:31] is not doing a good enough job and you so you have like tons of greater loops for example, it's really just a
[29:36] trade-off of like do you care a ton about correctness and quality or do you
[29:42] care a ton about cost? Um, so one thing you could do is like if you if you don't
[29:50] care that much about cost, uh, you could use a more powerful model, which
[29:55] probably doesn't need quite as strict of a like greater loop. Um,
[30:00] yeah, that would that would be my kind of first push. Um, is just you need to like optimize your needs for latency and
[30:06] cost. Um, in terms of the other loops, I don't think like latency is actually a huge thing there. Like the event driven
[30:12] one is more of a systems thing. the model loop. I guess one one idea here is
[30:18] like adding um guardrails. So you might want to like have sub agents um which
[30:25] are also called in that loop like time out after a given amount of time or set a max number of um cycles and then your
[30:32] agent like returns to the main user. Um so you can definitely put up like guard rails to control. Um and then I don't
[30:38] think latency is like a huge thing on the learning loop side. probably the issue there is like do you have enough
[30:44] data to make um good choices about harness changes?
[30:51] Um what are the biggest problems agent builders are solving with loops on your
[30:57] team? That's a great question. Um
[31:02] we have lots of awesome um internal agents built on our lang chain open
[31:08] source. So, I'm kind of um going through all of those. I'll say one really
[31:15] interesting one is our like go to market agent um that's accessible in Slack has
[31:20] a really awesome memory system. Um and I think we're working on improving that memory system with loops by not only
[31:26] pulling from data sources like right when the agent is triggered but also just trying to like distill other domain
[31:33] knowledge from resources like um you know email, Slack, etc. into things that
[31:40] are going to be relevant for that agent and its communication. So that's kind of the like event driven memory
[31:45] self-improvement loops. Um, another one is uh
[31:53] in terms of self-improvement stuff, just improving our repository context um and looking at traces. Uh, one thing I
[32:00] actually didn't mention with the learning loop that's really interesting is like not only can you make sure that
[32:05] your agent is doing the right thing, but is your agent doing the thing efficiently and correctly? So like is
[32:11] the tool call trajectory efficient and if not, why not? And how can you fix that? Um, and so that's like a very
[32:17] interesting research problem we're working on with coding agents specifically.
[32:26] Um, cool. A human in the loop question on human in the loop. How do you balance the bottleneck of requiring human
[32:33] approval uh with the need to scale these agentic workflows in a production environment?
[32:38] That's a great question. Um sort of two things here. one is I think if you're
[32:47] the if you can defer human approval um to
[32:54] someone who it's not uh challenged to um approve things then that's good. So for
[33:00] example like with the travel agent if the human approval relies on the like user of the travel agent that like
[33:06] totally scales with a production environment. The other thing that I would say is if you can use some model
[33:14] discretion to decide when human approval um is absolutely necessary that can help to kind of reduce the number of like
[33:21] approval requests that you're getting. For example, like with the email agent, I don't really need human approval to
[33:28] say like yes, this is spam. Don't um don't reply. Maybe just like for my most
[33:34] sensitive emails, I want like human in the loop there. Um and then I would also say making sure um
[33:42] you have all of the like human in the loop requests that are essential in a
[33:47] place that's very accessible for people. So this comes back to the like event driven loop, right? Which is like as
[33:53] soon as the docs agent has a PR that's ready to go, uh we send a Slack message
[33:58] with a ping so that you like keep the human in the loop, right? Like one of the worst things is if you have an agent
[34:04] doing valuable work but it's not getting the approval it needs. And so if you can leverage integrations um so that the
[34:11] human in the loop flow is super easy for folks then uh that helps a lot.
[34:23] Um, all right. For agents developed with lang graph in addition to using graders to tweak prompts and tool descriptions,
[34:30] uh, do you use them to optimize the structure of the graph? This is a great question. Um, I think we see more folks
[34:35] building with deep agents right now. So just around that like core agent loop, but we definitely do see folks still
[34:41] building with langraph for those more like bespoke kind of custom workflows where you're mixing more um, agentic and
[34:49] deterministic steps. Um we have not trained engine specifically
[34:55] to update well actually no I think engine could update langraph code if you wanted it to um and that definitely ties
[35:03] into the like trajectory of tool calls etc. So basically my answer is yes. And I think um the key for a lot of teams
[35:12] just as they've learned at the like levels one, two, and three uh is that
[35:17] your like self-improvement agent does often have to be like tailored to your use case, right? So like it needs to be
[35:23] very context aware um of what kind of improvements you might want to be making to your system and just like your system
[35:29] in general.
[35:35] How do we address context rot in a loop? That's a good question. I think this
[35:40] could go in a lot of different directions. So, I'm not exactly sure how to answer it, but um one interesting
[35:48] thing that I'll add is that we're considering uh you know, lots of teams are struggling right now with increased
[35:54] cost associated with their agent runs. Uh just because like state-of-the-art models are getting more expensive um as
[36:02] things run in these crazy loops, like it's not super sustainable. And so, prompt compression can be really
[36:07] helpful. Uh especially prompt compression if like I have a cla session where I've started talking about like
[36:14] you know three different things in series and I'm like only focused on the most recent thing like in the background
[36:21] compressing those old prompts etc can help to like address context rot and
[36:26] those longer running loops. So I think addressing context rot really is just a
[36:31] like context engineering game. Um yeah hopefully that answers that question. If
[36:37] there's like more specifics you were looking for happy to help.
[36:46] How do we build evals for scientific agents where we do not have a ground truth? This question might be above my
[36:53] pay grade, which is okay. I think it's great to have uh questions that I don't know the answer to. Um
[37:00] yeah, I don't know the answer to this one. I think having uh humans involved in like well okay
[37:08] actually I have an interesting answer to this one which like points at more questions but we recently released a
[37:15] blog post on eval engineering and that basically helps you autogenerate evals
[37:21] from live traces and the context of your repository. And so I would say I would point in that direction, which is
[37:28] basically like you probably need some way to test if your agent run was
[37:33] successful against some criteria that you have. Um, and if you give an agent the context of your challenge and trace
[37:41] context, it can do a like pretty good job of generating eval. So that's like an an interesting research question is
[37:47] like would that do a good job at automatedish eval generation
[37:52] where your uh agent doesn't have ground truth.
[37:59] Good question. I will forward along to some of our our more researchy folks.
[38:08] Uh what bre best practices do you implement to make a mental model of work um and changes made to the uh by the
[38:17] agent loop? Um work and changes made by the agent loop. Um
[38:24] I would say version control uh is great for changes made if you mean
[38:33] changes made by the agent loop for like the self-improving one version control uh work done by the agent. I think like
[38:39] trajectory views of traces are very interesting. Um and also just traces are super key here, right? Like what the
[38:45] heck did my agent do? you're only going to figure it out if [clears throat] you go through the trace and also if your tools have like breadcrumbs of impact.
[38:53] Hopefully that answers that.
[38:59] Okay, great question. How do you measure um and prove that the verification loop
[39:04] improves production outcomes rather than just increasing latency and cost? And do you have a reference architecture that
[39:12] you would recommend? That's a great question. Um, my favorite
[39:17] quote that I heard this week that I probably need to tweet about is this just sounds like an eval trench coat.
[39:23] Um, and that's exactly what this is. So, uh, how do you prove that it improves
[39:29] production outcomes? Like you can't unless you have, um, online emails. Um,
[39:37] and like offline emails are great, too. Um, and do you have a reference architecture? I mean, I think I would
[39:44] just point to our like stack that helps with the agent development life cycle.
[39:49] Um, build, test, monitor, deploy. So, we're building with open source. We're testing before deployment, deploy,
[39:57] observe. We use the results from observation to make improvements to the base harness. [clears throat]
[40:04] And then, you know, we're at the test step again. Um, yeah, that's that's
[40:10] really the only way to know. And then the last note that I'll have
[40:15] here is like increasing latency and cost. Yes, if it improves your outcomes, maybe that's like a trade-off that's
[40:21] worth it. Um, but again, you can like play the optimization game between like where does my like greater and
[40:28] verification loop help and like what power model should I use? For example,
[40:33] if I don't care that much about latency, but like cost is a factor, um you could use a like cheaper model and just like
[40:41] accept the latency of the greater verification loops.
[40:52] How do you deal with planner um to looping and token optimization for
[40:57] complex queries? Uh great question. I feel like [clears throat] I've kind of peacemeal
[41:02] answered this through some of the other questions, but uh context engineering and like prompt compression is
[41:08] definitely an important factor here. Um especially as like you are doing more
[41:14] loops, you can you can probably compress some of the like earlier iterations and
[41:20] histories, right? Because like once you reenter that like try again loop for an agent, it probably makes sense to
[41:27] compress most of the other like attempts. um and just work with like the
[41:33] current state of the artifact and the rubric criteria and goal. Um yeah,
[41:40] and then I I sort of talked about um how you can trade off cost and latency with
[41:45] loops.
[41:52] uh the hill climbing loop's performance would depend on the eval loop and uh
[41:58] that the eval loop and work is planned. Do you have any insights on
[42:03] automatically improving evals over time and the efficiency of that loop as well?
[42:09] That's a great question. Uh, I've been finding myself happy learning more and more about eval by the week. Um,
[42:17] because they're just like such an essential part of this cycle. Um,
[42:23] I think I mean the word automatically here like just points me
[42:29] [clears throat] directly into like another oh an agent could help with that thing. Um,
[42:35] but I think the important part of like automating eval generation is that there's like some understanding of the
[42:42] context of your what your agent is doing and like what the success criteria are.
[42:49] Um, and again I will point at the new skill that we just released on eval engineering that basically can look at
[42:56] traces and help to generate eval from those, but it also has the like base
[43:01] context of the um repository agent. And then I'll also note that that skill
[43:07] actually it's it's meant for a coding agent to help you extract evals. Um, but
[43:13] it is pretty interactive like it asks you the human lots of questions about like the context in which you want to
[43:18] generate these emails etc. almost like interviews you. Um, and then the other
[43:24] thing that I'll note on eval, uh, Nick from our open source team just released a great blog on like how we think about eval deep agents is um, you kind of want
[43:33] like two types of eval. One almost reminds me of like a unit test. It's like a baseline functionality thing. Um,
[43:39] so like is the agent doing the like bare minimum and and not regressing in terms of behavior and then the other one is
[43:45] like a a challenging integration test almost where it's like more of an endto-end thing or even like a um shoot
[43:52] for the stars sort of eval that you can like hill climb on. And so I think making sure that your email suite has
[43:58] both of those is good and especially making sure that your baseline ones um are really good is great. I think I have
[44:05] time for just one more question here. Um, oh great question. Uh, for the hill
[44:13] climbing loop, what types of changes are better in the harness? Changing code and
[44:18] architecture, so more runtime stuff, or updating memory/sklls/prompts?
[44:24] This is a fantastic question. So, um I can't unfortunately say which is
[44:32] better, but what I would push folks to generally try to do is like keep the agent architecture relatively similar,
[44:39] like trust in the power of that core agent loop. um and then update the
[44:44] memory and skills and prompts and see how far you can get with that because like most of the time the reason the
[44:49] agent does something wrong is not necessarily because the model isn't powerful enough but just cuz it doesn't have the right information. Um, and so I
[44:57] would lean towards like try to update memory and skills and prompts first and then if there are important architecture
[45:03] changes for example something like man the agent is never following this compliance step like then you can
[45:09] definitely uh you know add like deterministic code or change the runtime structure there. So first more of the
[45:17] memory stuff second more of the runtime stuff especially if it's like I needed to take this deterministic step.
[45:24] Um, all righty. Well, thank you folks for all the questions. I just have a couple more uh things to chat about
[45:30] here. So, the the first is that we are expanding our interrupt conference. Um,
[45:36] and so we now have interrupt 2026 planned in New York City uh September
[45:42] 24th and then interrupt 2026 in London um on the 13th of October. So super
[45:52] all there. Thank you so much for attending. Um if
[45:57] you have more questions, feel free to bug me on Twitter. Um yeah, much appreciated.

