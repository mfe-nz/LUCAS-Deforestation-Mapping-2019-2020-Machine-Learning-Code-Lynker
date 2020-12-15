# -*- coding: utf-8 -*-
# **************************** All rights reserved. Copyright (c) 2020 Lynker Analytics Ltd ****************************
# Author: David Knox
# Email: david.knox@lynker-analytics.com
# Date: 09/11/2020
# Functionality: configuration
# Version: py3.7.5
# **********************************************************************************************************************

#---------------------------------------------------------
# files and directories
#---------------------------------------------------------
modelfile='models/LUCAS_LA_2020.h5'
pickledir='pickles'
outdir='inferenceout/'
indir='indir/'

#---------------------------------------------------------
# image handling configuration 
#---------------------------------------------------------
dim=300
border=130
batch_size=256
shadow=[15,60,140]

#---------------------------------------------------------
# Profile template for raster outputs
#---------------------------------------------------------
from rasterio.crs import CRS
from rasterio.transform import Affine
profile={'driver': 'GTiff', 'dtype': 'uint8', 'nodata': 255, 'width': 319, 'height': 327, 'count': 1, 'crs': CRS.from_wkt('LOCAL_CS["NZGD_2000_New_Zealand_Transverse_Mercator",GEOGCS["GCS_NZGD_2000",DATUM["D_NZGD_2000",SPHEROID["GRS_1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6167"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4167"]],AUTHORITY["EPSG","2193"],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]'), 'transform': Affine(0.49036188179562834, 0.0, 1887840.011026467,
       0.0, -0.6657987466247166, 5819624.259919928), 'blockxsize': 128, 'blockysize': 128, 'tiled': True, 'compress': 'lzw', 'interleave': 'pixel', 'bigtiff':True}
