import numpy as np
import matplotlib.pyplot as plt
import socket
import pickle

array_size = 300

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.194', 12345))

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion() 

Z = np.zeros((array_size, array_size))

def update_plot(indices, data):
    x_indices = indices[1] 
    y_indices = indices[0] 
    ax.scatter(x_indices, y_indices, c='red', s=20) 
    plt.draw()
    plt.pause(0.001)

while True:
    data_length_bytes = client_socket.recv(4)
    data_length = int.from_bytes(data_length_bytes, byteorder='big')
    data_bytes = b""

    # Принимаем данные по блокам и собираем их 
    block_size = 4096
    remaining_bytes = data_length
    while remaining_bytes > 0:
        chunk = client_socket.recv(min(block_size, remaining_bytes))
        if not chunk:
            break
        data_bytes += chunk
        remaining_bytes -= len(chunk)

    indices_data, data = pickle.loads(data_bytes)

    indices = indices_data
    Z[indices] += data

    plt.clf()
    plt.imshow(Z, cmap='jet', extent=[-10, 10, -10, 10], origin='lower', interpolation='nearest')
    plt.colorbar()
    update_plot(indices, data)

plt.ioff() 
plt.show()

client_socket.close()
