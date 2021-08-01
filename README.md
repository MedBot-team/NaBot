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

### **Genrate token**
1. Generate token for requests authentication. You can do this manually or use urandom device file.
```
echo TOKEN=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20) > production/.env
```
Check your token:
```
$ cat production/.env
TOKEN=SOME_RANDOM_STRING
```

### **Choose your Dockerfile**

2. Copy your desired Dockerfile from docker directory. Default Dockerfile is Dockerfile-Slim.
```
cp production/rasa-server/docker/Dockerfile-Rasa production/rasa-server/Dockerfile
cp production/action-server/docker/Dockerfile-Rasa production/action-server/Dockerfile
```

### **Build an image**

3. Build a *rasa chatbot and action server* images

```
docker-compose -f production/docker-compose.yml build
```

### **Make containers and run images**

4. Run *docker-compose* to start and run the chatbot and its actions together in an isolated environment
```
docker-compose -f production/docker-compose.yml up -d
```

5. Test your chatbot
```
curl --location --request POST 'http://localhost:5005/webhooks/rest/webhook' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message" : "Can you give me dosage information of Abilify?",
    "sender" : "default"
}'
```
Debug your model. (Use your token instead of SOME_RANDOM_STRING)
```
curl --location --request POST 'http://localhost:5005/model/parse?token=SOME_RANDOM_STRING' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text" : "Can you give me dosage information of Abilify?"
}'
```
Or you can use following command. (Again you should use your token instead of SOME_RANDOM_STRING)
```
curl --location --request GET 'localhost:5005/conversations/default/tracker?token=SOME_RANDOM_STRING' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text" : "Can you give me dosage information of Abilify?"
}'
```

### **Monitor the chatbot**

6. Check for errors and warnings in logs
```
docker-compose -f production/docker-compose.yml logs -f -t
```

7. Monitor a live stream of containers resource usage statistics
```
docker stats
```

---

## In removing the chatbot case

8. Stop and remove chatbot containers
```
docker-compose -f production/docker-compose.yml down
```
