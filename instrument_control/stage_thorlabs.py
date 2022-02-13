import thorlabs_apt as apt
import time

class ThorLabsStage():
    """
    Stages from ThorLabs class
    """
    def __init__(self, stage_number, lower, upper):

        
        self.stage = apt.Motor(stage_number)

        self.parameters = self.stage.get_stage_axis_info()

        self.position_lower, self.position_upper = self.get_position_limits()
        self.lock = False


    def get_position(self):
        return self.stage.position


    def get_position_limits(self):
        self.parameters = self.stage.get_stage_axis_info()
        lower = self.parameters[0]
        upper = self.parameters[1]
        return lower, upper


    def set_position_limits(self, lower, upper):
        units = self.parameters[2]
        pitch = self.parameters[3]
        self.stage.set_stage_axis_info(lower, upper, units, pitch)
        self.position_lower, self.position_upper = self.get_position_limits()


    def set_position(self, new_value):
        if self.lock is False:
            self.stage.move_to(new_value, blocking=False)
        else:
            print("Cannot move, lock is active")


    def enable_lock(self):
        is_in_motion = self.stage.is_in_motion
        while is_in_motion:
            print("Waiting to lock...")
            time.sleep(0.5)
            is_in_motion = self.stage.is_in_motion

        self.lock = True

    def disable_lock(self):
        self.lock = False





