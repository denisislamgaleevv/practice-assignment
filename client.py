import socket
import matplotlib.pyplot as plt
 
from PIL import Image

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('37.112.20.173', 12345)   
client_socket.connect(server_address) 
#136.169.224.176 КИРИЛЛ 37.112.20.173
# Создаем окно для отображения рисунка
fig, ax = plt.subplots()

while True:
    
    image_bytes = b''
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        image_bytes += data

    
    img = Image.frombytes('RGB', (600, 400), image_bytes)
    plt.imshow(img)

   
    plt.pause(0.001)

 
client_socket.close()
