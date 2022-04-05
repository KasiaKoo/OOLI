import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
fig = Figure()
ax = fig.add_subplot(1,1,1)
im = ax.plot(np.random.randn(10,10))

# def update(i):
#     A = np.random.randn(10+i,10+i)
#     im.set_array(A)
#     return im

# ani = FuncAnimation(fig, update, interval=5, blit=False)
plt.show()

