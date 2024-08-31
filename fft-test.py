import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return np.exp(1j * x) * x


def idft(X):
    N = len(X)
    n = np.arange(0, N, 1)
    zs = np.array(
        [1 / N * X * np.exp(1j * 2 * np.pi * k * n / N) for k, X in enumerate(X)]
    )
    return np.sum(zs, axis=0)


X = np.arange(0, 100, 0.1)
Y = f(X)

N = len(X)
Xfft = np.fft.fftfreq(N)
Yfft = np.fft.fft(Y, N)

ifft = np.fft.ifft(Yfft)
ifft2 = idft(Yfft)

plt.plot(ifft.real, ifft.imag, "bo")
plt.plot(ifft2.real, ifft2.imag, "ro")
plt.axis("equal")
plt.xlim([-10, 10])
plt.ylim([-10, 10])
plt.show()
