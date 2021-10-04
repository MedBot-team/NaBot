from decouple import config
from flask import Flask, jsonify, request
from utils import Summarizer, load_conf


app = Flask(__name__)
# Read API_KEY from .env file
api_key = config('SUMMERIZER_API_KEY')


# Default model
conf = load_conf()
model_name = conf['DEFAULT_MODEL']
summ = Summarizer()
summ.model_init(model_name=model_name)


# Send requests with HTTP POST method for changeing model
@app.route('/model', methods=['POST'])
def ChModel():
    # Check if proper data has been send to Summerize server
    if not set(['model', 'api_key']) <= request.json.keys():
        return jsonify(code=403, message="bad request")
    # Check if request has been sent with the right api_key 
    elif request.json['api_key'] != api_key:
        return jsonify(code=403, message="bad request")
    # Check if the right model name has been used
    elif request.json['model'] not in summ.available_model():
        return jsonify(code=403, message="bad request")
    # Change default model to which user asked
    else:
        model_name = request.json['model']
        summ.model_init(model_name=model_name)
        return "Model has been changed successfully!"


# Send requests with HTTP POST method for summarizaition
@app.route('/', methods=['POST'])
def Summarize():
    # Check if proper data has been send to Summarize server
    if not set(['context', 'api_key']) <= request.json.keys():
        return jsonify(code=403, message="bad request")
    # Check if request has been sent with the right api_key 
    elif request.json['api_key'] != api_key:
        return jsonify(code=403, message="bad request")
    # Get the summary from model according to the context 
    else:
        context = request.json['context']
        summary = summ.get_summary(context=context)
        
        return jsonify(summary=summary, context=context, code=200)

# Run flask APP in production mode
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=9090)