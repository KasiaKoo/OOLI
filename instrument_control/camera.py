from instrument_control.camera_basler import Basler

class Camera:
    """
    Constructor class for camera control
    """
    def __init__(self, name):

        self.name = name
        self.model = self.get_model("assets/camera_list.json")


    def initiate(self):
        if self.model == "Basler":
            return Basler()

    def get_model(self, camera_list):
        # look up camera model in dictionary
        # TODO: Fix

        return "Basler"
