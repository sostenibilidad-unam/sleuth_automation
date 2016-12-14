#!/usr/bin/env python

import argparse
import sys

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
args = parser.parse_args()


for line in args.parameters.readlines():
    (product, run, diff, brd, sprd, slp, rg) = line.strip().split()
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


    
print "(product, run, diff, brd, sprd, slp, rg) "
print     (product, run, diff, brd, sprd, slp, rg) 
print "diff_start, diff_end, brd_start, brd_end, sprd_start, sprd_end, slp_start, slp_end, rg_start, rg_end"
print diff_start, diff_end, brd_start, brd_end, sprd_start, sprd_end, slp_start, slp_end, rg_start, rg_end



"""
INPUT_DIR={input_dir
OUTPUT_DIR={output_dir
WHIRLGIF_BINARY=/srv/home/fidel/sleuth/Whirlgif/whirlgif 
ECHO(YES/NO)=yes 
WRITE_COEFF_FILE(YES/NO)=yes
WRITE_AVG_FILE(YES/NO)=yes
WRITE_STD_DEV_FILE(YES/NO)=yes 
WRITE_MEMORY_MAP(YES/NO)=yes
LOGGING(YES/NO)=YES
LOG_LANDCLASS_SUMMARY(YES/NO)=yes 
LOG_SLOPE_WEIGHTS(YES/NO)=no 
LOG_READS(YES/NO)=no
LOG_WRITES(YES/NO)=no
LOG_COLORTABLES(YES/NO)=no
LOG_PROCESSING_STATUS(0:off/1:low verbosity/2:high verbosity)=1 
LOG_TRANSITION_MATRIX(YES/NO)=no
LOG_URBANIZATION_ATTEMPTS(YES/NO)=no 
LOG_INITIAL_COEFFICIENTS(YES/NO)=no 
LOG_BASE_STATISTICS(YES/NO)=yes 
LOG_DEBUG(YES/NO)= no
LOG_TIMINGS(0:off/1:low verbosity/2:high verbosity)=1
NUM_WORKING_GRIDS=8
RANDOM_SEED=1
MONTE_CARLO_ITERATIONS=5

CALIBRATION_DIFFUSION_START= 0 
CALIBRATION_DIFFUSION_STEP=  25 
CALIBRATION_DIFFUSION_STOP=  100 

CALIBRATION_BREED_START=     0 
CALIBRATION_BREED_STEP=      25 
CALIBRATION_BREED_STOP=      100 

CALIBRATION_SPREAD_START=    0 
CALIBRATION_SPREAD_STEP=     25 
CALIBRATION_SPREAD_STOP=     100 

CALIBRATION_SLOPE_START=     0 
CALIBRATION_SLOPE_STEP=      25 
CALIBRATION_SLOPE_STOP=      100 

CALIBRATION_ROAD_START=      0 
CALIBRATION_ROAD_STEP=       25 
CALIBRATION_ROAD_STOP=       100 

PREDICTION_DIFFUSION_BEST_FIT=  20 
PREDICTION_BREED_BEST_FIT=  20 
PREDICTION_SPREAD_BEST_FIT=  20 
PREDICTION_SLOPE_BEST_FIT=  20 
PREDICTION_ROAD_BEST_FIT=  20 

PREDICTION_START_DATE=2000 
PREDICTION_STOP_DATE=2025 

URBAN_DATA= cmex250.urban.1960.gif 
URBAN_DATA= cmex250.urban.1982.gif 
URBAN_DATA= cmex250.urban.1997.gif 
URBAN_DATA= cmex250.urban.2000.gif 

ROAD_DATA= cmex250.roads.1960.gif 
ROAD_DATA= cmex250.roads.1982.gif 
ROAD_DATA= cmex250.roads.1997.gif 
ROAD_DATA= cmex250.roads.2000.gif 

EXCLUDED_DATA= cmex250.excluded.gif 

SLOPE_DATA= cmex250.slope.gif 

BACKGROUND_DATA= cmex250.hillshade.gif 

WRITE_COLOR_KEY_IMAGES(YES/NO)=no 
ECHO_IMAGE_FILES(YES/NO)=no
ANIMATION(YES/NO)= no 

DATE_COLOR=     0XFFFFFF #white 

SEED_COLOR=  249, 209, 110 #pale yellow 

WATER_COLOR=  20, 52, 214 # royal blue

PROBABILITY_COLOR=   0,    50,         , #transparent 
PROBABILITY_COLOR=   50,   60, 0X005A00, #0, 90,0 dark green
PROBABILITY_COLOR=   60,   70, 0X008200, #0,130,0 
PROBABILITY_COLOR=   70,   80, 0X00AA00, #0,170,0 
PROBABILITY_COLOR=   80,   90, 0X00D200, #0,210,0 
PROBABILITY_COLOR=   90,   95, 0X00FF00, #0,255,0 light green
PROBABILITY_COLOR=   95,  100, 0X8B0000, #dark red 

LANDUSE_CLASS=  0,  Unclass , UNC   , 0X000000 
LANDUSE_CLASS=  1,  Urban   , URB   , 0X8b2323 #dark red
LANDUSE_CLASS=  2,  Agric   ,       , 0Xffec8b #pale yellow 
LANDUSE_CLASS=  3,  Range   ,       , 0Xee9a49 #tan 
LANDUSE_CLASS=  4,  Forest  ,       , 0X006400 
LANDUSE_CLASS=  5,  Water   , EXC   , 0X104e8b 
LANDUSE_CLASS=  6,  Wetland ,       , 0X483d8b 
LANDUSE_CLASS=  7,  Barren  ,       , 0Xeec591 

VIEW_GROWTH_TYPES(YES/NO)=NO 
GROWTH_TYPE_PRINT_WINDOW=0,0,0,0,1995,2020 
PHASE0G_GROWTH_COLOR=  0xff0000 # seed urban area 
PHASE1G_GROWTH_COLOR=  0X00ff00 # diffusion growth 
PHASE2G_GROWTH_COLOR=  0X0000ff # NOT USED 
PHASE3G_GROWTH_COLOR=  0Xffff00 # breed growth 
PHASE4G_GROWTH_COLOR=  0Xffffff # spread growth 
PHASE5G_GROWTH_COLOR=  0X00ffff # road influenced growth 

VIEW_DELTATRON_AGING(YES/NO)=NO 
DELTATRON_PRINT_WINDOW=0,0,0,0,1930,2020 
DELTATRON_COLOR=  0x000000 # index 0 No or dead deltatron 
DELTATRON_COLOR=  0X00FF00 # index 1 age = 1 year 
DELTATRON_COLOR=  0X00D200 # index 2 age = 2 year 
DELTATRON_COLOR=  0X00AA00 # index 3 age = 3 year 
DELTATRON_COLOR=  0X008200 # index 4 age = 4 year 
DELTATRON_COLOR=  0X005A00 # index 5 age = 5 year 

ROAD_GRAV_SENSITIVITY=0.01 
SLOPE_SENSITIVITY=0.1 
CRITICAL_LOW=0.97 
CRITICAL_HIGH=1.3 

CRITICAL_SLOPE=21.0 
BOOM=1.01 
BUST=0.9"""
