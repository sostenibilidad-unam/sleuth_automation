#!/usr/bin/env python

import os
import argparse
from os.path import join, abspath
from sh import which
import sleuth_automation as sleuth
from jinja2 import Environment, PackageLoader

description = """
This script will create a condor submit file for a batch of SLEUTH runs.
"""

parser = argparse.ArgumentParser(description=description)

parser.add_argument('--sleuth_path', required=True,
                    help='path to SLEUTH directory')
parser.add_argument('--region_dir',
                    required=True,
                    help='path to region dir containing locations')
parser.add_argument('--mpi_cores', default=0,
                    help="""number of cores available for MPI,
                            if 0 (default) don't use mpi""")
parser.add_argument('--predict_end', type=int, required=True,
                    help='ending year of prediction interval')
parser.add_argument('--montecarlo_iterations', type=int, default=50,
                    help='monte carlo iterations')
args = parser.parse_args()


if args.mpi_cores > 0:
    sleuth.configure(sleuth_path=args.sleuth_path,
                     use_mpi=True, mpi_cores=args.mpi_cores)
else:
    sleuth.configure(sleuth_path=args.sleuth_path,
                     use_mpi=False)


r = sleuth.Region(region_dir=args.region_dir,
                  predict_end=args.predict_end,
                  monte_carlo_iterations=args.montecarlo_iterations)

print "wrote " + r.build()
