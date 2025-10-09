import numpy as np
import matplotlib.pyplot as plt

fc = 2e9  # Частота сигнала, Гц
c = 3e8   # Скорость света, м/с
λ = c / fc  # Длина волны, м
F = 16
dx = λ / F  # Шаг расстояния между точками, м
V = 0.01     # Скорость абонента, м/с
N = 100    # Количество точек траектории
D = 1000   # Расстояние до базовой станции, м
NFFT = 128 # Размер ДПФ

# Угол расположения базовой станции
alpha = 0  # радианы

# Координаты базовой станции
BSx = D * np.cos(alpha)
BSy = D * np.sin(alpha)

# Траектория движения абонента
mdx = np.arange(N) * dx

# Временные моменты (вектор)
ts = mdx / V

# Вектор расстояний от BS к MS
d_p = D - mdx

# Волновое число
k = 2 * np.pi / λ

# Принимаемый сигнал (комплексная амплитуда)
r = np.exp(-1j * k * d_p)

# Амплитуда и фаза сигнала
amplitude = np.abs(r)
phase = np.angle(r)

# Дискретизация по времени — отдельная переменная!
dt = dx / V
fs = 1 / dt  # частота дискретизации

# Выполняем ДПФ сигнала
r_fft = np.fft.fftshift(np.fft.fft(r, NFFT))

# Частотная ось для ДПФ
f_axis = np.arange(-NFFT/2, NFFT/2) * fs / NFFT

# Находим пик в спектре (доплеровскую частоту)
peak_index = np.argmax(np.abs(r_fft))
doppler_frequency = f_axis[peak_index]

plt.figure(figsize=(15, 10))

# График 1: Изменение расстояния d = f(t)
plt.subplot(2, 3, 1)
plt.plot(ts * 1000, d_p, 'b-', linewidth=2)
plt.xlabel('Время, мс')
plt.ylabel('Расстояние, м')
plt.title('Изменение расстояния от BS до MS')
plt.grid(True, alpha=0.3)

# График 2: Амплитуда как функция времени
plt.subplot(2, 3, 2)
plt.plot(ts * 1000, amplitude, 'r-', linewidth=2)
plt.xlabel('Время, мс')
plt.ylabel('Амплитуда')
plt.title('Амплитуда сигнала как функция времени')
plt.grid(True, alpha=0.3)
plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Амплитуда = 1.0')
plt.legend()

# График 3: Амплитуда как функция расстояния
plt.subplot(2, 3, 3)
plt.plot(d_p, amplitude, 'g-', linewidth=2)
plt.xlabel('Расстояние, м')
plt.ylabel('Амплитуда')
plt.title('Амплитуда сигнала как функция расстояния')
plt.grid(True, alpha=0.3)
plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Амплитуда = 1.0')
plt.legend()

# График 4: Фаза как функция времени
plt.subplot(2, 3, 4)
plt.plot(ts * 1000, phase, 'purple', linewidth=2)
plt.xlabel('Время, мс')
plt.ylabel('Фаза, рад')
plt.title('Фаза сигнала как функция времени')
plt.grid(True, alpha=0.3)

# График 5: Фаза как функция расстояния
plt.subplot(2, 3, 5)
plt.plot(d_p, phase, 'orange', linewidth=2)
plt.xlabel('Расстояние, м')
plt.ylabel('Фаза, рад')
plt.title('Фаза сигнала как функция расстояния')
plt.grid(True, alpha=0.3)

# График 6: Спектр сигнала (Доплеровское смещение)
plt.subplot(2, 3, 6)
plt.plot(f_axis, np.abs(r_fft), 'blue', linewidth=2)
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда спектра')
plt.title('Спектр сигнала (Доплеровское смещение)')
plt.grid(True, alpha=0.3)
plt.axvline(x=doppler_frequency, color='red', linestyle='--',
           label=f'Доплер: {doppler_frequency:.2f} Гц')
plt.legend()

plt.tight_layout()
plt.show()