import os
from jinja2 import Environment, PackageLoader
from controlstats import ControlStats

class Location:

    def __init__(self, location, input_path, output_path, start, end, dates):
        """
        location is a name for the location according to sleuth docs
        path is a path to the location directory
        start and end enclose the temporal range for prediction
        dates is a list of years which are part of the .GIF filenames in the input data
        
        """
        self.location = location
        self.path = path
        self.start = start
        self.end = end
        self.dates = dates

        self.validate_path()
        
    def validate_path(self):
        pass
   
    def create_scenario_file(self, stage, monte_carlo_iterations):
        if stage == 'coarse':
            pass
        elif stage == 'fine':
            cs = ControlStats(os.path.join(os.path.join(self.output_path, stage), 'control_stats.log')
        
        env = Environment(loader=PackageLoader('sleuth_automation', 'templates'))
        template = env.get_template('scenario.jinja')

        arguments = {input_dir: self.input_dir + "/",
                    output_dir: self.output_dir + "/"
            monte_carlo_iterations=monte_carlo_iterations,
            predict_start=args.predict_start,
            predict_end=args.predict_end,
            urban=[p.name.replace(args.input_dir+"/", '') for p in args.urban],
            roads=[p.name.replace(args.input_dir+"/", '') for p in args.roads],
            exclude=args.exclude.name.replace(args.input_dir+"/", ''),
            slope=args.slope.name.replace(args.input_dir+"/", ''),
            hillshade=args.hillshade.name.replace(args.input_dir+"/", '')
                    }

        arguments.update(cs.params)
        template.render(arguments)        


    def sleuth_calibrate_coarse(self):
        diff = 50
        diff_start = 0
        diff_step = 25
        diff_end = 100

        brd = 50
        brd_start = 0
        brd_step = 25
        brd_end = 100

        sprd = 50
        sprd_start = 0
        sprd_step = 25
        sprd_end = 100

        slp = 50
        slp_start = 0
        slp_step = 25
        slp_end = 100

        rg = 50
        rg_start = 0
        rg_step = 25
        rg_end = 100


    def sleuth_calibrate(self, scenario_file_path, monte_carlo_iterations=5):
        # aqui ajustar el step segun el stage

        self.create_scenario_file('coarse', monte_carlo_iterations)
        self.create_scenario_file('fine', monte_carlo_iterations)
        self.create_scenario_file('final', monte_carlo_iterations)
        
    def sleuth_predict(self, scenario_file_path, monte_carlo_iterations=150):
        passself.create_scenario_file('predict', monte_carlo_iterations)
    

    def predict(self):
        pass




cs = ControlStats('/path/to/control_stats.log')

cs.diff -> 50
cs.diff_start -> 0
cs.diff_step
cs.diff_end 
