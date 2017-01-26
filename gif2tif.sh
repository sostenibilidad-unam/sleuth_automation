#!/bin/bash

INGIF=$1
DIR=`dirname $INGIF`
BASE=$DIR/`basename $INGIF .gif`
TMPGIF=${BASE}_tmp.gif
OUTTIF=${BASE}.tif

echo $INGIF
echo $BASE
echo $TMPGIF
echo $OUTTIF

echo "Translating"
gdal_translate -of GTiff \
	       -gcp 9.64484e-10 9.51673e-10 380109 2.31806e+06 \
	       -gcp 2255 3.02695e-10 605609 2.31806e+06 \
	       -gcp 2255 2460 605609 2.07206e+06 \
	       -gcp 2.24945e-09 2460 380109 2.07206e+06 \
	       $INGIF \
	       $TMPGIF

echo "warping"
gdalwarp -r near \
	 -order 1 \
	 -co COMPRESS=NONE \
	 $TMPGIF \
	 $OUTTIF

echo "cleaning up"
rm $TMPGIF
