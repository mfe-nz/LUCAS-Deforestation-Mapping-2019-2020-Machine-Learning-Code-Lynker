# LUCAS 
* Land Cover inference using ML.
* This repository contains the model weights file (models/LUCAS_LA_2020.h5) and the code to run inference over rgb rasters.
* the output of this code is a classified raster

## input requirements
* RGB rasters in NZTM
* approx 25cm GSD

## subdirs:
```
	models/			#location of trained ML model
	indir/			#Put RGB input rasters here
	inferenceout/		#Land cover inference, classified raster will appear here
```

## components:
* models/LUCAS_LA_2020.h5 - the trained ML model
* publish_infer.py - the code to run inference
* pilutil.py - image handling helper functions from the scipy.misc project
* common.py - ML model loading

