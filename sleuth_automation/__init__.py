import os
from jinja2 import Environment, PackageLoader
from controlstats import ControlStats
from sh import bash

config = {}


def configure(sleuth_path, use_mpi=False):
    config['sleuth_path'] = sleuth_path
    config['use_mpi'] = use_mpi
    config['whirlgif_binary'] = os.path.join(os.path.join(sleuth_path,
                                                          "Whirlgif"),
                                             'whirlgif')
    config['grow_binary'] = os.path.join(sleuth_path,
                                         "grow")


class Location:

    def __init__(self, location, input_path):
        """
        location is a name for the location according to sleuth docs
        path is a path to the location directory
        start and end enclose the temporal range for prediction
        dates is a list of years which are part of the .GIF
        filenames in the input data
        """

        assert len(config.keys()) > 0

        self.location = location
        self.input_path = input_path
        self.output_path = os.path.join(input_path, 'out')
        self.create_dir(self.output_path)
        # self.validate_input_path()

        self.urban_layers = []
        self.roads_layers = []
        for thisFile in os.listdir(input_path):
            if thisFile.endswith('.gif') and not thisFile.startswith("."):
                if ".urban." in thisFile:
                    self.urban_layers.append(thisFile)
                if ".roads." in thisFile:
                    self.roads_layers.append(thisFile)
                if ".slope." in thisFile:
                    self.slope_layer = thisFile
                if ".hillshade." in thisFile:
                    self.hillshade_layer = thisFile
                if ".excluded." in thisFile:
                    self.exclusion_layer = thisFile
        self.urban_layers.sort()
        self.roads_layers.sort()

        # predict start and end must be in scenario files, tho ignored
        # in calibration stages
        self.predict_start = self.urban_layers[-1].split('.')[-2]
        self.predict_end = int(self.predict_start)+1

        self.env = Environment(loader=PackageLoader('sleuth_automation',
                                                    'templates'))

    def create_dir(self, path):
        if not os.path.exists(path):
            os.mkdir(path, 0755)

    def create_scenario_file(self, params, monte_carlo_iterations):

        template = self.env.get_template('scenario.jinja')

        arguments = {'whirlgif_binary': config['whirlgif_binary'],
                     'input_dir': self.input_path + "/",
                     'output_dir': self.output_path + "/",
                     'monte_carlo_iterations': monte_carlo_iterations,

                     'urban': self.urban_layers,
                     'roads': self.roads_layers,

                     'exclude': self.exclusion_layer,
                     'slope': self.slope_layer,
                     'hillshade': self.hillshade_layer,

                     'predict_start': self.predict_start,
                     'predict_end': self.predict_end}

        arguments.update(params)
        return template.render(arguments)

    def calibrate_coarse(self, monte_carlo_iterations=50):
        self.create_dir(os.path.join(self.output_path, 'coarse'))
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
                         'rg_end': 100}
        with open(os.path.join(self.output_path,
                               'scenario.%s.coarse' % self.location),
                  'w') as f:
            scenario_file_path = f.name
            f.write(self.create_scenario_file(coarse_params,
                                              monte_carlo_iterations))

        bash('-c', "%s calibrate %s" % (config['grow_binary'],
                                        scenario_file_path))

    def calibrate_fine(self, monte_carlo_iterations=50):
        self.create_dir(os.path.join(self.output_path, 'fine'))
        default_step = 5
        cs = ControlStats(os.path.join(os.path.join(self.output_path,
                                                    'coarse'),
                                       'control_stats.log'), default_step)

        with open(os.path.join(self.output_path,
                               'scenario.%s.fine' % self.location), 'w') as f:
            f.write(self.create_scenario_file(cs.params,
                                              monte_carlo_iterations))

    def calibrate_final(self, monte_carlo_iterations=50):
        self.create_dir(os.path.join(self.output_path, 'final'))
        default_step = 1
        cs = ControlStats(os.path.join(os.path.join(self.output_path,
                                                    'fine'),
                                       'control_stats.log'), default_step)

        with open(os.path.join(self.output_path,
                               'scenario.%s.final' % self.location), 'w') as f:
            f.write(self.create_scenario_file(cs.params,
                                              monte_carlo_iterations))

    def sleuth_calibrate(self):
        self.calibrate_coarse()
        self.calibrate_fine()
        self.calibrate_final()

    def sleuth_predict(self,
                       start, end,
                       diff=None, brd=None, sprd=None, slp=None, rg=None,
                       monte_carlo_iterations=150):
        self.predict_start = start
        self.predict_end = end

        default_step = 1  # ignored for predict
        cs = ControlStats(os.path.join(os.path.join(self.output_path,
                                                    'final'),
                                       'control_stats.log'), default_step)

        if diff:
            cs.params['diff'] = diff

        if brd:
            cs.params['brd'] = brd

        if sprd:
            cs.params['sprd'] = sprd

        if slp:
            cs.params['slp'] = slp

        if rg:
            cs.params['rg'] = rg

        with open(os.path.join(self.output_path,
                               'scenario.%s.predict' % self.location),
                  'w') as f:
            f.write(self.create_scenario_file(cs.params,
                                              monte_carlo_iterations))
