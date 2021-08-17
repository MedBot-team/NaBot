from matplotlib.backends.backend_agg import RendererAgg
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from matplotlib.figure import Figure
import mysql.connector
import json
from decouple import config


password = config('password')

st.set_page_config(layout="wide")


def get_events():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='rasa')

    cursor = db.cursor()
    cursor.execute(
        "SELECT intent_name, data FROM events WHERE type_name = 'user'")
    events = [item for item in list(cursor)]

    return events


def get_intents(events):
    intents = [event[0] for event in events]
    return intents


def get_datas(events):
    datas = [event[1] for event in events]
    return datas


def get_confidences(datas):
    data_count = len(datas)
    intent_confidences = []
    entity_confidences = []
    timestamps = []

    for i in range(data_count):
        json_acceptable_string = datas[i].replace("'", "\"")
        dictionary = json.loads(json_acceptable_string)
        intent_confidences.append(
            dictionary['parse_data']['intent']['confidence'])

        for entity in dictionary['parse_data']['entities']:
            if len(entity) != 0 and 'confidence_entity' in entity.keys():
                entity_confidences.append(entity['confidence_entity'])

        timestamps.append(dictionary['timestamp'])

    return intent_confidences, entity_confidences, timestamps



matplotlib.use("agg")

_lock = RendererAgg.lock
sns.set_style("white")
st.text('Analyzing Chatbot Records')


events = get_events()
intents = get_intents(events)
datas = get_datas(events)
intent_confidences, entity_confidences, timestamps = get_confidences(datas)


st.write('')
row1_space1, row1_1, row1_space2, row1_2, row1_space3 = st.columns(
    (.1, 1, .1, 1, .1))

with row1_1, _lock:
    st.subheader('Intent Confidence Distribution')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(intent_confidences, color="dodgerblue", kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)
    st.markdown("Distribution of intents confidences")


with row1_2, _lock:
    st.subheader('Entity Confidence Distribution')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(entity_confidences, color="deeppink", kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)

    st.markdown("Distribution of entities confidences")


st.write('')
row2_space1, row2_1, row2_space2, row2_2, row2_space3 = st.columns(
    (.1, 1, .1, 1, .1))

with row2_1, _lock:
    st.subheader('Intents Distribution')
    fig = Figure(figsize=(8, 6))
    ax = fig.subplots()
    ax.hist(intents, density=True, bins=30)
    ax.set_xlabel('Intents')
    ax.set_ylabel('Density')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=70 )
    st.pyplot(fig)

    st.markdown("Distribution of intents")


with row2_2, _lock:
    st.subheader('Chatbot requests over time')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(timestamps, color="orange", kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)
    st.markdown("Chatbot requests over time")