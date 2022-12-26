from moviepy.editor import *
#clip1 = mp.VideoFileClip("background.mp4", audio=True)

story1 = "This is very confusing to me and I wish I didn\u2019t have it but it\u2019s not going away. Politically, I am a huge feminist, like the type that reads feminist literature and political theory and I hate how deep rooted misogyny is within our culture. HOWEVER in bed my stupid brain somehow seems to get off on men that hate women, and what\u2019s worse is that it doesn\u2019t draw the line at role play I am genuinely attracted to actual sexists. I don\u2019t know why I enjoy this and it goes against all of my morals but I can\u2019t seem to get rid of it."

text_clip = TextClip(txt=story1,
                        # fontsize=40,
                        size=(1080,1920),
                        font="Lane",
                        color="White",
                        bg_color="black")
'''
tc_width, tc_height = text_clip.size # (800, ?)
color_clip = ColorClip(size=(tc_width+100, tc_height+500))
'''

text_clip.save_frame("out.png")

'''
final = mp.CompositeVideoClip([clip1,text1])
final.write_videofile("video1.mp4")
'''
# 21 - 34 sec