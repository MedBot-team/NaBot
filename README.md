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
│   └── datasets
└── rasa-server
    ├── autocorrect
    │   └── data
    └── rasa
        ├── data
        ├── models
        └── tests
```
In the rest of document, we're going to build seperated images for actions and rasa and then run them together.


### **Build an image**

1. Build a *rasa chatbot* image

```
docker build -t rasa-server -f production/rasa-server/Dockerfile-Multistage production/rasa-server/
```

2. Build an *action server* image 

```
docker build -t action-server -f production/action-server/Dockerfile-Multistage production/action-server/
```


### **Make containers and run images**

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
