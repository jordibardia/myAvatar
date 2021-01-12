from train import train
import tensorflow as tf
from cv2 import cv2
from model_defs import resfcn256
import sys
from output_io import *
import numpy as np
import glob
import random
import re

def testing(test_inds, folder = 'posmap_output', model = 'saved_models/MSE_model_10_300W', generate_models = False):
    mode = 'my_computer'
    if len(sys.argv) > 1 and sys.argv[1] == 'HiPerGator':
        mode = sys.argv[1]

    network = resfcn256()

    #Loading mask for loss calculation
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

    files = glob.glob('model_output/*') #Clearing for new generation
    for f in files:
        os.remove(f)

    #test_inds, img_paths, posmap_paths = train(mode)
    img_paths = glob.glob(folder + '/image?????.jpg')
    posmap_paths = glob.glob(folder + '/image?????.npy')
    #img_paths = glob.glob('data_input/*.jpg')
    #test_inds = random.sample(range(0,len(img_paths)), num_samples)
    #test_inds = dict.fromkeys(test_inds, True)


    inp = tf.placeholder(tf.float32, shape=[None,256,256,3])
    out = network(inp, is_training=False)
    ground_truth = tf.placeholder(tf.float32, shape=[None,256,256,3])
    sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))


    #tf.train.Saver(network.vars).restore(sess, 'saved_models/256_256_resfcn256_weight')
    tf.train.Saver(network.vars).restore(sess, model)

    test_imgs = np.arange(len(test_inds.keys())*256*256*3)
    test_imgs = test_imgs.reshape(len(test_inds.keys()), 256, 256, 3).astype('float32')
    test_posmaps = np.arange(len(test_inds.keys())*256*256*3)
    test_posmaps = test_posmaps.reshape(len(test_inds.keys()), 256, 256, 3).astype('float32')
    test_imgs_filenames = []

    ind = 0

    for key in test_inds:
        filenames = img_paths[key].replace('\\','/')
        filenames_2 = filenames.split('/')
        filenames_3 = filenames_2[1].split('.')
        test_imgs_filenames.append(filenames_3[0])
        temp_img = cv2.imread(img_paths[key])
        temp_img = cv2.cvtColor(temp_img,cv2.COLOR_BGR2RGB)

        temp_posmap = np.load(posmap_paths[key])/(256.0*1.1)
        #test_imgs.append(temp_img/256.0)
        #test_posmaps.append((np.load(posmap_paths[key]))/(256.0*1.1))
        test_imgs[ind] = (temp_img/256.0)
        test_posmaps[ind] = temp_posmap
        ind += 1
    

    posmaps_pred = sess.run(out, feed_dict = {inp: test_imgs})
    posmaps_pred_loss = np.array(posmaps_pred)
    #loss = tf.reduce_mean(tf.square(posmaps_pred - test_posmaps)*temp)
    loss = np.mean(np.square(posmaps_pred_loss - test_posmaps)*temp)
    #loss = tf.metrics.mean_squared_error(new1, new2, weights=temp, name = 'MSE')
    posmaps_pred = posmaps_pred * (256.0*1.1)
    print("Loss: " + str(loss))


    triangles = np.loadtxt('indices/triangles.txt').astype(np.int32)
    uv_coords = generate_uv_coords()


    if model != 'saved_models/256_256_resfcn256_weight' and generate_models == True:
        for i in range(len(posmaps_pred)):
            texture = cv2.remap(test_imgs[i], posmaps_pred[i][:,:,:2].astype(np.float32), None, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,borderValue=(0))
            kpt = get_landmarks(posmaps_pred[i])
            vertices = get_vertices(posmaps_pred[i])
            new_vertices = frontalize(vertices)
            new_vertices[:,1] = 255 - new_vertices[:,1]

            path_texture = 'model_output/' + test_imgs_filenames[i] + '_tex.obj'
            write_obj_with_texture(path_texture, new_vertices, triangles, texture, uv_coords/256.0)

def main():
    folder = None
    img_paths = None
    test_inds = None
    if len(sys.argv) == 3 and sys.argv[2] == 'samples':
        folder = 'samples'
        img_paths = glob.glob(folder + '/image?????.jpg')
        test_inds = range(0, len(img_paths))
    elif len(sys.argv) == 2:
        folder = 'posmap_output'
        img_paths = glob.glob(folder + '/image?????.jpg')
        test_inds = random.sample(range(0,len(img_paths)), 100)

    
    test_inds = dict.fromkeys(test_inds, True)
    save_model_path = 'saved_models/'
    testing(test_inds = test_inds, folder = folder, model = save_model_path + str(sys.argv[1]), generate_models = True)

if __name__ == '__main__':
    main()






