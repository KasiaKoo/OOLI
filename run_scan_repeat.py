from experiment_control.scan_generator import *
from instrument_control.camera import *
from instrument_control.stage import *

camera = Camera("Solid HHG Detector").initiate()
camera.set_exposure(int(10e6))
camera.set_gain(27)

# wedge_stage = Stage("Wedge").initiate()
lens_stage = Stage("Lens").initiate()
hwp_stage = Stage("HWP").initiate()
#iris_stage = Stage("Iris").initiate()

scan = ScanGenerator()
scan.set_detector(camera)
scan.set_save_directory("Z:\\project\\electrondynamics\\live\\20230627", "Scan_hwp112_fscan-highf_c00_n25p7mbar_noaerosols_MCP3p0_800nm")
# scan.set_save_directory("Z:\\project\\electrondynamics\\live\\20230627", "test")
# scan.set_save_directory("C:\\Users\\reddragon\\Documents\\Data", "Timestamps")


#scan.run_repeats(10)
scan.add_axis(lens_stage, np.linspace(40,50,20))
#scan.add_axis(hwp_stage, np.repeat(np.logspace(np.log10(85),np.log10(112),30, base=10), 2))
# scan.add_axis(hwp_stage,[110,114])
# scan.add_axis(wedge_stage, np.repeat(np.array([7, 13, 20, 25]),5))

#hwp_stage.set_position(int(112))

scan.run_scan()
scan.output_config()

#iris_stage.set_position(76)

