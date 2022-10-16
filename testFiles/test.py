from moviepy.editor import *
text_clip = TextClip(txt="Hello World",
                     fontsize=40,
                     color="black",
                     bg_color="white")
text_clip.save_frame("out.png")