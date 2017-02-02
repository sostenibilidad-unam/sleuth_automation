import os
from math import floor
from jinja2 import Environment, PackageLoader
import pandas

class ControlStats:

    def __init__(self, path, step):
        self.step = step
        self.params = {}
        with open(path) as controlstats:
            widths = [7,8,8,8,8,8,8,8,8,8,8,8,8,8,5,5,5,5,5]
            df = pandas.read_fwf(controlstats, skiprows = 1, widths = widths)
            primeros10 = df.sort_values(by = 'Leesalee', ascending = False)[:10]
            best_fit = df.sort_values(by = 'Leesalee', ascending = False)[:1]

            diff = best_fit['Diff'].values[0]    
            diff_max = primeros10['Diff'].max()
            diff_start = self.start(primeros10['Diff'].min(), diff_max)
            diff_step = self.step(diff_max, diff_start)
            diff_end = self.end(diff_start, diff_step)

            brd = best_fit['Brd'].values[0]    
            brd_max = primeros10['Brd'].max()
            brd_start = self.start(primeros10['Brd'].min(), brd_max)
            brd_step = self.step(brd_max, brd_start)
            brd_end = self.end(brd_start, brd_step)

            sprd = best_fit['Sprd'].values[0]    
            sprd_max = primeros10['Sprd'].max()
            sprd_start = self.start(primeros10['Sprd'].min(), sprd_max)
            sprd_step = self.step(sprd_max, sprd_start)
            sprd_end = self.end(sprd_start, sprd_step)

            slp = best_fit['Slp'].values[0]    
            slp_max = primeros10['Slp'].max()
            slp_start = self.start(primeros10['Slp'].min(), slp_max)
            slp_step = self.step(slp_max, slp_start)
            slp_end = self.end(slp_start, slp_step)

            rg = best_fit['RG'].values[0]
            rg_max = primeros10['RG'].max()
            rg_start = self.start(primeros10['RG'].min(), rg_max)
            rg_step = self.step(rg_max, rg_start)
            rg_end = self.end(rg_start, rg_step)

            self.params = { 'diff': diff,
                            'diff_start': diff_start,
                            'diff_step': diff_step,
                            'diff_end': diff_end,

                            'brd': brd,
                            'brd_start': brd_start,
                            'brd_step': brd_step,
                            'brd_end': brd_end,

                            'sprd': sprd,
                            'sprd_start': sprd_start,
                            'sprd_step': sprd_step,
                            'sprd_end': sprd_end,

                            'slp': slp,
                            'slp_start': slp_start,
                            'slp_step': slp_step,
                            'slp_end': slp_end,

                            'rg': rg,
                            'rg_start': rg_start,
                            'rg_step': rg_step,
                            'rg_end': rg_end }

                        
    def step(Max, Start):
        if Max == 1:
            Max = 0
        if Max == Start:
            return self.step
        else:
            step = int(floor((Max - Start) / 4.0))
            if step < 1:
                return 1
            else:
                return self.step

    def end(Start, Step):
        return Start + (4 * Step)

    def start(Start, Max):
        if Start == 1:
            Start = 0
        if Max == 100 and Start == Max:
            Start = Max - (4 * args.step)
        return Start




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
