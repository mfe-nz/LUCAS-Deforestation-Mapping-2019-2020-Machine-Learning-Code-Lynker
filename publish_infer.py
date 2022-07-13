# -*- coding: utf-8 -*-
# **************************** All rights reserved. Copyright (c) 2020 Lynker Analytics Ltd ****************************
# Author: David Knox
# Email: david.knox@lynker-analytics.com
# Date: 09/11/2020
# Functionality: Using input raster files, output prediction of land cover class for forestry area
# Version: py3.7.5
# **********************************************************************************************************************
# Modified: David Knox July 2022 use pillow, py3.8.10
# **********************************************************************************************************************
import numpy as np
from os import listdir
from os.path import isfile
import re
import rasterio
from copy import deepcopy as cp
from rasterio.crs import CRS
from rasterio.transform import Affine
from PIL import Image,ImageEnhance
from common import *
from rasterio.windows import Window
import pickle
from config import *

from time import time

#---------------------------------------------------------
# Load neural network model file
#---------------------------------------------------------
print ( modelfile )
model=getmodel(modelfile)

#---------------------------------------------------------
# Check config
#---------------------------------------------------------
step = dim - 2*border
assert step == 40
assertsmallchipshape=(40,40,3)

#---------------------------------------------------------
# Load work list
#---------------------------------------------------------
infiles=listdir(indir)

def infer(dst,X_smallchips,X_bigchips,X_Windows):
	Ps=model.predict([np.array(X_smallchips),np.array(X_bigchips)])

	#---------------------------------------------------------
	# Numpy channels (axis=-1) reference
	#---------------------------------------------------------
	"""
	#0      Built Forest (skid site, access tracks)
	#1      Built Other (pavement, buildings)
	#2      Crop
	#3      Cutover
	#4      Exotic regenerating forest
	#5      Grass/Pasture
	#6      Mature Exotic Forest
	#7      Mature Native Forest
	#8      Natural Other (scree, river, pond, slip)
	#9      Natural regenerating forest
	#10     Plantation Seedlings
	#11	Water
	"""

	#---------------------------------------------------------
	# Post inference adjustments - may not be needed
	#---------------------------------------------------------
	"""
	Ps[:,10] += Ps[:,2]     #add Crop to Plantation
	Ps[:,2] *= 0.0  	#2      Crop
	Ps[:,11] *= 0.0   	#11   Water

	Ps[:,0] *= .2   	#0	Built skid sie, access tracks
	Ps[:,1] *= .5   	#1	Built Other
	Ps[:,6] *= 3.0   	#6	mature exotic
	Ps[:,5] *= 3.0   	#6	grass
	"""

	for i in range(len(Ps)):
		p=Ps[i]
		win=X_Windows[i]
		dst.write(np.argmax(p).astype(np.uint8).reshape((1,1)), window=win, indexes=1)
	return True

counter=0
for f in infiles:
	if re.search(".jpg$",f) or re.search(".tif$",f):
		if True:
			print ( 'starting', f, flush=True )
			counter+=1
			raster=rasterio.open(indir+f)
			profile=raster.profile
			profile.update(
				crs=CRS.from_epsg(2193),
				nodata=255
			)
	
			outfile=outdir+f.replace('.jpg','_ML.tif')
			imgoutfile=outdir+f.replace('.jpg','_rgb.jpg')
			mlprofile.update(
				transform=profile['transform'],
				width=profile['width'],
				height=profile['height']
			)

			dst=rasterio.open(outfile,'w',**mlprofile)
			im=np.zeros((raster.height,raster.width,raster.count),dtype=np.uint16)
			im[:,:,0]=raster.read(1)
			im[:,:,1]=raster.read(2)
			im[:,:,2]=raster.read(3)

			(h,w,c)=im.shape
			outf=f.replace('.jpg','')
	
			t1=time()
	
			b=0
			X_smallchips=[]
			X_bigchips=[]
			X_Windows=[]
	
			for x in range(0,w,step):
				for y in range(0,h,step):
					bigchip=cp(im[y:y+dim,x:x+dim,:]).astype(np.float32)
					smallchip=cp(bigchip[border:-border,border:-border,:])
	
					isshadow = (smallchip[:,:,0] < shadow[0]) & (smallchip[:,:,1] < shadow[1]) & (smallchip[:,:,2] < shadow[2])
	
					if np.mean(isshadow) < 0.7:
	
						bigchip-=np.min(bigchip)
						bigchip/=np.max(bigchip)
						bigchip*=255

						smallchip=cp(bigchip[border:-border,border:-border,:])
	
						bigchip[border:border+2,border:-border,:]=0
						bigchip[border:border+2,border:-border,0]=255
		
						bigchip[-border:-border+2,border:-border,:]=0
						bigchip[-border:-border+2,border:-border,0]=255
		
						bigchip[border:-border,border:border+2,:]=0
						bigchip[border:-border,border:border+2,0]=255
		
						bigchip[border:-border,-border:-border+2,:]=0
						bigchip[border:-border,-border:-border+2,0]=255
		
						bigoutfile=outdir+'/context/'+f+'_'+str(x)+'_'+str(y)+'.jpg'
						smalloutfile=outdir+f+'_'+str(x)+'_'+str(y)+'.jpg'
						if assertsmallchipshape == smallchip.shape:
							if np.max(smallchip) < 256:
								bigchip[bigchip==256]=0
								smallchip[smallchip==256]=0

								bigchip=ImageEnhance.Color(Image.fromarray(bigchip.astype(np.uint8))).enhance(2).resize((299,299))
								smallchip=ImageEnhance.Color(Image.fromarray(smallchip.astype(np.uint8))).enhance(2).resize((299,299))

								X_smallchips.append(np.array(smallchip)/255.)
								X_bigchips.append(np.array(bigchip)/255.)
								X_Windows.append(Window(x+border,y+border,step,step))
								b+=1
	
								if b >= batch_size:
									infer(dst,X_smallchips,X_bigchips,X_Windows)
									b=0
									X_smallchips=[]
									X_bigchips=[]
									X_Windows=[]
	
	
			if b>0:
				infer(dst,X_smallchips,X_bigchips,X_Windows)
			t2=time()
	
			print ( 'done', counter, f, 'in', t2-t1, 'seconds', flush=True )

print ( 'done.' )	
