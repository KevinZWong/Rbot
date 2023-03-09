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
NumPosts = 5
# data = [ ["title", "story"] , ["title", "story"] ]
dataTemp = RedditData.ScrapeData(SubRedditName, NumPosts)
data1 = RedditData.filter(dataTemp, 1000)
data = RedditData.manualSelection(data1)

audioFilePath = "VoiceFiles\\"
imageFilePath = "ImageFiles\\"
videoFilePath = "VideoFiles\\"
FinishedPath = "FinishedVideos\\"
script = []

for i in range(0, len(data)):
    '''
    post = ScrapReddit()
    data[i][1] = post.replaceAcronyms(data[i][1])
    data[i][0] = post.replaceAcronyms(data[i][0])
    '''

    rawStory = data[i][1]
    Title = data[i][0]
    print("data: ", data)
    FinalTitle = RedditData.titleFormater(data[i][0], 5)
    script = RedditData.ScriptSpliterV2(data[i][1])
    for i in range(0, len(script), 1):
        script[i] = RedditData.titleFormater(script[i], 6)

    script.insert(0, FinalTitle)
    print(script)
    
    audioScript = RedditData.audioScriptSplitter(rawStory, 250)
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
    regcognitionOutput = VoiceRecognitition1.recognize(audioFilePath + SubRedditName + ".wav")
    audioFileLength = VideoGenerator1.getLengthAudioFile(audioFilePath + SubRedditName + ".wav")
    VideoGenerator1.generateBackgroundFootage(audioFileLength, 'C://Users//14088//Videos//ValoClips//', videoFilePath + "background.mp4")
    VideoGenerator1.cropVideo(videoFilePath + "background.mp4", videoFilePath + "backgroundCroped.mp4")
    print("regcognitionOutput: ",regcognitionOutput)
    print("script: ",script)

    StartEndTimesList = RedditData.ExtractSegmentStartEnd(regcognitionOutput, script)
    VideoGenerator1.overlay_audio_video(videoFilePath + "backgroundCroped.mp4", audioFilePath + SubRedditName + ".wav", videoFilePath + "CropedAudio.mp4", audioFileLength)
    VideoGenerator1.add_text_overlay(videoFilePath + "CropedAudio.mp4", StartEndTimesList, FinishedPath + SubRedditName + str(int(time.time())) +".mp4", )


