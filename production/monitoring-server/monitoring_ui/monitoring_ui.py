import matplotlib
import streamlit as st
import seaborn as sns
from whatlies.transformers import Pca, Umap, Tsne
from whatlies import EmbeddingSet
from whatlies.language import SpacyLanguage
import nlpaug.augmenter.char as nac
from collections import Counter
from functools import reduce
import matplotlib.pyplot as plt
from decouple import config
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import RendererAgg
from monitoring import Monitoring
from utils import *
import pandas as pd
from string import punctuation


# Load parameters from .env file
DB_HOST = config('EVENTS_DB_HOST')
DB_NAME = config('POSTGRES_EVENTS_DATABASE')
DB_USER = config('POSTGRES_USER')
DB_PASSWD = config('POSTGRES_EVENTS_PASSWORD')
DB_PORT = config('POSTGRES_PORT')
TOKEN = config("TOKEN")

plt.set_loglevel('WARNING')  # Set matplotlib logging level to warnings
st.set_page_config(
    page_title="Monitoring",
    layout="wide",
)  # Set page layout to wide
# Change matplotlib backend to agg (change writing to file mode)
matplotlib.use("agg")
_lock = RendererAgg.lock
sns.set_style("white")  # Set seaborn style

# Initiate db from Monitoring
monitoring = Monitoring(DB_NAME, DB_USER, DB_PASSWD, DB_HOST, DB_PORT)

# SET page title
page_title = "<h1 style='text-align: center; color: black;'>Monitor NaBot</h1>"
st.markdown(page_title, unsafe_allow_html=True)

statement = st.sidebar.selectbox(
    "Do you want to monitor which time interval logs?",
    ['Last 24 hour', 'Last week', 'Last month'],
    index=0,
    key="events_time"
)

events = monitoring.get_events(statement)  # Get events from MySQL server
intents = monitoring.get_intents(events)  # Get list of all intents
feedbacks = monitoring.get_feedbacks(intents)  # Get list of user feedbacks
datas = monitoring.get_datas(events)  # Get list of all events
questions = monitoring.get_questions(datas)  # Get list of all questions
faq_question = dict(Counter(questions).most_common(
    5)).keys()  # give 5 most common questions
# Extract different parts of events
intent_confidences, entity_confidences, timestamps,\
    input_channels, entity_extractors = monitoring.get_variables(datas)
# Convert timestamps to the YYYY-MM-DD format
dates = monitoring.convert_date(timestamps)

if len(questions) == 0:
    st.sidebar.warning(f"Nabot haven't any records in {statement}")
    charts = st.sidebar.multiselect(
        "Please slecet analyzing method",
        ()
    )
else:
    charts = st.sidebar.multiselect(
        "Please slecet analyzing method",
        ('Records', 'NLU Model', 'Spell Generator', 'Question Distribution')
    )

if "Records" in charts:
    st.markdown("# Analyzing NaBot Records", unsafe_allow_html=True)
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
        time_skip = days_len//5 if days_len // 5 != 0 else 1
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

if "NLU Model" in charts:
    st.markdown("# Analyzing NaBot NLU Model", unsafe_allow_html=True)
    st.write('')
    st.write('')

    text_input = st.selectbox(
        f"most frequently questions in {statement}",
        faq_question,
        key="nm",
        index=0,
    )

    blob = get_api(text_input, TOKEN)
    text = blob["text"]
    text = text.translate(str.maketrans('', '', punctuation))
    tokens = text.split()

    st.markdown("## Tokens and Entities")
    st.write(
        create_displacy_chart(tokens=tokens, entities=blob["entities"]),
        unsafe_allow_html=True,
    )
    st.write('')
    st.write('')

    with st.expander("Full Entities Confidence"):
        st.json(blob["entities"])

    st.markdown("## Intents")

    chart_data = pd.DataFrame(blob["intent_ranking"]).sort_values("name")
    p = create_altair_chart(chart_data)
    st.altair_chart(p, use_container_width=True)

if "Spell Generator" in charts:
    st.markdown("# Analyzing NaBot Spell Generator", unsafe_allow_html=True)
    st.write('')
    st.write('')

    text_input = st.selectbox(
        f"most frequently questions in {statement}",
        faq_question,
        key="sg",
        index=0,
    )
    st.markdown("## Generator Settings")
    n_generate = st.slider(
        "Number of samples to generate",
        min_value=1, max_value=30, value=10, step=1, key="sample_generate"
    )
    min_char, max_char = st.slider(
        "Number of characters to change",
        min_value=0, max_value=10, value=(1, 2), step=1, key="char_change"
    )
    min_word, max_word = st.slider(
        "Number of words to change",
        min_value=0, max_value=10, value=(1, 2), step=1, key="word_change"
    )

    aug = nac.KeyboardAug(
        aug_char_min=min_char,
        aug_char_max=max_char,
        aug_word_min=min_word,
        aug_word_max=max_word,
        include_special_char=False,
        include_numeric=False,
        include_upper_case=False,
    )
    augs = aug.augment(text_input, n=n_generate)
    data = reduce(
        lambda a, b: a +
        b, [get_api(a, TOKEN)["intent_ranking"] for a in augs]
    )

    source = pd.DataFrame(data)[["name", "confidence"]].rename(
        columns={"name": "intent"})

    intents = set(source['intent'])
    dataset = [source[source.intent == intent]
               ["confidence"].values for intent in intents]

    fig = Figure(figsize=(14, 4), dpi=80)
    ax = fig.subplots()
    ax.violinplot(dataset)
    plt.gca().yaxis.grid(True)
    ax.set_xlabel('Intents')
    ax.set_ylabel('Confidence')
    ax.set_xticks(range(1, len(list(intents)) + 1))
    ax.set_xticklabels(list(intents), rotation=45)
    plt.setp(ax.xaxis.get_majorticklabels())

    st.markdown("## Simple Line View")
    st.pyplot(fig, use_container_width=True)

    with st.expander("Generated Examples"):
        st.experimental_show(augs)

if "Question Distribution" in charts:
    st.markdown("# Clustering Text")
    st.write('')
    st.write('')

    reduction_method = st.selectbox(
        "Reduction Method",
        ("PCA", "t-SNE", "Umap"),
        key="rm"
    )

    if reduction_method == "Umap":
        n_neighbors = st.slider(
            "Number of UMAP neighbors",
            min_value=1,
            max_value=50,
            value=2,
            step=1,
            key="n_neighbors",
        )
        min_dist = st.slider(
            "Minimum Distance for UMAP",
            min_value=0.01,
            max_value=0.99,
            value=0.5,
            step=0.01,
            key="min_dist",
        )
        reduction = Umap(2, n_neighbors=n_neighbors, min_dist=min_dist)
    elif reduction_method == "t-SNE":
        reduction = Tsne(2)
    else:
        reduction = Pca(2)

    lang = SpacyLanguage("en_core_web_md")
    emb = EmbeddingSet(*[lang[t] for t in questions])

    try:
        p = (
            emb.transform(reduction)
            .plot_interactive(annot=False)
            .properties(height=500, title="")
        )
        st.altair_chart(p, use_container_width=True)
    except:
        st.error("Sorry I can't plot with this methods")
