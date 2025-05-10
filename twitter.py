import tweepy
import json

# Set your Twitter API credentials
api_key = 'qWu1HyNvzQj7Nq2lnsBhl14XN'
api_secret_key = 'DL5WMMyAH3W1VZzvjUsLAUh3jy3S6k8g8LDrGDaNb7LmiD19Id'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAEjAzAEAAAAACCFZoyuudn9rV7K12SQsjn51DtI%3DzUIo8RzK3WmMDRs3EbvDtNxHm9Et1hBs3PGq1uqHNfDn0ZJKOE'

# Authenticate using Tweepy v2 API
client = tweepy.Client(bearer_token=bearer_token)

# Define search query
search_query = 'Super Bowl ad OR Super Bowl commercial -is:retweet'

# Fetch tweets
response = client.search_recent_tweets(query=search_query, max_results=100, tweet_fields=['text'])

# Extract tweet texts
tweet_texts = [tweet.text for tweet in response.data] if response.data else []

# Save tweets to a JSON file
with open('Twitter_comments.json', 'w') as file:
    json.dump(tweet_texts, file, indent=4)

print(f'Saved {len(tweet_texts)} tweets to Twitter_comments.json')
