# Copyright 2023 Kacper Wieleba
# Licensed under the MIT License.

# This code is responsible for recognizing people using the camera 
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
import cv2 as cv
import numpy as np
import os
from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder
import pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class CameraApp:
    def __init__(self, window, window_title):
        self.yolo_model = YOLO(r'best.pt')
        self.window = window
        self.window_title = window_title

        self.window.title(window_title)
        self.create_menu()
        self.start_video()
        self.facenet = FaceNet()
        self.faces_embeddings = np.load(r'faces_embeddings_50celebs.npz')
        self.Y = self.faces_embeddings['arr_1']
        self.encoder = LabelEncoder().fit(self.Y)
        self.model = pickle.load(open(r'svm_model_160x160_50celebs.pkl', 'rb'))

        self.window.bind("<Configure>", self.on_resize)

        self.delay = 5
        self.update()
        self.window.mainloop()
    
    def start_video(self):
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
    
    def create_menu(self):
        menubar = tk.Menu(self.window)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.window.config(menu=menubar)
    
    def update(self):
        ret, frame = self.vid.read()

        if ret:
            self.frame_count += 1
                
            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            yolo_results = self.yolo_model.predict(frame)
            frame_with_faces = self.draw_faces(frame, yolo_results)

            img = Image.fromarray(frame_with_faces)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.canvas.update()
            
                
        self.window.after(self.delay, self.update)

    def draw_faces(self, frame, yolo_results):
        rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        for result in yolo_results:
            boxes = result.boxes
            for box in boxes:
                tlx = int(box.xyxy.tolist()[0][0])
                tly = int(box.xyxy.tolist()[0][1])
                brx = int(box.xyxy.tolist()[0][2])
                bry = int(box.xyxy.tolist()[0][3])

                img = rgb_img[tly:bry, tlx:brx]
                img = cv.resize(img, (160, 160))
                img = np.expand_dims(img, axis=0)

                ypred = self.facenet.embeddings(img)

                face_name = self.model.predict(ypred)
                final_name = self.encoder.inverse_transform(face_name)[0]

                yhat_prob = self.model.predict_proba(ypred)
                class_index = face_name[0]
                class_probability = yhat_prob[0, class_index] * 100
                predict_names = self.encoder.inverse_transform(face_name)
                
                final_name = predict_names[0]
                cv.rectangle(frame, (tlx, tly), (brx, bry), (255, 0, 255), 10)
                cv.putText(frame, f"{final_name} ({class_probability:.2f}%)", (tlx, tly - 10),
                        cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv.LINE_AA)
        return frame
    
    def on_resize(self, event):
        self.width = event.widget.winfo_width()
        self.height = event.widget.winfo_height()

window = tk.Tk()
app = CameraApp(window, "YOLO face identification")