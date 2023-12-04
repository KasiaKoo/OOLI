from instrument_control.camera import *
import matplotlib.pyplot as plt 
import numpy as np

camera = Camera("007 Camera").initiate()

im = camera.photo_capture()

plt.imshow(im, vmax = 100)
plt.colorbar()
plt.show()

