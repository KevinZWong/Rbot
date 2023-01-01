string1 = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 25 26 27 28 29 30 31 32 33 34 35. we w e qwe qwe qwe wq eqw e qw e qw e qw e qw e qw e qw e qw e qw e qweqw e wqe qw 36 37 28 39 40"

split1 = "."

def ScriptSpliter(string1, split1, MaxSegmentLen): # brain of program

    listSentences = string1.split(split1)

    

    for i in range(0, len(listSentences),1):
        listSentences[i] = listSentences[i] + "."

    WordsNestedList = []
    for i in listSentences:
        WordsNestedList.append(i.split())
        


    
    FinalScript = []
    counter1 = 0
    for i in range(0,len(WordsNestedList)):
        if (len(WordsNestedList[i]) >= MaxSegmentLen * 2):
            tempList = []
            while(len(WordsNestedList[i]) >= MaxSegmentLen * 2):
                for j in range(0, MaxSegmentLen, 1):
                    tempList.append(WordsNestedList[i][0])
                    WordsNestedList[i].pop(0)
                FinalScript.append(tempList)
            FinalScript.append(WordsNestedList[i])
        else:
            FinalScript.append(WordsNestedList[i])
        FinalScriptV2 = [] 
        for i in FinalScript:
            temp1 = ""
            for j in i:
                temp1 += j + " "
            FinalScriptV2.append(temp1)


    return FinalScriptV2
print(ScriptSpliter(string1, split1, 15))
        

'''
if counter1 == 20:


counter1 += 1

    if (len(innerList) >= 30):
        tempList = []
        while(len(innerList) >= 30):
            for i in range(0, 15, 1):

            FinalScript.append(tempList)
    else:
        FinalScript.append(i)  

'''






