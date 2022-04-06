from instrument_control.spec_ocean import OceanOptics
import json

class Spectrometer:
    def __init__(self, name):
        self.name = name
        self.model = 0#self.get_model("assets/spectrometer_list.json")

    def initiate(self):
        if self.model ==0:
            return OceanOptics(self.name)

