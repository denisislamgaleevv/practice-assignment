import numpy as np
import matplotlib.pyplot as plt
import socket

# Размер массива
array_size = 100

# Создаем фигуру и оси для отображения данных
fig, ax = plt.subplots()

# Создаем изображение, которое будет обновляться
image = ax.imshow(np.zeros((array_size, array_size)), cmap='jet', extent=[-10, 10, -10, 10], origin='lower',
                  interpolation='nearest')

# Создаем цветовую шкалу
colorbar = plt.colorbar(image, ax=ax)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Real-time Plot')

# Функция для обновления изображения и цветовой шкалы
def update_image(Z):
    global array_size

    # Изменяем размер массива Z до желаемого размера
    Z.resize((array_size, array_size))

    image.set_data(Z)

    # Обновляем границы цветовой шкалы на основе текущих значений массива Z
    vmin = np.min(Z)
    vmax = np.max(Z)
    image.set_clim(vmin, vmax)

    plt.draw()


# Создаем клиентский сокет и подключаемся к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.194', 12345))
print('Connected to server')

# Получаем и отображаем данные в режиме реального времени
while True:
    data = client_socket.recv(array_size * array_size * 8) # 8 байт на каждое значение типа float64
    if not data:
        break

    # Проверяем, что размер данных является кратным размеру элемента
    if len(data)  != array_size * array_size * 8:
        continue

    # Преобразуем данные в массив numpy
    Z = np.frombuffer(data, dtype=np.float64)
    Z = Z.reshape((array_size, array_size))

    # Обновляем изображение и цветовую шкалу
    update_image(Z)
    plt.pause(0.001) #

# Закрываем соединение и окно с изображением
client_socket.close()
plt.close(fig)
