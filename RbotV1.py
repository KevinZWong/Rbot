from typing import Text
from scrapeRedditOOP import ScrapReddit
from TextToVoiceOOP import TextToVoice
import praw
import json
from datetime import date
from datetime import datetime

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

        with open(DataFileName, 'w') as f:
            json.dump(postList, f)

        return postList


RedditData = Rbot()

SubRedditName = "TIFU"
NumPosts = 1

# data = [ ["title", "story"] , ["title", "story"] ]
data = RedditData.ScrapeData(SubRedditName, NumPosts)

TextToVoice1 = TextToVoice()

print(TextToVoice1.getRate() )
today = date.today()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

TextToVoice1.convert_T2V( data[0][1], "story_" + str(current_time) + " " + str(today) )


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