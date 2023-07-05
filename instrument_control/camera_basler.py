from pypylon import pylon

class Basler():
    """
    Basler camera class
    """
    def __init__(self, name):

        # open camera
        # TODO: generalise to multiple basler cameras
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()

        self.name = name
        self.exposure = self.get_exposure()
        self.gain = self.get_gain()
        self.gain_lower, self.gain_upper = self.get_gain_limits()
        self.exposure_lower, self.exposure_upper = self.get_exposure_limits()


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


    def photo_capture(self):
        self.camera.StartGrabbing()
        photo = self.frame_capture()
        self.camera.StopGrabbing()
        return photo

    def photo_capture_repeat(self, repeat=1):
        self.camera.StartGrabbing()
        photo = 0
        for i in range(repeat):
            photo = photo + self.frame_capture()
        self.camera.StopGrabbing()


    def close(self):
        self.camera.Close()
