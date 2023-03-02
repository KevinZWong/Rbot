from typing import Text
from scrapeRedditOOP import ScrapReddit
from TextToVoiceOOP import TextToVoice
from moviePyOOP import VideoGenerator
from TikTokVoiceOOP import TikTokVoice
from VoiceRecognititionOOP import VoiceRecognitition
from RbotOOP import Rbot
import praw
import json
from datetime import date
from datetime import datetime
import time
import os
import glob



RedditData = Rbot()

SubRedditName = "AmItheAsshole"
NumPosts = 1
# data = [ ["title", "story"] , ["title", "story"] ]
data = RedditData.ScrapeData(SubRedditName, NumPosts)
input1 = 1
while (input1 != 0): 
    print("1. add to queue")
    print("2. remove Story")
    print("3. display")

    input1 = int(input("Type a number: "))
    if (input1 == 1):
        tempData = RedditData.ScrapeData(SubRedditName, NumPosts)
        print(tempData)
        input2 = input("Yes, Skip, End")
        
    print(data[len(data)-1])
