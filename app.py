import streamlit as st
from GoogleNews import GoogleNews
import tweepy

# Access Twitter credentials from Streamlit secrets
twitter_api_key = st.secrets["twitter"]["api_key"]
twitter_api_secret_key = st.secrets["twitter"]["api_secret_key"]
twitter_access_token = st.secrets["twitter"]["access_token"]
twitter_access_token_secret = st.secrets["twitter"]["access_token_secret"]
twitter_bearer_token = st.secrets["twitter"]["bearer_token"]
twitter_client_id = st.secrets["twitter"]["client_id"]
twitter_client_secret = st.secrets["twitter"]["client_secret"]

# Initialize Tweepy client with all credentials
client = tweepy.Client(
    bearer_token=twitter_bearer_token,
    consumer_key=twitter_api_key,
    consumer_secret=twitter_api_secret_key,
    access_token=twitter_access_token,
    access_token_secret=twitter_access_token_secret
)

googlenews = GoogleNews()

st.title('Keyword-Based Content Fetcher')

keyword = st.text_input('Enter a keyword to search for content:', '')

if keyword:
    googlenews.search(keyword)
    google_news_stories = googlenews.results()

    try:
        response = client.search_recent_tweets(query=keyword, tweet_fields=['context_annotations', 'created_at'], max_results=10)
        tweets = response.data
    except tweepy.errors.TweepyException as e:
        st.error(f"Error fetching tweets: {e}")
        if e.response:
            st.error(f"Response details: {e.response.status_code} {e.response.text}")
        raise

    st.header('Google News Stories')
    for article in google_news_stories:
        st.subheader(article['title'])
        st.write(article['desc'])
        st.write(f"[Read more]({article['link']})")

    st.header('Tweets')
    if tweets:
        for tweet in tweets:
            st.subheader(f"@{tweet.author_id}")
            st.write(tweet.text)
    else:
        st.write("No tweets found.")
