


from moviepy.editor import VideoFileClip


background_video_file_path = ""

videoclip = VideoFileClip("video.mp4")
new_clip = videoclip.without_audio()


new_clip.write_videofile("final_cut.mp4")