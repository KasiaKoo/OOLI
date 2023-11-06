from pypylon import pylon
from camera_universal import UniversalCamera

class Basler(UniversalCamera):
    """
    Basler camera class
    """
    def __init__(self, name):
        super.__init__(name)

    def initialise_camera(self):
        """ This creates self.camera module links to the basler python patch"""
        # TODO: generalise to multiple basler cameras
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    
    def open(self):
        self.camera.Open()

    def close(self):
        self.camera.Close()

    def get_exposure(self):
        return self.camera.ExposureTime.GetValue()


    def get_exposure_limits(self):
        lower = self.camera.ExposureTime.GetMin()
        upper = self.camera.ExposureTime.GetMax()
        return lower, upper


    def get_gain_limits(self):
        lower = self.camera.Gain.GetMin()
        upper = self.camera.Gain.GetMax()
        return lower, upper


    def get_gain(self):
        return self.camera.Gain.GetValue()


    def set_exposure(self, new_value):
        self.camera.ExposureTime.SetValue(new_value)
        self.exposure = self.get_exposure()


    def set_gain(self, new_value):
        self.camera.Gain.SetValue(new_value)
        self.gain = self.get_gain()


    def frame_capture(self):
        grab_result = self.camera.RetrieveResult(20000, pylon.TimeoutHandling_ThrowException)
        img = grab_result.Array.astype(int)
        return img

    def start_grab(self):
        self.camera.StartGrabbing()
    
    def stop_grab(self):
        self.camera.StopGrabbing()

