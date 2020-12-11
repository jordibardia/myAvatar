import tensorflow as tf
import numpy as np
from cv2 import cv2
import glob
import math
import random
import os
import sys

from posmap_defs import make_posmaps
from model_defs import resfcn256


def train(mode = 'HiPerGator', epochs = 10, loss_type = 'MSE'): #Mode: whether model is training on my computer or HiPerGator
    
    #test_amount = 32
    
    # Generating Position Maps
    #imgCount = len(glob.glob1('/blue/cis6930/jbardia/data_input', '*.jpg'))
    imgCount = None
    img_paths = None
    posmap_paths = None
    if mode == 'my_computer':
        #files = glob.glob('posmap_output/*') #Clearing for new generation
        #for f in files:
        #    os.remove(f)
        #imgCount = len(glob.glob1('AFLW2000', '*.jpg'))
        #make_posmaps(imgCount)
        imgCount = len(glob.glob1('data_input', '*.jpg'))
        img_paths = glob.glob('data_input/*.jpg')
        posmap_paths = glob.glob('data_input/*.npy')
    elif mode == 'HiPerGator':
        imgCount = len(glob.glob1('/blue/cis6930/jbardia/data_input', '*.jpg'))
        img_paths = glob.glob('/blue/cis6930/jbardia/data_input/*.jpg')
        posmap_paths = glob.glob('/blue/cis6930/jbardia/data_input/*.npy')
    else:
        raise ValueError("Error: Unknown Mode!")

    #test_inds = random.sample(range(0,imgCount), test_amount) #Images to test with
    #test_inds = dict.fromkeys(test_inds, True)
    #print(test_inds)

    #img_paths = glob.glob('/blue/cis6930/jbardia/data_input/*.jpg')
    #posmap_paths = glob.glob('/blue/cis6930/jbardia/data_input/*.npy')
    img_paths.sort()
    posmap_paths.sort()
    paths_comb = []
    
    for i in range(len(img_paths)):
        temp = [img_paths[i], posmap_paths[i]]
        paths_comb.append(temp)
    random.shuffle(paths_comb)
    #print(paths_comb)

    # Loading weights for loss calculation
    face_mask = cv2.imread('masks/uv_face_mask.png', cv2.IMREAD_GRAYSCALE)
    weight_mask = cv2.imread("masks/uv_weight_mask.png", cv2.IMREAD_GRAYSCALE)
    face_mask = np.array(face_mask).astype('float32')
    weight_mask = np.array(weight_mask).astype('float32')
    face_mask = face_mask / 255.0
    weight_mask = weight_mask / 16.0
    mask_comb = face_mask*weight_mask
    temp = np.arange(256*256*3)
    temp = temp.reshape(1,256,256,3).astype('float32')
    temp[0,:,:,0] = mask_comb
    temp[0,:,:,1] = mask_comb
    temp[0,:,:,2] = mask_comb

    # Training definitions
    model = resfcn256()
    truth = tf.placeholder(tf.float32, shape=[None, 256, 256, 3])
    inp = tf.placeholder(tf.float32, shape=[None, 256, 256, 3])
    out = model(inp, is_training=True)
    batch_size = 16
    #learning_rate = 0.0001
    #epochs = 50
    
    loss = None
    
    if loss_type == 'norm':
        loss = tf.reduce_sum(tf.norm(out - truth)*temp)
    elif loss_type == 'MSE':
        loss = tf.losses.mean_squared_error(truth, out, weights=temp)
    elif loss_type == 'mean_square':
        loss = tf.reduce_mean(tf.square(out-truth))
    train_loss_results = []
    
    global_step = tf.Variable(0, name='global_step', trainable=False)
    learning_rate = tf.train.exponential_decay(0.0001, global_step, 45000, 0.5, staircase=True)

    op_update = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies(op_update):
        train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss,global_step=global_step)

    session = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))
    session.run(tf.global_variables_initializer())
    session.run(global_step.initializer)

    saver = tf.train.Saver(var_list = tf.global_variables())
    save_path = 'saved_models/'
    
    print('Using ' + loss_type + ' loss for ' + str(epochs) + ' epochs')

    for i in range(epochs):
        random.shuffle(paths_comb)
        curr_batch = 0
        for j in range(math.floor(imgCount/batch_size)):
            batch = prepareBatch(paths_comb, batch_size, curr_batch, imgCount)
            curr_batch += 1
            if batch != None:
                loss_batch = session.run(loss, feed_dict={inp:batch[0], truth:batch[1]})
                train_loss_results.append(loss_batch)
                session.run(train_step, feed_dict={inp:batch[0], truth:batch[1]})
                print("Batch " + str(j) + " Loss: " + str(loss_batch))
        print("## EPOCH " + str(i) + " LOSS: " + str(sum(train_loss_results)/len(train_loss_results)) + " ##")
        train_loss_results.clear()
    
    saver.save(session, save_path + loss_type + '_model_' + str(epochs) + '_300W')
    #return test_inds, img_paths, posmap_paths


def prepareBatch(paths_comb,batch_size,curr_batch,imgCount):
    if (curr_batch + 1)*batch_size < imgCount:
        img_arr = []
        posmap_arr = []
        for i in range(curr_batch*batch_size, (curr_batch+1)*batch_size):
            img = cv2.imread(paths_comb[i][0])
            posmap = np.load(paths_comb[i][1])
            
            img_temp = np.array(img, dtype = np.float32)
            posmap_temp = np.array(posmap, dtype=np.float32)
    
            
            #batch.append([img/(256.0*1.1),posmap/(256.0*1.1)])
            img_arr.append(img_temp/256.0)
            posmap_arr.append(posmap_temp/(256.0*1.1))
        
        batch = [img_arr, posmap_arr]
        
        return batch

    
    return None

def main():
    if len(sys.argv) == 1:
        train()
    elif len(sys.argv) == 2:
        mode = sys.argv[1]
        train(mode = mode)

if __name__ == '__main__':
    main()