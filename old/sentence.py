rawinput = "hithere"
rawinput += " "
wordList = ["hi", "there", "how", "are", "you", "doing", "it", "the", "ware", "do", "in", "is", "register"]

rawChar = list(rawinput)

testcase = ""
Sentence = []
index = 0
indexOfStart = [0]
wordBool = True

ignoreList = []

while (index != len(rawChar) - 1):
    testcase += rawinput[index]

    if testcase in wordList and not(testcase in ignoreList):
        Sentence.append(testcase)
        testcase = ""
        wordBool = True 
        indexOfStart.append(index + 1)
        ignoreList = []
    else:
        wordBool = False 
    print(len(rawinput))
    print(index)
    if (not(wordBool) and (len(rawinput) - 2 == index)):
        ignoreList.append(Sentence[(len(Sentence) - 1)])
        Sentence.pop(len(Sentence) - 1)
        indexOfStart.pop(len(indexOfStart) - 1)
        index = indexOfStart[len(indexOfStart) - 1]
        testcase = ""
    else:
        index += 1
    print(Sentence)