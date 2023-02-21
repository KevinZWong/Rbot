import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips



#def concatenate_videos(videos, duration):
def concatenate_videos(final_duration, folder_name, final_path):
    def select_random_video(videos, used_videos):
        # Select a random video from the list of available videos
        video = random.choice(videos)

        # If the selected video has been used before, select a different video
        while video in used_videos:
            video = random.choice(videos)

        # Add the selected video to the list of used videos
        used_videos.append(video)

        return video
    # Folder name

    # List to hold the file names
    file_names = []

    # Loop through the files in the folder
    for file_name in os.listdir(folder_name):
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(os.path.join(folder_name, file_name)):
            # Add the file name to the list
            file_names.append(file_name)


    # Initialize an empty list to store the clips
    clips = []

    # Initialize an empty list to store the used videos
    used_videos = []

    # Select and concatenate clips until the duration is reached
    total_duration = 0
    while total_duration < final_duration:
        # Select a random video from the list of available videos
        video = select_random_video(file_names, used_videos)

        # Load the selected video clip
        clip = VideoFileClip(video)

        # Trim the clip to the desired duration or the remaining time available
        remaining_duration = final_duration - total_duration
        clip_duration = min(clip.duration, remaining_duration)
        clip = clip.subclip(0, clip_duration)

        # Add the trimmed clip to the list of clips
        clips.append(clip)

        # Update the total duration
        total_duration += clip_duration

    # Concatenate the clips
    final_clip = concatenate_videoclips(clips)
    # Export the final video to a file
    final_clip.write_videofile(final_path)













def generateBackgroundFootage(final_duration, folder_name, final_path):
    #folder_name = 'C://Users//14088//Videos//ValoClips//'

    # List to hold the file names
    file_names = []

    # Loop through the files in the folder
    for file_name in os.listdir(folder_name):
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(os.path.join(folder_name, file_name)):
            # Add the file name to the list
            file_names.append(folder_name + file_name)

    # List of video file names
    video_files = file_names

    # Desired final video duration in seconds
    #final_duration = 12

    # Shuffle the video file list
    random.shuffle(video_files)

    # List to hold selected video clips
    selected_clips = []

    # Loop through the video file list and select random clips until the total duration is equal to or greater than the desired duration
    total_duration = 0
    while total_duration < final_duration:
        # Select a random video clip
        clip = VideoFileClip(random.choice(video_files))
        
        # Calculate the remaining duration needed
        remaining_duration = final_duration - total_duration
        
        # If the clip duration is greater than the remaining duration, trim it
        if clip.duration > remaining_duration:
            start_time = random.uniform(0, clip.duration - remaining_duration)
            end_time = start_time + remaining_duration
            clip = clip.subclip(start_time, end_time)
        
        # Add the clip to the selected clips list
        selected_clips.append(clip)
        
        # Update the total duration
        total_duration += clip.duration

    # Concatenate the selected clips into a final video
    final_clip = concatenate_videoclips(selected_clips)

    # Export the final video to a file
    final_clip.write_videofile(final_path)