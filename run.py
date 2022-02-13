from experiment_control.scan_generator import *
from instrument_control.camera import *
from instrument_control.stage import *

camera = Camera("Solid HHG Detector").initiate()
camera.set_exposure(1000000)
camera.set_gain(27)

wedge_stage = Stage("Wedge").initiate()
lens_stage = Stage("Lens").initiate()

scan = ScanGenerator()
scan.set_detector(camera)
scan.set_save_directory("..", "OOLI_Test")

scan.add_axis(wedge_stage, np.linspace(0, 1, 2))
scan.add_axis(lens_stage, np.linspace(3, 4, 3))

scan.run_scan()

