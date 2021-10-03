import requests
import json
from decouple import config
from flask import Flask, render_template, request

rasa_url = config('RASA_SERVER_URL')
chitchat_url = config('CHITCHAT_SERVER_URL')
chitchat_api_key = config('CHITCHAT_API_KEY')
headers = {
                'Content-Type': 'application/json'
            }

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    t = request.args.get('chat_type')
    user_text = request.args.get('msg')
    if t=='false':
        payload = json.dumps({
                    "message": f"{user_text}",
                    "sender": f"me"
                })
        response = requests.request(
                    "POST", rasa_url, headers=headers, data=payload)
        return response.json()[0]['text'].replace('\n', '<br>')
    else:
        payload = json.dumps({
                    "utterance": f"{user_text}",
                    "api_key":chitchat_api_key
                })
        response = requests.request(
                    "POST", chitchat_url, headers=headers, data=payload)
        return response.json()['reply'].replace('\n', '<br>')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=8501)