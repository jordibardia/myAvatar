msg = "hi"
print(msg)
import tkinter as tk
from tkinter import filedialog, Text, PhotoImage
import os
from objloader import OBJ

root = tk.Tk()
images = []
filename = ""

def uploadFile():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", 
                filetypes=(("objects", "*.obj"), ("All Files","*.*")))
    images.append(filename)
    print(filename)

#function to run pygame window
def renderModel():
    os.system('viewobj.py')



welcomelabel = tk.Label(root, height=30 ,width = 50, padx = 5, text= "Please upload an image!")
welcomelabel.pack()

#Button to upload file
openFile = tk.Button(root, text="Choose File", padx=10, pady=5, fg="white", bg="#263D42", command=uploadFile)
openFile.pack() 

print(filename)

#Pass file into DL model and obj into viewobj.py
##

#Button to run pygame 
view = tk.Button(root, text="Render model", padx=10, pady=5, fg="white", bg="grey", command=renderModel)
view.pack()




root.mainloop()
