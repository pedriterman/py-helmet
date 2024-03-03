import pyaudio
import numpy as np
import scipy.signal as signal

# Constants for audio processing
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()


# Function to create Clone Trooper helmet effect
def clone_trooper_effect(data):
    # Applying metallic filter
    filtered_data = signal.lfilter([1, -0.5], [1], data)

    # Applying distortion
    distortion_factor = 0.7
    distorted_data = np.int16(filtered_data * (1 + distortion_factor * np.random.uniform(-1, 1, len(filtered_data))))

    # Applying modulation effect
    modulation_factor = 0.005
    modulated_data = np.int16(distorted_data * (1 + modulation_factor * np.sin(np.arange(len(distorted_data)) * 0.1)))

    return modulated_data


# Callback function for audio stream
def callback(in_data, frame_count, time_info, status):
    data = np.frombuffer(in_data, dtype=np.int16)
    modified_data = clone_trooper_effect(data)
    return modified_data.tobytes(), pyaudio.paContinue


# Open audio stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

# Start audio stream
print("Clone Trooper helmet effect started. Press Ctrl+C to stop.")
stream.start_stream()

try:
    while stream.is_active():
        pass
except KeyboardInterrupt:
    print("Clone Trooper helmet effect stopped.")

# Close audio stream
stream.stop_stream()
stream.close()
audio.terminate()
