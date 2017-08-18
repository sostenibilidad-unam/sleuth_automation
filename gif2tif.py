#!/usr/bin/env python

import argparse
import sys
import json
import os
from os.path import join
import subprocess

# python create_scenario_file.py --mode calibrate --input_dir /srv/home/fidel/Para_SLEUTH/Group1 --output_dir . --predict_start 2011 --predict_end 2060 --whirlgif_path /srv/home/fidel/sleuth/Whirlgif/whirlgif --template /srv/home/fidel/sleuth_automation/sleuth_scenario_template.jinja 
# falta que el path al whirlgif sea un parametro tambien


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--path', 
                    required=True,
                    help='path to the folder')
parser.add_argument('--predict_start',
                    type=int,
                    required=True,
                    help='year of prediction start')
parser.add_argument('--predict_end',
                    type=int,
                    required=True,
                    help='year of prediction end')



args = parser.parse_args()

carpetas = []
for folder in os.listdir(args.path):
    if os.path.isdir(join(args.path, folder)):
        print folder
        with open(join(join(args.path, folder),'extent.json')) as data_file:    
            data = json.load(data_file)
        print data["epsg"]
        columnas = str(int(data["columns"]) - 1)
        renglones = str(int(data["rows"]) - 1)
        epsg = 'EPSG:' + data["epsg"]
        xmin = str(data["xmin"])
        xmax = str(data["xmax"])
        ymin = str(data["ymin"])
        ymax = str(data["ymax"])
        carpetas.append(folder)
        for esteFile in os.listdir(join(join(join(args.path, folder),"out"), "prediction")):
            if ".gif" in esteFile:
                print esteFile
                elGif = join(join(join(join(args.path, folder),"out"), "prediction"), esteFile)
                elTif = elGif[:-4]+"_temp.tif"
                print 'gdal_translate', '-a_srs', epsg, '-of', 'GTiff', '-gcp', '0', renglones, xmin, ymin, '-gcp', columnas, renglones, xmax, ymin, '-gcp', columnas, '0', xmax, ymax, '-gcp', '0', '0', xmin, ymax, elGif, elTif
                subprocess.check_call(['gdal_translate', '-a_srs', epsg, '-ot', 'Float64', '-of', 'GTiff', '-gcp', '0', renglones, xmin, ymin, '-gcp', columnas, renglones, xmax, ymin, '-gcp', columnas, '0', xmax, ymax, '-gcp', '0', '0', xmin, ymax, elGif, elTif])


        for esteFile in os.listdir(join(join(join(args.path, folder),"out"), "prediction")):
            if "temp.tif" in esteFile and not esteFile.endswith("xml"):
                print esteFile
                eltempTiff = join(join(join(join(args.path, folder),"out"), "prediction"), esteFile)
                elTif = eltempTiff.replace("_temp", "")
                #otbcli_BandMath -il Coyoacan_urban_2042.tif -out test3.tif -exp "im1b1 < 9 ? im1b1 : 0"
                subprocess.check_call(['otbcli_BandMath', '-il', eltempTiff, '-out', elTif, '-exp', 'im1b1 < 9 ? im1b1 : 0'])               


#otbcli_BandMath -il im1.tif im2.tif im3.tif -out max.tif -exp "max(im1b1, im2b1,im3b1)"
##for year in range(args.predict_start, args.predict_end):
##    commandList = ['otbcli_BandMath', '-il']
##
##    
##    for carpeta in carpetas:
##        commandList.append(join(join(join(join(args.path, carpeta),"out"), "prediction"), carpeta + "_urban_" + str(year) + ".tif"))
##
##    commandList.append('-out')
##    commandList.append(join(args.path,'urban_' + str(year) + ".tif"))
##    commandList.append('-exp')
##
##    expresion = "max(im1b1"
##    for imageNumber in range(2,len(carpetas)):
##        expresion = expresion + ", im" + str(imageNumber) + "b1"
##
##    expresion = expresion + ")"
##    commandList.append(expresion)
##    print commandList
##    subprocess.check_call(commandList)
        
