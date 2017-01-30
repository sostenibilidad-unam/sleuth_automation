class Location:

    def __init__(self, location, path, start, end, dates):
        """
        location is a name for the location according to sleuth docs
        path is a path to the location directory
        start and end enclose the temporal range for prediction
        dates is a list of years which are part of the .GIF filenames in the input data
        
        """
        self.location = location
        self.path = path

        self.validate_path()

    def validate_path(self):
        pass

    def create_scenario_file(self, stage):
        pass

    def sleuth_calibrate(self, scenario_file_path):
        pass
    
    def calibrate(self):
        self.sleuth_calibrate(self.create_scenario_file('coarse'))
        self.sleuth_calibrate(self.create_scenario_file('fine'))
        self.sleuth_calibrate(self.create_scenario_file('final'))

    def predict(self):
        pass
