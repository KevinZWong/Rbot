def replaceCharacters(search, replacement, wordsString): #USE WITH CAUTION
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

#replaceCharacters(search, replacement, wordsString)

print(replaceCharacters("hi", "apple", "123hi45hi678hi"))
print(replaceCharacters("\n", "", "123\n45\n678\n"))