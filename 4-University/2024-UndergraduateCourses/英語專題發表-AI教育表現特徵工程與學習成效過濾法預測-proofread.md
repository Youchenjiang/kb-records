---
title: "英語專題發表：人工智慧教育表現預測、特徵工程與低成本過濾法模型"
event: "大學部人工智慧專題全英文發表會"
date: "2026-03-18"
talk_id: "AI-EDU-ENGLISH-PRESENTATION"
speakers: ["授課講師", "學員", "Youchen"]
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "classroom-lecture"
---

# 🎙️ AI-EDU-ENGLISH-PRESENTATION 英語專題發表：人工智慧教育表現預測、特徵工程與低成本過濾法模型 (授課講師 / 學員 / Youchen)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動問答，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語與標點符號，明確標註發言角色（授課講師／學員），並依授課脈絡劃分流暢之主題章節。

---

## 🎯 Introduction & Paradigm Shift: AI in Education Performance and Research Background

**【授課講師】**：好，接下來請專案小組進行全英文期末專題發表，題目為 Feature Selection and Review with AI in Education Performance，請開始發表。

**【學員】**：Hello everyone, we are 400th day request, and our topic is future lesson review with AI education performance. Today we will interview our neighbor in two six parts, and I will go into the introduction first. First, we should take care of education paradigm shift. What is paradigm shift? It's meant about the fast to fast to AI education.

**【學員】**：It's mean the learning, uh, learning habit shift, and there are three main steps. The first one is teacher lead, that mean the teacher teach the students fast to fast, and the the second one is system dominated, that mean we use ecast or some, uh, some courses online for learning, and the the nowadays we are standing inStudent-led, it means the student can choose what he or her want to learn about that, and this is this about education very paradigm shift.

**【學員】**：And why is is so important? It's about that we have three one dimension. The first one is that new features show up because of AI assistant. The learning features started, such as AI-generated content. Presently, it's made that how many words or how much we use AI to do that. The second one is AI lack of interpretability, means the models is like the black box, and it's not and and is, uh, it doesn't have enough interpretability for education.

**【學員】**：So it's the second dimension.The last one is the knowing. Knowing is that the AI use a negative impact students' academic performance, and it encourages to point out which features is much more important in nowadays student late learning with AI. And this is our three question, and our contribution is that two, this two below.

**【學員】**：The first one is that compare three method, uh, three traditional feature selection method on AI learning, and the second one is for we can we find out that positive correlate with correlate correlate with students' test features. And our research question there is there are four. The firstOne is that we will, uh, under unconstrained features of conditions, and we make three based features selection methods in most of the surveys via performance.

**【學員】**：And the second one is that, uh, we want to know when the features selection choose the best future state, and we divide one features in the state. What's the impact for each one features selection method? And the, uh, Q three, research question is about that, uh, what kinds of conditions oUTP（無遮蔽雙絞線 (Twisted Pair)）ut features for each one features selection?

**【學員】**：And the last research question is about that.Features. How can we predict powerful features on these two our methods? And let's go into another method. The relevant one can find now the feature learning for review lines. And our main feature selection methods are filter wrapper and blending. And the filter is about we are training models.

**【學員】**：After we choose filter features, after we choose features, we train models. It separates. And the second one is a wrapper. Wrapper means that we use the test wire just like we use models to to estimate the the featureThe features effects for the features goal to make the wrapper get the higher get the higher get the higher features.

**【學員】**：The second, the last one is the embedded. It means that we select features and the train features, train models together, just in the classifier training. After training the models, we get the features. Okay, and the features learning, uh, this two, this two hybrid and the ensemble is the up higher, is is top higher than the traditional three main feature selection methods.

**【學員】**：Just like hybrid is like combine filter wrapper or embedded. Just like we combine the traditional methods together, and it means the hybridAnd the ensemble, ensemble, ensemble is that we can choose a lot of filter, wrapper or embedding, and we can measure lots, uh, measure lots, their oUTP（無遮蔽雙絞線 (Twisted Pair)）ut and aggregation their oUTP（無遮蔽雙絞線 (Twisted Pair)）ut, and we can get much more clearly feature result.

**【學員】**：Okay, and the last one we will go into the feature, feature information. It's about the state, uh, it's about the scores for feature each features correlation with the target, and we will go into explain this algorithms for interview for a little. And the last one we will interview, and we will talk about the wrappers, RF, E, CWe estimate that, uh, just like RFECV, just like we choose the all features, and we will delete one features for a loop.

**【學員】**：Just like, uh, we choose all the features for training a model, and the model just, uh, the accuracy is lower if we delete, uh, one of the features and is about the RFECV. And the second means we can cross fold, uh, we can cross fold the features. Finish. Okay, I will t

## 📊 Multi-Label Feature Engineering: One-Hot Encoding for AI Tool Usage and Filter Selection

**【學員】**：ell you later. Okay. And the last one we just told about embedded DT. DT is means the decision tree. Why we use DT in our experiment? It means a lot. Uh, a lot of, a lot of other experiments just use the.This division trees just like the features on the right. So we choose the DT for our experiment. And next way, we will talk about the evaluation matrix.

**【學員】**：Uh, on this, on our paper, we use record and important features to match to measure our features get a higher impact for our training models. And let's talk about our experiment. And next one, we will take the uh take go to the researchers or team. Okay. Why? Hey, I'm not. Yeah, I'm not. Take camera. That is my turn to introduce our experimental methodology.

**【學員】**：And this starts our overall performance started with the data processes and andSet up the experimental configurations. Next, we run the four experiments, including a baseline experiment, spontaneous, to evaluate a evaluate the model. We use six metrics such such as recall and Jacks similarity. Finally, all results are saved in a JSON file for for future analysis.

**【學員】**：哇耶！Okay, let's start by detailing the data preprocessing steps. Our data set containing a eight thousand records and twenty six columns. And the first step was to handle missing values. After our check, we found no missing values in this data set. However, in the AI for use and AI use edge purpose columns withsome values labels now.

**【學員】**：We decide to keep these non-value because they still carry valuable information. Next, we decide the paths can't cover target labels to prevent other columns from during the model judgment starts, such as introducing noise or causing the model to rely solely on specific values. We decide to drop the student ID, performance, gender, grade, and final score columns.

**【學員】**：Okay, and finally, we process the specific encoding for grade level and AI tool use columns. For grade level, we encod, uh, we convert the uh the string values into integer values. Okay, a show in the picture on the left. And for AI tool use, we which is a multi-label feature. We first, we first identified all the unique features in the data for use, then required corresponding samples such as general nine use and general GPT use, and fill them with zero and one based on actual usage.

**【學員】**：好像耶。Okay, next I will explain our experimental configuration. On the right, you can see some general settings such as seed, top K feature, and sparsity. And primary library we use is this Cikit. Right. And based on the sparsity, we divided the data set into training and testing sets. Using randomWe set to ensure report report.

**【學員】**：However, we noticed that the ratio of test to non-test in the original data set was highly imbalanced. To prevent the worst case, where this imbalance worsens after splitting, we add the this parameter in the train test split function to maintain the original class distribution. Okay, and after splitting the data, we use a dissimilarity score classifier, and we set the entropy as our splitting criteria.

**【學員】**：And to address the imbalanced data issue mentioned earlier, we setCast weight parameter to balance. Okay, and finally, we implement three feature selection methods. 好的，please. Okay, first for the filter method, we use the K best with mutual information, and the wrapper method we simply use IFCV. And the third for the embedded method, we pair the decision tree with the tree from model matrix.

**【學員】**：We use the model internal feature importance attribute and set a threshold to the main importance, automatically retaining the most significant feature. 好的。Okay, and this slide shows the metric we use to evaluate our experimental results. Okay, the overallOf shows a comparison between sparse and the computation matrix, and the lower half with features two matrices, the first visually and for feature selection, we use Jaccard similarity to compare the distrib distribution difference diff difference of feature selected by different methods, and we adjust feature importance to explain the actual impact of each feature during the selection process.

**【學員】**：Oh, yes. Okay. Now let's move on to experiment. So, before we go into baseline, I want to talk about targetleakage， because we didn't drop final score and performance category at first. We achieve near 100% accuracy, which is not accurate at all. So after dropping those two, we got a 94.93% final score, which is high, but it's highly complex.

**【學員】**：Now let's move on to experiment one and two. So we kind of got unexpected result because they all pick the golden three, which is last exam score, assignment score average and co

## 💼 Experimental Results & Presentation Rehearsal: Filter Method Benefits and Timing Review

**【Youchen】**：ncept understanding score, which means we got the same result from experiment one and two. So now let's move on to experiment three. What if we add more features to pick? So you can see on the left side, embeddedModel basically dominates all the experiment, and when k equals seven, embedded model achieved the highest F1 score, but the model is still highly complex.

**【Youchen】**：And now let's look at Jaccard similarity. Because experiment one and two basically produce the same result, they all have a perfect one point zero Jaccard overlap, which proves that those golden three is the top three features for the algorithm. And as we go up to the number, we can see that the the algorithm starting to disagree which one to pick, because there are trash features which is not useful to the model and just produce more noise.

**【Youchen】**：And now下一個。If you look at the chart, you can see that those golden three basically produce seventy three point two percent of the prediction power. Which means we can only, uh, we can just choose those few features for our model, and we can save a lot of resource. Okay. Now, now let's move to section five discussion.

**【Youchen】**：Here we will talk about uh what our machine learning data means for education. First, let's take a look at why our model choose certain features. As you can see, traditional scores like letter exam score, a v a variety homework score, and concept underStandings score are still the most important. Why? Why?

**【Youchen】**：Because truly understanding the knowledge the which AI give is more important than just doing the work. Traditional grades are still the best way to see how much a student really work really knows. On the other hand, AI usage numbers like number of prompts per week and percentage of AI made content are also key helps clues.

**【Youchen】**：This show the bad side of letting the computer do the thinking. When students let AI do the do the hard thinking for them, it hurt the ability toLearn. Okay, next page. Uh, next we need to talk about the features our model didn't use in the past. Without the time spent, mean better learning. But in the age of AI, this is no longer true because AI makes things much faster.

**【Youchen】**：Also, features like uh, also features like age and gender were totally dropped by our model. This shows our model is fair and not biased. It proved proved that a student's actual learning actions are much more important than than who they are born as. Okay, next page.Like all studies, our ours has limit.

**【Youchen】**：But this help guide our future work. First, our current results only look at the one point in time. In the future, we plan to study students over a longer period to see how their actions change. Second, we want to know exactly how much our we gave up to make our model easy to understand. To find out, we need to compare it with more complex models.

**【Youchen】**：Finally, we plan to use a math tool called candle tool. We know some features overlap, butOther, we filter changes the model a lot. Candle tool will help us me measure this. This bring us to the the final part conclusion. To sum up, that we learned from our data, we have four main findings. First, we proved that just three three main features works better than using all of them.

**【Youchen】**：This means we only need to focus on the most most important learning steps instead of watching everything. Second, we suggest a two-step check. Schools should only look at the a student's behavior as a secondSecond, check if the if the students is at risk of failing. Third, for the computer model, the embedded m embedded method is very stable, even with limited computing power.

**【Youchen】**：Computing power, because it works directly with how we group the data. Fourth, the filter method works very well and costs very little. This will help make AI prediction towards in education much more common and easy to get. Okay, thank you for your time and for listening. 我講一下各自的時間，剩餘六分鐘，然後，然後龍龍。中路差不多兩分半，中路差不多兩分半。然後右城的話，我看一下，十四，十四千，五分五分半，五分半，好，五分半，OK，哦，這樣有點太長了，又是。

**【授課講師】**：好，謝謝這組的完整發表，時間控制得相當好。
