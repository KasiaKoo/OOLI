from experiment_control.scan_generator import *
from instrument_control.spectrometer import *
from instrument_control.stage import *
import time

# Initialising spectrometer - grabs the first one so make sure only one is plugged in
spectrometer = Spectrometer("chamber").initiate()

# Set exposure time in microseconds - 1e3 is milisecond 
spectrometer.set_time(1e5)

# initialise the stages you want to move - I added two to your stage list in assets
#mirror_stage = Stage("MirrorDelay").initiate()
wedge_stage = Stage("WedgeDelay").initiate()

# Starting up the scan
scan = ScanGenerator() #initialising an object
scan.set_detector(spectrometer) #setting detector

# Setting save directiory - first path is where you want to save it, second is the name of the folder you want the scan to be named
scan.set_save_directory("C:\\Users\\CLI\\OneDrive - Imperial College London (1)\\PhD\\09 Lab\Rose\Chiral LJ Work\\Chiral SHG\Raw data\\23.10.23", "Pulsescan_SFG_BBO")

# Adding axis to the scan - you can add as many as you want but top one is done last. 

#setting the scan parameters
m_init = wedge_stage.get_position() #getting the position you have now on the stage
print(m_init)

m_range = 3.0 #range in mm which you want to move on both sides
m_step_size = 0.25 #size of the step in mm 
#m_step_count = 400 #how many steps you need 

# adding axis first is the stage you're trying to add, second is the array you are adding 

scan.add_axis(wedge_stage, np.arange(m_init-m_range,m_init+m_range, m_step_size)) #this adds an array over the range with specific step size
#scan.add_axis(wedge_stage, [3,5,10])
#scan.add_axis(wedge_stage, np.linspace(m_init-m_range,m_init+m_range, m_step_count)) #you can swap to this one if you want specific number of steps 


#scan.run_scan_spec(no_averaging=100,repeats=1,lowest_wl= 350, highest_wl = 900) #averering and repeats must be at least 1!
scan.run_scan_spec_seperatedelays(no_averaging=1,repeats=100,lowest_wl= 200, highest_wl = 900)



