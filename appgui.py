msg = "hi"
print(msg)
import tkinter as tk
from tkinter import filedialog, Text, PhotoImage
import os
from objloader import OBJ
import cv2
from PIL import Image, ImageTk
from gui_funcs import generateModel, cropImage

root = tk.Tk()
#images = []
filename = ""


welcomelabel = tk.Label(root, height=30 ,width = 60, padx = 5, text= "Please upload an image!\n You can take a live photo, or look at previous models")
welcomelabel.pack()


def uploadFile():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", 
                filetypes=(("jpegs", "*.jpg"), ("All Files","*.*")))
    #images.append(filename)
    print(filename)
    if filename:
        Image.open(filename).save("userphoto/userinput.jpg")

#Code to handle user photo upload
pic = 0
cam = cv2.VideoCapture(0)
pictureTaken = False

#if not cam.isOpened():  
#    print("Camera unable to open")
#    exit()

def takeSelfie():
    global pic
    pic = pic + 1

#welcome1label = tk.Label(root, height=30 ,width = 50, padx = 5, text= "Render model or choose a different image to upload!")
welcome1label = tk.Label(root, height=30 ,width = 50, padx = 5, text= "Render model or retake picture!")

def displayFrame():
    global welcomelabel
    global pictureTaken

    takePictureOn = takePic.winfo_exists()
    welcomelabel.configure(width = 600, height = 300)
    global pic
    s, frame = cam.read()
    if not s:
        print("Frame not working...")
    else:
        #openFile.pack_forget()
        openCam.pack_forget()
        takePic.pack(side="bottom")   
        cvImg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cvImg = cv2.rectangle(cvImg, (190,110), (450, 370), (0,255,0), 2) #256x256 box
        img = Image.fromarray(cvImg)
        tkimg = ImageTk.PhotoImage(image=img)
        welcomelabel.tkimg = tkimg
        welcomelabel.configure(image=tkimg)
        welcomelabel.after(10,displayFrame)
        
        if pic == 1:
            welcomelabel.configure(width = 30, height = 50, text= "Please upload an image! Then render model")
            img.save("userphoto/userinput.jpg")
            cv2.imshow("picture", frame)
            pic = pic-1
            cam.release()
            #cv2.destroyAllWindows()
            welcomelabel.pack_forget()
            openCam.pack_forget()
            takePic.pack_forget()
            openPrevModels.pack_forget()
            welcome1label.pack()
            view.pack(side="bottom")
            retakePic.pack(side="bottom")

def retakeSelfie():
    if not cam.isOpened():
        cam.open(0)
    welcome1label.pack_forget()
    view.pack_forget()
    retakePic.pack_forget()
    welcomelabel.pack()
    displayFrame()


def renderModel():
    cropImage()
    path = generateModel(imagePath = 'userphoto/userinput_cropped.jpg')
    os.system('viewobj.py ' + str(path))

def openModels():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", 
            filetypes=(("objs", "*.obj"), ("All Files","*.*")))
    filename_vals = filename.split('/')
    obj_fileloc = filename_vals[len(filename_vals) - 2] + '/' + filename_vals[len(filename_vals) - 1]
    os.system('viewobj.py ' + str(obj_fileloc))




#Pass file into DL model and obj into viewobj.py
##



#Button to run pygame 
view = tk.Button(root, text="Render model", padx=10, pady=5, fg="white", bg="grey", command=renderModel)
#view.pack(side="bottom")

#Button to open previous models
openPrevModels = tk.Button(root, text="Open previous models", padx=10, pady=5, fg="white", bg="#263D42", command=openModels)
openPrevModels.pack(side="bottom")

#Button to upload file
#openFile = tk.Button(root, text="Choose File", padx=10, pady=5, fg="white", bg="#263D42", command=uploadFile)
#openFile.pack(side="bottom") 

#button to take picture
takePic = tk.Button(root, text="Take picture!", padx=10, pady=5, fg="white", bg="#263D42", command=takeSelfie)
#takePic.pack(side="bottom")

#Button to retake picture
retakePic = tk.Button(root, text="Retake picture", padx=10, pady=5, fg="white", bg="#263D42", command=retakeSelfie)

#button to open camera
openCam = tk.Button(root, text="Open up camera", padx=10, pady=5, fg="white", bg="#263D42", command=displayFrame)
openCam.pack(side="bottom")


cv2.destroyAllWindows()
root.mainloop()