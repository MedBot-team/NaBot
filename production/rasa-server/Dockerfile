FROM python:3.8-slim

WORKDIR /rasa-server

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_md

COPY autocorrect ./autocorrect
RUN python -c "import autocorrect; autocorrect.Speller('en_med')"

COPY rasa ./rasa
WORKDIR /rasa-server/rasa 

RUN rasa telemetry disable
RUN rasa train

CMD [ "rasa", "run", "--enable-api" ] 
