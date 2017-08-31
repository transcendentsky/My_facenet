#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 16:17:59 2017

@author: trans
"""
import numpy as np
probs = np.zeros((7,7,2,20))
filter_mat_probs = np.array(probs>=0.2,dtype='bool')
filter_mat_boxes = np.nonzero(filter_mat_probs) # nonzero() takes exactly 1 argument 