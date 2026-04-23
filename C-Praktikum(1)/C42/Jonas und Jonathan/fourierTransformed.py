import numpy as np
import matplotlib.pyplot as plt
import cmath
import math
from scipy.fft import fft, fftfreq, ifft

data = [0.347, 0.5775, 0.807, 0.4825, 0.365, 0.5274, 0.8877, 0.7125, 0.6920, 0.4610, 0.5514, 0.8314, 0.852, 0.5391,
        0.5270, 0.7102, 0.8870, 0.588, 0.434, 0.5497, 0.7296, 0.5324, 0.2730, 0.2948, 0.4154, 0.4174, 0.114, 0.038,
        0.0983, 0.1845, 0.0576, -0.0454, -0.0437, 0.0035, 0.015, -0.065, -0.0837, -0.0561, 0.0145, -0.01, -0.0712,
        -0.0653]

x_data = [2 * j for j in range(100, 59, -1)]
x_data.append(185)
x_data.sort(reverse=True)

fft = fft(data)
plt.scatter(x_data, data, c="red")
plt.plot(x_data, data, c="red")
plt.show()


n = len(data)
stepsize = 2

freq = fftfreq(n, d=stepsize)
plt.scatter(freq, np.abs(fft))
plt.show()

fft[7:11] = 0
fft[32:36] = 0
fft[20:23] = 0

plt.scatter(freq, np.abs(fft))
plt.show()

new_data = ifft(fft)
print(np.real(new_data))

plt.scatter(x_data, new_data, c="blue")
plt.plot(x_data, new_data, c="blue")
plt.scatter(x_data, data, c="red")
plt.plot(x_data, data, c="red")
plt.show()



