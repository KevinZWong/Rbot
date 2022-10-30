import wave
import contextlib
fname = "C:\\Users\\14088\\Desktop\\Rbot\\VoiceFiles\\script1_0.mp3"
with contextlib.closing(wave.open(fname,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print(duration)
