from moviepy.editor import *



location = r"C:\Users\14088\Videos\ValoClips\J3tKTNkf0IIBX7ErZvKnMQ.mp4"



clip = VideoFileClip(location)
clip = clip.without_audio()
clip = clip.cutout(clip.duration -2, clip.duration)
clip = clip.crop(x1=0, y1=0, x2=656.25, y2=0)
clip = clip.crop(x1=1263.75, y1=0, x2=1920, y2=0)
clip.write_videofile("vid1.mp4")