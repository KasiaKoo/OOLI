from instrument_control.camera import *

my_camera = Camera("Solid HHG Detector").initiate()
my_camera.set_gain(27)
my_camera.set_exposure(10000000)

image = my_camera.photo_capture()

plt.show(image, vmin = None, vmax = None, aspect = 'auto', cmap='magma')
plt.colorbar()
plt.show()
