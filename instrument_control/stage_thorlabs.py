import thorlabs_apt as apt

class ThorLabsStage():
    """
    Stages from ThorLabs class
    """
    def __init__(self, stage_number):

        
        self.stage = apt.Motor(stage_number)

        self.position = self.get_position()
        self.position_lower, self.position_upper = self.get_position_limits()
        self.moving = self.stage.is_in_motion()
        self.hold = True

    def get_position(self):
        return self.stage.position

    def get_position_limits(self):
        parameters = self.stage.get_stage_axis_info()
        lower = parameters[0]
        upper = parameters[1]
        return lower, upper

    def set_position(self, new_value):
        self.stage.move_to(new_value, blocking=self.hold)



