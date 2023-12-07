import vmbpy 
from instrument_control.camera_universal import UniversalCamera

class VMB(UniversalCamera):
    """
    VMB camera class
    """
    def __init__(self, name, id):
        super().__init__(name, id)


    def initialise_camera(self):
        self.vmb = vmbpy.VmbSystem.get_instance()
        self.vmb._startup()
        self.camera=self.vmb.get_camera_by_id(self.id)


    def open(self):
        self.camera._open()

    def close(self):
        self.camera._close()
        self.vmb._shutdown()
        print('closed the camera')


    def get_exposure(self):
        # exposure in us
        return self.camera.ExposureTimeAbs.get()


    def get_exposure_limits(self):
        lower = self.camera.ExposureTimeAbs.get_range()[0]
        upper = self.camera.ExposureTimeAbs.get_range()[1]
        return lower, upper


    def get_gain_limits(self):
        lower = self.camera.Gain.get_range()[0]
        upper = self.camera.Gain.get_range()[1]
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
        grab_result = self.camera.get_frame(timeout_ms = int(self.exposure*1.2*1e-3))
        grab_result.convert_pixel_format(vmbpy.PixelFormat.Mono8)
        img = grab_result.as_numpy_ndarray()
        return img

    def start_grab(self):
        pass
    
    def stop_grab(self):
        pass

