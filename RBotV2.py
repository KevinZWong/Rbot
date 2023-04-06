from typing import Text
from scrapeRedditOOP import ScrapReddit
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

SubRedditName = "storytime"
NumPosts = 5
# data = [ ["title", "story"] , ["title", "story"] ]

############################## COMMENT OUT FOR DEMO ##################################
'''
dataTemp = RedditData.ScrapeData(SubRedditName, NumPosts)
data1 = RedditData.filter(dataTemp, 1000)
data = RedditData.manualSelection(data1)
'''
#################################################################################
data =  [["The depressed student fails his exam", "Kevin Wong was a hard-working student who always studied diligently for his exams. He never missed a class, took copious notes, and even sought out extra tutoring from his professors. However, despite his best efforts, Kevin still managed to fail his latest exam."]]
audioFilePath = "VoiceFiles\\"
imageFilePath = "ImageFiles\\"
videoFilePath = "VideoFiles\\"
FinishedPath = "FinishedVideos\\"
script = []

for i in range(0, len(data)):
    #post script processing
    data[i][1] = RedditData.replace_acronyms(data[i][1])
    data[i][0] = RedditData.replace_acronyms(data[i][0])
    #data[i][0] = RedditData.ScriptProcessing(data[i][0])
    ############


    rawStory = data[i][1]
    Title = data[i][0]
    print("data: ", data)
    FinalTitle = RedditData.titleFormater(data[i][0], 5)
    script = RedditData.split_sentences(data[i][1])
    for i in range(0, len(script), 1):
        script[i] = RedditData.titleFormater(script[i], 6)

    script.insert(0, FinalTitle)
    print(script)
    
    audioScript = RedditData.split_sentences(rawStory)
    audioScript.insert(0, Title)
    print(audioScript)
    audioFileNames = []
    for i, v in enumerate(audioScript):
        TikTokVoice1 = TikTokVoice()
        TikTokVoice1.setName(audioFilePath + SubRedditName + str(i) + ".wav")
        audioFileNames.append(audioFilePath + SubRedditName + str(i) + ".wav")
        TikTokVoice1.setText(v)
        TikTokVoice1.GenerateMP3()
    VideoGenerator1 = VideoGenerator()
    print(audioFileNames)
    VideoGenerator1.combine_audio_files(audioFileNames, audioFilePath + SubRedditName + ".wav")
    # find which time each word is spoken
    VoiceRecognitition1 = VoiceRecognitition()
    StartEndTImes = VoiceRecognitition1.get_pauseTimes(audioScript , audioFilePath + SubRedditName + ".wav")
    #RegOutout_string = VoiceRecognitition1.regcognitionOutput_string(regcognitionOutput)
    print("checkpoint 1")
    #regcognitionOutput = RedditData.ScriptProcessing(script)
    audioFileLength = VideoGenerator1.getLengthAudioFile(audioFilePath + SubRedditName + ".wav")
    VideoGenerator1.generateBackgroundFootage(audioFileLength, 'ValoClips//', videoFilePath + "background.mp4")
    VideoGenerator1.cropVideo(videoFilePath + "background.mp4", videoFilePath + "backgroundCroped.mp4")
    #print("regcognitionOutput: ",regcognitionOutput)
    print("script: ",script)

    #StartEndTimesList = RedditData.ExtractSegmentStartEnd(regcognitionOutput, script)
    VideoGenerator1.overlay_audio_video(videoFilePath + "backgroundCroped.mp4", audioFilePath + SubRedditName + ".wav", videoFilePath + "CropedAudio.mp4", audioFileLength)
    VideoGenerator1.add_text_overlay(videoFilePath + "CropedAudio.mp4", StartEndTImes, FinishedPath + SubRedditName + str(int(time.time())) +".mp4", )


  