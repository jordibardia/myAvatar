import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

#from objloader import OBJ
from opengl_loaders.fasterobj import OBJ_vbo
import imgui
from opengl_loaders.custom_renderer import CustomRenderer


def view_obj(filename, display_surf):
    #pygame.init()
    #pygame.display.set_caption('Your Model')
    viewport = (800,600)
    hx = viewport[0]/2
    hy = viewport[1]/2
    display_surf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
    imgui.create_context() #Does not work with pygame 2.0+
    impl = CustomRenderer()

    io = imgui.get_io()
    io.display_size = viewport

    #Toggle visibility of hat
    #displayHat = False

    #Toggle which hat to display (0 = None, 1 = Leather Hat, 2 = Santa Hat)
    current = 0

    glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

    # LOAD OBJECT AFTER PYGAME INIT
    hats = [
        OBJ_vbo('hats/new_leather_hat.OBJ'), #Leather Hat
        OBJ_vbo('hats/bigger_santahat.OBJ')  #Santa Hat
    ]
    hat_vals = [
        [[0,0,0], [0,0,0]],
        [[0,-90,0], [0,-76,96]], #(rx, ry, rz), (tx, ty, tz)
        [[-175,88, 0], [0, 50, 130]]
    ]
    #hat = OBJ_vbo('hats/new_leather_hat.OBJ')
    output = OBJ_vbo(filename)

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

    #Head model rotational and translational values
    rx, ry, rz = (-175,88, 0) #Values found through trial and error
    tx, ty = (0,0)
    
    #Current hat rotational and translational values
    rx_h, ry_h, rz_h = (0,0,0)
    tx_h, ty_h, tz_h = (0,0,0)

    zpos = 265
    rotate = move = False
    is_running = True
    while is_running:
        time_delta = clock.tick(60)/1000.0

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    is_running = False
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
                if not imgui.core.is_any_item_active():
                    if rotate:
                        if rz + i <= 60 and rz + i >= -60:
                            rz += i
                            for k in range(1, len(hat_vals)):
                                #rz_h += i
                                hat_vals[k][0][2] += i
                    if move:
                        tx += i
                        ty -= j
                        rx += i
                        rx -= i
            if e.type != 16: #If not video resize event
                impl.process_event(e)

        imgui.new_frame()	
        imgui.begin("Options", True, flags=imgui.WINDOW_NO_RESIZE)
        imgui.set_window_size(200,200)
        clicked, current = imgui.listbox("Hats", current, ["None", "Leather Hat", "Santa Hat"])
        rx_h, ry_h, rz_h = hat_vals[current][0]
        tx_h, ty_h, tz_h = hat_vals[current][1]
        imgui.end()

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

        output.render()

        glPopMatrix()

        glPushMatrix()
        glLoadIdentity()

        model_2 = glGetDoublev(GL_MODELVIEW_MATRIX)

        glTranslate(tx/20, ty/20, -zpos)
        glRotate(ry_h, 1, 0, 0)
        glRotate(rx_h, 0, 1, 0)
        glRotate(rz_h, 0, 0, 1)
        glTranslate(0,ty_h,tz_h)
        #glRotate(hat_vals[current][0][1], 1, 0, 0)
        #glRotate(hat_vals[current][0][0], 0, 1, 0)
        #glRotate(hat_vals[current][0][2], 0, 0, 1)
        #glTranslate(0,hat_vals[current][1][1],hat_vals[current][1][2])

        glMultMatrixf(model_2)
        model_2 = glGetDoublev(GL_MODELVIEW_MATRIX)

        if current != 0:
            hats[current - 1].render()
        glPopMatrix()

        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()

    display_surf = pygame.display.set_mode((640,480))


if __name__ == '__main__':
    if len(sys.argv) != 0:
        pygame.init()
        pygame.display.set_caption('myAvatar')

        view_obj(sys.argv[1], None)
