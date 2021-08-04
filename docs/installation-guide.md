# MedBot Installation Guide

MedBot can be installed from its source code or by docker images. 

---
## Install MedBot by docker


1. Install [docker-compose](https://docs.docker.com/compose/install/)

2. Create your token

    ```
    echo TOKEN=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20) > .env
    ```

3. Create docker-compose file:

    ```
    $ cat docker-compose.yml

    services:
    rasa:
        image: alirazmdideh/medbot_server:latest
        container_name: chatbot-server
        restart: always
        ports:
        - 5005:5005
        volumes:
        - ./logs:/rasa-server/rasa/logs
        networks:
        - rasa-netowrk
        env_file:
        - .env
        command: [$TOKEN]
    app:
        image: alirazmdideh/action_server:latest
        container_name: action-server
        restart: always
        volumes:
        - ./logs:/action-server/logs
        networks:
        - rasa-netowrk
        expose: 
        - 5055 

    networks:
    rasa-netowrk:
        driver: bridge
    ```

4. Enjoy your chatbot :wink: 

    ```
    docker-compose -f docker-compose.yml up -d
    ```

---
## Install from source code

1. Clone Rasa branch

    ```
    git clone https://github.com/arezae/chatbot --branch rasa --single-branch --depth 1
    ```

2. Directory tree

    To run the Rasa chatbot, we need to run actions-server and chatbot-server separately. So we've separated actions, datasets, and the chatbot from each other.

    Action-Server will contain actions and datasets, and Rasa-Server will contain the chatbot model and its autocorrect component. In the rest of the document, we will install requirements and then run chatbot and action servers.

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

3. Install requirements

    Create python environment

    ```
    pip install --user --upgrade pip
    pip install --user virtualenv
    python -m venv rasa_env
    ```

4. Activate your python environment

    ```
    source virtualenv/bin/activate
    ```

5. Install rasa chatbot requirements

    ```
    pip install --no-cache-dir -r production/rasa-server/requirements.txt
    ```

6. Install rasa chatbot server and actions server requirements

    ```
    pip install --no-cache-dir -r production/rasa-server/requirements.txt -r production/action-server/requirements.txt
    ```

7. Download Spacy weights 

    ```
    python -m spacy download en_core_web_md
    ```

8. Download autocorrect module dictionaries. This dictionary consists of English and medical words.

    ```
    cd production/rasa-server
    python -c "import autocorrect; autocorrect.Speller('en_med')"
    ```

9. Train rasa model :hourglass:

    ```
    cd production/rasa-server/rasa
    rasa train
    ```

10. Run rasa server 
    We are almost done. Now we can run the rasa and actions server.

    * Run the Rasa server. If you would like to run the Rasa server with tokens to authenticate requests, You can add `--auth-token YOUR_TOKEN` at the end of the following command

        ```
        cd production/rasa-server/rasa
        mkdir logs
        rasa run --log-file logs/rasa-server.log --enable-api
        ```

    * Run the action server

        ```
        cd production/action-server/actions
        mkdir logs
        rasa run --log-file logs/action-server.log actions --actions actions
        ```

11. Enjoy chatting with MedBot :hugs:

    ```
    curl --location --request POST 'http://localhost:5005/webhooks/rest/webhook' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "message" : "Can you give me dosage information of Abilify?",
        "sender" : "default"
    }'
    ```

---
## Build a Docker image

1. Clone Rasa branch

    ```
    git clone https://github.com/arezae/chatbot --branch rasa --single-branch --depth 1
    ```

2. Directory tree

    To run the Rasa chatbot, we need to run actions-server and chatbot-server separately. So we've separated actions, datasets, and chatbots from each other.

    Action-Server will contain actions and datasets, and Rasa-Server will contain the chatbot model and its autocorrect component.

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

    In the rest of the document, we will build separated images for actions and rasa and then run them together.

3. Genrate token

    * Generate token for requests authentication. You can do this manually or use the *urandom* device file.

        ```
        echo TOKEN=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20) > production/.env
        ```

    * Check your token:

        ```
        $ cat production/.env
        TOKEN=SOME_RANDOM_STRING
        ```

4. Choose your Dockerfile

    Copy your desired Dockerfile from the docker directory. Default Dockerfile is Dockerfile-Slim.

    ```
    cp production/rasa-server/docker/Dockerfile-Rasa production/rasa-server/Dockerfile
    cp production/action-server/docker/Dockerfile-Rasa production/action-server/Dockerfile
    ```

5. Build an image

    Build a *rasa chatbot and action server* images

    ```
    docker-compose -f production/docker-compose.yml build
    ```

6. Make containers and run images

    Run *docker-compose* to start and run the chatbot and its actions together in an isolated environment

    ```
    docker-compose -f production/docker-compose.yml up -d
    ```

7. Test your chatbot
    * Talk with your chatbot

        ```
        curl --location --request POST 'http://localhost:5005/webhooks/rest/webhook' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "message" : "Can you give me dosage information of Abilify?",
            "sender" : "default"
        }'
        ```

    * Debug your model. (Use your token instead of SOME_RANDOM_STRING)

        ```
        curl --location --request POST 'http://localhost:5005/model/parse?token=SOME_RANDOM_STRING' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "text" : "Can you give me dosage information of Abilify?"
        }'
        ```

    * Or you can use the following command. (Again, you should use your token instead of SOME_RANDOM_STRING)

        ```
        curl --location --request GET 'localhost:5005/conversations/default/tracker?token=SOME_RANDOM_STRING' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "text" : "Can you give me dosage information of Abilify?"
        }'
        ```

8. Monitor the chatbot

    * Check for errors and warnings in logs

        ```
        docker-compose -f production/docker-compose.yml logs -f -t
        ```

    * Monitor a live stream of containers resource usage statistics

        ```
        docker stats
        ```


9. In removing the chatbot case

    Stop and remove chatbot containers

    ```
    docker-compose -f production/docker-compose.yml down
    ```
