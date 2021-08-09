import json
import requests
import streamlit as st
from decouple import config

# Read URL from .env file in the directory
url = config('RASA_SERVER_URL')

# Page header texts
st.set_page_config(page_title="Synthia")

st.markdown("<h1 style='text-align: center; color:grey;'>\
             MedBot</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: grey;'>\
             Ask your medical questions :) </h3>", unsafe_allow_html=True)
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

# Get the question from user
if st.button('Give me the answer'):
    if question == '':
        st.error('Please ask your question')
    else:
        with st.spinner('Wait for it...'):
            # Pass the question to the chatbot server
            result = question.title()

            payload = json.dumps({
                "message": f"{question}",
                "sender": "default"
            })

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)
            # Give the chatbot answer to the user
            st.markdown(response.json()[0]['text'].replace('\n', '<br>'), unsafe_allow_html=True)

st.markdown('___')
