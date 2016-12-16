#!/usr/bin/env python

import argparse
import sys
from jinja2 import Template

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--parameters', type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='five parameters with the largest product')
parser.add_argument('--input_dir',
                    required=True,
                    help='path to input dir')
parser.add_argument('--output_dir',
                    required=True,
                    help='path to output dir')
parser.add_argument('--urban', type=argparse.FileType('r'),
                    required=True,
                    nargs="+",
                    help='one or more urban gifs')
parser.add_argument('--roads', type=argparse.FileType('r'),
                    required=True,
                    nargs="+",
                    help='one or more roads gifs')
parser.add_argument('--exclude', type=argparse.FileType('r'),
                    required=True,
                    help='exclude gif')
parser.add_argument('--slope', type=argparse.FileType('r'),
                    required=True,
                    help='slope gif')
parser.add_argument('--hillshade', type=argparse.FileType('r'),
                    required=True,
                    help='hillshade gif')
parser.add_argument('--predict_start',
                    type=int,
                    required=True,
                    help='year of prediction start')
parser.add_argument('--predict_end',
                    type=int,
                    required=True,
                    help='year of prediction end')
parser.add_argument('--template', type=argparse.FileType('r'),
                    required=True,
                    help='path to screnario template file')

args = parser.parse_args()


for line in args.parameters.readlines():
    (diff, brd, sprd, slp, rg) = line.strip().split()
    diff = int(diff)
    brd = int(brd)
    sprd = int(sprd)
    slp = int(slp)
    rg = int(rg)

def rescale(par):
    if par == 100:
        return 90
    elif par == 1:
        return 11
    else:
        return par

diff_start = rescale(diff) - 10
diff_end = rescale(diff) + 10

brd_start = rescale(brd) - 10
brd_end = rescale(brd )+ 10

sprd_start = rescale(sprd) - 10
sprd_end = rescale(sprd) + 10

slp_start = rescale(slp) - 10
slp_end = rescale(slp )+ 10

rg_start = rescale(rg) - 10
rg_end = rescale(rg) + 10

template = Template(args.template.read())
print template.render(
    input_dir=args.input_dir,
    output_dir=args.output_dir,
    diff_start=diff_start,
    diff_end=diff_end,
    brd_start=brd_start,
    brd_end=brd_end,
    sprd_start=sprd_start,
    sprd_end=sprd_end,
    slp_start=slp_start,
    slp_end=slp_end,
    rg_start=rg_start,
    rg_end=rg_end,
    diff=diff,
    brd=brd,
    sprd=sprd,
    slp=slp,
    rg=rg,
    urban=[p.name for p in args.urban],
    roads=[p.name for p in args.roads],    
    predict_start=args.predict_start,
    predict_end=args.predict_end,
    exclude=args.exclude.name,
    slope=args.slope.name,
    hillshade=args.hillshade.name)
