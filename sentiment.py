import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

with open('YouTube_comments.json', 'r') as file:
    data = json.load(file)

analyzer = SentimentIntensityAnalyzer()

for entry in data:
    comment = entry['comment']
    sentiment_score = analyzer.polarity_scores(comment)
    
    
    entry['sentiment_score'] = sentiment_score


with open('comments_with_sentiment.json', 'w') as file:
    json.dump(data, file, indent=4)
