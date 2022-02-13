from stage_thorlabs import ThorLabsStage

class Stage:
    """
    Constructor class for stage control
    """
    def __init__(self, name):
        self.name = name
        self.model = self.get_model("assets/stage_list.json")

    def initiate(self):
        if self.model == "ThorLabs":
            return ThorLabsStage()

    def get_model(self, stage_list):
        # look up stage model in dictionary
        # TODO: Fix

        return "ThorLabs"
