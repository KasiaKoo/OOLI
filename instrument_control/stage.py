from instrument_control.stage_thorlabs import ThorLabsStage
import json

class Stage:
    """
    Constructor class for stage control
    """
    def __init__(self, name):
        self.name = name
        self.model, self.stage_number, self.lower, self.upper = self.get_info("assets/stage_list.json")


    def initiate(self):
        if self.model == "ThorLabs":
            stage = ThorLabsStage(self.name, self.stage_number)

        elif self.model == "SmarAct":
            pass

        stage.set_position_limits(self.lower, self.upper)
        return stage


    def get_info(self, stage_list):
        with open(stage_list) as f:
            stage_dict = json.load(f)

        model = stage_dict[self.name]["Model"]
        stage_number = stage_dict[self.name]["Stage Number"]
        lower = stage_dict[self.name]["Minimum"]
        upper = stage_dict[self.name]["Maximum"]

        return model, stage_number, lower, upper
