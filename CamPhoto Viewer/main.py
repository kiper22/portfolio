import tkinter as tk
import cv2
from PIL import Image, ImageTk
import datetime
from photoviewer import PhotoViewer


class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.stream_on = True
        self.photoviewer_open = False
        self.window.title(window_title)
        self.PhotoViewer = PhotoViewer(self.window)
        self.create_menu()
        self.start_video()

        self.window.bind('<space>', lambda _: self.snapshot())
        self.window.bind("<Configure>", self.on_resize)

        self.delay = 15
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
        menubar.add_checkbutton(label="Turn On/Off", variable=tk.BooleanVar(value=True), command=self.toggle_stream)
        self.btn_snapshot=tk.Button(window, text="Snapshot", width=50, height=2, command=self.snapshot)
        self.btn_snapshot.pack(fill=tk.X)
        self.window.config(menu=menubar)
        
    def snapshot(self):
        ret, frame = self.vid.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            now = datetime.datetime.now()
            filename = "images\\" + now.strftime("%d%m%Y%H%M%S") + '.jpeg'
            img.save(f'{filename}')
            
            print(f'Saved {filename}')
    
    def update(self):
        if self.stream_on:
            ret, frame = self.vid.read()

            if ret:
                frame = cv2.resize(frame, (self.width, self.height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                self.photo = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                self.canvas.update()
        
        self.window.after(self.delay, self.update)
    
    def toggle_stream(self):
        self.stream_on = not self.stream_on
        if  self.stream_on:
            self.PhotoViewer.on_off = False
            self.PhotoViewer.active()
            self.start_video()
            self.btn_snapshot.config(state='normal')
            self.canvas.pack(fill=tk.BOTH, expand=True)
        else:
            self.btn_snapshot.config(state='disabled')
            self.canvas.delete('all')
            self.vid.release()
            self.canvas.pack_forget()
            self.PhotoViewer.on_off = True
            self.PhotoViewer.active()
            
        self.update()
    
    def on_resize(self, event):
        self.width = event.widget.winfo_width()
        self.height = event.widget.winfo_height()

window = tk.Tk()
app = CameraApp(window, "Tkinter Camera")
