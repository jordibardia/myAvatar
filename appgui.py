import pygame
import pygame.camera
import pygame_gui
from viewobj import view_obj
from gui_funcs import generateModel, cropImage

def main():
    pygame.init()

    pygame.camera.init()
    cam_list = pygame.camera.list_cameras()
    cam = None
    if cam_list:
        cam = pygame.camera.Camera(cam_list[0], (640, 480))
        cam.start()

    display_surf = pygame.display.set_mode((640,480))
    pygame.display.set_caption("Avatar Creator")

    consolas_font = pygame.font.SysFont('Consolas', 20)
    #test_font = pygame.font.Font(pygame.font.get_default_font(), 30)


    #Initializing UI Managers for each state in the application
    main_menu = pygame_gui.UIManager((640,480))
    take_picture = pygame_gui.UIManager((640,540))
    view_prev_models = pygame_gui.UIManager((640,480))

    #Initializing UI Elements for each UI Manager
    picture_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((195,150), (250,60)), text="Take Picture", manager=main_menu)
    previous_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((195,210), (250,60)), text="View Previous Models", manager=main_menu)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((195,270), (250,60)), text="Exit", manager=main_menu)

    takepicture_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,480), (213,60)), text="Take Picture", manager=take_picture)
    rendermodel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((213,480), (213,60)), text="Render Model", manager=take_picture)
    picture_back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((426,480), (213,60)), text="Back", manager=take_picture)

    rendermodel_button.disable()

    pic_text = consolas_font.render("Position face within green box.", True, (255,255,255))
    text_rect = pic_text.get_rect()
    text_rect.center = (315,380)

    obj_loading = None
    file_dialog = None

    mode = "main_menu"

    clock = pygame.time.Clock()

    is_running = True
    error_loading = False

    #take_picture variables
    picture_taken = False
    currPicture = None

    while is_running:
        time_delta = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #main_menu
                    if event.ui_element == picture_button:
                        mode = "take_picture"
                        display_surf = pygame.display.set_mode((640,540))
                    if event.ui_element == previous_button:
                        mode = "view_prev_models"
                        file_dialog = pygame_gui.windows.UIFileDialog(pygame.Rect((60,60), (520, 300)), view_prev_models, window_title="Select a .OBJ...", initial_file_path='model_output', allow_existing_files_only=True)
                    if event.ui_element == exit_button:
                        is_running = False
                    #take_picture
                    if event.ui_element == takepicture_button:
                        picture_taken = not picture_taken
                        if picture_taken:
                            takepicture_button.set_text("Retake Picture")
                            rendermodel_button.enable()
                        else:
                            takepicture_button.set_text("Take Picture")
                            rendermodel_button.disable()
                    if event.ui_element == rendermodel_button:
                        pygame.image.save(currPicture, 'userphoto/userinput.jpg')
                        cropImage()
                        obj_path = generateModel('userphoto/userinput_cropped.jpg')
                        view_obj(obj_path, display_surf)
                    if event.ui_element == picture_back_button:
                        mode = "main_menu"
                        picture_taken = False
                        currPicture = None
                        rendermodel_button.disable()
                        takepicture_button.set_text("Take Picture")
                        display_surf = pygame.display.set_mode((640,480))

                if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                    if event.ui_element == file_dialog:
                        if not error_loading:
                            mode = "main_menu"
                        file_dialog.kill()
                    if event.ui_element == obj_loading:
                        if error_loading:
                            file_dialog.kill()
                            file_dialog = pygame_gui.windows.UIFileDialog(pygame.Rect((60,60), (520, 300)), view_prev_models, window_title="Select a .OBJ...", initial_file_path='gui_models', allow_existing_files_only=True)
                            error_loading = False
                        obj_loading.kill()
                if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                    if event.ui_element == file_dialog:
                        tmp = event.text.split('.')
                        if tmp[len(tmp) - 1] != 'obj':
                            obj_loading = pygame_gui.windows.UIMessageWindow(pygame.Rect((60,60), (520, 170)), "Error! Selected file is not a .obj!", view_prev_models)
                            error_loading = True
                        else:
                            file_arr = event.text.split('\\')
                            model_loc = file_arr[len(file_arr) - 2] + '/' + file_arr[len(file_arr) - 1]
                            view_obj(model_loc, display_surf)
            if mode == "main_menu":
                main_menu.update(time_delta)
            elif mode == "take_picture":
                take_picture.update(time_delta)
            elif mode == "view_prev_models":
                view_prev_models.update(time_delta)

                
        display_surf.fill((228,228,228))
        if mode == "main_menu":
            main_menu.process_events(event)
            #main_menu.update(time_delta)
            main_menu.draw_ui(display_surf)
        elif mode == "view_prev_models":
            view_prev_models.process_events(event)
            #view_prev_models.update(time_delta)
            view_prev_models.draw_ui(display_surf)
        elif mode == "take_picture":
            take_picture.process_events(event)
            if cam is not None:
                if not picture_taken:
                    image = cam.get_image()
                    currPicture = image
                    display_surf.blit(image, (0, 0))
                    display_surf.blit(pic_text, text_rect)
                    pygame.draw.rect(display_surf, (0,255,0), pygame.Rect((190,110), (256,256)), 2)
                else:
                    display_surf.blit(currPicture, (0,0))
            #main_menu.update(time_delta)
            take_picture.draw_ui(display_surf)
    
        pygame.display.update()



if __name__ == '__main__':
    main()
