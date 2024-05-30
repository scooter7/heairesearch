import streamlit as st
from GoogleNews import GoogleNews
import tweepy
import json

twitter_api_key = st.secrets["twitter"]["api_key"]
twitter_api_secret = st.secrets["twitter"]["api_secret"]
twitter_access_token = st.secrets["twitter"]["access_token"]
twitter_access_token_secret = st.secrets["twitter"]["access_token_secret"]
twitter_bearer_token = st.secrets["twitter"]["bearer_token"]

client = tweepy.Client(bearer_token=twitter_bearer_token)

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
