import json
import random
import requests
import streamlit as st
from decouple import config
from ui_annotator import HTMLAnnotator



# Create random user_id
if 'user_id' not in st.session_state:
    user_id = 'st' + str(random.randint(100000, 999999))
    st.session_state['user_id'] = user_id

# Configure the web page (header , ...)
st.set_page_config(page_title='MedBot',
                   layout='wide',
                   initial_sidebar_state='auto')

html_annotator = HTMLAnnotator()
text_annotator = html_annotator.annotated_text


# Read URL from .env file in the directory
url = config('RASA_SERVER_URL')

st.markdown("<h1 style='text-align: center; color:grey;'>\
             MedBot</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: grey;'>\
             Ask your medical questions 👩‍⚕️ </h3>", unsafe_allow_html=True)
st.write('')

# Show GitHub page badge
"""
[![Star](https://img.shields.io/github/stars/arezae/chatbot.svg?logo=github&style=social)](https://gitHub.com/arezae/chatbot)
"""

st.markdown('___')

# Page sidebar
# sidebar header
st.sidebar.header('About MedBot')
st.sidebar.write('')
# sidebar text
st.sidebar.markdown("<h4 style='text-align: left; color:grey;'>\
                    MedBot is a Rasa-based, smart medical chatbot.\
                    It can retrieve medicines and lab tests information\
                    for users just by chatting with it.</h4>", unsafe_allow_html=True)


st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')

# add expander to the sidebar for website detail
site_expander = st.sidebar.expander('Website')
site_expander.markdown(
    "[MedBot instruction](https://arezae.github.io/chatbot/)")

# add expander to the sidebar for some conversation examples
exm_expander = st.sidebar.expander('Conversation Example')
exm_expander.write("What is the globulin test?")
exm_expander.write("What are the Gemfibrozil side-effects?")


# Questions
st.markdown("<h2 style='text-align: left; color:#F63366;'><b>Ask your question<b></h2>",
            unsafe_allow_html=True)
st.write('')

question = st.text_area("We support medicine and lab test related questions. For more information visit our website",
                        max_chars=500, value="Can you give me dosage information of Acetaminophen?")


# Ask question button
ask_button = st.button('Give me the answer')

# Function to use when feedback button is clicked
def send_feedback(feedback):
    payload = json.dumps({
        "message": f"{feedback}",
        "sender": f"{st.session_state['user_id']}"
    })
    requests.request("POST", url, headers=headers, data=payload)
    st.success('Feedback submitted successfully')


# When ask question button is clicked
if ask_button:
    if question == '':
        st.error('Please ask your question')
    else:
        with st.spinner('Wait for it...'):
            # Pass the question to the chatbot server
            result = question.title()

            payload = json.dumps({
                "message": f"{question}",
                "sender": f"{st.session_state['user_id']}"
            })

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload).json()[0]
        
            # Display feedback buttons
            if len(response) != 0:
                response_text_json = json.loads(response['text'])
                context = response_text_json['context']
                
                if response['buttons']:
                    for button in response['buttons']:
                        b = st.button(
                            label=button['title'],
                            on_click=send_feedback,
                            args=[button['payload']],)
                
                context_preceding_answer = context[:response_text_json['start']]
                context_following_answer = context[response_text_json['end']:]

                # Show the response to the user with highlighting the answer
                text_annotator(
                    context_preceding_answer.replace('\n', ''),
                    (response_text_json['answer'].replace('\n', ''), "#afa"),
                    context_following_answer.replace('\n', ''),
                )
            else:
                print('Unfortunately, I don\'t know the answer to this question yet')

st.markdown('___')
