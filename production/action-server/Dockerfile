FROM python:3.8-slim

WORKDIR /action-server

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY actions/ ./actions
COPY datasets ./datasets

CMD [ "rasa", "run", "actions" ] 
