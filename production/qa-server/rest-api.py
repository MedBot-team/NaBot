from decouple import config
from flask import Flask, jsonify, request
from utils import QuestionAnswering


app = Flask(__name__)
# Read API_KEY from .env file
api_key = config('API_KEY')

# Default model
model_name = 'ahotrod/albert_xxlargev1_squad2_512'
qa = QuestionAnswering()
qa.model_init(model_name=model_name)


# Send requests with HTTP POST method for changeing model
@app.route('/model', methods=['POST'])
def ChModel():
    # Check if proper data has been send to QA server
    if not set(['model', 'api_key']) <= request.json.keys():
        return jsonify(code=403, message="bad request")
    # Check if request has been sent with the right api_key 
    elif request.json['api_key'] != api_key:
        return jsonify(code=403, message="bad request")
    # Check if the right model name has been used
    elif request.json['model'] not in qa.available_model():
        return jsonify(code=403, message="bad request")
    # Change default model to which user asked
    else:
        model_name = request.json['model']
        qa.model_init(model_name=model_name)
        return "Model has been changed successfully!"


# Send requests with HTTP POST method for asking question
@app.route('/', methods=['POST'])
def QuAn():
    # Check if proper data has been send to QA server
    if not set(['question', 'context', 'api_key']) <= request.json.keys():
        return jsonify(code=403, message="bad request")
    # Check if request has been sent with the right api_key 
    elif request.json['api_key'] != api_key:
        return jsonify(code=403, message="bad request")
    # Get the answer from model according to the context and question
    else:
        question = request.json['question']
        context = request.json['context']

        answer = qa.get_answer(question=question, context=context)
        return jsonify(answer=answer)

# Run flask APP in production mode
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
