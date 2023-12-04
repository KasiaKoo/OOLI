from instrument_control.camera_basler import Basler
from instrument_control.camera_ArtCam import ArtCam
from instrument_control.camera_vmb import VMB

import json

class Camera:
    """
    Constructor class for camera control
    """
    def __init__(self, name):

        self.name = name
        self.model = self.get_model("assets/camera_list.json")


    def initiate(self):
        if self.model == "Basler":
            return Basler(self.name)
        elif self.model == "ArtCam":
            return ArtCam(self.name)
        elif self.model == "VMB":
            return VMB(self.name)
        else:
            raise Exception('Class for this model not defined')

    def get_model(self, camera_list):
        with open(camera_list) as f:
            camera_dict = json.load(f)
        return camera_dict[self.name]["Model"]

