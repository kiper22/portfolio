
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
    def __init__(self, title, size):
        # main setup
        super().__init__()
        self.title(title)
        self.state('zoomed')
        
        # width= self.winfo_screenwidth()
        # height= self.winfo_screenheight()
        # #setting tkinter window size
        # self.geometry("%dx%d" % (width, height))
        
        # self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # ttkbootstrap theme
        style = ttk.Style()
        style.theme_use('darkly')

        # widgets
        
        # przekazać settings do odpowiednich klas !!!
        self.settings = Settings()
        self.search = None
        self.menu = Menu(self, self.search, self.settings)
        self.search = SearchLibrary(self, self.menu, self.settings)
        self.book_panel = BookPanel(self, self.settings)

        # run
        self.mainloop()


App('Class based app', (600,600))
