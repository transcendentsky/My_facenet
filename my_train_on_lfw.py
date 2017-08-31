#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 13:38:38 2017

@author: trans
"""

from __future__ import absolute_import
from __future__ import division

import tensorflow as tf
import numpy as np
import os, sys
import keras
import argparse
from keras.applications.mobilenet import _depthwise_conv_block, _conv_block
from keras.layers import Flatten, GlobalAveragePooling2D, Dense

def main(args):
    img_1 = tf.placeholder(shape=(224,224,3), name="img_1")
    img_2 = tf.placeholder(shape=(224,224,3), name="img_3")
    img_3 = tf.placeholder(shape=(224,224,3), name="img_3")
    
    triplet = tf.placeholder(shape=(3,224,224,3), name="triplet")
    
    sess = tf.Session()
#    s = sess.run(embeddings, feed_dict=feed_dict)
    
    
    prelogits = My_MobileNet(triplet)
    
    embeddings = tf.nn.l2_normalize(prelogits, 1 , epsilon=1e-10, name="embeddings")
    
    anchor, positive , negative = tf.unstack(tf.reshape(embeddings,([-1,3,args.embedding_size])), 3, 1)
    
    total_loss = cal_total_loss(triplet_loss(anchor, positive, negative, args.alpha))
    
    with tf.name_scope('SGD'):
    # Gradient Descent
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(total_loss)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)


def My_MobileNet(triplet, alpha=1.0, depth_multiplier=1):
    img_input = triplet
    x = _conv_block(img_input, 32, alpha, strides=(2, 2))
    x = _depthwise_conv_block(x, 64, alpha, depth_multiplier, block_id=1)

    x = _depthwise_conv_block(x, 128, alpha, depth_multiplier,
                              strides=(2, 2), block_id=2)
    x = _depthwise_conv_block(x, 128, alpha, depth_multiplier, block_id=3)

    x = _depthwise_conv_block(x, 256, alpha, depth_multiplier,
                              strides=(2, 2), block_id=4)
    x = _depthwise_conv_block(x, 256, alpha, depth_multiplier, block_id=5)

    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier,
                              strides=(2, 2), block_id=6)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=7)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=8)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=9)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=10)
    x = _depthwise_conv_block(x, 512, alpha, depth_multiplier, block_id=11)

    x = _depthwise_conv_block(x, 1024, alpha, depth_multiplier,
                              strides=(2, 2), block_id=12)
    x = _depthwise_conv_block(x, 1024, alpha, depth_multiplier, block_id=13)
    
    x = GlobalAveragePooling2D()(x)
    x = Flatten()(x)
    x = Dense(128)(x)
    
    return x

def parse_arguments(argv):
    paser = argparse.ArgumentParser()
    paser.add_argument('--learning_rate', type=float, 
                       help='wocao zhenidoubuzhidao', default=0.5)
    paser.add_argument('--epochs', type=int, 
                       help='', default=500)
    paser.add_argument('--embedding_size', type=int ,
                       help='embedding size , the final size', default=128)
    paser.add_argument('--alpha', type=float,
                       default=0.2)
    
    return paser.parse_args(argv)

def triplet_loss(anchor, positive, negative, alpha):
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), 1)
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), 1)
        
    basic_loss = tf.add(tf.subtract(pos_dist,neg_dist), alpha)
    loss = tf.reduce_mean(tf.maximum(basic_loss, 0.0), 0)  #tf.maximum return the max of the two value
    
    return loss
def cal_total_loss(loss):
    regularization_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
    total_loss = tf.add_n([triplet_loss] + regularization_losses, name='total_loss')
    
    return total_loss

if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))