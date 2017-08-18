#!/bin/bash

source /srv/home/fidel/python_envs/sleuth/bin/activate

#
# usage: ./group_calibrate.sh LOCATION /path/to/location_dir
#
# location must be the prefix of the input data according to this documentation:
# http://www.ncgia.ucsb.edu/projects/gig/Imp/imSetUp.htm#namingConvention
# /srv/home/fidel/sleuth/grow
# /srv/home/fidel/sleuth/Whirlgif/whirlgif


REGIONS_DIR=$1
PREDICT_START=$2
PREDICT_END=$3
WHIRLGIF_PATH=$4
GROW_PATH=$5
CONDOR_FILE_NAME=$6



./create_condor_file_for_regions.py --whirlgif_path $WHIRLGIF_PATH \
				    --grow_path $GROW_PATH \
				    --region_dir $REGIONS_DIR \
				    --predict_start $PREDICT_START \
				    --predict_end $PREDICT_END \
				    --condor_file_name $CONDOR_FILE_NAME \



condor_submit $CONDOR_FILE_NAME

				    




