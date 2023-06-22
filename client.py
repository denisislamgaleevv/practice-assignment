import socket
import cv2
import numpy as np
# IP-адрес и порт сервера
server_ip = '192.168.0.194'
server_port = 12345

# Создание сокета и подключение к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
print('Connected to the server.')

# Получение и отображение данных от сервера
while True:
    # Получение размера изображения
    image_size_bytes = client_socket.recv(4)
    image_size = int.from_bytes(image_size_bytes, 'big')

    # Получение данных изображения
    image_data = b''
    while len(image_data) < image_size:
        data = client_socket.recv(8096) #4096 *2 = 81?ө
        if not data:
            break
        image_data += data

    # Преобразование данных изображения в массив numpy
    image_array = bytearray(image_data)
     
    np_array = np.asarray(image_array, dtype=np.uint8)
    print(np_array)
    # Преобразование массива в изображение OpenCV
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Отображение изображения
    cv2.imshow('Image', image)
    cv2.waitKey(1)

# Закрытие соединения
client_socket.close()
