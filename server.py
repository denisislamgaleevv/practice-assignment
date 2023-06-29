import numpy as np
import matplotlib.pyplot as plt
import socket
import pickle

array_size = 300

 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.194', 12345))
server_socket.listen(1)
print('Waiting for client connection...')

client_socket, client_address = server_socket.accept()
print('Client connected:', client_address)
 
try:
    Z = np.load('array.npy')
except FileNotFoundError:
    Z = np.zeros((array_size, array_size))

drawing = False
prev_x, prev_y = None, None

def update_array(event):
    global Z, drawing, prev_x, prev_y

    if event.button == 1:
        if drawing:
            x, y = int(event.xdata), int(event.ydata)
            mu = [x, y]
            sigma = [[1, 0], [0, 1]]

            new_Z = np.exp(-(np.square(X - mu[0]) + np.square(Y - mu[1])) / (2 * sigma[0][0])) / (
                2 * np.pi * np.sqrt(np.linalg.det(sigma))
            )

            indices = np.nonzero(new_Z) 
            data = new_Z[indices] 

            Z[indices] += data

            prev_x, prev_y = x, y
        else:
            drawing = True
            prev_x, prev_y = int(event.xdata), int(event.ydata)

    elif event.button == 3:
        drawing = False

    plt.clf()
    plt.imshow(Z, cmap='jet', extent=[-10, 10, -10, 10], origin='lower', interpolation='nearest')
    plt.colorbar()
    plt.draw()

    if 'indices' in locals() and 'data' in locals():
        indices_data = (indices, data)
        data_bytes = pickle.dumps(indices_data)

        client_socket.sendall(data_bytes)

def on_close(event):
    np.save('array.npy', Z) 
    client_socket.close()
    server_socket.close()

x = np.linspace(-10, 10, array_size)
y = np.linspace(-10, 10, array_size)
X, Y = np.meshgrid(x, y)

plt.imshow(Z, cmap='jet', extent=[-10, 10, -10, 10], origin='lower', interpolation='nearest')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Сервер')

cid_press = plt.connect('button_press_event', update_array) 
cid_move = plt.connect('motion_notify_event', update_array) 
cid_close = plt.connect('close_event', on_close)  

plt.show()
