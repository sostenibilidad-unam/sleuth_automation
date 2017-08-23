from math import floor
import pandas


class ControlStats:
    """
    This class grabs values from the control_stats.log and calculates
    ranges for the parameters for next calibration stage:
    - diff
    - brd
    - sprd
    - slp
    - rg
    """

    def __init__(self, path, step):
        """
        input path to control_stats.log
        step
        """
        self.default_step = step
        self.params = {}
        with open(path) as controlstats:
            widths = [7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 5, 5, 5]
            df = pandas.read_fwf(controlstats, skiprows=1, widths=widths)
            primeros10 = df.sort_values(by='Leesalee', ascending=False)[:10]
            best_fit = df.sort_values(by='Leesalee', ascending=False)[:1]

            diff = int(best_fit['Diff'].values[0])
            diff_max = primeros10['Diff'].max()
            diff_start = self.start(primeros10['Diff'].min(), diff_max)
            diff_step = self.step(diff_max, diff_start)
            diff_end = self.end(diff_start, diff_step)

            brd = int(best_fit['Brd'].values[0])
            brd_max = primeros10['Brd'].max()
            brd_start = self.start(primeros10['Brd'].min(), brd_max)
            brd_step = self.step(brd_max, brd_start)
            brd_end = self.end(brd_start, brd_step)

            sprd = int(best_fit['Sprd'].values[0])
            sprd_max = primeros10['Sprd'].max()
            sprd_start = self.start(primeros10['Sprd'].min(), sprd_max)
            sprd_step = self.step(sprd_max, sprd_start)
            sprd_end = self.end(sprd_start, sprd_step)

            slp = int(best_fit['Slp'].values[0])
            slp_max = primeros10['Slp'].max()
            slp_start = self.start(primeros10['Slp'].min(), slp_max)
            slp_step = self.step(slp_max, slp_start)
            slp_end = self.end(slp_start, slp_step)

            rg = int(best_fit['RG'].values[0])
            rg_max = primeros10['RG'].max()
            rg_start = self.start(primeros10['RG'].min(), rg_max)
            rg_step = self.step(rg_max, rg_start)
            rg_end = self.end(rg_start, rg_step)

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
