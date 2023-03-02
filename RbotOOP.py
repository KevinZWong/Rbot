from typing import Text
from scrapeRedditOOP import ScrapReddit
from TextToVoiceOOP import TextToVoice
from moviePyOOP import VideoGenerator
from TikTokVoiceOOP import TikTokVoice
import praw
import json
from datetime import date
from datetime import datetime
import time
import os
import glob


class Rbot:
    def __init__(self):
        pass




    def ScrapeData(self, SubRedditName, NumPosts):
        askCorrectDirectory = input("Confirm that your current directory is /Rbot/? y/n: ")
        if askCorrectDirectory == "y":
            if not(os.path.exists("ScriptFiles")):
                os.mkdir("ScriptFiles")
            if not(os.path.exists("VoiceFiles")):
                os.mkdir("VoiceFiles")
            if not(os.path.exists("ImageFiles")):
                os.mkdir("ImageFiles")
            if not(os.path.exists("VideoFiles")):
                os.mkdir("VideoFiles")
            if not(os.path.exists("FinishedVideos")):
                os.mkdir("FinishedVideos")
        else:
            print("Cahnge your file location stuppid")
            quit()


        DataFileName = "ScriptFiles\\" + "Reddit_" + SubRedditName + "_Data.json"
        reddit_read_only = praw.Reddit(client_id="1LUhfALD3uJgbBeFVFMOGQ",         # your client id
                                    client_secret="46QJC2mttPTyOY7DwzlOdkP1nxYNqw",      # your client secret
                                    user_agent="Rbot")        # your user agent
        post = ScrapReddit()
        post.set_Subreddit(SubRedditName)
        subreddit = reddit_read_only.subreddit(post.get_Subreddit())

        postList = []
        for i in subreddit.hot(limit=NumPosts):
            data = []
            data.append(i.title)
            data.append(i.selftext)
            postList.append(data)
        #print("postList", type(postList))
  
        #postList = [["[Mod Post] post0", "post0 content"],["[Breaking News] post1", "post1 content"],["post2", "post2 content"],["post3", "post3 content"],["post4", "post4 content"]]

        postList = post.removePost(postList, "[Mod Post]")
        postList = post.removePost(postList, "[Breaking News]")

        for i in range(0, len(postList)):
            postList[i][1] = post.replaceCharacters("\n", " ", postList[i][1])


        print("Created: ", DataFileName)
        with open(DataFileName, 'w') as f:
            json.dump(postList, f)

        return postList
    def filter(self, data, maxWords):
        returnList = []
        for i in data:
            split1 = i[1].split()

            if (len(split1) <= maxWords):
                returnList.append(i)
        return returnList
    def manualSelection(self, data):
        returnList = []
        for story in data:
            print(story[0])
            print(story[1])
            input1 = input("Y or N: ")
            if (input1.upper() == "Y"):
                returnList.append(story)
        return returnList
    def CreateAudioFileName(self):
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return "story_" + str(current_time) + " " + str(today) 
    def ScriptSpliterV2(self, long_string): 
        # Split the string into individual sentences
        sentences = []
        start = 0
        for i in range(len(long_string)):
            if long_string[i] in ['.', '!', '?']:
                sentences.append(long_string[start:i+1])
                start = i + 1

        # Initialize an empty list to store long sentences
        long_sentences = []

        # Initialize a variable to store the previous sentence
        prev_sentence = ''

        # Iterate over the sentences and check if they have more than 10 words
        for i in range(len(sentences)):
            sentence = sentences[i].strip()
            words = sentence.split()

            if len(words) > 30:
                # If the sentence has more than 30 words, split it in half and add each half as a separate sentence
                words_per_half = len(words) // 2
                first_half = ' '.join(words[:words_per_half])
                second_half = ' '.join(words[words_per_half:])
                long_sentences.append(first_half.strip())
                long_sentences.append(second_half.strip())
            elif len(words) > 10:
                # If the sentence has between 10 and 30 words, add it to the long sentence list
                long_sentences.append(sentence)
                if prev_sentence:
                    long_sentences[-2] += ' ' + prev_sentence.strip()
                prev_sentence = ''
            else:
                # If the sentence has fewer than 10 words, add it to the next sentence
                if i < len(sentences) - 1:
                    next_sentence = sentences[i+1].strip()
                    long_sentences.append(sentence + ' ' + next_sentence)
                    prev_sentence = ''
                else:
                    # If this is the last sentence, add it to the long sentence list
                    long_sentences.append(sentence)
                    if prev_sentence:
                        long_sentences[-1] = prev_sentence.strip() + ' ' + long_sentences[-1]
                    prev_sentence = ''

        # Remove any empty elements from the list
        long_sentences = [s for s in long_sentences if s]

        return long_sentences
    
    def audioScriptSplitter(self, long_string, maxCharCount):
        punctuation = [".", "!", "?"]
        sentences = []
        start = 0
        for i in range(len(long_string)):
            if long_string[i] in punctuation:
                sentence = long_string[start:i+1]
                if len(sentence) <= maxCharCount:
                    if sentences and len(sentences[-1]) + len(sentence) <= maxCharCount:
                        sentences[-1] += sentence
                    else:
                        sentences.append(sentence.strip())
                else:
                    temp = sentence
                    while len(temp) > maxCharCount:
                        index = temp[:maxCharCount].rfind(" ")
                        sentences.append(temp[:index].strip())
                        temp = temp[index:].strip()
                    sentences.append(temp.strip())
                start = i + 1

        if start < len(long_string):
            last_sentence = long_string[start:].strip()
            if last_sentence:
                if sentences and len(sentences[-1]) + len(last_sentence) <= maxCharCount:
                    sentences[-1] += last_sentence
                else:
                    sentences.append(last_sentence)
        return sentences
        
        

    def ScriptSpliter(self, string1, split1, MaxSegmentLen): # brain of program

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
            FinalScriptV2.pop(len(FinalScriptV2) -1)



        return FinalScriptV2
    def titleFormater(self, title, rowWordCount):
        title = title.split()
        titleWordCounter = 0
        FinalTitle = ""
        for j,v in enumerate(title):
            if titleWordCounter == rowWordCount or v == len(title)-1:
                FinalTitle += "\n"
                titleWordCounter = 0
            FinalTitle += v + " "
            titleWordCounter += 1
        return FinalTitle
    
    def ExtractSegmentStartEnd(self, regcognitionOutput, Script):
        NumWords = 0
        indexes = []
        finalList = []

        ### something wrong here rewrite
        for i in Script:
            segment = i.split()
            indexes.append(NumWords)
            NumWords += len(segment)
            indexes.append(NumWords-1)
        ### something wrong here rewrite ## trying to acesss stuff past script
        tempListIndexes = []
        flip = 1
        for i in range(0, len(indexes), 1):
            tempListIndexes.append(regcognitionOutput[indexes[i]][flip])
            if (flip == 1):
                flip = 2
            else:
                finalList.append(tempListIndexes)
                tempListIndexes= []
                flip = 1
            #finalList.append([regcognitionOutput[indexes[i-1]][1], regcognitionOutput[indexes[i]][2]])
        for i in range(0, len(finalList), 1):
            finalList[i].insert(0, Script[i])
        # finalList = [["script segment here", starttime, endtime],["script segment here", starttime, endtime]]
        return finalList