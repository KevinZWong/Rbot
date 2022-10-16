
from subprocess import list2cmdline
import pyttsx3

class TextToVoice:
    
    def __init__(self):

        self.Subbreddit = ""
        self.engine = pyttsx3.init()
        self.voiceType = 1
        self.rate = 178
        self.volume = 230
    
    def getvoiceType(self):
        return self.voiceType
    def setVoiceType(self, voiceType): 
        self.voiceType = voiceType
    def getRate(self):
        return self.rate
    def setRate(self, rate): 
        self.rate = rate
    def getVolume(self):
        return self.volume
    def setVolume(self, volume): 
        self.volume = volume


    def convert_T2V(self, text, filename): # voiceType
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
        self.engine.setProperty('voice', voices[self.voiceType].id)
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        filename = SwapChacters(filename,':', '_')
        filename = "C:\\Users\\14088\\Desktop\\Rbot\\VoiceFiles\\" + CheckForFileType(filename)
        self.engine.save_to_file(text, filename)
        
            
        # Wait until above command is not finished.
        self.engine.runAndWait()

