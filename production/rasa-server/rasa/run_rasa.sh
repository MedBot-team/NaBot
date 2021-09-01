#!/bin/bash

# Set environment variables from .env file
set -a
source .env
set +a

# Create database in mysql-server to store rasa events
python -c "import sqlalchemy;\
sqlalchemy.create_engine('mysql://${SQL_USER}:${MYSQL_EVENTS_ROOT_PASSWORD}@${EVENTS_DB_HOST}?unix_socket=/var/run/mysqld/mysqld.sock')\
.execute('CREATE DATABASE IF NOT EXISTS ${MYSQL_EVENTS_DATABASE}')"

# List of files which will be modified 
declare -a files=("endpoints.yml" "credentials.yml")

# Substitute environment variables into the files
for file in "${files[@]}"; do
  # Create a temporary file. This is needed because of asynchronous property of the pipe
  tmpfile=$(mktemp)
  cp --attributes-only --preserve $file $tmpfile
  envsubst < $file > $tmpfile 
  mv $tmpfile $file
done

# Run rasa command
rasa run --log-file logs/rasa-server.log --enable-api --auth-token ${TOKEN}
