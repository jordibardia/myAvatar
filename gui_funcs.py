import tensorflow as tf
from cv2 import cv2
from model_defs import resfcn256
import numpy as np
from output_io import *
import glob
import sys
#import dlib

#face_detector = dlib.cnn_face_detection_model_v1('saved_models/mmod_human_face_detector.dat')

# Functions to be used by the GUI

#For predicting the position map of an image
def generatePositionMap(image, model = 'saved_models/256_256_resfcn256_weight'):
    network = resfcn256()
    image_norm = image / 256.0 #Does not assume image is normalized beforehand
    inp = tf.placeholder(tf.float32, shape=[None,256,256,3])
    out = network(inp, is_training=False)

    sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))
    tf.train.Saver(network.vars).restore(sess, model)

    posmap_pred = sess.run(out, feed_dict = {inp: [image_norm]})
    posmap_pred = np.squeeze(posmap_pred)
    posmap_pred = posmap_pred * (256.0*1.1)

    return posmap_pred

#For generating the 3D model
def generateModel(imagePath, model = 'saved_models/256_256_resfcn256_weight'):
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    posmap_pred = generatePositionMap(image, model)

    triangles = np.loadtxt('indices/triangles.txt').astype(np.int32)
    uv_coords = generate_uv_coords()

    texture = cv2.remap(image, posmap_pred[:,:,:2].astype(np.float32), None, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,borderValue=(0))
    kpt = get_landmarks(posmap_pred)
    vertices = get_vertices(posmap_pred)
    new_vertices = frontalize(vertices)
    new_vertices[:,1] = 255 - new_vertices[:,1]
    colors = get_colors(image, vertices)
    path_texture = 'gui_models/' + str(len(glob.glob('gui_models/*.obj')) + 1) + '_tex.obj'
    write_obj_with_texture(path_texture, new_vertices, triangles, texture, uv_coords/256.0)
    return path_texture


#Gets texture for model (Used only for report)
def getTexture(imagePath):
    #posmap_pred = generatePositionMap(image, model)
    img = cv2.imread(imagePath)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    posmap_path = imagePath.replace('jpg', 'npy')
    posmap = np.load(posmap_path)
    texture = cv2.remap(img, posmap[:,:,:2].astype(np.float32), None, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,borderValue=(0))
    texture_path = 'temp.png'
    cv2.imwrite(texture_path, texture)
    return texture

#Cropping image to 256x256 image
def cropImage(imagePath = 'userphoto/userinput.jpg'):
    img = cv2.imread(imagePath)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cropped_img = img[112:368, 192:448]
    cv2.imwrite('userphoto/userinput_cropped.jpg', cropped_img)


#For testing functions
def main():
    if len(sys.argv) != 0:
        generateModel(sys.argv[1])

if __name__ == '__main__':
    main()


