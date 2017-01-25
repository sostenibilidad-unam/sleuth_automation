#!/bin/bash

source /srv/home/fidel/python_envs/sleuth/bin/activate

GRUPO=Group$1
ROOT=/srv/home/fidel/Para_SLEUTH
INPUT=$ROOT/$GRUPO

mkdir -p $ROOT/$GRUPO/out/prediction

./create_scenario.py --input_dir $INPUT \
		     --output_dir $ROOT/$GRUPO/out/prediction \
		     --controlstats $ROOT/$GRUPO/out/final/control_stats.log \
		     --urban $INPUT/$GRUPO.urban.1980.gif \
		     $INPUT/$GRUPO.urban.1990.gif \
		     $INPUT/$GRUPO.urban.2000.gif \
		     $INPUT/$GRUPO.urban.2011.gif \
		     --roads $INPUT/$GRUPO.roads.1980.gif \
		     $INPUT/$GRUPO.roads.1990.gif \
		     $INPUT/$GRUPO.roads.2000.gif \
		     $INPUT/$GRUPO.roads.2011.gif \
		     --exclude $INPUT/$GRUPO.excluded.gif \
		     --slope $INPUT/$GRUPO.slope.gif \
		     --hillshade $INPUT/$GRUPO.hillshade.gif \
		     --predict_start 2011 \
		     --predict_end 2060 \
		     --template scenario_template.jinja \
		     --step 1 \
		     --mode predict \
		     > scenario.$GRUPO.predict

mpirun -np 40 /srv/home/fidel/sleuth/grow predict scenario.$GRUPO.predict
