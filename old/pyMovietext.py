import moviepy.editor as mp
clip1 = mp.VideoFileClip("background.mp4", audio=True)


text1 = mp.TextClip("hello world, hi there",fontsize=10 ,color="white").set_position(( "left" ,"top") ).set_duration(10) 

final = mp.CompositeVideoClip([clip1,text1])
final.write_videofile("video1.mp4")

