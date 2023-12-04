import vmbpy 
from instrument_control.camera_universal import UniversalCamera

class VMB(UniversalCamera):
    """
    VMB camera class
    """
    def __init__(self, name):
        super().__init__(name)

    def initialise_camera(self):
        # Try to generalise to multiple cameras - find id or something
        with vmbpy.VmbSystem.get_instance() as vmb:
            cams = vmb.get_all_cameras()
            if not cams:
                print('No valid camera plugged in')
        #As only single camera is available its the first one
        self.camera = cams[0] 

    def open(self):
        self.camera.Open()

    def close(self):
        self.camera.Close()

    def get_exposure(self):
        return self.camera.ExposureTimeAbs()


    def get_exposure_limits(self):
        # Not sure have to check on comp
        lower = 0 #self.camera.ExposureTimeAbs.GetMin()
        upper = 100# self.camera.ExposureTimeAbs.GetMax()
        return lower, upper


    def get_gain_limits(self):
        #Not Sure have to check on the comp
        lower = 0 #self.camera.Gain.GetMin()
        upper = 1000 #self.camera.Gain.GetMax()
        return lower, upper


    def get_gain(self):
        # gain in dB
        return self.camera.Gain.get()


    def set_exposure(self, new_value):
        self.camera.ExposureTimeAbs.set(new_value)
        self.exposure = self.get_exposure()


    def set_gain(self, new_value):
        self.camera.Gain.set(new_value)
        self.gain = self.get_gain()


    def frame_capture(self):
        grab_result = self.camera.get_frame()
        grab_result.convert_pixel_format(PixelFormat.Mono8)
        img = grab_result.as_numpy_ndarray()
        return img

    def start_grab(self):
        #no way to initialise there is _shutdown and _startup but not sure
        pass
        # self.camera.StartGrabbing()
    
    def stop_grab(self):
        #no way to initialise there is _shutdown and _startup but not sure
        pass
        # self.camera.StopGrabbing()

