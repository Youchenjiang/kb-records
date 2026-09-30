---
title: "國際頂尖學者講座：可解釋人工智慧 XAI、因果推論與反事實決策模型"
event: "國際資訊管理與計算科學特聘學者專題講座"
date: "2025-12-08"
talk_id: "KEYNOTE-UIC-XAI-CAUSAL-AI"
speakers: ["Prof. Ali (UIC)", "主持人"]
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
---

# 🎙️ KEYNOTE-UIC-XAI-CAUSAL-AI 國際頂尖學者講座：可解釋人工智慧 XAI、因果推論與反事實決策模型 (Prof. Ali (UIC) / 主持人)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與排版版**。保留講者所有原話發言、語意轉折、現場互動對話、幕後故事與問答，**未做任何刪減或摘要縮寫**；已全面修訂語音辨識錯字、同音字與專有名詞，並依演講敘事邏輯完成流暢的段落劃分與主題標題標註。

---

## 🎯 講座引言與學術背景：伊利諾大學芝加哥分校 UIC 學者介紹與 XAI 研究動機

**【主持人】**：Okay, good afternoon, everyone. Good afternoon. Okay, today is a very honor to invite Professor Ali, from the University of Illinois Chicago, and he is also the head of the Department of Information and Computing Science. Actually, he is also the senior editor of the top journal of the MIT. Okay, so I think this is a wonderful opportunity that you can be sharing about AI, and also a very good opportunity for you to interact with professors from the MIT.

**【主持人】**：Because not only we need to try.Welcome to the next stage. But now, Professor Ali is here. So, please, thanks, our panel, thanks, my sister, and if you can learn from the other. Actually, Professor Ali, he has done great research on the mice. So they are very impressive. So, we thought I think they can, we can share inside the studio.

**【主持人】**：Right. So, please join me to welcome Professor Ali. Thank you so much, everyone. It's a real honor to be invited to come to your wonderful institution as my first. Actually, it's my first visit ever in the country of Taiwan, and it's a beautiful country.Part of the day yesterday studying and such, and yeah, it really is a really an opportunity for me to have grown from Chicago to come here and share a little bit of the work that I've done to meet some new people, to get a sense of it's like experiencing this wonderful institution, National Central University.

**【Prof. Ali (UIC)】**：I drove here this morning and I saw your beautiful entrance going up the hill, and I was just wow, blown away by the beauty of your surroundings. I want to share a little bit about the work. I know that you have a background as I learned, and you may be very interested in artificial intelligence and the various ways of approaching the the field oftopic it's a transformative area right now so Ellen approximately how much time should I and for are we ending at two o'clock yeah okay two o'clock sharp so I will have to keep my remarks limited so that there will be also some time for questions and let me also make this a little bit informal by saying from the beginning that if a question comes to mind do not hesitate you can feel free to raise your hand in the middle of the talk at any point if you have a question about anything I'd be happy to answer so I will share with you a little bit about my research as well and my own scholar scholarship interests as I introduce and discuss this new this relatively untappedbranch of artificial intelligence I want to call causal artificial intelligence and want to tell you a little bit about what that is and I think it's an avenue in which there will be career opportunities in the future for you to explore.

**【Prof. Ali (UIC)】**：So I'm going to talk about what is causal AI, what kind of questions does it allow us to answer. I'm going to give some examples of approaching problems from a causal point of view and specifically why that's important when we think about artificial intelligence and its underpinnings, its outgro

## 📊 可解釋性 XAI 與因果推論：黑盒子模型洞察、政策衝擊反事實預測模型

**【Prof. Ali (UIC)】**：wth as a branch of causal inference, which is an established part of statistics and some tools. So when I talk aboutgeneralization and transportability. With a causal perspective, we can do things that the AI systems that we that we interact with nowadays, ChatGPT or the large language model based systems, chat based systems, they cannot do these things.

**【Prof. Ali (UIC)】**：They cannot do some things. So some of the things that they do not do yet very well is generalize or transport solution from one domain to another. And when they try to do it, they give faulty results. Understanding interpretability and explainability. I want to get to. Is there another slide? Which one is it?

**【Prof. Ali (UIC)】**：Is that one?Okay, there's is there a laser? Thank you.

**【Prof. Ali (UIC)】**：That's exactly it. So, interpretability and explainability, we the kinds of AI systems that we use now, we have no idea why how they're producing the results that we're seeing. You don't explain, you don't provide much insight into what they're delivering. So, I want to talk a little bit about that. And when you have causal explanation, you have a better grounding for fairness and understanding the source of bias.And then building C for systems for causal using causal AI, and then bringing it all together in a system architecture.

**【Prof. Ali (UIC)】**：So, although this is not a very large sub industry of artificial intelligence, there are some firms that are providing a causal based AI solutions. One of them is something called Causal Lens. They have a conference every year in which they show some case studies, the use cases for their work. So, this is something that you can search more and learn more about Causal Lens.

**【Prof. Ali (UIC)】**：So, they they have a very informative website as well, and they explain that what we're sometimes learning from our data is not real causal relationships, but rather correlations, and that does not really tell us why things are happening. And soThe current systems, AI systems that we see, deliver good predictions, but they don't always necessarily give us the best recommendations.

**【Prof. Ali (UIC)】**：And in order to give effective recommendations, we need to have a causal understanding, understanding of the underlying causal relationships. So, okay, let's go. Let me start with one example. At some point, it was believed that coffee consumption of coffee leads to increased rates of cancer. And the data showed correlation: people who were drinking more coffee were more likely toget cancer, but they were missing an important omitted variable, which is tobacco tobacco use.

**【Prof. Ali (UIC)】**：And so it might appear that when people are drinking more coffee from the data, they're more likely to get cancer. But you have to consider omitted. It's not that coffee consumption causes more it causes cancer, but rather they realize it's actually tobacco use that causes cancer. But people who are drinking more coffee are also using more tobacco.

**【Prof. Ali (UIC)】**：So that's just one example where correlation does not tell us why something is happening. You have to look at the underlying causes, and you look at you find the underlying causes by considering all of the variables that are relevant to the situation. That's just one simple example.Okay, so what you saw in the previous slide was a causal diagram, and in general, what I find that is that causal diagrams should be used more, not just by people who are observing correlations, but scholars, and with a with a collaborator, recently we published an opinion article, an issues and opinions article, and I'm historically explaining that there are real benefits from using a causal diagram to understand the underlying relationships between effects, and that can be useful for understanding everyday relationships, but also the reason why things are happening.

**【Prof. Ali (UIC)】**：So what is causal AI? It's a way that weGo beyond correlations to understanding why things are happening. It's a way of combining the causal models with the modern infrastructure pipelines in machine learning. So there, there is got to be a process for taking what you learn from causal analysis and bring that into the machine learning process, and then making predictions.

**【Prof. Ali (UIC)】**：But not this is important because you're not just observing what's happening. You're making predictions about what happens if a certain change or a certain policy is instituted. You're not just observing, but you are understanding what to expect if you institute a new policy.a new policy change。
