import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

from objloader import OBJ

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

displayHat = True

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
#output = OBJ('model_output/image00894_tex.OBJ', swapyz="True")
hat = OBJ('hats/bigger_santahat.OBJ', swapyz="True")
output = OBJ(sys.argv[1], swapyz="True")
#output = OBJ('clowp.OBJ', swapyz="True")

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 500.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

model_1 = glGetDoublev(GL_MODELVIEW_MATRIX)
model_2 = model_1

rx, ry, rz = (-175,88, 0) #Values found through trial and error
rx_1, ry_1, rz_1 = (0,-90,0)
#rx, ry, rz = (0,0,0)
#rx_1, ry_1, rz_1 = (0,0,0)
tx, ty = (0,0)
tx_1, ty_1, tz_1 = (0,-76,96)
zpos = 265
rotate = move = False
while 1:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN:
            if e.key == K_1:
                displayHat = not displayHat
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                if rz + i <= 60 and rz + i >= -60:
                    rz += i
                    rz_1 += i
            if move:
                tx += i
                ty -= j 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    model_1 = glGetDoublev(GL_MODELVIEW_MATRIX)

    # RENDER OBJECT
    glTranslate(tx/20, ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glRotate(rz, 0, 0, 1)
    #glScalef(0.1,0.1,0.1)

    glMultMatrixf(model_1)
    model_1 = glGetDoublev(GL_MODELVIEW_MATRIX)

    glCallList(output.gl_list)

    glPopMatrix()

    glPushMatrix()
    glLoadIdentity()

    model_2 = glGetDoublev(GL_MODELVIEW_MATRIX)
    #model_2 = temp

    glTranslate(0, 0, -zpos)
    glRotate(ry_1, 1, 0, 0)
    glRotate(rx_1, 0, 1, 0)
    glRotate(rz_1, 0, 0, 1)
    glTranslate(0,ty_1,tz_1)

    #glTranslate(tx_1, ty_1, tz_1)

    glMultMatrixf(model_2)
    model_2 = glGetDoublev(GL_MODELVIEW_MATRIX)
    if not displayHat:
        glCallList(hat.gl_list)
    glPopMatrix()

    pygame.display.flip()