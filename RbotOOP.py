from typing import Text
from scrapeRedditOOP import ScrapReddit
from TextToVoiceOOP import TextToVoice
from moviePyOOP import VideoGenerator
from TikTokVoiceOOP import TikTokVoice
import praw
import json
from datetime import date
from datetime import datetime
import time
import os
import glob


class Rbot:
    def __init__(self):
        pass

    def ScrapeData(self, SubRedditName, NumPosts):
        askCorrectDirectory = input("Confirm that your current directory is /Rbot/? y/n")
        if askCorrectDirectory == "y":
            if not(os.path.exists("ScriptFiles")):
                os.mkdir("ScriptFiles")
            if not(os.path.exists("VoiceFiles")):
                os.mkdir("VoiceFiles")
            if not(os.path.exists("ImageFiles")):
                os.mkdir("ImageFiles")
            if not(os.path.exists("VideoFiles")):
                os.mkdir("VideoFiles")
            if not(os.path.exists("FinishedVideos_tiktok")):
                os.mkdir("FinishedVideos_tiktok")
        else:
            print("Cahnge your file location stuppid")
            quit()


        DataFileName = "ScriptFiles\\" + "Reddit_" + SubRedditName + "_Data.json"
        reddit_read_only = praw.Reddit(client_id="1LUhfALD3uJgbBeFVFMOGQ",         # your client id
                                    client_secret="46QJC2mttPTyOY7DwzlOdkP1nxYNqw",      # your client secret
                                    user_agent="Rbot")        # your user agent
        post = ScrapReddit()
        post.set_Subreddit(SubRedditName)
        subreddit = reddit_read_only.subreddit(post.get_Subreddit())

        postList = []
        for i in subreddit.hot(limit=NumPosts):
            data = []
            data.append(i.title)
            data.append(i.selftext)
            postList.append(data)
        #print("postList", type(postList))
  
        #postList = [["[Mod Post] post0", "post0 content"],["[Breaking News] post1", "post1 content"],["post2", "post2 content"],["post3", "post3 content"],["post4", "post4 content"]]

        postList = post.removePost(postList, "[Mod Post]")
        postList = post.removePost(postList, "[Breaking News]")

        for i in range(0, len(postList)):
            postList[i][1] = post.replaceCharacters("\n", " ", postList[i][1])


        print("Created: ", DataFileName)
        with open(DataFileName, 'w') as f:
            json.dump(postList, f)

        return postList

    def CreateAudioFileName(self):
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return "story_" + str(current_time) + " " + str(today) 

    def ScriptSpliter(self, string1, split1, MaxSegmentLen): # brain of program

        listSentences = string1.split(split1)
        for i in range(0, len(listSentences),1):
            listSentences[i] = listSentences[i] + "."

        WordsNestedList = []

        for i in listSentences:
            WordsNestedList.append(i.split())
        
        FinalScript = []
        counter1 = 0
        for i in range(0,len(WordsNestedList)):
            if (len(WordsNestedList[i]) >= MaxSegmentLen * 2):
                tempList = []
                while(len(WordsNestedList[i]) >= MaxSegmentLen * 2):
                    for j in range(0, MaxSegmentLen, 1):
                        tempList.append(WordsNestedList[i][0])
                        WordsNestedList[i].pop(0)
                    FinalScript.append(tempList)
                FinalScript.append(WordsNestedList[i])
            else:
                FinalScript.append(WordsNestedList[i])  

            FinalScriptV2 = [] 
            for i in FinalScript:
                temp1 = ""
                for j in i:
                    temp1 += j + " "
                FinalScriptV2.append(temp1)
            FinalScriptV2.pop(len(FinalScriptV2) -1)

        return FinalScriptV2
    def titleFormater(self, title, rowWordCount):
        title = title.split()
        titleWordCounter = 0
        FinalTitle = ""
        for j,v in enumerate(title):
            if titleWordCounter == rowWordCount or v == len(title)-1:
                FinalTitle += "\n"
                titleWordCounter = 0
            FinalTitle += v + " "
            titleWordCounter += 1
        return FinalTitle