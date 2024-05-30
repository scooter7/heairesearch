import streamlit as st
from GoogleNews import GoogleNews
import tweepy
from linkedin_api import Linkedin

# Access secrets
twitter_api_key = st.secrets["twitter"]["api_key"]
twitter_api_secret = st.secrets["twitter"]["api_secret"]
twitter_access_token = st.secrets["twitter"]["access_token"]
twitter_access_token_secret = st.secrets["twitter"]["access_token_secret"]

linkedin_email = st.secrets["linkedin"]["email"]
linkedin_password = st.secrets["linkedin"]["password"]

# Twitter API setup
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(auth)

# LinkedIn API setup
linkedin_api = Linkedin(linkedin_email, linkedin_password)

# GoogleNews setup
googlenews = GoogleNews()

# Streamlit app
st.title('Keyword-Based Content Fetcher')

keyword = st.text_input('Enter a keyword to search for content:', '')

if keyword:
    # Fetch news stories from GoogleNews
    googlenews.search(keyword)
    google_news_stories = googlenews.results()

    # Fetch tweets
    tweets = tweepy.Cursor(twitter_api.search_tweets, q=keyword, lang='en').items(10)

    # Fetch LinkedIn posts (example, may require custom API implementation)
    linkedin_posts = linkedin_api.search_posts(keyword)

    st.header('Google News Stories')
    for article in google_news_stories:
        st.subheader(article['title'])
        st.write(article['desc'])
        st.write(f"[Read more]({article['link']})")

    st.header('Tweets')
    for tweet in tweets:
        st.subheader(f"@{tweet.user.screen_name}")
        st.write(tweet.text)

    st.header('LinkedIn Posts')
    for post in linkedin_posts:
        st.subheader(post['title'])
        st.write(post['description'])
        st.write(f"[Read more]({post['url']})")
