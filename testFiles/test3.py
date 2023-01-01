import glob,os

files = glob.glob('VideoFiles\\*')
for f in files:
    os.remove(f)
files = glob.glob('VoiceFiles\\*')
for f in files:
    os.remove(f)
files = glob.glob('ImageFiles\\*')
for f in files:
    os.remove(f)