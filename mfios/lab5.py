import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft
from mpl_toolkits.mplot3d import Axes3D

# ========== ПАРАМЕТРЫ ЗАДАНИЯ ==========
fc = 2e9  # 2 ГГц - несущая частота
c = 3e8   # скорость света
F = 16    # коэффициент передискретизации
lambda_ = c / fc  # длина волны
V = 10    # скорость движения абонента (м/с)
N = 20    # количество точек траектории (по заданию)
delta_x = lambda_ / F  # шаг расстояния между точками

# Параметры полосы частот
f_start = 1997.5e6  # 1997.5 МГц
f_end = 2002.5e6    # 2002.5 МГц
delta_f = 0.01e6     # шаг частотной сетки 0.01 МГц

# Коэффициенты передачи рассеивателей
alpha1 = 1.0
alpha2 = 0.5

# ========== РАСЧЕТ ЧАСТОТНОЙ СЕТКИ ==========
frequencies = np.arange(f_start, f_end + delta_f, delta_f)
Nf = len(frequencies)  # количество точек частотной характеристики

# ========== ГЕОМЕТРИЯ СЦЕНАРИЯ ==========
# Положение базовой станции (BS)
BS_x, BS_y = 0, 0

# Траектория движения мобильной станции (MS)
x_trajectory = np.arange(N) * delta_x
y_trajectory = np.zeros(N)

# Положение двух рассеивателей
scatterer1_x, scatterer1_y = 300, 200
scatterer2_x, scatterer2_y = -30, 80

# ========== РАСЧЕТ РАССТОЯНИЙ И ЗАДЕРЖЕК ==========
# Расстояния от BS к рассеивателям и к MS
d_BS_MS = np.sqrt((x_trajectory - BS_x)**2 + (y_trajectory - BS_y)**2)
d_BS_S1 = np.sqrt((scatterer1_x - BS_x)**2 + (scatterer1_y - BS_y)**2)
d_BS_S2 = np.sqrt((scatterer2_x - BS_x)**2 + (scatterer2_y - BS_y)**2)
d_S1_MS = np.sqrt((x_trajectory - scatterer1_x)**2 + (y_trajectory - scatterer1_y)**2)
d_S2_MS = np.sqrt((x_trajectory - scatterer2_x)**2 + (y_trajectory - scatterer2_y)**2)

# Полные задержки для каждого луча
tau_direct = d_BS_MS / c
tau_scatter1 = (d_BS_S1 + d_S1_MS) / c
tau_scatter2 = (d_BS_S2 + d_S2_MS) / c

# ========== МОДЕЛИРОВАНИЕ ЧАСТОТНОЙ ХАРАКТЕРИСТИКИ ==========
H_freq = np.zeros((N, Nf), dtype=complex)

for i in range(N):  # по точкам траектории
    for j, f in enumerate(frequencies):  # по частотам
        k = 2 * np.pi * f / c  # волновое число для текущей частоты
        
        # Прямой луч + два рассеянных луча
        H_freq[i, j] = (np.exp(-1j * k * d_BS_MS[i]) + 
                        alpha1 * np.exp(-1j * k * (d_BS_S1 + d_S1_MS[i])) +
                        alpha2 * np.exp(-1j * k * (d_BS_S2 + d_S2_MS[i])))

# ========== РАСЧЕТ ИМПУЛЬСНОЙ ХАРАКТЕРИСТИКИ ==========
# Параметры для импульсной характеристики
tau_max = 1 / delta_f
delta_tau = tau_max / Nf
tau_axis = np.arange(Nf) * delta_tau

# Импульсная характеристика для каждой точки траектории
h_impulse = np.zeros((N, Nf), dtype=complex)
for i in range(N):
    h_impulse[i, :] = ifft(H_freq[i, :]) * Nf  # ОДПФ

# ========== ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ ==========

# 1. Диаграмма размещения BS, MS, траектории перемещения MS
plt.figure(1, figsize=(12, 8))
plt.plot(BS_x, BS_y, 'ro', markersize=12, label='Базовая станция (BS)')
plt.plot(x_trajectory, y_trajectory, 'b-', linewidth=2, label='Траектория MS')
plt.plot(x_trajectory, y_trajectory, 'bo', markersize=4, alpha=0.6)
plt.plot(scatterer1_x, scatterer1_y, 's', color='orange', markersize=10, label='Рассеиватель 1')
plt.plot(scatterer2_x, scatterer2_y, 's', color='green', markersize=10, label='Рассеиватель 2')

# Показать линии распространения для начальной точки
i_start = 0
plt.plot([BS_x, x_trajectory[i_start]], [BS_y, y_trajectory[i_start]], 'k--', alpha=0.5, label='Прямой луч')
plt.plot([BS_x, scatterer1_x, x_trajectory[i_start]], [BS_y, scatterer1_y, y_trajectory[i_start]], 'r--', alpha=0.5, label='Луч через рассеиватель 1')
plt.plot([BS_x, scatterer2_x, x_trajectory[i_start]], [BS_y, scatterer2_y, y_trajectory[i_start]], 'g--', alpha=0.5, label='Луч через рассеиватель 2')

plt.xlabel('Координата X, м')
plt.ylabel('Координата Y, м')
plt.title('Диаграмма размещения BS, MS и траектории перемещения')
plt.legend()
plt.grid(True)
plt.axis('equal')

# 2. ТРЕХМЕРНЫЙ ГРАФИК: Переменная во времени частотная характеристика (модуль) по траектории
fig = plt.figure(2, figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Создание сетки для 3D графика
time_axis = x_trajectory / V
freq_GHz = frequencies / 1e9
T, F = np.meshgrid(time_axis, freq_GHz, indexing='ij')

# Модуль ЧХ в децибелах
H_db = 20 * np.log10(np.abs(H_freq) + 1e-10)

# Построение поверхности
surf = ax.plot_surface(F, T, H_db, cmap='viridis', alpha=0.8, 
                      linewidth=0, antialiased=True)

# Настройка осей
ax.set_xlabel('Частота, ГГц')
ax.set_ylabel('Время, с')
ax.set_zlabel('Модуль ЧХ, дБ')
ax.set_title('3D: Частотная характеристика канала по времени и частоте')

# Добавление цветовой шкалы
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Модуль ЧХ, дБ')

# Установка угла обзора
ax.view_init(elev=30, azim=45)

# 3. Модуль ЧХ на выбранной частоте от времени
plt.figure(3, figsize=(10, 6))
selected_freq_idx = Nf // 2  # центральная частота
plt.plot(time_axis, 20*np.log10(np.abs(H_freq[:, selected_freq_idx])), 'b-', linewidth=2)
plt.xlabel('Время, с')
plt.ylabel('Модуль ЧХ, дБ')
plt.title(f'Модуль ЧХ на частоте {frequencies[selected_freq_idx]/1e6:.2f} МГц')
plt.grid(True)

# 4. Модуль ЧХ во всей полосе в выбранной точке траектории
plt.figure(4, figsize=(10, 6))
selected_point_idx = N // 2  # средняя точка траектории
plt.plot(freq_GHz, 20*np.log10(np.abs(H_freq[selected_point_idx, :])), 'r-', linewidth=2)
plt.xlabel('Частота, ГГц')
plt.ylabel('Модуль ЧХ, дБ')
plt.title(f'Модуль ЧХ в точке траектории {selected_point_idx} (x={x_trajectory[selected_point_idx]:.2f} м)')
plt.grid(True)

# 5. Фаза ЧХ во всей полосе в выбранной точке траектории
plt.figure(5, figsize=(10, 6))
plt.plot(freq_GHz, np.angle(H_freq[selected_point_idx, :]), 'purple', linewidth=2)
plt.xlabel('Частота, ГГц')
plt.ylabel('Фаза ЧХ, радианы')
plt.title(f'Фаза ЧХ в точке траектории {selected_point_idx} (x={x_trajectory[selected_point_idx]:.2f} м)')
plt.grid(True)

# 6. Импульсная характеристика по траектории
tau_ns = tau_axis * 1e9  # наносекунды

# 7. Импульсная характеристика в выбранной точке траектории
plt.figure(6, figsize=(10, 6))
plt.plot(tau_ns, 20*np.log10(np.abs(h_impulse[selected_point_idx, :]) + 1e-10), 'b-', linewidth=2)
plt.xlabel('Задержка, нс')
plt.ylabel('Модуль ИХ, дБ')
plt.title(f'Импульсная характеристика в точке траектории {selected_point_idx}')
plt.grid(True)

plt.tight_layout()
plt.show()

# ========== ВЫВОД ИНФОРМАЦИИ ==========
print("ПАРАМЕТРЫ МОДЕЛИ:")
print(f"Несущая частота: {fc/1e9} ГГц")
print(f"Длина волны: {lambda_:.3f} м")
print(f"Скорость движения: {V} м/с")
print(f"Количество точек траектории: {N}")
print(f"Полоса частот: {f_start/1e6}-{f_end/1e6} МГц")
print(f"Шаг частотной сетки: {delta_f/1e3} кГц")
print(f"Количество точек ЧХ: {Nf}")
print(f"Коэффициенты рассеивателей: α1={alpha1}, α2={alpha2}")

print(f"\nПАРАМЕТРЫ ИМПУЛЬСНОЙ ХАРАКТЕРИСТИКИ:")
print(f"Максимальная задержка: {tau_max*1e9:.2f} нс")
print(f"Шаг по задержке: {delta_tau*1e9:.2f} нс")
print(f"Количество точек ИХ: {Nf}")

print(f"\nГЕОМЕТРИЯ:")
print(f"BS позиция: ({BS_x}, {BS_y}) м")
print(f"Рассеиватель 1: ({scatterer1_x}, {scatterer1_y}) м, коэффициент: {alpha1}")
print(f"Рассеиватель 2: ({scatterer2_x}, {scatterer2_y}) м, коэффициент: {alpha2}")
print(f"Длина траектории: {x_trajectory[-1]:.2f} м")
print(f"Время наблюдения: {time_axis[-1]:.2f} с")