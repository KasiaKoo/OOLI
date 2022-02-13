from instrument_control.camera import *
from instrument_control.stage import *

my_camera = Camera("Basler").initiate()

print("Camera Params")
print("-----------------")

print("Camera Gain:")
print(my_camera.gain)
print(my_camera.gain_lower, my_camera.gain_upper)

print("Changing Gain to 15...")
my_camera.set_gain(15)
print(my_camera.gain)

print("Camera Exposure")
print(my_camera.exposure)
print(my_camera.exposure_lower, my_camera.exposure_upper)

print("Changing Exposure to 20000...")
my_camera.set_exposure(20000)
print(my_camera.exposure)


print()

my_stage = Stage("ThorLabs").initiate()
print("Stage Params")
print("-----------------")

print("Stage Position")
print(my_stage.position)
print(my_stage.position_lower, my_stage.position_upper)

print("Changing Stage Position to 2...")
my_stage.set_position(2)
print(my_stage.position)

