import requests
import json
from decouple import config
from flask import Flask, render_template, request

url = config('RASA_SERVER_URL')
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
    user_text = request.args.get('msg')
    payload = json.dumps({
                "message": f"{user_text}",
                "sender": f"me"
            })
    response = requests.request(
                "POST", url, headers=headers, data=payload)
    
    return response.json()[0]['text'].replace('\n', '<br>')

if __name__ == "__main__":
    app.run()