import matplotlib
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from decouple import config
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import RendererAgg
from utils import Monitoring


plt.set_loglevel('WARNING')

database_host = config('HOST')
events_database = config('MYSQL_EVENTS_DATABASE')
mysql_user = config('SQL_USER')
mysql_password = config('MYSQL_ROOT_PASSWORD')

st.set_page_config(layout="wide")

matplotlib.use("agg")

_lock = RendererAgg.lock
sns.set_style("white")
st.text('Analyzing Chatbot Records')

monitoring = Monitoring(database_host, mysql_user,
                        mysql_password, events_database)
events = monitoring.get_events()
intents = monitoring.get_intents(events)
datas = monitoring.get_datas(events)
intent_confidences, entity_confidences, \
    timestamps, input_channels, entity_extractors = monitoring.get_confidences(datas)
dates = monitoring.convert_date(timestamps)
feedbacks = monitoring.get_feedbacks(intents)


st.write('')
row1_space1, row1_1, row1_space2, row1_2, row1_space3 = st.columns(
    (.1, 1, .1, 1, .1))

with row1_1, _lock:
    st.subheader('Input channels statistics')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(input_channels, color="turquoise", kde=True,
                 stat="density", linewidth=0, ax=ax)

    xticks = ax.get_xticks()
    ax.set_xticks(xticks[::len(xticks) // 2])
    st.pyplot(fig)
    st.markdown("Chatbot requests over time")


with row1_2, _lock:
    st.subheader('Feedback state')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(feedbacks, color="dodgerblue",
                 kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)
    st.markdown("Distribution of intents confidences")


st.write('')
row2_space1, row2_1, row2_space2, row2_2, row2_space3 = st.columns(
    (.1, 1, .1, 1, .1))

with row2_1, _lock:
    st.subheader('Chatbot requests over time')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(dates, color="orange", kde=True,
                 stat="density", linewidth=0, ax=ax)

    xticks = ax.get_xticks()
    ax.set_xticks(xticks[::len(xticks) // 2])
    ax.tick_params(axis='x', rotation=70)
    st.pyplot(fig)
    st.markdown("Chatbot requests over time")

with row2_2, _lock:
    st.subheader('Intents Distribution')
    fig = Figure(figsize=(8, 6))
    ax = fig.subplots()
    ax.hist(intents, density=True, bins=30, color='deepskyblue')
    ax.set_xlabel('Intents')
    ax.set_ylabel('Density')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=70)
    st.pyplot(fig)
    st.markdown("Distribution of intents")


st.write('')
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (.1, 1, .1, 1, .1))

with row3_1, _lock:
    st.subheader('Entity Confidence Distribution')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(entity_confidences, color="deeppink",
                 kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)
    st.markdown("Distribution of entities confidences")


with row3_2, _lock:
    st.subheader('Intent Confidence Distribution')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(intent_confidences, color="dodgerblue",
                 kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)
    st.markdown("Distribution of intents confidences")


st.write('')
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
    (.1, 1, .1, 1, .1))

with row4_1, _lock:
    st.subheader('Entity extractors statistics')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(entity_extractors, color="darkviolet",
                 kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)
    st.markdown("Distribution of entities confidences")
