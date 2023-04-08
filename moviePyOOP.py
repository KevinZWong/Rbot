from moviepy.editor import *
from scrapeRedditOOP import ScrapReddit
from TextToVoiceOOP import TextToVoice
from pydub import AudioSegment
import os
import subprocess
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
import concurrent.futures
class VideoGenerator:
    
    def __init__(self):
        self.size = (1080,1920)
        self.font="Lane"
        self.color="White"
        self.bg_color=(0, 0, 0, 0)
        self.fontsize=15
        
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
        audio = AudioFileClip(fname)
        duration = audio.duration
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
        image_clip = ImageClip(image_path).set_duration(audio_clip.duration)
        image_clip = image_clip.set_audio(audio_clip)
        image_clip.write_videofile(output_path, fps=24)

    def cropVideo(self, filePath, finalPath):
        # Load the video clip
        clip = VideoFileClip(filePath)

        # Get the original dimensions of the clip
        width, height = clip.size

        # Calculate the dimensions of the new clip with a 9:16 aspect ratio
        new_width = int(height * 9 / 16)
        new_height = height

        # Calculate the x-coordinate of the left edge of the crop box
        left = (width - new_width) / 2

        # Crop the clip to the new dimensions
        clip = clip.crop(x1=left, y1=0, x2=left+new_width, y2=new_height)

        # Export the modified clip to a file
        clip.write_videofile(finalPath)

        # Release the clip object
        clip.close()





    def generateBackgroundFootage(self, final_duration, folder_name, final_path):
        # Get list of video file names in folder
        video_filenames = [f for f in os.listdir(folder_name) if f.endswith('.mp4')]

        # Choose random video clips until final_duration is reached
        selected_clips = []
        total_duration = 0
        used_filenames = set()
        while total_duration < final_duration:
            # Select a random video that hasn't been used before
            unused_filenames = list(set(video_filenames) - used_filenames)
            if not unused_filenames:
                break
            random_filename = random.choice(unused_filenames)
            video_path = os.path.join(folder_name, random_filename)

            # Trim the video to the desired length
            duration = min(final_duration - total_duration, VideoFileClip(video_path).duration)
            video_clip = VideoFileClip(video_path).subclip(0, duration)
            selected_clips.append(video_clip)

            # Update the total duration and set of used filenames
            total_duration += video_clip.duration
            used_filenames.add(random_filename)

        # Concatenate the selected clips
        final_clip = concatenate_videoclips(selected_clips)

        # Save the final clip to the specified folder
        final_clip.write_videofile(final_path, fps=30, codec='libx264')
  
    def combine_audio_files(self, file_list, output_file):
        # Combine the audio files into a single file
        command = ['ffmpeg', '-y']
        for file in file_list:
            command += ['-i', file]
        command += ['-filter_complex', 'concat=n={}:v=0:a=1'.format(len(file_list)), '-vn', output_file]
        subprocess.run(command)

    def overlay_audio_video(self, video_path, audio_path, output_path, video_duration):
        # Load the video file and audio file
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Set the audio to the same duration as the video
        audio = audio.set_duration(video_duration)

        # Overlay the audio onto the video
        video_with_audio = video.set_audio(audio)

        # Write the new video file with the overlaid audio
        video_with_audio.write_videofile(output_path)

        # Close the video clips
        video.close()
        audio.close()
        video_with_audio.close()
        #return output_path
    def add_text_overlay(self ,video_path, text_list, output_path):
        # Load the video file
        video = VideoFileClip(video_path)

        # Iterate through the text list and add text to video clip
        for text, start_time, end_time in text_list:
            text_clip = TextClip(text, fontsize=self.fontsize, color=self.color, transparent=True).set_pos('center').set_duration(end_time - start_time).set_start(start_time)
            video = CompositeVideoClip([video, text_clip])

        # Write the new video file with the added text
        video.write_videofile(output_path)

        # Close the video clip
        video.close()

        return output_path

    def add_text_to_video_multithreading(self, video_path, text_list, output_path):
        # Load the video file
        video = VideoFileClip(video_path)

        # Define a function to add text to a single clip
        def add_text_to_clip(text, start_time, end_time):
            text_clip = TextClip(text, fontsize=30, color='white', bg_color='transparent').set_pos('center').set_duration(end_time - start_time).set_start(start_time)
            return CompositeVideoClip([video.subclip(start_time, end_time), text_clip])

        # Use concurrent.futures to process the text clips in parallel
        clips = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(add_text_to_clip, text, start_time, end_time) for text, start_time, end_time in text_list]
            for future in concurrent.futures.as_completed(futures):
                clips.append(future.result())

        # Combine the clips into a single video
        final_clip = concatenate_videoclips(clips)

        # Write the new video file with the added text
        final_clip.write_videofile(output_path, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')

        # Close the video clips
        video.close()
        final_clip.close()


'''        
def main():
    video1 = VideoGenerator()
    
    audioFilePath = "VoiceFiles\\"
    imageFilePath = "ImageFiles\\"
    videoFilePath = "VideoFiles\\"
    video1.add_static_image_to_audio( audioFilePath + "script0_0.mp3", imageFilePath + "image0_0.png", videoFilePath + "testvideo1.mp4")
'''
