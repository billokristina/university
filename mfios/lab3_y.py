import numpy as np
import matplotlib.pyplot as plt

fc = 2e9  # Частота сигнала, Гц
c = 3e8   # Скорость света, м/с
λ = c / fc  # Длина волны, м
F = 16
Δx = λ / F  # Шаг расстояния между точками, м
V = 10     # Скорость абонента, м/с
N = 100    # Количество точек траектории
D = 1000   # Расстояние до базовой станции, м
NFFT = 128 # Размер ДПФ

# Угол расположения базовой станции
alpha = 0  # радианы (базовая станция на оси Y)

# Координаты базовой станции
BSx = D * np.cos(alpha)
BSy = D * np.sin(alpha)

# Траектория движения абонента с составляющей Y
# Пример 1: Движение под углом 30 градусов к оси X
theta = np.radians(30)  # угол движения относительно оси X

x_points = np.arange(N) * Δx * np.cos(theta)  # составляющая X
y_points = np.arange(N) * Δx * np.sin(theta)  # составляющая Y

# Временные моменты
t_points = np.arange(N) * Δx / V  # время одинаковое для обеих компонент

# Вектор расстояний от BS к MS (теперь используем точную формулу)
d_points = np.sqrt((BSx - x_points)**2 + (BSy - y_points)**2)

# Волновое число
k = 2 * np.pi / λ

# Принимаемый сигнал (комплексная амплитуда)
r = np.exp(-1j * k * d_points)

# Амплитуда и фаза сигнала
amplitude = np.abs(r)
phase = np.angle(r)  # радианы

# Вычисление доплеровского смещения
ts = Δx / V  # интервал дискретизации
fs = 1 / ts  # частота дискретизации

# ДПФ сигнала
r_fft = np.fft.fftshift(np.fft.fft(r, NFFT))
f_axis = np.arange(-NFFT/2, NFFT/2) * fs / NFFT
peak_index = np.argmax(np.abs(r_fft))
doppler_frequency = f_axis[peak_index]

# Визуализация
plt.figure(figsize=(16, 12))

# График 2: Изменение расстояния
plt.subplot(2, 3, 2)
plt.plot(t_points * 1000, d_points, 'b-', linewidth=2)
plt.xlabel('Время, мс')
plt.ylabel('Расстояние, м')
plt.title('Изменение расстояния от BS до MS')
plt.grid(True, alpha=0.3)

# График 3: Амплитуда сигнала
plt.subplot(2, 3, 3)
plt.plot(t_points * 1000, amplitude, 'r-', linewidth=2)
plt.xlabel('Время, мс')
plt.ylabel('Амплитуда')
plt.title('Амплитуда сигнала')
plt.grid(True, alpha=0.3)
plt.axhline(y=1.0, color='black', linestyle='--', alpha=0.5)

# График 4: Фаза сигнала
plt.subplot(2, 3, 4)
plt.plot(t_points * 1000, phase, 'purple', linewidth=2)
plt.xlabel('Время, мс')
plt.ylabel('Фаза, рад')
plt.title('Фаза сигнала')
plt.grid(True, alpha=0.3)

# График 5: Скорость изменения расстояния (радиальная скорость)
radial_velocity = np.gradient(d_points, t_points)
plt.subplot(2, 3, 5)
plt.plot(t_points * 1000, radial_velocity, 'orange', linewidth=2)
plt.xlabel('Время, мс')
plt.ylabel('Радиальная скорость, м/с')
plt.title('Скорость изменения расстояния')
plt.grid(True, alpha=0.3)
plt.axhline(y=-V * np.cos(theta), color='red', linestyle='--', 
           label=f'Теоретическая: {-V * np.cos(theta):.2f} м/с')
plt.legend()

# График 6: Спектр сигнала
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

# Одномерный случай для сравнения
d_points_1d = D - x_points / np.cos(theta)  # Эквивалентное расстояние для 1D
r_1d = np.exp(-1j * k * d_points_1d)
doppler_1d = V / λ  # Теоретическое доплеровское смещение для 1D