import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, ifft
import io

# 1. Подготовка данных
data_string = """
0	-0,017666512
6	3,51860095
12	6,433736407
18	8,31880889
24	10,07613615
30	11,49757721
36	12,64414731
42	13,26124002
48	14,72131249
54	15,30874274
60	16,1815506
66	17,15434933
72	17,58897077
78	17,00971123
84	15,76740312
90	14,44608817
96	13,86322722
102	13,45172791
108	13,07988524
114	12,99371943
120	12,91008182
126	12,82440846
132	12,70437579
138	12,40262563
144	12,07355505
150	11,46827585
156	10,64437233
162	9,194453215
168	6,774990769
174	3,355177571
180	0,011142167
"""

data = io.StringIO(data_string)
# Читаем данные и разделяем их
x_values = []
y_values = []

for line in data:
    line = line.strip()  # Убираем лишние пробелы в начале и конце
    if line:  # Проверяем, что строка не пустая
        try:
            parts = line.split()
            x = int(parts[0])  # Первая часть - индекс (x)
            y_str = parts[1].replace(',', '.')  # Заменяем запятую на точку
            y = float(y_str)  # Вторая часть - значение (y)
            x_values.append(x)
            y_values.append(y)
        except (ValueError, IndexError) as e:
            print(f"Ошибка при обработке строки: {line}. Ошибка: {e}")

x = np.array(x_values)
y = np.array(y_values)

# 2. Вычисление быстрого преобразования фурье
N = len(y)
yf = fft(y, norm="ortho")
xf = fftfreq(N, d=(x[1]-x[0]))  # Частоты

def phase_shift(): #график номер 1
    phases = np.angle(yf[1:6])
    plt.figure(figsize=(10, 6))
    plt.bar(range(1, 6), phases, tick_label=[f' {i}' for i in range(1, 6)])
    plt.xlabel("Номер гармоники")
    plt.ylabel("Сдвиг фазы ( радианы )")
    plt.title("Сдвиг фаз для гармоник")
    plt.grid(True)
    
    plt.show()

def phase_spectr():
    plt.figure(figsize=(10, 6))
    plt.plot(xf[1:N//2], np.angle(yf[1:N//2])) # Отображаем только положительные частоты и отбрасываем постоянную составляющую
    plt.xlabel("Частота")
    plt.ylabel("Сдвиг фазы ( радианы )")
    plt.title("Спектр фаз")
    plt.grid(True)
    plt.show()

def amplitude_view(): # график номер 2
    amplitudes = np.abs(yf[1:16])
    plt.figure(figsize=(12, 6))  # Увеличиваем размер графика для лучшей читаемости
    plt.bar(range(1, 16), amplitudes, tick_label=[f' {i}' for i in range(1, 16)])
    plt.xlabel("Номер гармоники")
    plt.ylabel("Амплитуда")
    plt.title("Амплитуды первых 15 гармоник")
    plt.grid(True)
    plt.show()

def amplitude_spectr():
    plt.figure(figsize=(12, 6))
    plt.plot(xf[1:N//2], np.abs(yf[1:N//2]))
    plt.xlabel("Частота")
    plt.ylabel("Амплитуда")
    plt.title("Спектр амплитуда")
    plt.grid(True)
    plt.show()

def garmonic_session(): # график номер 3
    yf_truncated = np.copy(yf)
    # Сохраняем 15 положительных и 15 отрицательных частот
    yf_truncated[15+1:N-15] = 0  # обнуляем все, кроме первых 15 и последних 15

    y_reconstructed = ifft(yf_truncated, norm="ortho")

    plt.figure(figsize=(12, 6))
    plt.plot(x, y,'o', label="Оригинальный сигнал", color="blue")
    plt.plot(x, np.real(y_reconstructed), label="Восстановленный сигнал ( 15 гармоник )", color="orange")  # Take real part
    plt.xlabel("Угол поворота, град.")
    plt.ylabel("Момент, Нм")
    plt.title("График разложение сигнала")
    plt.legend()
    plt.grid(True)
    plt.xticks(np.arange(min(x), max(x)+1, 30))
    plt.show()

def garmo_single_plotter():
    plt.figure(figsize=(10, 6))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Гармоники ( фаза занулена )")
    plt.grid(True)

    for i in range(1, 6):
        yf_single_harmonic = np.zeros_like(yf, dtype=complex)
        yf_single_harmonic[i] = np.abs(yf[i])
        yf_single_harmonic[N-i] = np.abs(yf[N-i])

        y_single_harmonic = ifft(yf_single_harmonic)

        plt.plot(x, np.real(y_single_harmonic), label=f"Гармоника {i}")

    plt.legend()
    plt.show()

def garmo_multi_plotter():
    fig, axes = plt.subplots(5, 1, figsize=(10, 15))  # Создаем 5 subplot'ов в одном столбце

    for i in range(1, 6):
        yf_single_harmonic = np.zeros_like(yf, dtype=complex)
        # Зануляем фазу и оставляем мнимую часть (синус), инвертируем для положительной области
        yf_single_harmonic[i] = -1j * np.abs(yf[i])  # Представляем как мнимое число, инвертируем
        yf_single_harmonic[N-i] = 1j * np.abs(yf[i]) # Комплексное сопряжение для отриц. частот, инвертируем

        y_single_harmonic = ifft(yf_single_harmonic)

        ax = axes[i-1]  # Получаем доступ к нужному subplot'у
        ax.plot(x, np.real(y_single_harmonic))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"Гармоника {i} (Фаза занулена)")
        ax.grid(True)

    plt.tight_layout()  # Предотвращает перекрытия subplot'ов
    plt.show()
#phase_shift()
#amplitude_view()
garmonic_session()
#garmo_multi_plotter()

def calculate_modified_harmonic_coefficient(signal, sampling_rate, fundamental_frequency, num_harmonics=15):
    N = len(signal)
    yf = fft(signal)

    def find_frequency_index(frequency):
        return np.argmin(np.abs(np.fft.fftfreq(N, 1/sampling_rate) - frequency))

    # Индекс для 3-й гармоники
    harmonic_3rd_frequency = 3 * fundamental_frequency
    harmonic_3rd_index = find_frequency_index(harmonic_3rd_frequency)

    #  амплитуда 3-й гармоники
    harmonic_3rd_amplitude = 2 * np.abs(yf[harmonic_3rd_index]) / N

    # Вычисляем корень из суммы квадратов амплитуд первых num_harmonics гармоник
    sum_of_squares = 0.0
    for i in range(1, num_harmonics + 1):
        harmonic_frequency = i * fundamental_frequency
        harmonic_index = find_frequency_index(harmonic_frequency)
        harmonic_amplitude = 2 * np.abs(yf[harmonic_index]) / N
        sum_of_squares += harmonic_amplitude ** 2

    root_sum_of_squares = np.sqrt(sum_of_squares)

    #Проверяем, что знаменатель не равен 0
    if root_sum_of_squares == 0:
        print("error.")
        return None

    # Вычисляем нормированный коэффициент
    coefficient = harmonic_3rd_amplitude / root_sum_of_squares

    return coefficient

coefficient = calculate_modified_harmonic_coefficient(y, 5, 15, num_harmonics=15)

if coefficient is not None:
    print(f" коэффициент 3-й гармоники: {coefficient}")
