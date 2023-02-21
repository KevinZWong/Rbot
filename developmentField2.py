from moviepy.editor import *



#finalList = [["script segment here", starttime, endtime],["script segment here", starttime, endtime]]

def add_text_overlay(video_path, finalList):
    # Load the video file
    #video_path, text, start_time, end_time, fontsize=50, color='white', output_path=None
    video = VideoFileClip(video_path)
    for i in finalList:
        text = i[0]
        start_time = i[1]
        end_time = i[2]
        
        # Define the text to be overlayed
        text_clip = TextClip(text, fontsize=fontsize, color=color)

        # Set the duration of the text clip to be the same as the duration of the video
        text_clip = text_clip.set_duration(video.duration)

        # Set the start and end times for the text clip
        text_clip = text_clip.subclip(start_time, end_time)

        # Add the text overlay to the video
        video_with_text = CompositeVideoClip([video, text_clip])

    # Write the new video file with the text overlay
    if output_path is None:
        output_path = video_path[:-4] + "_with_text.mp4"
    video_with_text.write_videofile(output_path)

    # Close the video clips
    video.close()
    video_with_text.close()

    return output_path