
import pyttsx3

class TextToVoice:
    
    def __init__(self):

        self.Subbreddit = ""
        self.engine = pyttsx3.init()
        self.gender = 0
        self.rate = 2
        self.volume = 230
    
    def getGender(self):
        return self.gender
    def setGender(self, gender): # 0 male, 1 female
        self.gender = gender
    def getRate(self):
        return self.rate
    def setRate(self, rate): 
        self.rate = rate
    def getVolume(self):
        return self.volume
    def setVolume(self, volume): 
        self.volume = volume


    def convert_T2V(self, text, filename): # gender: 0 male, 1 female
        print('rate', self.rate)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[self.gender].id)
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)

        listFileName = list(filename)
        listFileName = listFileName[::-1]
        last4 = ""
        for i in range(0, 4, 1):
            last4 += listFileName[i]

        if last4 != ".mp3":
            self.engine.save_to_file(text, filename + ".mp3")
        else:
            self.engine.save_to_file(text, filename)
            
        # Wait until above command is not finished.
        self.engine.runAndWait()

