from instrument_control.camera import *
from instrument_control.stage import *
from data_processing.image_processing import *
import matplotlib.pyplot as plt 
import numpy as np

camera = Camera("Solid HHG Detector").initiate()
iris = Stage("Iris").initiate()
camera.set_exposure(1000000)
camera.set_gain(27)

def Oli_conversion(pix_array_length, mcp_height):
    coeff = [-5.29194209e-02,  56.6780912]
    offset = (5-mcp_height) * 881/4
    eV0 = (np.arange(pix_array_length)-offset) * coeff[0] + coeff[1]
    return 1240/eV0
iris.set_position(388)
bg = camera.photo_capture()
iris.set_position(370)
y_eV = Oli_conversion(bg.shape[1], 1)
ver = np.array(range(bg.shape[0]))
ver_mask = (ver>0)*(ver<bg.shape[0])
eV_mask = (y_eV<5)*(y_eV>35)
y_eV = y_eV[eV_mask]
ver = ver[ver_mask]
I = Image()

for i in range(2):
    fig, ax = plt.subplots(2)
    img = camera.photo_capture()
    proc = Image.quick_image(img, bg, 1, eV_mask, ver_mask, vmin, vmax)
    ax[0].set_title(i)
    ax[0].contourf(y_eV, ver, proc, aspect = 'auto')
    ax[1].plot(y_eV, proc.sum(0))
    plt.close(all)

