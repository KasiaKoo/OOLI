from experiment_control.scan_generator import *
from instrument_control.spectrometer import *
from instrument_control.stage import *
import time

spectrometer = Spectrometer("chamber").initiate()
tlim = spectrometer.get_timelim()
spectrometer.set_time(1e3)

frog_stage = Stage("FROG").initiate()

scan = ScanGenerator()
scan.set_detector(spectrometer)
scan.set_save_directory("C:\\Users\\CLI\\OneDrive - Imperial College London (1)\\PhD\\09 Lab\Rose\\Autocorrelation\\23.10.23", "Frog012_lowexposure")
pos0 = frog_stage.get_position()
scan.add_axis(frog_stage, np.arange(pos0-0.4,pos0+0.4, 0.002))

scan.run_scan_FROG(20, 360, 450)
scan.output_config()


