

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

    def replaceWords(self, search, replacement, wordsString):
        wordsList = wordsString.split()
        if search in wordsList:
            print("found something")
            
            for i, v in enumerate(wordsList):
                if v == search:
                    wordsList[i] = replacement
        

        else:
            print("No insatnce of", search, "found, returned original list" )
            return wordsString

                
        #print("wordsString: ", wordsString)
        #print("wordsList: ", wordsList)
        returnValue = ""
        for i in wordsList:
            returnValue += i
        return returnValue


def main():  
    obj1 = ScrapReddit()
    search = "TIFU,"
    replacement = "testing up,"
    wordsString = "TIFU, hello"
    print(obj1.replaceWords(search, replacement, wordsString))

main()
