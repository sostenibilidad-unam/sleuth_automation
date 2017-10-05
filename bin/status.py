#!/usr/bin/env python

import pickle
import argparse
from pprint import pprint

description = """
print out run status from pickled Location object
"""

parser = argparse.ArgumentParser(description=description)

parser.add_argument('pickle',  type=argparse.FileType('r'), help='path to location pickle')

args = parser.parse_args()


l = pickle.load(args.pickle)
pprint(l)
