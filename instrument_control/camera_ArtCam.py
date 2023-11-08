import ctypes as ct
import numpy as np
from instrument_control.camera_universal import UniversalCamera

class ArtCam(UniversalCamera):
    """
    ArtCam camera class for EHD-407UV camera - works in windows only
    Could be implemented for any ArtCam camera but would require different parameters

    This is quick and dirty way of using dll directly in python to access a sensor
    """
    def __init__(self, name):
        #Camera specific values - could be generalised to different ArtCams 
        self.ss_lower = 7
        self.ss_upper = 1074
        self.g_lower = 0
        self.g_upper = 1023
        self.pixNo_V = 1024 
        self.pixNo_H = 1360 
        self.pixSize_H = 4.65 #micrometers
        self.pixSize_V = 4.65 #micrometers

        #Initialising parent function
        super().__init__(name)

    
    def initialise_camera(self):
        """ This opens the library module that python communicates with the camera"""
        self.library = ct.windll.LoadLibrary(r'dll\ArtCamSdk_407UV_WOM.dll')
        self.CamID = self.library.ArtCam_Initialize()
        # Lastly we will set the bit format of the image to be monochrome and 16 bits
        self.library.ArtCam_SetColorMode(self.CamID, ct.c_long(16))

    def open(self):
        # This is already implemented in intialise so no need for this one
        pass

    def close(self):
        self.library.ArtCam_Release(self.CamID)

    def get_exposure(self):
        return self.library.ArtCam_GetRealExposureTime(self.CamID, ct.c_bool(False))

    def get_exposure_limits(self):
        # the camera units of exposure are in integer shutter speed (H)
        # I defined a specific to this camera function that translates between (H)
        # and the real time in um for easy of use
        upper =  self.shutter_speed_conversion(self.ss_lower)
        lower =  self.shutter_speed_conversion(self.ss_upper)
        return lower, upper


    def get_gain_limits(self):
        # Not sure if the gain works properly
        lower = self.g_lower
        upper = self.g_upper 
        return lower, upper


    def get_gain(self):
        return self.library.ArtCam_GetGlobalGain(self.CamID, ct.c_bool(0))


    def set_exposure(self, new_value):
        self.library.ArtCam_SetRealExposureTime(self.CamID, ct.c_long(new_value))
        self.exposure = self.get_exposure()


    def set_gain(self, new_value):
        self.library.ArtCam_SetGlobalGain(self.CamID, ct.c_long(new_value))
        self.gain = self.get_gain()


    def frame_capture(self):
        # To get images in dll we need to allocate space for the image first
        # We do that by making an empty array and filling it later

        #Calculate the size of the image that will be passed
        im_height = self.pixNo_V 
        im_width = self.pixNo_H
        dwBufferSize = im_height*im_width 

        #Create an empty array
        grab_arr = np.zeros((im_height, im_width), dtype=np.uint16) #dtype should match the one set in intialisation

        #Get the Image 
        self.library.ArtCam_SnapShot(self.CamID, grab_arr.ctypes.data_as(ct.POINTER(ct.c_int16)), ct.c_long(dwBufferSize*2),0)
        return grab_arr

    def start_grab(self):
        self.library.ArtCam_Capture(self.CamID)
    
    def stop_grab(self):
        self.library.ArtCam_Close(self.CamID)

    def shutter_speed_conversion(self, ss):
        # specific to this camera from p.7:
        # https://artray.co.jp/wp-content/uploads/2022/07/INTRDUCTION_ARTCAM-407UV-WOM_220425_V102.pdf
        return ((1074-ss)*1790+424)*0.042

