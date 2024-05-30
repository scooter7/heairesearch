import streamlit as st
from GoogleNews import GoogleNews
import tweepy
import json
import requests
from requests.auth import HTTPBasicAuth

twitter_client_id = st.secrets["twitter"]["client_id"]
twitter_client_secret = st.secrets["twitter"]["client_secret"]

def get_bearer_token(client_id, client_secret):
    response = requests.post(
        "https://api.twitter.com/oauth2/token",
        auth=HTTPBasicAuth(client_id, client_secret),
        data={'grant_type': 'client_credentials'}
    )
    if response.status_code != 200:
        raise Exception(f"Cannot get a bearer token (HTTP {response.status_code}): {response.text}")
    return response.json()['access_token']

bearer_token = get_bearer_token(twitter_client_id, twitter_client_secret)

client = tweepy.Client(bearer_token=bearer_token)

linkedin_cookies = json.loads(st.secrets["linkedin"]["cookies"])

googlenews = GoogleNews()

st.title('Keyword-Based Content Fetcher')

keyword = st.text_input('Enter a keyword to search for content:', '')

if keyword:
    googlenews.search(keyword)
    google_news_stories = googlenews.results()

    tweets = client.search_recent_tweets(query=keyword, tweet_fields=['context_annotations', 'created_at'], max_results=10)

    st.header('Google News Stories')
    for article in google_news_stories:
        st.subheader(article['title'])
        st.write(article['desc'])
        st.write(f"[Read more]({article['link']})")

    st.header('Tweets')
    for tweet in tweets.data:
        st.subheader(f"@{tweet.author_id}")
        st.write(tweet.text)
