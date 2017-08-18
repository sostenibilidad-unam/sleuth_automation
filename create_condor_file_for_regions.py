#!/usr/bin/env python

from jinja2 import Template
import jinja2
import os
import argparse
# Group1 /srv/home/fidel/qgis_sleuth/Group1 2011 2060 /srv/home/fidel/sleuth/Whirlgif/whirlgif /srv/home/fidel/sleuth/grow

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--whirlgif_path',
                    required=True,
                    help='path to the whirlgif executable, usualy in .../sleuth_installation_folder/Whirlgif/whirlgif')
parser.add_argument('--grow_path',
                    required=True,
                    help='path to the grow executable, usualy in .../sleuth_installation_folder/grow')
parser.add_argument('--region_dir',
                    required=True,
                    help='path to regions dir')
parser.add_argument('--predict_start',
                    type=int,
                    required=True,
                    help='year of prediction start')
parser.add_argument('--predict_end',
                    type=int,
                    required=True,
                    help='year of prediction end')
parser.add_argument('--condor_file_name',
                    required=True,
                    help='condor file name')



args = parser.parse_args()


list_of_regions = []
for thisFile in os.listdir(args.region_dir):
    if os.path.isdir(os.path.join(args.region_dir,thisFile)):
        list_of_regions.append({"name": thisFile, "path": os.path.join(args.region_dir,thisFile)})

print list_of_regions

def getTemplate(tpl_path):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename)

context = {'list_of_regions': list_of_regions,
           'predict_start': args.predict_start,
           'predict_end': args.predict_end,
           'whirlgif_path': args.whirlgif_path,
           'grow_path': args.grow_path
        }
getTemplate("sleuth_template.condor").stream(context).dump(args.condor_file_name)

    
