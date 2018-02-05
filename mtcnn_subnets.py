import tensorflow as tf
import numpy as np

slim = tf.contrib.slim

def PNET(_input):
    net = slim.conv2d(_input, 10, [3,3],padding='VALID', scope='conv1')
    net = slim.max_pool2d(net, [2,2], scope='pool')
    net = slim.conv2d(net, 16, [3,3], padding='VALID', scope='conv2')
    net = slim.conv2d(net, 32, [3,3], padding='VALID', scope='conv3')
    net = slim.conv2d(net, 2, [1,1], padding='VALID', scope='conv4-1')
    net1 = softmax(net, 3)
    net2 = slim.conv2d(net, 4, [1,1], scope='conv4-2')
    return net1, net2


def RNET(_input):
    net = slim.conv2d(_input, 28, [3,3], padding='VALID', scope='conv1')
    net = slim.max_pool2d(net, [3,3], stride=[2,2], scope='pool1')
    net = slim.conv2d(net, 48, [3,3], padding='VALID', scope='conv2')
    net = slim.conv2d

def softmax(self, target, axis, name=None):
    max_axis = tf.reduce_max(target, axis, keep_dims=True)
    target_exp = tf.exp(target-max_axis)
    normalize = tf.reduce_sum(target_exp, axis, keep_dims=True)
    softmax = tf.div(target_exp, normalize, name)
    return softmax



'''
conv(3, 3, 28, 1, 1, padding='VALID', relu=False, name='conv1')
             .prelu(name='prelu1')
             .max_pool(3, 3, 2, 2, name='pool1')
             .conv(3, 3, 48, 1, 1, padding='VALID', relu=False, name='conv2')
             .prelu(name='prelu2')
             .max_pool(3, 3, 2, 2, padding='VALID', name='pool2')
             .conv(2, 2, 64, 1, 1, padding='VALID', relu=False, name='conv3')
             .prelu(name='prelu3')
             .fc(128, relu=False, name='conv4')
             .prelu(name='prelu4')
             .fc(2, relu=False, name='conv5-1')
             .softmax(1,name='prob1'))
'''