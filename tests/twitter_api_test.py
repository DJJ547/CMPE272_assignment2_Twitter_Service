import os

from dotenv import load_dotenv


load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")


def test_page(client):
    response = client.get("/")
    assert b"<title>Twitter Ads API</title>" in response.data


def test_create_tweet_unauthorized(client):
    response = client.post("/process_text", data={"text": "create a tweet without authorization"})
    assert response.status_code != 200


# unable to perform this one because twitter required the auth-PIN to be manually copy & paste
# def test_create_tweet_authorized(client):
#     response = client.post("/process_text", data={"text": "create a tweet with authorization"})

def test_delete_tweet_with_unauthorized(client):
    incorrect_id = "12345"
    response = client.delete("/delete_tweet", data={"text": incorrect_id})
    assert response.status_code != 200

# unable to perform this one because twitter required the auth-PIN to be manually copy & paste
# def test_delete_tweet_authorized(client):
#     correct_id = "12345"
#     response = client.delete("/delete_tweet", data={"text": correct_id})

