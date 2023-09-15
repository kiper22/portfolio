#### Settings.py
from configparser import ConfigParser
import os
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

class Settings():
    def __init__(self, master, book_pdf = None):
        self.master = master
        self.book_pdf = book_pdf
        self.window = None
        self.config = ConfigParser()
        self.config.read('StartingValues.ini')
        self.read_settings()
        self.update('section_file', 'text', '')
        self.update('section_file', 'book_current_page', '0')

    def read_settings(self):
        # Odczytujemy wartości z pliku
        self.path_ = self.config.get('section_file', 'path_')
        self.last_book = self.config.get('section_file', 'last_book')
        self.pdf_pages = self.config.getint('section_file', 'pdf_pages')
        self.pdf_zoom = self.config.getfloat('section_file', 'pdf_zoom')

        self.rate = self.config.getint('section_audio', 'rate')
        self.language = self.config.get('section_audio', 'language')
        self.volume = self.config.getfloat('section_audio', 'volume')
        
        self.theme = self.config.get('section_theme', 'theme')
    
    def update(self, section, variable, new_value):
        self.config.set(section, variable, new_value)
        
        with open('StartingValues.ini', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        
        self.read_settings()

    def settings_window(self):
        self.window = tk.Toplevel()
        self.window.title('Settings')
        self.window.geometry('500x400')
        self.current_spinbox_index = 0
        self.spinboxes = []
        
        self.window.columnconfigure((0, 1), weight=2, uniform='s')
        self.window.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='s')
        self.window.columnconfigure(1, weight=3)
        
        # File section
        self.label_path = tk.Label(self.window, text=f'Path: ')
        self.label_path_respond = tk.Label(self.window, text=f'{self.path_}')
        self.label_last_book = tk.Label(self.window, text=f'Last opened book: ')
        book = self.last_book.split('\\')[-1]
        self.label_last_book_respond = tk.Label(self.window, text=f'{book}')
        
        self.label_pdf_pages = tk.Label(self.window, text=f'Number of shown pdf pages: ')
        self.spinbox_pdf_pages = tk.Spinbox(self.window, from_=1, to=2, command=self.on_pdf_pages_change)
        self.spinbox_pdf_pages.delete(0, 'end')
        self.spinbox_pdf_pages.insert(0, int(self.pdf_pages))
        self.spinboxes.append(self.spinbox_pdf_pages)
        
        self.label_pdf_zoom = tk.Label(self.window, text='PDF zoom:')
        self.spinbox_pdf_zoom = tk.Spinbox(self.window, from_=50, to=150, command=self.on_zoom_change)
        self.spinbox_pdf_zoom.delete(0, 'end')
        self.spinbox_pdf_zoom.insert(0, int(self.pdf_zoom*100))
        self.spinboxes.append(self.spinbox_pdf_zoom)
        
        self.label_path.grid(column=0, row=0)
        self.label_path_respond.grid(column=1, row=0)
        self.label_last_book.grid(column=0, row=1)
        self.label_last_book_respond.grid(column=1, row=1)
        self.label_pdf_pages.grid(column=0, row=2)
        self.spinbox_pdf_pages.grid(column=1, row=2)
        self.label_pdf_zoom.grid(column=0, row=3)
        self.spinbox_pdf_zoom.grid(column=1, row=3)
    
        # Audio section
        self.label_volume = tk.Label(self.window, text='Volume:')
        self.spinbox_volume = tk.Spinbox(self.window, from_=0, to=100, command=self.on_volume_change)
        self.spinbox_volume.delete(0, 'end')
        self.spinbox_volume.insert(0, int(self.volume*100))
        self.spinboxes.append(self.spinbox_volume)

        self.label_rate = tk.Label(self.window, text='Rate:')
        self.spinbox_rate = tk.Spinbox(self.window, from_=50, to=200, command=self.on_rate_change)
        self.spinbox_rate.delete(0, 'end')
        self.spinbox_rate.insert(0, int(self.rate))
        self.spinboxes.append(self.spinbox_rate)
        
        self.label_language = tk.Label(self.window, text='Language:')
        self.language_var = tk.StringVar()
        self.language_var.set(str(self.language))
        self.spinbox_language = tk.Spinbox(self.window, values=('Polski', 'English'), textvariable=self.language_var, command=self.on_language_change)
        self.spinboxes.append(self.spinbox_language)
        
        self.label_volume.grid(column=0, row=4)
        self.spinbox_volume.grid(column=1, row=4)
        self.label_rate.grid(column=0, row=5)
        self.spinbox_rate.grid(column=1, row=5)
        self.label_language.grid(column=0, row=6)
        self.spinbox_language.grid(column=1, row=6)
        
        # themes
        self.label_theme = tk.Label(self.window, text='Theme:')
        self.theme_var = tk.StringVar()
        self.theme_var.set(str(self.theme))
        self.spinbox_theme = tk.Spinbox(self.window, values=ttk.Style().theme_names(), textvariable=self.theme_var, command=self.on_theme_change)
        self.spinboxes.append(self.spinbox_theme)
        
        self.label_theme.grid(column=0, row=7)
        self.spinbox_theme.grid(column=1, row=7)
        
        # selecting spinboxes
        self.spinboxes[self.current_spinbox_index].focus_set()
        self.window.bind('<Left>', self.on_left_arrow)
        self.window.bind('<Right>', self.on_right_arrow)
        
    def on_left_arrow(self, event):
        if self.current_spinbox_index > 0:
            self.current_spinbox_index -= 1
            self.spinboxes[self.current_spinbox_index].focus_set()

    def on_right_arrow(self, event):
        if self.current_spinbox_index < len(self.spinboxes) - 1:
            self.current_spinbox_index += 1
            self.spinboxes[self.current_spinbox_index].focus_set()
    
    def on_num_pages_change(self, value):
        pass
    
    def on_volume_change(self):
        value = self.spinbox_volume.get()
        value = str(float(float(value)/100))
        self.update('section_audio', 'volume', value)

    def on_rate_change(self):
        value = self.spinbox_rate.get()
        self.update('section_audio', 'rate', value)

    def on_language_change(self):
        selected_language = self.spinbox_language.get()
        self.update('section_audio', 'language', selected_language)    
    
    def on_zoom_change(self):
        value = self.spinbox_pdf_zoom.get()
        value = str(float(value) / 100)
        self.update('section_file', 'pdf_zoom', value)
    
    def on_pdf_pages_change(self):
        value = self.spinbox_pdf_pages.get()
        self.update('section_file', 'pdf_pages', value)
    
    def on_theme_change(self):
        value = self.spinbox_theme.get()
        self.update('section_theme', 'theme', value)
        self.master.set_theme()
    
