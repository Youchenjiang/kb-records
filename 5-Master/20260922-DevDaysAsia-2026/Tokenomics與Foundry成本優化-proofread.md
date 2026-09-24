---
title: "Tokenomics: Driving Cost & Outcome Efficiency with Microsoft Foundry"
event: "DevDays Asia 2026"
talk_id: "122"
speaker: "Ash (Microsoft Commercial & GTM Strategy)"
type: "verbatim-narrative-transcript"
verbatim: true
---

# 🎙️ 122 Tokenomics: Driving Cost & Outcome Efficiency with Microsoft Foundry (Ash)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。保留講者 Ash 所有原話演說、架構思維、生動問答互動與企業數據，**未做任何刪減或摘要縮寫**；全面修復英文語音轉錄之斷句、專業術語（如 Microsoft IQ, M365 Profiler, KV Caching, Agent Optimizer, Agent Traces, Spend Telemetry, Phi-4 等），並依演講邏輯劃分清晰結構與主題小標。

---

## 🧠 Architecture Rethink: Prompt Context vs. Knowledge Base & Microsoft IQ

Be smart about what context needs to be in a prompt versus what needs to be in a knowledge base that the agent can then call. A lot of times, you have 40-page documents bundled directly into the prompt, or you have all of this context, world policies, raw text, or images that don't actually need to be in the prompt. It can simply be indexed information sitting in a knowledge base that the agent can then dynamically retrieve if and when it needs that information.

Okay, so how many of you guys have heard of Microsoft IQ? Anyone? Anyone using IQ today? Anyone using M365 Profiler? No? Wow, okay, I'm surprised. Okay, if you're not using M365 Profiler, one of the core IQs—which is Web IQ—comes built-in. But using IQs as part of your agentic solution basically reduces your token spend by 80%.

In my next session, I'll show you a demo of the four IQs coming to life. But think of IQs as nothing more than an intelligent context layer. To do anything, your agents need context; but instead of blindly stuffing the entire context into the prompt, it's an abstraction layer you build on top of the agents that they can retrieve intelligently. We need to get organizations to start using M365 Copilot with this architecture.

So these first three solutions to reducing your token spend and making sure you have a more outcome-efficient, driven response require you to make fundamental architectural changes to your existing agentic or AI application stack.

## ⚡ The Caching Framework: Prompt Caching, Semantic Caching, and Tool Result Caching

Now, the last two solutions I'm going to talk about are about locking those gains in. Once you complete steps one, two, and three, step four is something you can execute very easily on an ongoing basis.

Caching is pretty simple, right? Think of it this way: every time you send a prompt, before the model can respond, it has to read and tokenize what that prompt is into numbers and vectors. Every single time it does this, it costs you money. And in enterprise applications, 90% of the time, the system instructions and prefix prompt are identical. If you are doing this over and over again, you are paying unnecessary overhead every time you invoke the engine for repetitive tasks.

With caching, that's the easiest and fastest way to cut costs. Just remember: this is not traditional database caching; this is LLM KV-cache and prompt caching, so the principles are quite different. You want to structure your prompts strategically: static content first, dynamic user content last. If more than 50% of your input requests repeat across an agent or LLM workflow, turn on caching immediately.

Most model providers, depending on the model you use, publish clear instructions on how to cache properly. In Microsoft Foundry, caching is natively integrated right out of the box.

Here is the three-tier framework for caching effectively:
1. **Prompt Caching**: Cache static prefix tokens, system instructions, and schema definitions.
2. **Semantic Caching**: Cache semantically similar queries to return pre-computed answers without hitting the foundational LLM.
3. **Tool Result Caching**: Cache deterministic outputs from expensive external API calls and database tools.

We have a dedicated GitHub repository detailing this entire caching implementation framework. Connect with me on LinkedIn, or access the materials after this conference to explore the code.

## 🔄 Continuous Simplification & Lifecycle Model Swapping

Step five is all about simplification. Every time you have multiple agents collaborating, or every agent handoff, all that context has to be re-packaged and forwarded to the next agent in the loop.

The point of simplification is recognizing that managing AI applications is an ongoing operational process. You don't build an agent once, ship it, and wash your hands. Foundational models retire or get superseded almost every year. For whatever enterprise use case you have, you will continuously swap models out, evaluate newer models, deprecate obsolete agents, and introduce specialized ones. This optimization review is a process you should run monthly, if not even more frequently.

## 🛠️ Microsoft Foundry Observability & Optimization Tooling

This is the core Tokenomics framework we walk through with enterprise customers to cut token spend, boost reliability, and accelerate business outcomes. Backing this framework, Microsoft Foundry provides three powerful built-in tools:

1. **Agent Optimizer (Public Preview)**:
   It automatically benchmarks your prompts, models, and tools against the custom evaluators you defined in your evaluation suite. When you define your business criteria, Agent Optimizer runs the comparative analysis across wrong prompts, frontier models, and SLMs, and tells you objectively: *'For this specific task, you should be using model X instead of paying for model Y.'* It works seamlessly like an intelligent model router.

2. **Agent Traces**:
   Observability and telemetry are essential to ensure agents don't drift off course. Agent Traces provides end-to-end distributed tracing. If an agent's task is submitting an expense report, you can inspect every single step down to the millisecond timestamp: what tools were invoked, what data sources were queried, where execution stalled, whether it got trapped in an infinite loop, or how many retries occurred. This gives you concrete engineering proof whether your architecture is flawed or if you're using the wrong model.

3. **Spend Telemetry**:
   A common friction point in enterprise AI is FinOps. Teams go to finance, and finance only sees an aggregate token invoice without understanding who incurred the costs, which business unit they belong to, or which application drove the bill. Spend Telemetry breaks down every dollar: separating production agents from pilot experiments, detailing tool invocation costs, context retrieval storage, compute instances, and even correlating costs caused by model hallucinations.

When you integrate Agent Traces, Spend Telemetry, Model Router, and custom Evaluators inside Microsoft Foundry, you obtain full visibility into your AI estate.

## 💼 Enterprise Real-World Case Study: AT&T's $10M+ Savings with Phi-4

Let me share a concrete real-world customer example from the United States: AT&T. AT&T is a massive telecommunications carrier, comparable to Chunghwa Telecom or Taiwan Mobile here in Taiwan.

AT&T processes over **700 billion tokens per month** on Microsoft Foundry. Instead of burning budget running heavyweight frontier models across all workloads, they utilized our Tokenomics framework, evaluation suites, and Model Router. The empirical data proved that for their high-volume operational tasks, they did not need a frontier model at all.

They routed those workloads to **Microsoft Phi-4**—a highly capable, lightweight Small Language Model (SLM). By right-sizing their models, AT&T saved **over $10 million dollars**.

Even for mid-market and smaller organizations, optimizing your tokenomics yields savings in the hundreds of thousands of dollars, because running AI at scale is anything but cheap.

If you don't use Foundry today, you can sign up as a first-time user and receive $200 in free credits to experiment with these frameworks. Even if you invoke Anthropic Claude or OpenAI models directly via API, you can connect those endpoints into Microsoft Foundry and utilize these optimization and telemetry tools.

The simplest action you can take right now is turning on prompt caching. Structure your prompts properly, and you will immediately shave 20% to 30% off your monthly bill.

Remember: *Instead of counting tokens, make every token count.*

Thank you so much! I'm happy to take questions outside. (MC: Thank you Ash for sharing your insights. We will now take a short 10-minute break. Please be back by 4:00 PM. Thank you!)
