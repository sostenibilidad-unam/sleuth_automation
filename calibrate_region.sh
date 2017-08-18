#!/bin/bash

source /srv/home/fidel/python_envs/sleuth/bin/activate

#
# usage: ./group_calibrate.sh LOCATION /path/to/location_dir
#
# location must be the prefix of the input data according to this documentation:
# http://www.ncgia.ucsb.edu/projects/gig/Imp/imSetUp.htm#namingConvention
# /srv/home/fidel/sleuth/grow
# /srv/home/fidel/sleuth/Whirlgif/whirlgif


LOCATION=$1
LPATH=$2
PREDICT_START=$3
PREDICT_END=$4
WHIRLGIF_PATH=$5
GROW_PATH=$6


OUTDIR=$LPATH/out/coarse
mkdir -p $OUTDIR
./create_scenario_file.py --input_dir $LPATH \
			  --output_dir $OUTDIR \
			  --whirlgif_path $WHIRLGIF_PATH \
			  --predict_start $PREDICT_START \
			  --predict_end $PREDICT_END \
			  --template sleuth_scenario_template.jinja \
			  --step 25 \
			  > $LPATH/scenario.$LOCATION.coarse

mpirun -np 40 $GROW_PATH calibrate $LPATH/scenario.$LOCATION.coarse

OUTDIR=$LPATH/out/fine
mkdir -p $OUTDIR

./create_scenario_file.py --input_dir $LPATH \
			  --output_dir $OUTDIR \
			  --whirlgif_path $WHIRLGIF_PATH \
			  --controlstats $LPATH/out/coarse/control_stats.log \
			  --predict_start $PREDICT_START \
			  --predict_end $PREDICT_END \
			  --template sleuth_scenario_template.jinja \
			  --step 5 \
			  > $LPATH/scenario.$LOCATION.fine

mpirun -np 40 $GROW_PATH calibrate $LPATH/scenario.$LOCATION.fine

OUTDIR=$LPATH/out/final
mkdir -p $OUTDIR

./create_scenario_file.py --input_dir $LPATH \
			  --output_dir $OUTDIR \
			  --whirlgif_path $WHIRLGIF_PATH \
			  --controlstats $LPATH/out/fine/control_stats.log \
			  --predict_start $PREDICT_START \
			  --predict_end $PREDICT_END \
			  --template sleuth_scenario_template.jinja \
			  --step 1 \
			  > $LPATH/scenario.$LOCATION.final

mpirun -np 40 $GROW_PATH calibrate $LPATH/scenario.$LOCATION.final


OUTDIR=$LPATH/out/prediction
mkdir -p $OUTDIR

./create_scenario_file.py --input_dir $LPATH \
			  --output_dir $OUTDIR \
			  --whirlgif_path $WHIRLGIF_PATH \
			  --controlstats $LPATH/out/final/control_stats.log \
			  --predict_start $PREDICT_START \
			  --predict_end $PREDICT_END \
			  --template sleuth_scenario_template.jinja \
			  --step 1 \
			  --mode predict \
			  > $LPATH/scenario.$LOCATION.predict

mpirun -np 1 $GROW_PATH predict $LPATH/scenario.$LOCATION.predict


