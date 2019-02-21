"""
Purpose: To create individual audio files for all 88 piano
keys in the Youtube video here:
https://www.youtube.com/watch?v=dHb8R5gDvgM
"""

import numpy as np
import librosa
import matplotlib.pyplot as plt
import scipy.io as sio
import subprocess
import os

if __name__ == '__main__':
    y, fs = librosa.load("PianoKeys/pianokeys.mp3")
    z = np.cumsum(y**2)
    w = z[4096::] - z[0:-4096]
    w = np.array(w > 1e-12, dtype=float)
    idx = np.arange(w.size-1)[w[1::]-w[0:-1] == 1]
    idx = idx.tolist()
    idx = [0] + idx + [y.size]
    for i in range(len(idx)-1):
        yi = y[idx[i]:idx[i+1]]
        sio.wavfile.write("%i.wav"%i, fs, yi)
        subprocess.call(["ffmpeg", "-i", "%i.wav"%i, "PianoKeys/%i.mp3"%i])
        os.remove("%i.wav"%i)