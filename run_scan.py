from matplotlib.cbook import weakref
from experiment_control.scan_generator import *
from instrument_control.camera import *
from instrument_control.stage import *
import time

camera = Camera("Solid HHG Detector").initiate()
camera.set_exposure(int(10e6))
camera.set_gain(27)

# wedge_stage = Stage("Wedge").initiate()
# lens_stage = Stage("Lens").initiate()
# c_stage = Stage("Compression").initiate()
hwp_stage = Stage("HWP").initiate()
# rot_stage = Stage("ROT").initiate()
# FW_stage = Stage("Filter Wheel").initiate()
# iris_stage = Stage("Iris").initiate()


# lens_stage.set_position(12.5)
# c_stage.set_position(5.3)
# hwp_stage.set_position(114)
# time.sleep(5)

# print(lens_stage.get_position())
# print(c_stage.get_position())
# print(hwp_stage.get_position())

scan = ScanGenerator()
scan.set_detector(camera)
scan.set_save_directory("Z:\\project\\electrondynamics\\live\\20230908", "Scan_MCP3p5cm1850V_5p4mbar_iris33_fullpower300_delay9p0_labair_powerscan_WITHpump")
#c_stage.set_position(5.1462)
# mid_pos = c_stage.get_position()
# scan.add_axis(c_stage, np.repeat(np.linspace(mid_pos-0.3,mid_pos+0.3,7),12))
# scan.add_axis(hwp_stage, np.repeat([5.0,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,13.0,15.0],3))
# scan.add_axis(rot_stage, np.repeat(np.linspace(5,185,18),18))
# scan.add_axis(hwp_stage,[25,22,16,13,10,5,0])
scan.add_axis(hwp_stage,np.arange(45,65 , 2))
# scan.add_axis(lens_stage, np.arange(18.6, 27.8,0.2))
#scan.add_axis(FW_stage, np.repeat(np.array([0,120,240]),6*20))
# scan.add_axis(wedge_stage, np.repeat(np.linspace(10,25,9),24))
# scan.add_axis(iris_stage, np.repeat(np.linspace(47,45,7),30))

#scan.run_repeats(20*6)
scan.run_scan(lims=[0,3600, 2000,4000], repeat=3)
scan.output_config()
#iris_stage.set_position(76)
# hwp_stage.set_position(25)
