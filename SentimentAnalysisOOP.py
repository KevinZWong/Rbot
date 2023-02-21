
from textblob import TextBlob

class SentimentAnalysis:
    def __init__(self):
        pass
    def getPolarityScore(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity
    def getSubjectivityScore(self, text):
        blob = TextBlob(text)
        return blob.sentiment.subjectivity
'''    
SentimentAnalysis1 = SentimentAnalysis()
print(SentimentAnalysis1.getPolarityScore("I love dogs"))
'''

