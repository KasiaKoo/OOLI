from instrument_control.camera import *
from instrument_control.stage import *

my_camera = Camera("Basler").initiate()
print("Camera Params")
print("-----------------")
print(my_camera.gain)
print(my_camera.gain_lower, my_camera.gain_upper)
print(my_camera.exposure)
print(my_camera.exposure_lower, my_camera.exposure_upper)
print()

my_stage = Stage("ThorLabs").initiate()
print("Stage Params")
print("-----------------")
print(my_stage.position)
print(my_stage.position_lower, my_stage.position_upper)


