#### BookPDF.py
import fitz
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from Settings import *


class BookPDF(ttk.Frame):
    def __init__(self, parent, file_path, settings):
        super().__init__(parent)
        self.place(relx = 0.3, rely = 0.05, relwidth = 0.7, relheight = 0.9)
        self.file_name = file_path
        self.settings = settings
        self.text = ''
        self.zoom = self.settings.pdf_zoom
        self.doc = fitz.open(self.file_name)
        self.mat = fitz.Matrix(self.zoom, self.zoom)
        self.num_pages = len(self.doc)
        self.current_page = 0
        
        self.create_widgets()
        self.show_page()
    
    def create_widgets(self):
        self.canvas_list = []
        for i in range(self.settings.pdf_pages):
            # Create a frame to hold each canvas
            frame = ttk.Frame(self)
            frame.pack(side='left', fill='both', expand=1)

            # Create canvas
            canvas = ttk.Canvas(frame)
            canvas.pack(side='left', fill='both', expand=1)
            self.canvas_list.append(canvas)
    
    def pdf_to_img(self, page_num): # gets text too but commented
        page = self.doc.load_page(page_num)
        pix = page.get_pixmap(matrix=self.mat)
        self.text = page.get_text('text')
        return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    def show_page(self):
        for page_num, canvas in enumerate(self.canvas_list):
            try:
                assert 0 <= self.current_page < self.num_pages
                im = self.pdf_to_img(self.current_page + page_num)
                img_tk = ImageTk.PhotoImage(im)
                frame = ttk.Frame(canvas)
                panel = ttk.Label(frame, image=img_tk)
                panel.pack(side="bottom", fill="both", expand="yes")
                frame.image = img_tk
                canvas.create_window(0, 0, anchor='nw', window=frame)
                frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
            except Exception as e:
                print("Error:", e)
    
    def update_pdf_settings(self): # nie jest uruchamiana
        print('Settings updated')
        print(f'Zoom before: {self.zoom}')
        self.zoom = self.settings.pdf_zoom
        print(f'Zoom after: {self.zoom}')
        self.mat = fitz.Matrix(self.zoom, self.zoom)
        self.show_page()
    
    def return_text(self):
        return self.text
    
    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def next_page(self):
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.show_page()
