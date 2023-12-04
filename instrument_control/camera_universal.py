class UniversalCamera():
    """ Universal Class for Camera which is the parent to all specific models. 
    All methods with 'Still using Universal' require change for specific cameras."""

    def __init__(self, name):

        self.name = name
        self.initialise_camera()
        self.open()
        self.exposure = self.get_exposure()
        self.gain = self.get_gain()
        self.gain_lower, self.gain_upper = self.get_gain_limits()
        self.exposure_lower, self.exposure_upper = self.get_exposure_limits()
        fdsjlkdsfj§
    

    # Following methods have to be overritten for specific cameras
    def initialise_camera(self):
        """ This should create a model specific camera object"""
        raise Exception('Still using Universal')
        print('Implement camera object from specific class')
        self.camera = None

    def open(self):
        raise Exception('Still using Universal')

    def close(self):
        raise Exception('Still using Universal')

    def get_exposure(self):
        raise Exception('Still using Universal')
        return 0


    def get_exposure_limits(self):
        raise Exception('Still using Universal')
        lower = 0
        upper = 0
        return lower, upper


    def get_gain_limits(self):
        raise Exception('Still using Universal')
        lower = 0 
        upper = 0
        return lower, upper


    def get_gain(self):
        raise Exception('Still using Universal')
        return 0


    def set_exposure(self, new_value):
        raise Exception('Still using Universal')
        print('No change to exposure - implement new function')
        self.exposure = self.get_exposure()


    def set_gain(self, new_value):
        raise Exception('Still using Universal')
        print('No change to gain - implement new function')
        self.gain = self.get_gain()


    def frame_capture(self):
        """ This class should return an array object"""
        raise Exception('Still using Universal')
        img = 0
        return img

    
    def start_grab(self):
        raise Exception('Still using Universal')
        print('Implement start grabing function')

    def stop_grab(self):
        raise Exception('Still using Universal')
        print('Implement stop grabing function')


    # Following methods should be left alone
    def photo_capture(self):
        self.start_grab()
        photo = self.frame_capture()
        self.stop_grab()
        return photo

    def photo_capture_repeat(self, repeat=1):
        self.start_grab()
        photo = 0
        for i in range(repeat):
            photo = photo + self.frame_capture()
        self.stop_grab()
        return photo

