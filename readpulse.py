import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, irfft, rfftfreq

video_path = "pulse.mp4"  
cap = cv2.VideoCapture(video_path)

green_channel_values = []
fps = int(cap.get(cv2.CAP_PROP_FPS)) 
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    green_channel = frame[:, :, 1] 
    green_channel_values.append(np.mean(green_channel))  

cap.release()

signal = np.array(green_channel_values)

mean_signal = signal - np.mean(signal)

plt.figure(figsize=(12, 4))
plt.plot(mean_signal, color='green', label='Mean Normalized Signal')
plt.title("Mean Normalized Green Channel Signal")
plt.xlabel("Frame")
plt.ylabel("Intensity")
plt.legend()
plt.show(block=False)  

freqs = rfftfreq(len(mean_signal), d=1/fps)  
fft_values = rfft(mean_signal)  

plt.figure(figsize=(12, 4))
plt.plot(freqs, np.abs(fft_values), label='FFT Amplitude')
plt.title("Frequency Spectrum of the Signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.xlim(0, 10)  
plt.legend()
plt.show(block=False)  

low, high = 0.45, 8  
filtered_fft = np.where((freqs < low) | (freqs > high), 0, fft_values)

filtered_signal = irfft(filtered_fft)

plt.figure(figsize=(12, 4))
plt.plot(filtered_signal, color='blue', label="Filtered Signal")
plt.title("Filtered Signal (After Removing Unwanted Frequencies)")
plt.xlabel("Frame")
plt.ylabel("Intensity")
plt.legend()
plt.show(block=False)  

dominant_freq = freqs[np.argmax(np.abs(filtered_fft))]  

bpm = dominant_freq * 60
print(f"Estimated Heart Rate: {bpm:.2f} BPM")

plt.show()
