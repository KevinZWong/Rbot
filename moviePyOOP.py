from moviepy.editor import *
from scrapeRedditOOP import ScrapReddit
from TextToVoiceOOP import TextToVoice
class VideoGenerator:
    
    def __init__(self):
        self.size = (0,0)
        self.font="Lane"
        self.color="White"
        self.bg_color="black" 
        self.fontsize=40
    def getFontsize(self):
        return self.fontsize
    def setFontsize(self, initFontsize): 
        self.fontsize = initFontsize
    def getSize(self):
        return self.size
    def setSize(self, initSize): 
        self.size = initSize
    def getFont(self):
        return self.font
    def setFont(self, initFont): 
        self.font = initFont
    def getColor(self):
        return self.color
    def setColor(self, initColor): 
        self.color = initColor
    def getBg_color(self):
        return self.bg_color
    def setBg_color(self, initBg_color): 
        self.bg_color = initBg_color

    def imageFromText(self, caption, imageName):
        text_clip = TextClip(txt=caption,
                             fontsize = self.fontsize,
                             size = self.size,
                             font = self.font,
                             color = self.color,
                             bg_color = self.bg_color)
        accessCheckForFileType = TextToVoice()
        imageName = accessCheckForFileType.CheckForFileType("C:\\Users\\14088\\Desktop\\Rbot\\ImageFiles\\" + imageName, ".png")
        text_clip.save_frame(imageName)


    '''
    def generateVideo(self, audioFileName, audioFileLocation, caption):
        text_clip = TextClip(txt=caption,
                        fontsize = self.fontsize,
                        size = self.size,
                        font = self.font,
                        color = self.color,
                        bg_color = self.bg_color)
        text_clip.save_frame("out.png")
        
        text1 = TextClip("hello world, hi there",fontsize=10 ,color="white").set_position(( "left" ,"top") ).set_duration(10) 
    '''
def main():
    video1 = VideoGenerator()
    video1.imageFromText( "hi there", "image1")
