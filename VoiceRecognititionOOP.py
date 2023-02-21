import os
import sys
import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel
# !pip install vosk
from Word import Word
class Word:
    ''' A class representing a word from the JSON format for vosk speech recognition API '''

    def __init__(self, dict):
        '''
        Parameters:
          dict (dict) dictionary from JSON, containing:
            conf (float): degree of confidence, from 0 to 1
            end (float): end time of the pronouncing the word, in seconds
            start (float): start time of the pronouncing the word, in seconds
            word (str): recognized word
        '''

        self.conf = dict["conf"]
        self.end = dict["end"]
        self.start = dict["start"]
        self.word = dict["word"]

    def to_string(self):
        ''' Returns a string describing this instance '''
        return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%".format(
            self.word, self.start, self.end, self.conf*100)
    def getWord(self):
        return self.word
    def getStartTime(self):
        return self.start
    def getEndTime(self):
        return self.end
    def getConfidence(self):
        return self.conf*100


class VoiceRecognitition: 
    def __init__(self):


        #https://alphacephei.com/vosk/models
        self.model_path = r"C:\Users\14088\Downloads\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"
    

    def recognize(self, audio_filename):       
        # name of the audio file to recognize
        #audio_filename = r"C:\Users\14088\Desktop\Projects\Rbot\VoiceFiles\script21_0 (1).wav"
        # name of the text file to write recognized text
        #text_filename = r"C:\Users\14088\Desktop\Projects\Rbot\outputText.txt"
        SetLogLevel(0)
        if not os.path.exists(self.model_path ):
            print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {self.model_path }")
            sys.exit()

        print(f"Reading your vosk model '{self.model_path }'...")
        model = Model(self.model_path )
        print(f"'{self.model_path }' model was successfully read")

        if not os.path.exists(audio_filename):
            print(f"File '{audio_filename}' doesn't exist")
            sys.exit()

        print(f"Reading your file '{audio_filename}'...")
        wf = wave.open(audio_filename, "rb")
        print(f"'{audio_filename}' file was successfully read")

        # check if audio is mono wav
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            sys.exit()

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        results = []

        # recognize speech using vosk model
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                results.append(part_result)

        part_result = json.loads(rec.FinalResult())
        results.append(part_result)


        # convert list of JSON dictionaries to list of 'Word' objects

        list_of_Words = []
        for sentence in results:
            if len(sentence) == 1:
                # sometimes there are bugs in recognition 
                # and it returns an empty dictionary
                # {'text': ''}
                continue
            for obj in sentence['result']:
                w = Word(obj)  # create custom Word object
                list_of_Words.append(w)  # and add it to list
        # forming a final string from the words
        text = ''
        for r in results:
            text += r['text'] + ' '
        '''
        print(f"Saving text to '{text_filename}'...")
        with open(text_filename, "w") as text_file:
            text_file.write(text)
        print(f"Text successfully saved")
        '''
        returnList = []
        # output to the screen
        for word in list_of_Words:
            returnList.append([word.getWord(), word.getStartTime(),word.getEndTime()])

        return returnList
    


'''
wordtest = VoiceRecognitition()
audio_filename = r""

# [[word, start, end], [word, start, end], [word, start, end]]
print(wordtest.recognize(audio_filename))
'''


