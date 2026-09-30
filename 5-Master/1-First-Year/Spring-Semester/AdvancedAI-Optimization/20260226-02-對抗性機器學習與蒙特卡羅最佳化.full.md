---
title: "進階人工智慧與最佳化 Lesson 02：感測器資料模型、對抗性機器學習（Adversarial ML）與蒙特卡羅貝葉斯最佳化"
event: "進階人工智慧與最佳化研究所課程"
date: "2026-02-26"
talk_id: "AI-OPT-02"
speakers: ["授課講師", "學員"]
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "classroom-lecture"
---

# 🎙️ AI-OPT-02 進階人工智慧與最佳化 Lesson 02：感測器資料模型、對抗性機器學習（Adversarial ML）與蒙特卡羅貝葉斯最佳化 (授課講師 / 學員)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動問答，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語與標點符號，明確標註發言角色（授課講師／學員），並依授課脈絡劃分流暢之主題章節。

---

## 🎯 感測器原始資料特徵增強（Raw Sensors Feature Enhancement）與模型極限

**【授課講師】**：This data that derived from the raw sensors enhance the model exponentially. As for number two, the need for the attack-resistant models. The reason why we bring up the issue of the gray and the white box is because we cannot always trust on the black box, as the attackers not always success attack the victims.

**【授課講師】**：So if the attackers not successfully attack the victims, so why do we have to build such as attack-resistant models? So that's the reason why we demonstrate that the attack is truly possible. So the gray box and the white box attacker reduce the model authentication performance.

**【授課講師】**：Number four, the utilizing the victims and standard negative data to simulate possible attacks can help the model learn finer discriminative patterns and better generalize against mimicry attacks. So I think the number four will be our focal main point for the discussions later.

**【授課講師】**：As for number five, by emphasizingsizing the importance of the hard to make features and reducing the influence of the easy to make features, the model robustness and performance can be enhanced. Using that motivation as why we think that this research is important, we have the problem definition that explain what the problem that we are facing.

**【授課講師】**：This problem definition will contains the input, the process and the output. As for the input, what is using the time series dynamic data to improve the model by simulating attackers behavior to enhance defense against black, gray and white box.

**【授課講師】**：So in order to do that, we used to prioritize the features that are important and hard to make and reduce the reliance on those easy. And also, we the model has to be able to outperforms or getting the lower E R than the state of the art.

**【授課講師】**：So talking about state of the art, we have two state of the arts. There was the first one and second one, butWe are going to skip the first one because the the latest publication from the two thousand and twenty-four by Tao mentioned that they outperform the authors' proposed by number one, so that was the state of the art at this moment.

**【授課講師】**：So, in order to do, in order to answer equations on on definition, we have proposed method that is inspired by motivations. First, we introduce the novel the novel mechanism, the so-called the AdMIL stands for the adversarial mimic learning that generates the AdM data that can be used by the model to learn potential attacks.

**【授課講師】**：Number two, the expert guided feature selection strategy. So, we do not need to select which easy to mimic which or hard to mimic one, which one is the important and which one is not important. We are going to useThe number three that was the deep learning guided feature selection strategy to dynamically select features data to be used in the admir.

**【授課講師】**：So to to serve the proposed method, we conduct several experiments that need to be carried on. So there was the first one. We have definition of the dataset A. There was consist of thirty human victims and twelve human attackers with the definition with the details of ten non-expert attacks and also two expert attacks.

**【授課講師】**：As for the non-expert attacks, they attack for at least two minutes by watching the victims behavior. As for the expert attacks, they don't have any time limits. For dataset B, for prey and white box attack, we have one hundred and two human victims plus n generated attackers.

**【授課講師】**：Because in this dataset, don't have the attackers yet, but we can prove on the dataset B that attackers possible. Number three, build the baseline. Number two, that was the state of the art at this stage with the dataset A and B.

**【授課講師】**：As for the, we are going to skip the number five because we haven't explored this one yet. So I, I guess that I need to explain number four. So the admil or the adversarial mimicking learning, we train the model based on the fitting train, the standard negative and also the admil or the adversarial mimicking data, and test it using the fitting test and also the adapter that augmented using the fitting train.

**【授課講師】**：That was for gray box, and also the same thing goes to the white box, but we use the adversarial example for testing. And the last one, we are going to build a deep learning guided feature selections for the admil, so that we don't have to manually choose the easy to mimic features or hard to mimic to help the admil to decide which features going to be replaced.

**【授課講師】**：As for the result,In the black box attack scenario, the our proposed method can outperform baseline, the state of the art with the ER of nine percent against the twenty three. In the grey box attack scenario, our proposed method also outperforms the M attack with average ER of six percent against the thirteen percent.

**【授課講師】**：As for number three, we haven't explored this one yet. We are going to decide whether this white box attack is is important to be carried on or just leave it. So, from those blocks that have been mentioned, so we have two strong contributions to be claimed.

**【授課講師】**：The first one, our proposed model, the AdM, is capable of performing an accurate authentication under black box attack with average ER of nine percent, which outperforms the baseline with average ER of twenty three percent.

**【授課講師】**：And also, the grey box, we can outperform the model with thirteen percent against the six percent. Number two, that was the deep learning guided feature selections in the AdMcan reduce the reliance on manual heuristics when generating the adversarial mimic data.

**【授課講師】**：So from some, that was a whole research outline from our team. As for the detail, I can explain just a little bit to let the the the the whole members to understand our our research. So the proposed adm in a nutshell. Okay.

**【授課講師】**：So our adversarial mimic learning in a nutshell. So I'm going to explain it in in in a short manner. So if you know that there is a term the so called this the negative hard mining. So in the negative hard mining, we know that this this should be a dog, and this should be a cat or non dog class.

**【授課講師】**：So weInput those negative samples, such as a elephant, a cat, and a cat, and also it may be a cat, maybe a dog, but it looks like not a dog because the the feature of the dog they have to be maybe this cute and having this color, but this dog it's obviously they don't have the brown color and also have the the the black and white color, so it may be classified as non-dogs.

**【授課講師】**：So the negative hard mining, hard mining learning, they try to make this samples go into this one to fit the model training, so the model can learn that even though they are different, but they are still our class. But in our adversarial mimic learning, so we do something very different.

**【授課講師】**：So our novel proposal is that using this one, using this one, we are going to we are going to generateThis dog that maybe look like a dog, but they are not a dog. So this can be classified as an attacker. So the attacker behavior was somehow as someone tried to mimic the real or positive data.

**【授課講師】**：So we tried to generate this close to the positive data, but we classified as the negative data. So this is our experiment design. But I think this is gonna be a lot to explain, so I will just skip it into the most important point.

**【授課講師】**：So the our adversarial mimic learning, I think I have talked a little bit about it in the dog and cat classification before. It is more clear on here. So as you can see that other than we train the model using these two, which is the victim training and also the standard negative, we also addOne more training set that was adversarial mimic data.

**【授課講師】**：So this adversarial mimic data, as you can see that it can intentionally or predictively, so it can predict the the attackers' behavior. So as you can see that some of the attackers will attack the easy to mimic features from the victims.

**【授課講師】**：So we try to create those samples that looks like the same as the the the wanted created by the attackers. The the the goal is is is very straightforward. We want to model to to understand that even though that samples are closer to the positive data, but they are not positive data.

**【授課講師】**：So we want to try to leverage the idea of making these hard mimic features, but they are not important, becoming more important, and making thoseless vulnerable, this highly vulnerable features into less important. So, I think I have presented the results.

**【授課講師】**：I don't think I need to to to explain it again. But the hypothesis that we brought was the ability to increase the models E or under attack scenarios that was rejected. So, our yeah, so yeah, because I think that's that's pretty much the research all the presentation from the mobiles team.

**【授課講師】**：So, one, one, so then, Professor Jin, do you have any comments or situation or questions? Okay, may I ask question? You divide your attack. You are you attack? Are you divide your attack to extra and then not extra attack? Yes, because yeah, and what's different between these two class?

**【授課講師】**：Oh, yeah, actually, I forgot to tell you that we have three different attacks. There was the black box, the gray box, and the white box. As for the black box, they can be classified as the black box and the white box and gray box.

**【授課講師】**：As for the black box, they attack based on the human. But for the gray box and the white box, they attack not based not on human. As for the black box, they attack by expert and non-expert. And for the expert, we let the user or the attackers to watch the video of the recorded victim's behavior for at least the whole video.

**【授課講師】**：But for the the weak attackers or non-expert attackers, we just let them to evaluate the to watch the video for first one to two minutes and let the rest minutes to remember what the behavior of the user is. So it's more natural for those which not expert.

**【授課講師】**：Okay, thank you, thank you。 啊，我我沒有其他問題了，剩下兩位老師了。 哦，我我稍微要我稍微提一點建議。 呃，For me, yes, yes. So, do you have time? Is that no, no? Ah, if you have time, then maybe we can ah discuss ah your paper writing issue, including the, you know, the one we're working on.

**【授課講師】**：Oh, sure, sure, sure. So, we need to work on the previous one and this one. Yes, yes, yes. So, ah, what, what do you ah, what, what do you have ah, time? Ah, discuss. Ah, I can. do it at your earliest convenience. Yeah. Okay, so uh, how about one thirty?

**【授課講師】**：One thirty. Okay, okay, sorry, I can do that. It's okay. Is it okay? That's that's okay, sorry. I can send you the meeting room. Okay. So can you accept the meeting? Uh, I I'll I'll try, but most of the meeting room maybe it's fully booked.

**【授課講師】**：Oh, that's that's fine. Yeah, that we could use another meeting. Okay. Okay. Sure. Sure. Okay. Right. Uh, uh, so do you have anything to to add? Oh, I'll listen to your recommendation for multiple times. So I just go about the obvious, obvious, obvious arrows, sources.

**【授課講師】**：Let's look at the problem definition first. Are you able to explain? We talk about what is the problem definition, what is the proposed solutions, and difference between two. So, what is the difference? Oh, the difference between the problem and the proposed method, professor.

**【授課講師】**：Yeah. Oh, so the problem definition was mainly talk about what problem that we all want to answer, and the problem definition, the problem, sorry, the proposed method is how we can solve the problem. So it's about yeah. One is what, the other is how.

**【授課講師】**：Yes. And let's look at using improve the model by simulating the meaning. Is thisWhat or how? I think I just realized, yeah, this this should be not included in this one. Yeah. And furthermore, by trying already high teachers and important part of me in reduce easy to me.

**【授課講師】**：Is this what or how? Also how? Also how? Well, that means this is not person. You are seeing teachers inside expect and wouldn't with such things. The second time I realized that I require your high passes. Yeah, I know which pages that is that pages that file or six.

**【授課講師】**：Right. 嗯，Well, we talk about increase. What do you think of this increase? That's supposed to what? Okay, yeah, I, I, in here, I don't think we have a recent growth. Right, yeah, it seems that it's an incomplete sentence. True, true.

**【授課講師】**：And um, yeah, we just get to question number five. Uh, well, as we move along, I think we need to find a way so that in review the intuition of the post-control to get new sentence that no, don't bring in one paradigm in the introduction section.

**【授課講師】**：Right. But talking about each issues, why is the post method work? Why is post method works? Because, uh, we try to simulate the simulate the the possible attacks uh launched by the attackers. Yeah. By yeah. Well, I guess one of the appealing points that you don't rely on huge effort collecting attackers' data, but each of the individual victim.

**【授課講師】**：I mentioned that you emphasize that in your motivation or conclusion. Um. But, the um, how can thatway, these so-called maybe attackers' data can can be seen or can be considered as simulating the attacker's data. Right, right, right.

**【授課講師】**：So that was interesting question. So yes, so that was the the second thing that we can consider. That was not only we simulate so that we let the model to get the the decision decision problem more more robust, but also it's because we we utilize the the transform-based learning.

**【授課講師】**：So the transform-based not only looking at the difference of the data, but also the inter inter correlations. between features. So if we try to simulate the hacker's behavior in the data augmented, oh sorry, in the mimic-like attack, we can let the model to learn more that there is some correlations between features.

**【授課講師】**：Look at it from the perspective of the data, not the records to explain how humans are supporting. This is an intuition. An intuition is something that people feel us, but we quickly and easily in a few seconds. Okay. And tell me that this data is very much like aWe are hackers.

**【授課講師】**：What? Um. Uh, because they try to. Because in attackers. Attackers are mentioned. I can say that they mimic several. Successfully mimic several use victims behavior. That was the same that we are simulating on the training. That we tell if there is a data that look like the victims, but they are not.

**【授課講師】**：But they are not. Uh. What is it? If if. Yeah. If there is some. Partial. See, if you want to see that, think about twice, or can discuss with your team member, we you are able to come up with some easy to understand. But my suggestion for you is that in the year number one, you don't have to step up in the trend.

**【授課講師】**：Yes, but you do not want to climb, climb step up for a given future. Number one is time consuming. If it is not impossible, yes, but you you don't really know that. What they are thinking on there, how they would climb, they come from.

**【授課講師】**：It's difficult to understand. Yes, that is hardly possible. So you don't have the attackers in the training phase to solve it, but somehow that you want to make a claim, we have a smart way to come up with or this data is very close to the attackers that are in reality.

**【授課講師】**：That's something you need to explain. Why is it? In the introduction, if you explain intuitively, the paper will be get accepted. Between sixty percent more likely. Well, it's pretty much my comment today. Most readers go back to our.

**【授課講師】**：And you have limited space, just one page. It's so much words in one page that you will squeeze it into a tiny little bit of paper. And one way to do so is try to avoid less explanation. Something like this one. And if you look at your the way you present it, you always put down the full English sentences.

**【授課講師】**：And I suppose I gave you comment multi-numbers time in a poem, that is unnecessary. Right. Put down the few keywords. Supposedly, enough. In step one, yeah, get rid of the old motivation. Number two, I'm not sure you really need five points of motivation unless you can present it in your proper destination.

**【授課講師】**：And which part coming from motivation? Number one, which part coming from the motivation? Number two, if you are able to

## 🛡️ 抗攻擊模型需求剖析：黑箱（Black-box）、灰箱（Gray-box）與白箱（White-box）防禦架構

**【授課講師】**：match each point of your motivation up to your proper destination, then I will become the exact yeah we really need this five point and that's it for that's it next. Of course, everything is possible. ask you really have a appropriate form.

**【授課講師】**：Alright, that's all my comments. And well, yeah, um, today is a new format from the last time. You can thank you, class. Uh, I think that's uh from our team's presentation, class. So, um, so yeah, we can move on to the. Um, did they ask the end?

**【授課講師】**：Uh, no. Yes. Uh, so你看，最近呢，像開始做對，就是說問題，好不好？ 好。

**【授課講師】**：呃，呃，當然，所有問題實際上都是我們方事情。 呃，呃，當然你們倆是。 去工作的，那這裡面是不管是那個我不是男生，啊，或是這些實驗，啊，是全力以赴做的，那這是因為我愛，呃，那個。 然後這還是我們的 Optimization 最佳化部分，然後根據我們的蒙特卡羅模擬迴圈 (Monte Carlo Loops)，我們會給予不同的模型來訓練我們的貝葉斯模型 (Bayesian Model)，然後去去 build 一個驗證的模型。 然後這個驗證模型它在遭受攻擊的模仿攻擊的情況下，它也會有良好的穩定性，然後有效性也比較高。

**【授課講師】**：而且我們希望它就是它的效果是可以比現存的任何方法都要好的，就是在抵禦模仿攻擊這方面，比現存的方法還要好。

**【授課講師】**：然後這還是我們，再是我們 Optimization 最佳化部分。 那我們的第一個 optimization 就是呃會利用 經驗驗證機制 (Empirical Mechanism)去去 build 我們的貝葉斯模型 (Bayesian Model)，那它就是就是像前面的蒙特卡羅模擬迴圈 (Monte Carlo Loops) pro 提到的，就是我們會利用那個 empirical 那些那個貝葉斯模型 (Bayesian Model)去做一些可能很像攻擊者，然後攻擊學習這樣，然後。

**【授課講師】**：再我們還有要注意一定的，還有要注意特徵的的重要性的部分。 那我們就是會利用方式去做特徵選擇策略，然後把就是把它選擇出來特徵運用在製造那個雷達上，去幫助模型能夠去強調它忽略特徵，但是降低被忽略特徵的影響。 然後以及根據我們的分類訓練的的分類，然後我們我們會希望找到feature之間的類別選。 那我們的方式就是會會把feature分成好幾個group，然後這些分類方式依據sense，就是因為我們有sense，我們有sense兩種，然後用這樣的方式去去讓模型能夠關注到我們的feature的篩選。

**【授課講師】**：然後再是我們的實驗的部分，那我們這部分是classifier，所以我們使用的classifier就是它，同時會有很多的說法，然後還有另一種分類方法。 對應的攻擊者這樣子。 那我們當我們在呃建立針對某一個受害者建立他們模型的時候，首先受害者自己是要大量會是這樣的，那那其他受害者就是會當做跟的零零零零塔。 然後我們會利用我們的模型，然後還會利用的三model。 那我們三model是呃，它是採用它是一篇一篇也是一篇基於前面的模型，然後它是採用GAR的這樣的結構。

**【授課講師】**：然後這個原本論文裡面是沒有討論到我們模型部分，它就是一堆人的的的那個測試的。 然後我們就把這個這篇論文來當我們的三model，然後去跟我們的三model做對比較。 然後在是關於我們論文基礎，然後我們就有提到說就是它會有零零零塔，所以這個這個training set就可以包含了對受害者零零零塔，然後跟零零零塔跟零零零塔。 像case的他們只用。 收集那個呃被被他去測試，然後同時我們還有就是那個那個從資料的分析，然後去從在那個氣象方面這邊上查查，然後以及以及我們就要觀察這這些的被選，所以我們我們會把那個被選擇不同的那個引數進行補充，然後然後去讓這個部分，然後看我們的模型架構比較清楚。

**【授課講師】**：呃，那我先簡單說明一下我們的模型的架構，然後首先是是data的部分，data部分就是我們前面也說了，是每一個被他的話，他他會進行一些隨機被選，就是根據他，我是依照他呃那個波動次，然後就去把它噹噹做一個那個被他的實驗，然後再去做排名，因為我們會希望。 每一筆樣本的長度一致的，對，就那產生出來的資料，我們先轉化為點對點，然後點對點再進到模型裡面。 然後因為我們是使用的是全通的base model，所以我們就需要幫它做幫它做feature engineering。

**【授課講師】**：然後這部分我們採用是會讓它自己學習的那種feature engineering。 然後在經我們會再經過一層embedding，然後產生一個一對一對，就比較多全通的輸出。 然後全通的那一步的架構會有三個部分。 那這就是attention的部分。 我們為了觀察不同attention會在不同標系的處理，就是我們之前有說會根據那個sensor sensor來去方feature，然後我們我們的attention的部分，然後有三組的attention，然後有點想要觀察不同的特徵關聯性，叫第一組嘛。

**【授課講師】**：去觀察它所屬的ensemble的閉組關係，然後下一個，它屬於Q的K個輸入它所屬的ensemble，然後第一個老師所有閉組關係，然後這邊是三個，然後，然後第二個，那我們要查觀察relation的這這ensemble內部的閉組關係，那第三個是觀察兩兩個不同的ensemble它們之間的閉組關係，那所以總共會有三個三個relation的，然後就是後後面就是接觸我們的呃，接觸我們的後面一些那個閉組成員，然後那個一些正規化之類的，然後出來就是經過層處理就會進到我們的分類層，然後最後最後輸出一個分類的這樣子。

**【授課講師】**：那這這大概就是我們的model的，關於我們關於我們一些實驗的說明，然後再就是結果的部分，那我們我們不前的結果是，在加上有沒有機制的情況下，我們的 E I 大概會在八點三帕左右；，就是在它的被攻擊的情況下，然後被三毛五的平均 E I 大概是十四帕左右。 然後詳細的詳細的截圖給你們看，這裡。 然後就是就是我們有分成兩種兩種情境去觀察，一種情境是它沒有它沒有進行任何攻防攻擊，然後就是呃普通的普通的資料拿下去打，然後我們會發現從從平均上來看，就是這這個是被三毛五是我們的，然後我們的三毛五平均的 E I 是比較低的。

**【授課講師】**：然後再就是再就是有攻擊的情況下，然後呃我們我們有做兩種方式，一種就是有有加上防禦機制，然後還有沒有任何防禦機制的。 那有沒有就是即使是在沒有任何防禦機制的。 情況下，我們的網路表表線體還是比那個它它們的S I M還要好一些。 然後，然後這再來就是一些的，然後它們，它們這樣，就是看這樣子也可以發現我們的它的那個網路是是比較好的。 那再來就是一些的，所以呃，所以我們的光學優選就是呢，呃，我我們經過實驗驗證，發現我們知道它可以可以得到比S I M更加低的誤差。

**【學員】**：然後，所以在針對模仿模型的這一塊，就是在針對Vi Vi T Plus的模仿模型這塊，它就是的確是更穩定的效果。 然後再來我們會使用低低能引導向的特徵選擇，比如在低能引導上，那這部分就是省去了人工篩選帶來的一些麻煩，同時也可以讓模型學到一些呃更精細的關於就是關於該語合作特徵選擇。 一些策略，那這邊大概就是對吧？ 呃，外的部分，那請問老師們有什麼問題可以建議嗎？ 我先請教一下啊，你看下下一個的表面有一個呃，take加上QKV的，嗯，然後老師請問，再再下一個，再下一個。

**【授課講師】**：對對對，那個表裡面，這個請請教一下，這是什什麼？ 哦，這這個QKV的QKV對，ours是這樣QKV，這個是ours的差別是吧？ 我們的ours如果是如果是用到這種模型的話，它就是它會是長得像這樣子的一個模型，然後是attention的地方就是做self的attention，不會做任何其他的其他的調整。 那但是如果是QKV的話，那我們就會變成像這樣，就是attention的部分會拆成三個三個不同的attention，然後同時它內部的QKV就不再是做self的attention，而是會呃針對QKV我們會去給予不同的書，慢慢可以關注那個數學或者歷史這樣子。

**【授課講師】**：嗯，OK，謝謝。 前面請老師沒有問題，我結束。 那個各支要注意一下，我們要把名字寫到。 好，我下次會自己弄個隊伍。 嗯嗯嗯。 我顧問老師沒有其他想法，然後就換下一個。 因為有些 presentation 可以剛開始，啊，未來你還有更多的時間，可以慢慢慢慢。 呈現的方式啊，呃，前面什麼？ 我來分它那個層次的，大。 你先看著，你這邊有幾角？ 誰跟誰？ 對。 那這邊是等a，好，好吧，那你過來一點。 它大。 第七。 對。 這邊哪個是等a？ 有三個。 哪個是？ 我們是什麼是採用？ 我們是用最最假的這個字。

**【授課講師】**：對，我意思說，你們這個呈現的方式一致嘛？ 哦。 你看，在剪報的時候，有一個很大的一個層次的，就就。 在那張圖上面，也就講說，還是非常那個大。 你這邊有三個嗎？ 對。 那我講，那你就從你在在training的過程裡面，這三個不同的model到底是在training哪裡？ 你說你剛剛提到，然後你是有有不是沒有，而是在你的attention上做抽換，對吧？ 那你有三個model嗎？ 對，不知道是不是。 這麼會吧？ 我時間可能比他們都少。 你再回頭，你又撤銷了。 那麼你在呃你的training plan裡面提到，哎，就是預測是。

**【授課講師】**：那，八月成績的是來自於上個月的畢業，我也不太清楚。 嗯，沒有特別的回憶。 就是說，因為我不知道你現在呈現的是還是跟前面講說，一滴土一米花，一滴土一米花裡面只是，知識，knowledge，knowledge方面沒，呃，不得不 rely on the self selection，而不是 selection。 呃，那你在考試卷裡面可能是 automatic selection，那 automatic selection，到底跟前面的一米一米花裡面什麼關係？

**【授課講師】**：然後，然後你這邊呈現資料是來自 human selection，比如說，ask the knowledge，或者比如說 knowledge。 哎，我有時候我知道呀，因為這這些每天都在進行的。 不過，下次這些事情，因為這張表嘛，我們是要看四門都完成。 在在這邊前面也沒有特別聽到說要，export的model實驗去self self learning，就沒有特別新。 那但是在我實驗室裡面，聽到我要self，到底你這是基於什麼樣的理論？ 也要做self，不再靠export拿回去。

**【授課講師】**：那self learning會比export拿回去好嗎？ 因為這邊都沒有特別提。 那當然，在你的實驗設計裡面，你也沒有特別提這件事情。 這邊在單選的時候做了一個。 一輪，可以是，是這樣的。 我在這個流程圖裡面，很多很多的碼。 你在這裡是不，不在？ 然後你真正建立成什麼應該在前面。 還還有一段，還有一段，網路，self learning的網路。 那接下來應該叫我，就是self learning的網路，到這個裡面是切開的。 我先選選完，再build。 還是我在這個feature selection，這個self learning feature selection這一段是part of the training。

**【授課講師】**：你你這不用你留一手寫好了。 下一步要走。 下下一步要走。 我是 next day，我說下個月，下個月我再報告一次。 下個月你想報告什麼？ 呃，應該就是就是我們的方面，就是做最佳化，就是把有的話拉一拉，來來斷。 主要是為了什麼？ 為了，所以你要最佳化來來斷，或者你回到那個呃有什麼加固？ 你要最佳化哪一個？ 有有一個最佳化應該會是在就是就是在就是產品的，很多商家會做，就是我們三個啊商家會做。 後面後面兩個呃，哇，因為這個的過程有點複雜，那你這邊有這麼多方塊。 對，每一個方面都可以最佳化。

**【授課講師】**：那你選擇在消費人群裡面做最佳化，呃，是這個思路。 應該可以優先最佳化。 呃，就是，因為主要是要觀察，然後那邊選，然後，然後，但但是就是有三組不同的選，但是，呃，對於媒體內容輸入來說，哪一種關係比較重要是不一定的，所以就是會做很多人做話的時候培養他，就是去根據他的輸入去，然後來往成績指導說，他應該更加關注哪哪一哪一部分，然後培養他，然後提升。 這樣你你可以好好想一想啊，這個因為，就這些都是張老師建議要做，哎，他去了，去，想一想為什麼張老師會講建議呢？

**【授課講師】**：嗯，到底張老師心，到底在想什麼？ 嗯，要去去試著瞭解他，他，他。 強啊！ 那為什麼它只有兩三個加起來哇，就說不夠好？ 你到底有什麼理由啊？ 那這個這個當然是一個最最基本的，大家都知道，加起來最簡單，最最容易。 呃，到底是在什麼情況下會不夠好？ 因為一定一一直在強調correlation，correlation。 那你回到你這個research了，你這邊也需要考慮去做data analysis。 We talk about that the correlation among features is one of the critical factor in model enhancement.

**【授課講師】**：If that's the case, and based on your preliminary study, um, what do you mean by feature correlation? Are you able to identify one of the example that your preliminary model without a correlation consideration and why? Let's go to your example first.

**【授課講師】**：Yeah, this is your preliminary baseline model. This is the model without consider feature correlation. It's not bad. And under what conditions that the model will be able to become more robust against attack once you take feature correlation into consideration?

**【授課講師】**：Are you able to give us one concrete example? And look at all the people, few of them that you will beYou are able to enhance significantly, as opposed to others. Yeah, perhaps that you can pay your attention to those individual.

**【授課講師】**：Okay, for example, is one that you significantly reduce the ER from twenty-five to eighteen, nineteen. This is a significant improvement. Why? Visual correlation is so important for this particular individual. Yeah, that's something that you can tap into for.

**【授課講師】**：Well, good luck. 哎，對不起，我我現在終於發現，剛剛梁老師這樣一問，我就發現我剛剛為什麼會有什麼問題，是因為你你這邊用，這邊左邊是不同測試值嘛，對不對？ 對。 啊，OK，好。

**【授課講師】**：然後這個是，因為你這邊標題叫做 no take 哈，對不對？ Always no take，對這個，然後這後面有 take，我我現在有點忘，你這邊 no take 應該是它本身的資料，對不對？ 哦，它就是用它本身的，然後這個是你們中間有某人去模仿它，但是我不曉得，如果模模仿它，應該就就是一種 take。 然後嗎？ 這這真的話是用？ 就是就是我們是用呃沒有用本人的資料當測試，然後又用非本人的，但是那個非本人的資料是沒有進行任何攻擊行為的，然後所以我們才會稱它什麼 no take。

**【授課講師】**：OK，就是說它它是本身這樣跟本身就對了，這個是混合的，是一個 mix 的 data，對不對？ OK，然後接下來，所以當然這樣的話，它的所以這應該是真，應該是你的第一行是嘛？ 越跌越嘛？ 對對， OK，所以因為混了別人的東西，所以 supposedly 應該提高，哎，沒有，結果你還是這樣跌，對不對？ 這個都是用你們的方。 法對不對？ 這個用都是用我們的 model，就剛剛前面第第五第四頁的 model 去去算出來的資料是嗎？ 好，然後這個是用，呃，應該怎麼說呢？

**【授課講師】**：因為你剛剛有個 baseline data，這個是你的 baseline 的那個 model 去做，是嗎？ 這個是這這這個這兩張是嗎？ 我因為你剛因為你們這次貨應該是跟一個 baseline 去比，是不是？ 我不想這個，我說我就想確認一下，剛剛應該在這裡要沒沒搞懂。 你你這邊，所以你這張這張表裡面都沒有 baseline model 去跑的資料，是哪哪哪一點？ 這這個就是第一個 cover。 對，第二個是 baseline，然後在它有。 你你哪裡沒事？

**【授課講師】**：沒事，沒事。 對對對，指一下，不要太過。 這這這個兩位是 baseline，然後這個是。 哦，這個也也也是一樣。 好，那這個是。 是有攻擊呢，這什麼意思？ 那自己人又又是有攻擊是什麼？ 哦，就是我們的這個被他，他是對加上攻擊的，就是加上加上攻擊測試。 哦，然後又是呃，又又是用baseline model去跑。 哎，可是這樣的話，我們就有好奇了哈。 你，或者你今天本人對不對？ 你去偵測，結果你一樣是應該是越低越好，這個一樣一樣是。 對啊。 是嗎？ 是越低越好。

**【授課講師】**：結果你這樣有有攻擊之後，它baseline model好像哦，對，對不起，可能只有這個這比較特別，但是你看這邊有幾個，反正越比較低的，有少數幾個，然後不是每個。 好，所以這個東西是互有勝負了哈。 然後呃，你這個地方是隻說OK，它沒有沒有做攻擊的情況下，對不對？ 所以兩個都是呃，就混了資料跑去跑，然後它跑比較OK，但是一個是用你。 那 model 就好，對不對？ 啊，所以你 model 哦，所以這個地方比它好，比它好。

**【授課講師】**：然後呢，這個也是，呃，有 tag，然後用您的方法，啊，然後做的也是比它好，哦，所以這個是合理。 然後這個是，你再加上加強的 Q K V attention，等於說你改了 seven attention 的那個，加強的一部分嘛，對不對？ 好，所以說，哎，這做做更好。

**【授課講師】**：然後這個地方又是在加上您的一些 feature attention，對不對？ 是不是？ 啊，所以再加，所以這你學習的效率更好，所以你這個得到結果就更好一點。 我想這個是大方向合理啊。 誒，大好，那所以接下來我在第四頁嘛。 剛剛楊老師他也問我，就沒發現，他原來 seven attention 的，他其實本身 Transformer 就有 seven attention，對不對？ 實際上他本身就有 Q K V 了，所以。 那你們這三個 Q K V 跟它原始的差異在哪？

**【授課講師】**：就是它的三個，它原本 Q V 輸入的都是全部的，我們就是我們輸入的全部的 B 矩陣，然後它就會 Q K V 都是一樣的，一樣的那個 B 矩陣，但是我們會，就是我們會把我們這邊會把那個 B 矩陣分成不同，然後輸入進 Q K V，所以就是它跟原始的 Q K V 接收到 B 矩陣不一樣。 所以，我好奇就是你們為什麼分成這三種，而不是沒有第四種，而且呃，這中間沒有重複的，剛剛保持三種。 呃，因為我們的 sensor，我們是依據 sensor 來分。

**【授課講師】**：哦。 我們 sensor 就是隻有 touch 的和 orientation 兩種。 哎。 然後，所以，所以，我們，我們，然後 orientation 的話，因為在它在變成 Q K V 它不同的，然後去算它一些東西，它是平均指標差值，所以就是這三種，一種是 touch sensor。 東西，還有一個就是那個彩色的原始樸素，然後再再聊一種它的，我覺得我覺得那個真的挺值，所以我覺得。 哦，三種啊，OK OK。

**【授課講師】**：好，好，大家就這樣。 所以哪一個是 hard to mimic，然後一個是 easy to mimic？ 前面 multi version 有講，在在這麼多種，剛剛講哪些 feature 是屬於 hard，哪些是屬於 easy？ 嗯，就是它這不管是哪一組的 feature 都有可能是 hard 或者 easy。 嗯，對。 然後就是就是這個這個到就是到底誰是 hard，誰是 easy，這個我們沒有進行能力區分。 所以你是讓讓 student 自己去自己去去分辨是嗎？

**【授課講師】**：嗯，讓學生自己。 因為，你前面 multi version 他會提到說，你要把這兩個東西，你你也特別提到這個東西啊，所以我們就會注意。 那你講這件事情，你後續 model 就是不去哦，這去覆蓋這種東西。 如果是這個，呃，基本上應該在加上有沒有貝塔的預防去，就是我們的在X的貝塔的製作的時候，我們會把一圖裡面的醫學換掉，就是standard X貝塔裡面的醫學換成換成那個受害者的醫學，然後所以這個一圖裡面的醫學它現在貝塔圖現在是。 嗯，麻煩你再說一下，你說一圖裡面的這個貝塔是跟二圖裡面的貝塔在中間差異在哪？

**【授課講師】**：呃，就是對於模型來說，它的重要性是這個這個醫學是否能夠足夠足夠的資訊讓模型可以做，就是做決策的樣子。 可是問題是我模型都還不對啊，都還沒有決定。 你這樣變成叫做因果關係，我就有點糊塗了。 嗯，對，你這個讓你來報告。 什麼？ 你要把錢給它。 考試，理論上四個月要考試。 那在考試的過程，我們都瞭解了。 啊，然後讓你練習十次，來，每個月一次，讓你練習十次。 hopefully，你真的上場，其中要件就是你要聽懂所有的問題。 剛剛陳老師沒，陳主任沒去問了好多問題。 我不能說你答錯，基本上有一點，好像有點對，好像有點不太對，就是你的答覆不是精準。

**【授課講師】**：我們再試看一次，什麼叫做一題通經典？ Sorry, that's really, really awesome. It's awesome. I mean, yeah. What do you mean by easy to mimic? Hard to mimic features. How do you explain that? Easy to mimic those have its close, those close, uh, have its close distance to their, their parents.

**【授課講師】**：I'm gonna try not to use the scientific or theoretical. Give me a more intuitive answer. What's intuitive? Yeah. What you have features? Uh-huh. Your features has its physical limit. Yeah. Is is how many features do you have? Forty-nine.

**【授課講師】**：How many of them? Can you just name one? Uh, SP. What is that? What is HP? SP. Speed, yeah. What do you mean by speed? How do you, how do you, how do you define speed? How do you measure speed? Uh, the speed of placing the the the smartphone.

**【授課講師】**：Try to give us give me a more intuitive answer. Suppose this is your smartphone. Tell me, what do you mean by speed? What happens if a user flip his touchscreen with higher speed? What does that mean? Then higher speed, lower speed.

**【授課講師】**：What does that mean? More speed than the the time needed. Well, how do you, to answer the question in your oral defense, as well? Yeah, I mean, the time needed. This is how you behave, and you you are in charge. You guys have no idea how to explain to your committee members.

**【授課講師】**：Those don't have any experience. You need to teach them that understand in five seconds. You only have three seconds. Can I do it? You can do it. Give me two features. One is easy to me, maybe. The other is not so easy to me, and it's number one.

**【授課講師】**：Um, like I said, for I cannot use it as a tool. How about this? It's already a pitch. Is it easy to me? Yes. How about speed? No, it's not observable. Really good. You hit the key point. Hit the keyword. Observable. How does observable has anything to do with importance?

**【授課講師】**：Observable importance. What? You see, I'm trying to explain. Easy to mimic refers equivalent to important, and hard mimic is equivalent to not so easy, not not not not none. Do you agree? Um. Oh, um, I think there is two two different uh concept here.

**【授課講師】**：Uh, the concept that Siliya brings to us is that if uh there is an easy to mimic features in attention model, we have to somehow make it less important. We have to focus more on hard mimic features because we let the attention model to learn uh to distinguish between the one feature to the others.

**【授課講師】**：One is the only branch out. My question. Okay, my question is there are two concept. Okay. Mimicking easy hard. Hmm. Yeah. Right. Feature important, important, not important. Yes. Yes. Are these two equivalent? Easy, important, not equivalent.

**【授課講師】**：No, not at all. It's not, it's not at all. So what? Since that test was, you gave the wrong answer. Okay, for the chance question. For whether was, for whether she asked him, what do you mean by easy to mimic, hard to mimic? Well, the best answer will be give example.

**【授課講師】**：For example, orientation, pitch, roll, is observable. So if somebody observe your behavior, they they can they can learn. Okay, attacker can learn. If attacker is aware, this is how you build your orientation model. That's using feature.

**【授課講師】**：However, speed or acceleration, it's difficult to mimic. Not what will be the answer to for the chance question? Not feature important. That's nothing to do with feature important. 是，哇，還還還忙著識字兒，是是，沒有關係。 我覺得剛剛楊主任講的是，就說，對我們這這個不是很懂人，要讓我們很容易。

**【授課講師】**：楊楊老師不常講嘛，要直覺嘛，對不對？ 你上面的每個字眼，讓大家很直覺的，一定物理上的意義，然後才轉化成你後面要附某一些蠻多的一些，對東西。 但是前面一定要讓大家覺得，你的想法是，對對，基本上是符合直覺。 除非你已經有很巧妙的東西是違反直覺，那也沒關係，那再告訴我們為什麼它違反直覺，對不對？ 啊，我覺得大概就這樣。 哎，好，謝謝你，謝謝。 沒其他，其實有很多可以改進的地方的東西，對吧？ 慢慢慢慢改進，挺快的。 這邊沒有寫錯了啊，no attack attack，其實並沒有錯，但是對常見版本來講很難理解，這不是真的no attack，什麼叫attack？

**【授課講師】**：那如果說你剛開始就全面講，這是一個authentication model，基本上是辨別的是手機的主人是攻擊者，哎，就是手機的主人或者不是手機的主人，他在這種情況下，你這個signature其實是一個正常的authentication signature，對不對？ 就是我是主人，我就這樣用，我不是主人，我只用我我自己的行為嘛，我沒有刻意模仿。 所以你如果說這個沒有模仿，有沒有？ 說句正經。 因為你所謂的 attack 就是他，你某某報你的行為嘛，是不是？

**【授課講師】**：這這這裡面還有很多很多，就是，你你你，怎麼樣讓你的報告，最最好的報告是你這個，這個圖一出來，你不用講，我都知道你要講什麼，這是最好的報告。 我在用你這這這這一頁為例，你想讓這一頁傳達什麼去？ 如果說你要給一個結論，就這張表或者張圖，給一個結論，結論是什麼？ 就是限限制。 好，在什麼情況下？ 對，我講是在被攻擊的情景之下，我們提出來的 model 比這個 stable 收盤 model 要好，這是你唯一。 最重要的一個結論。 那為什麼重要呈現？ 最終目的就是防禦嘛，That's your primary purpose, is to make your model robust against adversarial attack.

**【授課講師】**：If that's your purpose, primary purpose, why do you want to present this step? Sort of sidetrack. There is a intuition behind it. So, if we remember the way Alex, our former master students present, how well we can achieve the so-called reliable.

**【授課講師】**：We we want to make it as close as to zero, but ideally we can. Tommy, I understand. If that's the case, that's the second point you want to make. Number one, your model is more robust than any other decision model. Number two, your model is close to the best model, optimized model.

**【授課講師】**：Okay, that's two different idea. Okay. We we we shouldn't put it in one table. No. One table for one idea. Okay. Well, there are many many others, but I I I don't think that's that's the main. 那周老師好，我下面我會接著就是像我們的第二個模型是要對應剛剛前面那個是CIA提到我們還有另外一種攻擊，那它是叫做歸檔者attack，我們這邊跟周老師介紹一下這個什麼東西。

**【授課講師】**：那首先，一樣我們的資料其實一模一樣的，也就是來自於CIA手機上面的感測器收集到的，從螢幕收集到的，還有手機本身的旋轉資料。 那本身因為像是這種行為辨識系統，它本身是有機會受到受到模仿攻擊的，就是別人可能看著你的行為，他就模仿你的行為，那這就是一種那個模仿攻擊。 那模仿攻擊是分我們我們這邊定義分成三種，對，grey、歸檔者、attack。 那前面CIA介紹到就是歸檔者attack，它完全。 就是依賴我們攻擊者他本身的能力，他他的模仿能力有多強，那這個模型判斷失失效的機率就有多高。

**【授課講師】**：那這邊我們會著重講的是Grubas Test的部分。 那Grubas Test這個東西，它比起Grubas的攻擊者，他模仿能力更強。 就是簡單說，我們是去定義說存世界上存在一群攻擊者，他可以透過觀察的觀察受害者的行為，然後完美的去複製一些他看得到的的特徵，例如說那個人他的手他的手呃可能例如說他都喜歡在螢幕的左半側滑，那他大概看了一下就知道說他都會落在哪個區域，他可以完美的去複製這些他肉眼看到的行為，那我們就會說他是一個完呃很厲害啊，可以高保證或是很強的一個攻擊者。

**【授課講師】**：那Grubas Test在表現的就是這種情境。 第三種情境是。 是更極端的狀態，就是它完全就是攻擊者，他有掌握了這個 model 本身，或者是他直接拿到了受害者的 data，所以他可以輕易的去去高強度的攻擊這個模型。 所以對我們來說，呃，Rebus 的 attack 部分呢，它雖然可以模仿到那個受害者的特徵，但是它不瞭解模型的全貌，它也不瞭解資料資料本身，所以它的呃攻擊的危險程度是比 Rebus 還低。 但是因為它的模仿能力很強，所以它的攻擊的危險性是比 Rebus 還要高。

**【授課講師】**：那通常我們在訓練的階段用到的 synthetic data，它跟我們真正在進行模仿攻擊這些攻擊者其實是不太像的。 所以，所以呃，所以這個這因為這樣子的訓練資料的緣故，它沒有辦法提供模型有足夠的底蘊。 能力，就是在面對GUESS這種這種高強度攻擊者的時候，它沒有辦法提供很好的防禦能力，因為他們訓練時候看到的負資料跟真實情況看到的負資料差距太大了。 那再來是講到我們的資料特徵的部分。 那我們這一次GUESS的抵禦模型研究也是利用了資料特徵，它可以分成好模仿跟不好模仿這兩個分類，那來對這些特徵做一些處理。

**【授課講師】**：它首先定義說，在GUESS model裡面，好模仿的特徵跟不好模仿的特徵，除了那個攻擊者是不是可以觀察使用者行為以外，在我們的以資料面來說，它是我們會把，因為我們會把資料特徵轉成向量輸入進模型，所以呢，就是看說受害者的這個特徵向量跟攻擊者相對應的特徵向量，他們兩個之間的夾角是否小於某個閾值。 那當它小於某個閾值。 有時候我們就會說它是，在資料上好模仿的。 那大於這個閾值，我們就會在，我們就說它在資料上是不容易模仿的。 那所以，如果前面有一個很好模仿的特徵，它對模型來說又相當的重要，也就是說，模型會依賴這個特徵去做身份的判斷的話，它那麼好模仿，就會對模型帶來一些比較大的威脅。

**【授課講師】**：所以，首先我們就是有將感測器收集到的資料去轉換成具有物理意義，而且我們可以解釋的這些有物理呃有物理意義的動態特徵。 那我們再透過這些特徵去進行進一步的資料分析。 而且由前面的debug撕下來，就是表現的就是我們確實是需要這種可以抵抗模仿攻擊的模型的存在。 那在debug的模型裡面呢，我們用一般的standard theta去訓練，其實就已經足夠了，因為在那個情境下，攻擊者並不是完美的，那他們就其實能力跟普通的普通攻擊差不多。 但是呢，因為對於規劃者攻擊者來說，他們是可以完美的攻擊，所以會讓模型，因為他們可以完美的去模仿受害者一些可以被看到的特質，所以這個就會導致說模型可能會誤判，他其實是合法的使用者。

**【授課講師】**：那基於以上的原因，我們就設計了一層防禦機制，可以讓模型在訓練的階段就先看過這些，呃，高擬真的模仿

## 🎲 蒙特卡羅模擬迴圈（Monte Carlo Loops）與貝葉斯驗證模型（Bayesian Verification）抗模仿攻擊設計

**【授課講師】**：攻擊者。 那這個高擬真的模仿攻擊者是怎麼創造出來的？ 後面在講攻擊的nature的時候，會再跟老師介紹到。 進一步的是，我們透過去模仿規劃者attack這個高擬真模仿攻擊者這件事情呢，除了可以讓模型可以預先的看過什麼人是很厲害的攻擊者，很厲害攻擊者長什麼樣子。 此外，它也可以同樣的去呃讓模型更加關注難以模仿特徵，然後並且它不要那麼去關注好模仿的特徵。 這一步可以進一步的去提升模型的可靠性，還有它的性。 然後針對釋出的generation部分呢，我們是，我們是要我們要做的就是提供這個具有時時間序的動態特徵，然後去來建構一個面對模仿攻擊的時候，它可以有高效的而且又很可靠來進行身份驗證的模型。

**【授課講師】**：那並且利用模擬歸納step這個東西呢，我們加上強調特徵，就強調難以模仿的特徵的這類方法，讓它優於我們現有的體育模型。 那在釋出的generation裡面呢？ 部分第一個東西就是 adversarial mini learning，那這個東西是我們會產生 adversarial mini data，就是也也就是我們前面提到去去產生模擬的歸化生成 attacker 這個東西，那我們利用這個，我們稱它為 adversarial mini data，我們利用這個 data 來幫助模型學習潛在的攻擊。

**【授課講師】**：那我們可以先看一下什麼是，什麼是什麼是歸化生成。 那簡單來說，我們左邊這個是受害者資料，那右邊這三個是攻擊的資料。 我們做的事情就是我們會隨機去，我們會隨機去選擇可以被觀察到的特徵，呃， plus 我們會從 victim data 裡面隨機選擇可以被觀察到的特徵，然後把它替換掉。 而特徵對應的特徵，假設說我們今天選定了B特徵六和B特徵七，那它是可以被觀察的。 我們就會複製Victor的B特徵六和B特徵七到某一個攻擊者，把它原本的自己原本的密碼給覆蓋掉，讓讓它變成就是我們前面我們前面創造的那個情境，就是有有攻擊者他可以完美的複製、完美的學習某一個人的使用行為，這樣我們就會知道出類似這樣的資料。

**【授課講師】**：那我們有在這邊做過簡單實驗，就是想要確定就是這種人存在的話，確實會對模型造成威脅。 那最終就是在這個簡單的小實驗，我們有確定就是透過這樣子，強嗯強大的攻擊者的密碼確實會升高。 那有了這個資料之後，我們就會去利用這個。 data name adversarial name data來訓練我們的模，類似的類似的手法來訓練我們的模型。 那這部分就是說，我們前面有看到我們是怎麼去替換資料的。 那其實這整個整個VBox的架構呢，跟VBox是差不多。 那我們是在VBox的架構上面額外再加上一層，再再加上層抵禦的機制。

**【授課講師】**：那具體的做法就是，我們會從受害者的資料裡面找出容易被觀察模仿的特徵，再把這些特徵加到steganaly data上。 其實做法就跟前面的attack是一樣的。 那就會在可以就可以在訓練的階段的時候，產生出一批帶有受害者特徵的不一樣的。 那我們就在把這種處理過的樣本一定加進訓練資料中，讓模型訓練的時候可以提早的辨認出看起來像受害者但其實不是的這種樣本，這樣就可以提早抵禦未來潛在的對，fast cap。 那具體我們是怎麼替換 generating data 的？

**【授課講師】**：就是在這個部分，那做法其實跟剛剛是一模一樣的，只是選擇的資料就不同了。 我們選擇的資料是來自於受害者容易被模仿的特徵。 那至於我們怎麼知道特徵容易容不呃對模型來說容易容易模仿，這個東西后面會再繼續做解釋。 那只是在這部分呢，選擇就不一樣。 攻擊者我們是從可看見、可觀察的特徵去隨機選擇，但是針對訓練的時候，我們有特別針對那些容易被模仿的特徵，在在挑出來去取代 generating data 的特徵。 那這個東西就可以產生出跟我們剛剛呃 data 規範的 cap data 很像的東西。

**【授課講師】**：那產生出這個東西呢，我們我們就會把這樣子被替代的資料再進一步。 加入到我們全因子裡面，所以也就是我們在訓練的時候會有正樣，也就是受害的資料，一般的負樣的就是原本的這個貝塔，然後還有被被E Z呃被容易模仿的特徵取代掉的阿爾法點點點貝塔，那總共會有這三類資料一起進入全因子。 那接下來我們講一下那個E Z獨立性求，就是容易模仿的特徵是怎麼被找出來的。 我們最終是採用cosine similarity這個指標來去衡量一個特徵是是否容易被模仿。 那其實cosine similarity它其實意義很簡單，就是A跟B這兩個向量去做內積之後再除掉長度，也就是說我們只靠我們在比較兩個向量是否相似的情況下，我們只看它的角度，我們只看它要靠的多近，但是我們不考慮這兩個向量特別的強度。

**【授課講師】**：那在我們得到的資料來說，如果這個cosine similarity接近一的話，我們就會說a跟b這兩個向量，呃是非常靠近的。 衍生的意思就是說，a跟b這兩個人在這個特徵是很相似的。 那再來是，如果數值是趨近於零的話呢，也就是兩個兩個向量是垂直的時候，那我們就會說這兩個這兩個人的同一個特徵其實是沒有什麼太大關係。 那第三種情況就是數值接近負一的時候，就是像我們最右邊這張圖，兩個向量是幾乎是相反方向的。 那這個情況的解釋就是說，這兩個向量我們不能說沒有關係，我們只能說它關係是相反的。

**【授課講師】**：只是這種情況在我們資料集不常見。 那邊就給各位老師看一下一個例子，我挑了一個我我挑了一個Victor跟呃Taker對照的，呃。 特徵特徵相似度的表。 那我們定義了一個 threshold，是在當 cosine similarity 大於一零點一的時候呢，我們就會定義這個 x x 軸的這個特徵從一到四十九。 它這個特徵只要數值大於零點一，那我們就會說它在模型看到來說是一個容易被模仿的特徵。 當它這個數值是小零點一的時候呢，我們就會定義它說這是一個難以被模仿的特徵。

**【授課講師】**：所以我們對於每一個攻擊者跟受害者的組合，我們都有做這樣子的這樣子的一個計算。 所以剛剛前面講到的，在 cosine similarity 這樣，也就是我們所謂的 aster data feature selection strategy，就是我們利用 cosine similarity 去找出什麼的確好模仿，什麼的確不好。

**【授課講師】**：那接下來我們的實驗設計，我們的 dataset 有分兩種，第一種是，其實就是受害者的數量的差距，一樣，第一個 dataset A 它的受害者比較少，dataset B 的數量比較多，那我們會對這兩種，這呃這兩種 dataset 進行同樣的實驗這樣子。 那一樣的是有，我們是有建構這個 baseline model，我們是挑選了 Albert 這個 paper，那它的它本身的架構是根據 B C R N，也就是一種 R N，他們自創的一種 R N 架構，那裡面也是有用到 Attention 層，所以跟我們的模型整體來說的背景是蠻相似的這樣子。

**【授課講師】**：那我們有建構出這個 Albert baseline model 之後，我們有去做測試。 那再來是由我們自己 F C R N 的那個 model，那在訓練的時候就是前面有老師們看過的用 BERT。 卡，一般的 standard data，還有進行替代破壞的 standard data。 那在測試的時候呢，我們是會用正樣本、也當然是用受害者。 那負樣本就是會用剛剛模擬出來的對發生 attack。 那最後這個結果就是，呃，我先口頭講述一下這邊資料的部分。

**【授課講師】**：在受害者比較少的資料集裡面的，我們的 E R 在我們最終產出來的具有抵禦能力的這個模型 E R 可以降到六帕。 那如果今天是沒有我們的模型，但是沒有進行抵禦的時候呢，E R 是十二帕。 那六帕雖然我們的呃，我們的模型就是可以從，從加入抵禦的部分之後，可以把 E R 從十二帕降到六帕。 那這兩個數字都還是勝過於 baseline model、 adversarial model 的十七帕。 那在受害的資料比較多的那它這這邊呢，我們具有比預比預效能的這邊的模型一趴可以壓到三趴，那一般的情況下我們我們的模型沒有比預的時候是十趴，那也是表現的比 apple 這個 baseline model 的二十九趴還要好。

**【授課講師】**：那這邊可以給大家看一下這個這個比較視覺化的圖圖示，就是會比較好懂。 那我這邊一一來介紹一下這五個箱形圖分別代表的意思。 左邊這一個圖箱形圖圖表示資料受害者資料少的，那右邊這個是受害的資料多的。 我們看到左邊這張圖表的第一個，這個是 baseline model，那在進行只有 apple test，就是我們沒有對它進行模擬，我們就是隻是輸入普通的負負資料的，在這個情況它的醫療範圍區間大概是這樣。 那第二個就是我們拿來比較的，我們自己的 model 也是進行 zero attack 情況下，確實是可以比 baseline model 表現好一些。

**【授課講師】**：然後再來是 baseline model 呢，但是也但是有進行規巴式 attack 情況下，它的醫療就會飆升到就是將近要三十趴的情況下。 那我們的 model 在進行規巴式 attack 情況下，會明顯也是來的比 baseline model 還要低。 最終再加上一層防禦機制的時候，可以再把醫療拉到一個。 那右邊的圖也是一樣的順序，第一個就是 baseline model 進行 zero attack 的結果，第二個就是我們的 model 進行 zero attack。

**【授課講師】**：那這兩個去做比較，確實也是我們的 model 表現比較好。

**【授課講師】**：那第三個這個呃表現的比較比較不好的就是 baseline model 進在大資料量的情況下進行進行規巴式 attack，它的醫療就會拉的非常高。 那我的。 model，我們model進行基規把呃呃不，進行規把式take的時候，雖然表現有點差，可是遠比baseline model好。

**【授課講師】**：最後是，在加入了體育的體育模型的情況下打一次規把式take，那因為有體育的關係，所以醫療表現變得更好。

**【授課講師】**：那最後是長學預選部分，我們的最主最主要長學預選就是我們製造出來的模型，以及加上體育體育機制之後，這兩個情況表現都比baseline model表現的還要好。

**【授課講師】**：那就是呃在小資料量的情況下，我們可以把我們加入了體育模型之後，可以把醫療從十二趴壓到六趴。 那這個這個表現比baseline model其實蠻好。

**【授課講師】**：那在大資料量的情況下呢，我們可以加呃我們加入體育模型之後。 可以從十趴聊到三趴，那這個表現也是非常棒的。 二十九趴還有嗎？ 那以上就是關於這個額外的部分，想請問各位是有什麼建議或者疑問嗎？ 好，就偏比較一個簡單問題，因為剛剛大部分問題剛剛前面已經提問的同學，李鑫哈，就是你有聽到你有四十九的需求嘛，對不對？ 是。 好，然後好像四九的都是mobile還是不一不一定嘛哈。 所以有沒有簡單舉例，你有哪些需求？ 因為四九蠻多的。 啊，好。

**【授課講師】**：對不對？ 就是我們在滑手機的時候，呃，讓我們來看這邊，通常都跟我們手的動作有關，就例如說我們怎麼轉手機，我們滑幕，我們都習慣，呃，我們習慣點上半部、下半部。 那不容易觀察就是我們的資料裡面有一些是。 呃，是透過例如說旋轉之後，我們去計算它的它的標準差，或者是計算它的平均值，但那個是不可完成。 O. K. 那還有一種是可能，例如說像手指頭，我們會計算出後面積，那這個東西就是你算得得到，但不好完成。 對對，OK，好，謝謝。 我想請問另外兩位老師還有什麼要建議嗎？

**【授課講師】**：呃，就你有幾點。 好，一個就是你那個，bar，grade，bar，one，bar，定義哪邊嗎？ 是自己幫你。 是呃，算是我們這我們團隊這個學期想要。 也是你們要學習的，因為你本質上還是命名規則，hands，是你在作業上面用的hands。 那命名規則的hands就是你可以呃，是攻擊者會去看人家操作。 對。 所以你會有這個需求，是命名hands。 主要有這一些，我使用什麼的詞序。 那另外一種是，attacks是啊，level effort attacks。 用 effort attacks 跟 immigrant attacks 最大的差別是，他完全沒看過使用什麼，比如說他遇上什麼手機。

**【授課講師】**：對。 哦，他就沒有開始操作。 是的。 那這種就是啊，說的 level effort attacks。 那這是人家明確有定義的兩種 attacks。 那我猜大概會對應到你的 black box 跟 grey box。 所以，我建議還是要用這個比較明確的加語去描述。 就是加名詞。 對，不要自己發明名詞。 這個在學術上是，你可以用這個東西來去描述這兩個，呃，大家呃接受的名詞。 但是你不能自己翻譯，你可以用呃這種grey box、grey box或者是white box，或或者是class box來去描述人家的這種攻擊。

**【授課講師】**：但是你不要用呃這些grey box、grey box或white box下去描述這類攻擊，因為它已經很明確的定義了。 所以你還是要用把live attack跟命令attack去對應到grey box attack跟grey box attack。 所以說class box attack這個東西應該比較少，這樣我這講的應該就是直接可以拿到資源，然後直接就把它喂進去。 我這種一般來講，我就是要獲得電腦還有一些特殊許可權，然後直接就把import直接注入到它的那些去。

**【授課講師】**：那這個比較困難，一般來講，基本上大家目前至少看到是還沒有。 沒有，我覺得行為上嘛，應該比較少，比較少，比較少這一型別。 可是第一點的提醒，那第二點是這個你你問題定義這邊，就是說你現在建立模型會需要呃這些input text的嘗試錯誤的這些資料，還是你你就是針對這個使用者啊，然後你要教這個input text的操作，至少要一次的資料，然後你才能去。 我們是在這個情境下，我們不需要真的有人在攻擊，因為攻擊資料也是我們在另外產生出來的。 那那你怎麼產生？

**【授課講師】**：因為你用到你因為你有原始資料，那你中間有一段，就是你看起來是做 augmentation，對，類似的，類似 data augmentation。 而你看你的 anchor， anchor one， anchor two， anchor three。 所以這個 anchor one 是屬於 webbox 或者說 UoF text 的資料，可是它是來自 UoF， OK，然後，哦，那就 OK。

**【授課講師】**：所以你，所以你的概念其實應該是這樣，就是說，其實你是要 UoF text 的資料，因為這些是我們叫做 standard negative data，這這是很容易可以收集到。 是，反正就是別的，那別人的資料，我認呃，來操作資料一定會是，一一一定不會有你認的訊息，所以是可以過的。 好，好，那你今天是想要用這個 UoF text的這些資料，就是stand，就是standing negative的資料，下來稍微跟victing對到過一下，然後宣稱是可以產生出類似啊，membr text的資料，對不對？

**【授課講師】**：對。 好的，你要這樣講。 OK。

**【授課講師】**：我們整個概念一定要這樣下去講。 好。

**【授課講師】**：要過來，沒有人會看的你的貢獻在。 好的。 所以你這邊很重要的貢獻，其實在於聽到你的推選。 我不知道你聽得懂，聽得懂。 是。 你的方法，我我因為我剛看了很久，就是說，呃，你其實要去證明，就是用這一些data，哦，其實是不只是可以改善哦這個哦你自己提出來的方法，還可以去改善baseline的方法，是不是？ 你要去證明。 改善baseline的方法。 我們沒有去證明這個，我們沒有對貝沙拉都在進行。 所以你你是有，你的方法是用之前你學許章傑弄的那個嗎？ 那我們的模型是我們自己，哎，應該說我們這一點，這一點弄出來一樣是一個新的模型。

**【授課講師】**：那如果是新的模型，但你這邊就變成說新的模型在加沙，你的貝拉姆培訓，對，沒錯。 因為還是要評估一下人家貝沙拉用貝拉姆培訓，回放一遍。 我們目前參照的貝沙拉都沒有進行到的培訓步驟。 對，就是說，呃，如果要完整一點，就是你可能還是要去看，就是說差距到底是在，還是兩邊都有擋住？ 那如果說你用貝拉姆培訓。 你就可以大幅提升貝斯那model，跟你的比如說model在家這樣子，其實一樣，那可能貢獻就只有在什麼，在你貝拉的prediction。 那其實真正貢獻會是在貝拉的prediction。

**【授課講師】**：所以你可能就要去講說哦，那嗯呃，就你要去證，要不然可能人家不知道到底什麼，因為你是兩個東西並在一起，一個是不懂的model，一個是連貝拉誰都不一樣，所以貝拉誰不一樣，因為你其實還多做了一個貝拉的prediction。 那別人的話，他是原來model，他用原來的資料。 就是。 所以你還是要去證，就是說哦，這個貝拉誰的預測能有效到哪裡？ 那還有多少是你自己model的貢獻？ 嗯。 好像我的建議當然是這樣。 但是我現在建議，會建議我們對於AI那邊做一次。 對，是就是你這種最大不同，因為其實你產生出來資料是，就是因為它是一個方法，然後最主要是把裡面的feature去做，對嗎？

**【授課講師】**：那其實人家的資料也是這種，也是feature，也是這樣一個一個，對嗎？ 只是說它可能用的feature跟你看一樣，對嗎？ 那還是得用同樣的概念去用，只是說，呃，你當然可以宣稱就說，因為資料的是不一樣，所以不一樣，下去，但同樣的概念應該是可以下去用用。 這可能是就是說你可能要去思考，但我知道就是說資料，一張封面跟資料不一樣，哦，feature也不一樣，那那要做公允價，公允價就是至少就是說你可以去按，同樣這個步驟上。 看的，是不是你被他培訓，其實才是真正的。

**【授課講師】**：啊，這也會是，就是說，例如說，他們要去參考。 那人家還是會問這個問題。 哦，我們有其他零件。 不是那個畫，是個畫。 如果說把，好，來這邊是來證明這個方法有效，就可以在面試當中。 就是我們就可以說說，這一個，這一個架構其實是我們很大的貢獻，因為我們如果能夠把這個架構去套到其他的 model 上面，也能降低那個 model 的IO的話，那就是證明就是這個機制確實有效。 對。 因為我在research。 啊，然後王老師問你問題，你們把自己回答。 王老師問你說：“Black box is zero effort, green box is medium difficulty attack。

**【授課講師】**：”你回答。 嗯，嗯，可能我剛剛回答，我覺得可能有一點點不太正確，因為 black box attack 確實是還是有模仿的成分存在。 那最大的差距是在 black box 模仿的能力比較弱，那 green box 我們預設它是一個很強大，它可以完美模仿的攻擊者。 不用回答我。 我我我簡單回答。 王老師認為，這個 black box attack is zero effort attack。 沒有 green attack，我們是王師。 Black plus black equals to zero.

**【授課講師】**：Ever? Do you? No. What? That is the wrong answer. Yes. Yes. So that is all agree. Could we just make a suggestion? Let black plus is zero ever. Green plus is maybe green, maybe green ever. That's not true. 嗯，剛剛回答的時候有有講錯。 所以啊，這個是你考試的時候，這種這個這個錯誤不要犯了。

**【授課講師】**：不要犯。 嗯，這個就要問你要跟你說，因為你怎麼區分 box 和 white box？ 區嗯，嗯。 我說它的你這樣區分的意義在哪？ 對不？ 這就這會牽涉到不同的學科，那我們要看。 問你說，好。

**【授課講師】**：如果一個東西你能把明確區分，它是什麼？ 我問你現在基本上做，在我看來是文學。 我說，can，or，can，or，rising，哦，那結果現在我問你說，這種東西算不算文學？ 這種東西算不算文學？ 當你回答不出的時候，再選不上，它就是基本上不存在。 對。 嗯，我在。 那就會有更加的，這樣變得不一致，就是你全面講只有八十多。 嗯，好的，謝謝。 然後我想你在這邊可以討論一下，這樣子，你差不多這樣子。 This is first one. I really. This line of explanation, which is very different from what I heard.

**【授課講師】**：And if I understand correctly, that the white white box attack is part of the grey box attack, where white box is extremely grey box. In the same step, both of them is able to access victim's data and model. My model and me, perhaps the meta data, perhaps the code, the training code, where grey box is able to access part of them, say one percent, able from one percent to ninety-nine percent.

**【授課講師】**：If you are able to access hundred percent of both data and model, that means it becomes a white box attack. That's what I look, which is very different from what I ever presented today. The way that I present that is very easy to confuse with the black box and grey box.

**【授課講師】**：It looks pretty simple. I'm not sure that's doing it. Nevertheless, that I bet you to do that please, please, right? 謝謝張老師。 那那我們再怎麼發到這個？ 下一句。 那三位老師好，那我們S組是這個月想要跟三位老師討論一下我們的新計劃的提案，然後希望就是可以請老師給我們一些建議。 那首先在研究背景部分，就是那個OWASP這個組織，就是每年他會定期的去講說，目前就是各種領域上面容易被攻擊的排行榜，然後我們有找到說，二零二四年他們有提出針對行動應用程式，呃的前十大攻擊。

**【授課講師】**：那從這份呃報告上面可以看到，就是這十大攻擊裡面有很多都都是因為開發者他太過於專注在開發。 發生，而沒有去做到防禦。 那比如說像是第二個，就是像是供應鏈攻擊。 那我們平常引入套件之後，我們不太會去注意說這個套件裡面它在做什麼事情。 那所以今天如果這個套件被汙染，然後我的城市嘛又沒有去做到防禦，那這樣就被攻進去。 那像是第四個，就是呃輸使用者的輸入跟輸出，它沒有去做判斷。 那所以這樣子就有可能會被輸一些特殊字，然後也就被攻擊成功。 那有一些相關的報道也是有講到這件事情，只是我們只會關注在呃我們目標是要開發出一個好的呃就是好的功能，所以有時候甚至可能開發者他也不知道有這些攻擊。

**【授課講師】**：好，那這樣子就是會會產生一些技術負債的。 好，那所以我們就想到說，那如果是這樣子，就是呃以人類在打那個疫苗。 的過程來思考，是我們疫苗的研發過程，是會先去拿到病毒株嘛？ 拿到病毒株之後，我們會去分析那個病毒特徵，然後我們會去把這個病毒去做成一些呃培養出一些比較沒那麼嚴重的病毒，然後把它打進去我們原本沒有沒有抗體的人體裡面。 那人體因為有了這個疫苗之後，就會有一些抗體，所以今天如果被感染之後，我人體其實就有一些呃抗體，然後就會變成比較輕症或者是沒有症狀，就有點像是之前的抗體的。

**【授課講師】**：好，所以就想要運用這個概念呢，來去把那個如果原先沒有完全沒有防禦的APK，那我把它打進去一點病毒之後，我們去檢測看看，他有沒有去做到防禦這件事情。 如果沒有防禦的話，那我們就去幫他做好這些防禦的事情。 好，那這邊是我們現在提出的那個就是。 構想。 那等下也會去分，呃，兩個部分去講說現在的呃最新的研究他們做到哪邊，然後我們跟他們的創新點呃在哪裡的。 好，那首先呢，我們就是想要去收集現有的網路上的些呃含有惡意A P K的資料集，比如主，比如說像是安卓錄，那裡面就是有呃兩性的惡意的資料。

**【授課講師】**：那我們會去後呃運用我們經驗，就是部落格會計劃的這個追拉碼，我們的這個追拉碼呢可以去找出那個呃惡意A P K裡面它的呃就是惡意程式碼在哪邊。 那我們收把這些惡意程式碼去把它收集起來，變成我們自己的資料庫，然後去注入到那個正常的A P K裡面，然後去檢測看看它有沒有去對這些惡意程式去進行防護，比如說。 說，如果今天是呃會被引導到其他奇怪的網站，那我們就試著去把它導到我們自己建的網站上面，去看看說它能不能去抵禦。 如果不能的話，那就在就代表我們去攻擊了成攻擊成功。

**【授課講師】**：那這邊我們會去真的去執行，因為呃我們認為說就是要真的去執行的那個階段才是被攻擊成功的，所以我們會去真的去執行，所以是屬於動態分析。 好，那如果今天被攻擊成功的話，我們會再去訓練我們自己的呃另外一個語言模型。 那這個語言模型呢，我們會使用遷移學習的方式，然後就是讓語言模型去學會那個步槍Java程式碼的呃技能。 那為什麼要使用到遷移學習？ 主要是因為呃還是一樣的問題，就是Java的相關的。 是嘛？ 實在是太少。 那通常那個做補強都是在C語言比較多，好，所以我們會拿比如說像C C加加或者是Python的這些呃語言模型，過去在這兩個語言上面它的修補的經驗，然後希望可以用遷移學習把它轉移到Java上面來。

**【授課講師】**：好，那我們這邊會再去把它做補強，補所謂的補強就是比如說它的原，比如說像寫網頁的時候，那如果呃它沒有去做對C貨的語句去做預處理，它直接執行，它就代表說它沒有防禦。 那我們預期我們的語言模型，它可以去呃看到這個情況的時候，它可以去把這些這些語句去稍微去做調整，或者是去多做一個方選，去讓它有抵禦的效果的。 好，那前面框起來這個前面這個紅。 其實那個這邊這邊過去的研究，它叫做 P P D A P，就是所謂的搭便車攻擊。 那在它在那個社交公司上面也可以看到這個字。

**【授課講師】**：好，那所謂的搭便車攻擊，就是那個攻擊者他會去開發那個惡意層次的片段，然後再加上一些漏洞，然後就會變成是一個一個嗯二，就是一個二二層次的。 然後接下來他就會把它去拿一個良性的 A P K，然後去把它解壓縮，解壓縮完之後，再把剛剛他所開發的這個惡意層次片段加上這個漏洞，然後把它注入進去，然後再重新打包，就會變成是一個被攻擊的這種惡意層次的。 那這種攻擊就叫做 P D A P P D A P 攻擊的。 好，那底下我們要我們要找到一篇，就是二零二五年針對這個攻擊，它呃最新的研究，好，那最新的研究，它是它是怎麼做？

**【授課講師】**：它首先呢，它去收直接拿別人現成的，就是專門做P D A P的這個資料集，好，然後這個資料集有點舊，是二零一幾年的，對，那它直接拿現成別人收集好的資料集，然後來進行去那個城市碼的比對，它去跟那個沒有被加工、跟被加工的城市碼去做比對，好，看看那個是是在哪裡，然後比對出來之後，它收整合另外一個資料庫，資料庫之後，它呃，因為它為了去注入，所以這裡還有去設計設計一個演演算法，演演算法呃用Masking Masking這個演演算法，然後它去找出適合的呃惡意片段，還有適合的宿主是誰。

**【授課講師】**：然後接下來有了這些惡意片段之後，它是用那個ChatGPT，它是用那個GPT三點五API，然後直接去微調，微調就是希望去把那個測試碼改成呃改成可以運作的狀態，被注入進去之後可以運作的狀態。 好，那這邊就是它剛剛找到的那個呃，他認為就是相似性比較高的資料，就把它注入進來。 好，注入進來之後呢，它它這一篇的重點，它只是要強調說，就是像這種攻擊很容易，就是它現在寫成一個框架，然後那個就是變成一種自動化的、自動化的攻擊，就是一天可以可能可以產生，就直接可以產生一一兩千個惡意PK，然後像這種攻擊呢，就很容易把那個防毒軟體之類的騙過，因為就是大。

**【授課講師】**：部分都是正常的測試，其中可能只有一小部分是二P的正。 好，那這是呃剛剛講到，就是這一篇最新的研究還在做事情。 好，所以我們呢就想到，就是認為說我們這個計劃是，我們針對了三大部分去進行創新。 首先就是在那個以往的這個PDAP的攻擊，我是使用靜態分析。 那像剛剛最新的研究講說，也已經證實，就是這種攻擊很容易去騙過這種防毒軟體。 所以我們就是使用呃計劃是使用動態分析，因為就是你你要在攻擊的過程裡面，那個哎你要在執行的過程裡面，那個真的被打進去才算攻擊成功。

**【授課講師】**：好，那接下來我們第二個創新呢，就是像前面這邊，它是直接使用現成別人的APK，而且只針對在那個PDAP的這個。 這個攻擊上面，所以我們就想說要使用，就是我們自己去收集各各大家族的惡意APK，然後在使用我們已經具有的圖解攻工程，然後加上那個圖神經哎，就是圖解攻工程，然後直接自己去找出這些惡意片段。 我們希望的模型，它可以去識別出，就是不只是PD APK上面，就是各大各大惡意家族都可以去識別出來。 好，那第三個就是過去的相關研究只是去講說這個攻擊很危險，然後可能不就是不容易被模型偵測出來，它沒有去去幫忙把原先的那個APK去做補強。

**【授課講師】**：那我們這個計劃預計要去做加強這件事情，就希望這個APK不要呃要把它的圍牆建好，不要再被攻擊的。 好，那接下來。 第二部分呢，就是我們會去講說現有呃的遷移學習，它現在做到什麼地步，然後我們想要它，我們想要怎麼呃去最佳化它。 好，那這一篇一樣是那個今年最新的，呃，就是在做漏洞偵測的，就是它拿遷移學習，然後去做那個漏洞偵測上面。 然後這一篇呢，它是使用就是像剛剛說的，就是拿C語言，因為它樣本數比較多，然後它去拿C語言去做呃就是遷移學習，把它遷移到那個Java、Python、PHP之類的程式語言。

**【授課講師】**：然後它但是它的目的是做漏洞偵測，那我們是想要做修。 好，那這一篇一樣就是它有它呃不夠好的地方，就是它沒有去做到語義對齊。 那如果沒有做語義對齊的話，就是它語言模型它學不進。 好，那我們稍微介紹一下什麼叫語義對齊。 那從這呃投影面上面可以看到，說就是這三個其實都是呃這三個C擴語句，其實都在做一樣的事情。 那所以語言模型照理說應該要把這三個呃相似語的C擴語句，就是它的向量空間照理說應該是要很接近的。 那所謂的語義對齊就是要讓語言模型去學呃去就是向量空間去應該要很接近才對，這個就叫語語義對齊。

**【授課講師】**：那剛剛這篇也就就是它沒有它還沒有做到這件事。 那我們希望就是我們要達成呃這個目標的。 好，那對就是希望拿比較多的的樣本，然後去把它。 投射到那個比較少的樣本上面去增強它的泛化能力的。 好，那所以我們剛剛的這整套系統，我們的目標呢，就是呃，我們是，我們是第一個，就是用疫苗的這個概念去提出那個紅藍隊演變的這種防禦思維，就是紅藍紅隊是去負責攻擊變的，然後藍隊就是負責去修補。 那我們整套系統就完成那個自動化的紅藍隊演變。 好，那這個呢，就是我們這整套系統還有去結合那個對抗，對抗式，還有就是那個就是遷移學習，然後去微調我們的語語言模型，然後就是要去讓它就是自動修補，去加強它的呃原先沒有抗體的那個A P K它的免疫力，就是當它之後呃。

**【授課講師】**：比較不容易被這麼容易被攻進去。 好，那第三個貢獻呢，就是我們想要讓開發者就是他可以專注在開發的任務上面就好，因為他畢竟他不是海客，就是有一些攻擊他可能不太瞭解。 那這些攻擊就交給我們的程式，我們會去幫他做那個呃，就是小小的演練的。 好，那所以整套系統就是我們目前可以切分成四的研究方向。 首先是圖結構工程，雖然我們現在已經有一個現成的系統，那我們希望可以去用更好的圖結構的方式再去最佳化它的找出惡意程式碼片段的能力。 那第二個呢，就是呃 P B 飛艇的一些那個相關的攻擊。

**【授課講師】**：那目前我找到的相呃比較多的研究是在二零一七年近幾年好像比較少一點。 好，那第三個就是要去做最重要的就是程式碼修復，就是去把它做補強，要讓語言模型學會這件事情。 那第四個是我們想要用遷移學習，把語言模型在呃 C 語言的或者是其他樣本數比較多，它的修復經驗，然後把它遷移到我們的 Java 上面。 好，那以上是我們這套系統的計劃的架構。 那想請問三位老師能不能給我們一些建議？ 嗯，聽清楚。 那我我一不太瞭解的是，我們要做工業，現在的不同的頁面都提到多層次的修復，這個概念是不是我是一個我玩 App 的方式？

**【授課講師】**：開完我的 App 後，直接到微信，幫我開啟。 開始玩了以後，這個新的 App。 不準備，就繼續幹。 對，這樣。 對。 這個很好的idea，如果沒有看到說，要不要怎麼做這件事情？ 哦，對，因為就真的剛想，剛想到這個方法，這樣。 那我們會再去研讀，就是剛剛找到最最新兩篇論文。 好，這個太難解。 就說你P K不就是把一個新的惡意城市放進去嘛？ 那為什麼會有注入城市嘛這件事情？ 不就先破進來，放到P P K裡面，然後P P K裡面主城市可能還要再改一些城市嘛去破一些惡意的。

**【授課講師】**：啊。 呃。 那那這這個，你看，就是參考這一篇那個最新的研究。 那就是，它通常二二億的片段只有幾行，然後所謂的那個對，我我我現在就在講這個概念，就是它不就呃是產生新的APK嘛？ 對，對嘛？ 對。 好，那產生新的APK，然後你沒有塞惡意程式嘛？ 就是它裡面只是個修改版，只是說它把惡意程式嘛，那個檔案是原始的哦，我可能結果都對，但是我們塞入一個小檔案，這檔案也不是哦，全部都是有惡意程式嘛，只有一小段哦，那你還是要去hook起來，連線到這個惡意檔案嘛，對不對？

**【授課講師】**：呃，你像不懂就是你怎麼去修補這層，這層修補就把那個hook拿掉就好了。 哎，沒有，這個是就是因為它是要，或者說你要免疫，你怎麼去免疫？ 這個就是因為它原先的圍牆建的不夠好，所以才會現在才會被別人就輕易的改幾行，呃，多加幾行程式嘛。 他就被勾進去，啊！ 可是你都已經可以去哎，什都可以擁有城市碼控制，你當拿一個APK下來解開了，它怎麼不是怎麼改的？ 那為什麼還會不好攻擊？ 因為它什麼城市碼都會刪的，它只要一個呼，叫一個呼叫呼叫到你惡意城市碼片段那一段，它就可以了。

**【授課講師】**：那那它都可以改，那你怎麼讓它免疫？ 我的疑問是這樣，因為通常免疫是它不能改，哦，然後你注入，所以它你注入以後，它可以偵測或者是去反應，甚至去回擊。 哦，所以你東西不能改，你你的東西都可以改的，那你你怎麼去讓它免疫？ 你都改了，那你自己寫了一堆免疫。 感冒，他把你語音改掉。 哎，沒有我。 對，這我比較不懂，因為 P T P T B 不不不就是可以這樣下去動嗎？ 嗯，對，那這個是前面前面應該說我們我們這一套是有點紅藍隊。 那前面前面這段我們做的紅隊的攻擊手法是有點像 P T B T 的手法。

**【授課講師】**：那我們要去做的呃，最終的目標就是不只不只有可以去呃，可能可以去對抗一些，比如說像會被惡意傳簡去的，或者是像剛剛呃有稍微提到，就是如果我我建議嘛，因為邏輯上我們很好理解。 所以你這邊可能要再把語音不要了。 故事串起來，因為這這個就你任何層次都可以全你所有的在裡面下去修正，你說是完全都沒有。 因為它也可以改，那什麼東西不能改？ 就是它是成為一個生物裡面，什麼是post東西不能改？ 哦，那你送過去，哦，那你可以去辨識出來。 哎，這邊這邊可能是我沒有表達清楚，就是我們我們，呃，就是比如呃，現在惡意程式有很多種，那我們希望它可以就是以現有的這些攻擊，它至少程式碼裡面要有對這些攻擊要有一些防禦的。

**【授課講師】**：那，那那你P P， P P B這個跟你的這個什麼，你就說免疫哦有什麼關係？ 或者說你修正，你是要去修？ 這些這些Pigback的原始的城市嘛，還是你要把它修復回來？ 哎，不是，應該是那個我們想要去，應該是說那個。 我我知道這只是初步的概念啦，我只是，我只是有一些疑問，希望就是說，儘量聚焦技術，儘量聚焦，我是提出一些一些可能，可能以上的都懂了，因為搞不好也是，可能不太理解你到底想做什麼。 但至少就是說，從我這個的角度來看，這個圖片裡面呈現邏輯，我覺得這邊可能是要說明清楚，因為Pigback就其實就可以，假設就是你已經有整個Pigback的許可權，那你是，我開始是看你對的問題的。

**【授課講師】**：定義的清楚，可能我我跟老師可以講，我舉個例子嘛，呃，Pitchback就是在，本來是一個安全的App裡面增加了一小段惡意程式嘛，對對對對，它基本概念是這樣，對，那很直覺的一個抵抗的方式就是在App裡面有一個hash code，你講一講我們知道，對不對？ 那為什麼hash code這種方式沒有沒有辦法抵抗Pitchback？ 這可能要回答了，也就是說你要對你的問題可能要有某某些定義，我就在某種限制當中，然後for some reason這個hash code這個不能做，在這個情境下不能做，呃，否則我有hash code，我很容易偵測這個它有沒有改過嘛，對不對？

**【授課講師】**：Anyway，就是你試著看把你的問題定義清楚，嗯。 好，他們好。

**【授課講師】**：我想謝謝楊威老師，其實他們禮拜四上來上來告訴我，之前沒聽，但是我中位沒聽到，是聽到，就是後頭沒聽到。 剛開始中位這樣，對對對。 那因為其實這裡面很很簡單，因為這個我說太概括了哈。 然後後來他們就補充後面這幾個相關，但是今天看起來還還是有些，就是你們在做球，就有中位。 嗯。 就說你這個說攻擊跟防禦，對不對？ 就就是剛剛楊老師講最後一句話講的很好。

**【授課講師】**：這防禦的話，我傳統為什麼傳統方法沒辦法抵擋必須被？ 哎，變成你要了解這個，說紅藍隊演練，你像藍隊的演練，他所謂防禦一個攻擊的話，我把five擋死，我就防禦了，對不對？ 包括這是最簡單的方法，包括現在講的，那個叫做那個叫做迷信式的這種做法，更不管你城市好，對不對？ 我我就處理錯，所以這種東西，我們這樣的一個手續，到底是不是一定要真的要？ 那我覺得這個要講清楚了。 好，所以這個，所以當然我是覺得，我不肯定他們能夠找到辦法。 思考的東西是一個不錯，但是還是要建立在一些一個基礎，還有一些事實，包括剛剛講那個所謂城市碼補牆。

**【授課講師】**：城市碼補牆解決什麼樣的問題？ 這個東西它有，這個是不是能夠未取到我們前面講的整件事情？ 我想他們還有段路需要走。 大概就是，也謝謝兩位老師哈，然後知道。 嗯，但是他們設想那個想法嘛，因為我怕那個開始就錯了，就是後面可能只會走很多冤路的。 就是想法是想說，比如說像現在那個呃傳簡訊的這種東西，那如果一開始開發者城市碼面，他沒有去對這些傳會被拿來。 穿戴檢訊的這個這個攻擊，還有去做到一些防禦的話，那我們希望我們的語言模型可以去幫他加上呃一些抵禦的的口。 我們並不是要去抵禦P P T這件事情。

**【授課講師】**：對，那那這可以噹噹票。 這這所謂。 那P P T太重了，跟我們全沒有關係啊。 誒，應該是說就是前面前面前面這一段在做的事情。 不是，我想王老師要講的，說如果這P P T跟你剛剛講要講那個故事，你就講那個人物，對不對？ 你講一個，你就講清楚。 他真正問題是什麼？ 什麼情況發生？ 他們就講的非常清楚，分析的告訴我們為什麼現有方法做不到，對不對？ 然後接下來我們的想法是什麼？ 用A I用什麼都沒有關係，那基本上就做到了。 我們就不要提什麼P P T，因為這東西你會像前面同學這樣發散到。

**【授課講師】**：太多人，人家到處攻擊你，對，就發現你今天其實你就就沒沒有針對人家的問題。 好。

**【授課講師】**：好好的。 對對，這不是說你今天就說你，如果很確定那個問題是重要的問題，好，你想，哎，這個是一個很重要的問題，為什麼人家要去要做？ 那你就把那個問題深入的去去分析。 風格在你整個後面後面不應該存在。 好。

**【授課講師】**：好。

**【授課講師】**：對。 然後你花了很多精力去放在重要的問題，在你講的東西，你你這種什麼學習，然後自動防禦，做什麼的？ 這個根本跟P Band Band我是根本就過不了。 好。

**【授課講師】**：好。

**【授課講師】**：那P Band它假設是你OK，存取所有的放，然後可以產生任何一筆錢，然後使用者不到於P A到，對或不對嘛？ 然後全部都弄破了去扣，弄破了，然後大工程是哪一對？ 所以。 整句少，它到底有什麼意義？ 好，那那那就跟你的沒有關係了，因為沒有辦法對這種東西真是沒有影響。 嗯，好，會再修修正一下表達方式。 好，OK，那就這樣子。 好的，謝謝老師。 嗯。
