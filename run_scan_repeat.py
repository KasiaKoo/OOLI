from experiment_control.scan_generator import *
from instrument_control.camera import *
from instrument_control.stage import *

camera = Camera("Solid HHG Detector").initiate()
camera.set_exposure(10000000)
camera.set_gain(27)

# wedge_stage = Stage("Wedge").initiate()
# lens_stage = Stage("Lens").initiate()
# hwp_stage = Stage("HWP").initiate()
#iris_stage = Stage("Iris").initiate()

scan = ScanGenerator()
scan.set_detector(camera)
scan.set_save_directory("Z:\\project\\laserprojectsmatthews\\live\\Kasia_RDS\\SolidHHG\\20221104", "Scan_MCP1800V_1p3cmMCP_800nm_f5p5mm_noaeroosols_longScan")


scan.run_repeats(6*25)
# scan.add_axis(hwp_stage, np.linspace(95,100,5)[::-1])
# scan.add_axis(lens_stage, np.linspace(0,30,5))
# scan.add_axis(wedge_stage, np.repeat(np.array([7, 13, 20, 25]),5))

# scan.run_scan()

#iris_stage.set_position(76)

