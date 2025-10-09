import numpy as np
import matplotlib.pyplot as plt

# Параметры задачи
fc = 2e9  # 2 ГГц - несущая частота
c = 3e8   # скорость света
F = 16    # коэффициент передискретизации
lambda_ = c / fc  # длина волны
V = 10    # скорость движения абонента (м/с)
N = 100   # количество точек измерения
NFFT = 128 # размер БПФ для спектрального анализа
D = 1000  # базовое расстояние до отражателей (м)

# Шаг по оси x (пространственное разрешение)
delta_x = lambda_ / F

# Временные отсчёты (время прохождения между точками измерения)
t = np.arange(N) * delta_x / V

# Количество переотражений (многолучевых компонент)
M = 20

# Моделирование релеевских замираний: амплитуды с Рэлеевским распределением по точкам и отражениям
# Рэлеевское распределение моделирует случайные изменения амплитуды сигнала
amplitudes = np.random.rayleigh(scale=1.0, size=(N, M))

# Случайные фазы для каждого отражения в каждой точке
# Равномерное распределение фаз от 0 до 2π
phases = np.random.uniform(0, 2 * np.pi, size=(N, M))

# Задержки отражённых сигналов с разбросом вокруг базового расстояния
# Каждое отражение имеет случайное расстояние в пределах 10 шагов от базового
delays = D - np.random.uniform(0, 10 * delta_x, M)

# Волновое число
k = 2 * np.pi / lambda_

# ========== МОДЕЛИРОВАНИЕ СИГНАЛА ==========

# Формирование сигнала для каждой точки траектории с суммой переотражений с Рэлеевским распределением
r_rayleigh = np.zeros(N, dtype=complex)
for i in range(N):
    # Для каждой точки траектории вычисляем сумму сигналов от всех отражателей
    # Каждый компонент имеет случайную амплитуду (Рэлеевскую) и случайную фазу
    r_rayleigh[i] = np.sum(amplitudes[i, :] * np.exp(1j * phases[i, :]) * np.exp(-1j * k * delays))

# Вычисление спектра Доплера
R_fft = np.fft.fftshift(np.fft.fft(r_rayleigh, NFFT))
fs = 1 / (delta_x / V)  # частота дискретизации
f_doppler = np.fft.fftshift(np.fft.fftfreq(NFFT, d=1/fs))

# ========== ГРАФИК 1: ГЕОМЕТРИЯ СЦЕНАРИЯ ==========
plt.figure(1, figsize=(10, 8))

# Траектория движения абонента (прямолинейное движение)
x_trajectory = np.linspace(0, (N-1)*delta_x, N)  # координаты по x
y_trajectory = np.zeros(N)  # движение вдоль оси x

# Положение отражателей (случайное распределение в пространстве)
reflector_x = np.random.uniform(-50, 50, M)  # случайные x координаты
reflector_y = np.random.uniform(800, 1200, M)  # отражатели в районе базового расстояния

plt.plot(x_trajectory, y_trajectory, 'b-', linewidth=2, label='Траектория абонента')
plt.plot(x_trajectory, y_trajectory, 'bo', markersize=4, alpha=0.6)
plt.plot(reflector_x, reflector_y, 'ro', markersize=6, label='Отражатели')
plt.xlabel('Координата X, м')
plt.ylabel('Координата Y, м')
plt.title('Геометрия сценария: движение абонента и отражатели')
plt.legend()
plt.grid(True)
plt.axis('equal')

# ========== ГРАФИК 2: АМПЛИТУДА СИГНАЛА ==========
plt.figure(2, figsize=(10, 6))
plt.plot(np.abs(r_rayleigh), 'g-', linewidth=2, label='Амплитуда сигнала')
plt.xlabel('Точки траектории')
plt.ylabel('Амплитуда')
plt.title('Амплитуда сигнала (Релеевские замирания)')
plt.legend()
plt.grid(True)

# ========== ГРАФИК 3: ФАЗА СИГНАЛА ==========
plt.figure(3, figsize=(10, 6))
plt.plot(np.angle(r_rayleigh), 'purple', linewidth=2, label='Фаза сигнала')
plt.xlabel('Точки траектории')
plt.ylabel('Фаза, радианы')
plt.title('Фаза сигнала')
plt.legend()
plt.grid(True)

# ========== ГРАФИК 4: СПЕКТР ДОПЛЕРА ==========
plt.figure(4, figsize=(10, 6))
plt.plot(f_doppler, np.abs(R_fft), 'r-', linewidth=2, label='Спектр Доплера')
plt.xlabel('Частота Доплера, Гц')
plt.ylabel('Амплитуда')
plt.title('Спектр Доплера')
plt.legend()
plt.grid(True)

# ========== ОТОБРАЖЕНИЕ ВСЕХ ГРАФИКОВ ОДНОВРЕМЕННО ==========
plt.show()

# ========== ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ ==========
print("ПАРАМЕТРЫ МОДЕЛИ:")
print(f"Несущая частота: {fc/1e9} ГГц")
print(f"Длина волны: {lambda_:.3f} м")
print(f"Скорость движения: {V} м/с")
print(f"Количество точек измерения: {N}")
print(f"Количество переотражений: {M}")
print(f"Базовое расстояние: {D} м")
print(f"Пространственный шаг: {delta_x:.3f} м")
print(f"Временной шаг: {delta_x/V:.3f} с")

# Расчет теоретической доплеровской частоты
f_doppler_max = V / lambda_
print(f"\nТеоретическая максимальная доплеровская частота: {f_doppler_max:.2f} Гц")
print(f"Наблюдаемый диапазон доплеровских частот: от {f_doppler.min():.2f} до {f_doppler.max():.2f} Гц")

# Анализ замираний
signal_power = np.mean(np.abs(r_rayleigh)**2)
fading_depth = np.max(np.abs(r_rayleigh)**2) / np.min(np.abs(r_rayleigh)**2)
print(f"\nСредняя мощность сигнала: {signal_power:.2f}")
print(f"Глубина замираний: {10*np.log10(fading_depth):.2f} дБ")