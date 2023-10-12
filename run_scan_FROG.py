from experiment_control.scan_generator import *
from instrument_control.spectrometer import *
from instrument_control.stage import *
import time

spectrometer = Spectrometer("chamber").initiate()
tlim = spectrometer.get_timelim()
spectrometer.set_time(5e3)

frog_stage = Stage("FROG").initiate()



scan = ScanGenerator()
scan.set_detector(spectrometer)
scan.set_save_directory("Z:\\project\\electrondynamics\\live\\FROG\\August", "FROG_pumpbeam_long")
pos0 = frog_stage.get_position()
scan.add_axis(frog_stage, np.arange(pos0-0.15,pos0+0.18, 0.001))
scan.run_scan_spec(20, 365, 425)
scan.output_config()

