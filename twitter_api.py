import os

# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# from selenium import webdriver

from requests_oauthlib import OAuth1Session
import json
import webbrowser
from flask import Flask, Response, render_template, request, jsonify
# import asyncio
from dotenv import load_dotenv


load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
account_name = os.getenv("ACCOUNT_NAME")
t1 = 0
t2 = 0
pin = 0


# This part is done by Yifu Fang, together with the index.html file
async def oauth_authentication1():
    # 3 steps of oauth
    # step 1: request oauth token
    global t1, t2
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    oauth_token = fetch_response.get("oauth_token")
    oauth_token_secret = fetch_response.get("oauth_token_secret")
    t1 = oauth_token
    t2 = oauth_token_secret
    # step 2: Get authorization using the oauth token
    authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(authorization_url)
    print("go to the authorize url: %s" % authorization_url)

    webbrowser.open(authorization_url)
    return


# This part is done by Jiajun Dai, together with the pytest
async def oauth_authentication2():
    oauth_token, oauth_token_secret = t1, t2
    verifier = pin
    # verifier = input("enter PIN: ")
    print(verifier)

    # step 3: Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]
    print("access token: %s" % access_token)
    print("access token secret: %s" % access_token_secret)
    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    return oauth


# -----------------python function to create tweet and delete tweet, POST and DELETE request-----------------------
# This part is done by Sarah Yu
async def create_tweet(s):
    payload = {"text": s}
    oauth = await oauth_authentication2()
    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    print(f"Response code: {response.status_code}")

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))
    # tweet_id = json_response['data']['id']
    return json_response['data']['id'], json_response, response.status_code


async def delete_tweet(tweet_id):
    oauth = await oauth_authentication2()
    response = oauth.delete("https://api.twitter.com/2/tweets/{}".format(tweet_id))
    print(f"Response code: {response.status_code}")
    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))
    return json_response, response.status_code


# ---------------------------------Python flask to interact with frontend------------------------------
# This part is done by Walton Ma
def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/authenticate', methods=['POST'])
    async def authenticate():
        await oauth_authentication1()
        print(t1, t2)
        return jsonify({'result': 'authenticated'})

    @app.route('/process_text', methods=['POST'])
    async def process_text():
        output = {
            "errors": False,
            "error_message": "",
            "id": "",
            "result": "",
        }
        text = request.json['text']
        tweet_id, response, status = await create_tweet(text)
        if 200 <= status <= 299:
            output["id"] = tweet_id
            output["result"] = f"You have created a tweet: {text} \n ID: {tweet_id}"
            webbrowser.open(f'https://twitter.com/{account_name}/status/{tweet_id}')
        else:
            output["errors"] = True
            output["error_message"] = f"status {status}"
        # return jsonify({'result': result})
        return Response(json.dumps(output), status=200)

    @app.route('/delete_tweet', methods=['DELETE'])
    async def remove_tweet():
        output = {
            "errors": False,
            "error_message": "",
            "id": "",
            "result": "",
        }
        tweet_id = request.json['text']
        response, status = await delete_tweet(tweet_id)
        if 200 <= status <= 299:
            output["result"] = f"You have deleted a tweet with an ID of: {tweet_id}"
            webbrowser.open(f'https://twitter.com/{account_name}/status/{tweet_id}')
        else:
            output["errors"] = True
            output["error_message"] = f"status {status}"
        # return jsonify({'result': result})
        return Response(json.dumps(output), status=200)

    @app.route('/get_pin', methods=['POST'])
    async def get_pin():
        global pin
        pin = request.json['text']
        result = f"You have entered pin: {pin}"
        return jsonify({'result': result})
    return app


if __name__ == '__main__':
    application = create_app()
    application.run(debug=True)
