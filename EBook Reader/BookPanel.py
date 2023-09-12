import fitz
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from BookPDF import BookPDF
from BookEPUB import BookEPUB
from Settings import *


class BookPanel(ttk.Frame):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.place(relx=0.3, rely=0.95, relwidth=0.7, relheight=0.05)

        self.book_pdf = None
        self.book_epub = None
        self.settings = settings

        self.create_widgets()

    def create_widgets(self):
        button_left = ttk.Button(self, text='Prev. page', command=self.previous_page)
        button_settings = ttk.Button(self, text='Settings', command=self.open_settings)
        button_audiobook = ttk.Button(self, text='Audio')
        button_right = ttk.Button(self, text='Next page', command=self.next_page)

        self.set_icons(button_left, 'icons/arrow_left.png')
        self.set_icons(button_right, 'icons/arrow_right.png')
        self.set_icons(button_settings, 'icons/settings.png')
        self.set_icons(button_audiobook, 'icons/speaker_disable.png')

        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='b')

        button_left.grid(row=1, column=0, sticky='nswe')
        button_settings.grid(row=1, column=1, sticky='nswe')
        button_audiobook.grid(row=1, column=2, sticky='nswe')
        button_right.grid(row=1, column=3, sticky='nswe')

    def set_icons(self, button, icon_path):
        photo = ImageTk.PhotoImage(Image.open(icon_path))
        button.configure(image=photo)
        button.image = photo

    def set_book_pdf(self, book_pdf):
        self.book_epub = None
        self.book_pdf = book_pdf

    def set_book_epub(self, book_epub):
        self.book_pdf = None
        self.book_epub = book_epub

    def previous_page(self):
        if self.book_pdf:
            self.book_pdf.previous_page()
        elif self.book_epub:
            self.book_epub.previous_page()

    def next_page(self):
        if self.book_pdf:
            self.book_pdf.next_page()
        elif self.book_epub:
            self.book_epub.next_page()
    
    def open_settings(self):
        self.settings.settings_window()
