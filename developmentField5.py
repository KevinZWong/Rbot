import wave
import numpy as np
import matplotlib.pyplot as plt
def get_pauseTimes(fileName):
    pass
    def get_amplitudes(filename):
        # Open the audio file
        with wave.open(filename, 'rb') as audio_file:
            # Get the frame rate (number of frames per second)
            frame_rate = audio_file.getframerate()

            # Get the number of frames in the audio file
            num_frames = audio_file.getnframes()

            # Get the size of each sample (in bytes)
            sample_size = audio_file.getsampwidth()

            # Calculate the time increment based on the frame rate
            time_increment = 0.01  # 100ms time increments
            num_steps = int(num_frames / (frame_rate * time_increment))
            
            # Initialize an array to hold the amplitude values
            amplitudes = np.zeros(num_steps)

            # Move to the beginning of the audio file
            audio_file.rewind()

            # Read the first sample data
            sample_data = audio_file.readframes(1)

            # Loop through the time increments and read the sample data at each point
            for i in range(num_steps):
                # Calculate the time in seconds for the current step
                time = i * time_increment

                # Move to the frame for the current time step
                frame = int(time * frame_rate)
                audio_file.setpos(frame)

                # Read the sample data at the current time step
                sample_data = audio_file.readframes(1)

                # Convert the sample data to an integer value
                if sample_size == 1:
                    # 8-bit samples are unsigned
                    amplitude = ord(sample_data)
                else:
                    # Other sample sizes are signed
                    amplitude = int.from_bytes(sample_data, byteorder='little', signed=True)

                # Store the amplitude value in the array
                amplitudes[i] = amplitude
                result = []
                time = 0
                for i in amplitudes:
                    time += time_increment
                    result.append([time, abs(i)])
        return result
        # Get the amplitudes for the audio file
    amplitudes = get_amplitudes(fileName)
    counter = 0
    pauses = 0
    timesList = []
    times = []
    for i in amplitudes:
        if i[1] < 300 :
            counter += 1
        else:
            if counter != 0:
                times.append(i[0])
                timesList.append(times) 
                times = []
            counter = 0
        if counter == 1:
            times.append(i[0])
            
    minPauseLength = 0.2 #seconds


    finalReturnTImes = []
    for i in range(0,len(timesList)):
        if timesList[i][1] - timesList[i][0] >= minPauseLength:
            pauses += 1
            finalReturnTImes.append([timesList[i][0], timesList[i][1]])
            plt.axvline(x=(timesList[i][1] - timesList[i][0])/2 + timesList[i][0], color='r')

    
    print(timesList)
    print(pauses)
    # Create a time array based on the time increment and number of steps
    time_increment = 0.01  # 100ms time increments
    num_steps = len(amplitudes)
    time = np.arange(num_steps) * time_increment

    # Plot the amplitudes over time

    plt.plot(time, amplitudes)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()
    return timesList

    '''
    print(timesList)
    print(pauses)

    # Create a time array based on the time increment and number of steps
    time_increment = 0.01  # 100ms time increments
    num_steps = len(amplitudes)
    time = np.arange(num_steps) * time_increment

    # Plot the amplitudes over time

    plt.plot(time, amplitudes)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()
    '''
    return finalReturnTImes
print(get_pauseTimes(r"VoiceFiles\\storytime.wav"))


