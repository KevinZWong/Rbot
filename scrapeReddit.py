import praw
 
reddit_read_only = praw.Reddit(client_id="1LUhfALD3uJgbBeFVFMOGQ",         # your client id
                               client_secret="46QJC2mttPTyOY7DwzlOdkP1nxYNqw",      # your client secret
                               user_agent="Rbot")        # your user agent
 
 

def removeModPost(postList):
    returnIndexs = []
    
    for i,v in enumerate(postList):
        modPost = v[0]
        modPost = list(modPost)
        first10 = ""
        try:
            for j in range(0, 10):
                first10 += modPost[j]
        except:
            pass


        if first10 == "[Mod Post]":
            pass
        else:
            returnIndexs.append(i)
    returnValues = []
    for i in returnIndexs:
        returnValues.append(postList[i])
    return returnValues






subreddit = reddit_read_only.subreddit("AskReddit")
 
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
postList = removeModPost(postList)
for i in postList:
    print("postList", i)
    print("\n\n\n\n")
