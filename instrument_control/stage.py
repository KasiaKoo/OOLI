from instrument_control.stage_thorlabs import ThorLabsStage

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

        if self.model == "Smoract":
            pass

    def get_model(self, stage_list):
        # look up stage model in dictionary using self.name
        # TODO: Fix

        return "ThorLabs", 83820741
