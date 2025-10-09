import numpy as np
import matplotlib.pyplot as plt

N = 10000

h_i = np.random.normal(0, 0.5, N)
h_q = np.random.normal(0, 0.5, N)

h = h_i + 1j * h_q

amplitude = np.abs(h)
phase = np.angle(h)

corr_full = np.correlate(h, h, mode='full')
corr = corr_full[N-1:]
lags = np.arange(0, len(corr))

plt.figure(figsize=(15, 10))

plt.subplot(4,1,1)
plt.hist(h_i, bins=1000, color='blue', alpha=0.7, density=True)
plt.title('Распределение $h_i$ (ин-фаза)')
plt.xlabel('$h_i$')
plt.ylabel('Плотность вероятности')

plt.subplot(4,1,2)
plt.hist(h_q, bins=1000, color='blue', alpha=0.7, density=True)
plt.title('Распределение $h_q$ (квадратура)')
plt.xlabel('$h_q$')
plt.ylabel('Плотность вероятности')

plt.subplot(4,1,3)
plt.hist(amplitude, bins=1000, color='blue', alpha=0.7, density=True)
plt.title('Распределение амплитуды $|h|$')
plt.xlabel('$|h|$')
plt.ylabel('Плотность вероятности')

plt.subplot(4,1,4)
plt.hist(phase, bins=1000, color='blue', alpha=0.7, density=True)
plt.title(r'Распределение аргумента $\arg(h)$ (фаза)')
plt.xlabel('Угол (радианы)')
plt.ylabel('Плотность вероятности')

plt.figure(figsize=(8, 6))
plt.plot(lags, np.abs(corr) / np.abs(corr[0]))
plt.title('Автокорреляция комплексного отклика $h$')
plt.xlabel('Сдвиг')
plt.ylabel('Нормированная автокорреляция')
plt.grid(True)

plt.tight_layout(pad=3.0)
plt.subplots_adjust(hspace=0.5)
plt.show()