from instrument_control.camera import *
import matplotlib.pyplot as plt 
import numpy as np

try:
    camera = Camera("007 Camera").initiate()
    camera.set_exposure(1e6)

    im = camera.photo_capture()
    camera.close()
    camera.vmb._shutdown()
except:
    camera.vmb._shutdown()

plt.imshow(im, vmax = 100)
plt.colorbar()
plt.show()

