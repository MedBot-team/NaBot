#!/bin/bash

# Set environment variables from .env file
set -a
source .env
set +a

# Create database in mysql-server to store rasa events
python -c "import sqlalchemy;\
sqlalchemy.create_engine('mysql://${SQL_USER}:${MYSQL_ROOT_PASSWORD}@${HOST}')\
.execute('CREATE DATABASE IF NOT EXISTS ${MYSQL_EVENTS_DATABASE}')"

# Substitute environment variables into endpoints file
envsubst < endpoints.yml | tee endpoints.yml > /dev/null

# Run rasa command
rasa run --log-file logs/rasa-server.log --enable-api --auth-token ${TOKEN}
