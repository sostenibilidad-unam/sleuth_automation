#!/usr/bin/env python

import pandas
import argparse
import sys
from math import floor
from jinja2 import Template
import os

# python create_scenario_file.py --mode calibrate --input_dir /srv/home/fidel/Para_SLEUTH/Group1 --output_dir . --predict_start 2011 --predict_end 2060 --whirlgif_path /srv/home/fidel/sleuth/Whirlgif/whirlgif --template /srv/home/fidel/sleuth_automation/sleuth_scenario_template.jinja 
# falta que el path al whirlgif sea un parametro tambien


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--mode', 
                    default='calibrate',
                    choices=['calibrate', 'predict'],
                    help='calibrate mode sets montecarlo iterations to 5, predict mode sets it to 150')
parser.add_argument('--controlstats', type=argparse.FileType('r'),
                    required=False,
                    help='path to control_stats.log file of previous calibration stage, will create coarse scenario if absent')
parser.add_argument('--step',
                    type=int,
                    default=25,
                    help='step hint for calibration interval (suggested: 25 for coarse, 5 for fine, 1 for final)')
parser.add_argument('--input_dir',
                    required=True,
                    help='path to input dir')
parser.add_argument('--output_dir',
                    required=True,
                    help='path to output dir')
parser.add_argument('--predict_start',
                    type=int,
                    required=True,
                    help='year of prediction start')
parser.add_argument('--predict_end',
                    type=int,
                    required=True,
                    help='year of prediction end')
parser.add_argument('--whirlgif_path',
                    required=True,
                    help='path to the whirlgif executable, usualy in .../sleuth_installation_folder/Whirlgif/')
parser.add_argument('--template', type=argparse.FileType('r'),
                    required=True,
                    help='path to screnario template file')

args = parser.parse_args()

if args.mode == 'calibrate':
    monte_carlo_iterations = 5
elif args.mode == 'predict':
    monte_carlo_iterations = 150


def step(Max, Start):
    if Max == 1:
        Max = 0
    if Max == Start:
        return args.step
    else:
        step = int(floor((Max - Start) / 4.0))
        if step < 1:
            return 1
        else:
            return step

def end(Start, Step):
    return Start + (4 * Step)

def start(Start, Max):
    if Start == 1:
        Start = 0
    if Max == 100 and Start == Max:
        Start = Max - (4 * args.step)
    return Start



if args.controlstats:
    widths = [7,8,8,8,8,8,8,8,8,8,8,8,8,8,5,5,5,5,5]
    df = pandas.read_fwf(args.controlstats, skiprows = 1, widths = widths)
    primeros10 = df.sort_values(by = 'Leesalee', ascending = False)[:10]
    best_fit = df.sort_values(by = 'Leesalee', ascending = False)[:1]

    diff = best_fit['Diff'].values[0]    
    diff_max = primeros10['Diff'].max()
    diff_start = start(primeros10['Diff'].min(), diff_max)
    diff_step = step(diff_max, diff_start)
    diff_end = end(diff_start, diff_step)

    brd = best_fit['Brd'].values[0]    
    brd_max = primeros10['Brd'].max()
    brd_start = start(primeros10['Brd'].min(), brd_max)
    brd_step = step(brd_max, brd_start)
    brd_end = end(brd_start, brd_step)

    sprd = best_fit['Sprd'].values[0]    
    sprd_max = primeros10['Sprd'].max()
    sprd_start = start(primeros10['Sprd'].min(), sprd_max)
    sprd_step = step(sprd_max, sprd_start)
    sprd_end = end(sprd_start, sprd_step)

    slp = best_fit['Slp'].values[0]    
    slp_max = primeros10['Slp'].max()
    slp_start = start(primeros10['Slp'].min(), slp_max)
    slp_step = step(slp_max, slp_start)
    slp_end = end(slp_start, slp_step)

    rg = best_fit['RG'].values[0]
    rg_max = primeros10['RG'].max()
    rg_start = start(primeros10['RG'].min(), rg_max)
    rg_step = step(rg_max, rg_start)
    rg_end = end(rg_start, rg_step)
else:
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


listOfUrbanLayers = []
listOfroadsLayers = [] 
for thisFile in os.listdir(args.input_dir):
    if ".gif" in thisFile and not "aux.xml" in thisFile and not thisFile.startswith("."):
        if ".urban." in thisFile:
            listOfUrbanLayers.append(thisFile)
        if ".roads." in thisFile:
            listOfroadsLayers.append(thisFile)
        if ".slope." in thisFile:
            slopeLayer = thisFile
        if ".hillshade." in thisFile:
            hillshadeLayer = thisFile
        if ".excluded." in thisFile:
            exclusionLayer = thisFile
        
listOfUrbanLayers.sort()
listOfroadsLayers.sort()

        
    
    
template = Template(args.template.read())
print template.render(
    whirlgif_path=args.whirlgif_path,
    input_dir=args.input_dir+"/",
    output_dir=args.output_dir + "/",
    diff_start=diff_start,
    diff_end=diff_end,
    diff_step=diff_step,
    brd_start=brd_start,
    brd_end=brd_end,
    brd_step=brd_step,
    sprd_start=sprd_start,
    sprd_end=sprd_end,
    sprd_step=sprd_step,
    slp_start=slp_start,
    slp_end=slp_end,
    slp_step=slp_step,
    rg_start=rg_start,
    rg_end=rg_end,
    rg_step=rg_step,
    diff=diff,
    brd=brd,
    sprd=sprd,
    slp=slp,
    rg=rg,
    monte_carlo_iterations=monte_carlo_iterations,
    predict_start=args.predict_start,
    predict_end=args.predict_end,
    urban=listOfUrbanLayers,
    roads=listOfroadsLayers,
    exclude=exclusionLayer,
    slope=slopeLayer,
    hillshade=hillshadeLayer)
