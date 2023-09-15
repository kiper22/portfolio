
######## plik App.py
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from SearchLibrary import *
from Menu import *
from BookPanel import *
from Settings import *
from Audio import *


class App(tk.Tk):
    def set_theme(self):
            ttk.Style().theme_use(self.settings.theme)
    
    def __init__(self, title, size):
        # main setup
        super().__init__()
        self.title(title)
        self.state('zoomed')
        
        # width= self.winfo_screenwidth()
        # height= self.winfo_screenheight()
        
        self.minsize(size[0], size[1])

        self.settings = Settings(self)
        self.style = ttk.Style()
        self.style = self.style.theme_use(self.settings.theme)
        
        # self.audio = Audio(self.settings)
        self.search = None
        self.menu = Menu(self, self.search, self.settings)
        self.search = SearchLibrary(self, self.menu, self.settings)
        self.book_panel = BookPanel(self, self.settings)

        # run
        self.mainloop()


App('Class based app', (600,600))
