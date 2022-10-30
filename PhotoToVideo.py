from moviepy.editor import *

clips = []
clip1 =  ImageClip('image1.jpg').set_duration(2)
clip2 =  ImageClip('image2.jpg').set_duration(3)
clips.append(clip1)
clips.append(clip2)

video_clip = concatenate_videoclips(clips, method='compose')
video_clip.write_videofile("video-output.mp4", fps=24, remove_temp=True, codec="libx264", audio_codec="aac")