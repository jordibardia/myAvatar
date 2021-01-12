import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame_gui

from global_vals import *

from objloader import OBJ

def view_obj(filename, display_surf):
    #pygame.init()
    #pygame.display.set_caption('Your Model')
    viewport = (800,600)
    hx = viewport[0]/2
    hy = viewport[1]/2
    display_surf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

    model_view = pygame_gui.UIManager((800,600))

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,0), (250,90)), text="Back", manager=model_view)

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
    hat = OBJ('hats/new_leather_hat.OBJ', swapyz="True")
    #output = OBJ(sys.argv[1], swapyz="True")
    output = OBJ(filename, swapyz = "True")

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
    #rx_1, ry_1, rz_1 = (0,-90,0) #For santa hat
    rx_1, ry_1, rz_1 = (0,-90,180)
    tx, ty = (0,0)
    #tx_1, ty_1, tz_1 = (0,-76,96) #For santa hat
    tx_1, ty_1, tz_1 = (0, 50, 130)
    zpos = 265
    rotate = move = False
    is_running = True
    while is_running:
        #clock.tick(30)
        time_delta = clock.tick(60)/1000.0

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
            elif e.type == pygame.USEREVENT:
                if e.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if e.ui_element == back_button:
                        is_running = False
            elif e.type == KEYDOWN:
                if e.key == K_1:
                    displayHat = not displayHat
                if e.key == K_ESCAPE:
                    is_running = False
            #elif e.type == KEYDOWN and e.key == K_ESCAPE:
                #pygame.quit()
            #    is_running = False
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
                    rx += i
                    rx -= i
            #model_view.update(time_delta)

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

        glTranslate(tx/20, ty/20, -zpos)
        glRotate(ry_1, 1, 0, 0)
        glRotate(rx_1, 0, 1, 0)
        glRotate(rz_1, 0, 0, 1)
        glTranslate(0,ty_1,tz_1)

        #glTranslate(tx_1, ty_1, tz_1)

        glMultMatrixf(model_2)
        model_2 = glGetDoublev(GL_MODELVIEW_MATRIX)
        #if not displayHat:
        glCallList(hat.gl_list)
        glPopMatrix()

        #model_view.process_events(e)
        #model_view.update(time_delta)
        #model_view.draw_ui(display_surf)

        pygame.display.flip()

    display_surf = pygame.display.set_mode((640,480))

if len(sys.argv) != 0:
    pygame.init()
    pygame.display.set_caption('myAvatar')

    view_obj(sys.argv[1], None)
