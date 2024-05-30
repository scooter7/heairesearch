import streamlit as st
from GoogleNews import GoogleNews
import tweepy
import json

twitter_api_key = st.secrets["twitter"]["api_key"]
twitter_api_secret = st.secrets["twitter"]["api_secret"]
twitter_access_token = st.secrets["twitter"]["access_token"]
twitter_access_token_secret = st.secrets["twitter"]["access_token_secret"]

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(auth)

googlenews = GoogleNews()

st.title('Keyword-Based Content Fetcher')

keyword = st.text_input('Enter a keyword to search for content:', '')

if keyword:
    googlenews.search(keyword)
    google_news_stories = googlenews.results()

    tweets = tweepy.Cursor(twitter_api.search_tweets, q=keyword, lang='en').items(10)

    st.header('Google News Stories')
    for article in google_news_stories:
        st.subheader(article['title'])
        st.write(article['desc'])
        st.write(f"[Read more]({article['link']})")

    st.header('Tweets')
    for tweet in tweets:
        st.subheader(f"@{tweet.user.screen_name}")
        st.write(tweet.text)
