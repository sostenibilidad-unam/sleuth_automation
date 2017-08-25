#!/usr/bin/env python

import os
import argparse
from os.path import join, abspath
from sh import which
import sleuth_automation
from jinja2 import Environment, PackageLoader


parser = argparse.ArgumentParser(description='')

parser.add_argument('--sleuth_path', required=True,
                    help='path to SLEUTH directory')
parser.add_argument('--locations_dir',
                    required=True,
                    help='path to regions dir')
parser.add_argument('--mpi_cores', default=0,
                    help="""number of cores available for MPI,
                            if 0 (default) don't use mpi""")
parser.add_argument('--predict_start', type=int, required=True,
                    help='starting year of prediction interval')
parser.add_argument('--predict_end', type=int, required=True,
                    help='ending year of prediction interval')
parser.add_argument('--montecarlo_iterations', type=int, default=50,
                    help='monte carlo iterations')
args = parser.parse_args()


env = Environment(loader=PackageLoader('sleuth_automation',
                                       'templates'))

list_of_regions = []
for thisFile in os.listdir(args.locations_dir):
    if os.path.isdir(join(args.locations_dir, thisFile)):
        list_of_regions.append({"name": thisFile,
                                "path": abspath(join(args.locations_dir, thisFile)) + '/'})

template = env.get_template("sleuth_template.condor")

with open(join(args.locations_dir, 'submit.condor'), 'w') as f:
    f.write(template.render({'executable': which('sleuth_run.py'),
                             'list_of_regions': list_of_regions,
                             'predict_start': args.predict_start,
                             'predict_end': args.predict_end,
                             'sleuth_path': args.sleuth_path,
                             'mpi_cores': args.mpi_cores,
                             'montecarlo_iterations': args.montecarlo_iterations,
                             'virtualenv': os.environ.get('VIRTUAL_ENV',
                                                          None)}))
