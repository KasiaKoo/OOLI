from matplotlib.cbook import weakref
from experiment_control.scan_generator import *
from instrument_control.camera import *
from instrument_control.stage import *
import time

camera = Camera("UV Camera").initiate()
camera.set_exposure(int(73150))
camera.set_gain(918)

hwp_stage = Stage("HWP").initiate()
lens_stage = Stage("Lens").initiate()
wedge_stage = Stage("Wedge").initiate()

scan = ScanGenerator()
scan.set_detector(camera)
scan.set_save_directory("L:\\reddragon\\data-rep\\SolidHHG\\20231124", "Scan_UVCam_quartz100_1400nm_5th_hwp+wedgescan")

#scan.add_axis(hwp_stage,np.repeat(np.arange(24,26,0.1), 5))
scan.add_axis(hwp_stage,[35,50,66,70])
# scan.add_axis(lens_stage, np.repeat(np.arange(0, 40,5),5))
scan.add_axis(wedge_stage, np.repeat(np.linspace(0, 25,9),5))


scan.run_scan(lims=[350,650, 0,1360], repeat=30)
scan.output_config()

