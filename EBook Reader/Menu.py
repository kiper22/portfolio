import tkinter as tk
from tkinter import ttk, StringVar
import ttkbootstrap as ttk
import os
from Settings import Settings
from BookPDF import BookPDF
from BookEPUB import BookEPUB


class PlaceholderEntry(ttk.Entry):
    def __init__(self, menu, placeholder=''):
        super().__init__(menu)

        self.menu = menu
        self.string_variable = StringVar()
        self.placeholder = placeholder
        self.config(textvariable=self.string_variable)
        self.config(width=50)

        # self.placeholder_color = 'gray'
        # self.default_color = 'black'

        self.insert('end', self.placeholder)
        # self['foreground'] = self.placeholder_color

        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)

    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, 'end')
            # self['foreground'] = self.default_color
            self.string_variable.trace('w', self.update_tree)
        self.bind('<KeyRelease>', self.update_tree)

    def update_tree(self, *args):
        path = self.menu.treeview_frame.get_treeview_heading_text()
        sv = self.string_variable.get().lower()
        self.menu.update_treeview(path, sv)

    def on_focus_out(self, event):
        if self.get() == self.placeholder:
            self.insert('end', self.placeholder)
            # self['foreground'] = self.placeholder_color
        else:
            # self['foreground'] = self.default_color
            sv = self.string_variable.get().lower()
            if sv and sv != self.placeholder.lower():
                path = self.menu.treeview_frame.get_treeview_heading_text()
                self.menu.update_treeview(path, sv)


class TreeviewFrame(ttk.Frame):
    def __init__(self, parent, menu):
        super().__init__(parent)
        self.place(x=0, rely=0.15, relwidth=0.3, relheight=0.85)

        self.menu = menu
        self.settings = self.menu.settings
        self.path = self.settings.path_

        self.create_widgets()

        self.tree.bind('<Double-Button-1>', self.open_book)
        self.tree.bind('<Return>', self.open_book)

    def create_widgets(self):
        # create widgets
        self.tree = ttk.Treeview(self)
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text=self.path, anchor='w')

        # create the grid
        self.columnconfigure((0), weight=1, uniform='t')
        self.rowconfigure((0), weight=1, uniform='t')

        # place widgets
        self.tree.grid(row=0, column=0, sticky='nswe')
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')

    def open_book(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_path = ""
            item = selected_item[0]  # Take only 1st marked element
            while item != "":
                item_text = self.tree.item(item)['text']
                item_path = os.path.join(item_text, item_path)
                item = self.tree.parent(item)
            item_path = item_path.rstrip("\\")  # path looks like "C\...file.pdf\""
            print('otwarto: ', item_path)
            self.settings.update('section_file', 'last_book', item_path)
            if self.menu.winfo_toplevel().book_panel.book_epub is not None:
                self.menu.winfo_toplevel().book_panel.book_epub.destroy()
            if self.menu.winfo_toplevel().book_panel.book_pdf is not None:
                self.menu.winfo_toplevel().book_panel.book_pdf.destroy()
            if item_path.endswith('.pdf'):
                self.menu.winfo_toplevel().book_panel.set_book_pdf(
                    BookPDF(self.menu.winfo_toplevel(), item_path, self.menu.settings))
            elif item_path.endswith('.epub'):
                self.menu.winfo_toplevel().book_panel.set_book_epub(
                    BookEPUB(self.menu.winfo_toplevel(), item_path, self.menu.settings))

    def process_directory(self, parent, path, string_variable=''):
        print(string_variable, 'process directory')
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            if not isdir:
                file_name = p.lower()
                if string_variable in file_name:
                    if p.lower().endswith('.pdf') and self.menu.pdf_variable.get():
                        self.tree.insert(parent, 'end', text=p)
                    if p.lower().endswith('.epub') and self.menu.epub_variable.get():
                        self.tree.insert(parent, 'end', text=p)
            if isdir:
                oid = self.tree.insert(parent, 'end', text=p, open=True)
                self.process_directory(oid, abspath, string_variable)

    def update_treeview(self, folder_path, sv=''):
        self.path = folder_path
        self.tree.delete(*self.tree.get_children())
        self.tree.heading('#0', text=self.path, anchor='w')
        abspath = os.path.abspath(self.path)
        root_node = self.tree.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath, sv)

    def get_treeview_heading_text(self):
        return self.tree.heading('#0', 'text')


class Menu(ttk.Frame):
    def __init__(self, parent, search, settings):
        super().__init__(parent)
        self.place(relx=0, rely=0.05, relwidth=0.3, relheight=0.10)

        self.settings = settings
        self.folder_path = self.settings.path_
        self.search = search

        self.pdf_variable = tk.BooleanVar(value=True)
        self.epub_variable = tk.BooleanVar(value=True)
        self.treeview_frame = TreeviewFrame(parent, self)

        self.create_widgets()
        self.update_treeview(self.folder_path)

    def create_widgets(self):
        # create widgets
        menu_toggle1 = ttk.Checkbutton(self, text='PDF', variable=self.pdf_variable,
                                       command=lambda: self.update_treeview(self.treeview_frame.get_treeview_heading_text()))
        menu_toggle2 = ttk.Checkbutton(self, text='EPUB', variable=self.epub_variable,
                                       command=lambda: self.update_treeview(self.treeview_frame.get_treeview_heading_text()))
        entry = PlaceholderEntry(self, placeholder='search')

        # create the grid
        self.columnconfigure((0, 1), weight=1, uniform='m')
        self.rowconfigure((0, 1), weight=1, uniform='m')

        # place widgets
        entry.grid(column=0, row=1, columnspan=2)
        menu_toggle1.grid(column=0, row=0)
        menu_toggle2.grid(column=1, row=0)

    def update_treeview(self, path, string_variable=''):
        self.folder_path = path
        self.treeview_frame.update_treeview(self.folder_path, string_variable)
