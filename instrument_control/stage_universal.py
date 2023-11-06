
class UniversalStage():
    """ Universal Class for Stage which is the parent to all specific models. 
    All methods with 'Still using Universal' require change for specific stages."""

    def __init__(self, name, stage_number):

        self.name = name
        self.stage_number = stage_number
        self.initialise()
        self.get_parameters()
        self.position_lower, self.position_upper = self.get_position_limits()
        self.lock = False

    def initialise(self):
        raise Exception('Still using Universal')
        self.stage = apt.Motor(self.stage_number)

    def get_parameters(self):
        raise Exception('Still using Universal')
        self.parameters = self.stage.get_stage_axis_info()

    def get_position(self):
        raise Exception('Still using Universal')
        return self.stage.position


    def get_position_limits(self):
        raise Exception('Still using Universal')
        lower = self.parameters[0]
        upper = self.parameters[1]
        return lower, upper


    def set_position_limits(self, lower, upper):
        raise Exception('Still using Universal')
        units = self.parameters[2]
        pitch = self.parameters[3]
        self.stage.set_stage_axis_info(lower, upper, units, pitch)
        self.position_lower, self.position_upper = self.get_position_limits()


    def set_position(self, new_value):
        raise Exception('Still using Universal')
        if self.lock is False:
            self.stage.move_to(new_value, blocking=False)
        else:
            print("Cannot move, lock is active")


    def enable_lock(self):
        raise Exception('Still using Universal')
        is_in_motion = self.stage.is_in_motion
        while is_in_motion:
            print("Waiting to lock...")
            time.sleep(0.5)
            is_in_motion = self.stage.is_in_motion

        self.lock = True

    def disable_lock(self):
        self.lock = False





