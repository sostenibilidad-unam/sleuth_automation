import os
from jinja2 import Environment, PackageLoader
from controlstats import ControlStats

class Location:

    def __init__(self, location, input_path, output_path, predict_start, predict_end, dates, sleuth_path):
        """
        location is a name for the location according to sleuth docs
        path is a path to the location directory
        start and end enclose the temporal range for prediction
        dates is a list of years which are part of the .GIF filenames in the input data
        
        """
        self.location = location
        self.input_path = input_path
        self.output_path = output_path        
        self.predict_start = predict_start
        self.predict_end = predict_end
        self.dates = dates
        self.create_dir(output_path)
        self.create_dir(os.path.join(output_path, 'coarse'))
        self.create_dir(os.path.join(output_path, 'fine'))
        self.create_dir(os.path.join(output_path, 'final'))                
        self.validate_input_path()
        self.whirlgif_binary = os.path.join(os.path.join(sleuth_path, "Whirlgif"), 'whirlgif' )

    def create_dir(self, path):
         if not os.path.exists(path):
            os.mkdir(path, 0755)
        
    def validate_input_path(self):
        assert os.path.isdir(self.input_path)
        for date in self.dates:
            assert os.path.isfile(os.path.join(self.input_path,"%s.urban.%s.gif" % (self.location, date)))
            assert os.path.isfile(os.path.join(self.input_path, "%s.roads.%s.gif" % (self.location, date)))
        assert os.path.isfile(os.path.join(self.input_path, "%s.hillshade.gif" % self.location))
        assert os.path.isfile(os.path.join(self.input_path, "%s.slope.gif" % self.location))        
        assert os.path.isfile(os.path.join(self.input_path, "%s.excluded.gif" % self.location))

        
           
    def create_scenario_file(self, params, monte_carlo_iterations):
        
        env = Environment(loader=PackageLoader('sleuth_automation', 'templates'))
        template = env.get_template('scenario.jinja')

        arguments = { 'whirlgif_binary': self.whirlgif_binary,
                      'input_dir': self.input_path + "/",
                      'output_dir': self.output_path + "/",
                      'monte_carlo_iterations': monte_carlo_iterations,
                      'predict_start': self.predict_start,
                      'predict_end': self.predict_end,
                      'urban' : ["%s.urban.%s.gif" % (self.location, date) for date in self.dates],
                      'roads': ["%s.roads.%s.gif" % (self.location, date) for date in self.dates],
                      'exclude': os.path.join(self.input_path, "%s.excluded.gif" % self.location),
                      'slope': os.path.join(self.input_path, "%s.slope.gif" % self.location),
                      'hillshade': os.path.join(self.input_path, "%s.hillshade.gif" % self.location),
                      }

        arguments.update(params)
        return template.render(arguments)        


    def calibrate_coarse(self):
        coarse_params = {'diff': 50,
                         'diff_start': 0,
                         'diff_step': 25,
                         'diff_end': 100,
                         'brd': 50,
                         'brd_start': 0,
                         'brd_step': 25,
                         'brd_end': 100,

                         'sprd': 50,
                         'sprd_start': 0,
                         'sprd_step': 25,
                         'sprd_end': 100,

                         'slp': 50,
                         'slp_start': 0,
                         'slp_step': 25,
                         'slp_end': 100,

                         'rg': 50,
                         'rg_start': 0,
                         'rg_step': 25,
                         'rg_end': 100 }
        return self.create_scenario_file(coarse_params, 50)

    def calibrate_fine(self):
        cs = ControlStats(os.path.join(os.path.join(self.output_path, 'coarse'), 'control_stats.log'))
        self.create_scenario_file(cs.params, 5)
        
    def calibrate_final(self):
        cs = ControlStats(os.path.join(os.path.join(self.output_path, 'fine'), 'control_stats.log'))
        self.create_scenario_file(cs.params, 1)

    def sleuth_calibrate(self, scenario_file_path, monte_carlo_iterations=5):
        self.calibrate_coarse()
        self.calibrate_fine()
        self.calibrate_final()

                
    def sleuth_predict(self, scenario_file_path, monte_carlo_iterations=150):
        passself.create_scenario_file('predict', monte_carlo_iterations)
    

    def predict(self):
        pass





