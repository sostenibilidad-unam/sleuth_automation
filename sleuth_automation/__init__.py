# coding: utf-8
# Authors: Fidel Serrano, Rodrigo García
"""
An object oriented wrapper for SLEUTH_, an urban growth model.

.. _SLEUTH: http://www.ncgia.ucsb.edu/projects/gig/

This module defines the `Location` class, which is a work unit for SLEUTH.

How to use this module
======================

1. Import it::

    import sleuth_automation as sa

2. Configure it at least with a path to SLEUTH binaries::

    sa.configure(sleuth_path='/path/to/sleuth',
                 use_mpi=True, mpi_cores=32)

2. Create an instance::

    l = sa.Location('my_location',
                    '/path/to/my_location')

3. Calibrate model::

    l.calibrate_coarse()
    l.calibrate_fine()
    l.calibrate_final()

or calibrate with a single call::

    l.sleuth_calibrate()

4. Predict growth::

    l.sleuth_predict(2017, 2060)

5. Format prediction as TIFF::

    l.gif2tif(2017, 2060)


"""

__docformat__ = 'restructuredtext'

import os
from os.path import join, abspath
from jinja2 import Environment, PackageLoader
from sleuth_automation.controlstats import ControlStats
import json
import pickle
import datetime


try:
    from sh import bash, gdal_translate, otbcli_BandMath, which
except ImportError:
    print("failed to import one of bash, gdal_translate, otbcli_BandMath, which. Please add them to your PATH variable.")
    exit()

try:
    from sh import mpirun
except:
    pass

config = {}


def create_dir(path):
    """
    If directory doesn't exist: create it.
    """
    if not os.path.exists(path):
        os.mkdir(path, mode=0o755)


def configure(sleuth_path, use_mpi=False, mpi_cores=40):
    """
    Merge extra parameters into global config.

    Parameters:

    - `sleuth_path`: path to SLEUTH directory.
    - `use_mpi`: wether to call SLEUTH binaries thru the MPI.
    - `mpi_cores`: if so, how many cores to use.
    """

    config['sleuth_path'] = sleuth_path
    config['use_mpi'] = use_mpi
    config['mpi_cores'] = mpi_cores
    config['whirlgif_binary'] = join(join(sleuth_path,
                                          "Whirlgif"),
                                     'whirlgif')
    config['grow_binary'] = join(sleuth_path,
                                 "grow")


class Location:
    """
    This class represents the main work unit of the SLEUTH model.
    Within a location urban growth is simulated. A location should
    have a name which is just a string and is used for naming output
    files, and a directory containing GIF files as specified by
    the SLEUTH documentation_.

    .. _documentation: http://www.ncgia.ucsb.edu/projects/gig/About/dtInput.htm
    """

    def save_status(self):
        with open(join(self.input_path, "%s.pickle" % self.location), 'wb') as p:
            pickle.dump(self.status, p)


    def __init__(self, location, input_path):
        """
        Initialize a `Location` object.

        Parameters:

        - `location`: a name for the location according to sleuth docs
        - `input_path`: a path to the location directory
        """

        assert len(config.keys()) > 0

        self.location = location
        self.input_path = input_path
        self.output_path = join(input_path, 'out')
        create_dir(self.output_path)

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

        s = self.__dict__.copy()
        del(s['env'])
        s.update(config)

        self.status = {'init': {'stamp': datetime.datetime.now(),
                                'data': s},
                       'calibration': {'coarse':{},
                                       'fine': {},
                                       'final': {}},
                       'prediction': {}}

        self.save_status()


    def create_scenario_file(self, params, monte_carlo_iterations):
        """
        Merges extra parameters to global config and renders them into
        a SLEUTH scenario file.

        Parameters:

        - `params`: extra parameters to merge.
        - `monte_carlo_iterations`: more iterations take a longer time
           to run but add precision.
        """

        template = self.env.get_template('scenario.jinja')

        arguments = {'whirlgif_binary': config['whirlgif_binary'],
                     'input_dir': self.input_path,
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
        """
        Run SLEUTH coarse calibration.

        Parameters:

        - `monte_carlo_iterations`: iterations for the coarse calibration step.

        """
        coarse_dir = join(self.output_path, 'coarse')
        create_dir(coarse_dir)
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
                         'rg_end': 100,

                         'output_dir': coarse_dir + '/'}

        with open(join(self.output_path,
                       'scenario.%s.coarse' % self.location),
                  'w') as f:
            scenario_file_path = f.name
            f.write(self.create_scenario_file(coarse_params,
                                              monte_carlo_iterations))

        self.status['calibration']['coarse']['start'] = datetime.datetime.now()
        self.status['calibration']['coarse']['params'] = coarse_params
        self.save_status()
        if config['use_mpi']:
            mpirun('-np',
                   config['mpi_cores'],
                   config['grow_binary'],
                   'calibrate',
                   scenario_file_path,
                   _out=join(coarse_dir, 'mpi_out.log'),
                   _err=join(coarse_dir, 'mpi_err.log'))
        else:
            bash('-c', "%s calibrate %s" % (config['grow_binary'],
                                            scenario_file_path))
        self.status['calibration']['coarse']['end'] = datetime.datetime.now()
        self.save_status()


    def calibrate_fine(self, monte_carlo_iterations=50):
        """
        Run SLEUTH fine calibration.

        Parameters:

        - `monte_carlo_iterations`: iterations for the fine calibration step.

        """

        fine_dir = join(self.output_path, 'fine')
        create_dir(fine_dir)
        default_step = 5

        cs = ControlStats(join(join(self.output_path,
                                    'coarse'),
                               'control_stats.log'), default_step)
        cs.params['output_dir'] = fine_dir + '/'
        cs.params['monte_carlo_iterations'] = monte_carlo_iterations
        with open(join(self.output_path,
                       'scenario.%s.fine' % self.location), 'w') as f:
            scenario_file_path = f.name
            f.write(self.create_scenario_file(cs.params,
                                              monte_carlo_iterations))


        self.status['calibration']['fine']['start'] = datetime.datetime.now()
        self.status['calibration']['fine']['params'] = cs.params
        self.save_status()
        if config['use_mpi']:
            mpirun('-np',
                   config['mpi_cores'],
                   config['grow_binary'],
                   'calibrate',
                   scenario_file_path,
                   _out=join(fine_dir, 'mpi_out.log'),
                   _err=join(fine_dir, 'mpi_err.log'))
        else:
            bash('-c', "%s calibrate %s" % (config['grow_binary'],
                                            scenario_file_path))
        self.status['calibration']['fine']['end'] = datetime.datetime.now()
        self.save_status()


    def calibrate_final(self, monte_carlo_iterations=50):
        """
        Run SLEUTH final calibration.

        Parameters:

        - `monte_carlo_iterations`: iterations for the final calibration step.

        """

        final_dir = join(self.output_path, 'final')
        create_dir(final_dir)
        default_step = 1

        cs = ControlStats(join(join(self.output_path,
                                    'fine'),
                               'control_stats.log'), default_step)
        cs.params['output_dir'] = final_dir + '/'
        cs.params['monte_carlo_iterations'] = monte_carlo_iterations
        with open(join(self.output_path,
                       'scenario.%s.final' % self.location), 'w') as f:
            scenario_file_path = f.name
            f.write(self.create_scenario_file(cs.params,
                                              monte_carlo_iterations))

        self.status['calibration']['final']['start'] = datetime.datetime.now()
        self.status['calibration']['final']['params'] = cs.params
        self.save_status()
        if config['use_mpi']:
            mpirun('-np',
                   config['mpi_cores'],
                   config['grow_binary'],
                   'calibrate',
                   scenario_file_path,
                   _out=join(final_dir, 'mpi_out.log'),
                   _err=join(final_dir, 'mpi_err.log'))
        else:
            bash('-c', "%s calibrate %s" % (config['grow_binary'],
                                            scenario_file_path))
        self.status['calibration']['final']['end'] = datetime.datetime.now()
        self.save_status()


    def sleuth_calibrate(self):
        """
        Run coarse, fine and final calibration steps in one call.
        """
        self.calibrate_coarse()
        self.calibrate_fine()
        self.calibrate_final()

    def sleuth_predict(self,
                       end,
                       diff=None, brd=None, sprd=None, slp=None, rg=None,
                       monte_carlo_iterations=50):
        """
        Run SLEUTH prediction step for range enclosed in start, end.

        Parameters:

        - `end`: end of temporal range for prediction, beggining is infered from last input
        - `diff`: TODO: see model documentation
        - `brd`: TODO: see model documentation
        - `sprd`: spread
        - `slp`: slope
        - `rg`: TODO: see model documentation
        - `monte_carlo_iterations`: iterations for the prediction step
        """

        self.predict_end = end

        predict_dir = join(self.output_path, 'predict')
        create_dir(predict_dir)

        default_step = 0  # ignored for predict
        cs = ControlStats(join(join(self.output_path,
                                    'final'),
                               'control_stats.log'), default_step)
        cs.params['output_dir'] = predict_dir + '/'

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

        cs.params['monte_carlo_iterations'] = monte_carlo_iterations
        with open(join(self.output_path,
                       'scenario.%s.predict' % self.location),
                  'w') as f:
            scenario_file_path = f.name
            f.write(self.create_scenario_file(cs.params,
                                              monte_carlo_iterations))


        self.status['prediction']['start'] = datetime.datetime.now()
        self.status['prediction']['params'] = cs.params
        self.save_status()
        if config['use_mpi']:
            mpirun('-np',
                   1,
                   config['grow_binary'],
                   'predict',
                   scenario_file_path,
                   _out=join(predict_dir, 'mpi_out.log'),
                   _err=join(predict_dir, 'mpi_err.log'))
        else:
            bash('-c', "%s predict %s" % (config['grow_binary'],
                                          scenario_file_path))
        self.status['prediction']['end'] = datetime.datetime.now()
        self.save_status()


    def gif2tif(self, start, end):
        """
        Convert `prediction output`_ from GIF to TIFF.

        Will use extent.json and gdal_translate to recover geospatial
        information lost to GIF format.

        Parameters:

        - `start`: beginning of prediction range.
        - `end`: ending of prediction range, inclusive.

        Start and end parameters are necessary to figure out paths.

        .. _`prediction output`: http://www.ncgia.ucsb.edu/projects/gig/About/dtImOut.htm
        """
        predict_dir = join(self.output_path, 'predict')
        with open(join(self.input_path, 'extent.json')) as extent_file:
            extent = json.load(extent_file)
            columnas = str(int(extent["columns"]) - 1)
            renglones = str(int(extent["rows"]) - 1)
            epsg = 'EPSG:' + extent["epsg"]
            xmin = str(extent["xmin"])
            xmax = str(extent["xmax"])
            ymin = str(extent["ymin"])
            ymax = str(extent["ymax"])

            self.save_status('gif2tif')
        for year in range(start + 1, end + 1):
            gif = join(predict_dir,
                       "%s_urban_%s.gif" % (self.location, year))
            tmp_tif = join(predict_dir,
                           "%s_urban_%s_tmp.tif" % (self.location, year))
            tmp_xml = join(predict_dir,
                           "%s_urban_%s_tmp.tif.aux.xml" % (self.location,
                                                            year))
            tif = join(predict_dir,
                       "%s_urban_%s.tif" % (self.location, year))

            gdal_translate('-a_srs', epsg,
                           '-ot', 'Float64',
                           '-of', 'GTiff',
                           '-gcp', '0', renglones, xmin, ymin,
                           '-gcp', columnas, renglones, xmax, ymin,
                           '-gcp', columnas, '0', xmax, ymax,
                           '-gcp', '0', '0', xmin, ymax,
                           gif, tmp_tif)

            otbcli_BandMath('-il', tmp_tif,
                            '-out', tif, '-exp', 'im1b1 < 9 ? im1b1 : 0')
            try:
                os.remove(tmp_tif)
                os.remove(tmp_xml)
            except:
                pass


class Region:
    """
    A directory containing several Locations
    """

    def __init__(self, region_dir,
                 predict_end,
                 monte_carlo_iterations):
        self.region_dir = region_dir
        self.predict_end = predict_end
        self.monte_carlo_iterations = monte_carlo_iterations
        self.env = Environment(loader=PackageLoader('sleuth_automation',
                                                    'templates'))

        self.locations = []
        for f in os.listdir(region_dir):
            if os.path.isdir(join(region_dir, f)):
                self.locations.append({"name": f,
                                       "path": abspath(join(region_dir,
                                                            f)) + '/'})



    def build(self):
        template = self.env.get_template("condor_submit.jinja")
        with open(join(self.region_dir, 'submit.condor'), 'w') as f:
            f.write(template.render({'executable': which('sleuth_run.py'),
                                     'list_of_regions': self.locations,
                                     'predict_end': self.predict_end,
                                     'sleuth_path': config['sleuth_path'],
                                     'mpi_cores': config['mpi_cores'],
                                     'montecarlo_iterations':
                                     self.monte_carlo_iterations}))
        return f.name
