from instrument_control.camera import *
import matplotlib.pyplot as plt

my_camera = Camera("Solid HHG Detector").initiate()
my_camera.set_gain(27)
my_camera.set_exposure(3000000)

image = my_camera.photo_capture()

plt.imshow(image, vmin = None, vmax = None, aspect = 'auto', cmap='magma')
plt.colorbar()
plt.show()
