# RasaReport

# Pros
- Support both text and voice-based conversations
- Great commandline tools for:
    - Training
    - Testing
    - Finetuning
    - Data processing
    - Debugging
    - <img src="report_images/cmd_debugging.png" width="650">

- Include interactive shell for visualization, debugging and data generating purposes
    - <img src="report_images/interactive_visulization.png" width="650">

- Include policy visualization tools for visualizing what so-called happy path
    - <img src="report_images/visulization.png" width="400">

- Easy to configure pipeline and policies

    |  config.yml  | Component Lifecycle  |
    |------------|-------------|
    | <img src="report_images/config_yml.png" width="400"> | <img src="report_images/component_lifecycle.png" width="400"> |

- Supporting many messaging and voice channels by default:
    - Your Website
    - Facebook Messenger
    - Slack
    - Telegram
    - Twilio
    - Microsoft Bot Framework
    - Cisco Webex Teams
    - RocketChat
    - Mattermost
    - Google Hangouts Chat
    - Custom Connectors

- Supporting CDD for real data generation by Rasa X platform
    - Conversation-Driven Development (CDD) is the process of listening to your users and using those insights to improve your AI assistant.
    - CDD includes the following actions:
        - Share your assistant with users as soon as possible
        - Review conversations regularly
        - Annotate messages and use them as NLU training data
        - Test that your assistant always behaves as you expect
        - Track when your assistant fails and measure its performance over time
        - Fix how your assistant handles unsuccessful conversations

- Tools for handling unexpected conversation paths
    - Handling Out-of-scope Messages with *out_of_scope* intent
    - Fallbacks to handle incoming messages with low NLU confidence.
    - <img src="report_images/fallback.png" width="450">
    - Support machine-learning-based policies such as the TED Policy.
    - Human Handoff
    - Handling contextual interjections with *requested_slot*

- Reaching out first
    - <img src="report_images/reaching_out_first.png" width="450">
- External Events
    - Sometimes, you want an external device to change the course of an ongoing conversation. For example, if you have a moisture-sensor attached to a Raspberry Pi, you could use it to notify you when a plant needs watering via your assistant.

- Reminders
    - You can have your assistant reach out to the user after a set amount of time using Reminders.

- Support many components by default:
    - Language Models
        - MitieNLP
        - SpacyNLP
    - Tokenizers
        - WhitespaceTokenizer
        - JiebaTokenizer
        - MitieTokenizer
        - SpacyTokenizer
    - Featurizers
        - MitieFeaturizer
        - SpacyFeaturizer
        - ConveRTFeaturizer
        - LanguageModelFeaturizer (HuggingFace's Transformers)
            - BERT
            - GPT
            - GPT-2
            - GPTNeo
            - Transformer-XL
            - XLNet
            - XLM
            - DistilBERT
            - CTRL
            - CamemBERT
            - ALBERT
            - T5
            - XLM-RoBERTa
            - RoBERTa
            - FlauBERT
            - Bart
            - BARThez
            - DialoGPT
            - Reformer
            - M2M100
            - MarianMT
            - Pegasus
            - Longformer
            - MBart
            - Lxmert
            - Funnel Transformer
            - LayoutLM
            - DeBERTa
            - SqueezeBERT
        - RegexFeaturizer   
        - CountVectorsFeaturizer
        - LexicalSyntacticFeaturizer
    -  Intent Classifiers
        - MitieIntentClassifier
        - SklearnIntentClassifier
        - KeywordIntentClassifier
        - DIETClassifier
        - FallbackClassifier
    - Entity Extractors
        - MitieEntityExtractor
        - SpacyEntityExtractor
        - CRFEntityExtractor
        - DucklingEntityExtractor
        - DIETClassifier
        - EntitySynonymMapper
    - Combined Intent Classifiers and Entity Extractors
        - DIETClassifier
    - Selectors
        - ResponseSelector
    - Custom Components
        - You can create a custom component to perform a specific task which NLU doesn't currently offer (for example, sentiment analysis).

- Policies
    - Your assistant uses policies to decide which action to take at each step in a conversation. There are machine-learning and rule-based policies that your assistant can operate in tandem.
    - Support policy priority
        - If two policies predict with equal confidence (for example, the Memoization and Rule Policies might both predict with confidence 1), the priority of the policies is considered.
    - Machine Learning Policies
        - Transformer Embedding Dialogue (TED) Policy
        - Memoization Policy
            - The MemoizationPolicy remembers the stories from your training data. It checks if the current conversation matches the stories in your *stories.yml* file. 
        - Augmented Memoization Policy
    - Rule-based Policies
    - Custom Policies

- Contextual conversations support
    - With slots
        - Slots are your assistant's memory. They can be helpful for contextual conversations.
    - With machine-learning-based policies such as the TED Policy.
    - Also, support *max_history* for a certain amount of context that's relevant to your assistant. 

- Multi-Intent Classification

- Active contributors
    - <img src="report_images/contributor.png" width="600">

- Great customers
    - <img src="report_images/customer.png" width="400">

# Cons
- Some of the rasa's features (Like CDD, Analytics, ...) are only available in proprietary solutions.
    - <img src="report_images/rasa_platform.png" width="600">

- License issue in Rasa X
    - You can:
        - Use Rasa X to build AI assistants for commercial or non-commercial purposes
        - Host Rasa X for your own project
    - You can't:
        - Offer a SaaS product or any online service built with or on top of Rasa X that competes with or provides similar functionality to Rasa X
        - Use or copy the Rasa X Software for decompilation or reverse engineering
        - Change the code


- Not support visual tasks. RASA is mainly restricted to ChitChat and FAQ tasks.

- Models (both rule-based and machine-learning-based) are retrieval-based. Generative models or Hybrid models (generative models + retrieval models) are not supported.

- If we use **language models** in our pipeline, we'll be restricted to only Spacy or MITIE supported languages. But alternatively, we can use **LanguageModelFeaturizer featurizer** with a little more effort.
    - <img src="report_images/spacy.png" width="500">



# New Ideas
- Design an easy-to-use GUI for the Rasa platform. 

- Fork of rasa with support of more models. (Generative and Hybrid models like BlenderBot)

- Design task-based models. For example medical bots. (Like [Dialogue](https://www.dialogue.co/en/))
    - <img src="report_images/dialogue.png" width="300">

# Enterprise platforms to generate new ideas.
## Enterprise platforms with proprietary models
- [Google Dialogflow](https://cloud.google.com/dialogflow)
    - <img src="report_images/dialogflow.png" width="600">
- [Facebook wit.ai](https://wit.ai/)
- [Microsoft Bot Framework](https://dev.botframework.com/)
- [Amazon Lex](https://aws.amazon.com/lex/)
    - <img src="report_images/amazon.png" width="600">
- [IBM Watson](https://www.ibm.com/watson)
- [SAP Conversational AI](https://www.sap.com/italy/products/conversational-ai.html)

## Enterprise platforms with semi-opensource models
- [Rasa Enterprise](https://rasa.com/enterprise/)
- [Botpress Enterprise](https://botpress.com/enterprise)
    - <img src="report_images/botpress.png" width="600">
- [Flow.ai](https://flow.ai/)
    - <img src="report_images/flow.png" width="600">

