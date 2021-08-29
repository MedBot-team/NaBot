from decouple import config
from flask import Flask, jsonify, request
from utils import QuestionAnswering

app = Flask(__name__)
api_key = config('API_KEY')
model_name = 'bert-large-cased-whole-word-masking-finetuned-squad'

qa = QuestionAnswering()
qa.model_init(model_name=model_name)


@app.route('/', methods=['POST'])
def QuAn():
    if not set(['question', 'context', 'api_key']) <= request.json.keys():
        return jsonify(code=403, message="bad request")
    elif request.json['api_key'] != api_key:
        return jsonify(code=403, message="bad request")
    else:
        question = request.json['question']
        context = request.json['context']

        answer = qa.get_answer(question=question, context=context)
        return jsonify(answer=answer)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
