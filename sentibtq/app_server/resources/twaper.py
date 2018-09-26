from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import json

#Variables that contains the user credentials to access Twitter API
#
# JrSzvu3iuEwfuR8vlk3LnziPV (API key)
#
# cbanfeBFzNvUBN8I7eV6LRNPlZbZwgJ9ICpUzFdu5edv2gnrJO (API secret key)

# 966949129271181313-PVGLRrVkg5pPKb1fC58Dk8Blymf4bOT (Access token)
#
# zPq77mbP6NpXyp3VZBhZrKB8czoHTpHaNBENLZUjdsoDg
import yaml

config = yaml.loads("confg/config.yaml")

access_token = config.get("access_token")
access_token_secret = config.get("access_token_secret")
consumer_key =  config.get("consumer_key")
consumer_secret = config.get("consumer_secret")
from watson_developer_cloud import ToneAnalyzerV3
import requests
versioni = "2017-09-21"

#This is a basic listener that just prints received tweets to stdout.
f = open("tweet_samples.txt","w")
tone_analyzer = ToneAnalyzerV3(
    version=versioni,
    username="1ca9ed3d-7558-44d8-a0e9-89d8413521a4",
    password='4Y487tNNcNDm',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)
uniq_em = {}
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        data_json = json.loads(data)
        cleaned_text = data_json.get("text")
        if cleaned_text:
            if cleaned_text.startswith("RT @"):
                cleaned_text = re.sub(r'.*:', '', cleaned_text)
                print cleaned_text
                tone_analysis = tone_analyzer.tone({'text': cleaned_text}, 'application/json').get_result()
                # print kil
                r = requests.post()
                for tone in tone_analysis.get("document_tone").get("tones"):
                    debug_string = "Score "+str(tone.get("score"))+" "+tone.get("tone_id")+" "+str(tone.get("tone_name"))
                    f.write(debug_string+"\n")
                    uniq_em[tone.get("tone_id")] = 1
                    self.post_to_kibana(debug_string)
                    print("Score "+str(tone.get("score"))+" "+tone.get("tone_id")+" "+str(tone.get("tone_name")))
        # f.write(str(data)+"\n")
        return True

    def on_error(self, status):
        print(status)

    def post_to_kibana(data):
        headers = {
            'Content-Type': 'application/x-ndjson',
        }

        params = (
            ('pretty', ''),
        )

        data = open('logs.jsonl', 'rb').read()
        response = requests.post('https://427ae6340b68467898ce65a978ffb80d.us-east-1.aws.found.io:9243/_bulk',
                                 headers=headers, params=params, data=data, verify=False,
                                 auth=('elastic', 'zlmJ5nN9oWbR2aGSrxYFgwmt'))




#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://427ae6340b68467898ce65a978ffb80d.us-east-1.aws.found.io:9243/_bulk?pretty', headers=headers, data=data, verify=False, auth=('elastic', 'zlmJ5nN9oWbR2aGSrxYFgwmt'))


def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # stream.sample()
    stream.sample()

