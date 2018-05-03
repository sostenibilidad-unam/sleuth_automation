# coding: utf-8
# Authors: Fidel Serrano, Rodrigo García
"""
An object representation of a SLEUTH control_stats.log_ file.

control_stats.log_ files are the output of calibration steps. They
contain the ranges for next calibration or prediction steps. This
helper module extracts those ranges for all SLEUTH parameters:

    - diff
    - brd
    - sprd
    - slp
    - rg

This is helper module will extract parameter ranges into a dictionary
that can be rendered into a jinja2 template for the creation of SLEUTH
scenario files.

How to use this module
======================

1. Import it: ``from controlstats import ControlStats``.

2. Create an instance::

    cs = ControlStats('/path/to/my_location/output/coarse/control_stats.log'),
                      step=5)

   parameter ranges are extracted into the **params** attribute: ``cs.params``

3. ``cs.params`` is passed to ``Location.create_scenario_file`` to render scenario files.

.. _control_stats.log: http://www.ncgia.ucsb.edu/projects/gig/About/dtStatOut.htm
"""
from math import floor
import pandas


class ControlStats:
    """
    This class grabs values from a **control_stats.log** file and calculates
    ranges for the parameters for next calibration stage.

    It will find ranges for:

    - diff
    - brd
    - sprd
    - slp
    - rg

    Including values for start, end and step.

    All fetched parameters will be stored into the **params** property.
    """

    def __init__(self, path, step):
        """
        Initialize class.

        Parameters:

        - `path`: path to control_stats.log file
        - `step`: width of step for creation of range
        """
        self.default_step = step
        self.params = {}
        with open(path) as controlstats:
            widths = [7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 5, 5, 5]
            df = pandas.read_fwf(controlstats, skiprows=1, widths=widths)

            df['osm'] = df['Compare'] * df['Pop'] * df['Edges'] * df['Clusters'] * df['Slope'] * df['Xmean'] * df['Ymean']

            primeros10 = df.sort_values(by='osm', ascending=False)[:10]
            best_fit = df.sort_values(by='osm', ascending=False)[:1]

            diff = int(best_fit['Diff'].values[0])
            diff_max = primeros10['Diff'].max()
            diff_start = self.start(primeros10['Diff'].min(), diff_max) if self.default_step != 0 else diff
            diff_step = self.step(diff_max, diff_start) if self.default_step != 0 else 1
            diff_end = self.end(diff_start, diff_step) if self.default_step != 0 else diff

            brd = int(best_fit['Brd'].values[0])
            brd_max = primeros10['Brd'].max()
            brd_start = self.start(primeros10['Brd'].min(), brd_max) if self.default_step != 0 else brd
            brd_step = self.step(brd_max, brd_start) if self.default_step != 0 else 1
            brd_end = self.end(brd_start, brd_step) if self.default_step != 1 else brd

            sprd = int(best_fit['Sprd'].values[0])
            sprd_max = primeros10['Sprd'].max()
            sprd_start = self.start(primeros10['Sprd'].min(), sprd_max) if self.default_step != 0 else sprd
            sprd_step = self.step(sprd_max, sprd_start) if self.default_step != 0 else 1
            sprd_end = self.end(sprd_start, sprd_step) if self.default_step != 1 else sprd

            slp = int(best_fit['Slp'].values[0])
            slp_max = primeros10['Slp'].max()
            slp_start = self.start(primeros10['Slp'].min(), slp_max) if self.default_step != 0 else slp
            slp_step = self.step(slp_max, slp_start) if self.default_step != 0 else 1
            slp_end = self.end(slp_start, slp_step) if self.default_step != 1 else slp

            rg = int(best_fit['RG'].values[0])
            rg_max = primeros10['RG'].max()
            rg_start = self.start(primeros10['RG'].min(), rg_max) if self.default_step != 0 else rg
            rg_step = self.step(rg_max, rg_start) if self.default_step != 0 else 1
            rg_end = self.end(rg_start, rg_step) if self.default_step != 0 else rg

            self.params = {'diff': diff,
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
                           'rg_end': rg_end}

    def step(self, Max, Start):
        """
        Returns step size.
        """
        if Max == 1:
            Max = 0
        if Max == Start:
            return self.default_step
        else:
            step = int(floor((Max - Start) / 4.0))
            if step < 1:
                return 1
            else:
                return step

    def end(self, Start, Step):
        return int(Start + (4 * Step))

    def start(self, Start, Max):
        if Start == 1:
            Start = 0
        if Max == 100 and Start == Max:
            Start = Max - (4 * self.default_step)
        return int(Start)
