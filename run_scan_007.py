from matplotlib.cbook import weakref
from experiment_control.scan_generator import *
from instrument_control.camera import *
from instrument_control.stage import *
import time

camera = Camera("007 Camera").initiate()
camera.set_exposure(int(1e6))
camera.set_gain(1)

try:
    hwp_stage = Stage("HWP007").initiate()



    h_start = hwp_stage.get_position()
    time.sleep(5)

    scan = ScanGenerator()
    scan.set_detector(camera)
    scan.set_save_directory("C:\\Users\\Atto\\OneDrive - Imperial College London (1)\\Documents\\TESTOOLI", "Scan_test1")

    scan.add_axis(hwp_stage,np.arange(h_start-3,h_start+3 , 1))


    scan.run_scan()
    scan.output_config()
    camera.close()
except Exception as error:
    print('Failed Try')
    camera.close()
    print(error)
