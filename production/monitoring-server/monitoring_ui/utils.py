import json
import spacy
import requests
import altair as alt
from spacy import displacy
from spacy.tokens import Doc


def create_displacy_chart(tokens, entities):
    nlp = spacy.blank("en")
    doc = Doc(nlp.vocab, words=tokens, spaces=[True for _ in tokens])

    taken = []
    conf = 0
    for ent in entities:
        label = ""
        if (ent["start"], ent["end"]) not in taken:
            if ent["extractor"] == "DIETClassifier":
                conf = ent["confidence_entity"]

            if conf != 0:
                label = ent["entity"] + " " + f"({str(round(conf, 2))})"
            else:
                label = ent["entity"]
            
            span = doc.char_span(ent["start"], ent["end"], label=label)
            doc.ents = list(doc.ents) + [span]
            taken.append((ent["start"], ent["end"]))

    return displacy.render(doc, style="ent")


def create_altair_chart(dataf):
    return (
        alt.Chart(dataf)
        .mark_bar()
        .encode(
            y="name:N",
            x="confidence:Q",
            tooltip=["name", "confidence"],
        )
    )


def get_api(question: str, token: str) -> dict:
    reqUrl = f"https://api.nabot.ml/model/parse?token={token}"
    
    payload = json.dumps({
        "text": question
    })

    response = requests.request("POST", reqUrl, data=payload)
    answer = json.loads(response.text)

    return answer