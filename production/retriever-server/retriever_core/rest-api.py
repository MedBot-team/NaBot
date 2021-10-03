from decouple import config
from flask import Flask, jsonify, request
from utils import store_document, read_csv, DensePassage

app = Flask(__name__)
# .env variables
api_key: str = config("REST_API_KEY")
csv_file: str = config("CSV_PATH")
# Default models
query_model: str = config("QUERY_DEFAULT_MODEL")
passage_model: str = config("PASSAGE_DEFAULT_MODEL")

# read csv dataset
dataset = read_csv(csv_file)
# dataset to Document form
documents = store_document(dataset)


retriever = DensePassage()

retriever.go(documents, query_model, passage_model)


# Send requests with HTTP POST method for changeing model
@app.route('/model', methods=['POST'])
def change_model():
    # Check data send completely
    if not set(["query_model", "passage_model", 'api_key']) <= request.json.keys():
        return jsonify(code=403, message="bad request")
    # validation api_key
    elif request.json['api_key'] != api_key:
        return jsonify(code=403, message="bad request")
    # Check models are correct
    elif request.json['query_model'] not in retriever.query_available_model:
        return jsonify(code=403, message="bad request")
    elif request.json["passage_model"] not in retriever.passage_available_model:
        return jsonify(code=403, message="bad request")
    # Change models to which user asked
    else:
        query_model = request.json['query_model']
        passage_model = request.json["passage_model"]
        retriever.go(documents, query_model, passage_model)
        return jsonify(code=200, message="Model has been changed successfully!")


# Send requests with HTTP POST method
@app.route('/', methods=['POST'])
def rest():
    # Check data send completely
    if not set(['query', "top_k", 'api_key']) <= request.json.keys():
        return jsonify(code=403, message="bad request")
    # validation api_key
    elif request.json['api_key'] != api_key:
        return jsonify(code=403, message="bad request")
    # Get the answer from model according to the context and question
    else:
        query = request.json["query"]
        top_k = request.json["top_k"]
        contexts = retriever.retrieve(query=query, top_k=top_k)

        return jsonify(code=200, contexts=contexts, top_k=top_k)


# Run flask APP in production mode
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
