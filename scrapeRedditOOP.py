

class ScrapReddit:

    
    def __init__(self):
        self.Subbreddit = ""

    def set_Subreddit(self, SubReddit):
        self.Subbreddit = SubReddit
        print("in setreddit")
    def get_Subreddit(self):
        print("in getreddit")
        return self.Subbreddit
    def removePost(self, postList, target):
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

        


