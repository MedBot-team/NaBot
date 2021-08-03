# Base image
FROM python:3.8-slim AS base

RUN apt-get update -qq && \
    apt-get upgrade -qq && \
    apt-get autoremove -y -qq && \
    apt-get autoclean -y -qq

# Build image
FROM base AS build-stage

WORKDIR /build
COPY requirements.txt /build

ENV PATH="/opt/venv/bin:$PATH"

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip wheel && \
    pip wheel --requirement=requirements.txt --wheel-dir=wheels && \
    pip install --no-deps wheels/*.whl && \
    rm -rf wheels *.egg-info
  
RUN python -m spacy download en_core_web_md && \
    python -m spacy link en_core_web_md en

WORKDIR /rasa-server

COPY autocorrect ./autocorrect
RUN mkdir ./autocorrect/data && \
    python -c "import autocorrect; autocorrect.Speller('en_med')"
    
COPY rasa ./rasa
WORKDIR /rasa-server/rasa 
RUN rasa telemetry disable && \
    rasa train

# Runtime image
FROM base AS runtime-stage

COPY --from=build-stage /opt/venv /opt/venv
COPY --from=build-stage /rasa-server /rasa-server

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /rasa-server/rasa 
VOLUME /tmp

EXPOSE 5005
ENTRYPOINT ["rasa", "run", "--log-file", "logs/rasa-server.log", "--enable-api", "--auth-token"]
CMD [ "YOUR TOKEN" ] 
