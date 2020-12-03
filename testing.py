from train import train
import tensorflow as tf
from cv2 import cv2
from model_defs import resfcn256
import sys
from output_io import *
import numpy as np

mode = 'my_computer'
if len(sys.argv) > 1 and sys.argv[1] == 'HiPerGator':
    mode = sys.argv[1]

network = resfcn256()

test_inds, img_paths, posmap_paths = train(mode)
inp = tf.placeholder(tf.float32, shape=[None,256,256,3])
out = network(inp, is_training=False)
sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))

tf.train.Saver(network.vars).restore(sess, 'saved_models/final.model')

test_imgs = []
#test_posmaps = []

for key in test_inds:
    test_imgs.append((cv2.imread(img_paths[key]))/(256.0*1.1))
    #test_posmaps.append((np.load(posmap_paths[key]))/(256.0*1.1))

posmaps_pred = sess.run(out, feed_dict = {inp: test_imgs})
posmaps_pred = posmaps_pred * (256.0*1.1)

triangles = np.loadtxt('indices/triangles.txt').astype(np.int32)

for i in range(len(posmaps_pred)):
    kpt = get_landmarks(posmaps_pred[i])
    vertices = get_vertices(posmaps_pred[i])
    colors = get_colors(test_imgs[i], vertices)
    path = 'model_output/head_' + str(i) + '.obj'
    write_obj_with_colors(path, vertices, triangles, colors)






