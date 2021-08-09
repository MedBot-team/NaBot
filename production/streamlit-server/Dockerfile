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

# Runtime stage
FROM base AS runtime-stage
# Copy installed libraries and streamlit server codes
COPY --from=build-stage /opt/venv /opt/venv

COPY streamlit /streamlit
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /streamlit
# Create temp path
VOLUME /tmp
# Expose 8501 port for api 
EXPOSE 8501
# Create logs. And set an API enabled
ENTRYPOINT ["streamlit", "run"]
# Run container with your token and command
CMD [ "medbot_ui.py" ] 
