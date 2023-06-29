import numpy as np
import matplotlib.pyplot as plt
import socket


array_size = 400


fig, ax = plt.subplots()

image = ax.imshow(np.zeros((array_size, array_size)), cmap='jet', extent=[-10, 10, -10, 10], origin='lower',
                  interpolation='nearest')

colorbar = plt.colorbar(image, ax=ax)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Клиент')

def update_image(Z):
    global array_size

    Z.resize((array_size, array_size))

    image.set_data(Z)

    vmin = np.min(Z)
    vmax = np.max(Z)
    image.set_clim(vmin, vmax)

    plt.draw()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.194', 12345))
print('Connected to server') 
while True:
    data = client_socket.recv(array_size * array_size * 8)  
    if not data:
        break

    
    if len(data)  != array_size * array_size * 8:
        continue

    
    Z = np.frombuffer(data, dtype=np.float64)
    Z = Z.reshape((array_size, array_size))

    
    update_image(Z)
    plt.pause(0.001) 

 
client_socket.close()
plt.close(fig)
