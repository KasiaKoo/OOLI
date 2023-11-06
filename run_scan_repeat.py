from experiment_control.scan_generator import *
from instrument_control.camera import *
from instrument_control.stage import *

camera = Camera("Solid HHG Detector").initiate()
camera.set_exposure(int(10e6))
camera.set_gain(27)

# wedge_stage = Stage("Wedge").initiate()
#lens_stage = Stage("Lens").initiate()
# hwp_stage = Stage("HWP").initiate()
#iris_stage = Stage("Iris").initiate()

scan = ScanGenerator()
scan.set_detector(camera)
scan.set_save_directory("Z:\\project\\electrondynamics\\live\\20230908", "StabilityScan_Mcp3p5cm_1850V")

# scan.set_save_directory("Z:\\project\\electrondynamics\\live\\20230627", "test")
# scan.set_save_directory("C:\\Users\\reddragon\\Documents\\Data", "Timestamps")


scan.run_repeats(60, lims=[0,3600,2000,4000], save='png')
#scan.add_axis(lens_stage, [50])
# scan.add_axis(hwp_stage, np.repeat(np.append(np.linspace(156,201,10), np.linspace(198.5,158.5,9)),1))
# scan.add_axis(hwp_stage, np.repeat(np.linspace(156,201,10),1))
# scan.add_axis(hwp_stage,np.repeat([156],3))
# scan.add_axis(hwp_stage,[110,114])
# scan.add_axis(wedge_stage, np.repeat(np.array([7, 13, 20, 25]),5))

#hwp_stage.set_position(int(112))

# scan.run_scan(repeat=6)
# scan.output_config()

#iris_stage.set_position(76)

