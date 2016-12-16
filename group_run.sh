#!/bin/bash

source /srv/home/fidel/python_envs/sleuth/bin/activate 

GRUPO=Group$1
ROOT=/srv/home/fidel/Para_SLEUTH
INPUT=$ROOT/$GRUPO


mkdir -p $ROOT/$GRUPO/out/coarse
echo "50 50 50 50 50" | ./calibrate.py --input_dir $INPUT \
				       --output_dir $ROOT/$GRUPO/out/coarse \
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
				       --span 50 \
				       > scenario.$GRUPO.coarse

/srv/home/fidel/sleuth/grow calibrate scenario.$GRUPO.coarse

mkdir -p $ROOT/$GRUPO/out/fine
./extract_params.sh $ROOT/$GRUPO/out/coarse/control_stats.log | ./calibrate.py --input_dir $INPUT \
				       --output_dir $ROOT/$GRUPO/out/fine \
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
				       --span 10 \
				       > scenario.$GRUPO.fine

/srv/home/fidel/sleuth/grow calibrate scenario.$GRUPO.fine

mkdir -p $ROOT/$GRUPO/out/final
./extract_params.sh $ROOT/$GRUPO/out/fine/control_stats.log | ./calibrate.py --input_dir $INPUT \
									     --output_dir $ROOT/$GRUPO/out/final \
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
				       --span 2 \
				       > scenario.$GRUPO.final

/srv/home/fidel/sleuth/grow calibrate scenario.$GRUPO.final
