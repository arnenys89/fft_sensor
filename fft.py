import numpy as np

def compute_fft(signal, sampling_rate):
    n = len(signal)
    fft_vals = np.fft.fft(signal)
    fft_vals = np.abs(fft_vals[:n // 2])

    freqs = np.fft.fftfreq(n, d=1/sampling_rate)
    freqs = freqs[:n // 2]

    return freqs, fft_vals


def dominant_frequency(signal, sampling_rate):
    freqs, fft_vals = compute_fft(signal, sampling_rate)
    idx = np.argmax(fft_vals)
    return freqs[idx], fft_vals[idx]
