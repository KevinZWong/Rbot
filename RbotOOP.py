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
import openai

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

        #############################################################################
        #############################################################################
        # ERROR PREVENTION
        duplicate_list = list(regcognitionOutput)
        regcognitionOutput.extend(duplicate_list)
        #############################################################################
        #############################################################################

        NumWords = 0
        indexes = []
        finalList = []
        indexesPt2 = []
        test1 = ""
        for i in regcognitionOutput:
            test1 += i[0] + " "
        print("test1: ", test1)

        for i in range(0, len(Script)):
            segment = Script[i].split()
            indexes.append(NumWords)
            NumWords += len(segment)
            indexesPt2.append(NumWords-1)
        print(indexes)
        print("indexes length", len(indexes))


        for i in range(0, len(indexes)-1, 1):
            tempListIndexes = []
            tempListIndexes.append(regcognitionOutput[indexes[i]][1])
            tempListIndexes.append(regcognitionOutput[indexesPt2[i]][2])
            finalList.append(tempListIndexes)
            #finalList.append([regcognitionOutput[indexes[i-1]][1], regcognitionOutput[indexes[i]][2]])
        for i in range(0, len(finalList), 1):
            finalList[i].insert(0, Script[i])
        
        # finalList = [["script segment here", starttime, endtime],["script segment here", starttime, endtime]]
        return finalList


    def regcognitionOutput_string(self, regcognitionOutput):
        for i in regcognitionOutput:
            test1 += i[0] + " "
        return test1

    def ScriptProcessing(self, script):
        # Set up OpenAI API credentials
        openai.api_key = "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"

        # Set up the OpenAI GPT-3 model
        model_engine = "text-davinci-002"
        model_prompt = f"Please correct the following paragraph for grammar mistakes:\n{script}\nCorrection:"
        # Generate the summary using GPT-3
        response = openai.Completion.create(
            engine=model_engine,
            prompt=model_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract the summary from the GPT-3 response
        result = response.choices[0].text.strip()
        result = result.split(":")[-1].strip()

        # Print the summary
        return result



    def replace_acronyms(self, passage):
        reddit_acronyms = {}
        try:
            with open('acronym_dict.json', 'r') as f:
                reddit_acronyms = json.load(f)
        except:
            print("couldn't find dictionary of acronyms")
        words = passage.split()
        new_words = []
        for word in words:
            if word.upper() in reddit_acronyms:
                new_words.append(reddit_acronyms[word.upper()])
            else:
                new_words.append(word)
        new_passage = ' '.join(new_words)
        return new_passage
    


if __name__ == "__main__":
    regcognitionOutput = [['am', 0.18, 0.39], ['i', 0.39, 0.48], ['the', 0.48, 0.63], ['asshole', 0.63, 1.08], ['for', 1.08, 1.32], ['not', 1.32, 1.53], ['buying', 1.53, 1.86], ['a', 1.86, 1.95], ['car', 1.95, 2.22], ['for', 2.22, 2.4], ['my', 2.4, 2.52], ['stepdaughter', 2.52, 3.18], ['english', 3.45, 3.96], ['is', 3.96, 
4.14], ['not', 4.14, 4.38], ['my', 4.38, 4.56], ['first', 4.56, 4.95], ['language', 4.95, 5.52], ["i'm", 5.55, 5.76], ['childfree', 5.76, 6.48], ['i', 7.08, 7.23], ['like', 7.23, 7.44], ['kids', 7.44, 7.77], ['i', 7.8, 7.89], ['just', 7.89, 8.13], ["don't", 8.13, 8.34], ['want', 8.34, 8.55], ['to', 8.55, 8.64], ['bring', 8.64, 8.91], ['one', 8.91, 9.18], ['into', 9.21, 9.45], ['this', 9.45, 9.69], ['world', 9.69, 10.08], ['i', 10.65, 10.77], ['have', 10.77, 11.01], ['a', 11.01, 11.04], ['sister', 11.04, 11.49], ['and', 11.49, 11.61], ['a', 11.61, 11.67], ['brother', 11.67, 12.06], ['my', 12.66, 12.87], ['sister', 12.87, 13.29], ['is', 13.29, 13.44], ['also', 13.44, 13.77], ['childfree', 13.77, 14.4], ['but', 14.4, 14.64], ['my', 14.64, 14.79], ['brother', 14.79, 15.18], ['has', 15.18, 15.45], ['a', 15.45, 15.48], ['sixteen', 15.48, 15.96], ['yo', 15.96, 16.17], ['daughter', 16.17, 16.59], ['we', 17.19, 17.34], ['love', 17.34, 17.61], ['our', 17.61, 17.76], ['niece', 17.76, 18.15], ['and', 18.18, 18.33], ['we', 18.33, 18.48], ['like', 18.48, 18.69], ['to', 18.69, 18.81], ['spoil', 18.81, 19.17], ['her', 19.17, 19.44], ['for', 19.62, 19.8], ['her', 19.8, 19.95], ['sick', 19.95, 20.16], ['nineteenth', 20.16, 20.49], ['birthday', 20.49, 21.0], ['we', 21.12, 21.3], ['decided', 21.3, 21.72], ['to', 21.72, 21.84], ['buy', 21.84, 22.05], ['a', 22.05, 22.11], ['car', 22.11, 22.38], ['for', 22.38, 22.56], ['her', 22.56, 22.74], ['which', 22.74, 22.98], ['made', 22.98, 23.22], ['her', 23.22, 23.37], ['very', 23.37, 23.64], ['happy', 23.64, 24.06], ['i', 24.69, 24.81], ['married', 24.81, 25.17], ['my', 25.17, 25.35], ['wife', 25.35, 25.62], ['a', 25.62, 25.65], ['year', 25.65, 25.89], ['ago', 25.89, 26.22], ['after', 26.22, 26.55], ['dating', 26.55, 26.85], ['for', 26.85, 27.03], ['thirteen', 27.03, 27.51], ['years', 27.51, 27.96], ['she', 28.53, 28.77], ['has', 28.77, 29.07], ['a', 29.07, 29.13], ['daughter', 29.13, 29.61], ['and', 29.82, 30.06], ['a', 30.06, 30.09], ['son', 30.09, 30.48], ['from', 30.48, 30.72], ['her', 30.72, 30.93], ['previous', 30.93, 31.53], ['relationship', 31.53, 32.43], ['i', 32.97, 33.09], ['like', 33.09, 33.33], ['her', 33.33, 33.45], ['kids', 33.45, 33.87], ['and', 34.08, 34.2], ['i', 34.2, 34.29], ['think', 34.29, 34.53], ['we', 34.53, 34.62], ['generally', 34.62, 35.1], ['get', 35.1, 35.28], ['along', 35.28, 35.67], ['her', 35.94, 36.12], ['daughter', 36.12, 36.42], ['turned', 36.42, 36.72], ['sixteen', 36.72, 37.17], ['a', 37.17, 37.23], ['week', 37.23, 37.53], ['ago', 37.53, 37.86], ['and', 37.86, 37.98], ['i', 37.98, 38.07], ['bought', 38.07, 38.31], ['her', 38.31, 38.46], ['a', 38.46, 38.52], ['nice', 38.52, 38.82], ['bag', 38.82, 39.15], ['that', 39.15, 39.3], ['she', 39.3, 39.51], ['had', 39.51, 39.6], ['said', 39.6, 39.81], ['she', 39.81, 39.99], ['wanted', 39.99, 40.32], ['it', 40.32, 40.47], ['i', 41.04, 41.16], ['thought', 41.16, 41.43], ["it's", 41.43, 41.55], ['a', 41.55, 41.64], ['good', 41.64, 41.97], ['and', 42.0, 42.09], ['thoughtful', 42.09, 42.48], ['gift', 42.48, 42.78], ['but', 42.78, 42.93], ['my', 42.93, 43.08], ['wife', 43.08, 43.44], ['looked', 43.44, 43.62], ['shocked', 43.62, 44.04], ['she', 44.16, 44.37], ["didn't", 44.37, 44.64], ['say', 44.64, 44.94], ['anything', 44.94, 45.33], ['in', 45.33, 45.42], ['front', 45.42, 45.66], ['of', 45.66, 45.72], ['the', 45.72, 45.81], ['guest', 45.81, 46.23], ['but', 46.23, 46.44], ['after', 46.47, 46.8], ['the', 46.8, 46.92], ['party', 46.92, 47.25], ['was', 47.25, 47.43], 
['over', 47.43, 47.7], ['she', 47.7, 47.88], ['blew', 47.88, 48.15], ['up', 48.15, 48.3], ['at', 48.3, 48.39], ['me', 48.39, 48.66], ['and', 48.69, 48.87], ['called', 48.87, 49.14], ['me', 49.14, 49.32], ['an', 49.32, 49.44], ['asshole', 49.44, 49.95], ['she', 50.49, 50.73], ['said', 50.73, 51.09], ['they', 51.09, 51.21], ['expected', 51.21, 51.75], ['a', 51.75, 51.81], ['car', 51.81, 52.08], ['since', 52.08, 52.38], ['i', 52.38, 52.5], ['bought', 52.5, 52.74], ['a', 52.74, 52.8], ['car', 52.8, 53.07], ['from', 53.07, 53.25], ['my', 53.25, 53.4], ['niece', 53.4, 53.85], ['we', 54.42, 54.6], ['got', 54.6, 54.84], ['into', 54.84, 55.08], ['a', 55.08, 55.14], ['fight', 55.14, 55.56], ['and', 55.59, 55.71], ['she', 55.71, 55.92], ['is', 55.92, 56.07], ['not', 56.07, 56.28], ['talking', 56.28, 56.64], ['to', 56.64, 56.76], ['me', 56.76, 56.91], ['now', 56.91, 57.24], ['edit', 57.51, 57.84], ['edited', 58.14, 58.56], ['a', 58.56, 58.62], ['typo', 58.62, 59.13], ['we', 59.49, 59.67], ['dated', 59.67, 59.97], ['for', 59.97, 60.15], ['thirty', 60.15, 60.48], ['ten', 60.48, 60.63], ['years', 60.63, 60.9], ['not', 60.9, 61.11], ['three', 61.11, 61.32], ['years', 61.32, 61.77]]
    script = ['AITA for not buying a car for my stepdaughter? ', "English is not my first language I'm childfree. I like kids I just don't want to bring one into this world. ",
                "I like kids I just don't want to bring one into this world. ", 'I have a sister and a brother. My sister is also childfree but my  brother has a 16yo daughter. ',
                'My sister is also childfree but my brother has a 16yo daughter. ', 'We love our niece and we like to spoil her. For her 16th birthday we decided to buy a car for her which made her very happy. ',
                'For her 16th birthday we decided to buy a car for her which made her very  happy. ', 'I married my wife a year ago after dating for 13 years. ',
                'She has a daughter and a son from her previous relationship. ', 'I like her kids and I think we generally get along. ', 'Her daughter turned 16 a week ago and I bought her a nice bag that she had said she wanted. ',
                "I thought it's a good and thoughtful gift but my wife looked shocked. ", "She didn't say anything in front of the guests but after the party was over she blew up at me and called me an asshole. ",
                'She said they expected a car since I bought a car for my niece. ', 'We got into a fight and she is not talking to me now.  ', 'Edit: edited a typo. ']
    print("Script length: ", len(script))

    print("regcognitionOutput length: ", len(regcognitionOutput))

    recognized = ""
    for i in regcognitionOutput:
        recognized += i[0] + " "
    print(recognized)



    
    RedditData = Rbot()
    StartEndTimesList = RedditData.ExtractSegmentStartEnd(regcognitionOutput, script)
    
    #print("StartEndTimesList:", len(StartEndTimesList))
    #print("StartEndTimesList:", StartEndTimesList)

