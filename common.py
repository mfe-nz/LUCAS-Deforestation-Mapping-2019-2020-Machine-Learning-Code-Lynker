# -*- coding: utf-8 -*-
# **************************** All rights reserved. Copyright (c) 2020 Lynker Analytics Ltd ****************************
# Author: David Knox
# Email: david.knox@lynker-analytics.com
# Date: 09/11/2020
# Common functions for neural network model training and loading
# Version: py3.7.5
# **********************************************************************************************************************

from keras.models import load_model
import tensorflow as tf
from keras.optimizers import Adam

eta=1e-9

#focal loss from here: https://github.com/mkocabas/focal-loss-keras
from keras import backend as K
def focal_loss(gamma=2., alpha=.25):
        def focal_loss_fixed(y_true, y_pred):
                eps=1e-7
                y_pred = K.clip(y_pred, eps, 1-eps)
                pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
                pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
                return -K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1))-K.sum((1-alpha) * K.pow( pt_0, gamma) * K.log(1. - pt_0))
        return focal_loss_fixed

#this is a workaround for loading existing models
def focal_loss_fixed(y_true, y_pred):
        gamma=2.
        alpha=.25
        eps=1e-7
        y_pred = K.clip(y_pred, eps, 1-eps)
        pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
        pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
        return -K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1))-K.sum((1-alpha) * K.pow( pt_0, gamma) * K.log(1. - pt_0))

def getmodel(modelfile):
	return load_model(modelfile)
