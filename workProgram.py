import numpy as np
import matplotlib.pyplot as plt

array_size = 100

try:
    Z = np.load('array.npy')
except FileNotFoundError:
    Z = np.empty((0, array_size, array_size))

drawing = False

def update_array(event):
    global Z, drawing

    if event.button == 1:
        if drawing:
            x, y = int(event.xdata), int(event.ydata)
            mu = [x, y]
            sigma = [[1, 0], [0, 1]]

            x_vals, y_vals = np.meshgrid(np.linspace(-10, 10, array_size), np.linspace(-10, 10, array_size))
            diff_x = x_vals - mu[0]
            diff_y = y_vals - mu[1]
            denominator = 2 * np.pi * np.sqrt(np.linalg.det(sigma))
            new_Z = np.exp(-(diff_x ** 2 + diff_y ** 2) / (2 * sigma[0][0])) / denominator

            Z = np.append(Z, [new_Z], axis=0)
        else:
            drawing = True

    elif event.button == 3:
        drawing = False

    plt.clf()  
    plt.imshow(np.sum(Z, axis=0), cmap='viridis', extent=[-10, 10, -10, 10], origin='lower')
    plt.colorbar()
    plt.draw()

def on_close():
    np.save('array.npy', np.sum(Z, axis=0))

plt.imshow(np.sum(Z, axis=0), cmap='viridis', extent=[-array_size//2, array_size//2, -array_size//2, array_size//2], origin='lower')
plt.colorbar()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Практика Роснефть')

cid_press = plt.connect('button_press_event', update_array)
cid_move = plt.connect('motion_notify_event', update_array)
cid_close = plt.connect('close_event', on_close)

plt.show()
