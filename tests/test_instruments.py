from instrument_control.camera import *
from instrument_control.stage import *
import time
import matplotlib.pyplot as plt
from experiment_control.scan_generator import *

my_camera = Camera("Solid HHG Detector").initiate()

print("Camera Params")
print("----------------------------------------------------------------------")

print("Camera Gain:")
print(my_camera.gain)
print(my_camera.gain_lower, my_camera.gain_upper)

print("Changing Gain to 5...")
my_camera.set_gain(5)
print(my_camera.gain)

print("Camera Exposure")
print(my_camera.exposure)
print(my_camera.exposure_lower, my_camera.exposure_upper)

print("Changing Exposure to 50000...")
my_camera.set_exposure(50000)
print(my_camera.exposure)

print("Taking picture...")
image = my_camera.photo_capture()
plt.imshow(image)
plt.show()

print("Resetting exposure and gain...")
my_camera.set_exposure(10000)
my_camera.set_gain(0)

my_camera.camera.Close()

print()
print("----------------------------------------------------------------------")
print()

my_stage = Stage("Lens").initiate()
print("Stage Params")
print("----------------------------------------------------------------------")

print("Stage Position")
print(my_stage.get_position())
print(my_stage.position_lower, my_stage.position_upper)
print(my_stage.lock)

print("Changing Stage Position to 5...")
my_stage.set_position(5)
print(my_stage.get_position())
my_stage.enable_lock()

print(my_stage.lock)
print(my_stage.get_position())

print("Changing Stage Position to 0...")
my_stage.set_position(0)

my_stage.disable_lock()
print("Changing Stage Position to 0...")
my_stage.set_position(0)

my_stage.enable_lock()
print(my_stage.get_position())

print()
print("----------------------------------------------------------------------")
print()

