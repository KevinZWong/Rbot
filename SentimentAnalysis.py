from textblob import TextBlob
text = "I hate this stupid car"
blob = TextBlob(text)
polarity_score = blob.sentiment.polarity
subjectivity_score = blob.sentiment.subjectivity
#The polarity score is a value between -1 and 1 that indicates the sentiment of the text, 
# with negative values indicating negative sentiment, positive values indicating positive sentiment, 
# and a score of 0 indicating neutral sentiment.
print("polarity_score", polarity_score)

# how opionionated a text is
print("subjectivity_score", subjectivity_score)