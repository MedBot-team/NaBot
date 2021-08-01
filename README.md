# Rasa Medical Chatbot

## Installation guide

### **Clone Rasa branch**
```
git clone https://github.com/arezae/chatbot --branch rasa --single-branch --depth 1
```

### **Directory tree**

To run Rasa chatbot we need to run actions-server and chatbot-server separately. So we've seperated actions, datasets and chatbot from each other.

Action-Server will contain actions and datasets and Rasa-Server will contain chatbot model and its autocorrect component.

```
production/
├── action-server
│   ├── actions
│   ├── datasets
│   └── docker
└── rasa-server
    ├── autocorrect
    │   └── data
    ├── docker
    └── rasa
        ├── data
        ├── models
        └── tests
```
In the rest of document, we're going to build seperated images for actions and rasa and then run them together.

### **Choose your Dockerfile**

1. Copy your desired Dockerfile from docker directory. Default Dockerfile is Dockerfile-Slim.
```
cp production/rasa-server/docker/Dockerfile-Rasa production/rasa-server/Dockerfile
cp production/action-server/docker/Dockerfile-Rasa production/action-server/Dockerfile
```

### **Build an image**

2. Build a *rasa chatbot and action server* images

```
docker-compose -f production/docker-compose.yml build
```

### **Make containers and run images**

3. Run *docker-compose* to start and run the chatbot and its actions together in an isolated environment
```
docker-compose -f production/docker-compose.yml up -d --no-build
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



### **Monitor the chatbot**

5. Check for errors and warnings in logs
```
docker-compose -f production/docker-compose.yml logs -f -t
```

6. Monitor a live stream of containers resource usage statistics
```
docker stats
```

---

## In removing the chatbot case

7. Stop and remove chatbot containers
```
docker-compose -f production/docker-compose.yml down
```
