#### Settings.py
from configparser import ConfigParser
import os
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

class Settings():
    def __init__(self, book_pdf = None):
        self.book_pdf = book_pdf
        self.window = None
        self.config = ConfigParser()
        self.config.read('StartingValues.ini')
        
        self.read_settings()

    def read_settings(self):
        # Odczytujemy wartości z pliku
        self.path_ = self.config.get('section_file', 'path_')
        self.last_book = self.config.get('section_file', 'last_book')
        self.pdf_pages = self.config.getint('section_file', 'pdf_pages')
        self.pdf_zoom = self.config.getfloat('section_file', 'pdf_zoom')

        self.rate = self.config.getint('section_audio', 'rate')
        self.language = self.config.get('section_audio', 'language')
        self.volume = self.config.getfloat('section_audio', 'volume')
    
    def update(self, section, variable, new_value):
        self.config.set(section, variable, new_value)
        
        with open('StartingValues.ini', 'w') as configfile:
            self.config.write(configfile)
        
        self.read_settings()

    def settings_window(self):
        self.window = tk.Toplevel()
        self.window.title('Settings')
        self.window.geometry('500x400')
        
        self.window.columnconfigure((0, 1), weight=1, uniform='s')
        self.window.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='s')
        self.window.columnconfigure(1, weight=3)
        
        # File section
        self.label_path = tk.Label(self.window, text=f'Path: ')
        self.label_path_respond = tk.Label(self.window, text=f'{self.path_}')
        self.label_last_book = tk.Label(self.window, text=f'Last opened book: ')
        book = self.last_book.split('\\')[-1]
        self.label_last_book_respond = tk.Label(self.window, text=f'{book}')
        self.label_pdf_pages = tk.Label(self.window, text=f'Number of shown pdf pages: ')
        self.label_pdf_pages_respond = tk.Label(self.window, text=f'{self.pdf_pages}')
        self.label_pdf_zoom = tk.Label(self.window, text='PDF zoom:')
        self.slider_pdf_zoom = tk.Scale(self.window, from_=5, to=15, orient='horizontal', command=self.on_zoom_change)
        self.slider_pdf_zoom.set(self.pdf_zoom * 10)
        
        self.label_path.grid(column=0, row=0)
        self.label_path_respond.grid(column=1, row=0)
        self.label_last_book.grid(column=0, row=1)
        self.label_last_book_respond.grid(column=1, row=1)
        self.label_pdf_pages.grid(column=0, row=2)
        self.label_pdf_pages_respond.grid(column=1, row=2)
        self.label_pdf_zoom.grid(column=0, row=3)
        self.slider_pdf_zoom.grid(column=1, row=3)
    
        # Audio section
        self.label_volume = tk.Label(self.window, text='Volume:')
        self.label_volume.grid(column=0, row=4)
        self.slider_volume = tk.Scale(self.window, from_=0, to=100, orient='horizontal', command=self.on_volume_change)
        self.slider_volume.set(self.volume * 100)
        self.slider_volume.grid(column=1, row=4)

        self.label_rate = tk.Label(self.window, text='Rate:')
        self.label_rate.grid(column=0, row=5)
        self.slider_rate = tk.Scale(self.window, from_=50, to=200, orient='horizontal', command=self.on_rate_change)
        self.slider_rate.set(self.rate)
        self.slider_rate.grid(column=1, row=5)
        
        self.label_language = tk.Label(self.window, text='Language:')
        self.label_language.grid(column=0, row=6)
        # voices = self.get_available_voices()
        self.combobox_language = ttk.Combobox(self.window) #values=voices)
        self.combobox_language.set(self.language)
        self.combobox_language.grid(column=1, row=6)
        self.combobox_language.bind("<<ComboboxSelected>>", self.on_language_change)
    
    def on_volume_change(self, value):
        value = str(float(float(value)/100))
        self.update('section_audio', 'volume', value)

    def on_rate_change(self, value):
        self.update('section_audio', 'rate', value)

    def on_language_change(self, event):
        selected_language = self.combobox_language.get()
        self.update('section_audio', 'language', selected_language)

    # def get_available_voices(self):
    #     # Ta metoda może zostać wywołana przez combobox, aby pobrać dostępne języki z klasy Audio
    #     audio = Audio()
    #     voices = audio.engine.getProperty('voices')
    #     return [voice.id for voice in voices]        
    
    def on_zoom_change(self, value):
        value = str(float(value) / 10)
        self.update('section_file', 'pdf_zoom', value)
