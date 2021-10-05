# Base Stage - Buster-Slim is used as a base image
FROM python:3.8-slim AS base

# Update base image. It might be helpful for security reasons 
RUN apt-get update -qq && \
    apt-get upgrade -qq -y && \
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
# Copy installed libraries from the build stage
COPY --from=build-stage /opt/venv /opt/venv

COPY retriever_core /retriever_core
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /retriever_core
# Create temp path
VOLUME /tmp
# create db dir for FAISS index
RUN mkdir db
# Expose 9095 port for api 
EXPOSE 9595
# Run 
ENTRYPOINT ["python"]
CMD [ "rest-api.py" ] 