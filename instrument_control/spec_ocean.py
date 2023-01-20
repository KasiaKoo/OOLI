import seabreeze
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import Spectrometer, list_devices
import matplotlib.pyplot as plt
import numpy as np

class OceanOptics:

    def __init__(self, name):
        #TODO: generalise to multiple
        self.spec = Spectrometer.from_first_available()
        self.name = name
        

    def get_spec(self):
        wl = self.spec.wavelengths()
        I = self.spec.intensities()
        return wl, I

    def get_timelim(self):
        tlim = self.spec.integration_time_micros_limits
        return tlim

    def set_time(self,x):
        self.spec.integration_time_micros(x)





