# To-Do: Make Docker Builds Multi-Platform
# Base Stage - Buster-Slim is used as a base image
FROM python:3.8-slim AS base

# Update base image. It might be helpful for security reasons 
RUN apt-get update -qq && \
    apt-get upgrade -qq -y && \
    apt-get autoremove -y -qq && \
    apt-get autoclean -y -qq

# Build stage
FROM base AS build-stage
# install build-essential for compiling sources
RUN apt-get install -qq -y build-essential
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

# Copy chitchat_core config files from the host
# Download blenderbot model weights
RUN python -c 'from transformers import pipeline; \
model_name="ahotrod/albert_xxlargev1_squad2_512"; \
model = model_name; \
tokenizer = model_name'

# Runtime stage
FROM base AS runtime-stage
# Copy installed libraries and blenderbot server from the build stage 
COPY --from=build-stage /opt/venv /opt/venv
COPY --from=build-stage /root/.cache/huggingface /root/.cache/huggingface/
COPY qa_core ./qa_core

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /qa_core 

VOLUME /tmp
# Expose 5000 port for api 
EXPOSE 5000
# Create logs. And set an API enabled
ENTRYPOINT ["python"]
# Run container with your token and command
CMD [ "rest-api.py" ] 
