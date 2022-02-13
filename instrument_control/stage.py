from instrument_control.stage_thorlabs import ThorLabsStage
import json

class Stage:
    """
    Constructor class for stage control
    """
    def __init__(self, name):
        self.name = name
        self.model, self.stage_number = self.get_model("assets/stage_list.json")


    def initiate(self):
        if self.model == "ThorLabs":
            return ThorLabsStage(self.stage_number)


    def get_model(self, stage_list):
        with open(stage_list) as f:
            stage_dict = json.load(f)

        model = stage_dict[self.name]["Model"]
        stage_number = stage_dict[self.name]["Stage Number"]
        print(stage_number)

        return model, stage_number
