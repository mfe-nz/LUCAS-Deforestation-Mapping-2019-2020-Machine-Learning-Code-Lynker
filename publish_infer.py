# -*- coding: utf-8 -*-
# **************************** All rights reserved. Copyright (c) 2020 Lynker Analytics Ltd ****************************
# Author: David Knox
# Email: david.knox@lynker-analytics.com
# Date: 09/11/2020
# Functionality: Using input raster files, output prediction of land cover class for forestry area
# Version: py3.7.5
# **********************************************************************************************************************
import numpy as np
from os import listdir
from os.path import isfile
import re
import rasterio
from copy import deepcopy as cp
from pilutil import imresize
from common import *
from rasterio.windows import Window
import pickle
from config import *

from time import time

#---------------------------------------------------------
# Load neural network model file
#---------------------------------------------------------
model=getmodel(modelfile)

#---------------------------------------------------------
# configuration 
#---------------------------------------------------------
step = dim - 2*border
assert step == 40
assertsmallchipshape=(40,40,3)

infiles=listdir(indir)

def infer(dst,X_smallchips,X_bigchips,X_Windows,name):
	Ps=model.predict([np.array(X_smallchips),np.array(X_bigchips)])
	np.save(pickledir+'/'+name,Ps)

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
	# Post inference adjustments
	#---------------------------------------------------------
	Ps[:,10] += Ps[:,2]     #add Crop to Plantation
	Ps[:,2] *= 0.0  	#2      Crop
	Ps[:,11] *= 0.0   	#11   Water

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
			profile_new=raster.profile
			profile.update(
				transform=profile_new['transform'],
				width=profile_new['width'],
				height=profile_new['height']
			)
	
			outfile=outdir+f.replace('.jpg','.tif')
			dst=rasterio.open(outfile,'w',**profile)
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
					bigchip=cp(im[y:y+dim,x:x+dim,:])
					smallchip=cp(bigchip[border:-border,border:-border,:])
	
					isshadow = (smallchip[:,:,0] < shadow[0]) & (smallchip[:,:,1] < shadow[1]) & (smallchip[:,:,2] < shadow[2])
	
					if np.mean(isshadow) < 0.7:
	
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
								bigchip=imresize(bigchip,(299,299)).reshape((299,299,3))/255.
								smallchip=imresize(smallchip,(299,299)).reshape((299,299,3))/255.
	
								X_smallchips.append(smallchip)
								X_bigchips.append(bigchip)
								X_Windows.append(Window(x+border,y+border,step,step))
								name=f+'_'+str(x)+'_'+str(y)
								b+=1
	
								if b >= batch_size:
									infer(dst,X_smallchips,X_bigchips,X_Windows,name)
									b=0
									X_smallchips=[]
									X_bigchips=[]
									X_Windows=[]
	
			if b>0:
				infer(dst,X_smallchips,X_bigchips,X_Windows,name)
			t2=time()
	
			print ( 'done', counter, f, 'in', t2-t1, 'seconds', flush=True )


print ( 'done.' )	
