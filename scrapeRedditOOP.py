

class ScrapReddit:

    
    def __init__(self):
        self.Subbreddit = ""

    def set_Subreddit(self, SubReddit):
        self.Subbreddit = SubReddit
    def get_Subreddit(self):
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
            #print("found something")
            
            for i, v in enumerate(wordsList):
                if v == search:
                    wordsList[i] = replacement
        

        else:
            #print("No insatnce of", search, "found, returned original list" )
            return wordsString

                
        #print("wordsString: ", wordsString)
        #print("wordsList: ", wordsList)
        returnValue = ""
        for i in wordsList:
            returnValue += i
        return returnValue
    def replaceAcronyms(self, script):
        acronyms = [
            ['FU', 'fuck up'],
            ['AFAIK', 'As far as I know'],
            ['AMA', 'Ask Me Anything'],
            ['CMV', 'Change My View'],
            ['DAE', 'Does Anyone Else'],
            ['ELI5', 'Explain Like I\'m 5'],
            ['FTFY', 'Fixed That For You'],
            ['IAMA', 'I Am A'],
            ['IMO', 'In My Opinion'],
            ['ITT', 'In This Thread'],
            ['MRW', 'My Reaction When'],
            ['NSFW', 'Not Safe For Work'],
            ['OC', 'Original Content'],
            ['OP', 'Original Poster'],
            ['PSA', 'Public Service Announcement'],
            ['TIL', 'Today I Learned'],
            ['TL;DR', 'Too Long; Didn\'t Read'],
            ['TLDR', 'Too Long; Didn\'t Read'],
            ['YMMV', 'Your Mileage May Vary'],
            ['FU', 'fuck up'] 

        ]
        for i in range(0, len(acronyms)):
            script = self.replaceWords(acronyms[i][0], acronyms[i][1], script)
        return script

    def replaceCharacters(self, search, replacement, wordsString): #USE WITH CAUTION
        wordsChar = list(wordsString)
        searchChar = list(search)
        index = 0
        wordsFoundCounter = 0

        finalReturn = ""
        potential = ""
        for i,v in enumerate(wordsChar):
            if searchChar[index] == v:
                index += 1
                potential += ""
            else:
                index = 0
                finalReturn += v
            if len(searchChar) == index:
                wordsFoundCounter += 1
                finalReturn += replacement
                potential= ""
                index = 0
        return finalReturn
                


def main():  
    obj1 = ScrapReddit()
    search = "TrueOffMyChest,"
    replacement = "testing up,"
    wordsString = "TIFU, hello"
    print(obj1.replaceWords(search, replacement, wordsString))

#main()
