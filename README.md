# myAvatar

Face3D and model by Yao Feng:

- https://github.com/YadiraF/PRNet

- https://github.com/YadiraF/face3d

Training based on:

- https://openaccess.thecvf.com/content_ECCV_2018/papers/Yao_Feng_Joint_3D_Face_ECCV_2018_paper.pdf

Datasets used:

 - 300W-LP and AFLW2000-3D: http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm


Requires the following packages:
- Tensorflow <= 1.4.0
- Pygame 1.9.6
- Pygame GUI 0.6.0
- Pyimgui 1.3.0
- PyOpenGL

And Python 3.5/3.6.

More details can be found [on my website](https://jordibardia.github.io).

Executable coming soon.

## Instructions
The application requires a model to run. The original author's model can be downloaded from [here](https://drive.google.com/file/d/1UoE-XuW1SDLUjZmJPkIZ1MLxvQFgmTFH/view?usp=sharing) and the one I trained for my class [here](https://drive.google.com/file/d/13ZHCaBC8rVgGq1i0U0YKztMJAAqejOVQ/view?usp=sharing). The model must be placed in a folder called <code>saved_models</code>. I currently have the default model set to be that of the original author's.

To run the application, run this command in the terminal:

    python appgui.py
    

You can run the view object program separately by running the command:

    python viewobj.py [filename]