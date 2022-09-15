

class ScrapReddit:
    import praw
    def __init__(self):
        self.reddit_read_only = self.praw.Reddit(client_id="1LUhfALD3uJgbBeFVFMOGQ",         # your client id
                                    client_secret="46QJC2mttPTyOY7DwzlOdkP1nxYNqw",      # your client secret
                                    user_agent="Rbot")        # your user agent
    def readSub(self, SubReddit):
        self.subreddit = self.reddit_read_only.subreddit(SubReddit)
        return self.subreddit
    def removePost(postList, target):
        returnIndexs = []
        
        for i,v in enumerate(postList):
            modPost = v[0]
            modPost = list(modPost)
            targetLen = len(target)
            search = ""
            try:
                for j in range(0, targetLen):
                    search += modPost[j]
            except:
                pass


            if search == target:
                pass
            else:
                returnIndexs.append(i)
        returnValues = []
        for i in returnIndexs:
            returnValues.append(postList[i])
        return returnValues




post = ScrapReddit()
subreddit = post.readSub("TIFU")
 
# Display the name of the Subreddit
print("Display Name:", subreddit.display_name)
 
# Display the title of the Subreddit
print("Title:", subreddit.title)
 

postList = []

for post in subreddit.hot(limit=5):
    data = []
    print(post.title, "\n")
    data.append(post.title)
    data.append(post.selftext)
    postList.append(data)

#postList = [["[Mod Post] post0", "post0 content"],["post1", "post1 content"],["post2", "post2 content"],["post3", "post3 content"],["post4", "post4 content"]]
postList = post.removePost(postList, "[Mod Post]")
postList = post.removePost(postList, "[Breaking News]")
print(postList)
