# To-Do: Make Docker Builds Multi-Platform
# Base Stage - Buster-Slim is used as a base image
FROM python:3.8-slim AS base

# Update base image. It might be helpful for security reasons 
RUN apt-get update -qq && \
    apt-get upgrade -qq -y && \
    apt-get install -qq -y gettext-base \
                default-libmysqlclient-dev && \
    apt-get autoremove -y -qq && \
    apt-get autoclean -y -qq

# Build stage
FROM base AS build-stage
# install wget for downloading model weights
RUN apt-get install -qq -y wget \
                           build-essential
# Change current directory to build
WORKDIR /build
# Copy requirements list from the host
COPY requirements.txt /build
# Activate virtual environment. 
# Download python pacakges and compile some of them
# Install binaries. and the make things clear 
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip wheel && \
    pip wheel --requirement=requirements.txt --wheel-dir=wheels && \
    pip install --no-deps wheels/*.whl && \
    rm -rf wheels *.egg-info

WORKDIR /rasa-server
# Copy rasa config files from the host
COPY rasa ./rasa
# Pass the version of model weights as an argument to the dockerfile. 
# The default value is the latest (v0.1.0) version tag.
# This version should be the same as the MedBot version you've cloned.
ARG VERSION=v0.2.0
# Download rasa model weights
RUN mkdir -p /rasa-server/rasa/models && \
    wget -q https://www.dropbox.com/s/304elqbdfptcyvl/$VERSION.tar.gz \
    -P /rasa-server/rasa/models/
# Download and extract ConveRT model weights
RUN mkdir -p /rasa-server/rasa/weights/model && \
    wget -q https://github.com/connorbrinton/polyai-models/releases/download/v1.0/model.tar.gz \
    -P /rasa-server/rasa/weights/ && \
    tar -xvzf /rasa-server/rasa/weights/model.tar.gz -C /rasa-server/rasa/weights/model && \
    rm /rasa-server/rasa/weights/model.tar.gz
# Runtime stage
FROM base AS runtime-stage
# Copy installed libraries and rasa-server from the build stage 
COPY --from=build-stage /opt/venv /opt/venv
COPY --from=build-stage /rasa-server /rasa-server

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /rasa-server/rasa 
RUN rasa telemetry disable

VOLUME /tmp
# Expose 5005 port for api 
EXPOSE 5005
# Create logs. And set an API enabled
ENTRYPOINT ["bash"]
# Run container with your token and command
CMD [ "run_rasa.sh" ] 
