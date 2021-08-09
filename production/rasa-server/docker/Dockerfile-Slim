# To-Do: Make Docker Builds Multi-Platform
# Base Stage - Buster-Slim is used as a base image
FROM python:3.8-slim AS base

# Update base image. It might be helpful for security reasons 
RUN apt-get update -qq && \
    apt-get upgrade -qq -y && \
    apt-get install -qq -y curl && \
    apt-get autoremove -y -qq && \
    apt-get autoclean -y -qq

# Build stage
FROM base AS build-stage
# install wget for downloading model weights
RUN apt-get install -qq -y wget
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
# Download spacy model weights 
RUN python -m spacy download en_core_web_md && \
    python -m spacy link en_core_web_md en

WORKDIR /rasa-server
# Copy autocorrect module from the host
COPY autocorrect ./autocorrect
# Download autocorrect module dictionary
RUN mkdir -p ./autocorrect/data && \
    python -c "import autocorrect; autocorrect.Speller('en_med')"
# Copy rasa config files from the host
COPY rasa ./rasa
# Pass the version of model weights as an argument to the dockerfile. 
# The default value is the latest (v0.1.0) version tag.
# This version should be the same as the MedBot version you've cloned.
ARG VERSION=v0.1.0
# Download rasa model weights
RUN mkdir -p /rasa-server/rasa/models && \
    wget -q https://www.dropbox.com/s/u1o8s2u96lpt8cv/$VERSION.tar.gz \
    -P /rasa-server/rasa/models/

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
ENTRYPOINT ["rasa", "run", "--log-file", "logs/rasa-server.log", "--enable-api", "--auth-token"]
# Run container with your token and command
CMD [ "YOUR TOKEN" ] 
