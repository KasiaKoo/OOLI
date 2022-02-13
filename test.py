from instrument_control.camera import *
from instrument_control.stage import *
import time

my_camera = Camera("Solid HHG Detector").initiate()

print("Camera Params")
print("-----------------")

print("Camera Gain:")
print(my_camera.gain)
print(my_camera.gain_lower, my_camera.gain_upper)
time.sleep(1)

print("Changing Gain to 5...")
my_camera.set_gain(5)
print(my_camera.gain)
time.sleep(1)

print("Camera Exposure")
print(my_camera.exposure)
print(my_camera.exposure_lower, my_camera.exposure_upper)
time.sleep(1)

print("Changing Exposure to 50000...")
my_camera.set_exposure(50000)
print(my_camera.exposure)
time.sleep(1)

print("Resetting exposure and gain...")
my_camera.set_exposure(10000)
my_camera.set_gain(0)


print()

my_stage = Stage("Lens").initiate()
print("Stage Params")
print("-----------------")

print("Stage Position")
print(my_stage.get_position())
print(my_stage.position_lower, my_stage.position_upper)
print(my_stage.hold)
time.sleep(1)

print("Changing Stage Position to 5...")
my_stage.set_position(5)
print(my_stage.get_position())

my_stage.toggle_lock()
print(my_stage.hold)
print(my_stage.get_position())

print("Changing Stage Position to 0...")
my_stage.set_position(0)
time.sleep(1)

my_stage.toggle_lock()
print("Changing Stage Position to 0...")
my_stage.set_position(0)

time.sleep(10)
print(my_stage.get_position())

