
from subprocess import list2cmdline
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
        def CheckForFileType(filename):
            listFileName = list(filename)
            listFileName = listFileName[::-1]
            last4 = ""
            try:
                for i in range(0, 4, 1):
                    last4 += listFileName[i]
                print("last4:",last4)
                if last4 != "3pm.":
                    return filename + ".mp3"
                else:
                    return filename
            except:
                return filename + ".mp3"
        def SwapChacters(str1,remove, replace):
            listStr = list(str1)
            returnStr = ""
            for i,v in enumerate(listStr):
                if (v == remove):
                    listStr[i] = replace
                returnStr += listStr[i]
            return returnStr
            


        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[self.gender].id)
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        filename = SwapChacters(filename,':', '_')
        self.engine.save_to_file(text, CheckForFileType(filename))
        
            
        # Wait until above command is not finished.
        self.engine.runAndWait()

