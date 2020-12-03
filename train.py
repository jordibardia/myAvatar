import tensorflow as tf
import numpy as np
from cv2 import cv2
import glob
import math
import random
import os

from posmap_defs import make_posmaps
from model_defs import resfcn256


def train(mode = 'my_computer'): #Mode: whether model is training on my computer or HiPerGator
    # Generating Position Maps
    imgCount = len(glob.glob1('AFLW2000', '*.jpg'))
    if mode == 'my_computer':
        files = glob.glob('posmap_output/*') #Clearing for new generation
        for f in files:
            os.remove(f)
        #imgCount = len(glob.glob1('AFLW2000', '*.jpg'))
        make_posmaps(imgCount)
    elif mode == 'HiPerGator':
        imgCount = len(glob.glob1('posmap_output', 'image?????.jpg'))
    else:
        raise ValueError("Error: Unknown Mode!")

    test_inds = random.sample(range(0,imgCount), 10) #Images to test with
    test_inds = dict.fromkeys(test_inds, True)

    img_paths = glob.glob('posmap_output/image?????.jpg')
    posmap_paths = glob.glob('posmap_output/image?????.npy')
    paths_comb = []
    for i in range(len(img_paths)):
        if i not in test_inds:
            temp = [img_paths[i], posmap_paths[i]]
            paths_comb.append(temp)
    random.shuffle(paths_comb)

    # Loading weights for loss calculation
    face_mask = cv2.imread('masks/uv_face_mask.png', cv2.IMREAD_GRAYSCALE)
    weight_mask = cv2.imread("masks/uv_weight_mask.png", cv2.IMREAD_GRAYSCALE)
    face_mask = np.array(face_mask).astype(np.float)
    weight_mask = np.array(weight_mask).astype(np.float)
    face_mask = face_mask / 256.0
    weight_mask = weight_mask / 256.0
    mask_comb = face_mask*weight_mask #Set for (256,256,3)
    temp = np.arange(256*256*3)
    temp = temp.reshape(1,256,256,3).astype(np.float)
    temp[0,:,:,0] = mask_comb
    temp[0,:,:,1] = mask_comb
    temp[0,:,:,2] = mask_comb

    # Training definitions
    model = resfcn256()
    batch_size = 16
    #learning_rate = 0.0001
    global_step = tf.Variable(0, name='global_step', trainable=False)
    learning_rate = tf.train.exponential_decay(0.0001, global_step, 40000, 0.5, staircase=True)
    epochs = 20

    truth = tf.placeholder(tf.float32, shape=[None, 256, 256, 3])
    inp = tf.placeholder(tf.float32, shape=[None, 256, 256, 3])
    out = model(inp, is_training=True)

    loss = tf.losses.mean_squared_error(truth, out, weights=temp)
    #loss = tf.reduce_sum(tf.norm(out - truth)*temp)
    #loss = tf.losses.mean_squared_error(truth, out)
    train_loss_results = []

    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies(update_ops):
        train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss,global_step=global_step)

    session = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))
    session.run(tf.global_variables_initializer())
    session.run(global_step.initializer)

    saver = tf.train.Saver(var_list = tf.global_variables())
    save_path = 'saved_models/'
    curr_batch = 0

    for i in range(epochs):
        random.shuffle(paths_comb)
        curr_batch = 0
        for j in range(math.floor(imgCount/batch_size)):
            batch = prepareBatch(paths_comb, batch_size, curr_batch, imgCount)
            if batch != None:
                loss_batch = session.run(loss, feed_dict={inp:batch[0], truth:batch[1]})
                train_loss_results.append(loss_batch)
                session.run(train_step, feed_dict={inp:batch[0], truth:batch[1]})
                print("Batch " + str(j) + " Loss: " + str(loss_batch))
    
    saver.save(session, save_path + 'final.model')
    return test_inds, img_paths, posmap_paths


def prepareBatch(paths_comb,batch_size,curr_batch,imgCount):
    if (curr_batch + 1)*batch_size < imgCount:
        img_arr = []
        posmap_arr = []
        for i in range(curr_batch*batch_size, (curr_batch+1)*batch_size):
            img = cv2.imread(paths_comb[i][0])
            posmap = np.load(paths_comb[i][1])
            #batch.append([img/(256.0*1.1),posmap/(256.0*1.1)])
            img_arr.append(img/(256*1.1))
            posmap_arr.append(posmap/(256*1.1))
        
        batch = [img_arr, posmap_arr]
        
        return batch

    
    return None




