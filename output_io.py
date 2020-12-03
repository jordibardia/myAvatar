## CODE BY YAO FENG ##
import numpy as np

uv_kpt_ind = np.loadtxt('indices/uv_kpt_ind.txt').astype(np.int32)
face_ind = np.loadtxt('indices/face_ind.txt').astype(np.int32)
#triangles = np.loadtxt('indices/triangles.txt').astype(np.int32)

def get_landmarks(pos):
    '''
    Args:
        pos: the 3D position map. shape = (256, 256, 3).
    Returns:
        kpt: 68 3D landmarks. shape = (68, 3).
    '''
    kpt = pos[uv_kpt_ind[1,:], uv_kpt_ind[0,:], :]
    return kpt

def get_vertices(pos):
    '''
    Args:
        pos: the 3D position map. shape = (256, 256, 3).
    Returns:
        vertices: the vertices(point cloud). shape = (num of points, 3). n is about 40K here.
    '''
    all_vertices = np.reshape(pos, [256**2, -1])
    vertices = all_vertices[face_ind, :]
    return vertices

def get_colors(image, vertices):
    '''
    Args:
        pos: the 3D position map. shape = (256, 256, 3).
    Returns:
        colors: the corresponding colors of vertices. shape = (num of points, 3). n is 45128 here.
    '''
    [h, w, _] = image.shape
    vertices[:,0] = np.minimum(np.maximum(vertices[:,0], 0), w - 1)  # x
    vertices[:,1] = np.minimum(np.maximum(vertices[:,1], 0), h - 1)  # y
    ind = np.round(vertices).astype(np.int32)
    colors = image[ind[:,1], ind[:,0], :] # n x 3
    return colors

def write_obj_with_colors(obj_name, vertices, triangles, colors):
    ''' Save 3D face model with texture represented by colors.
    Args:
        obj_name: str
        vertices: shape = (nver, 3)
        colors: shape = (nver, 3)
        triangles: shape = (ntri, 3)
    '''
    triangles = triangles.copy()
    triangles += 1 # meshlab start with 1
    
    if obj_name.split('.')[-1] != 'obj':
        obj_name = obj_name + '.obj'
        
    # write obj
    with open(obj_name, 'w') as f:
        
        # write vertices & colors
        for i in range(vertices.shape[0]):
            # s = 'v {} {} {} \n'.format(vertices[0,i], vertices[1,i], vertices[2,i])
            s = 'v {} {} {} {} {} {}\n'.format(vertices[i, 0], vertices[i, 1], vertices[i, 2], colors[i, 0], colors[i, 1], colors[i, 2])
            f.write(s)

        # write f: ver ind/ uv ind
        [k, ntri] = triangles.shape
        for i in range(triangles.shape[0]):
            # s = 'f {} {} {}\n'.format(triangles[i, 0], triangles[i, 1], triangles[i, 2])
            s = 'f {} {} {}\n'.format(triangles[i, 2], triangles[i, 1], triangles[i, 0])
            f.write(s)
####