# Base Stage - Buster-Slim is used as a base image
FROM python:3.8-slim AS base

# Update base image. It might be helpful for security reasons 
RUN apt-get update -qq && \
    apt-get upgrade -qq -y && \
    apt-get install -qq -y libpq-dev && \
    apt-get autoremove -qq -y && \
    apt-get autoclean -qq -y

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

# Runtime stage
FROM base AS runtime-stage
# Copy installed libraries from the build stage
COPY --from=build-stage /opt/venv /opt/venv

COPY qa_server /qa_server
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /qa_server
# Create temp path
VOLUME /tmp
# Expose 9095 port for api 
EXPOSE 9095
# Run 
ENTRYPOINT ["python"]
CMD [ "rest-api.py" ] 
