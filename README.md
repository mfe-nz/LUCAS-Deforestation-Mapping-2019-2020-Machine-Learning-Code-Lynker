# LUCAS 
* Land Cover inference using ML.
* This repository contains the code to run landcover inference over rgb rasters.
* This repository does not contain the model weights file (models/publish_LUCAS_2022.h5)
** the weights file is too large to store in github as versioned code. However, the weights file is stored in the release (release1).
* the output of this code is a classified raster

## input requirements
* RGB rasters in NZTM
* approx 20cm GSD

## subdirs:
```
	models/			#location of trained ML model
	indir/			#Put RGB input rasters here
	inferenceout/		#Land cover inference, classified raster will appear here
```

## components:
* models/publish_LUCAS_2022.h5 - the trained ML model
* publish_infer.py - the code to run inference
* pilutil.py - image handling helper functions from the scipy.misc project
* common.py - ML model loading

## output landcover classes:
        * 0      Built Forest (skid site, access tracks)
        * 1      Built Other (pavement, buildings)
        * 2      Crop
        * 3      Cutover
        * 4      Exotic regenerating forest
        * 5      Grass/Pasture
        * 6      Mature Exotic Forest
        * 7      Mature Native Forest
        * 8      Natural Other (scree, river, pond, slip)
        * 9      Natural regenerating forest
        * 10     Plantation Seedlings
        * 11     Water

## New Zealand deforestation mapping 2019 and 2020 Technical report - Lynker Analytics
https://environment.govt.nz/publications/new-zealand-deforestation-mapping-2019-and-2020-technical-report/
