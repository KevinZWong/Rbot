

#filename = r"VoiceFiles\\storytime.wav"

import pyaudio
import wave
import struct

# Open the audio file
filename = r"VoiceFiles\\storytime.wav"
wavefile = wave.open(filename, 'rb')

# Read the audio file properties
channels = wavefile.getnchannels()
framerate = wavefile.getframerate()
sample_width = wavefile.getsampwidth()

# Set the threshold amplitude
threshold = 0.3

# Initialize variables
amplitude_below_threshold = False
period_start = 0
period_end = 0

# Loop through the audio file frames
while True:
    # Read the next frame of audio data
    data = wavefile.readframes(1)
    if not data:
        # End of file
        break

    # Convert the binary data to a numeric value
    sample = struct.unpack("<h", data)[0]

    # Calculate the amplitude
    if sample_width == 1:
        amplitude = (sample - 128) / 128.0
    else:
        amplitude = sample / 32768.0

    # Check if the amplitude is below the threshold
    if amplitude < threshold:
        # Amplitude is below the threshold
        if not amplitude_below_threshold:
            # Start of a new period
            amplitude_below_threshold = True
            period_start = wavefile.tell() / framerate
    else:
        # Amplitude is above the threshold
        if amplitude_below_threshold:
            # End of a period
            amplitude_below_threshold = False
            period_end = wavefile.tell() / framerate
            # Print the period
            print(f"Amplitude below threshold from {period_start:.2f} seconds to {period_end:.2f} seconds")

# Close the audio file
wavefile.close()
