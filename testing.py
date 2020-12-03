from train import train
import tensorflow as tf
from cv2 import cv2
from model_defs import resfcn256

network = resfcn256()

test_inds, img_paths, posmap_paths = train()
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



