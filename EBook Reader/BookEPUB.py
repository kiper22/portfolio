import ebooklib
from ebooklib import epub
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import scrolledtext
from bs4 import BeautifulSoup


class BookEPUB(ttk.Frame):
    def __init__(self, parent, file_path, settings):
        super().__init__(parent)
        self.place(relx=0.3, rely=0.05, relwidth=0.7, relheight=0.9)
        self.settings = settings
        self.file_path = file_path
        self.pages = []
        self.current_page = 0
        self.formatted_text = ''
        self.create_widgets()
        self.read_epub()

    def create_widgets(self):
        self.text = tk.Text(self, wrap=tk.WORD, font=('Calibri', 12))
        self.text.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.show_page()

    def format_text(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        paragraphs = soup.find_all('p')
        formatted_text = '\n\n'.join([p.get_text() for p in paragraphs])
        return formatted_text

    def create_pages(self, text):
        pages = []
        lines_per_page = 40
        chars_per_line = 170
        text_fragments = text.split('\n')
        fragment = 0

        while fragment < len(text_fragments):
            current_page = ''
            for _ in range(lines_per_page):
                if fragment >= len(text_fragments):
                    break

                if len(text_fragments[fragment]) <= chars_per_line:
                    line = text_fragments[fragment]
                    fragment += 1
                elif len(text_fragments[fragment]) > chars_per_line:
                    last_space = text_fragments[fragment].rfind(' ', 0, chars_per_line + 1)
                    last_coma = text_fragments[fragment].rfind(',', 0, chars_per_line + 1)
                    last_period = text_fragments[fragment].rfind('.', 0, chars_per_line + 1)
                    last_break = max(last_space, last_coma, last_period)

                    line = text_fragments[fragment][:last_break]
                    text_fragments[fragment] = text_fragments[fragment][last_break:]

                current_page += line + '\n'

            pages.append(current_page)

        return pages

    def show_page(self):
        if 0 <= self.current_page < len(self.pages):
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, self.pages[self.current_page])

    def read_epub(self):
        book = epub.read_epub(self.file_path)
        text = ""
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                text += item.get_content().decode('utf-8')
        self.formatted_text = self.format_text(text)

        self.pages = self.create_pages(self.formatted_text)

        self.text.insert(tk.END, self.pages[self.current_page])
    
    def return_text(self):
        return str(self.pages[self.current_page])

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_page()
