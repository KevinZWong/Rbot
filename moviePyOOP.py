from moviepy.editor import *
from scrapeRedditOOP import ScrapReddit
from TextToVoiceOOP import TextToVoice

from pydub import AudioSegment

class VideoGenerator:
    
    def __init__(self):
        self.size = (1080,1920)
        self.font="Lane"
        self.color="White"
        self.bg_color="green" 
        self.fontsize=60
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

    def getLengthAudioFile(self, fname):
        import wave
        import contextlib
        with contextlib.closing(wave.open(fname,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration



    def imageFromText(self, caption, imageName):
        text_clip = TextClip(txt=caption,
                             fontsize = self.fontsize,
                             size = self.size,
                             font = self.font,
                             color = self.color,
                             bg_color = self.bg_color)
        accessCheckForFileType = TextToVoice()
        imageName = accessCheckForFileType.CheckForFileType("ImageFiles\\" + imageName, ".png")
        text_clip.save_frame(imageName)


    def add_static_image_to_audio(self, image_path, audio_path, output_path):

        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path)
        video_clip = image_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration
        video_clip.fps = 1
        video_clip.write_videofile(output_path)
    '''
    def monoToStereo(self, audio_path):
        print("audio_path", audio_path)
        left_channel = AudioSegment.from_wav(audio_path)
        right_channel = AudioSegment.from_wav(audio_path)

        stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
        stereo_sound.export(audio_path, format="wav")
    '''
        
    def conbineAllVideos(self, VideoFileNameList, name):
        clipList = []
        for i in VideoFileNameList:
            clip = VideoFileClip(i)
            clipList.append(clip)
        concat_clip = concatenate_videoclips(clipList, method="compose")
        concat_clip.write_videofile(name)

    
def main():
    video1 = VideoGenerator()
    
    audioFilePath = "VoiceFiles\\"
    imageFilePath = "ImageFiles\\"
    videoFilePath = "VideoFiles\\"
    video1.add_static_image_to_audio( audioFilePath + "script0_0.mp3", imageFilePath + "image0_0.png", videoFilePath + "testvideo1.mp4")
