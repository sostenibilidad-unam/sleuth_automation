#!/bin/bash

ROOT=/srv/home/fidel/Para_SLEUTH
INPUT=$ROOT/Grupo1

echo "50 50 50 50 50" | ./calibrate.py --input_dir $INPUT \
				       --output_dir $ROOT/Grupo1/out \
				       --urban $INPUT/Group1.urban.1980.gif \
  				           $INPUT/Group1.urban.1990.gif \
					   $INPUT/Group1.urban.2000.gif \
					   $INPUT/Group1.urban.2011.gif \
				       --roads $INPUT/Group1.roads.1980.gif \
				           $INPUT/Group1.roads.1990.gif \
					   $INPUT/Group1.roads.2000.gif \
					   $INPUT/Group1.roads.2011.gif \
				       --exclude $INPUT/Group1.excluded.gif \
				       --slope $INPUT/Group1.slope.gif \
				       --hillshade $INPUT/Group1.hillshade.gif \
				       --predict_start 2011 \
				       --predict_end 2060 \
				       --template scenario_template.jinja \
				       --span 50 \
				       > scenario.group1.coarse
