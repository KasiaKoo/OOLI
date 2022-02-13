
class ThorLabsStage():
    """
    Stages from ThorLabs class
    """
    def __init__(self):
        self.stage = 0#initiate stage

        self.position = self.get_position()
        self.position_lower, self.position_upper = self.get_position_limits()
        self.moving = False
        self.hold = True

    def get_position(self):
        pass

    def get_position_limits(self):
        return 1,1

    def set_position(self, new_value):
        pass



