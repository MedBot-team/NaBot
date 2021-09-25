# NaBot Medical Chatbot :robot:
![Chatbot Unit testing](https://github.com/MedBot-team/NaBot/actions/workflows/rasa-test.yml/badge.svg?style=svg)
![Action server workflow](https://github.com/MedBot-team/NaBot/actions/workflows/docker_push_actions.yml/badge.svg?style=svg)
![Chatbot server workflow](https://github.com/MedBot-team/NaBot/actions/workflows/docker_push_chatbot.yml/badge.svg?style=svg)
![Chatbot UI workflow](https://github.com/MedBot-team/NaBot/actions/workflows/docker_push_ui.yml/badge.svg?style=svg)
![Chatbot Monitoring workflow](https://github.com/MedBot-team/NaBot/actions/workflows/docker_push_monitoring.yml/badge.svg?style=svg)

![Logo](https://github.com/Ali-Razmdideh/NaBot/blob/main/logo.png)

NaBot is a smart medical chatbot. It can retrieve medicines and lab tests information for users just by chatting with it.

- Hey, NaBot, can you give me dosage information of Acetaminophen?
- Of course, I can! :wink:

We will support more features in the future. But now, we only support medicines and lab tests information.

# Test Chatbot

- Use website:
  - https://nabot.ml/
- Use Telegram channel
  - http://t.me/ask_nabot

# Use api
  - https://api.nabot.ml

# Test Monitoring tools
  - https://monitor.nabot.ml/

# List of NaBot features

You can find out a list of medicines, labs, and their information which we're supporting, in the following. 

* [List of medicines in our dataset](https://github.com/MedBot-team/NaBot/wiki/List-of-medicines)
* [List of lab tests in our dataset](https://github.com/MedBot-team/NaBot/wiki/List-of-lab-test)
* [List of information about medicines that NaBot supports](https://github.com/MedBot-team/NaBot/wiki/Medicines-information)
* [List of information about lab tests that NaBot supports](https://github.com/MedBot-team/NaBot/wiki/Lab-tests-information)

# Installation Guide

NaBot can be installed from its source code or by docker images. For more information, please read our [installation guide document](https://github.com/MedBot-team/NaBot/wiki/Installation-Guide).

# Contributing

If you have an idea for improving NaBot, or even if you want medicine or lab test information, which is not supported in NaBot yet, do not hesitate. Create an issue in GitHub. :heart:

NaBot needs an open-source contribution. The more features it has, the more skillful it becomes! 

# Credits
Our chatbot gets its power from the [Rasa](https://rasa.com/) engine. We are thankful to their team for their contribution to open-source society. :heart_eyes:

Our autocorrect component in the chatbot is based on [SymSpell](https://github.com/wolfgarbe/SymSpell), which medical and Persian dictionaries are added to it. We are thankful to their team for their contribution to open-source society. :heart_eyes:

UI of ourchatbot gets its power from [Streamlit](https://github.com/streamlit/streamlit). Thanks for their contribution to the open-source society. :heart_eyes:

A list of medicines information has been collected from [Drugs.com](https://www.drugs.com/) and [MedlinePlus](https://medlineplus.gov/druginformation.html). We're appreciating their teams for producing great medicines information. :hugs:

A list of lab tests information has been collected from [Lab tests online](https://labtestsonline.org/) and [MedlinePlus](https://medlineplus.gov/lab-tests/). We're appreciating their teams for producing great lab tests information. :hugs:
