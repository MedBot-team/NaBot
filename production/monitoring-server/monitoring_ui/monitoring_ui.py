import time
import matplotlib
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from decouple import config
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import RendererAgg
from utils import Monitoring

# Set matplotlib logging level to warnings
plt.set_loglevel('WARNING')

# Load some parameters from .env file
database_host = config('EVENTS_DB_HOST')
events_database = config('MYSQL_EVENTS_DATABASE')
mysql_user = config('SQL_USER')
mysql_password = config('MYSQL_EVENTS_ROOT_PASSWORD')
refresh_rate=config('REFRESH_RATE')

# Set page layout to wide
st.set_page_config(layout="wide")
# Change matplotlib backend to agg (change writing to file mode)
matplotlib.use("agg")
_lock = RendererAgg.lock
# Set seaborn style
sns.set_style("white")

# Set page title 
page_title = "<h1 style='text-align: center; color: black;'>Analyzing Chatbot Records</h1>"
st.markdown(page_title, unsafe_allow_html=True)


# Initiate monitoring utils
monitoring = Monitoring(database_host, mysql_user,
                        mysql_password, events_database)
# Get events from MySQL server
events = monitoring.get_events()
# Get list of all intents
intents = monitoring.get_intents(events)
# Get list of user feedbacks
feedbacks = monitoring.get_feedbacks(intents)
# Get list of all events
datas = monitoring.get_datas(events)
# Extract different parts of events
intent_confidences, entity_confidences, timestamps,\
input_channels, entity_extractors = monitoring.get_variables(datas)
# Convert timestamps to the YYYY-MM-DD format 
dates = monitoring.convert_date(timestamps)


st.write('')
st.write('')

_, row1_1, _, row1_2, _ = st.columns((.1, 1, .1, 1, .1))
# Plot Chatbot channels statistics
with row1_1, _lock:
    subheader_1 = "<h2 style='text-align: center; color: black;'>Chatbot channels statistics</h2>"
    st.markdown(subheader_1, unsafe_allow_html=True)

    fig = Figure()
    ax = fig.subplots()
    sns.histplot(input_channels, color="turquoise", kde=True,
                 stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)

# Plot Feedbacks statistics
with row1_2, _lock:
    subheader_2 = "<h2 style='text-align: center; color: black;'>Feedbacks statistics</h2>"
    st.markdown(subheader_2, unsafe_allow_html=True)
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(feedbacks, color="dodgerblue", kde=True, 
                 stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)

st.write('')
st.write('')

_, row2_1, _, row2_2, _ = st.columns((.1, 1, .1, 1, .1))
# Plot chatbot requests over time
with row2_1, _lock:
    subheader_3 = "<h2 style='text-align: center; color: black;'>Chatbot requests over time</h2>"
    st.markdown(subheader_3, unsafe_allow_html=True)
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(dates, color="orange", kde=True,
                 stat="density", linewidth=0, ax=ax)

    xticks = ax.get_xticks()
    # In the xticks only show the limited number of days
    days_len = len(xticks)
    time_skip = days_len//5 if days_len// 5 != 0 else 1
    ax.set_xticks(xticks[::time_skip])

    ax.tick_params(axis='x', rotation=70)
    st.pyplot(fig)

# Plot chatbot intents distribution
with row2_2, _lock:
    subheader_4 = "<h2 style='text-align: center; color: black;'>Intents Distribution</h2>"
    st.markdown(subheader_4, unsafe_allow_html=True)
    fig = Figure(figsize=(8, 6))
    ax = fig.subplots()
    ax.hist(intents, density=True, bins=30, color='deepskyblue')
    ax.set_xlabel('Intents')
    ax.set_ylabel('Density')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=70)
    st.pyplot(fig)

st.write('')
st.write('')

_, row3_1, _, row3_2, _ = st.columns((.1, 1, .1, 1, .1))
# Plot chatbot entities confidence distribution
with row3_1, _lock:
    subheader_5 = "<h2 style='text-align: center; color: black;'>Entities Confidence Distribution</h2>"
    st.markdown(subheader_5, unsafe_allow_html=True)
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(entity_confidences, color="deeppink",
                 kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)

# Plot Intents Confidence Distribution
with row3_2, _lock:
    subheader_6 = "<h2 style='text-align: center; color: black;'>Intents Confidence Distribution</h2>"
    st.markdown(subheader_6, unsafe_allow_html=True)
    st.subheader('')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(intent_confidences, color="dodgerblue",
                 kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)

st.write('')
st.write('')

_, row4_1, _, row4_2, _ = st.columns((.1, 1, .1, 1, .1))
# Plot Entity extractors statistics
with row4_1, _lock:
    subheader_7 = "<h2 style='text-align: center; color: black;'>Entity extractors statistics</h2>"
    st.markdown(subheader_7, unsafe_allow_html=True)
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(entity_extractors, color="darkviolet",
                 kde=True, stat="density", linewidth=0, ax=ax)
    st.pyplot(fig)

time.sleep(int(refresh_rate))
