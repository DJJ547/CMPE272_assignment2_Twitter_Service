from requests_oauthlib import OAuth1Session
import json
import webbrowser
from flask import Flask, render_template, request, jsonify
import asyncio

with open('credential.json', 'r') as file:
    credentials = json.load(file)

consumer_key = credentials["CONSUMER_KEY"]
consumer_secret = credentials["CONSUMER_SECRET"]
# access_token = credentials["ACCESS_TOKEN"]
# access_token_secret = credentials["ACCESS_TOKEN_SECRET"]

t1 = 0
t2 = 0
pin = 0


async def oauth_authentication1():
    # 3 steps of oauth
    # step 1: request oauth token
    global t1,t2
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

async def oauth_authentication2():
    oauth_token, oauth_token_secret =t1, t2
    verifier = pin
    ##verifier = input("enter PIN: ")
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
    print("access token: %s" %access_token)
    print("access token secret: %s" %access_token_secret)
    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    return oauth
##----------------------------------python function to create tweet and delete tweet, POST and DELETE request--------------------------------------##
async def createTweet(str):
    payload = {"text": str}
    oauth = await oauth_authentication2()
    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    print(f"Response code: {response.status_code}" )

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))
    return json_response['data']['id']

async def deleteTweet(id):
    oauth = await oauth_authentication2()
    response = oauth.delete("https://api.twitter.com/2/tweets/{}".format(id))
    print(f"Response code: {response.status_code}" )
    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

##-------------------------------------------------Python flask to interact with frontend--------------------------------------------------------###
asyncio = Flask(__name__)
@asyncio.route('/')
def index():
    return render_template('index.html')

@asyncio.route('/authenticate', methods=['POST'])
async def authticate():
    text = request.json['text']
    await oauth_authentication1()
    print(t1, t2)
    return jsonify({'result': 'authenticated'})

@asyncio.route('/process_text', methods=['POST'])
async def process_text():
    text = request.json['text']
    id = await createTweet(text)
    result = f"You have created a tweet: {text} \n ID: {id}"
    webbrowser.open(f'https://twitter.com/SjsuF31335/status/{id}')
    return jsonify({'result': result})

@asyncio.route('/delete_tweet', methods=['DELETE'])
async def delete_tweet():
    text = request.json['text']
    await deleteTweet(text)
    result = f"You have deleted a tweet with an ID of: {text}"
    webbrowser.open(f'https://twitter.com/SjsuF31335/status/{text}')
    return jsonify({'result': result})

@asyncio.route('/get_pin', methods=['POST'])
async def get_pin():
    global pin
    pin = request.json['text']
    result = f"You have entered pin: {pin}"
    return jsonify({'result': result})

if __name__ == '__main__':
    asyncio.run(debug=True)