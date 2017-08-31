#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:06:53 2017

@author: trans
"""
from __future__ import division
from __future__ import absolute_import

import tensorflow as tf
import numpy as np
import os , sys
import cv2

BASE_PATH = "/media/trans/NewVolume/Data/Face/LFW"

def img_to_array(img):
    x = np.asarray(img)
    return x

def select_contrast(batch_1, batch_2, alpha = 5):
    first_pic = True
    for i in xrange(batch_1.shape[0]):
        pic_1 = batch_1[i]
        pic_2 = batch_2[i]
        pos_dist = np.sum(np.square(pic_1 - pic_2))/float(batch_1.shape[1]*batch_1.shape[2])
        neg_dist = []
        a = [i]
        for j in xrange(batch_1.shape[0]):
            if j!=i:
                test_pic = batch_1[j]
                dist = np.sum(np.square(pic_1 - test_pic))/float(batch_1.shape[1]*batch_1.shape[2])
                if dist - pos_dist < alpha:
                    neg_dist.append(j)
        if len(neg_dist) == 0:
            x3_idx = (i + 1)%batch_1.shape[0]
        else:
            x3_idx = neg_dist[np.random.randint(len(neg_dist))]
        x3 = batch_1[x3_idx]
        x3 = np.expand_dims(x3,axis=0)
        if first_pic == True:
            batch_3 = x3
            first_pic = False
        else:
            batch_3 = np.concatenate((batch_3,x3))
            
    return batch_3

pic_idx = 1


def get_img_tribatch(pairfile, batchsize):
    global pic_idx
    print pic_idx
    start_idx = pic_idx
    end_idx = pic_idx + batchsize
    first_pic = True
    
    try:
        fid = open(pairfile, 'rw+')
    except Exception:
        raise Exception
        
    # pass x lines
    for i in xrange(pic_idx):
        line = fid.readline()
    
    while (pic_idx < end_idx):
        
        line = fid.readline()
        if line:
            pic_idx += 1
            data_info = line.split('\t')
            img_name_1 = os.path.join(BASE_PATH,'lfw',data_info[0],data_info[0]+'_'+'%04d'%int(data_info[1])) + '.jpg'
            img_name_2 = os.path.join(BASE_PATH,'lfw',data_info[0],data_info[0]+'_'+'%04d'%int(data_info[2])) + '.jpg'
            img1 = cv2.imread(img_name_1, 1)           
            cv2.resize(img1, (224,224))
            img2 = cv2.imread(img_name_2, 1)
            cv2.resize(img2, (224,224))
                   
            x1 = img_to_array(img1)        
            x2 = img_to_array(img2)
            
            x1 = np.expand_dims(x1, axis=0)
            x2 = np.expand_dims(x2, axis=0)
            
            if first_pic == True:
                batch_pic_1 = x1
                batch_pic_2 = x2
                first_pic = False
            else:
                batch_pic_1 = np.concatenate((batch_pic_1, x1))
                batch_pic_2 = np.concatenate((batch_pic_2, x2))
                
#        update_progress(float((pic_idx-start_idx+1)/ batchsize) )
            
    batch_pic_3 = select_contrast(batch_pic_1, batch_pic_2)
    fid.close()
    
    return batch_pic_1, batch_pic_2, batch_pic_3
        
def test():
    pairfile = os.path.join(BASE_PATH, "pairs.txt")
    b1, b2, b3 = get_img_batch(pairfile, batchsize=10)
    print b1.shape, b2.shape, b3.shape
    print b1[0]

def main():
    test()
    print "finist"
    return

def update_progress(progress):
    barLength = 30 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), int(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
        