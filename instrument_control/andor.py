import PyAndor
from seabreeze.spectrometers import Spectrometer, list_devices
import matplotlib.pyplot as plt
import numpy as np


def get_pic(spec = Spectrometer.from_first_available(), safe=False, file ='spectrum.npz'):
    wl = spec.wavelengths()
    I = spec.intensities()
    if safe==True:
        np.savez(file, wl, I)
    return wl, I

def move_stage(stageidx = 0., pos = 0., wait=False):
    print('Moved the Virtual Stage')
    pass

devices = list_devices()
spec = Spectrometer(devices[0])
spec.integration_time_micros(100)

def scan_trace(stageidx = 0., pos = 0., wait=False, cam = Spectrometer.from_first_available(), step_list = range(10),safe=False, file ='FROG.npz'):
    FROG_spectra = np.zeros(len(spec_list))
    for i in range(len(step_list)):
        move_stage(step_list[i])
        wl, I = get_spec(spec)
        FROG_spectra[i] = [wl,I]

    if safe==True:
        np.savez(file,FROG)


cam = Andor()
cam.SetDemoReady()
cam.StartAcquisition()
data = []
cam.GetAcquiredData(data)
cam.SaveAsTxt("raw.txt")
cam.ShutDown()






