#libraries
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import soundfile as sf
import hashlib
from typing import List, Tuple
from scipy import signal
from scipy.io import wavfile
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (binary_erosion,
                                      generate_binary_structure,
                                      iterate_structure)


#constants
wsize = 4096
wratio = 0.5
CONNECTIVITY_MASK = 8
DEFAULT_AMP_MIN = 10
DEFAULT_FAN_VALUE = 5  # 15 was the original value.

#read the audio file
#data, samplerate = sf.read('Lavender_Town_Japan.wav')
samplerate,data = wavfile.read('Lavender_Town_Japan.wav')
#convert to mono the signal
data = np.mean(data, axis=1)
print(samplerate)
#samplig input signal to 44100Hz
samplerate = 44100
#data= signal.resample(data, int(len(data)*samplerate/len(data)))
segmentSize=2
seconds = data.shape[0] / samplerate
segments = seconds / segmentSize
samplesPerSegment = int(data.shape[0] / segments)
#plot the audio file in time domain
plt.plot(data)
plt.show()

#continuos time processing
#using the fast fourier transform to convert the audio file to frequency domain
#fft = np.fft.fft(data)
#plot the audio file in frequency domain
#plt.plot(fft)
#plt.show()
plt.plot(data)
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.subplot(212)
plt.specgram(data[0:samplesPerSegment],Fs=samplerate, mode='psd')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.show()


fft = np.fft.fft(data)
#peack finding from spectrogram
#peaks, _ = signal.find_peaks(fft, height=0)
#plt.plot(peaks, fft[peaks], "x")
#plt.plot(np.zeros_like(fft), "--", color="gray")
#plt.show()
#FFT the signal and extract frequency components
arr2D = mlab.specgram(data,NFFT=wsize,Fs=44100,window=mlab.window_hanning,noverlap=int(wsize * wratio))[0]

    # Apply log transform since specgram function returns linear array. 0s are excluded to avoid np warning.
arr2D = 10 * np.log10(arr2D, out=np.zeros_like(arr2D), where=(arr2D != 0))

#graphical representation of the spectrogram
plt.imshow(arr2D, cmap='hot', interpolation='nearest')
plt.show()

#peack finding from spectrogram
def get_peaks(inputsignal,amp_min):
    struct = generate_binary_structure(2, CONNECTIVITY_MASK)
    neighborhood = iterate_structure(struct, 20)
    # Find local peaks using our fliter shape. Filtro pasa altos
    local_max = maximum_filter(inputsignal, footprint=neighborhood) == inputsignal
    background = (inputsignal == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    # Boolean mask of arr2D with True at peaks.
    detected_peaks = local_max ^ eroded_background
    # Extract peaks
    amps = inputsignal[detected_peaks]
    freqs, times = np.where(detected_peaks)
    # Filter peaks
    amps = amps.flatten()
    #Get indices for frequency and time
    filteridx = np.where(amps > amp_min)
    freqs_filter = freqs[filteridx]
    times_filter = times[filteridx]

    #scatter plot of the peaks
    fig, ax = plt.subplots()
    ax.imshow(inputsignal)
    ax.scatter(times_filter, freqs_filter, c='r')
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency')
    ax.set_title('Spectrogram')
    plt.gca().invert_yaxis()
    plt.show()

    return list(zip(freqs_filter, times_filter))


get_peaks(arr2D, DEFAULT_AMP_MIN)