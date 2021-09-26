from decouple import config
from flask import Flask, jsonify, request
from utils import ChitChat


app = Flask(__name__)
# Read API_KEY from .env file
api_key = config('CHITCHAT_API_KEY')
chitchat_log = config('CHITCHAT_LOG')


if chitchat_log:
    postgres_user = config('POSTGRES_USER')
    postgres_password = config('POSTGRES_EVENTS_PASSWORD')
    postgres_host = config('EVENTS_DB_HOST')
    postgres_port = config('POSTGRES_PORT')
    postgres_database = config('POSTGRES_EVENTS_DATABASE')

    chitchat = ChitChat(postgres_user=postgres_user,
                        postgres_password=postgres_password,
                        postgres_host=postgres_host,
                        postgres_port=postgres_port,
                        postgres_database=postgres_database)
else:
    chitchat = ChitChat()


# Default model
model_name = 'facebook/blenderbot-400M-distill'
chitchat.model_init(model_name=model_name)

# Send requests with HTTP POST method for changeing model
@app.route('/model', methods=['POST'])
def ChModel():
    # Check if proper data has been send to chitchat server
    if not set(['model', 'api_key']) <= request.json.keys():
        return jsonify(code=403, message="bad request")
    # Check if request has been sent with the right api_key
    elif request.json['api_key'] != api_key:
        return jsonify(code=403, message="bad request")
    # Check if the right model name has been used
    elif request.json['model'] not in chitchat.available_model():
        return jsonify(code=403, message="bad request")
    # Change default model to which user asked
    else:
        model_name = request.json['model']
        chitchat.model_init(model_name=model_name)
        return "Model has been changed successfully!"


# Send requests with HTTP POST method for chitchat
@app.route('/', methods=['POST'])
def ChitChat():
    # Check if proper data has been send to chitchat server
    if not set(['utterance', 'api_key']) <= request.json.keys():
        return jsonify(code=403, message="bad request")
    # Check if request has been sent with the right api_key
    elif request.json['api_key'] != api_key:
        return jsonify(code=403, message="bad request")
    # Get the reply from model according to the utterance
    else:
        utterance = request.json['utterance']
        reply = chitchat.get_reply(utterance=utterance)

        if chitchat_log:
            table_name = 'chitchat'
            chitchat.createdb(table_name)
            chitchat.updatedb(table_name, utterance, reply)

        return jsonify(reply=reply)


# Run flask APP in production mode
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
