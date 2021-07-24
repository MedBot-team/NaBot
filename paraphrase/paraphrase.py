import time
import json
import requests
from decouple import config



class wordtune():
    def __init__(self, token, draftId):
        super(wordtune, self).__init__()
        self.token = token
        self.draftId = draftId
        self.url = "https://api.wordtune.com/rewrite"

    # Generate Payload
    def payload_generator(self, inp):
        inp_len = len(inp)

        payload = json.dumps({
            "text": inp,
            "action": "REWRITE",
            "start": 0,
            "end": inp_len,
            "selection": {
                "wholeText": inp,
                "bulletText": "",
                "start": 0,
                "end": inp_len
            },
            "draftId": self.draftId,
            "emailAccount": None,
            "emailMetadata": {},
            "lookaheadIndex": 0
        })

        payload_without_whitespace = payload.replace(
            ": ", ":").replace(", ", ",")
        # Calulate content_length header
        self.content_length = str(len(payload_without_whitespace))

        return payload
    
    # Generate Headers
    def headers_generator(self):
        headers = {
            'host': 'api.wordtune.com',
            'connection': 'keep-alive',
            'content-length': self.content_length,
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'dnt': '1',
            'x-wordtune-origin': 'null',
            'x-wordtune-version': '0.0.1',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
            'content-type': 'application/json',
            'x-wordtune': '1',
            'token': self.token,
            'accept': '*/*',
            'origin': 'https://app.wordtune.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://app.wordtune.com/',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-US,en;q=0.9'
        }

        return headers

    # Performing Post HTTP request
    def requests(self, payload, headers):
        # Make delay for security reason - Account Suspension Prevention
        time.sleep(2)
        response = requests.request(
            "POST", self.url, headers=headers, data=payload)
        response_json = response.json()

        return response_json

    # Get list of suggestions
    def get_suggestion(self, response_json, inp):
        suggestion_list = []

        for suggestion in response_json['suggestions']:
            wordtune_changedText = suggestion[0]
            changedText_start = suggestion[1][0]
            changedText_end = suggestion[1][1]
            rephrased = inp[0:changedText_start] + \
                wordtune_changedText + inp[changedText_end:-1]
            suggestion_list.append(rephrased)

        return suggestion_list


def main():
    # environmental variables must be in .env file in the same dir as this file
    token = config('TOKEN')
    draftId = config('DRAFTID')
    paraphrase = wordtune(token, draftId)
    
    inps = ['How are you?', 'How should I take Acetaminophen?']
    for inp in inps:
        payload = paraphrase.payload_generator(inp)
        headers = paraphrase.headers_generator()
        response = paraphrase.requests(payload, headers)
        suggestion_list = paraphrase.get_suggestion(response, inp)
        print(suggestion_list)


if __name__ == '__main__':
    main()
