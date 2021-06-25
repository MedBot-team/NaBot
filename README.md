# Survey

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
[List](https://github.com/arezae/chatbot/blob/main/First_Survey/paperswithcode.md) of datasets and related papers and source codes.


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
|text-classification-chatbot|This Python 3 environment comes with many helpful analytics libraries installed. It is defined by the kaggle/python docker image|[https://www.kaggle.com/rahulvks/text-classification-chatbot](https://www.kaggle.com/rahulvks/text-classification-chatbot)|

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
| [Moltron](https://sid321axn.github.io/moltron_website/) | Moltron is a personal project, that answers queries related to machine learning. It can also handle generalized questions, which chatbots often struggle to respond to. Lastly, it gives multimedia-rich responses in the form of videos and explainer images. The assistant is open source and available for the community to fork on GitHub.| [Github](https://github.com/sid321axn/rasa_ml_bot)
| [CalFireAlertChatBot]() | A service that texts people updates on the California Forest Fires. Chatbot built with RASA to update users with info about their city| [Github](https://github.com/amittallapragada/CalFireAlertChatBot)
| [CBOT]() | The bot answers questions about the C programming language, and also solves queries using the Stack Overflow API if the question is outside of the assistant's domain. The idea for CBOT came about as a way to help students new to programming.| [Github](https://github.com/amittallapragada/CalFireAlertChatBot)
| [Gliobot]() | Gliobot is a chatbot embedded in the website that answers questions about glioblastoma multiforme.| []()
| [Nora](https://norabot.ml/) | Nora is an AI assistant that answers questions about the coronavirus and provides information about social distancing, self-isolation, and the latest coronavirus news.| [Github](https://github.com/Archish27/nora-covid-19-bot)
| [Golfbot](https://arxiv.org/abs/1803.11175) | Golfbot, built by Greg Stephens, returns rules and regulations from the 2019 United States Golf Association, using Rasa and the Google Universal Sentence Encoder.| []()
| [booking salon appointments]() | Using a suite of technologies working in concert, Josh Converse's AI assistant interprets voice commands to book salon appointments, with Rasa driving NLU and dialogue management.| []()
| [A voice-controlled avatar]() | Anna is a voice-controlled avatar made with Blender and Panda3D, powered by a Raspberry Pi 4 running Rasa. Julian Gerhard built Anna in his free time, as a proof of concept demonstrating the SmartBoard in an educational use case.| []()
| [Jokebot]() | Greg Stephens built Jokebot, a demo assistant that can respond to users with corny jokes, geek jokes, or funny quotes, all sourced from open APIs.| [Github](https://github.com/rgstephens/jokebot)
| [A Multilingual DemoBot]() | Thomas Zezula's DemoBot can handle basic chitchat in English and German. It allows the user to explore the project page and subscribe to a newsletter. The objective was to build a multilingual bot prototype. The project makes it easy to add a new language model and spin up a new Rasa agent, and it all ships as a single package that can be deployed to Heroku.| [GitLab](https://gitlab.com/langnerd/chatbot-engine)

## Platforms

| Name | Description| Link |
|---|---|---|
| [Smartloop](https://smartloop.ai/) | A point and click conversational AI platform that allows anyone to build a contextual AI assistant in less than 10 minutes.|
| [Unique.ai](https://rasa.com/showcase/unique-ai/) | A platform to design chatbots that increase  recruitment team's efficiency by recieving the information from candidates in a conversational interface and pre-qualifying them.|
| [Vocinity's conversational cognitive agent](https://www.vocinity.com/index/coronavirus-hotlines/) | A platform to create chatbots that can used across telephone, text, and chat channels to automatically get specifed information from people throw a conversation. This was used to collect surveys about COVID-19 during the recent pandemic.|
| [JobAI](https://jobai.de/musterstellenangebot/) | Provides an interface to create recruiting chatbots that can answer questions about companies, collect jobseekers' information and inform them anout open roles and even arrange interview meetings. |

