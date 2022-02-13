from basler import Basler

class Camera:
    def __init__(self, name):
        """__init__.

        :param name:
        """

        self.name = name
        self.model = self.get_model("assets/camera_list.json")


    def initiate(self):
        if self.model == "Basler":
            return Basler()

    def get_model(self, camera_list):
        # look up camera model in dictionary

        return "Basler"
