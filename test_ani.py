import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
im = ax.imshow(np.random.randn(10,10))

def update(i):
    A = np.random.randn(10+i,10+i)
    im.set_array(A)
    return im

# ani = FuncAnimation(fig, update, interval=5, blit=False)
plt.show()

for i in range(3):
    update(i)
