

class ScrapReddit:
    def __init__(self):
        pass
    
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

                
        print("wordsString: ", wordsString)
        print("wordsList: ", wordsList)
        
obj1 = ScrapReddit()
search = "hi"
replacement = "hithere"
wordsString = "hi, dsjad hi hihi"
obj1.replaceWords(search, replacement, wordsString)
