import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()
images = []

def uploadFile():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", 
                filetypes=(("jpegs", "*.jpg"), ("All Files","*.*")))
    images.append(filename)
    print(filename)

#canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
#canvas.pack()

welcomelabel = tk.Label(root, height=30 ,width = 50, padx = 10, text= "Please upload an image!")
welcomelabel.pack()

#root.filename = filedialog.askopenfilename(initialdir="/images", title="Select a file", filetypes=(("all file type","*.*")))
openFile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#263D42", command=uploadFile)
openFile.pack()


root.mainloop()