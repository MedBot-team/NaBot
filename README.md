﻿# Survey

# Data
List the existing data used for building chatbots by others


| Name | Description| Link |
|---|---|---|
| [SQuAD Stanford Question Answering Dataset] | The SQuAD v1.1 is the Benchmark for QA tasks|https://deepai.org/dataset/squad
| [Persian question answering Dataset] | Persian Question Answering (PersianQA) Dataset is a reading comprehension dataset on Persian Wikipedia. The crowd-sourced dataset consists of more than 9,000 entries. Each entry can be either an impossible-to-answer or a question with one or more answers spanning in the passage (the context) from which the questioner proposed the question. Much like the SQuAD2.0 dataset, the impossible or unanswerable questions can be utilized to create a system which "knows that it doesn't know the answer".|https://github.com/sajjjadayobi/PersianQA 
| [CoQA Dataset] |CoQA is a Conversational Question Answering dataset released by Stanford NLP in 2019. It is a large-scale dataset for building Conversational Question Answering Systems. This dataset aims to measure the ability of machines to understand a text passage and answer a series of interconnected questions that appear in a conversation. The unique feature about this dataset is that each conversation is collected by pairing two crowd workers to chat about a passage in the form of questions and answers and hence, the questions are conversational.  | http://downloads.cs.stanford.edu/nlp/data/coqa/coqa-train-v1.0.json
| [SQuADv2.0 Dataset] |a corpus of research papers to answer COVID-19 related questions |https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json
| [BioASQ2-9 Dataset] |The recent success of question answering systems is largely attributed to pre-trained language models. However, as language models are mostly pre-trained on general domain corpora such as Wikipedia, they often have difficulty in understanding biomedical questions. In this paper, we investigate the performance of BioBERT, a pre-trained biomedical language model, in answering biomedical questions including factoid, list, and yes/no type questions. BioBERT uses almost the same structure across various question types and achieved the best performance in the 7th BioASQ Challenge (Task 7b, Phase B). BioBERT pre-trained on SQuAD or SQuAD 2.0 easily outperformed previous state-of-theart models. BioBERT obtains the best performance when it uses the appropriate pre-/post-processing strategies for questions, passages, and answers. | http://participants-area.bioasq.org/datasets/  && https://drive.google.com/file/d/1-KzAQzaE-Zd4jOlZG_7k7D4odqPI3dL1/view 
| [Disfl-QA: A Benchmark Dataset for Understanding Disfluencies in Question Answering ] | Disfl-QA is a targeted dataset for contextual disfluencies in an information seeking setting, namely question answering over Wikipedia passages. Disfl-QA builds upon the SQuAD-v2 (Rajpurkar et al., 2018) dataset, where each question in the dev set is annotated to add a contextual disfluency using the paragraph as a source of distractors. The final dataset consists of ~12k (disfluent question, answer) pairs. Over 90% of the disfluencies are corrections or restarts, making it a much harder test set for disfluency correction. Disfl-QA aims to fill a major gap between speech and NLP research community. We hope the dataset can serve as a benchmark dataset for testing robustness of models against disfluent inputs. | https://github.com/google-research-datasets/disfl-qa

# Paperswithcode
List of datasets and related source codes
| Name | Description| Link |
|---|---|---|
| PERSONA-CHAT | The PERSONA-CHAT dataset contains multi-turn dialogues conditioned on personas. The dataset consists of 8939 complete dialogues for training, 1000 for validation, and 968 for testing. Each dialogue was performed between two crowd-source workers assuming artificial personas. There are 955 possible personas for training, 100 for validation, and 100 for testing.| [link](https://paperswithcode.com/dataset/persona-chat-1)
| ConvAI2 | The ConvAI2 dataset for training models is based on the PERSONA-CHAT dataset. The speaker pairs each have assigned profiles coming from a set of 1155 possible personas (at training time), each consisting of at least 5 profile sentences, setting aside 100 never seen before personas for validation. | [link](https://paperswithcode.com/dataset/convai2)
| DailyDialog | DailyDialog is a high-quality multi-turn open-domain English dialog dataset. It contains 13,118 dialogues split into a training set with 11,118 dialogues and validation and test sets with 1000 dialogues each. On average there are around 8 speaker turns per dialogue with around 15 tokens per turn. | [link](https://paperswithcode.com/dataset/dailydialog)
| UDC | Ubuntu Dialogue Corpus (UDC) is a dataset containing almost 1 million multi-turn dialogues, with a total of over 7 million utterances and 100 million words. The dataset has both the multi-turn property of conversations in the Dialog State Tracking Challenge datasets, and the unstructured nature of interactions from microblog services such as Twitter. | [link](https://paperswithcode.com/dataset/ubuntu-dialogue-corpus)
| SQuAD | The Stanford Question Answering Dataset (SQuAD) is a collection of question-answer pairs derived from Wikipedia articles. In SQuAD, the correct answers of questions can be any sequence of tokens in the given text. Because the questions and answers are produced by humans through crowdsourcing, it is more diverse than some other question-answering datasets. | [link](https://paperswithcode.com/dataset/squad)
| GLUE | General Language Understanding Evaluation (GLUE) benchmark is a collection of nine natural language understanding tasks, including single-sentence tasks CoLA and SST-2, similarity and paraphrasing tasks MRPC, STS-B and QQP, and natural language inference tasks MNLI, QNLI, RTE and WNLI. The QNLI (Question-answering NLI) dataset is part of GLEU benchmark. <br /> **The QNLI dataset is a Natural Language Inference dataset automatically derived from the Stanford Question Answering Dataset. The dataset was converted into sentence pair classification by forming a pair between each question and each sentence in the corresponding context, and filtering out pairs with low lexical overlap between the question and the context sentence.**| [link](https://paperswithcode.com/dataset/glue)
| TriviaQA | TriviaQA is a realistic text-based question answering dataset which includes 950K question-answer pairs from 662K documents collected from Wikipedia and the web. This dataset is more challenging than standard QA benchmark datasets such as Stanford Question Answering Dataset (SQuAD), as the answers for a question may not be directly obtained by span prediction and the context is very long. TriviaQA dataset consists of both human-verified and machine-generated QA subsets. | [link](https://paperswithcode.com/dataset/triviaqa)
| Natural Questions | The Natural Questions corpus is a question answering dataset containing 307,373 training examples, 7,830 development examples, and 7,842 test examples. Each example is comprised of a Google query and a corresponding Wikipedia page. Each Wikipedia page has a passage (or long answer) annotated on the page that answers the question and one or more short spans from the annotated passage containing the actual answer. | [link](https://paperswithcode.com/dataset/natural-questions)
| MS MARCO | The MS MARCO (Microsoft MAchine Reading Comprehension) is a collection of datasets focused on deep learning in search. The first dataset was a question answering dataset featuring 100,000 real Bing questions and a human generated answer. Over time the collection was extended with a 1,000,000 question dataset, a natural language generation dataset, a passage ranking dataset, keyphrase extraction dataset, crawling dataset, and a conversational search. | [link](https://paperswithcode.com/dataset/ms-marco)
| HotpotQA | HotpotQA is a question answering dataset collected on the English Wikipedia, containing about 113K crowd-sourced questions that are constructed to require the introduction paragraphs of two Wikipedia articles to answer. Each question in the dataset comes with the two gold paragraphs, as well as a list of sentences in these paragraphs that crowdworkers identify as supporting facts necessary to answer the question. | [link](hhttps://paperswithcode.com/dataset/hotpotqa)
| WikiQA | The WikiQA corpus is a publicly available set of question and sentence pairs, collected and annotated for research on open-domain question answering. In order to reflect the true information need of general users, Bing query logs were used as the question source. Each question is linked to a Wikipedia page that potentially has the answer. | [link](https://paperswithcode.com/dataset/wikiqa)
| NewsQA | The NewsQA dataset is a crowd-sourced machine reading comprehension dataset of 120,000 question-answer pairs. In this dataset documents are CNN news articles. | [link](https://paperswithcode.com/dataset/newsqa)
| WebQuestions | The WebQuestions dataset is a question answering dataset using Freebase as the knowledge base and contains 6,642 question-answer pairs. It was created by crawling questions through the Google Suggest API, and then obtaining answers using Amazon Mechanical Turk. | [link](https://paperswithcode.com/dataset/webquestions)
| bAbI | The bAbI dataset is a textual QA benchmark composed of 20 different tasks. Each task is designed to test a different reasoning skill, such as deduction, induction, and coreference resolution. Some of the tasks need relational reasoning, for instance, to compare the size of different entities. | [link](https://paperswithcode.com/dataset/babi-1)
| VQA | Visual Question Answering (VQA) is a dataset containing open-ended questions about images. These questions require an understanding of vision, language and commonsense knowledge to answer. | [link](https://paperswithcode.com/dataset/visual-question-answering)
| VQA v2.0 | Visual Question Answering (VQA) v2.0 is a dataset containing open-ended questions about images. These questions require an understanding of vision, language and commonsense knowledge to answer. It is the second version of the VQA dataset. | [link](https://paperswithcode.com/dataset/visual-question-answering-v2-0)
| Visual7W | Visual7W is a large-scale visual question answering (QA) dataset, with object-level groundings and multimodal answers. Each question starts with one of the seven Ws, what, where, when, who, why, how and which. It is collected from 47,300 COCO iamges and it has 327,929 QA pairs, together with 1,311,756 human-generated multiple-choices and 561,459 object groundings from 36,579 categories. | [link](https://paperswithcode.com/dataset/visual7w)
| VisDial | Visual Dialog (VisDial) dataset contains human annotated questions based on images of MS COCO dataset. This dataset was developed by pairing two subjects on Amazon Mechanical Turk to chat about an image. One person was assigned the job of a ‘questioner’ and the other person acted as an ‘answerer’. The questioner sees only the text description of an image (i.e., an image caption from MS COCO dataset) and the original image remains hidden to the questioner. | [link](https://paperswithcode.com/dataset/visdial)
| SNIPS | The SNIPS Natural Language Understanding benchmark is a dataset of over 16,000 crowdsourced queries distributed among 7 user intents of various complexity: SearchCreativeWork (e.g. Find me the I, Robot television show), GetWeather (e.g. Is it windy in Boston, MA right now?), BookRestaurant (e.g. I want to book a highly rated restaurant in Paris tomorrow night), PlayMusic (e.g. Play the last track from Beyoncé off Spotify), AddToPlaylist (e.g. Add Diamonds to my roadtrip playlist), RateBook (e.g. Give 6 stars to Of Mice and Men), SearchScreeningEvent (e.g. Check the showtimes for Wonder Woman in Paris).| [link](https://paperswithcode.com/dataset/snips)
| Pushshift Reddit | Pushshift makes available all the submissions and comments posted on Reddit between June 2005 and April 2019. The dataset consists of 651,778,198 submissions and 5,601,331,385 comments posted on 2,888,885 subreddits. | [link](https://paperswithcode.com/dataset/pushshift-reddit)
| BST | To analyze how these capabilities would mesh together in a natural conversation, and compare the performance of different architectures and training schemes. | [link](https://paperswithcode.com/dataset/blended-skill-talk)
| Metaphorical Connections | The Metaphorical Connections dataset is a poetry dataset that contains annotations between metaphorical prompts and short poems. Each poem is annotated whether or not it successfully communicates the idea of the metaphorical prompt. | [link](https://paperswithcode.com/dataset/metaphorical-connections)


# Repositories
List all interesting github or gitlab repositories about chatbots
| Name | Description| Link |
|---|---|---|
| [Building a Question-Answering System from Scratch] | I am using the Stanford Question Answering Dataset (SQuAD). The problem is pretty famous with all the big companies trying to jump up at the leaderboard and using advanced techniques like attention based RNN models to get the best accuracy. All the GitHub repositories that I found related to SQuAD by other people have also used RNNs. | https://towardsdatascience.com/building-a-question-answering-system-part-1-9388aadff507
| [Question Answering with a Fine-Tuned BERT] | For something like text classification, you definitely want to fine-tune BERT on your own dataset. For question answering, however, it seems like you may be able to get decent results using a model that’s already been fine-tuned on the SQuAD benchmark. |https://mccormickml.com/2020/03/10/question-answering-with-a-fine-tuned-BERT/
| [Train A Question-Answering Machine Learning Model (Bio-BERT)] |This tutorial covers how to train the Bio-BERT question-answering model on a corpus of research papers to answer COVID-19 related questions. |https://console.paperspace.com/te9htf38d/notebook/riux64pvhze1om8
| [Pre-trained Language Model for Biomedical Question Answering ] | This repository provides the source code and pre-processed datasets of our participating model for the BioASQ Challenge 7b. We utilized BioBERT, a language representation model for the biomedical domain, with minimum modifications for the challenge. | https://github.com/spaditha/biobert
| [Pre-trained Language Model for Biomedical Question Answering ] | This repository provides the source code and pre-processed datasets of our participating model for the BioASQ Challenge 7b. We utilized BioBERT, a language representation model for the biomedical domain, with minimum modifications for the challenge. | https://github.com/dmis-lab/bioasq-biobert

# Kaggle 
This is a list of interesting Kaggle notebook or competitions

| Name | Description| Link |
|---|---|---|
|Chatbot Tourist Guide (ToGu)|One of the important use of chatbot is as a tourist guide. It will help in providing information about an unknown city to the user. Information like important monuments in the city, famous foods, travel mode, etc. can be found easily. Step for getting started with any kind of chatbot:Setting up Environment/Text Gathering/Text cleaning/Word Embedding/Generating answer/Conversation|[https://www.kaggle.com/manzoormahmood/getting-started-with-chatbot](https://www.kaggle.com/manzoormahmood/getting-started-with-chatbot)|
|Building a Chatbot|Creating your own chatbot: RelaBot|[https://www.kaggle.com/melkmanszoon/building-a-chatbot](https://www.kaggle.com/melkmanszoon/building-a-chatbot)|
|CHAT BOT TUTORIAL 2020|In this model I have created a basic AI Interface with External plugin abilities; An Interface AI_Contracts enables for Intefacing with the AI; Implementing the Interface and placing in the the compiled DLL into the APP\Plugins folder enables for the AI_Interface to discover and call the plugin obtaining a response to be returned to the user; The project was design in 4 stages ; Each stage or milestone enables for the development and extension of the Chatbot to become a enriched product worthy of public release.|[https://github.com/spydaz/Chatbot_2020_Tutorial](https://github.com/spydaz/Chatbot_2020_Tutorial)|
| 2020 Athens EESTECH Challenge | Speech Command Recognition: Build an assistive chatbot able to understand speech commands. Dataset contains 97 speakers saying 248 different phrases. The 248 utterances map to 31 unique intents, that are divided into three slots: action, object, and location. The goal in preparing this dataset was to provide a benchmark for end-to-end spoken language understanding models. | [https://www.kaggle.com/c/2020-athens-eestech-challenge](https://www.kaggle.com/c/2020-athens-eestech-challenge) |
| | | |

# RASA
RASA is one of the main players in this domain. Here we study what they have reported in their website.
RASA has a list of chatbots built based on their platform listed in [https://rasa.com/showcase/](https://rasa.com/showcase/). The show cases are presented in three groups. 
 
## Commercial Assistants

| Name | Description | Link | Dataset | Language |
|---|---|---|---|---|
| [Alex](https://rentalpaca.com) | Alex is a virtual real estate agent that's free to use, available 24/7, and literally at the user's fingertips. The bot's secret weapon is called Alex's Alpaca Insights, which provides market information like rental breakdown, lease incentives, and brokers' fees.| [Facebook Messenger bot](https://www.messenger.com/t/102134301160135/) | - | English
| [PicPay's Virtual Assistant](https://www.picpay.com/) | PicPay's Virtual Assistant validates whether a user qualifies for aid with the Brazilian government and helps them claim their benefits.| https://www.picpay.com/ | - | Portuguese
| [Europeana chatbot](https://culturebot.eu/) | The Europeana chatbot was developed by the Culture Chatbot project, led by the Jewish Heritage Network, to increase engagement with the archive through a conversational UI. The chatbot incorporates a knowledge graph and semantic search to uncover connections between records—persons, places, and other entities—allowing the user to search the archive and discover relevant materials using natural language.| https://culturebot.eu/ | - | Spanish, Italian, English, Dutch, Polish
| [TransPerfect covid-19 chatbot](https://www.transperfect.com/dataforce/covid-19-chatbot) | Chatbots and virtual assistants have played a vital role in broadcasting information during the global Covid-19 pandemic.| [Schedule a demo chatbot](https://www.transperfect.com/dataforce-covid-19-chat-demo) | [Data](https://www.transperfect.com/file/Dataforce-Data-Samples.zip ) | English, Spanish, Chinese, Arabic
| [Digital Assistant Robot (DAR)](link) | Digital Assistant Robot (DAR) is a digital employee, built using Rasa, that manages all leave and visa requests at International Software Solutions (ISS) Software Hive. The chatbot helps employees submit leave requests through WhatsApp or Telegram. Employees can also view their submitted requests, track requests, view pending tasks, and respond directly to tasks.| Not found | - | English, Arabic
| [Neon chatbot](https://n26.com/) | Answering questions and solving problems for bank customers. Neon is live in the N26 in the mobile app, handling 20% of customer service requests. | [Mobile app](https://play.google.com/store/apps/details?id=de.number26.android&hl=en_US&gl=US) | - | English, French, German
| [Albert Heijn's AI assistant](https://www.ah.nl/klantenservice) | Albert Heijn's AI assistant works side by side with human agents, answering questions in the customer support chat queue. Acting as a first line of support, the assistant allows employees to spend more time helping customers and less time on FAQs and administrative tasks. | https://www.ah.nl/klantenservice | - | Dutch
| [Eva](https://www.escolavirtual.gov.br/perguntas-frequentes) | Supporting learners at Brazil's Virtual School of the Government. Eva handles common requests and sends a support email only if the request is very specific and she cannot answer.| https://www.escolavirtual.gov.br/perguntas-frequentes | - | Portuguese
| [Culture Chatbot](http://chatbot.jck.nl/) | Culture Chatbot, the digital assistant for the Jewish Historical Museum in Amsterdam, is a virtual tour guide for the museum. In addition to providing practical information about the museum, like hours and ticket prices, it also offers a fun and educational way for users to explore the museum's collection. | http://chatbot.jck.nl/ | - | Dutch, English, Spanish
| [Doodle Bot](https://doodle.com/content/doodle-bot/) | The Doodle Bot helps users coordinate meeting times across teams. Using natural language commands, the Doodle Bot turns scheduling into a human-centered process instead of a tool-centered one. Users can provide the Slack bot with key meeting details and let Doodle Bot do the rest, allowing busy professionals to focus on important tasks instead of performing repetitive manual actions to schedule meetings. | [Slack bot](https://doodle.com/content/doodle-bot) | - | English
| [Cooper](https://www.lemonade.com/blog/rise-autonomous-organization/) | The chatbot assists the Devops Engineering team with tasks like preparing testing environments, running automated tests, and even deploying updates. It also handles tasks like sprint planning. | [Not public. Lemonade's internal automation bot](https://www.lemonade.com/blog/rise-autonomous-organization/) | - | English
| [Helvetia's assistant](m.me/helvetia.ga.liestal/) | Helvetia's assistant allows customers to submit insurance claims for stolen bicycles through an easy to use chat available day or night. | [Facebook Messenger bot](m.me/helvetia.ga.liestal/) | - | German
| [Eddy Travels assistant](https://www.eddytravels.com/) | Eddy Travels assistant helps you travel via an embedded AI assistant. | https://www.eddytravels.com/ | - | English
| [Djingo](https://www.orange.com/en) | Orange's Djingo assistant is capable of looking up account information, answering billing questions, and suggesting steps to diagnose phone and internet connectivity issues. | [Facebook Messenger](https://www.orange.jo/en/pages/djingo-chatbot.aspx) | - | French, English, Arabic
| [Dialogue Virtual Clinic chatbot](https://www.dialogue.co/en/) | The Virtual Clinic chatbot asks patients a series of questions to surface the most relevant information about the patient's condition, equipping human health care practitioners with important background information before their appointment begins. | [Mobile App](https://www.dialogue.co/en/) | - | English, French, German
| [Adobe Sensei AI Assistant](https://www.adobe.com/sensei.html) | Adobe's voice-enabled assistant allows users to sift through hundreds of millions of Adobe Stock assets using an intuitive conversational interface. Users can start with a broad query and use spoken commands to explore options and refine the request, to find just the right image. | https://www.adobe.com/sensei.html | - | English
| [McAi](https://www.vocinity.com/webrtc/?destination=mcdonalds) | The McAi voice assistant allows customers to place orders using spoken voice commands—just like going through the drive-thru. Vocinity's Cognitive Conversational Agents like McAi allow human agents to focus on higher level tasks while providing unlimited scalability for enterprises. | https://www.vocinity.com/webrtc/?destination=mcdonalds | - | English
| [Lola](https://synaptitudebrainhealth.com/) | Lola keeps users on track with their brain health goals by reinforcing healthy habits. Along with Synaptitude's personalized brain health program, Lola provides tracking and motivation for diet, exercise, sleep, stress management and cognitive training. | [SMS, Web Chat](https://synaptitudebrainhealth.com/) | - | English, Mandarin
| [Maya](https://www.lemonade.com/) | The chatbot allows customers to purchase insurance, file claims, and resolve customer service inquiries. | [Mobile App](https://play.google.com/store/apps/details?id=com.lemonadeinc.lemonade&hl=en_US&gl=US) | - | English, German
| [Tia](https://asktia.com) | Providing women's health advice through a HIPAA-compliant interface | [Mobile App](https://apps.apple.com/us/app/tia-female-health-advisor/id1184002073) | - | English






## Personal Projects


| Name | Description| Link |
|---|---|---|
| [name](link) | Explain why this is interesting|

## Platforms

| Name | Description| Link |
|---|---|---|
| [Smartloop](https://smartloop.ai/) | A point and click conversational AI platform that allows anyone to build a contextual AI assistant in less than 10 minutes.|
| [Unique.ai](https://rasa.com/showcase/unique-ai/) | A platform to design chatbots that increase  recruitment team's efficiency by recieving the information from candidates in a conversational interface and pre-qualifying them.|
| [Vocinity's conversational cognitive agent](https://www.vocinity.com/index/coronavirus-hotlines/) | A platform to create chatbots that can used across telephone, text, and chat channels to automatically get specifed information from people throw a conversation. This was used to collect surveys about COVID-19 during the recent pandemic.|
| [JobAI](https://jobai.de/musterstellenangebot/) | Provides an interface to create recruiting chatbots that can answer questions about companies, collect jobseekers' information and inform them anout open roles and even arrange interview meetings. |

