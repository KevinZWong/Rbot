from typing import Text
from scrapeRedditOOP import ScrapReddit
from TextToVoiceOOP import TextToVoice
from moviePyOOP import VideoGenerator
import praw
import json
from datetime import date
from datetime import datetime
import time
class Rbot:
    def __init__(self):
        pass

    def ScrapeData(self, SubRedditName, NumPosts):
        DataFileName = "Reddit_" + SubRedditName + "_Data.json"
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


RedditData = Rbot()

SubRedditName = "TrueOffMyChest"
NumPosts = 2

# data = [ ["title", "story"] , ["title", "story"] ]
data = RedditData.ScrapeData(SubRedditName, NumPosts)

script = []
for i in range(1, len(data)):
    script.append(data[i][0]) # appending title as an element
    wordsList = data[i][1].split()
    counter = 0
    AppendList = []
    for j,v in enumerate(wordsList):
        AppendList.append(v)
        if counter == 10 or j == len(wordsList)-1:
            
            appendStr = ""
            for x in AppendList:
                appendStr += x + " "  
            print("appendStr", appendStr)
            script.append(appendStr)
            AppendList = []
            appendStr = ""

            counter = 0
        counter += 1
    print("script", script)


    for j,v in enumerate(script):
        TextToVoice1 = TextToVoice()
        VideoGenerator1 = VideoGenerator()
        VideoGenerator1.imageFromText(v,  "image"+ str(i) +"_"+ str(j))
        TextToVoice1.convert_T2V( v, "script"+ str(i) +"_"+ str(j))
    





















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