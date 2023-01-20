from instrument_control.spectrometer import *
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.animation import FuncAnimation
import os

spec = Spectrometer("chamber").initiate()
print('name of the file') 
spec.set_time(1e6)
name_file = input()
N = 10 
x, y = spec.get_spec()
wl = x
spec_array = np.zeros((N, y.shape[0]))

for i in range(N):
    x, y = spec.get_spec()
    spec_array[i] = y

folder = "Z:\\project\\laserprojectsmatthews\\live\\Kasia_RDS\\SolidHHG\\20221031"
file_name = os.path.join(folder, name_file)
np.save(file_name+'_spectra', spec_array)
np.save(file_name+'_wavelength', wl)


