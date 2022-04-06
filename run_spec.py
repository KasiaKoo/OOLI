from instrument_control.spectrometer import *
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.animation import FuncAnimation

spectrometer = Spectrometer("chamber").initiate()

fig, ax = plt.subplots()
x, y = spectrometer.get_spec()
line, = ax.plot(x,y)


def update(i):
    x, y = spectrometer.get_spec()
    line.set_data(x,y)
    return line

ani = FuncAnimation(plt.gcf(), update, frames=range(100), interval=5, blit=False)

plt.show()
