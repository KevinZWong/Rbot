import os
import sys
import wave
import json
import wave
import numpy as np
import matplotlib.pyplot as plt
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
        self.model_path = r"vosk-model-small-en-us-0.15"
        #self.model_path = r"C:\Users\14088\Desktop\vosk-model-en-us-0.42-gigaspeech\vosk-model-en-us-0.42-gigaspeech"
    

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
    
    def get_pauseTimes(self, FullScript,fileName, endLength):
        def format_list(input_list, start_val, end_val):
            output_list = [[start_val, input_list[0][0]]]
            for i in range(len(input_list)-1):
                output_list.append([input_list[i][1], input_list[i+1][0]])
            output_list.append([input_list[-1][1], end_val])
            return output_list
        pass
        def get_amplitudes(filename):
            # Open the audio file
            with wave.open(filename, 'rb') as audio_file:
                # Get the frame rate (number of frames per second)
                frame_rate = audio_file.getframerate()

                # Get the number of frames in the audio file
                num_frames = audio_file.getnframes()

                # Get the size of each sample (in bytes)
                sample_size = audio_file.getsampwidth()

                # Calculate the time increment based on the frame rate
                time_increment = 0.01  # 100ms time increments
                num_steps = int(num_frames / (frame_rate * time_increment))
                
                # Initialize an array to hold the amplitude values
                amplitudes = np.zeros(num_steps)

                # Move to the beginning of the audio file
                audio_file.rewind()

                # Read the first sample data
                sample_data = audio_file.readframes(1)

                # Loop through the time increments and read the sample data at each point
                for i in range(num_steps):
                    # Calculate the time in seconds for the current step
                    time = i * time_increment

                    # Move to the frame for the current time step
                    frame = int(time * frame_rate)
                    audio_file.setpos(frame)

                    # Read the sample data at the current time step
                    sample_data = audio_file.readframes(1)

                    # Convert the sample data to an integer value
                    if sample_size == 1:
                        # 8-bit samples are unsigned
                        amplitude = ord(sample_data)
                    else:
                        # Other sample sizes are signed
                        amplitude = int.from_bytes(sample_data, byteorder='little', signed=True)

                    # Store the amplitude value in the array
                    amplitudes[i] = amplitude
                    result = []
                    time = 0
                    for i in amplitudes:
                        time += time_increment
                        result.append([time, abs(i)])
            return result
        # Get the amplitudes for the audio file
        amplitudes = get_amplitudes(fileName)
        counter = 0
        pauses = 0
        timesList = []
        times = []
        for i in amplitudes:
            if i[1] < 300 :
                counter += 1
            else:
                if counter != 0:
                    times.append(i[0])
                    timesList.append(times) 
                    times = []
                counter = 0
            if counter == 1:
                times.append(i[0])
                
        minPauseLength = 0.32 #seconds


        finalReturnTImes = []

        if (len(timesList) == len(FullScript)):
            print("Length of calcuated times matches the length of the script")
        else:
            print("ERROR: Length of calcuated times does not match the length of the script")

        print(timesList)
        print(pauses)
        popBeginning = False
        popEnd = False
        for i in range(0,len(timesList)):
            if timesList[i][1] - timesList[i][0] >= minPauseLength:
                
                finalReturnTImes.append([timesList[i][0], timesList[i][1]])
                #finalReturnTImes.append([timesList[i][0], timesList[i][1]])
                pauses += 1
                #plt.axvline(x=(timesList[i][1] - timesList[i][0])/2 + timesList[i][0], color='r')
                if ((timesList[i][1] - timesList[i][0])/2 + timesList[i][0] < 1) and i== 0:
                    popBeginning = True
                if ((timesList[i][1] - timesList[i][0])/2 + timesList[i][0] > endLength-1) and i == len(timesList) -1:
                    popEnd = True
        
        # Create a time array based on the time increment and number of steps
        time_increment = 0.01  # 100ms time increments
        num_steps = len(amplitudes)
        time = np.arange(num_steps) * time_increment

        # Plot the amplitudes over time
        '''
        plt.plot(time, amplitudes)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.show()
        '''
        if (popBeginning):
            finalReturnTImes.pop(0)
        if (popEnd):
            finalReturnTImes.pop[len(finalReturnTImes)-1]
        if finalReturnTImes ==[]:
            finalReturnTImes = [0]
        finalReturnTimes2 = format_list(finalReturnTImes, 0, endLength)
        for i in range(0, len(FullScript)):
            finalReturnTimes2[i].insert(0, FullScript[i])

        
        
        return finalReturnTimes2
    def ScriptSplitterV2_times(self, strings , times):
        intervals = []
        current_time = 0
        for i in range(len(strings)):
            interval = [strings[i], current_time, current_time + times[i]]
            intervals.append(interval)
            current_time += times[i]
        return intervals

'''
wordtest = VoiceRecognitition()
audio_filename = r"VoiceFiles\storytime.wav"

# [[word, start, end], [word, start, end], [word, start, end]]
# #get_pauseTimes(self, FullScript,fileName, endLength)
FullScript = ['My Neighbour Saw Me Naked ', 'I go to bed naked and \nusually get up and don’t put \nclothes on until after I’ve had \nmy shower. ', 'This morning I forgot I had \nclothes in the washer. ', 'My washer and dryer is located \nin the basement. ', 'My basement has one window you \ncan look out of close to \nthe bottom of the stairs facing \nright next to our neighbours house. ', 'For context I live in a \nduplex/ cul-de-sac subdivision. ', 'The neighbours front porch overlooks the \nbasement window. ', 'I was in my birthday suit \nwalking down the stairs as I \nlooked out the window. ', 'I could see a women standing \nat the front porch. ', 'I’m sure she was looking directly \nat me. ', 'For some reason I awkwardly smiled \nat her but then remembered I’m \nnot wearing anything. ', 'I’m pretty sure she saw everything \nbut I ran down the stairs \nthe last few steps as fast \nas I could after that. ', 'Not thinking of anything other than \nI just flashed my neighbour. ']
print(wordtest.get_pauseTimes(FullScript, audio_filename, 48.82))


'''
