import streamlit as st
from whatlies.transformers import Pca, Umap, Tsne
from whatlies import EmbeddingSet
from whatlies.language import SpacyLanguage
from utils import read_bytes


uploaded = st.file_uploader(
    "Upload a `.yml` file like `nlu.yml` for clustering.",
    type="yml",
)

if not uploaded:
    filepath = "default.yml"
    with open(filepath) as f:
        texts = read_bytes(f)
else:
    bytes_data = uploaded.read()
    texts = read_bytes(bytes_data.decode("utf-8"))

reduction_method = st.selectbox("Reduction Method", ("Pca", "Tsne", "Umap"))
if reduction_method == "Umap":
    n_neighbors = st.slider(
        "Number of UMAP neighbors", min_value=1, max_value=50, value=2, step=1
    )
    min_dist = st.slider(
        "Minimum Distance for UMAP",
        min_value=0.01,
        max_value=0.99,
        value=0.5,
        step=0.01,
    )
    reduction = Umap(2, n_neighbors=n_neighbors, min_dist=min_dist)
elif reduction_method == "Tsne":
    reduction = Tsne(2)
else:
    reduction = Pca(2)

st.markdown("# Clustering Text")
st.markdown(
    "Let's say you've gotten a lot of feedback from clients on different channels. You might like to be able to distill main topics and get an overview. It might even inspire some intents that will be used in a virtual assistant!"
)
st.markdown(
    "This tool will help you discover them. This app will attempt to cluster whatever text you give it. The chart will try to clump text together and you can explore underlying patterns."
)

lang = SpacyLanguage("en_core_web_md")
if st.button("Plot cluster"):
    emb = EmbeddingSet(*[lang[t] for t in texts])
    p = (
        emb.transform(reduction)
        .plot_interactive(annot=False)
        .properties(width=500, height=500, title="")
    )

    st.write(p, use_container_width=True)
