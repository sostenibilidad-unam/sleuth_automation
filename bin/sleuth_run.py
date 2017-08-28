#!/usr/bin/env python
from os.path import join
import argparse

parser = argparse.ArgumentParser(
    description="""Run full SLEUTH pipeline for location""")

parser.add_argument('--sleuth_path', required=True,
                    help='path to SLEUTH directory')
parser.add_argument('--location_dir', required=True,
                    help='path to location directory')
parser.add_argument('--location_name', required=True,
                    help='name of location')
parser.add_argument('--mpi_cores', default=0,
                    help="""number of cores available for MPI,
                            if 0 (default) don't use mpi""")
parser.add_argument('--predict_start', type=int, required=True,
                    help='starting year of prediction interval')
parser.add_argument('--predict_end', type=int, required=True,
                    help='ending year of prediction interval')
parser.add_argument('--montecarlo_iterations', type=int, default=50,
                    help='monte carlo iterations')
parser.add_argument('--virtualenv', default=None,
                    help='path to python virtualenv')

args = parser.parse_args()

if args.virtualenv:
    activate_this = join(args.virtualenv, 'bin/activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

import sleuth_automation as sa

if args.mpi_cores > 0:
    sa.configure(sleuth_path=args.sleuth_path,
                 use_mpi=True, mpi_cores=args.mpi_cores)
else:
    sa.configure(sleuth_path=args.sleuth_path,
                 use_mpi=False)

l = sa.Location(args.location_name,
                args.location_dir)

l.calibrate_coarse(monte_carlo_iterations=args.montecarlo_iterations)
l.calibrate_fine(monte_carlo_iterations=args.montecarlo_iterations)
l.calibrate_final(monte_carlo_iterations=args.montecarlo_iterations)

l.sleuth_predict(args.predict_start,
                 args.predict_end)

l.gif2tif(args.predict_start,
          args.predict_end)
