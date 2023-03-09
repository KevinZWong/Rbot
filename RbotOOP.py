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
        for i in range(0, len(Script)):
            segment = Script[i].split()
            indexes.append(NumWords)
            NumWords += len(segment)
            indexes.append(NumWords-1)
        ### something wrong here rewrite ## trying to acesss stuff past script
        print(indexes)

        tempListIndexes = []
        flip = 1
        for i in range(0, len(indexes)-1, 1):
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
if __name__ == "__main__":
    regcognitionOutput = [['ada', 0.21, 0.478288], ['for', 0.478288, 0.72], ['leaving', 0.72, 1.14], ['my', 1.14, 1.32], ['sister', 1.32, 1.89],
                         ['in', 1.95, 2.1], ['europe', 2.1, 2.55], ['after', 2.58, 3.0], ['she', 3.0, 3.24], ['disrespected', 3.245742, 4.11],
                         ['the', 4.11, 4.23], ['local', 4.23, 4.68], ['customs', 4.68, 5.34], ['my', 5.58, 5.79], ['twenty', 5.79, 6.12],
                         ['one', 6.12, 6.36], ['meter', 6.36, 6.66], ['sister', 6.66, 7.11], ['eighteen', 7.11, 7.53], ['f', 7.53, 7.77],
                         ['and', 7.77, 7.89], ['i', 7.89, 8.01], ['had', 8.01, 8.19], ['been', 8.19, 8.37], ['planning', 8.37, 8.76],
                         ['this', 8.76, 8.97], ['trip', 8.97, 9.24], ['to', 9.24, 9.36], ['france', 9.36, 9.72], ['for', 9.72, 9.87],
                         ['years', 9.87, 10.26], ["we've", 10.83, 11.07], ['both', 11.07, 11.37], ['been', 11.37, 11.52], ['saving', 11.52, 11.94],
                         ['up', 11.94, 12.06], ['for', 12.06, 12.21], ['years', 12.21, 12.51], ['to', 12.51, 12.63], ['get', 12.63, 12.81],
                         ['the', 12.81, 12.9], ['money', 12.9, 13.26], ['and', 13.62, 13.77], ['we', 13.77, 13.89], ['went', 13.89, 14.1], 
                         ['for', 14.1, 14.25], ['winter', 14.25, 14.58], ['break', 14.58, 14.88], ['a', 14.88, 14.91], ['few', 14.91, 15.12],
                         ['months', 15.12, 15.36], ['ago', 15.36, 15.69], ['we', 15.96, 16.14], ['were', 16.14, 16.32], ['really', 16.32, 16.68],
                         ['exited', 16.68, 17.07], ['to', 17.07, 17.16], ['see', 17.16, 17.37], ['all', 17.37, 17.52], ['the', 17.52, 17.64],
                         ['sites', 17.64, 18.12], ['especially', 18.21, 18.75], ['some', 18.75, 18.99], ['of', 18.99, 19.08], ['the', 19.08, 19.17],
                         ['older', 19.17, 19.47], ['historical', 19.47, 20.04], ['buildings', 20.04, 20.58], ['at', 21.18, 21.36], ['this', 21.36, 21.57],
                         ['really', 21.57, 21.9], ['old', 21.9, 22.11], ['church', 22.11, 22.41], ['we', 22.41, 22.5], ['wanted', 22.5, 22.8], ['to', 22.8, 22.92],
                         ['go', 22.92, 23.13], ['into', 23.13, 23.49], ['they', 23.7, 23.88], ['explained', 23.88, 24.33], ['my', 24.33, 24.48], ['sister', 24.48, 24.9],
                         ['could', 24.9, 25.11], ['not', 25.11, 25.32], ['without', 25.32, 25.65], ['changing', 25.65, 26.04], ['because', 26.04, 26.37],
                         ['of', 26.37, 26.49], ['the', 26.49, 26.58], ['dress', 26.58, 26.85], ['code', 26.85, 27.21], ["she'd", 27.42, 27.69], ['have', 27.69, 27.84],
                         ['to', 27.84, 27.96], ['cover', 27.96, 28.29], ['her', 28.29, 28.41], ['hair', 28.41, 28.74], ['with', 28.74, 28.92], ['the', 28.92, 29.04],
                         ['short', 29.048535, 29.385707], ['thing', 29.385707, 29.61], ['they', 29.61, 29.76], ['had', 29.76, 30.09], ['where', 30.36, 30.63],
                         ['this', 30.63, 30.87], ['wraparound', 30.87, 31.44], ['skirt', 31.44, 31.83], ['over', 31.86, 32.13], ['her', 32.13, 32.28],
                         ['pants', 32.28, 32.73], ['and', 32.97, 33.15], ['wear', 33.15, 33.33], ['long', 33.33, 33.6], ['sleeves', 33.6, 34.11],
                         ['well', 34.68, 34.98], ['apparently', 34.98, 35.52], ['she', 35.52, 35.76], ['decided', 35.76, 36.24], ['she', 36.24, 36.39],
                         ['was', 36.39, 36.6], ['too', 36.6, 36.72], ['good', 36.72, 36.96], ['for', 36.96, 37.11], ['that', 37.11, 37.47], ['and', 37.65, 37.83],
                         ['she', 37.83, 37.98], ['refused', 37.98, 38.46], ['to', 38.46, 38.55], ['go', 38.55, 38.76], ['in', 38.76, 38.88], ['at', 38.88, 38.97],
                         ['all', 38.97, 39.24], ['i', 39.87, 40.02], ['was', 40.02, 40.2], ['pissed', 40.2, 40.65], ['i', 40.86, 40.98], ['went', 40.98, 41.19],
                         ['back', 41.19, 41.43], ['to', 41.43, 41.52], ['the', 41.52, 41.64], ['hotel', 41.64, 42.12], ['got', 42.36, 42.6], ['the', 42.6, 42.69],
                         ['next', 42.69, 43.02], ['ticket', 43.02, 43.26], ['home', 43.26, 43.59], ['packed', 43.68, 44.1], ['and', 44.37, 44.52], ['left', 44.52, 44.79],
                         ['without', 44.79, 45.09], ['telling', 45.09, 45.42], ['her', 45.42, 45.66], ['i', 46.23, 46.41], ['texted', 46.41, 46.83], ['her', 46.83, 46.98],
                         ['once', 46.98, 47.28], ['before', 47.28, 47.64], ['i', 47.64, 47.73], ['got', 47.73, 48.0], ['on', 48.0, 48.09], ['the', 48.09, 48.18],
                         ['plane', 48.18, 48.45], ['so', 48.45, 48.66], ['she', 48.66, 48.84], ['know', 48.848042, 49.05], ['where', 49.05, 49.26], ['i', 49.26, 49.35],
                         ['was', 49.35, 49.71], ['but', 49.89, 50.1], ['that', 50.1, 50.28], ['was', 50.28, 50.49], ['it', 50.49, 50.64], ["i'm", 50.88, 51.09],
                         ['not', 51.09, 51.24], ['gonna', 51.24, 51.45], ['go', 51.45, 51.69], ['on', 51.69, 51.81], ['a', 51.81, 51.87], ['trip', 51.87, 52.2],
                         ['with', 52.2, 52.35], ['someone', 52.35, 52.71], ['who', 52.71, 52.83], ['disrespects', 52.83, 53.58], ['local', 53.58, 53.97],
                         ['cultures', 53.97, 54.51], ['and', 54.78, 55.02], ['acts', 55.02, 55.29], ['like', 55.29, 55.5], ['every', 55.5, 55.8], ['bad', 55.8, 56.1],
                         ['american', 56.1, 56.58], ['stereotype', 56.58, 57.36], ['our', 57.57, 57.78], ['parents', 57.78, 58.14], ['rhymney', 58.14, 58.5],
                         ['when', 58.5, 58.71], ['i', 58.71, 58.77], ['got', 58.77, 59.01], ['home', 59.01, 59.34], ['saying', 59.4, 59.85], ['our', 59.85, 60.0],
                         ['as', 60.0, 60.09], ['being', 60.09, 60.33], ['terrible', 60.33, 60.81], ['for', 60.81, 60.99], ['leaving', 60.99, 61.35], 
                         ['her', 61.35, 61.53], ['for', 61.53, 61.71], ['the', 61.71, 61.8], ['last', 61.8, 62.16], ['week', 62.16, 62.4], ['of', 62.4, 62.49], 
                         ['the', 62.49, 62.58], ['trip', 62.58, 62.85], ['alone', 62.85, 63.24], ["we'd", 63.27, 63.51], ['only', 63.51, 63.81], ['been', 63.81, 63.99], 
                         ['there', 63.99, 64.11], ['two', 64.11, 64.32], ['days', 64.32, 64.74], ['but', 65.31, 65.52], ["she's", 65.52, 65.79], ['an', 65.79, 65.94], 
                         ['adult', 65.94, 66.33], ['if', 66.51, 66.66], ['she', 66.66, 66.78], ['wants', 66.78, 67.05], ['to', 67.05, 67.17], ['be', 67.17, 67.32], 
                         ['so', 67.32, 67.56], ['disrespectful', 67.56, 68.37], ['of', 68.37, 68.52], ['other', 68.52, 68.73], ['cultures', 68.73, 69.27], 
                         ['she', 69.45, 69.66], ['can', 69.66, 69.84], ['fly', 69.84, 70.08], ['home', 70.08, 70.38], ['alone', 70.38, 70.83], ['she', 71.07, 71.34], 
                         ["hasn't", 71.34, 71.73], ['spoken', 71.73, 72.24], ['to', 72.24, 72.36], ['me', 72.36, 72.57], ['since', 72.57, 72.9], ['she', 72.9, 73.08], 
                         ['got', 73.08, 73.35], ['home', 73.35, 73.71], ['which', 73.98, 74.25], ['is', 74.25, 74.4], ['fine', 74.4, 74.76], ['since', 74.76, 75.09], 
                         ['all', 75.09, 75.338379], ['our', 75.36, 75.48], ['one', 75.48, 75.75], ['is', 75.75, 75.9], ['an', 75.9, 76.02], ['apology', 76.02, 76.68]]
    script = ['AITA for leaving my sister \nin Europe after she disrespected \nthe local customs? ', 
              'My (21m) sister (18f) and I \nhad been planning this trip to \nFrance for years. ',
                "We've both been saving up for \nyears to get the money, and \nwe went for winter break a \nfew months ago. ", 
                'We were really exited to see \nall the sights, especially some of \nthe older historical buildings. ', 
                'At this really old church we \nwanted to go into, they explained \nmy sister could not without changing \nbecause of the dress code. ',
                "She'd have to cover her hair \nwith this shawl thing they had, \nwear this wrap around skirt over \nher pants, and wear long sleeves. ", 
                'Well apparently she decided she was \ntoo good for that, and she \nrufused to go in at all. ', 
                'I was pissed. I went back \nto the hotel, got the next \nticket home, packed, and left without \ntelling her. ', 
                'I went back to the hotel, \ngot the next ticket home, packed, \nand left without telling her. ',
                "I texted her once before I \ngot on the plane so she'd \nknow where I was, but that \nwas it. ",
                "I'm not gonna go on a \ntrip with someone who disrespects local \ncultures, and acts like every bad \nAmerican stereotype. ",
                "Our parents reamed me when I \ngot home, saying I was being \nterrible for leaving her for the \nlast week of the trip alone \n(we'd only been there two days). ", 
                "But she's an adult, if she \nwants to be so disrespectful of \nother cultures, she can fly home \nalone. ", 
                "She hasn't spoken to me since \nshe got home, which is fine \nsince all I want is an \napology. "]
    testList =[]
    for i in range(0, len(script)):
        segment = script[i].split()
        for j in segment:
            testList.append(j) 
    print("testList", testList)
    print(len(testList))
    print("Script length: ", len(script))
    print("regcognitionOutput length: ", len(regcognitionOutput))
    RedditData = Rbot()
    StartEndTimesList = RedditData.ExtractSegmentStartEnd(regcognitionOutput, script)
    print("StartEndTimesList:", StartEndTimesList)

