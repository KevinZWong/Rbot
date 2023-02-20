from typing import Text
from scrapeRedditOOP import ScrapReddit
from TextToVoiceOOP import TextToVoice
from moviePyOOP import VideoGenerator
from TikTokVoiceOOP import TikTokVoice
from RbotOOP import Rbot
import praw
import json
from datetime import date
from datetime import datetime
import time
import os
import glob

RedditData = Rbot()

SubRedditName = "AskReddit"
NumPosts = 1
# data = [ ["title", "story"] , ["title", "story"] ]
data = RedditData.ScrapeData(SubRedditName, NumPosts)

script = []
for i in range(0, len(data)):
    
    print("data: ", data)
    FinalTitle = RedditData.titleFormater(data[i][0], 5)
    script = RedditData.ScriptSpliter(data[i][1], ".", 20)
    displayScript = []
    for i in range(0, len(script), 1):
        script[i] = RedditData.titleFormater(script[i], 10)

    script.insert(0, FinalTitle)
    print("script:", script)

    imageNameList = []
    audiofileName = []
    #TextToVoice1 = TextToVoice()
    TikTokVoice1 = TikTokVoice()
    audioFilePath = "VoiceFiles\\"
    imageFilePath = "ImageFiles\\"
    videoFilePath = "VideoFiles\\"

    VideoGenerator1 = VideoGenerator()
    for j,v in enumerate(script):


        imageNameList.append("image"+ str(i) +"_"+ str(j))
        audiofileName.append("script"+ str(i) +"_"+ str(j))
        VideoGenerator1.imageFromText(v,  "image"+ str(i) +"_"+ str(j))
        #def convert_T2V(self, text, filename)
        #TextToVoice1.convert_T2V( v, "script"+ str(i) +"_"+ str(j))
        TikTokVoice1.setName(audioFilePath + "script"+ str(i) +"_"+ str(j) + ".mp3")
        TikTokVoice1.setText(v)
        TikTokVoice1.GenerateMP3()
        #VideoGenerator1.monoToStereo(audioFilePath + "script"+ str(i) +"_"+ str(j) + ".mp3")
     


    videoFilesList = []
    for j in range(0, len(imageNameList)):
        videoFilesList.append(videoFilePath + "video"+ str(j) + ".mp4")
        VideoGenerator1.add_static_image_to_audio( imageFilePath + imageNameList[j] + ".png", audioFilePath + audiofileName[j] + ".mp3", videoFilePath + "video"+ str(j) + ".mp4")
        

    VideoGenerator1.conbineAllVideos(videoFilesList, "FinishedVideos_tiktok\\tiktok" + str(i+1) + ".mp4")
    # PRUGE ALL FILES CREATED

    files = glob.glob('VideoFiles\\*')
    for f in files:
        os.remove(f)
    files = glob.glob('VoiceFiles\\*')
    for f in files:
        os.remove(f)
    files = glob.glob('ImageFiles\\*')
    for f in files:
        os.remove(f)




'''
for i in range(0, len(data)):
    time.sleep(1)
    TextToVoice1 = TextToVoice()
    AudioFileName = RedditData.CreateAudioFileName()
    print("Created", AudioFileName)
    TextToVoice1.convert_T2V( data[i][1], AudioFileName)

'''





















#print(data)


''' 
# Display the name of the Subreddit
print("Display Name:", subreddit.display_name)
 
# Display the title of the Subreddit
print("Title:", subreddit.title)
 
'''



'''
postList = [["[Mod Post] post0", "post0 content"],["post1", "post1 content"],["post2", "post2 content"],["post3", "post3 content"],["post4", "post4 content"]]

postList = post.removePost(postList, "[Mod Post]")
print(postList)
'''