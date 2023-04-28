from instrument_control.spectrometer import *
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.animation import FuncAnimation
import os

spec = Spectrometer("chamber").initiate()
print('name of the file') 
spec.set_time(300e6)
for i in range(100):
    pass
# name_file = input()
N = 10
x, y = spec.get_spec()
wl = x

plt.plot(x,y)
plt.show()
folder = "Z:\\project\\laserprojectsmatthews\\live\\Kasia_RDS\\SolidHHG\\20230125"
file_name = os.path.join(folder, name_file)
# np.save(file_name+'_spectra', spec_array)
# np.save(file_name+'_wavelength', wl)


