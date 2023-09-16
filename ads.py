from requests_oauthlib import OAuth1Session
import json
import webbrowser
from flask import Flask, render_template, request, jsonify
consumer_key = 'pWCBijvKjZijuZIt5G0i7gGjS'
consumer_secret = 'yO7dD0j4KhHkn6LD2wAkkkI69Wo2K4A9KM80NCwpkXYrJ0FJMy'

def oauth_authentication():
    # 3 steps of oauth
    # step 1: request oauth token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    print(fetch_response)
    oauth_token = fetch_response.get("oauth_token")
    oauth_token_secret = fetch_response.get("oauth_token_secret")

    # step 2: Get authorization using the oauth token
    authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(authorization_url)
    print("go to the authorize url: %s" % authorization_url)
    webbrowser.open(authorization_url)
    verifier = input("input the PIN: ")

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

def createTweet(str):
    payload = {"text": str}
    oauth = oauth_authentication()
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

def deleteTweet(id):
    oauth = oauth_authentication()
    response = oauth.delete("https://api.twitter.com/2/tweets/{}".format(id))
    print(f"Response code: {response.status_code}" )
    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

##Python flask to interact with frontend
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.json['text']
    id = createTweet(text)
    result = f"You have created a tweet: {text} \n ID: {id}"
    webbrowser.open(f'https://twitter.com/SjsuF31335/status/{id}')
    return jsonify({'result': result})

@app.route('/delete_tweet', methods=['DELETE'])
def delete_tweet():
    text = request.json['text']
    deleteTweet(text)
    result = f"You have deleted a tweet: with an ID of: {text}"
    webbrowser.open(f'https://twitter.com/SjsuF31335/status/{text}')
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)