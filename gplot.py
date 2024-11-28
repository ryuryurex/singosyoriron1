from pydub import AudioSegment
import wave
import numpy as np
import matplotlib.pyplot as plt

input_filename = 'aiueo.wav'
output_filename = 'aiueo_pcm.wav'

audio = AudioSegment.from_wav(input_filename)
audio.export(output_filename, format='wav', codec='pcm_s16le')

with wave.open(output_filename, 'r') as wav_file:
    sample_rate = wav_file.getframerate()
    n_frames = wav_file.getnframes()
    n_channels = wav_file.getnchannels()

    audio_data = wav_file.readframes(n_frames)
    
audio_array = np.frombuffer(audio_data, dtype=np.int16)

if n_channels == 2:
    audio_array = audio_array[::2]

time = np.linspace(0, n_frames / sample_rate, num=n_frames)

plt.figure(figsize=(10, 4))
plt.plot(time, audio_array)
plt.title('Time Domain Waveform')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

