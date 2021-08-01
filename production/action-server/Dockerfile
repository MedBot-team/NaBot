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
  
# Runtime image
FROM base AS runtime-stage

COPY --from=build-stage /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /action-server
VOLUME /tmp

COPY actions/ ./actions
COPY datasets ./datasets

RUN rasa telemetry disable
ENTRYPOINT ["rasa"]
CMD [ "run", "actions" ] 
