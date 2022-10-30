

def findChraceter(key_word, strGiven):
    key_wordChar = list(key_word)
    strGivenChar = list(strGiven)


    index = 0
    keywordIndex = 0
    for i in range(0, len(strGivenChar)):
        print("strGivenChar[index]", strGivenChar[index])
        print("key_wordChar[keywordIndex]", key_wordChar[keywordIndex])
        if strGivenChar[index] == key_wordChar[keywordIndex]:
            if keywordIndex + 1 == len(key_wordChar):
                return True
            else:
                keywordIndex = 0
            keywordIndex += 1
        index += 1
    return False

#print(findChraceter("the", "hithere"))




def replaceCharacters( search, replacement, wordsString): #USE WITH CAUTION
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


print(replaceCharacters("hi", "hellow", "hithere"))

            









