# Copyright (c) 2023, Kacper Wieleba
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for private, non-commercial purposes only, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import tkinter as tk
from PIL import Image, ImageTk
import os
import cv2


class PhotoViewer:
    def __init__(self, window):
        self.window = window
        self.img_canvas = None
        self.image_list = None
        self.on_off = True
        
    def active(self):
        if self.on_off:

            self.get_img()
            self.start_display()
            self.display_image()

            self.window.bind("<a>", lambda _: self.change_image(-1))
            self.window.bind("<d>", lambda _: self.change_image(1))
            self.window.bind("<f>", lambda _: self.detect_faces())
            self.window.bind("<BackSpace>", lambda _: self.delate_photo())
            
            self.window.mainloop()
            
        else:
            self.quit_display()
        
    def get_img(self):
        self.image_list = []
        self.current_image_index = 0
        for filename in os.listdir("images"):
            if filename.endswith(".jpeg"):
                self.image_list.append(os.path.join("images", filename))
    
    def start_display(self):
        self.img_canvas = tk.Canvas(self.window, width=800, height=600)
        self.img_canvas.pack()
    
    def display_image(self):
        if not self.image_list:
            self.img_canvas.create_text(400, 300, text="No images found!", fill="red", font=("Arial", 24))
            return
        
        self.img = Image.open(self.image_list[self.current_image_index])
        self.img = self.img.resize((800, 600), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)
        self.img_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def change_image(self, delta):
        self.current_image_index = (self.current_image_index + delta) % len(self.image_list)
        self.display_image()
    
    def delate_photo(self):
        if self.image_list:
            os.remove(self.image_list[self.current_image_index])
            self.image_list.pop(self.current_image_index)
            self.current_image_index = min(self.current_image_index, len(self.image_list) - 1)
            self.display_image()
        else:
            self.img_canvas.create_text(400, 300, text="No images found!", fill="red", font=("Arial", 24))

    def detect_faces(self):
        self.img = cv2.imread(self.image_list[self.current_image_index])
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)

        for (x, y, w, h) in faces:
            self.img_canvas.create_rectangle(x, y, x + w, y + h, outline="red")
            self.img_canvas.update()
    
    def quit_display(self):
        self.img_canvas.pack_forget()
        if self.img_canvas != None:
            self.img_canvas.delete('all')
        if self.image_list != None:
            self.image_list.clear()
