########## plik Search.py
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import filedialog
from Menu import TreeviewFrame
from Settings import *

class SearchLibrary(ttk.Frame):
    def __init__(self, parent, menu, settings):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=0.05)

        self.menu = menu
        self.settings = settings
        self.folder_path = self.settings.path_
        self.create_widgets()

    def create_widgets(self):
        # create the widgets
        self.menu_button = ttk.Button(self, text=self.folder_path, command=self.browse_button)

        # create the grid
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.columnconfigure(1, weight=4)
        self.rowconfigure((0), weight=1, uniform='a')

        # place the widgets
        self.menu_button.grid(row=0, column=1, sticky='nswe')

    def browse_button(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.folder_path = selected_directory
            self.menu_button.configure(text=self.folder_path)
            self.menu.update_treeview(self.folder_path)
            self.settings.update('section_file', 'path_', self.folder_path)
