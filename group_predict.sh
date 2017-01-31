#!/bin/bash

source /srv/home/fidel/python_envs/sleuth/bin/activate

#
# usage: ./group_predit.sh LOCATION /path/to/location_dir
#
# location must be the prefix of the input data according to this documentation:
# http://www.ncgia.ucsb.edu/projects/gig/Imp/imSetUp.htm#namingConvention

LOCATION=$1
LPATH=$2

OUTDIR=$LPATH/out/prediction
mkdir -p $OUTDIR

./create_scenario.py --input_dir $LPATH \
		     --output_dir $OUTDIR \
		     --controlstats $LPATH/out/final/control_stats.log \
		     --urban $LPATH/${LOCATION}.urban.1980.gif \
		       $LPATH/${LOCATION}.urban.1990.gif \
		       $LPATH/${LOCATION}.urban.2000.gif \
		       $LPATH/${LOCATION}.urban.2011.gif \
		     --roads $LPATH/${LOCATION}.roads.1980.gif \
		       $LPATH/${LOCATION}.roads.1990.gif \
		       $LPATH/${LOCATION}.roads.2000.gif \
		       $LPATH/${LOCATION}.roads.2011.gif \
		     --exclude $LPATH/${LOCATION}.excluded.gif \
		     --slope $LPATH/${LOCATION}.slope.gif \
		     --hillshade $LPATH/${LOCATION}.hillshade.gif \
		     --predict_start 2011 \
		     --predict_end 2060 \
		     --template scenario_template.jinja \
		     --step 1 \
		     --mode predict \
		     > $LPATH/scenario.$LOCATION.predict

mpirun -np 40 /srv/home/fidel/sleuth/grow predict $LPATH/scenario.$LOCATION.predict
