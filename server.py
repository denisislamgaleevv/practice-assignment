import numpy as np
import matplotlib.pyplot as plt
import socket

array_size = 100

# Создаем серверный сокет и ждем подключения клиента
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.194', 12345))
server_socket.listen(1)
print('Waiting for client connection...')

client_socket, client_address = server_socket.accept()
print('Client connected:', client_address)

# Загружаем массив Z из файла или создаем новый массив, если файл не найден
try:
    Z = np.load('array.npy')
except FileNotFoundError:
    Z = np.zeros((array_size, array_size))

drawing = False
prev_x, prev_y = None, None

def update_array(event):
    global Z, drawing, prev_x, prev_y

    if event.button == 1:
        # Левая кнопка мыши нажата
        if drawing:
            # Если уже рисуется, обновляем массив Z в соответствии с положением мыши
            x, y = int(event.xdata), int(event.ydata)
            mu = [x, y]
            sigma = [[1, 0], [0, 1]]

            new_Z = np.exp(-(np.square(X - mu[0]) + np.square(Y - mu[1])) / (2 * sigma[0][0])) / (
                2 * np.pi * np.sqrt(np.linalg.det(sigma))
            )

            Z += new_Z

            prev_x, prev_y = x, y
        else:
            # Если только начинается рисование, запоминаем положение мыши
            drawing = True
            prev_x, prev_y = int(event.xdata), int(event.ydata)

    elif event.button == 3:
        # Правая кнопка мыши нажата
        drawing = False

    # Очищаем текущий график и отображаем массив Z
    plt.clf()
    plt.imshow(Z, cmap='jet', extent=[-10, 10, -10, 10], origin='lower', interpolation='nearest')
    plt.colorbar()
    plt.draw()

    # Преобразуем массив Z в тип float64, вытягиваем его в одномерный массив и отправляем клиенту
    Z_bytes = Z.astype(np.float64).flatten().tobytes()
    client_socket.sendall(Z_bytes)

def on_close(event):
    # Событие закрытия графического окна
    np.save('array.npy', Z)  # Сохраняем массив Z в файл
    client_socket.close()
    server_socket.close()

# Создаем сетку значений x и y
x = np.linspace(-10, 10, array_size)
y = np.linspace(-10, 10, array_size)
X, Y = np.meshgrid(x, y)

# Отображаем начальный массив Z на графике
plt.imshow(Z, cmap='jet', extent=[-10, 10, -10, 10], origin='lower', interpolation='nearest')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Практика Роснефть')

# Подключаем обработчики событий
cid_press = plt.connect('button_press_event', update_array)  # Нажатие кнопки мыши
cid_move = plt.connect('motion_notify_event', update_array)  # Движение мыши
cid_close = plt.connect('close_event', on_close)  # Закрытие графического окна

plt.show()
