import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import socket

array_size = 100
 
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

            Z += new_Z

            prev_x, prev_y = x, y
        else:
            drawing = True
            prev_x, prev_y = int(event.xdata), int(event.ydata)

    elif event.button == 3:
        drawing = False

    plt.clf()   
    plt.imshow(Z, cmap='viridis', extent=[-10, 10, -10, 10], origin='lower')
    plt.colorbar()
    plt.draw()

  
    fig = plt.gcf()
    fig.canvas.draw()
    image = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())

 
    with io.BytesIO() as output:
        image.save(output, format='JPEG')
        image_bytes = output.getvalue()

 
    image_size = len(image_bytes).to_bytes(4, 'big')  
    client_socket.sendall(image_size + image_bytes)

def on_close():
    np.save('array.npy', Z)
    client_socket.close()
    server_socket.close()

x = np.linspace(-10, 10, array_size)
y = np.linspace(-10, 10, array_size)
X, Y = np.meshgrid(x, y)

plt.imshow(Z, cmap='viridis', extent=[-10, 10, -10, 10], origin='lower')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Практика Роснефть')

cid_press = plt.connect('button_press_event', update_array)
cid_move = plt.connect('motion_notify_event', update_array)
cid_close = plt.connect('close_event', on_close)

plt.show()
