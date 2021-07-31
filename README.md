# Rasa Medical Chatbot

1. Build a *rasa chatbot* image

```
docker build -t rasa-server production/rasa-server/
```

2. Build an *action server* image 

```
docker build -t action-server production/action-server/
```

3. Run *docker-compose* to start and run the chatbot and its actions together in an isolated environment
```
docker-compose -f production/docker-compose.yml up -d
```

4. Test your chatbot
```
curl --location --request POST 'http://localhost:5005/webhooks/rest/webhook' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message" : "Can you give me dosage information of abilify?",
    "sender" : "default"
}'
```

5. Check for errors and warnings in logs
```
docker-compose -f production/docker-compose.yml logs -f -t
```

6. Monitor a live stream of containers resource usage statistics
```
docker stats
```

7. Stop and remove chatbot containers
```
docker-compose -f production/docker-compose.yml down
```
